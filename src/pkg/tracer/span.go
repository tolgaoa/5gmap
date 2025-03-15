package tracer

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/trace"

	"revproxy/pkg/configParser"
)

func StartSpanWithVNFInfo(ctx context.Context, req *http.Request) (context.Context, trace.Span, time.Time) {
	tracer := otel.Tracer("revproxy")

	// Extract trace context from incoming request headers
	ctx = propagator.Extract(ctx, propagation.HeaderCarrier(req.Header))

	// Load VNF-specific information
	cfg := configParser.LoadConfig()
	networkSliceID := req.Header.Get("X-Network-Slice-ID")
	if networkSliceID == "" {
		networkSliceID = cfg.NetworkSliceID
	}

	locationID := req.Header.Get("X-Location-ID")
	if locationID == "" {
		locationID = cfg.LocationID
	}

	vnfType := cfg.ServiceName
	if vnfType == "Unknown-VNF" {
		vnfType = determineVNFType(req.URL.Path) // Fallback
	}

	// **NEW: Use the HTTP method and path as the span name**
	spanName := fmt.Sprintf("HTTP %s %s", req.Method, req.URL.Path)

	// Start a new span
	ctx, span := tracer.Start(ctx, spanName, trace.WithSpanKind(trace.SpanKindServer))

	// Attach metadata to the span
	span.SetAttributes(
		attribute.String("network.slice.id", networkSliceID),
		attribute.String("location.id", locationID),
		attribute.String("vnf.type", vnfType),
		attribute.String("http.method", req.Method),
		attribute.String("http.url", req.URL.String()),
	)

	// Capture request start time
	startTime := time.Now()

	// Log event when request starts
	span.AddEvent("Request received")

	return ctx, span, startTime
}
