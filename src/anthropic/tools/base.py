from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, fields, replace
from datetime import datetime
from typing import Any, Dict, List, Optional

from anthropic.types.beta import BetaToolUnionParam


class MetaCognitiveState:
    def __init__(self):
        self.current = {}
        self.history = []

    def update(self, operation: Dict):
        self.history.append(self.current.copy())
        self.current.update(operation)


class TimeSeriesMetrics:
    def __init__(self):
        self.data = {
            "operation_duration": [],
            "operation_frequency": [],
            "resource_usage": [],
            "error_rate": [],
        }

    def record_operation(
        self,
        operation_type: str,
        start_time: datetime,
        end_time: datetime,
        metadata: Dict,
    ):
        duration = (end_time - start_time).total_seconds()
        self.data["operation_duration"].append(
            {
                "timestamp": end_time,
                "value": duration,
                "operation": operation_type,
                "metadata": metadata,
            }
        )

    def get_latest(self) -> Dict:
        return {k: v[-1] if v else None for k, v in self.data.items()}


class BaseAnthropicTool(metaclass=ABCMeta):
    """Abstract base class for Anthropic-defined tools with monitoring capabilities."""

    def __init__(self):
        self.meta_state = MetaCognitiveState()
        self.metrics = TimeSeriesMetrics()
        self.operation_history = []

    @abstractmethod
    def __call__(self, **kwargs) -> Any:
        """Executes the tool with the given arguments."""
        ...

    @abstractmethod
    def to_params(self) -> BetaToolUnionParam:
        raise NotImplementedError

    def record_operation(self, operation: Dict, result: Any):
        """Record operation details and update metrics."""
        self.operation_history.append(
            {
                "operation": operation,
                "result": result,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.meta_state.update(operation)


@dataclass(kw_only=True, frozen=True)
class ToolResult:
    """Represents the result of a tool execution with monitoring data."""

    output: str | None = None
    error: str | None = None
    base64_image: str | None = None
    system: str | None = None
    metrics: Dict | None = None
    patterns: List[Dict] | None = None

    def __bool__(self):
        return any(getattr(self, field.name) for field in fields(self))

    def __add__(self, other: "ToolResult"):
        def combine_fields(
            field: str | None, other_field: str | None, concatenate: bool = True
        ):
            if field and other_field:
                if concatenate:
                    return field + other_field
                raise ValueError("Cannot combine tool results")
            return field or other_field

        return ToolResult(
            output=combine_fields(self.output, other.output),
            error=combine_fields(self.error, other.error),
            base64_image=combine_fields(self.base64_image, other.base64_image, False),
            system=combine_fields(self.system, other.system),
            metrics=self.metrics if self.metrics else other.metrics,
            patterns=self.patterns if self.patterns else other.patterns,
        )

    def replace(self, **kwargs):
        """Returns a new ToolResult with the given fields replaced."""
        return replace(self, **kwargs)


class CLIResult(ToolResult):
    """A ToolResult that can be rendered as a CLI output."""


class ToolFailure(ToolResult):
    """A ToolResult that represents a failure."""


class ToolError(Exception):
    """Raised when a tool encounters an error."""

    def __init__(self, message):
        self.message = message
