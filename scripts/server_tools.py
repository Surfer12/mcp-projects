#!/usr/bin/env python3
"""
Script for managing MCP servers and tools.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
from pydantic import BaseModel

from mcp.tools.integrated import (
    DeveloperTool,
    AdvancedDeveloperTools,
    MemoryTool,
    VisualizationTool
)

class ToolExecutionRequest(BaseModel):
    """Model for tool execution requests."""
    tool_name: str
    parameters: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

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
        """Add a new MCP server.

        Args:
            name: Server name
            url: Server URL
            tools: List of tools to enable
            description: Server description
        """
        if name in self.servers["servers"]:
            print(f"Server '{name}' already exists", file=sys.stderr)
            return False

        # Validate server URL
        try:
            response = requests.get(f"{url}/health")
            response.raise_for_status()
        except Exception as e:
            print(f"Error connecting to server: {e}", file=sys.stderr)
            return False

        # Add server configuration
        self.servers["servers"][name] = {
            "url": url,
            "tools": tools or [],
            "description": description,
            "status": "active"
        }
        self._save_config()
        return True

    def remove_server(self, name: str) -> bool:
        """Remove an MCP server.

        Args:
            name: Server name
        """
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
        """Add tools to a server.

        Args:
            name: Server name
            tools: List of tools to add
        """
        if name not in self.servers["servers"]:
            print(f"Server '{name}' not found", file=sys.stderr)
            return False

        server = self.servers["servers"][name]
        url = server["url"]

        # Validate tools
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

        # Add tools to server
        try:
            for tool in tools:
                if tool not in server["tools"]:
                    # Register tool with server
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
        """Remove tools from a server.

        Args:
            name: Server name
            tools: List of tools to remove
        """
        if name not in self.servers["servers"]:
            print(f"Server '{name}' not found", file=sys.stderr)
            return False

        server = self.servers["servers"][name]
        url = server["url"]

        try:
            for tool in tools:
                if tool in server["tools"]:
                    # Unregister tool from server
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

    def execute_tool(
        self,
        server_name: str,
        tool_name: str,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a tool on a specific server.

        Args:
            server_name: Name of the server to execute the tool on
            tool_name: Name of the tool to execute
            parameters: Tool parameters
            context: Optional execution context

        Returns:
            Tool execution results
        """
        if server_name not in self.servers["servers"]:
            raise ValueError(f"Server '{server_name}' not found")

        server = self.servers["servers"][server_name]
        url = f"{server['url']}/tools/{tool_name}/execute"

        request_data = ToolExecutionRequest(
            tool_name=tool_name,
            parameters=parameters,
            context=context
        )

        try:
            response = requests.post(url, json=request_data.dict())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to execute tool: {str(e)}")

    def get_tool_info(self, server_name: str, tool_name: str) -> Dict[str, Any]:
        """Get information about a specific tool.

        Args:
            server_name: Name of the server
            tool_name: Name of the tool

        Returns:
            Tool information
        """
        if server_name not in self.servers["servers"]:
            raise ValueError(f"Server '{server_name}' not found")

        server = self.servers["servers"][server_name]
        url = f"{server['url']}/tools/{tool_name}/info"

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to get tool info: {str(e)}")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MCP Server Management")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Add server command
    add_parser = subparsers.add_parser("add", help="Add MCP server")
    add_parser.add_argument("name", help="Server name")
    add_parser.add_argument("url", help="Server URL")
    add_parser.add_argument(
        "--tools",
        nargs="+",
        choices=["dev", "advanced-dev", "memory", "visualization"],
        help="Tools to enable"
    )
    add_parser.add_argument(
        "--description",
        help="Server description"
    )

    # Remove server command
    remove_parser = subparsers.add_parser("remove", help="Remove MCP server")
    remove_parser.add_argument("name", help="Server name")

    # List servers command
    list_parser = subparsers.add_parser("list", help="List MCP servers")
    list_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )

    # Add tools command
    tools_add_parser = subparsers.add_parser("tools-add", help="Add tools to server")
    tools_add_parser.add_argument("name", help="Server name")
    tools_add_parser.add_argument(
        "tools",
        nargs="+",
        choices=["dev", "advanced-dev", "memory", "visualization"],
        help="Tools to add"
    )

    # Remove tools command
    tools_remove_parser = subparsers.add_parser("tools-remove", help="Remove tools from server")
    tools_remove_parser.add_argument("name", help="Server name")
    tools_remove_parser.add_argument(
        "tools",
        nargs="+",
        help="Tools to remove"
    )

    # Execute command
    execute_parser = subparsers.add_parser("execute", help="Execute a tool on a server")
    execute_parser.add_argument("server", help="Server name")
    execute_parser.add_argument("tool", help="Tool name")
    execute_parser.add_argument(
        "--parameters",
        nargs="+",
        help="Tool parameters (format: key=value)"
    )
    execute_parser.add_argument(
        "--context",
        help="Execution context"
    )

    # Info command
    info_parser = subparsers.add_parser("info", help="Get tool information")
    info_parser.add_argument("server", help="Server name")
    info_parser.add_argument("tool", help="Tool name")

    # Common options
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to config file"
    )

    return parser.parse_args()


def format_server(server: Dict[str, Any]) -> str:
    """Format server information for text output."""
    return (
        f"Name: {server['name']}\n"
        f"URL: {server['url']}\n"
        f"Status: {server['status']}\n"
        f"Tools: {', '.join(server['tools']) if server['tools'] else 'None'}\n"
        f"Description: {server['description']}\n"
    )


def main() -> int:
    """Main entry point."""
    args = parse_args()
    manager = MCPServerManager(config_path=args.config)

    try:
        if args.command == "add":
            if manager.add_server(
                args.name,
                args.url,
                args.tools,
                args.description
            ):
                print(f"Successfully added server '{args.name}'")
                return 0
            return 1

        elif args.command == "remove":
            if manager.remove_server(args.name):
                print(f"Successfully removed server '{args.name}'")
                return 0
            return 1

        elif args.command == "list":
            servers = manager.list_servers()
            if args.format == "json":
                print(json.dumps(servers, indent=2))
            else:
                if not servers:
                    print("No servers configured")
                else:
                    for server in servers:
                        print("-" * 40)
                        print(format_server(server))
            return 0

        elif args.command == "tools-add":
            if manager.add_tools(args.name, args.tools):
                print(f"Successfully added tools to server '{args.name}'")
                return 0
            return 1

        elif args.command == "tools-remove":
            if manager.remove_tools(args.name, args.tools):
                print(f"Successfully removed tools from server '{args.name}'")
                return 0
            return 1

        elif args.command == "execute":
            # Parse parameters from command line
            params = {}
            if args.parameters:
                for param in args.parameters:
                    key, value = param.split("=", 1)
                    params[key] = value

            result = manager.execute_tool(
                args.server,
                args.tool,
                parameters=params,
                context=json.loads(args.context) if args.context else None
            )
            print(json.dumps(result, indent=2))
            return 0

        elif args.command == "info":
            info = manager.get_tool_info(args.server, args.tool)
            print(json.dumps(info, indent=2))
            return 0

        else:
            print("No command specified", file=sys.stderr)
            return 1

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())