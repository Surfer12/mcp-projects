"""Collection classes for managing multiple tools."""

from datetime import datetime
from typing import Any, Dict, List

from anthropic.types.beta import BetaToolUnionParam

from .base import (
    BaseAnthropicTool,
    MetaCognitiveState,
    TimeSeriesMetrics,
    ToolError,
    ToolFailure,
    ToolResult,
)


class MetaCognitiveWorkflowManager:
    def __init__(self):
        self.meta_state = MetaCognitiveState()
        self.metrics = TimeSeriesMetrics()
        self.workflow_history = []

    def record_workflow(self, workflow_data: Dict):
        self.workflow_history.append(workflow_data)
        self.meta_state.update(workflow_data)

        if "start_time" in workflow_data and "end_time" in workflow_data:
            self.metrics.record_operation(
                operation_type=workflow_data.get("tool"),
                start_time=workflow_data["start_time"],
                end_time=workflow_data["end_time"],
                metadata=workflow_data,
            )

    def analyze_workflow(self) -> Dict:
        return {
            "state": self.meta_state.current,
            "metrics": self.metrics.get_latest(),
            "patterns": self._analyze_patterns(),
        }

    def _analyze_patterns(self) -> List[Dict]:
        if not self.workflow_history:
            return []

        patterns = []

        # Analyze tool usage patterns
        tool_usage = {}
        for workflow in self.workflow_history:
            tool = workflow.get("tool")
            if tool:
                tool_usage[tool] = tool_usage.get(tool, 0) + 1

        if tool_usage:
            patterns.append({"type": "tool_usage_frequency", "data": tool_usage})

        # Analyze timing patterns
        if len(self.workflow_history) >= 2:
            intervals = []
            for i in range(len(self.workflow_history) - 1):
                start = datetime.fromisoformat(self.workflow_history[i]["timestamp"])
                end = datetime.fromisoformat(self.workflow_history[i + 1]["timestamp"])
                intervals.append((end - start).total_seconds())

            avg_interval = sum(intervals) / len(intervals)
            patterns.append(
                {"type": "workflow_timing", "average_interval": avg_interval}
            )

        return patterns


class ToolCollection:
    """A collection of anthropic-defined tools with monitoring capabilities."""

    def __init__(self, *tools: BaseAnthropicTool):
        self.tools = tools
        self.tool_map = {tool.to_params()["name"]: tool for tool in tools}
        self.workflow_manager = MetaCognitiveWorkflowManager()

    def to_params(self) -> list[BetaToolUnionParam]:
        return [tool.to_params() for tool in self.tools]

    async def run(self, *, name: str, tool_input: dict[str, Any]) -> ToolResult:
        # Record workflow start
        workflow_start = datetime.now()

        tool = self.tool_map.get(name)
        if not tool:
            return ToolFailure(error=f"Tool {name} is invalid")

        try:
            # Execute tool
            result = await tool(**tool_input)

            # Record workflow completion
            workflow_data = {
                "tool": name,
                "input": tool_input,
                "start_time": workflow_start,
                "end_time": datetime.now(),
                "result": result,
                "timestamp": datetime.now().isoformat(),
            }
            self.workflow_manager.record_workflow(workflow_data)

            # Add workflow analysis to result
            workflow_analysis = self.workflow_manager.analyze_workflow()
            return ToolResult(
                output=result.output if result else None,
                error=result.error if result else None,
                base64_image=result.base64_image if result else None,
                metrics=workflow_analysis["metrics"],
                patterns=workflow_analysis["patterns"],
            )

        except ToolError as e:
            error_data = {
                "tool": name,
                "input": tool_input,
                "error": e.message,
                "timestamp": datetime.now().isoformat(),
            }
            self.workflow_manager.record_workflow(error_data)
            return ToolFailure(error=e.message)

    def get_workflow_analysis(self) -> Dict:
        """Get the current workflow analysis."""
        return self.workflow_manager.analyze_workflow()
