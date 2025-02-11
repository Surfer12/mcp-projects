#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if jq is installed
check_jq() {
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}jq is not installed. Please install it using the following command:${NC}"
        echo -e "${GREEN}magic install jq${NC}"
        exit 1
    fi
}

# Function to parse JSON
parse_json() {
    local json_input="$1"
    echo -e "${GREEN}Parsing JSON...${NC}"
    echo "$json_input" | jq '.'
}

# Main script logic
check_jq

if [ -z "$1" ]; then
    echo -e "${RED}No JSON input provided. Please provide a JSON string or file.${NC}"
    exit 1
fi

if [ -f "$1" ]; then
    # If input is a file
    parse_json "$(cat "$1")"
else
    # If input is a string
    parse_json "$1"
fi

exit 0