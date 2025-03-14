#!/bin/bash

# Usage: ./replace_string.sh <search_string> <replace_string> <directory>

# Check if sufficient arguments are provided
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <search_string> <replace_string> <directory>"
    exit 1
fi

SEARCH_STRING=$1
REPLACE_STRING=$2
TARGET_DIR=$3

# Verify the target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory $TARGET_DIR does not exist."
    exit 1
fi

# Find and replace
find "$TARGET_DIR" -type f -exec sed -i "s/${SEARCH_STRING}/${REPLACE_STRING}/g" {} +

echo "Replacement complete."

