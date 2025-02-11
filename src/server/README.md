# Unified Server Implementation

This directory contains the unified server implementation that combines features from both Claude and Cursor servers.

## Directory Structure

```
server/
├── archive/         # Historical server implementations
├── common/          # Shared utilities and handlers
│   └── tool-handler.js
├── index.js         # Server entry point
├── unified-server.js # Main server implementation
└── README.md        # This file
```

## Features

The unified server provides:

### Communication Protocols
- HTTP REST API
- Server-Sent Events (SSE)
- WebSocket support (configurable)

### Tool Management
- Unified tool handling interface
- Dynamic tool loading
- Real-time tool usage notifications
- Cross-client communication

### API Endpoints

#### HTTP Endpoints
- `GET /v1/tools` - List available tools
- `POST /v1/tools/{toolName}` - Execute a tool
- `GET /v1/sse` - SSE connection for real-time updates

#### WebSocket Messages
- `tool_request` - Execute a tool
- `list_tools` - Get available tools
- `tools_list` - Initial tools list (sent on connection)
- `update` - Real-time updates

## Configuration

Environment variables:
```
PORT=3000              # Server port (default: 3000)
WS_ENABLED=true       # Enable WebSocket support (default: false)
NODE_ENV=development  # Environment (development/production)
```

## Usage

Starting the server:
```javascript
const server = require('./unified-server');

async function start() {
    await server.initialize();
    server.listen(3000);
}

start();
```

For historical implementations, see the [archive](./archive/README.md) directory.