"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.setupMLService = void 0;
const provider_selector_1 = require("./provider-selector");
const providerSelector = new provider_selector_1.ProviderSelector();
const setupMLService = (app) => {
    // Initialize ML service routes
    app.post('/api/ml/predict', async (req, res) => {
        try {
            const { input, model } = req.body;
            const result = await providerSelector.predict('openai', input, { model });
            res.json(result);
        }
        catch (error) {
            res.status(500).json({ error: 'Prediction failed' });
        }
    });
};
exports.setupMLService = setupMLService;
//# sourceMappingURL=index.js.map