interface SonarQubeConfig {
    serverUrl: string;
    token: string;
}
interface SonarQubeAnalysisOptions {
    projectKey: string;
    analysisMode: 'quality' | 'security' | 'full';
}
interface SonarQubeIssue {
    severity: 'BLOCKER' | 'CRITICAL' | 'MAJOR' | 'MINOR' | 'INFO';
    message: string;
    line?: number;
    component: string;
}
interface SonarQubeMeasures {
    complexity: number;
    duplicatedLines: number;
    coverage?: number;
    bugs: number;
    vulnerabilities: number;
    codeSmells: number;
}
interface SonarQubeAnalysisResult {
    issues: SonarQubeIssue[];
    measures: SonarQubeMeasures;
}
export declare class SonarQubeClient {
    private config;
    constructor(config: SonarQubeConfig);
    analyze(code: string, options: SonarQubeAnalysisOptions): Promise<SonarQubeAnalysisResult>;
    private getMetricValue;
}
export {};
