import { AnthropicProvider } from './providers/anthropic';
import { GoogleProvider } from './providers/google';
import { OpenAIProvider } from './providers/openai';

export interface MLProvider {
    supportedModels: string[];
    predict(input: string, options?: { model?: string }): Promise<string>;
}

export class ProviderSelector {
    private providers: Record<string, MLProvider> = {
        anthropic: new AnthropicProvider(),
        google: new GoogleProvider(),
        openai: new OpenAIProvider()
    };

    getProvider(providerName: string): MLProvider {
        const provider = this.providers[providerName];
        if (!provider) {
            throw new Error(`Provider ${providerName} not found`);
        }
        return provider;
    }

    async predict(
        providerName: string, 
        input: string, 
        options?: { model?: string }
    ): Promise<string> {
        const provider = this.getProvider(providerName);
        return provider.predict(input, options);
    }
}