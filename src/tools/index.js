// Tool Management System
const path = require('path');
const fs = require('fs');

// Tool Categories
const TOOL_CATEGORIES = {
    AI: 'ai',
    WEB: 'web',
    GOOGLE: 'google',
    META: 'meta',
    PATTERN: 'pattern',
    WORKFLOW: 'workflow',
    CODE: 'code',
    CODE_ANALYSIS: 'code-analysis',
    ML_SERVICES: 'ml-services',
    INTEGRATED: 'integrated'
};

class ToolManager {
    constructor() {
        this.tools = new Map();
        this.initialized = false;
    }

    async initialize() {
        if (this.initialized) return;

        // Load tools from each category
        for (const category of Object.values(TOOL_CATEGORIES)) {
            const categoryPath = path.join(__dirname, category);
            if (fs.existsSync(categoryPath)) {
                try {
                    const files = fs.readdirSync(categoryPath);
                    for (const file of files) {
                        if (file.endsWith('.js') || file.endsWith('.ts')) {
                            const toolPath = path.join(category, file);
                            const toolModule = require(`./${toolPath}`);
                            if (toolModule.default) {
                                this.tools.set(`${category}/${file}`, new toolModule.default());
                            } else {
                                this.tools.set(`${category}/${file}`, toolModule);
                            }
                        }
                    }
                } catch (error) {
                    console.warn(`Failed to load tools from category ${category}:`, error);
                }
            }
        }

        this.initialized = true;
    }

    getTool(category, name) {
        const key = `${category}/${name}`;
        return this.tools.get(key);
    }

    getAllTools() {
        return Array.from(this.tools.entries()).map(([key, tool]) => ({
            path: key,
            tool
        }));
    }

    getToolsByCategory(category) {
        return Array.from(this.tools.entries())
            .filter(([key]) => key.startsWith(category))
            .map(([key, tool]) => ({
                path: key,
                tool
            }));
    }
}

// Export constants and manager
module.exports = {
    TOOL_CATEGORIES,
    ToolManager: new ToolManager(),
};