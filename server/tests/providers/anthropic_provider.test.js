const { expect } = require('chai');
const AITool = require('../../src/tools/ai/ai_tool');

describe('Anthropic AI Provider Tests', () => {
    let aiTool;

    beforeEach(() => {
        aiTool = new AITool();
    });

    it('should initialize Anthropic client when API key is available', () => {
        expect(aiTool.anthropic).to.exist;
    });

    it('should handle error scenarios gracefully', async () => {
        const errorResponse = await aiTool.generateResponse({
            prompt: '', // Empty prompt should trigger error
            provider: 'anthropic'
        });

        expect(errorResponse).to.have.property('success', false);
        expect(errorResponse).to.have.property('error', 'Prompt cannot be empty');
    });

    it('should generate response using Anthropic provider', async () => {
        const response = await aiTool.generateResponse({
            prompt: 'Write a short poem about technology',
            provider: 'anthropic'
        });

        expect(response).to.have.property('success', true);
        expect(response).to.have.property('text');
        expect(response.metadata.provider).to.equal('anthropic');
    });
});