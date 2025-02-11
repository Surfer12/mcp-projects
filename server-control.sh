#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if server is running
check_server() {
    if pgrep -f "node.*simple-server.js" > /dev/null; then
        return 0 # Server is running
    else
        return 1 # Server is not running
    fi
}

# Function to start the server
start_server() {
    if check_server; then
        echo -e "${RED}Server is already running${NC}"
    else
        echo -e "${GREEN}Starting server...${NC}"
        node src/server/simple-server.js &
        sleep 2 # Wait for server to start
        if check_server; then
            echo -e "${GREEN}Server started successfully${NC}"
        else
            echo -e "${RED}Failed to start server${NC}"
        fi
    fi
}

# Function to stop the server
stop_server() {
    if check_server; then
        echo -e "${GREEN}Stopping server...${NC}"
        pkill -f "node.*simple-server.js"
        sleep 2 # Wait for server to stop
        if ! check_server; then
            echo -e "${GREEN}Server stopped successfully${NC}"
        else
            echo -e "${RED}Failed to stop server${NC}"
        fi
    else
        echo -e "${RED}Server is not running${NC}"
    fi
}

# Function to restart the server
restart_server() {
    echo "Restarting server..."
    stop_server
    sleep 2
    start_server
}

# Function to run tests
run_tests() {
    echo -e "${GREEN}Running tests...${NC}"
    if ! check_server; then
        echo -e "${RED}Server must be running to execute tests${NC}"
        echo -e "Starting server first..."
        start_server
    fi
    node test/test-endpoints.js
}

# Main script logic
case "$1" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        restart_server
        ;;
    test)
        run_tests
        ;;
    status)
        if check_server; then
            echo -e "${GREEN}Server is running${NC}"
        else
            echo -e "${RED}Server is not running${NC}"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|test|status}"
        exit 1
        ;;
esac

exit 0