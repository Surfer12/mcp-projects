"""
Integration module for connecting all MCP components.
"""
from typing import Any, Dict, List, Optional
import asyncio
from datetime import datetime

from .base import BaseCognitiveTool, CognitiveToolResult
from .collection import MetaCognitiveToolCollection
from .evolution import CognitiveEvolutionTool
from .meta_analysis import MetaAnalysisTool
from ..tools import WebTool, GoogleTool, AnthropicTool
from ..visualization import PatternVisualizer

class IntegratedCognitiveSystem:
    """
    Central integration system that coordinates all MCP components.
    """
    def __init__(self):
        # Initialize tool collection
        self.tool_collection = MetaCognitiveToolCollection()

        # Initialize visualization
        self.visualizer = PatternVisualizer(style="whitegrid")

        # Initialize state tracking
        self.state = {
            "session_start": datetime.now().isoformat(),
            "operations": [],
            "patterns": [],
            "metrics": {}
        }

        # Set up tools
        self._setup_tools()

    def _setup_tools(self):
        """Initialize and register all tools."""
        # Core cognitive tools
        self.tool_collection.register_tool(
            MetaAnalysisTool(self._get_analysis_config())
        )
        self.tool_collection.register_tool(
            CognitiveEvolutionTool(self._get_evolution_config())
        )

        # External API tools
        self.tool_collection.register_tool(WebTool())
        self.tool_collection.register_tool(GoogleTool())
        self.tool_collection.register_tool(AnthropicTool())

    def _get_analysis_config(self) -> Dict[str, Any]:
        """Get meta-analysis configuration."""
        return {
            "pattern_analysis": {
                "min_pattern_frequency": 2,
                "max_pattern_depth": 3
            },
            "trend_analysis": {
                "window_size": 5,
                "min_trend_strength": 0.7
            }
        }

    def _get_evolution_config(self) -> Dict[str, Any]:
        """Get evolution configuration."""
        return {
            "mutation": {
                "rate": 0.2,
                "strength": 0.5
            },
            "adaptation": {
                "rate": 0.3
            },
            "pruning": {
                "threshold": 0.4
            }
        }

    async def process_input(
        self,
        input_data: Dict[str, Any],
        analysis_type: Optional[str] = None,
        visualization_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process input through all relevant components.

        Args:
            input_data: The input data to process
            analysis_type: Type of analysis to perform
            visualization_type: Type of visualization to generate

        Returns:
            Dict containing processed results
        """
        try:
            # Track operation start
            operation_start = datetime.now()

            # Process through tool collection
            result = await self.tool_collection.run(
                tool_name=input_data.get("tool", "meta_analysis"),
                tool_input={
                    "operation": input_data.get("operation", "analyze"),
                    "data": input_data.get("data", {}),
                    "analysis_type": analysis_type
                }
            )

            # Update state
            self._update_state(input_data, result, operation_start)

            # Generate visualizations if requested
            if visualization_type:
                viz_result = self._generate_visualization(
                    visualization_type,
                    result.data,
                    self.state
                )
                result.visualization = viz_result

            return {
                "success": True,
                "result": result.data,
                "meta_analysis": result.metadata,
                "state": self.state,
                "visualization": getattr(result, "visualization", None)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "state": self.state
            }

    def _update_state(
        self,
        input_data: Dict[str, Any],
        result: CognitiveToolResult,
        operation_start: datetime
    ):
        """Update system state with operation results."""
        operation_end = datetime.now()
        operation_duration = (operation_end - operation_start).total_seconds()

        operation = {
            "timestamp": operation_end.isoformat(),
            "input": input_data,
            "result": result.data,
            "duration": operation_duration,
            "tool": input_data.get("tool", "unknown")
        }

        self.state["operations"].append(operation)

        if hasattr(result, "patterns"):
            self.state["patterns"].extend(result.patterns)

        if hasattr(result, "metrics"):
            self.state["metrics"].update(result.metrics)

    def _generate_visualization(
        self,
        viz_type: str,
        data: Dict[str, Any],
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate visualization based on type and data."""
        try:
            if viz_type == "pattern":
                self.visualizer.plot_tool_usage_heatmap(
                    data.get("usage_data"),
                    title="Tool Usage Patterns"
                )
            elif viz_type == "network":
                self.visualizer.create_cognitive_network(
                    data.get("nodes", []),
                    data.get("edges", [])
                )
            elif viz_type == "performance":
                self.visualizer.plot_tool_performance(
                    data.get("performance_data"),
                    metric="execution_time"
                )

            return {
                "success": True,
                "type": viz_type,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "type": viz_type
            }

    async def cleanup(self):
        """Cleanup resources and save final state."""
        # Save final state
        final_state = {
            **self.state,
            "session_end": datetime.now().isoformat()
        }

        # Cleanup tool collection
        await self.tool_collection.cleanup()

        return final_state