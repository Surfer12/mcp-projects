"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.setupIDEService = void 0;
const plugin_1 = require("./plugin");
const setupIDEService = (app) => {
    // Initialize IDE integration routes
    app.post('/api/ide/command', async (req, res) => {
        try {
            const { command, params } = req.body;
            const result = await plugin_1.plugin.executeCommand(command, params);
            res.json(result);
        }
        catch (error) {
            res.status(500).json({ error: 'IDE command execution failed' });
        }
    });
};
exports.setupIDEService = setupIDEService;
//# sourceMappingURL=index.js.map