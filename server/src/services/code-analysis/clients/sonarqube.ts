import axios from 'axios';
import * as sonarqubeScanner from 'sonarqube-scanner';

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

export class SonarQubeClient {
  private config: SonarQubeConfig;

  constructor(config: SonarQubeConfig) {
    this.config = config;
  }

  async analyze(code: string, options: SonarQubeAnalysisOptions): Promise<SonarQubeAnalysisResult> {
    try {
      // Run SonarQube analysis
      await sonarqubeScanner({
        serverUrl: this.config.serverUrl,
        token: this.config.token,
        options: {
          'sonar.projectKey': options.projectKey,
          'sonar.sources': '.',
          'sonar.inclusions': '**/*.{js,ts,jsx,tsx}',
          'sonar.javascript.lcov.reportPaths': 'coverage/lcov.info',
        },
      });

      // Fetch analysis results
      const response = await axios.get(
        `${this.config.serverUrl}/api/issues/search?projectKeys=${options.projectKey}`,
        {
          headers: {
            Authorization: `Bearer ${this.config.token}`,
          },
        }
      );

      // Fetch metrics
      const metricsResponse = await axios.get(
        `${this.config.serverUrl}/api/measures/component?component=${options.projectKey}&metricKeys=complexity,duplicated_lines,coverage,bugs,vulnerabilities,code_smells`,
        {
          headers: {
            Authorization: `Bearer ${this.config.token}`,
          },
        }
      );

      return {
        issues: response.data.issues,
        measures: {
          complexity: this.getMetricValue(metricsResponse.data, 'complexity'),
          duplicatedLines: this.getMetricValue(metricsResponse.data, 'duplicated_lines'),
          coverage: this.getMetricValue(metricsResponse.data, 'coverage'),
          bugs: this.getMetricValue(metricsResponse.data, 'bugs'),
          vulnerabilities: this.getMetricValue(metricsResponse.data, 'vulnerabilities'),
          codeSmells: this.getMetricValue(metricsResponse.data, 'code_smells'),
        },
      };
    } catch (error) {
      console.error('SonarQube analysis failed:', error);
      throw new Error('Failed to perform SonarQube analysis');
    }
  }

  private getMetricValue(response: any, metricKey: string): number {
    const measure = response.component?.measures?.find((m: any) => m.metric === metricKey);
    return measure ? Number(measure.value) : 0;
  }
}