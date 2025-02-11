import { AnthropicProvider } from './providers/anthropic';
import { GoogleAIProvider } from './providers/google';
import { OpenAIProvider } from './providers/openai';

export interface MLProvider {
  predict(input: string, options?: any): Promise<string>;
  supportedModels: string[];
}

class ProviderSelector {
  private providers: Map<string, MLProvider>;
  private defaultProvider: string;

  constructor() {
    this.providers = new Map();
    this.defaultProvider = process.env.DEFAULT_AI_PROVIDER || 'anthropic';

    // Initialize providers
    this.providers.set('anthropic', new AnthropicProvider());
    this.providers.set('openai', new OpenAIProvider());
    this.providers.set('google', new GoogleAIProvider());
  }

  async predict(input: string, model?: string): Promise<string> {
    try {
      // If model is specified, find the provider that supports it
      if (model) {
        for (const [name, provider] of this.providers) {
          if (provider.supportedModels.includes(model)) {
            return provider.predict(input, { model });
          }
        }
        throw new Error(`No provider found for model: ${model}`);
      }

      // Use default provider
      const provider = this.providers.get(this.defaultProvider);
      if (!provider) {
        throw new Error(`Default provider ${this.defaultProvider} not found`);
      }

      return provider.predict(input);
    } catch (error) {
      console.error('Prediction failed:', error);
      throw new Error('Failed to generate prediction');
    }
  }

  getProvider(name: string): MLProvider {
    const provider = this.providers.get(name);
    if (!provider) {
      throw new Error(`Provider ${name} not found`);
    }
    return provider;
  }

  getSupportedModels(): Record<string, string[]> {
    const models: Record<string, string[]> = {};
    for (const [name, provider] of this.providers) {
      models[name] = provider.supportedModels;
    }
    return models;
  }
}

export const providerSelector = new ProviderSelector();
