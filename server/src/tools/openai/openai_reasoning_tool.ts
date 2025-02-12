import OpenAI from 'openai';

interface CallModelParams {
    prompt: string;
    model?: string;
    temperature?: number;
    reasoningLevel?: string;
}

interface MCPReasoningParams {
    prompt: string;
    mcpServices?: Array<{ type: string; execute: (response: string) => Promise<void> }>;
}

class OpenAIReasoningTool {
    private client: OpenAI;

    constructor(apiKey: string) {
        if (!apiKey) {
            throw new Error('An OpenAI API key is required to use this tool.');
        }

        this.client = new OpenAI({ apiKey });
    }

    async callModel({ prompt, model = 'gpt-4', temperature = 0.7, reasoningLevel = 'high' }: CallModelParams): Promise<string> {
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

    async highReasoning(prompt: string): Promise<string> {
        return this.callModel({ prompt, reasoningLevel: 'high' });
    }

    async lowReasoning(prompt: string): Promise<string> {
        return this.callModel({ prompt, reasoningLevel: 'low', temperature: 0.3 });
    }

    async creativeReasoning(prompt: string): Promise<string> {
        return this.callModel({ prompt, reasoningLevel: 'creative', temperature: 1.0 });
    }

    async mcpIntegratedReasoning({ prompt, mcpServices = [] }: MCPReasoningParams): Promise<{ success: boolean; response: string; mcpServicesProcessed: number }> {
        const response = await this.highReasoning(prompt);

        for (const service of mcpServices) {
            await service.execute(response);
        }

        return { success: true, response, mcpServicesProcessed: mcpServices.length };
    }
}

export default OpenAIReasoningTool;