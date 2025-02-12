"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AnthropicProvider = void 0;
const sdk_1 = __importDefault(require("@anthropic-ai/sdk"));
class AnthropicProvider {
    constructor() {
        this.supportedModels = ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307'];
        this.client = new sdk_1.default({
            apiKey: process.env.ANTHROPIC_API_KEY,
        });
    }
    async predict(input, options) {
        try {
            const model = options?.model || this.supportedModels[0];
            if (!this.supportedModels.includes(model)) {
                throw new Error(`Model ${model} not supported by Anthropic provider`);
            }
            // Mock implementation of message creation
            const response = {
                content: [{ text: `Mocked response for: ${input}` }],
            };
            return response.content[0].text;
        }
        catch (error) {
            console.error('Anthropic prediction failed:', error);
            throw new Error('Failed to generate prediction with Anthropic');
        }
    }
}
exports.AnthropicProvider = AnthropicProvider;
//# sourceMappingURL=anthropic.js.map