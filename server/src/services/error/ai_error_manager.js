const fs = require('fs').promises;
const path = require('path');
const { createLogger, format, transports } = require('winston');
require('winston-daily-rotate-file');

class AIErrorManager {
    constructor(config = {}) {
        this.config = {
            logDirectory: config.logDirectory || path.join(process.cwd(), 'logs'),
            providers: config.providers || ['anthropic', 'openai', 'google'],
            logLevel: config.logLevel || 'info'
        };

        this.logger = this.setupLogger();
        this.errorRegistry = new Map();
    }

    setupLogger() {
        // Ensure log directory exists
        const logDir = this.config.logDirectory;
        fs.mkdir(logDir, { recursive: true }).catch(console.error);

        return createLogger({
            level: this.config.logLevel,
            format: format.combine(
                format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
                format.errors({ stack: true }),
                format.splat(),
                format.json()
            ),
            defaultMeta: { service: 'ai-error-manager' },
            transports: [
                // Console transport
                new transports.Console({
                    format: format.combine(
                        format.colorize(),
                        format.simple()
                    )
                }),
                // Daily rotate file for all logs
                new transports.DailyRotateFile({
                    filename: path.join(logDir, 'application-%DATE%.log'),
                    datePattern: 'YYYY-MM-DD',
                    zippedArchive: true,
                    maxSize: '20m',
                    maxFiles: '14d'
                }),
                // Error specific log
                new transports.DailyRotateFile({
                    filename: path.join(logDir, 'error-%DATE%.log'),
                    datePattern: 'YYYY-MM-DD',
                    level: 'error',
                    zippedArchive: true,
                    maxSize: '20m',
                    maxFiles: '14d'
                })
            ]
        });
    }

    registerError(provider, errorType, details) {
        const errorKey = `${provider}-${errorType}`;
        const timestamp = new Date().toISOString();

        if (!this.errorRegistry.has(errorKey)) {
            this.errorRegistry.set(errorKey, []);
        }

        const errorEntry = {
            timestamp,
            provider,
            type: errorType,
            details,
            occurrences: 1
        };

        this.errorRegistry.get(errorKey).push(errorEntry);

        // Log the error
        this.logger.error(`AI Provider Error: ${errorKey}`, {
            provider,
            errorType,
            details
        });

        return errorEntry;
    }

    async analyzeErrorPatterns() {
        const errorAnalysis = {};

        for (const [errorKey, errors] of this.errorRegistry.entries()) {
            const [provider, errorType] = errorKey.split('-');
            
            const analysisPrompt = `Analyze the following AI provider error pattern:

            Provider: ${provider}
            Error Type: ${errorType}
            Error Occurrences: ${errors.length}

            Provide:
            1. Potential root causes
            2. Recommended mitigation strategies
            3. Potential systemic issues
            4. Suggestions for error prevention
            `;

            try {
                const aiTool = new AITool(); // Assuming AITool is imported
                const analysis = await aiTool.generateResponse({
                    prompt: analysisPrompt,
                    temperature: 0.3,
                    provider: 'anthropic'
                });

                errorAnalysis[errorKey] = {
                    totalOccurrences: errors.length,
                    analysis: analysis.text
                };
            } catch (aiAnalysisError) {
                this.logger.warn('Error during AI-powered error analysis', {
                    errorKey,
                    error: aiAnalysisError
                });
            }
        }

        return errorAnalysis;
    }

    async generateComprehensiveErrorReport() {
        const errorAnalysis = await this.analyzeErrorPatterns();
        
        const reportPath = path.join(
            this.config.logDirectory, 
            `error-report-${new Date().toISOString().replace(/:/g, '-')}.json`
        );

        const report = {
            timestamp: new Date().toISOString(),
            errorAnalysis,
            providerStats: this.getProviderErrorStats()
        };

        await fs.writeFile(reportPath, JSON.stringify(report, null, 2));

        return report;
    }

    getProviderErrorStats() {
        const stats = {};
        for (const provider of this.config.providers) {
            const providerErrors = [...this.errorRegistry.entries()]
                .filter(([key]) => key.startsWith(`${provider}-`));
            
            stats[provider] = {
                totalErrors: providerErrors.reduce((sum, [, errors]) => sum + errors.length, 0),
                uniqueErrorTypes: new Set(providerErrors.map(([key]) => key.split('-')[1])).size
            };
        }
        return stats;
    }

    async purgeOldErrors(retentionDays = 30) {
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - retentionDays);

        for (const [errorKey, errors] of this.errorRegistry.entries()) {
            const filteredErrors = errors.filter(error => 
                new Date(error.timestamp) > cutoffDate
            );

            this.errorRegistry.set(errorKey, filteredErrors);
        }
    }
}

module.exports = AIErrorManager;