"""
Integrated MCP tools.
"""

class BaseTool:
    """Base class for all MCP tools."""
    def __init__(self, name: str):
        self.name = name

class DeveloperTool(BaseTool):
    """Basic developer tools."""
    def __init__(self):
        super().__init__("dev")

class AdvancedDeveloperTools(BaseTool):
    """Advanced developer tools."""
    def __init__(self):
        super().__init__("advanced-dev")

class MemoryTool(BaseTool):
    """Memory management tools."""
    def __init__(self):
        super().__init__("memory")

class VisualizationTool(BaseTool):
    """Visualization tools."""
    def __init__(self):
        super().__init__("visualization")