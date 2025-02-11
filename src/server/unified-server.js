const http = require('http');
const WebSocket = require('ws');
const path = require('path');
const toolHandler = require('./common/tool-handler');

class UnifiedServer {
    constructor() {
        this.httpServer = null;
        this.wsServer = null;
        this.sseClients = new Set();
    }

    async initialize() {
        try {
            await toolHandler.initialize();
            console.log('Tool handler initialized successfully');

            // Create HTTP server
            this.httpServer = http.createServer(this.handleHttpRequest.bind(this));

            // Create WebSocket server if WS_ENABLED is true
            if (process.env.WS_ENABLED === 'true') {
                this.wsServer = new WebSocket.Server({ server: this.httpServer });
                this.wsServer.on('connection', this.handleWsConnection.bind(this));
                console.log('WebSocket server enabled');
            }

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

        // Handle SSE endpoint
        if (pathname === '/v1/sse' && req.method === 'GET') {
            console.log(`${new Date().toISOString()} - GET /v1/sse`);
            this.handleSSE(req, res);
            return;
        }

        // Handle tool listing endpoint
        if (pathname === '/v1/tools' && req.method === 'GET') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ tools: toolHandler.getAvailableTools() }));
            return;
        }

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

                        // Notify SSE clients about tool usage
                        this.notifySSEClients({
                            type: 'tool_used',
                            tool: toolName,
                            timestamp: new Date().toISOString()
                        });
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

    handleSSE(req, res) {
        res.writeHead(200, {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        });

        // Add client to SSE clients set
        this.sseClients.add(res);
        console.log(`SSE client connected. Total clients: ${this.sseClients.size}`);

        // Setup heartbeat
        const heartbeat = setInterval(() => {
            res.write(':\n\n');
        }, 15000);

        // Send initial tools list
        this.sendSSEEvent(res, 'tools_list', {
            tools: toolHandler.getAvailableTools()
        });

        // Cleanup on connection close
        req.on('close', () => {
            clearInterval(heartbeat);
            this.sseClients.delete(res);
            console.log(`SSE client disconnected. Total clients: ${this.sseClients.size}`);
        });
    }

    handleWsConnection(ws) {
        console.log('New WebSocket connection established');

        // Send initial tools list
        ws.send(JSON.stringify({
            type: 'tools_list',
            payload: { tools: toolHandler.getAvailableTools() }
        }));

        ws.on('message', async (message) => {
            try {
                const { type, payload } = JSON.parse(message);
                let response;

                switch (type) {
                    case 'tool_request':
                        response = await toolHandler.handleRequest(payload.tool, payload.data);
                        // Notify SSE clients about tool usage
                        this.notifySSEClients({
                            type: 'tool_used',
                            tool: payload.tool,
                            timestamp: new Date().toISOString()
                        });
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
    }

    sendSSEEvent(client, event, data) {
        client.write(`event: ${event}\n`);
        client.write(`data: ${JSON.stringify(data)}\n\n`);
    }

    notifySSEClients(data) {
        this.sseClients.forEach(client => {
            this.sendSSEEvent(client, 'update', data);
        });
    }

    listen(port) {
        this.httpServer.listen(port, () => {
            console.log(`Unified server running on port ${port}`);
            console.log('Available tools:', toolHandler.getAvailableTools());
            console.log('Server features:');
            console.log('- HTTP API endpoints');
            console.log('- Server-Sent Events (SSE)');
            if (this.wsServer) {
                console.log('- WebSocket support');
            }
        });
    }
}

// Export server instance
module.exports = new UnifiedServer();