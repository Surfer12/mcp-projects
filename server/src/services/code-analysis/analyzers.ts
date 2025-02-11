import { SonarQubeClient } from './clients/sonarqube';

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

class CodeAnalyzers {
  private sonarqube: SonarQubeClient;

  constructor() {
    this.sonarqube = new SonarQubeClient({
      serverUrl: process.env.SONARQUBE_URL || 'http://localhost:9000',
      token: process.env.SONARQUBE_TOKEN || '',
    });
  }

  async analyze(code: string, options: AnalyzeOptions): Promise<AnalysisResult> {
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
    } catch (error) {
      console.error('Code analysis failed:', error);
      throw new Error('Failed to analyze code');
    }
  }
}

export const analyzers = new CodeAnalyzers();