const fs = require('fs').promises;
const path = require('path');

class AIProviderConfigManager {
    constructor(config = {}) {
        this.configPath = config.configPath || path.join(process.cwd(), 'config', 'ai_providers.json');
        this.providers = {
            anthropic: {
                models: [
                    'claude-3-opus-20240229',
                    'claude-3-sonnet-20240229',
                    'claude-3-haiku-20240307'
                ],
                defaultModel: 'claude-3-sonnet-20240229',
                capabilities: {
                    contextWindow: 200000,
                    multimodalSupport: true,
                    recommendedUseCases: ['complex reasoning', 'creative writing', 'code generation']
                }
            },
            openai: {
                models: [
                    'gpt-4-turbo',
                    'gpt-4',
                    'gpt-3.5-turbo'
                ],
                defaultModel: 'gpt-4-turbo',
                capabilities: {
                    contextWindow: 128000,
                    multimodalSupport: true,
                    recommendedUseCases: ['general purpose', 'analytical tasks']
                }
            },
            google: {
                models: [
                    'gemini-pro',
                    'gemini-ultra'
                ],
                defaultModel: 'gemini-pro',
                capabilities: {
                    contextWindow: 32000,
                    multimodalSupport: true,
                    recommendedUseCases: ['research', 'data analysis']
                }
            }
        };
    }

    async loadConfiguration() {
        try {
            const configFile = await fs.readFile(this.configPath, 'utf8');
            const userConfig = JSON.parse(configFile);
            
            // Merge user config with default config
            this.providers = this.deepMerge(this.providers, userConfig);
            return this.providers;
        } catch (error) {
            // If file doesn't exist or is invalid, return default config
            console.warn('No custom AI provider configuration found. Using default.');
            return this.providers;
        }
    }

    async saveConfiguration(newConfig) {
        try {
            // Validate new configuration
            this.validateConfiguration(newConfig);

            // Merge new config with existing config
            this.providers = this.deepMerge(this.providers, newConfig);

            // Ensure config directory exists
            await fs.mkdir(path.dirname(this.configPath), { recursive: true });

            // Write updated configuration
            await fs.writeFile(
                this.configPath, 
                JSON.stringify(this.providers, null, 2)
            );

            return this.providers;
        } catch (error) {
            console.error('Failed to save AI provider configuration:', error);
            throw error;
        }
    }

    validateConfiguration(config) {
        for (const [providerName, providerConfig] of Object.entries(config)) {
            if (!this.providers[providerName]) {
                throw new Error(`Invalid provider: ${providerName}`);
            }

            // Validate models
            if (providerConfig.models) {
                if (!Array.isArray(providerConfig.models)) {
                    throw new Error(`Models for ${providerName} must be an array`);
                }
            }

            // Validate default model
            if (providerConfig.defaultModel) {
                if (!providerConfig.models?.includes(providerConfig.defaultModel)) {
                    throw new Error(`Default model must be in the list of models for ${providerName}`);
                }
            }
        }
    }

    getProviderRecommendation(taskDescription) {
        const prompt = `Given the task description, recommend the most suitable AI provider and model:

        Task Description: ${taskDescription}

        Provide:
        1. Recommended Provider
        2. Specific Model
        3. Rationale for selection
        4. Potential limitations
        `;

        // This would ideally use the AI tool to make a dynamic recommendation
        // For now, we'll use a simple heuristic
        const aiTool = new AITool(); // Assuming AITool is imported
        return aiTool.generateResponse({
            prompt,
            temperature: 0.3,
            provider: 'anthropic'
        });
    }

    deepMerge(target, source) {
        for (const key in source) {
            if (source.hasOwnProperty(key)) {
                if (source[key] instanceof Object) {
                    if (!target[key]) Object.assign(target, { [key]: {} });
                    this.deepMerge(target[key], source[key]);
                } else {
                    Object.assign(target, { [key]: source[key] });
                }
            }
        }
        return target;
    }

    async generateModelComparisonReport() {
        const analysisPrompt = `Compare the capabilities of the following AI models:

        ${Object.entries(this.providers).map(([providerName, providerConfig]) => 
            `${providerName.toUpperCase()} Models:
            ${providerConfig.models.map(model => `- ${model}`).join('\n')}
        `).join('\n\n')}

        For each model, analyze:
        1. Strengths
        2. Weaknesses
        3. Best use cases
        4. Performance characteristics
        5. Cost-effectiveness
        `;

        const aiTool = new AITool(); // Assuming AITool is imported
        return aiTool.generateResponse({
            prompt: analysisPrompt,
            temperature: 0.4,
            provider: 'anthropic'
        });
    }
}

module.exports = AIProviderConfigManager;