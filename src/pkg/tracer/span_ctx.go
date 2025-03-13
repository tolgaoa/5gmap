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

// StartSpanWithVNFInfo creates a span and tracks network slice, location, and VNF type
func StartSpanWithVNFInfo(ctx context.Context, req *http.Request) (context.Context, trace.Span, time.Time) {
	tracer := otel.Tracer("revproxy")

	// Extract trace context from incoming request headers
	ctx = propagator.Extract(ctx, propagation.HeaderCarrier(req.Header))

	// Extract VNF-specific data
	networkSliceID := req.Header.Get("X-Network-Slice-ID")
	if networkSliceID == "" {
		networkSliceID = configParser.LoadConfig().NetworkSliceID
	}

	locationID := req.Header.Get("X-Location-ID")
	if locationID == "" {
		locationID = configParser.LoadConfig().LocationID
	}

	vnfType := configParser.LoadConfig().VNFType
	if vnfType == "Unknown-VNF" {
		vnfType = determineVNFType(req.URL.Path) // Fallback
	}

	// Start a new span with parent context
	ctx, span := tracer.Start(ctx, fmt.Sprintf("VNF-Request-%s", vnfType), trace.WithSpanKind(trace.SpanKindServer))

	// Add attributes for classification
	span.SetAttributes(
		attribute.String("network.slice.id", networkSliceID),
		attribute.String("location.id", locationID),
		attribute.String("vnf.type", vnfType),
		attribute.String("http.method", req.Method),
		attribute.String("http.url", req.URL.String()),
	)

	// Capture start time for latency calculation
	startTime := time.Now()

	// Log event when request starts
	span.AddEvent("Request received")

	return ctx, span, startTime
}
