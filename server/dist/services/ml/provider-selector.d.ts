export interface MLProvider {
    supportedModels: string[];
    predict(input: string, options?: {
        model?: string;
    }): Promise<string>;
}
export declare class ProviderSelector {
    private providers;
    getProvider(providerName: string): MLProvider;
    predict(providerName: string, input: string, options?: {
        model?: string;
    }): Promise<string>;
}
