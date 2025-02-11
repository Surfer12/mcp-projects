"""
Integration layer for Node.js and Python components.
"""
import asyncio
import json
import sys
from typing import Any, Dict, Optional

from ..core.integration import IntegratedCognitiveSystem

class NodeJSIntegration:
    """
    Handles communication between Node.js and Python components.
    """
    def __init__(self):
        self.cognitive_system = IntegratedCognitiveSystem()
        self.input_queue = asyncio.Queue()
        self.output_queue = asyncio.Queue()

    async def handle_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input from Node.js."""
        try:
            action = data.get("action")
            if not action:
                return {
                    "success": False,
                    "error": "No action specified"
                }

            handlers = {
                "process": self._handle_process,
                "analyze": self._handle_analyze,
                "visualize": self._handle_visualize,
                "cleanup": self._handle_cleanup
            }

            handler = handlers.get(action)
            if not handler:
                return {
                    "success": False,
                    "error": f"Unknown action: {action}"
                }

            return await handler(data.get("data", {}))

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _handle_process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general processing requests."""
        return await self.cognitive_system.process_input(
            input_data=data,
            analysis_type=data.get("analysis_type"),
            visualization_type=data.get("visualization_type")
        )

    async def _handle_analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle analysis-specific requests."""
        return await self.cognitive_system.process_input(
            input_data={
                "tool": "meta_analysis",
                "operation": "analyze",
                "data": data
            },
            analysis_type=data.get("type", "structural")
        )

    async def _handle_visualize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle visualization requests."""
        return await self.cognitive_system.process_input(
            input_data=data,
            visualization_type=data.get("type", "pattern")
        )

    async def _handle_cleanup(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle cleanup requests."""
        final_state = await self.cognitive_system.cleanup()
        return {
            "success": True,
            "final_state": final_state
        }

    async def run(self):
        """Main processing loop."""
        while True:
            try:
                # Read input from Node.js
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                if not line:
                    break

                # Parse input data
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    print(json.dumps({
                        "success": False,
                        "error": "Invalid JSON input"
                    }), flush=True)
                    continue

                # Process the request
                result = await self.handle_input(data)

                # Send response back to Node.js
                print(json.dumps(result), flush=True)

            except Exception as e:
                print(json.dumps({
                    "success": False,
                    "error": str(e)
                }), flush=True)

def main():
    """Entry point for Node.js integration."""
    integration = NodeJSIntegration()
    asyncio.run(integration.run())

if __name__ == "__main__":
    main()