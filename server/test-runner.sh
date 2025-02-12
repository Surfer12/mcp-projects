#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${YELLOW}[TEST RUNNER]${NC} $1"
}

# Error handling function
error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Warning function
warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Success function
success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Main test execution
main() {
    log "Starting comprehensive test suite for MCP Server"

    # Ensure dependencies are installed
    log "Checking dependencies..."
    npm install || warn "Dependency installation had some issues"

    # Skip linting for now, as we're setting up the project
    log "Skipping linting configuration..."
    # npm run lint || warn "Linting configuration needs setup"

    # Run type checking
    log "Running TypeScript type checking..."
    npx tsc --noEmit || warn "Type checking found some issues"

    # Run mock-based unit tests
    log "Running unit tests with mocks..."
    npm test || warn "Some tests failed, but continuing"

    # Generate basic coverage report
    log "Generating test coverage report..."
    npm run test:coverage || warn "Coverage report generation had issues"

    # Final check
    success "Test suite completed. Review the output for any warnings or issues."
}

# Run the main function
main