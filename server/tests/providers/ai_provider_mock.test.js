const { expect } = require('chai');
const MockAITool = require('../../tests/mocks/mock_ai_tool');

describe('AI Tool Provider Tests', () => {
    let aiTool;

    beforeEach(() => {
        aiTool = new MockAITool();
    });

    describe('General Response Generation', () => {
        it('should generate a response for each provider', async () => {
            const providers = ['anthropic', 'openai', 'google'];
            
            for (const provider of providers) {
                const response = await aiTool.generateResponse({
                    prompt: `Test prompt for ${provider}`,
                    provider
                });

                expect(response).to.have.property('success', true);
                expect(response).to.have.property('text');
                expect(response.metadata).to.have.property('provider', provider);
            }
        });

        it('should handle empty prompts gracefully', async () => {
            const response = await aiTool.generateResponse({
                prompt: '',
                provider: 'anthropic'
            });

            expect(response).to.have.property('success', false);
            expect(response).to.have.property('error');
        });
    });

    describe('Code-Related Methods', () => {
        const sampleCode = `
        function add(a, b) {
            return a + b;
        }
        `;

        it('should analyze code', async () => {
            const codeAnalysis = await aiTool.analyzeCode({
                code: sampleCode,
                provider: 'anthropic'
            });

            expect(codeAnalysis).to.have.property('success', true);
            expect(codeAnalysis.text).to.be.a('string');
        });

        it('should enhance documentation', async () => {
            const documentation = await aiTool.enhanceDocumentation({
                code: sampleCode,
                provider: 'openai',
                docStyle: 'jsdoc'
            });

            expect(documentation).to.have.property('success', true);
            expect(documentation.text).to.be.a('string');
        });

        it('should suggest code improvements', async () => {
            const improvements = await aiTool.suggestImprovements({
                code: sampleCode,
                provider: 'google',
                focusAreas: ['performance', 'readability']
            });

            expect(improvements).to.have.property('success', true);
            expect(improvements.text).to.be.a('string');
        });
    });

    describe('Provider Flexibility', () => {
        it('should fall back to default provider if specified provider is invalid', async () => {
            const response = await aiTool.generateResponse({
                prompt: 'Test fallback',
                provider: 'invalid-provider'
            });

            expect(response).to.have.property('success', true);
            expect(response.metadata.provider).to.equal('anthropic');
        });
    });
});