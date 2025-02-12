import { MLProvider } from '../provider-selector';
export declare class GoogleProvider implements MLProvider {
    supportedModels: string[];
    constructor();
    predict(input: string, options?: {
        model?: string;
    }): Promise<string>;
}
