import express, { Request, Response } from 'express';
import OpenAIReasoningTool from './tools/openai/openai_reasoning_tool';

const app = express();
const PORT = process.env.PORT || 3000;

// Mock: Developer and ComputerController services
const developer = { execute: async (cmd: string) => console.log('Developer executed:', cmd) };
const computercontroller = { execute: async (cmd: string) => console.log('Computer Controller executed:', cmd) };

app.use(express.json());

// Initialize OpenAI Reasoning Tool
const openAITool = new OpenAIReasoningTool(process.env.OPENAI_API_KEY || 'mock-api-key');

// Reasoning Route
app.post('/api/reasoning', async (req: Request, res: Response) => {
    const { prompt, mcpServices } = req.body;

    try {
        const result = await openAITool.mcpIntegratedReasoning({ prompt, mcpServices });
        res.json(result);
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        res.status(500).send({ error: errorMessage });
    }
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));