import { MLProvider } from '../provider-selector';
export declare class OpenAIProvider implements MLProvider {
    supportedModels: string[];
    constructor();
    predict(input: string, options?: {
        model?: string;
    }): Promise<string>;
}
