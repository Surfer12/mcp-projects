#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to run linting
lint() {
    echo -e "${GREEN}Running built-in Cursor JSON linter on JSON files in src/ ...${NC}"
    if command -v cursor &> /dev/null; then
        cursor json lint src/
    else
        echo -e "${YELLOW}Cursor CLI not found. Please install Cursor CLI from https://cursor.example.com or via your package manager.${NC}"
        exit 1
    fi
}

# Main script logic
lint

exit 0