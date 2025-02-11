"""
Developer tools for MCP providing shell command execution, text editing, and testing capabilities.
"""

import subprocess
from pathlib import Path
from typing import Any, Optional

from anthropic.types.beta import BetaToolUnionParam

from ..base import BaseCognitiveTool, CognitiveToolResult


class DeveloperTool(BaseCognitiveTool):
    """Tool for development operations including shell commands, text editing, and testing."""

    name = "developer_tool"
    description = "Executes development operations like shell commands, text editing, and testing."

    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize the developer tool.

        Args:
            workspace_root: Root directory for workspace operations. Defaults to current directory.
        """
        self.workspace_root = workspace_root or Path.cwd()

    def __call__(self, **kwargs) -> CognitiveToolResult:
        """Execute a development operation.

        Args:
            operation: The operation to perform ('shell', 'edit', 'test')
            command: Shell command to execute (for 'shell' operation)
            file_path: Path to file to edit (for 'edit' operation)
            content: New content for file (for 'edit' operation)
            test_args: Arguments for test execution (for 'test' operation)
        """
        if not self.validate_args(**kwargs):
            return CognitiveToolResult(
                success=False,
                error="Invalid arguments provided"
            )

        operation = kwargs.get('operation')
        try:
            if operation == 'shell':
                result = self._execute_shell(kwargs['command'])
            elif operation == 'edit':
                result = self._edit_file(kwargs['file_path'], kwargs['content'])
            elif operation == 'test':
                result = self._run_tests(kwargs.get('test_args', []))
            else:
                return CognitiveToolResult(
                    success=False,
                    error=f"Unknown operation: {operation}"
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
                            "enum": ["shell", "edit", "test"],
                            "description": "Operation to perform"
                        },
                        "command": {
                            "type": "string",
                            "description": "Shell command to execute"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Path to file to edit"
                        },
                        "content": {
                            "type": "string",
                            "description": "New content for file"
                        },
                        "test_args": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Arguments for test execution"
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
        if operation == 'shell' and 'command' not in kwargs:
            return False
        elif operation == 'edit' and ('file_path' not in kwargs or 'content' not in kwargs):
            return False

        return True

    def _execute_shell(self, command: str) -> dict[str, Any]:
        """Execute a shell command."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.workspace_root
            )
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except subprocess.SubprocessError as e:
            raise RuntimeError(f"Shell command failed: {str(e)}")

    def _edit_file(self, file_path: str, content: str) -> dict[str, Any]:
        """Edit a file with new content."""
        try:
            path = self.workspace_root / file_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return {
                'path': str(path),
                'size': path.stat().st_size
            }
        except IOError as e:
            raise RuntimeError(f"File editing failed: {str(e)}")

    def _run_tests(self, test_args: list[str]) -> dict[str, Any]:
        """Run tests with specified arguments."""
        command = ['pytest'] + test_args
        return self._execute_shell(' '.join(command))