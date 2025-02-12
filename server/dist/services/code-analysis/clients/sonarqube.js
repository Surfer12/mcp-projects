"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.SonarQubeClient = void 0;
const axios_1 = __importDefault(require("axios"));
const sonarqubeScanner = __importStar(require("sonarqube-scanner"));
class SonarQubeClient {
    constructor(config) {
        this.config = config;
    }
    async analyze(code, options) {
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
            const response = await axios_1.default.get(`${this.config.serverUrl}/api/issues/search?projectKeys=${options.projectKey}`, {
                headers: {
                    Authorization: `Bearer ${this.config.token}`,
                },
            });
            // Fetch metrics
            const metricsResponse = await axios_1.default.get(`${this.config.serverUrl}/api/measures/component?component=${options.projectKey}&metricKeys=complexity,duplicated_lines,coverage,bugs,vulnerabilities,code_smells`, {
                headers: {
                    Authorization: `Bearer ${this.config.token}`,
                },
            });
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
        }
        catch (error) {
            console.error('SonarQube analysis failed:', error);
            throw new Error('Failed to perform SonarQube analysis');
        }
    }
    getMetricValue(response, metricKey) {
        const measure = response.component?.measures?.find((m) => m.metric === metricKey);
        return measure ? Number(measure.value) : 0;
    }
}
exports.SonarQubeClient = SonarQubeClient;
//# sourceMappingURL=sonarqube.js.map