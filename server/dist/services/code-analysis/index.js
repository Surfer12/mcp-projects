"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.setupCodeAnalysisService = void 0;
const analyzers_1 = require("./analyzers");
const setupCodeAnalysisService = (app) => {
    // Initialize code analysis routes and services
    app.post('/api/analyze', async (req, res) => {
        try {
            const { code, type } = req.body;
            const result = await analyzers_1.analyzers.analyze(code, type);
            res.json(result);
        }
        catch (error) {
            res.status(500).json({ error: 'Analysis failed' });
        }
    });
};
exports.setupCodeAnalysisService = setupCodeAnalysisService;
//# sourceMappingURL=index.js.map