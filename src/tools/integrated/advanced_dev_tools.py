"""
Advanced development tools for MCP providing CI, testing, linting, and documentation capabilities.
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Optional, List, Dict
from datetime import datetime

from anthropic.types.beta import BetaToolUnionParam

from ..base import BaseCognitiveTool, CognitiveToolResult
from .dev_tools import DeveloperTool
from .memory_tools import MemoryTool


class AdvancedDeveloperTools(BaseCognitiveTool):
    """Advanced development tools including CI, testing, linting, and documentation."""

    name = "advanced_dev_tool"
    description = "Executes advanced development operations like CI, testing, linting, and documentation."

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        memory_tool: Optional[MemoryTool] = None
    ):
        """Initialize the advanced developer tools.

        Args:
            workspace_root: Root directory for workspace operations
            memory_tool: MemoryTool instance for storing results
        """
        self.workspace_root = workspace_root or Path.cwd()
        self.dev_tool = DeveloperTool(workspace_root=workspace_root)
        self.memory_tool = memory_tool or MemoryTool()

    def __call__(self, **kwargs) -> CognitiveToolResult:
        """Execute an advanced development operation.

        Args:
            operation: The operation to perform ('test', 'lint', 'docs', 'container')
            test_type: Type of test to run ('tox', 'coverage', 'e2e')
            lint_type: Type of linting ('black', 'flake8', 'mypy', 'all')
            doc_type: Type of documentation ('sphinx', 'mkdocs')
            container_op: Container operation ('build', 'test', 'run')
            store_results: Whether to store results in memory
            extra_args: Additional arguments for the operation
        """
        if not self.validate_args(**kwargs):
            return CognitiveToolResult(
                success=False,
                error="Invalid arguments provided"
            )

        operation = kwargs.get('operation')
        try:
            if operation == 'test':
                result = self._run_tests(
                    kwargs.get('test_type', 'pytest'),
                    kwargs.get('extra_args', []),
                    kwargs.get('store_results', True)
                )
            elif operation == 'lint':
                result = self._run_linting(
                    kwargs.get('lint_type', 'all'),
                    kwargs.get('extra_args', []),
                    kwargs.get('store_results', True)
                )
            elif operation == 'docs':
                result = self._build_docs(
                    kwargs.get('doc_type', 'sphinx'),
                    kwargs.get('extra_args', [])
                )
            elif operation == 'container':
                result = self._container_ops(
                    kwargs.get('container_op', 'build'),
                    kwargs.get('extra_args', [])
                )
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
                            "enum": ["test", "lint", "docs", "container"],
                            "description": "Operation to perform"
                        },
                        "test_type": {
                            "type": "string",
                            "enum": ["tox", "coverage", "e2e"],
                            "description": "Type of test to run"
                        },
                        "lint_type": {
                            "type": "string",
                            "enum": ["black", "flake8", "mypy", "all"],
                            "description": "Type of linting"
                        },
                        "doc_type": {
                            "type": "string",
                            "enum": ["sphinx", "mkdocs"],
                            "description": "Type of documentation"
                        },
                        "container_op": {
                            "type": "string",
                            "enum": ["build", "test", "run"],
                            "description": "Container operation"
                        },
                        "store_results": {
                            "type": "boolean",
                            "description": "Whether to store results in memory"
                        },
                        "extra_args": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Additional arguments"
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
        valid_operations = {
            'test': ['tox', 'coverage', 'e2e'],
            'lint': ['black', 'flake8', 'mypy', 'all'],
            'docs': ['sphinx', 'mkdocs'],
            'container': ['build', 'test', 'run']
        }

        if operation not in valid_operations:
            return False

        if operation == 'test' and 'test_type' in kwargs:
            if kwargs['test_type'] not in valid_operations['test']:
                return False
        elif operation == 'lint' and 'lint_type' in kwargs:
            if kwargs['lint_type'] not in valid_operations['lint']:
                return False
        elif operation == 'docs' and 'doc_type' in kwargs:
            if kwargs['doc_type'] not in valid_operations['docs']:
                return False
        elif operation == 'container' and 'container_op' in kwargs:
            if kwargs['container_op'] not in valid_operations['container']:
                return False

        return True

    def _run_tests(
        self,
        test_type: str,
        extra_args: List[str],
        store_results: bool
    ) -> Dict[str, Any]:
        """Run tests with the specified configuration."""
        timestamp = datetime.utcnow().isoformat()
        result = {}

        if test_type == 'tox':
            # Run tox for multi-environment testing
            cmd_result = self.dev_tool(
                operation='shell',
                command=f"tox {' '.join(extra_args)}"
            )
            result['tox'] = cmd_result.data

        elif test_type == 'coverage':
            # Run pytest with coverage
            cmd_result = self.dev_tool(
                operation='shell',
                command=f"pytest --cov=src --cov-report=html {' '.join(extra_args)}"
            )
            result['coverage'] = cmd_result.data

            # Parse coverage report
            if cmd_result.success:
                coverage_dir = self.workspace_root / 'htmlcov'
                if coverage_dir.exists():
                    result['coverage_report'] = str(coverage_dir)

        elif test_type == 'e2e':
            # Run end-to-end tests with playwright
            cmd_result = self.dev_tool(
                operation='shell',
                command=f"playwright test {' '.join(extra_args)}"
            )
            result['e2e'] = cmd_result.data

        # Store results if requested
        if store_results and result:
            self.memory_tool(
                operation='store',
                key=f"test_results_{test_type}_{timestamp}",
                data=result,
                tags=['test', test_type, timestamp[:10]]
            )

        return result

    def _run_linting(
        self,
        lint_type: str,
        extra_args: List[str],
        store_results: bool
    ) -> Dict[str, Any]:
        """Run linting with the specified configuration."""
        timestamp = datetime.utcnow().isoformat()
        result = {}

        if lint_type in ('black', 'all'):
            # Run black formatter
            cmd_result = self.dev_tool(
                operation='shell',
                command=f"black src tests {' '.join(extra_args)}"
            )
            result['black'] = cmd_result.data

        if lint_type in ('flake8', 'all'):
            # Run flake8
            cmd_result = self.dev_tool(
                operation='shell',
                command=f"flake8 src tests {' '.join(extra_args)}"
            )
            result['flake8'] = cmd_result.data

        if lint_type in ('mypy', 'all'):
            # Run mypy
            cmd_result = self.dev_tool(
                operation='shell',
                command=f"mypy src {' '.join(extra_args)}"
            )
            result['mypy'] = cmd_result.data

        # Store results if requested
        if store_results and result:
            self.memory_tool(
                operation='store',
                key=f"lint_results_{lint_type}_{timestamp}",
                data=result,
                tags=['lint', lint_type, timestamp[:10]]
            )

        return result

    def _build_docs(
        self,
        doc_type: str,
        extra_args: List[str]
    ) -> Dict[str, Any]:
        """Build documentation with the specified configuration."""
        result = {}

        if doc_type == 'sphinx':
            # Build Sphinx documentation
            cmd_result = self.dev_tool(
                operation='shell',
                command=f"sphinx-build -b html docs/source docs/build/html {' '.join(extra_args)}"
            )
            result['sphinx'] = cmd_result.data

            # Check for built documentation
            docs_dir = self.workspace_root / 'docs/build/html'
            if docs_dir.exists():
                result['docs_path'] = str(docs_dir)

        elif doc_type == 'mkdocs':
            # Build MkDocs documentation
            cmd_result = self.dev_tool(
                operation='shell',
                command=f"mkdocs build {' '.join(extra_args)}"
            )
            result['mkdocs'] = cmd_result.data

            # Check for built documentation
            site_dir = self.workspace_root / 'site'
            if site_dir.exists():
                result['docs_path'] = str(site_dir)

        return result

    def _container_ops(
        self,
        container_op: str,
        extra_args: List[str]
    ) -> Dict[str, Any]:
        """Perform container operations."""
        result = {}

        if container_op == 'build':
            # Build container
            cmd_result = self.dev_tool(
                operation='shell',
                command=f"docker build -t mcp . {' '.join(extra_args)}"
            )
            result['build'] = cmd_result.data

        elif container_op == 'test':
            # Run tests in container
            cmd_result = self.dev_tool(
                operation='shell',
                command=f"docker run --rm mcp pytest {' '.join(extra_args)}"
            )
            result['test'] = cmd_result.data

        elif container_op == 'run':
            # Run container
            cmd_result = self.dev_tool(
                operation='shell',
                command=f"docker run --rm mcp {' '.join(extra_args)}"
            )
            result['run'] = cmd_result.data

        return result