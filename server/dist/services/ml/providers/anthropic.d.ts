import { MLProvider } from '../provider-selector';
export declare class AnthropicProvider implements MLProvider {
    private client;
    supportedModels: string[];
    constructor();
    predict(input: string, options?: {
        model?: string;
    }): Promise<string>;
}
