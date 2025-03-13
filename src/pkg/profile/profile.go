// File: profile/profile.go

package profile

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"

	log "github.com/sirupsen/logrus"
)

// ProxyProfile represents an instance profile of the otel_proxy
type ProxyProfile struct {
	InstanceID     string `json:"instanceId"`
	InstanceName   string `json:"instanceName"`
	Function       string `json:"function"`
	Status         string `json:"status"`
	IPv4Address    string `json:"ipv4"`
	Location       string `json:"location"`
	K8sDNS         string `json:"dns"`
	Clients        int    `json:"clients"`
	ServingVNFType string `json:"servingVNFType"`
	ServingVNFID   string `json:"servingVNFID"`
	SliceID        string `json:"sliceId"`
}

// LoadProxyProfile initializes the profile using environment variables
func LoadProxyProfile() *ProxyProfile {
	return &ProxyProfile{
		InstanceID:     getEnv("INSTANCE_ID", "otel-proxy-001"),
		InstanceName:   getEnv("INSTANCE_NAME", "otel-proxy-instance"),
		Function:       getEnv("FUNCTION", "Proxy"),
		Status:         getEnv("STATUS", "Active"),
		IPv4Address:    getEnv("IPV4_ADDRESS", "127.0.0.1"),
		Location:       getEnv("LOCATION", "default-location"),
		K8sDNS:         getEnv("K8S_DNS", "otel-proxy.svc.cluster.local"),
		Clients:        getEnvAsInt("CLIENTS", 0),
		ServingVNFType: getEnv("SERVING_VNF_TYPE", "Unknown"),
		ServingVNFID:   getEnv("SERVING_VNF_ID", "Unknown"),
		SliceID:        getEnv("SLICE_ID", "default-slice"),
	}
}

// ProfileToJSON converts the ProxyProfile struct to a JSON string
func (p *ProxyProfile) ProfileToJSON() (string, error) {
	data, err := json.Marshal(p)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

// Display prints the ProxyProfile information
func (p *ProxyProfile) Display() {
	log.Infof("otel_proxy Instance Info")
	log.Infof("\tInstance ID: %s", p.InstanceID)
	log.Infof("\tInstance Name: %s", p.InstanceName)
	log.Infof("\tFunction: %s", p.Function)
	log.Infof("\tStatus: %s", p.Status)
	log.Infof("\tIPv4 Address: %s", p.IPv4Address)
	log.Infof("\tLocation: %s", p.Location)
	log.Infof("\tClients: %d", p.Clients)
	log.Infof("\tServing VNF Type: %s", p.ServingVNFType)
	log.Infof("\tServing VNF ID: %s", p.ServingVNFID)
	log.Infof("\tServing Slice ID: %s", p.SliceID)
}

// GetInstanceID returns the instance ID of the ProxyProfile
func (p *ProxyProfile) GetInstanceID() string {
	return p.InstanceID
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
	valueStr := getEnv(key, fmt.Sprintf("%d", defaultValue))
	value, err := strconv.Atoi(valueStr)
	if err != nil {
		log.Printf("Invalid value for %s: %s, using default: %d", key, valueStr, defaultValue)
		return defaultValue
	}
	return value
}
