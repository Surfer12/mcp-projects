"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.setupCoreService = void 0;
const server_1 = require("./server");
const setupCoreService = (app) => {
    // Initialize core service routes
    app.post('/api/core/execute', async (req, res) => {
        try {
            const { command } = req.body;
            const result = await server_1.server.execute(command);
            res.json(result);
        }
        catch (error) {
            res.status(500).json({ error: 'Command execution failed' });
        }
    });
};
exports.setupCoreService = setupCoreService;
//# sourceMappingURL=index.js.map