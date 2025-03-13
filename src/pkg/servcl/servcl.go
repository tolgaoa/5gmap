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

	"revproxy/pkg/configParser"
	"revproxy/pkg/tracer"

	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/trace"
)

var cfg = configParser.LoadConfig()
var propagator = propagation.TraceContext{} // OpenTelemetry propagator

// ForwardRequest forwards requests while preserving trace context
func ForwardRequest(req *http.Request) (*http.Response, time.Duration, error) {
	// Start tracing and update the request context
	ctx, span, startTime := tracer.StartSpanWithVNFInfo(req.Context(), req)
	defer span.End()
	req = req.WithContext(ctx)

	// Construct target URL
	incUrl := fmt.Sprintf("http://%s%s", req.Host, req.RequestURI)
	intUrl := strings.Replace(incUrl, strconv.Itoa(cfg.ProxyPort), strconv.Itoa(cfg.ServicePort), 1)

	// Read request body
	bodyBytes, err := io.ReadAll(req.Body)
	if err != nil {
		log.Printf("Error reading request body: %v", err)
		span.SetAttributes(attribute.String("error", "Failed to read request body"))
		span.AddEvent("Request failed", trace.WithAttributes(attribute.String("error", err.Error())))
		return nil, 0, err
	}
	req.Body = io.NopCloser(bytes.NewBuffer(bodyBytes)) // Restore request body

	// Create a new HTTP request
	proxyReq, err := http.NewRequestWithContext(ctx, req.Method, intUrl, bytes.NewReader(bodyBytes))
	if err != nil {
		log.Printf("Error creating proxy request: %v", err)
		span.SetAttributes(attribute.String("error", "Failed to create proxy request"))
		span.AddEvent("Proxy request creation failed", trace.WithAttributes(attribute.String("error", err.Error())))
		return nil, 0, err
	}

	// Copy headers and inject trace context
	for name, values := range req.Header {
		for _, value := range values {
			proxyReq.Header.Add(name, value)
		}
	}
	propagator.Inject(ctx, propagation.HeaderCarrier(proxyReq.Header)) // Inject trace context

	// Add network slice and location info
	proxyReq.Header.Set("X-Network-Slice-ID", cfg.NetworkSliceID)
	proxyReq.Header.Set("X-Location-ID", cfg.LocationID)

	// Capture request duration
	start := time.Now()
	client := http.Client{}
	res, err := client.Do(proxyReq)
	duration := time.Since(start)

	if err == nil {
		// Capture response status & log success
		span.SetAttributes(
			attribute.String("http.status_code", fmt.Sprintf("%d", res.StatusCode)),
			attribute.Float64("http.request.duration_ms", float64(time.Since(startTime).Milliseconds())),
		)
		span.AddEvent("Response received")
	} else {
		// Log error in span
		span.SetAttributes(attribute.String("error", "Failed to receive response"))
		span.AddEvent("Response failed", trace.WithAttributes(attribute.String("error", err.Error())))
	}

	return res, duration, err
}
