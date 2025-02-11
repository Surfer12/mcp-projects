from typing import Dict, List, Type

from .base import BaseCognitiveTool, CognitiveToolResult
from .meta_analysis import MetaAnalysisTool
from .mojo_tools import MojoStructureTool


class CognitiveToolCollection:
    """Collection of tools for the cognitive framework."""

    def __init__(self):
        self.tools: Dict[str, BaseCognitiveTool] = {}
        self.tool_history: List[Dict] = []

    def register_tool(self, tool: BaseCognitiveTool) -> None:
        """Register a new tool in the collection."""
        if tool.name in self.tools:
            raise ValueError(f"Tool with name '{tool.name}' already registered")

        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> BaseCognitiveTool:
        """Get a tool by name."""
        if name not in self.tools:
            raise KeyError(f"Tool '{name}' not found")

        return self.tools[name]

    def list_tools(self) -> List[Dict]:
        """List all registered tools and their descriptions."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "version": tool.version,
            }
            for tool in self.tools.values()
        ]

    def to_anthropic_params(self) -> List[Dict]:
        """Convert all tools to Anthropic tool parameters."""
        return [tool.to_anthropic_param() for tool in self.tools.values()]

    def execute_tool(self, tool_name: str, **kwargs) -> CognitiveToolResult:
        """Execute a tool by name with the given arguments."""
        tool = self.get_tool(tool_name)

        # Record tool execution in history
        execution_record = {"tool": tool_name, "arguments": kwargs}

        try:
            result = tool(**kwargs)
            execution_record["success"] = result.success
            execution_record["result"] = result.data
            execution_record["metadata"] = result.metadata

            if not result.success:
                execution_record["error"] = result.error

            self.tool_history.append(execution_record)
            return result

        except Exception as e:
            execution_record["success"] = False
            execution_record["error"] = str(e)
            self.tool_history.append(execution_record)
            raise

    def get_tool_history(self) -> List[Dict]:
        """Get the history of tool executions."""
        return self.tool_history

    @classmethod
    def create_default_collection(
        cls, mojo_type_registry: Dict, analysis_config: Dict
    ) -> "CognitiveToolCollection":
        """Create a default tool collection with standard tools."""
        collection = cls()

        # Register standard tools
        collection.register_tool(MojoStructureTool(type_registry=mojo_type_registry))
        collection.register_tool(MetaAnalysisTool(analysis_config=analysis_config))

        return collection
