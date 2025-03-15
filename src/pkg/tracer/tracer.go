package tracer

import (
	"context"
	"fmt"
	"os"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.17.0"

	"revproxy/pkg/configParser"
)

var (
	// OpenTelemetry propagator
	propagator       = propagation.TraceContext{}
	tracerProvider   *sdktrace.TracerProvider
	cfg              = configParser.LoadConfig() // Load configuration once
	defaultCollector = "opentelemetry-collector.otel.svc.cluster.local:4317"
)

// InitTracer initializes OpenTelemetry Tracer with VNF classification
func InitTracer() (func(context.Context) error, error) {
	ctx := context.Background()

	// Load service name and attributes dynamically
	serviceName := cfg.ServiceName
	if serviceName == "Unknown-VNF" {
		serviceName = os.Getenv("SERVICENAME") // Fallback to environment variable
	}

	res, err := resource.New(ctx,
		resource.WithAttributes(
			semconv.ServiceNameKey.String(serviceName),
		),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create resource: %w", err)
	}

	// Set OTEL collector dynamically from env variable
	collectorAddr := os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
	if collectorAddr == "" {
		collectorAddr = defaultCollector
	}

	// Establish gRPC connection
	ctx, cancel := context.WithTimeout(ctx, time.Second*5)
	defer cancel()

	conn, err := grpc.DialContext(ctx, collectorAddr,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithBlock(),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to OTLP collector (%s): %w", collectorAddr, err)
	}

	// Set up a trace exporter
	traceExporter, err := otlptracegrpc.New(ctx, otlptracegrpc.WithGRPCConn(conn))
	if err != nil {
		return nil, fmt.Errorf("failed to create trace exporter: %w", err)
	}

	// Configure a batch span processor
	bsp := sdktrace.NewBatchSpanProcessor(traceExporter)
	tracerProvider = sdktrace.NewTracerProvider(
		sdktrace.WithSampler(sdktrace.AlwaysSample()),
		sdktrace.WithResource(res),
		sdktrace.WithSpanProcessor(bsp),
	)

	// Set the tracer provider globally
	otel.SetTracerProvider(tracerProvider)
	otel.SetTextMapPropagator(propagator)

	return tracerProvider.Shutdown, nil
}
