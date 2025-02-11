# Archived Server Implementations

This directory contains the original server implementations that were consolidated into the unified server (`src/server/unified-server.js`).

## Directory Structure

```
archive/
├── claude/          # Original Claude server implementation
│   └── simple-server.js
└── cursor/          # Original Cursor server implementation
    ├── code-analysis/
    ├── core/
    ├── integration/
    ├── ml-services/
    └── server.js
```

## Historical Context

These implementations were archived on February 11, 2024, as part of a server consolidation effort. The key features from both implementations have been preserved and enhanced in the unified server:

### Claude Server Features
- HTTP API endpoints
- Server-Sent Events (SSE) support
- Tool execution via HTTP POST
- Basic error handling and logging

### Cursor Server Features
- WebSocket support
- Real-time tool execution
- Advanced error handling
- ML services integration

## Migration

All functionality from these implementations has been migrated to the unified server, which provides:
- Combined HTTP and WebSocket support
- Enhanced SSE capabilities
- Improved tool management
- Better error handling and logging
- Cross-client notifications

For current server implementation, please refer to:
- `src/server/unified-server.js` - Main server implementation
- `src/server/index.js` - Server entry point
- `src/server/common/tool-handler.js` - Unified tool handling

## Note

These implementations are kept for historical reference and should not be used in production. All new development should use the unified server implementation.