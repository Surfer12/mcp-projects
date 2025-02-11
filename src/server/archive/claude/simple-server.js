const http = require('http');
const path = require('path');
const toolHandler = require('../common/tool-handler');

// Now you can access environment variables via process.env
const PORT = process.env.PORT || 3000;

// Create HTTP server
const server = http.createServer((req, res) => {
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
  const path = url.pathname;

  // Handle SSE endpoint
  if (path === '/v1/sse' && req.method === 'GET') {
    console.log(`${new Date().toISOString()} - GET /v1/sse`);
    handleSSE(req, res);
    return;
  }

  // Handle other endpoints
  if (req.method === 'POST') {
    console.log(`${new Date().toISOString()} - POST ${path}`);
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', async () => {
      try {
        const data = JSON.parse(body);
        let response = { error: 'Endpoint not found' };

        // Route to appropriate tool handler
        if (path.startsWith('/v1/tools/')) {
          const toolName = path.split('/')[3];
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
});

// Handle SSE connections
function handleSSE(req, res) {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
  });

  const heartbeat = setInterval(() => {
    res.write(':\n\n');
  }, 15000);

  req.on('close', () => {
    clearInterval(heartbeat);
  });

  console.log('SSE connection established');
}

// Initialize server
async function initialize() {
  try {
    await toolHandler.initialize();
    console.log('Tool handler initialized successfully');
  } catch (error) {
    console.error('Failed to initialize tool handler:', error);
    process.exit(1);
  }
}

// Export server and initialize function
module.exports = {
  server,
  initialize,
  listen: (port) => {
    server.listen(port, () => {
      console.log(`Server running on port ${port}`);
      console.log('Available tools:', toolHandler.getAvailableTools());
    });
  }
};