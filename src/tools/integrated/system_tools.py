"""
Computer control tools for MCP providing system automation and web interaction capabilities.
"""

import json
import os
import platform
import subprocess
from pathlib import Path
from typing import Any, Optional
import requests

from anthropic.types.beta import BetaToolUnionParam

from ..base import BaseCognitiveTool, CognitiveToolResult


class ComputerControlTool(BaseCognitiveTool):
    """Tool for computer control operations including system automation and web interactions."""

    name = "computer_control_tool"
    description = "Executes system automation and web interaction operations."

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize the computer control tool.

        Args:
            cache_dir: Directory for caching web results. Defaults to ~/.mcp/cache
        """
        self.cache_dir = cache_dir or Path.home() / '.mcp' / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._setup_platform()

    def __call__(self, **kwargs) -> CognitiveToolResult:
        """Execute a computer control operation.

        Args:
            operation: The operation to perform ('applescript', 'web_search', 'web_fetch', 'cache')
            script: AppleScript to execute (for 'applescript' operation)
            query: Search query (for 'web_search' operation)
            url: URL to fetch (for 'web_fetch' operation)
            cache_key: Key for cache operations (for 'cache' operation)
            cache_data: Data to cache (for 'cache' operation)
        """
        if not self.validate_args(**kwargs):
            return CognitiveToolResult(
                success=False,
                error="Invalid arguments provided"
            )

        operation = kwargs.get('operation')
        try:
            if operation == 'applescript' and self.is_macos:
                result = self._run_applescript(kwargs['script'])
            elif operation == 'web_search':
                result = self._web_search(kwargs['query'])
            elif operation == 'web_fetch':
                result = self._web_fetch(kwargs['url'])
            elif operation == 'cache':
                if 'cache_data' in kwargs:
                    result = self._cache_write(kwargs['cache_key'], kwargs['cache_data'])
                else:
                    result = self._cache_read(kwargs['cache_key'])
            else:
                return CognitiveToolResult(
                    success=False,
                    error=f"Unknown or unsupported operation: {operation}"
                )

            return CognitiveToolResult(
                success=True,
                data=result
            )
        except Exception as e:
            return CognitiveToolResult(
                success=False,
                error=str(e)
            )

    def to_anthropic_param(self) -> BetaToolUnionParam:
        """Convert to Anthropic tool parameter format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["applescript", "web_search", "web_fetch", "cache"],
                            "description": "Operation to perform"
                        },
                        "script": {
                            "type": "string",
                            "description": "AppleScript to execute"
                        },
                        "query": {
                            "type": "string",
                            "description": "Search query for web search"
                        },
                        "url": {
                            "type": "string",
                            "description": "URL to fetch"
                        },
                        "cache_key": {
                            "type": "string",
                            "description": "Key for cache operations"
                        },
                        "cache_data": {
                            "type": "object",
                            "description": "Data to cache"
                        }
                    },
                    "required": ["operation"]
                }
            }
        }

    def validate_args(self, **kwargs) -> bool:
        """Validate the arguments for this tool."""
        if 'operation' not in kwargs:
            return False

        operation = kwargs['operation']
        if operation == 'applescript' and not self.is_macos:
            return False
        elif operation == 'applescript' and 'script' not in kwargs:
            return False
        elif operation == 'web_search' and 'query' not in kwargs:
            return False
        elif operation == 'web_fetch' and 'url' not in kwargs:
            return False
        elif operation == 'cache' and 'cache_key' not in kwargs:
            return False

        return True

    def _setup_platform(self):
        """Setup platform-specific configurations."""
        self.is_macos = platform.system().lower() == 'darwin'
        if self.is_macos:
            # Verify osascript is available
            try:
                subprocess.run(['which', 'osascript'], check=True, capture_output=True)
            except subprocess.SubprocessError:
                self.is_macos = False

    def _run_applescript(self, script: str) -> dict[str, Any]:
        """Execute an AppleScript."""
        if not self.is_macos:
            raise RuntimeError("AppleScript is only supported on macOS")

        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except subprocess.SubprocessError as e:
            raise RuntimeError(f"AppleScript execution failed: {str(e)}")

    def _web_search(self, query: str) -> dict[str, Any]:
        """Perform a web search using DuckDuckGo."""
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _web_fetch(self, url: str) -> dict[str, Any]:
        """Fetch content from a URL."""
        response = requests.get(url)
        response.raise_for_status()
        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text
        }

    def _cache_write(self, key: str, data: Any) -> dict[str, Any]:
        """Write data to cache."""
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps(data))
        return {
            'path': str(cache_file),
            'size': cache_file.stat().st_size
        }

    def _cache_read(self, key: str) -> Any:
        """Read data from cache."""
        cache_file = self.cache_dir / f"{key}.json"
        if not cache_file.exists():
            return None
        return json.loads(cache_file.read_text())