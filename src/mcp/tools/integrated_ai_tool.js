const OpenAI = require('openai');
const Anthropic = require('@anthropic-ai/sdk');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs').promises;
require('dotenv').config({ path: 'config/.env' });

class IntegratedAITool {
    constructor() {
        // Validate required environment variables
        if (!process.env.OPENAI_API_KEY) {
            throw new Error('OPENAI_API_KEY environment variable is not set');
        }
        if (!process.env.ANTHROPIC_API_KEY) {
            throw new Error('ANTHROPIC_API_KEY environment variable is not set');
        }
        if (!process.env.GOOGLE_API_KEY) {
            throw new Error('GOOGLE_API_KEY environment variable is not set');
        }

        // Initialize AI clients
        this.openai = new OpenAI({
            apiKey: process.env.OPENAI_API_KEY
        });

        this.anthropic = new Anthropic({
            apiKey: process.env.ANTHROPIC_API_KEY
        });

        // Initialize Python integration process
        this.pythonProcess = null;
        this.initializePythonIntegration();

        // Import configuration from AITool
        this.models = {
            openai: {
                default: 'o1-2024-12-17',
                fallback: ['o3-mini-2025-01-31', 'gpt-4o-2024-05-13']
            },
            anthropic: {
                default: 'claude-3-5-sonnet-20241022',
                fallback: 'claude-3-5-haiku-20241022'
            }
        };

        this.reasoningTypes = {
            default: 'auto',
            types: [
                'auto',
                'step_by_step',
                'tree_of_thought',
                'chain_of_thought',
                'fast',
                'analytical',
                'creative'
            ]
        };

        // Track tool usage for visualization
        this.toolUsageData = {
            timestamps: [],
            tools: {},
            performance: []
        };
    }

    async initializePythonIntegration() {
        // Start Python integration process
        const pythonPath = path.join(__dirname, '../tools/js_integration.py');
        this.pythonProcess = spawn('python', [pythonPath], {
            env: { ...process.env }
        });

        // Handle Python process output
        this.pythonProcess.stdout.on('data', (data) => {
            console.log(`Python integration: ${data}`);
        });

        this.pythonProcess.stderr.on('data', (data) => {
            console.error(`Python integration error: ${data}`);
        });

        // Wait for integration to be ready
        await new Promise(resolve => setTimeout(resolve, 2000));
    }

    async generateResponse(params) {
        try {
            // Track start time for performance monitoring
            const startTime = Date.now();

            // Generate AI response
            const result = await this._generateAIResponse(params);
            this._trackToolUsage('ai_model', startTime);

            // Process through Python integration
            const processedResult = await this._processThroughIntegration({
                action: 'process',
                data: {
                    ai_response: result,
                    analysis_type: params.analysisType || 'structural',
                    visualization_type: params.visualizationType || 'pattern',
                    web_search: params.webSearch,
                    google_search: params.googleSearch,
                    mojo_operation: params.mojoOperation
                }
            });

            // Track tool usage from Python components
            if (processedResult.state?.operations) {
                processedResult.state.operations.forEach(op => {
                    this._trackToolUsage(op.tool, op.duration * 1000);
                });
            }

            return {
                ...result,
                metaAnalysis: processedResult.meta_analysis,
                patterns: processedResult.result?.patterns,
                visualization: processedResult.visualization,
                state: processedResult.state
            };

        } catch (error) {
            console.error('Error in integrated response generation:', error);
            throw error;
        }
    }

    async _generateAIResponse(params) {
        const { provider = 'anthropic', model = null } = params;

        if (provider === 'anthropic') {
            const response = await this.anthropic.messages.create({
                model: model || this.models.anthropic.default,
                max_tokens: params.maxTokens || 4096,
                messages: [
                    { role: 'user', content: params.prompt }
                ]
            });
            return {
                success: true,
                text: response.content[0].text,
                provider: 'anthropic'
            };
        } else {
            const response = await this.openai.chat.completions.create({
                model: model || this.models.openai.default,
                messages: [
                    { role: 'user', content: params.prompt }
                ]
            });
            return {
                success: true,
                text: response.choices[0].message.content,
                provider: 'openai'
            };
        }
    }

    _trackToolUsage(toolName, startTime) {
        const timestamp = new Date().toISOString();
        const duration = Date.now() - startTime;

        this.toolUsageData.timestamps.push(timestamp);
        this.toolUsageData.tools[toolName] = (this.toolUsageData.tools[toolName] || 0) + 1;
        this.toolUsageData.performance.push({
            tool: toolName,
            duration,
            timestamp
        });
    }

    async _processThroughIntegration(data) {
        return new Promise((resolve, reject) => {
            // Send data to Python process
            this.pythonProcess.stdin.write(JSON.stringify(data) + '\n');

            const handler = (data) => {
                try {
                    const response = JSON.parse(data.toString());
                    this.pythonProcess.stdout.removeListener('data', handler);
                    resolve(response);
                } catch (error) {
                    reject(error);
                }
            };

            this.pythonProcess.stdout.on('data', handler);
        });
    }

    async cleanup() {
        try {
            // Clean up through Python integration
            const finalState = await this._processThroughIntegration({
                action: 'cleanup',
                data: this.toolUsageData
            });

            // Save final tool usage data
            const usageDataPath = path.join(__dirname, '../../visualization/data/tool_usage_history.json');
            await fs.writeFile(usageDataPath, JSON.stringify({
                ...this.toolUsageData,
                final_state: finalState
            }, null, 2));

            // Cleanup Python process
            if (this.pythonProcess) {
                this.pythonProcess.kill();
            }

            return finalState;
        } catch (error) {
            console.error('Error during cleanup:', error);
            throw error;
        }
    }
}

module.exports = IntegratedAITool;