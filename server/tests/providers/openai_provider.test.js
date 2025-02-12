const { expect } = require('chai');
const AITool = require('../../src/tools/ai/ai_tool');

describe('OpenAI AI Provider Tests', () => {
    let aiTool;

    beforeEach(() => {
        aiTool = new AITool();
    });

    it('should handle JSON response format', async () => {
        const response = await aiTool.handleJSONResponse({
            prompt: 'Convert this response to JSON',
            provider: 'openai'
        });

        expect(response).to.have.property('success', true);
        expect(response.data).to.be.an('object');
        expect(response.data).to.have.property('original_prompt', 'Convert this response to JSON');
    });

    it('should handle error scenarios gracefully', async () => {
        const errorResponse = await aiTool.generateResponse({
            prompt: '', // Empty prompt should trigger error
            provider: 'openai'
        });

        expect(errorResponse).to.have.property('success', false);
        expect(errorResponse).to.have.property('error', 'Prompt cannot be empty');
    });
});