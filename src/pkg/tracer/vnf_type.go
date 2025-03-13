package tracer

import (
	"strings"
)

// determineVNFType extracts the VNF type from the API path using CAPIF conventions
func determineVNFType(apiPath string) string {
	switch {
	case strings.Contains(apiPath, "/namf"):
		return "AMF"
	case strings.Contains(apiPath, "/nsmf"):
		return "SMF"
	case strings.Contains(apiPath, "/nudr"):
		return "UDR"
	case strings.Contains(apiPath, "/nausf"):
		return "AUSF"
	case strings.Contains(apiPath, "/nrf"):
		return "NRF"
	case strings.Contains(apiPath, "/npcf"):
		return "PCF"
	case strings.Contains(apiPath, "/nnssf"):
		return "NSSF"
	default:
		return "Unknown-VNF"
	}
}
