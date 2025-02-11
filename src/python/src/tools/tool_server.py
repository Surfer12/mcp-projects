"""
Tool server for handling integration between JavaScript and Python components.
"""
import asyncio
import json
import sys
from typing import Dict, Any

from cognitive_framework.tools import (
    CognitiveToolCollection,
    MetaAnalysisTool,
    CognitiveEvolutionTool,
    MetaCognitiveToolCollection
)
from web_tool import WebTool
from google_tool import GoogleTool
from mojo_tools import MojoStructureTool
from visualization.pattern_viz import PatternVisualizer

class ToolServer:
    def __init__(self):
        # Initialize tool configuration
        self.tool_configs = {
            "analysis_config": {
                "pattern_analysis": {
                    "min_pattern_frequency": 2,
                    "max_pattern_depth": 3
                },
                "trend_analysis": {
                    "window_size": 5,
                    "min_trend_strength": 0.7
                }
            },
            "evolution_config": {
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
            },
            "mojo_type_registry": {
                "Concept": dict,
                "Process": dict,
                "Framework": dict
            }
        }

        # Initialize visualization
        self.pattern_visualizer = PatternVisualizer(style="whitegrid")

        # Initialize tool collection with meta-cognitive capabilities
        self.tool_collection = MetaCognitiveToolCollection()
        self.setup_tools()

    def setup_tools(self):
        """Initialize and register all tools."""
        # Register meta-analysis tool
        self.tool_collection.register_tool(
            MetaAnalysisTool(self.tool_configs["analysis_config"])
        )

        # Register evolution tool
        self.tool_collection.register_tool(
            CognitiveEvolutionTool(self.tool_configs["evolution_config"])
        )

        # Register web tool
        self.tool_collection.register_tool(WebTool())

        # Register Google tool
        self.tool_collection.register_tool(GoogleTool())

        # Register Mojo structure tool
        self.tool_collection.register_tool(
            MojoStructureTool(self.tool_configs["mojo_type_registry"])
        )

    async def process_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input from Node.js and return results."""
        action = data.get("action")
        input_data = data.get("data", {})

        action_handlers = {
            "analyze": self.handle_analysis,
            "evolve": self.handle_evolution,
            "web_request": self.handle_web_request,
            "google_search": self.handle_google_search,
            "mojo_structure": self.handle_mojo_structure,
            "visualize": self.handle_visualization
        }

        handler = action_handlers.get(action)
        if handler:
            return await handler(input_data)
        else:
            return {
                "error": f"Unknown action: {action}",
                "success": False
            }

    async def handle_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle meta-analysis requests."""
        try:
            result = await self.tool_collection.run(
                "meta_analysis",
                {
                    "operation": "pattern_analysis",
                    "data": [data],
                    "analysis_type": data.get("analysis_type", "structural")
                }
            )

            return {
                "success": True,
                "patterns": result.data.get("patterns", {}),
                "metrics": result.data.get("metrics", {}),
                "timestamp": data.get("timestamp")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def handle_evolution(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle cognitive evolution requests."""
        try:
            result = await self.tool_collection.run(
                "cognitive_evolution",
                {
                    "operation": data.get("operation", "adapt"),
                    "target": data.get("target", "concept"),
                    "data": data,
                    "context": data.get("context", {})
                }
            )

            return {
                "success": True,
                "evolved_data": result.data,
                "timestamp": data.get("timestamp")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def handle_web_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle web requests."""
        try:
            result = await self.tool_collection.run(
                "web_tool",
                {
                    "url": data.get("url"),
                    "method": data.get("method", "GET"),
                    "params": data.get("params"),
                    "headers": data.get("headers")
                }
            )

            return {
                "success": True,
                "response": result.data,
                "timestamp": data.get("timestamp")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def handle_google_search(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Google API requests."""
        try:
            result = await self.tool_collection.run(
                "google_tool",
                {
                    "query": data.get("query"),
                    "type": data.get("type", "search"),
                    "params": data.get("params", {})
                }
            )

            return {
                "success": True,
                "results": result.data,
                "timestamp": data.get("timestamp")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def handle_mojo_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Mojo structure operations."""
        try:
            result = await self.tool_collection.run(
                "mojo_structure",
                {
                    "operation": data.get("operation"),
                    "structure_type": data.get("structure_type"),
                    "data": data.get("data")
                }
            )

            return {
                "success": True,
                "result": result.data,
                "timestamp": data.get("timestamp")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def handle_visualization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle visualization requests."""
        try:
            viz_type = data.get("type", "pattern")
            viz_data = data.get("data", {})

            if viz_type == "pattern":
                self.pattern_visualizer.plot_tool_usage_heatmap(
                    viz_data.get("usage_data"),
                    title=viz_data.get("title", "Tool Usage Patterns")
                )
            elif viz_type == "network":
                self.pattern_visualizer.create_cognitive_network(
                    viz_data.get("nodes", []),
                    viz_data.get("edges", [])
                )
            elif viz_type == "performance":
                self.pattern_visualizer.plot_tool_performance(
                    viz_data.get("performance_data"),
                    metric=viz_data.get("metric", "execution_time")
                )

            return {
                "success": True,
                "visualization_type": viz_type,
                "timestamp": data.get("timestamp")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def run(self):
        """Main server loop."""
        while True:
            try:
                # Read input from Node.js
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                if not line:
                    break

                # Parse input data
                data = json.loads(line)

                # Process the request
                result = await self.process_input(data)

                # Send response back to Node.js
                print(json.dumps(result), flush=True)

            except json.JSONDecodeError:
                print(json.dumps({
                    "success": False,
                    "error": "Invalid JSON input"
                }), flush=True)
            except Exception as e:
                print(json.dumps({
                    "success": False,
                    "error": str(e)
                }), flush=True)

if __name__ == "__main__":
    server = ToolServer()
    asyncio.run(server.run())