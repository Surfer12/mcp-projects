"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const code_analysis_1 = require("@services/code-analysis");
const core_1 = require("@services/core");
const ide_1 = require("@services/ide");
const ml_1 = require("@services/ml");
const dotenv_1 = __importDefault(require("dotenv"));
const express_1 = __importDefault(require("express"));
// Load environment variables
dotenv_1.default.config({ path: './config/env/.env' });
const app = (0, express_1.default)();
const port = process.env.PORT || 3000;
// Middleware
app.use(express_1.default.json());
// Initialize services
(0, code_analysis_1.setupCodeAnalysisService)(app);
(0, core_1.setupCoreService)(app);
(0, ide_1.setupIDEService)(app);
(0, ml_1.setupMLService)(app);
// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});
// Start server
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
//# sourceMappingURL=main.js.map