package main

import (
	"context"
	"log"
	"net/http"

	"revproxy/pkg/servcl"
	"revproxy/pkg/tracer"

	"go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/baggage"
	"go.opentelemetry.io/otel/trace"
)

func main() {
	tp, err := tracer.InitTracer()
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
		if err := tp(context.Background()); err != nil {
			log.Printf("Error shutting down tracer provider: %v", err)
		}
	}()

	defaultHandler := func(w http.ResponseWriter, req *http.Request) {
		// Corrected assignment: Handle all three return values
		ctx, span, _ := tracer.StartSpanWithVNFInfo(req.Context(), req)
		defer span.End()

		// Extract baggage attributes (e.g., username)
		bag := baggage.FromContext(ctx)
		username := bag.Member("username").Value()
		if username == "" {
			username = "unknown-user"
		}

		// Log processing event
		span.AddEvent("handling request", trace.WithAttributes(attribute.String("username", username)))

		// Forward request
		res, duration, err := servcl.ForwardRequest(req)
		if err != nil {
			span.RecordError(err)
			http.Error(w, err.Error(), http.StatusBadGateway)
			return
		}

		// Send response
		servcl.WriteResponse(w, res)

		// Log request stats
		servcl.PrintStats(req, res, duration)
	}

	otelHandler := otelhttp.NewHandler(http.HandlerFunc(defaultHandler), "HTTP Request")

	http.Handle("/", otelHandler)
	log.Println("Starting HTTP server on :11095")
	err = http.ListenAndServe(":11095", nil)
	if err != nil {
		log.Fatal(err)
	}
}
