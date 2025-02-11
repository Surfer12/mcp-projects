import { EventEmitter } from 'events';

export class MCPServer extends EventEmitter {
  private tools: Map<string, MCPTool> = new Map();

  registerTool(tool: MCPTool) {
    this.tools.set(tool.id, tool);
    this.emit('tool_registered', tool);
  }

  async invokeTool(toolId: string, params: unknown) {
    const tool = this.tools.get(toolId);
    if (!tool) throw new Error(`Tool not found: ${toolId}`);

    try {
      const result = await tool.execute(params);
      this.emit('tool_executed', { toolId, result });
      return result;
    } catch (error) {
      this.emit('tool_error', { toolId, error });
      throw error;
    }
  }
}

export interface MCPTool {
  id: string;
  execute: (params: unknown) => Promise<unknown>;
}
