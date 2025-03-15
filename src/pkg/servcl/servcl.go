package servcl

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net/http"
	"strconv"
	"strings"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/propagation"

	"revproxy/pkg/tracer"
)

type Proxy struct{}

const (
	proxyPort   = 11095
	servicePort = 8080
)

func ForwardRequest(req *http.Request) (*http.Response, time.Duration, error) {
	ctx, span, startTime := tracer.StartSpanWithVNFInfo(req.Context(), req)
	defer span.End()

	// Construct destination URL
	incUrl := fmt.Sprintf("http://%s%s", req.Host, req.RequestURI)
	intUrl := strings.Replace(incUrl, strconv.Itoa(proxyPort), strconv.Itoa(servicePort), 1)

	// Read request body safely
	bodyBytes, err := io.ReadAll(req.Body)
	if err != nil {
		span.RecordError(err)
		return nil, 0, fmt.Errorf("failed to read request body: %w", err)
	}
	req.Body.Close()
	rdr1 := io.NopCloser(bytes.NewBuffer(bodyBytes))

	log.Printf("Incoming URL: %s | Forward URL: %s | Method: %s", incUrl, intUrl, req.Method)

	// Create a new proxied request
	proxyReq, err := http.NewRequestWithContext(ctx, req.Method, intUrl, rdr1)
	if err != nil {
		span.RecordError(err)
		return nil, 0, fmt.Errorf("failed to create proxy request: %w", err)
	}

	// Forward headers
	for key, values := range req.Header {
		for _, value := range values {
			proxyReq.Header.Add(key, value)
		}
	}

	// Set trace context in headers
	otel.GetTextMapPropagator().Inject(ctx, propagation.HeaderCarrier(proxyReq.Header))

	// Make the request
	start := time.Now()
	httpClient := http.Client{}
	res, err := httpClient.Do(proxyReq)
	duration := time.Since(start)

	if err != nil {
		span.RecordError(err)
		return nil, 0, fmt.Errorf("failed to forward request: %w", err)
	}

	// Total request processing time (including proxy forwarding)
	totalDuration := time.Since(startTime)

	// Log the duration in OpenTelemetry
	span.SetAttributes(
		attribute.Float64("request.forwarding_duration_ms", float64(duration.Milliseconds())),
		attribute.Float64("request.total_duration_ms", float64(totalDuration.Milliseconds())),
	)

	return res, duration, nil
}

func WriteResponse(w http.ResponseWriter, res *http.Response) {
	// Copy all the header values from the response.
	for name, values := range res.Header {
		w.Header()[name] = values
	}

	// Set a special header to notify that the proxy actually serviced the request.
	w.Header().Set("Server", "amazing-proxy")

	// Set the status code returned by the destination service.
	w.WriteHeader(res.StatusCode)

	// Copy the contents from the response body.
	io.Copy(w, res.Body)

	// Finish the request.
	res.Body.Close()
}

func PrintStats(req *http.Request, res *http.Response, duration time.Duration) {
	fmt.Printf("Request Duration: %v\n", duration)
	fmt.Printf("Request Size: %d\n", req.ContentLength)
	fmt.Printf("Response Size: %d\n", res.ContentLength)
	fmt.Printf("Response Status: %d\n\n", res.StatusCode)
}
