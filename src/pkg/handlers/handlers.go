package handlers

import (
	"net/http"

	log "github.com/sirupsen/logrus"
)

// DefaultHandler processes requests without OpenTelemetry instrumentation
// Used to test the interception functionality
func DefaultHandler(w http.ResponseWriter, req *http.Request) {
	log.Info("DEFAULT_HANDLER: Processing New Request")
	log.Infof("Received request: %s %s", req.Method, req.URL.Path)

	// Example response
	w.Header().Set("Content-Type", "text/plain")
	w.WriteHeader(http.StatusOK)
	_, err := w.Write([]byte("Default Handler Response"))
	if err != nil {
		log.Errorf("Error writing response: %v", err)
	}
}
