// Mock AI Tool for Testing
class MockAITool {
    constructor() {
        this.availableProviders = ['anthropic', 'openai', 'google'];
    }

    async generateResponse({
        prompt,
        provider = 'anthropic',
        temperature = 0.7
    }) {
        // Simulate different responses based on provider
        const mockResponses = {
            anthropic: {
                success: true,
                text: 'Mocked Anthropic response for prompt: ' + prompt,
                metadata: { 
                    provider: 'anthropic', 
                    model: 'claude-3-sonnet' 
                }
            },
            openai: {
                success: true,
                text: 'Mocked OpenAI response for prompt: ' + prompt,
                metadata: { 
                    provider: 'openai', 
                    model: 'gpt-4' 
                }
            },
            google: {
                success: true,
                text: 'Mocked Google AI response for prompt: ' + prompt,
                metadata: { 
                    provider: 'google', 
                    model: 'gemini-pro' 
                }
            }
        };

        // Simulate some randomness and potential errors
        if (prompt.trim() === '') {
            return {
                success: false,
                error: 'Empty prompt is not allowed',
                metadata: { provider }
            };
        }

        return mockResponses[provider] || mockResponses['anthropic'];
    }

    async analyzeCode({
        code,
        provider = 'anthropic',
        analysisType = 'general'
    }) {
        return this.generateResponse({
            prompt: `Analyze code: ${code} (Type: ${analysisType})`,
            provider
        });
    }

    async enhanceDocumentation({
        code,
        provider = 'anthropic',
        docStyle = 'jsdoc'
    }) {
        return this.generateResponse({
            prompt: `Generate documentation for code: ${code} (Style: ${docStyle})`,
            provider
        });
    }

    async suggestImprovements({
        code,
        provider = 'anthropic',
        focusAreas = null
    }) {
        return this.generateResponse({
            prompt: `Suggest improvements for code: ${code} (Focus: ${focusAreas?.join(', ') || 'general'})`,
            provider
        });
    }
}

module.exports = MockAITool;