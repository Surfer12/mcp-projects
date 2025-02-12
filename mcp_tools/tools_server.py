# tools_server.py

from mcp.server.fastmcp import FastMCP
import os

# Initialize the MCP server
mcp = FastMCP("tools-server")

import sys
from typing import Any, List, Dict

# Logging tool registrations with decorator
def log_tool_registration(tool):
    print(f"Registered tool: {tool.__name__}", file=sys.stderr)
    return tool

# Tool: Sum two numbers
@mcp.tool()
@log_tool_registration
def generate_sum(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

# Tool: Analyze text
@mcp.tool()
@log_tool_registration
def analyze_text(text: str) -> dict[str, Any]:
    """Analyze text for word count and unique words."""
    words = text.split()
    return {
        "word_count": len(words),
        "unique_words": len(set(words))
    }

# Tool: List files in a directory
@mcp.tool()
@log_tool_registration
def list_files(directory: str) -> list[str]:
    """List all files in a directory."""
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except Exception as e:
        return {"error": str(e)}

print("Starting MCP Tools Server", file=sys.stderr)
mcp.run(transport="stdio")