"""
Visualization tools for MCP providing dashboard and pattern visualization capabilities.
"""

from pathlib import Path
from typing import Any, Optional, Union
import json
import asyncio
from datetime import datetime

from anthropic.types.beta import BetaToolUnionParam

from ..base import BaseCognitiveTool, CognitiveToolResult
from ...visualization import run_dashboard, PatternVisualizer


class VisualizationTool(BaseCognitiveTool):
    """Tool for visualization operations including dashboards and pattern visualization."""

    name = "visualization_tool"
    description = "Executes visualization operations for dashboards and patterns."

    def __init__(self, output_dir: Optional[Path] = None):
        """Initialize the visualization tool.

        Args:
            output_dir: Directory for storing visualization outputs. Defaults to ~/.mcp/viz
        """
        self.output_dir = output_dir or Path.home() / '.mcp' / 'viz'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._pattern_viz = PatternVisualizer()
        self._active_dashboard = None

    def __call__(self, **kwargs) -> CognitiveToolResult:
        """Execute a visualization operation.

        Args:
            operation: The operation to perform ('dashboard', 'pattern', 'save')
            data: Data to visualize
            pattern_type: Type of pattern to visualize (for 'pattern' operation)
            title: Title for the visualization
            description: Description of the visualization
            output_format: Format for saving visualization ('html', 'png', 'svg')
        """
        if not self.validate_args(**kwargs):
            return CognitiveToolResult(
                success=False,
                error="Invalid arguments provided"
            )

        operation = kwargs.get('operation')
        try:
            if operation == 'dashboard':
                result = self._run_dashboard(
                    kwargs['data'],
                    kwargs.get('title', 'MCP Dashboard'),
                    kwargs.get('description', '')
                )
            elif operation == 'pattern':
                result = self._visualize_pattern(
                    kwargs['data'],
                    kwargs['pattern_type'],
                    kwargs.get('title', ''),
                    kwargs.get('description', '')
                )
            elif operation == 'save':
                result = self._save_visualization(
                    kwargs['data'],
                    kwargs.get('output_format', 'html'),
                    kwargs.get('title', '')
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
                            "enum": ["dashboard", "pattern", "save"],
                            "description": "Operation to perform"
                        },
                        "data": {
                            "type": "object",
                            "description": "Data to visualize"
                        },
                        "pattern_type": {
                            "type": "string",
                            "description": "Type of pattern to visualize"
                        },
                        "title": {
                            "type": "string",
                            "description": "Title for the visualization"
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the visualization"
                        },
                        "output_format": {
                            "type": "string",
                            "enum": ["html", "png", "svg"],
                            "description": "Format for saving visualization"
                        }
                    },
                    "required": ["operation", "data"]
                }
            }
        }

    def validate_args(self, **kwargs) -> bool:
        """Validate the arguments for this tool."""
        if 'operation' not in kwargs or 'data' not in kwargs:
            return False

        operation = kwargs['operation']
        if operation == 'pattern' and 'pattern_type' not in kwargs:
            return False

        return True

    def _run_dashboard(
        self,
        data: Any,
        title: str,
        description: str
    ) -> dict[str, Any]:
        """Run the MCP dashboard with the provided data."""
        # Store the dashboard data
        dashboard_file = self.output_dir / 'dashboard_data.json'
        dashboard_file.write_text(json.dumps({
            'title': title,
            'description': description,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }))

        # Run the dashboard in the background
        if self._active_dashboard:
            self._active_dashboard.cancel()

        self._active_dashboard = asyncio.create_task(
            run_dashboard(data, title=title, description=description)
        )

        return {
            'status': 'running',
            'data_file': str(dashboard_file)
        }

    def _visualize_pattern(
        self,
        data: Any,
        pattern_type: str,
        title: str,
        description: str
    ) -> dict[str, Any]:
        """Visualize a pattern in the data."""
        # Generate the visualization
        viz_data = self._pattern_viz.visualize(
            data,
            pattern_type=pattern_type,
            title=title,
            description=description
        )

        # Store the visualization data
        output_file = self.output_dir / f'pattern_{datetime.utcnow().isoformat()}.json'
        output_file.write_text(json.dumps({
            'pattern_type': pattern_type,
            'title': title,
            'description': description,
            'data': viz_data
        }))

        return {
            'visualization': viz_data,
            'output_file': str(output_file)
        }

    def _save_visualization(
        self,
        data: Any,
        output_format: str = 'html',
        title: str = ''
    ) -> dict[str, Any]:
        """Save a visualization in the specified format."""
        timestamp = datetime.utcnow().isoformat()
        base_name = f"{title.lower().replace(' ', '_')}_{timestamp}" if title else f"viz_{timestamp}"
        output_file = self.output_dir / f"{base_name}.{output_format}"

        if output_format == 'html':
            # Save as interactive HTML
            self._pattern_viz.to_html(data, output_file)
        else:
            # Save as static image
            self._pattern_viz.to_image(data, output_file, format=output_format)

        return {
            'format': output_format,
            'output_file': str(output_file)
        }