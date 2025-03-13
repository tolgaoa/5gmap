package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	// Internal packages
	"revproxy/pkg/configParser"
	"revproxy/pkg/handlers"
	"revproxy/pkg/profile"
	"revproxy/pkg/tracer"

	// Proxy modules
	h1t "revproxy/pkg/http1TLSproxy"
	h1 "revproxy/pkg/http1proxy"
	h2 "revproxy/pkg/http2proxy"
	h3 "revproxy/pkg/http3proxy"
	hs "revproxy/pkg/httpsproxy"

	// External
	log "github.com/sirupsen/logrus"
	"go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

// setLogLevel configures log verbosity based on the LOG_LEVEL environment variable
func setLogLevel() {
	log.SetFormatter(&log.TextFormatter{
		ForceColors:     true,
		TimestampFormat: "2006-01-02 15:04:05.000000",
		FullTimestamp:   true,
	})

	logLevel := os.Getenv("LOG_LEVEL")
	if logLevel == "" {
		logLevel = "info"
	}

	switch strings.ToLower(logLevel) {
	case "trace":
		log.SetLevel(log.TraceLevel)
	case "debug":
		log.SetLevel(log.DebugLevel)
	case "info":
		log.SetLevel(log.InfoLevel)
	case "warn":
		log.SetLevel(log.WarnLevel)
	case "error":
		log.SetLevel(log.ErrorLevel)
	case "fatal":
		log.SetLevel(log.FatalLevel)
	case "panic":
		log.SetLevel(log.PanicLevel)
	default:
		log.Warnf("Unknown log level: %s, defaulting to info", logLevel)
		log.SetLevel(log.InfoLevel)
	}
}

func main() {
	// Set log level first
	setLogLevel()

	// Load configuration
	cfg := configParser.LoadConfig()

	// Initialize Proxy Profile
	proxyProfile := profile.LoadProxyProfile()
	proxyProfile.Display() // Log profile details

	// Initialize OpenTelemetry Tracer
	tp, err := tracer.InitTracer()
	if err != nil {
		log.Fatalf("Tracer initialization failed: %v", err)
	}
	defer func() {
		if err := tp(context.Background()); err != nil {
			log.Errorf("Error shutting down tracer provider: %v", err)
		}
	}()

	// Select Proxy Mode
	opmode := os.Getenv("OPERATION_MODE")
	if opmode == "" {
		opmode = "HTTP1" // Default to HTTP1
	}

	// Validate Proxy Mode
	validModes := map[string]bool{"HTTP1": true, "HTTPS": true, "HTTP2": true, "HTTP3": true}
	if !validModes[opmode] {
		log.Warnf("Invalid OPERATION_MODE: %s, defaulting to HTTP1", opmode)
		opmode = "HTTP1"
	}

	var handler http.Handler

	// Run Proxy Based on Selected Mode
	switch opmode {
	case "DEFAULT":
		log.Info("Using Default HTTP handler")
		handler = http.HandlerFunc(handlers.DefaultHandler)
	case "OTEL":
		log.Info("Using OpenTelemetry HTTP handler")
		handler = otelhttp.NewHandler(http.HandlerFunc(handlers.DefaultHandler), "otelHandler")
	case "HTTP1":
		log.Info("Starting Proxy in HTTP1 <--> HTTP1 Forwarding Mode")
		go h1.StartHTTP1Proxy()
	case "HTTPS":
		log.Info("Starting Proxy in HTTP1 <--> HTTP1 (with TLS) Forwarding Mode")
		go h1t.StartHTTP1Proxy()
		go hs.StartHTTPSProxy()
	case "HTTP2":
		log.Info("Starting Proxy in HTTP1 <--> HTTP2 Forwarding Mode")
		go h2.StartHTTP1toHTTP2Proxy()
		go h2.StartHTTP2toHTTP1Proxy()
	case "HTTP3":
		log.Info("Starting Proxy in HTTP1 <--> HTTP3 Forwarding Mode")
		go h3.StartHTTP1toHTTP3Proxy()
		go h3.StartHTTP3toHTTP1Proxy()
	}

	// Start the main HTTP server
	server := &http.Server{
		Addr:    fmt.Sprintf(":%d", cfg.ProxyPort),
		Handler: handler,
	}

	go func() {
		log.Infof("Starting HTTP server on port %d", cfg.ProxyPort)
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server failed: %v", err)
		}
	}()

	// Graceful Shutdown Handling
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

	<-sigChan
	log.Info("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Errorf("Server shutdown error: %v", err)
	}
	log.Info("Server gracefully stopped.")
}
