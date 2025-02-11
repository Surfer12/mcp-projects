const http = require('http');
const WebSocket = require('ws');
const path = require('path');
const toolHandler = require('../common/tool-handler');

class CursorServer {
    constructor() {
        this.httpServer = null;
        this.wsServer = null;
    }

    async initialize() {
        try {
            await toolHandler.initialize();
            console.log('Tool handler initialized successfully');

            // Create HTTP server
            this.httpServer = http.createServer(this.handleHttpRequest.bind(this));

            // Create WebSocket server
            this.wsServer = new WebSocket.Server({ server: this.httpServer });
            this.wsServer.on('connection', this.handleWsConnection.bind(this));

        } catch (error) {
            console.error('Failed to initialize server:', error);
            throw error;
        }
    }

    handleHttpRequest(req, res) {
        // Set CORS headers
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

        // Handle preflight requests
        if (req.method === 'OPTIONS') {
            res.writeHead(200);
            res.end();
            return;
        }

        // Parse URL
        const url = new URL(req.url, `http://${req.headers.host}`);
        const pathname = url.pathname;

        // Handle POST requests
        if (req.method === 'POST') {
            console.log(`${new Date().toISOString()} - POST ${pathname}`);
            let body = '';
            req.on('data', chunk => {
                body += chunk.toString();
            });
            req.on('end', async () => {
                try {
                    const data = JSON.parse(body);
                    let response = { error: 'Endpoint not found' };

                    // Route to appropriate tool handler
                    if (pathname.startsWith('/v1/tools/')) {
                        const toolName = pathname.split('/')[3];
                        response = await toolHandler.handleRequest(toolName, data);
                    }

                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify(response));
                } catch (error) {
                    res.writeHead(500, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: error.message }));
                }
            });
            return;
        }

        // Handle unknown endpoints
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not found' }));
    }

    handleWsConnection(ws) {
        console.log('New WebSocket connection established');

        ws.on('message', async (message) => {
            try {
                const { type, payload } = JSON.parse(message);
                let response;

                switch (type) {
                    case 'tool_request':
                        response = await toolHandler.handleRequest(payload.tool, payload.data);
                        break;
                    case 'list_tools':
                        response = { tools: toolHandler.getAvailableTools() };
                        break;
                    default:
                        response = { error: 'Unknown message type' };
                }

                ws.send(JSON.stringify({
                    type: `${type}_response`,
                    payload: response
                }));
            } catch (error) {
                ws.send(JSON.stringify({
                    type: 'error',
                    payload: { error: error.message }
                }));
            }
        });

        ws.on('close', () => {
            console.log('WebSocket connection closed');
        });

        // Send available tools on connection
        ws.send(JSON.stringify({
            type: 'tools_list',
            payload: { tools: toolHandler.getAvailableTools() }
        }));
    }

    listen(port) {
        this.httpServer.listen(port, () => {
            console.log(`Cursor server running on port ${port}`);
            console.log('Available tools:', toolHandler.getAvailableTools());
        });
    }
}

// Export server instance
module.exports = new CursorServer();