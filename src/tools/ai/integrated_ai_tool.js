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

        // Initialize Python subprocess for tools
        this.pythonProcess = null;
        this.initializePythonTools();

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

        // Initialize visualization server
        this.visualizationServer = null;
        this.initializeVisualization();

        // Track tool usage for visualization
        this.toolUsageData = {
            timestamps: [],
            tools: {},
            performance: []
        };
    }

    async initializePythonTools() {
        // Start Python subprocess for tools
        const pythonPath = path.join(__dirname, '../../python/src/tools');
        this.pythonProcess = spawn('python', ['-m', 'tool_server'], {
            cwd: pythonPath,
            env: { ...process.env }
        });

        // Handle Python process output
        this.pythonProcess.stdout.on('data', (data) => {
            console.log(`Python tools: ${data}`);
        });

        this.pythonProcess.stderr.on('data', (data) => {
            console.error(`Python tools error: ${data}`);
        });

        // Wait for server to be ready
        await new Promise(resolve => setTimeout(resolve, 2000));
    }

    async initializeVisualization() {
        // Create visualization data directory if it doesn't exist
        const vizDataPath = path.join(__dirname, '../../visualization/data');
        await fs.mkdir(vizDataPath, { recursive: true });

        // Start visualization server
        const vizPath = path.join(__dirname, '../../visualization');
        this.visualizationServer = spawn('streamlit', ['run', 'dashboard.py'], {
            cwd: vizPath,
            env: { ...process.env }
        });

        this.visualizationServer.stdout.on('data', (data) => {
            console.log(`Visualization server: ${data}`);
        });
    }

    async generateResponse(params) {
        try {
            // Track start time for performance monitoring
            const startTime = Date.now();

            // Generate AI response
            const result = await this._generateAIResponse(params);

            // Track tool usage
            this._trackToolUsage('ai_model', startTime);

            // Enhance response with meta-analysis
            const metaAnalysis = await this.performMetaAnalysis(result);
            this._trackToolUsage('meta_analysis', startTime);

            // Perform web operations if needed
            if (params.web_search) {
                const webData = await this.performWebOperations(params.web_search);
                result.webData = webData;
                this._trackToolUsage('web_tool', startTime);
            }

            // Perform Google operations if needed
            if (params.google_search) {
                const googleData = await this.performGoogleOperations(params.google_search);
                result.googleData = googleData;
                this._trackToolUsage('google_tool', startTime);
            }

            // Handle Mojo structures if needed
            if (params.mojo_operation) {
                const mojoData = await this.performMojoOperations(params.mojo_operation);
                result.mojoData = mojoData;
                this._trackToolUsage('mojo_tool', startTime);
            }

            // Update visualizations
            await this.updateVisualizations(result, metaAnalysis);
            this._trackToolUsage('visualization', startTime);

            return {
                ...result,
                metaAnalysis,
                visualizationUrl: 'http://localhost:8501'
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

    async performWebOperations(params) {
        return this._sendToPython({
            action: 'web_request',
            data: params
        });
    }

    async performGoogleOperations(params) {
        return this._sendToPython({
            action: 'google_search',
            data: params
        });
    }

    async performMojoOperations(params) {
        return this._sendToPython({
            action: 'mojo_structure',
            data: params
        });
    }

    async performMetaAnalysis(result) {
        return this._sendToPython({
            action: 'analyze',
            data: {
                response: result,
                timestamp: new Date().toISOString()
            }
        });
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

    async updateVisualizations(result, metaAnalysis) {
        // Prepare visualization data
        const vizData = {
            response: result,
            analysis: metaAnalysis,
            usage: this.toolUsageData,
            timestamp: new Date().toISOString()
        };

        // Update visualization data files
        const dataPath = path.join(__dirname, '../../visualization/data/latest.json');
        await fs.writeFile(dataPath, JSON.stringify(vizData, null, 2));

        // Update visualizations through Python server
        await this._sendToPython({
            action: 'visualize',
            data: {
                type: 'pattern',
                data: {
                    usage_data: this._prepareUsageData(),
                    performance_data: this._preparePerformanceData()
                }
            }
        });
    }

    _prepareUsageData() {
        // Convert usage data to format expected by visualization
        const tools = Object.keys(this.toolUsageData.tools);
        const periods = [...new Set(this.toolUsageData.timestamps)];

        return {
            tools,
            periods,
            data: tools.map(tool => ({
                tool,
                usage: this.toolUsageData.tools[tool]
            }))
        };
    }

    _preparePerformanceData() {
        return {
            data: this.toolUsageData.performance
        };
    }

    async _sendToPython(data) {
        return new Promise((resolve, reject) => {
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
        // Save final tool usage data
        const usageDataPath = path.join(__dirname, '../../visualization/data/tool_usage_history.json');
        await fs.writeFile(usageDataPath, JSON.stringify(this.toolUsageData, null, 2));

        // Cleanup subprocesses
        if (this.pythonProcess) {
            this.pythonProcess.kill();
        }
        if (this.visualizationServer) {
            this.visualizationServer.kill();
        }
    }
}

module.exports = IntegratedAITool;