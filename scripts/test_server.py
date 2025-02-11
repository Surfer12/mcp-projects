#!/usr/bin/env python3
"""
Test server for MCP tools integration testing.
"""

from fastapi import FastAPI, HTTPException, Request
from typing import Dict, List, Optional
import uvicorn
import json
from pathlib import Path
from pydantic import BaseModel

class ToolRequest(BaseModel):
    """Model for tool execution requests."""
    tool_name: str
    parameters: Dict[str, any]
    context: Optional[Dict[str, any]] = None

app = FastAPI(title="MCP Test Server")

# Tool registry
AVAILABLE_TOOLS = {
    "dev": {
        "name": "dev",
        "description": "Development tools for code analysis and manipulation",
        "parameters": ["action", "target"]
    },
    "visualization": {
        "name": "visualization",
        "description": "Tools for data visualization and analysis",
        "parameters": ["data", "type"]
    }
}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/tools")
async def list_tools():
    """List available tools with their descriptions and parameters."""
    return {"tools": AVAILABLE_TOOLS}

@app.get("/status")
async def server_status():
    """Get server status."""
    return {
        "status": "running",
        "version": "1.0.0",
        "tools_enabled": True,
        "active_tools": len(AVAILABLE_TOOLS)
    }

@app.post("/tools/{tool_name}/execute")
async def execute_tool(tool_name: str, request: ToolRequest):
    """Execute a specific tool."""
    if tool_name not in AVAILABLE_TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

    # Validate parameters
    required_params = set(AVAILABLE_TOOLS[tool_name]["parameters"])
    provided_params = set(request.parameters.keys())

    if not required_params.issubset(provided_params):
        missing = required_params - provided_params
        raise HTTPException(
            status_code=400,
            detail=f"Missing required parameters: {', '.join(missing)}"
        )

    # Mock tool execution
    return {
        "tool": tool_name,
        "status": "success",
        "result": {
            "executed": True,
            "parameters": request.parameters,
            "context": request.context
        }
    }

@app.get("/tools/{tool_name}/info")
async def tool_info(tool_name: str):
    """Get detailed information about a specific tool."""
    if tool_name not in AVAILABLE_TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

    return AVAILABLE_TOOLS[tool_name]

def main():
    """Run the test server."""
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()