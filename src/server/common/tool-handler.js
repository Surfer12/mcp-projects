const { ToolManager, TOOL_CATEGORIES } = require('../../tools');

class ToolHandler {
    constructor() {
        this.toolManager = ToolManager;
    }

    async initialize() {
        await this.toolManager.initialize();
    }

    async handleRequest(toolType, data) {
        // Map legacy tool names to new categories
        const categoryMap = {
            'llm_code_generate': TOOL_CATEGORIES.AI,
            'analyze_code': TOOL_CATEGORIES.CODE_ANALYSIS,
            'enhance_documentation': TOOL_CATEGORIES.CODE,
            'suggest_improvements': TOOL_CATEGORIES.CODE,
            'generate': TOOL_CATEGORIES.AI,
            'gemini_generate': TOOL_CATEGORIES.GOOGLE
        };

        const category = categoryMap[toolType] || toolType;
        const tools = this.toolManager.getToolsByCategory(category);

        if (tools.length === 0) {
            return { error: `No tools found for type: ${toolType}` };
        }

        // Use the first available tool in the category
        const { tool } = tools[0];

        try {
            return await tool.process(data);
        } catch (error) {
            console.error(`Error processing tool request:`, error);
            return { error: error.message || 'Tool processing failed' };
        }
    }

    getAvailableTools() {
        return this.toolManager.getAllTools().map(({ path }) => path);
    }
}

module.exports = new ToolHandler();