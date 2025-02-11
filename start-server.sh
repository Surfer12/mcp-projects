#!/bin/bash

# Load environment variables
export $(cat claude-mcp-server/.env | xargs)

# Change to server directory
cd claude-mcp-server

# Start the server
npm run start:dev