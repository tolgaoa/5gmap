package configParser

import (
	"log"
	"os"
	"strconv"
)

// Config holds all application-wide configuration values
type Config struct {
	ProxyPort      int
	ServicePort    int
	NetworkSliceID string
	LocationID     string
	ServiceName    string
}

// LoadConfig reads environment variables and assigns default values if missing
func LoadConfig() *Config {
	return &Config{
		ProxyPort:      getEnvAsInt("PROXY_PORT", 11095),
		ServicePort:    getEnvAsInt("SERVICE_PORT", 8080),
		NetworkSliceID: getEnv("NETWORK_SLICE_ID", "default-slice"),
		LocationID:     getEnv("LOCATION_ID", "unknown-location"),
		ServiceName:    getEnv("SERVICENAME", "Unknown-VNF"), // VNF Type from env
	}
}

// getEnv reads a string environment variable or returns a default value
func getEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	log.Printf("Environment variable %s not set, using default: %s", key, defaultValue)
	return defaultValue
}

// getEnvAsInt reads an int environment variable or returns a default value
func getEnvAsInt(key string, defaultValue int) int {
	valueStr := getEnv(key, strconv.Itoa(defaultValue))
	value, err := strconv.Atoi(valueStr)
	if err != nil {
		log.Printf("Invalid value for %s: %s, using default: %d", key, valueStr, defaultValue)
		return defaultValue
	}
	return value
}
