export interface AnalysisResult {
    issues: Array<{
        severity: 'BLOCKER' | 'CRITICAL' | 'MAJOR' | 'MINOR' | 'INFO';
        message: string;
        line?: number;
        file?: string;
    }>;
    metrics: {
        complexity: number;
        duplicatedLines: number;
        coverage?: number;
        bugs: number;
        vulnerabilities: number;
        codeSmells: number;
    };
}
export interface AnalyzeOptions {
    type: 'quality' | 'security' | 'full';
    projectKey?: string;
}
declare class CodeAnalyzers {
    private sonarqube;
    constructor();
    analyze(code: string, options: AnalyzeOptions): Promise<AnalysisResult>;
}
export declare const analyzers: CodeAnalyzers;
export {};
