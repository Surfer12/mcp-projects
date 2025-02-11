"""
MCP Server Management functionality.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List
import requests

from mcp.tools.integrated import (
    DeveloperTool,
    AdvancedDeveloperTools,
    MemoryTool,
    VisualizationTool
)

class MCPServerManager:
    """Manager for MCP servers and tools."""

    def __init__(self, config_path: Path = None):
        """Initialize the server manager.

        Args:
            config_path: Path to config file. Defaults to ~/.mcp/servers.json
        """
        self.config_path = config_path or Path.home() / '.mcp' / 'servers.json'
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.servers = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load server configuration."""
        if self.config_path.exists():
            return json.loads(self.config_path.read_text())
        return {"servers": {}}

    def _save_config(self):
        """Save server configuration."""
        self.config_path.write_text(json.dumps(self.servers, indent=2))

    def add_server(
        self,
        name: str,
        url: str,
        tools: List[str] = None,
        description: str = ""
    ) -> bool:
        """Add a new MCP server."""
        if name in self.servers["servers"]:
            print(f"Server '{name}' already exists", file=sys.stderr)
            return False

        try:
            response = requests.get(f"{url}/health")
            response.raise_for_status()
        except Exception as e:
            print(f"Error connecting to server: {e}", file=sys.stderr)
            return False

        self.servers["servers"][name] = {
            "url": url,
            "tools": tools or [],
            "description": description,
            "status": "active"
        }
        self._save_config()
        return True

    def remove_server(self, name: str) -> bool:
        """Remove an MCP server."""
        if name not in self.servers["servers"]:
            print(f"Server '{name}' not found", file=sys.stderr)
            return False

        del self.servers["servers"][name]
        self._save_config()
        return True

    def list_servers(self) -> List[Dict[str, Any]]:
        """List all configured servers."""
        return [
            {"name": name, **config}
            for name, config in self.servers["servers"].items()
        ]

    def add_tools(self, name: str, tools: List[str]) -> bool:
        """Add tools to a server."""
        if name not in self.servers["servers"]:
            print(f"Server '{name}' not found", file=sys.stderr)
            return False

        server = self.servers["servers"][name]
        url = server["url"]

        valid_tools = {
            "dev": DeveloperTool,
            "advanced-dev": AdvancedDeveloperTools,
            "memory": MemoryTool,
            "visualization": VisualizationTool
        }

        invalid_tools = set(tools) - set(valid_tools.keys())
        if invalid_tools:
            print(f"Invalid tools: {', '.join(invalid_tools)}", file=sys.stderr)
            return False

        try:
            for tool in tools:
                if tool not in server["tools"]:
                    response = requests.post(
                        f"{url}/tools",
                        json={"tool": tool}
                    )
                    response.raise_for_status()
                    server["tools"].append(tool)

            self._save_config()
            return True

        except Exception as e:
            print(f"Error adding tools: {e}", file=sys.stderr)
            return False

    def remove_tools(self, name: str, tools: List[str]) -> bool:
        """Remove tools from a server."""
        if name not in self.servers["servers"]:
            print(f"Server '{name}' not found", file=sys.stderr)
            return False

        server = self.servers["servers"][name]
        url = server["url"]

        try:
            for tool in tools:
                if tool in server["tools"]:
                    response = requests.delete(
                        f"{url}/tools/{tool}"
                    )
                    response.raise_for_status()
                    server["tools"].remove(tool)

            self._save_config()
            return True

        except Exception as e:
            print(f"Error removing tools: {e}", file=sys.stderr)
            return False