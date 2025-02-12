const { expect } = require('chai');
const AITool = require('../../src/tools/ai/ai_tool');

describe('Google AI Provider Tests', () => {
    let aiTool;

    beforeEach(() => {
        aiTool = new AITool();
    });

    it('should initialize Google client when API key is available', () => {
        expect(aiTool.google).to.exist;
    });

    it('should generate response using Google provider', async () => {
        const response = await aiTool.generateResponse({
            prompt: 'Describe the concept of machine learning',
            provider: 'google'
        });

        expect(response).to.have.property('success', true);
        expect(response).to.have.property('text');
        expect(response.metadata.provider).to.equal('google');
    });

    it('should handle code generation with Google', async () => {
        const response = await aiTool.generateResponse({
            prompt: 'Generate a Python function to calculate factorial',
            provider: 'google'
        });

        expect(response.text.includes('Python')).to.be.true;
    });

    it('should analyze code using Google provider', async () => {
        const response = await aiTool.analyzeCode({
            code: `
            def fibonacci(n):
                if n <= 1:
                    return n
                else:
                    return fibonacci(n-1) + fibonacci(n-2)
            `,
            provider: 'google'
        });

        expect(response).to.have.property('text');
        expect(response.text).to.include('Analyze code:');
    });

    it('should handle error scenarios gracefully', async () => {
        const emptyResponse = await aiTool.generateResponse({
            prompt: '',
            provider: 'google'
        });

        expect(emptyResponse.success).to.be.false;
        expect(emptyResponse).to.have.property('error');
    });
});