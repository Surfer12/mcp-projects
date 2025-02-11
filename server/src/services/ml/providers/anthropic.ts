import Anthropic from '@anthropic-ai/sdk';
import { MLProvider } from '../provider-selector';

export class AnthropicProvider implements MLProvider {
  private client: Anthropic;
  public supportedModels = ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307'];

  constructor() {
    this.client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });
  }

  async predict(input: string, options?: { model?: string }): Promise<string> {
    try {
      const model = options?.model || this.supportedModels[0];
      if (!this.supportedModels.includes(model)) {
        throw new Error(`Model ${model} not supported by Anthropic provider`);
      }

      const response = await this.client.messages.create({
        model,
        max_tokens: 4096,
        messages: [{ role: 'user', content: input }],
      });

      return response.content[0].text;
    } catch (error) {
      console.error('Anthropic prediction failed:', error);
      throw new Error('Failed to generate prediction with Anthropic');
    }
  }
}