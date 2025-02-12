const OpenAI = require('openai');
const { sequentialReasoning } = require('../../mcp/sequentialReasoning'); // Assuming MCP integration

class OpenAIReasoningTool {
    constructor(apiKey) {
        if (!apiKey) {
            throw new Error('An OpenAI API key is required to use this tool.');
        }

        this.client = new OpenAI({ apiKey });
    }

    async callModel({ prompt, model = 'gpt-4', temperature = 0.7, reasoningLevel = 'high' }) {
        const systemPrompt = `You are an AI with ${reasoningLevel} reasoning capabilities.`;

        const response = await this.client.chat.completions.create({
            model,
            messages: [
                { role: 'system', content: systemPrompt },
                { role: 'user', content: prompt }
            ],
            temperature,
            max_tokens: 1500
        });

        return response.choices[0].message.content;
    }

    async highReasoning(prompt) {
        return this.callModel({ prompt, reasoningLevel: 'high' });
    }

    async lowReasoning(prompt) {
        return this.callModel({ prompt, reasoningLevel: 'low', temperature: 0.3 });
    }

    async creativeReasoning(prompt) {
        return this.callModel({ prompt, reasoningLevel: 'creative', temperature: 1.0 });
    }

    async sequentialReasoningChain(prompt, steps = 5) {
        const reasoningChain = [];

        let currentPrompt = prompt;
        for (let i = 0; i < steps; i++) {
            const response = await this.callModel({ prompt: currentPrompt, reasoningLevel: 'high' });
            reasoningChain.push(response);

            currentPrompt = `Based on this response:
            ${response}
            What should I consider next?`;
        }

        return reasoningChain;
    }

    async mcpIntegratedReasoning({ prompt, mcpServices = [] }) {
        // Apply Developer and ComputerController MCP logic
        const response = await this.callModel({ prompt, reasoningLevel: 'high' });

        for (const service of mcpServices) {
            if (service.type === 'developer') {
                await developer.execute(response); // Developer logic
            } else if (service.type === 'computercontroller') {
                await computercontroller.execute(response); // Computer control logic
            }
        }

        return { success: true, response, mcpServicesProcessed: mcpServices.length };
    }
}

module.exports = OpenAIReasoningTool;