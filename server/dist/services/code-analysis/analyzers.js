"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.analyzers = void 0;
const sonarqube_1 = require("./clients/sonarqube");
class CodeAnalyzers {
    constructor() {
        this.sonarqube = new sonarqube_1.SonarQubeClient({
            serverUrl: process.env.SONARQUBE_URL || 'http://localhost:9000',
            token: process.env.SONARQUBE_TOKEN || '',
        });
    }
    async analyze(code, options) {
        try {
            const result = await this.sonarqube.analyze(code, {
                projectKey: options.projectKey || 'temp-analysis',
                analysisMode: options.type,
            });
            return {
                issues: result.issues.map(issue => ({
                    severity: issue.severity,
                    message: issue.message,
                    line: issue.line,
                    file: issue.component,
                })),
                metrics: {
                    complexity: result.measures.complexity || 0,
                    duplicatedLines: result.measures.duplicatedLines || 0,
                    coverage: result.measures.coverage,
                    bugs: result.measures.bugs || 0,
                    vulnerabilities: result.measures.vulnerabilities || 0,
                    codeSmells: result.measures.codeSmells || 0,
                },
            };
        }
        catch (error) {
            console.error('Code analysis failed:', error);
            throw new Error('Failed to analyze code');
        }
    }
}
exports.analyzers = new CodeAnalyzers();
//# sourceMappingURL=analyzers.js.map