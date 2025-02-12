"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ProviderSelector = void 0;
const anthropic_1 = require("./providers/anthropic");
const google_1 = require("./providers/google");
const openai_1 = require("./providers/openai");
class ProviderSelector {
    constructor() {
        this.providers = {
            anthropic: new anthropic_1.AnthropicProvider(),
            google: new google_1.GoogleProvider(),
            openai: new openai_1.OpenAIProvider()
        };
    }
    getProvider(providerName) {
        const provider = this.providers[providerName];
        if (!provider) {
            throw new Error(`Provider ${providerName} not found`);
        }
        return provider;
    }
    async predict(providerName, input, options) {
        const provider = this.getProvider(providerName);
        return provider.predict(input, options);
    }
}
exports.ProviderSelector = ProviderSelector;
//# sourceMappingURL=provider-selector.js.map