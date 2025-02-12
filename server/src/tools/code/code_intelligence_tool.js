const fs = require('fs').promises;
const path = require('path');

class CodeIntelligenceTool {
    constructor(aiTool) {
        this.aiTool = aiTool;
    }

    async analyzeProjectStructure(projectPath) {
        try {
            const projectAnalysis = {
                directories: [],
                files: [],
                summary: null
            };

            // Recursive directory traversal
            async function traverseDirectory(dirPath) {
                const entries = await fs.readdir(dirPath, { withFileTypes: true });
                
                for (const entry of entries) {
                    const fullPath = path.join(dirPath, entry.name);
                    
                    if (entry.isDirectory()) {
                        projectAnalysis.directories.push(fullPath);
                        await traverseDirectory(fullPath);
                    } else if (entry.isFile()) {
                        projectAnalysis.files.push(fullPath);
                    }
                }
            }

            // Start traversal
            await traverseDirectory(projectPath);

            // Generate summary using AI
            const summaryPrompt = `Analyze the following project structure:

            Directories: ${projectAnalysis.directories.join(', ')}
            Files: ${projectAnalysis.files.join(', ')}

            Please provide:
            1. Project type and potential framework
            2. Architectural overview
            3. Potential code organization improvements
            4. Estimated complexity and scalability assessment
            `;

            const summaryResponse = await this.aiTool.generateResponse({
                prompt: summaryPrompt,
                temperature: 0.3,
                provider: 'anthropic'
            });

            projectAnalysis.summary = summaryResponse.text;

            return projectAnalysis;
        } catch (error) {
            console.error('Project structure analysis failed:', error);
            throw new Error(`Failed to analyze project structure: ${error.message}`);
        }
    }

    async detectPotentialRefactoringOpportunities(code, language = 'javascript') {
        const prompt = `Analyze the following ${language} code and identify potential refactoring opportunities:

        \`\`\`${language}
        ${code}
        \`\`\`

        For each identified opportunity, provide:
        1. Specific refactoring suggestion
        2. Rationale for the refactoring
        3. Potential performance or readability improvements
        4. Complexity reduction strategies
        5. Estimated effort to implement the refactoring
        `;

        return this.aiTool.generateResponse({
            prompt,
            temperature: 0.4,
            provider: 'anthropic',
            systemPrompt: "You are an expert code architect specializing in code quality and refactoring."
        });
    }

    async generateArchitecturalRecommendations(projectStructure, existingArchitecture) {
        const prompt = `Analyze the following project architecture and provide strategic recommendations:

        Existing Architecture:
        ${existingArchitecture}

        Project Structure:
        ${JSON.stringify(projectStructure, null, 2)}

        Please provide:
        1. Architectural design patterns that could be applied
        2. Potential microservices or modularization strategies
        3. Scalability and performance optimization suggestions
        4. Technology stack recommendations
        5. Potential integration of design principles (SOLID, DRY, etc.)
        `;

        return this.aiTool.generateResponse({
            prompt,
            temperature: 0.3,
            provider: 'anthropic',
            systemPrompt: "You are a senior software architect providing strategic technical guidance."
        });
    }

    async compareImplementations(implementations) {
        const prompt = `Compare the following code implementations:

        ${implementations.map((impl, index) => 
            `Implementation ${index + 1} (${impl.language}):
            \`\`\`${impl.language}
            ${impl.code}
            \`\`\`
        `).join('\n\n')}

        For each implementation, analyze:
        1. Time complexity
        2. Space complexity
        3. Readability
        4. Potential performance bottlenecks
        5. Best practices adherence
        6. Recommendation for the most suitable implementation

        Provide a comprehensive comparative analysis.
        `;

        return this.aiTool.generateResponse({
            prompt,
            temperature: 0.4,
            provider: 'anthropic',
            systemPrompt: "You are a senior software engineer specializing in code performance and best practices."
        });
    }

    // Static method for generating test cases
    static generateTestCaseTemplate(functionSignature, language = 'javascript') {
        const testCaseTemplates = {
            'javascript': `
describe('${functionSignature}', () => {
    test('should handle normal case', () => {
        // Arrange
        
        // Act
        
        // Assert
        expect().toBe();
    });

    test('should handle edge cases', () => {
        // Arrange
        
        // Act
        
        // Assert
        expect().toThrow();
    });
});
            `,
            'python': `
def test_${functionSignature.replace(/\W+/g, '_')}():
    # Normal case
    def test_normal_case():
        # Arrange
        
        # Act
        
        # Assert
        assert 

    # Edge case
    def test_edge_case():
        # Arrange
        
        # Act
        
        # Assert
        with pytest.raises(Exception):
            pass
            `
        };

        return testCaseTemplates[language] || testCaseTemplates['javascript'];
    }
}

module.exports = CodeIntelligenceTool;