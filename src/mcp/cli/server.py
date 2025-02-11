"""
MCP Server Management CLI.
"""

import json
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from mcp.server.manager import MCPServerManager

app = typer.Typer(help="MCP Server Management CLI")
console = Console()

@app.command()
def add(
    name: str = typer.Argument(..., help="Server name"),
    url: str = typer.Argument(..., help="Server URL"),
    tools: Optional[List[str]] = typer.Option(
        None,
        help="Tools to enable",
        autocompletion=lambda: ["dev", "advanced-dev", "memory", "visualization"]
    ),
    description: str = typer.Option("", help="Server description"),
    config: Optional[Path] = typer.Option(None, help="Path to config file")
):
    """Add a new MCP server."""
    manager = MCPServerManager(config_path=config)
    if manager.add_server(name, url, tools, description):
        console.print(f"[green]Successfully added server '{name}'[/green]")
    else:
        raise typer.Exit(code=1)

@app.command()
def remove(
    name: str = typer.Argument(..., help="Server name"),
    config: Optional[Path] = typer.Option(None, help="Path to config file")
):
    """Remove an MCP server."""
    manager = MCPServerManager(config_path=config)
    if manager.remove_server(name):
        console.print(f"[green]Successfully removed server '{name}'[/green]")
    else:
        raise typer.Exit(code=1)

@app.command()
def list_servers(
    output_format: str = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format",
        autocompletion=lambda: ["table", "json"]
    ),
    config: Optional[Path] = typer.Option(None, help="Path to config file")
):
    """List all configured servers."""
    manager = MCPServerManager(config_path=config)
    servers = manager.list_servers()

    if not servers:
        console.print("[yellow]No servers configured[/yellow]")
        return

    if output_format == "json":
        console.print_json(json.dumps(servers, indent=2))
        return

    # Create rich table
    table = Table(title="MCP Servers")
    table.add_column("Name", style="cyan")
    table.add_column("URL", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Tools", style="blue")
    table.add_column("Description")

    for server in servers:
        table.add_row(
            server["name"],
            server["url"],
            server["status"],
            ", ".join(server["tools"]) if server["tools"] else "None",
            server["description"] or "No description"
        )

    console.print(table)

@app.command()
def add_tools(
    name: str = typer.Argument(..., help="Server name"),
    tools: List[str] = typer.Argument(
        ...,
        help="Tools to add",
        autocompletion=lambda: ["dev", "advanced-dev", "memory", "visualization"]
    ),
    config: Optional[Path] = typer.Option(None, help="Path to config file")
):
    """Add tools to a server."""
    manager = MCPServerManager(config_path=config)
    if manager.add_tools(name, tools):
        console.print(f"[green]Successfully added tools to server '{name}'[/green]")
    else:
        raise typer.Exit(code=1)

@app.command()
def remove_tools(
    name: str = typer.Argument(..., help="Server name"),
    tools: List[str] = typer.Argument(..., help="Tools to remove"),
    config: Optional[Path] = typer.Option(None, help="Path to config file")
):
    """Remove tools from a server."""
    manager = MCPServerManager(config_path=config)
    if manager.remove_tools(name, tools):
        console.print(f"[green]Successfully removed tools from server '{name}'[/green]")
    else:
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()