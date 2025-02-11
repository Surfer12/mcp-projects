"""Monitoring integration for computer use demo."""

import threading
import time
from typing import Dict, Optional

from prometheus_client import Counter, Gauge, Histogram, start_http_server


class PrometheusMonitoring:
    """Prometheus monitoring integration."""

    def __init__(self, port: int = 8000):
        self.port = port
        self._metrics = {}
        self._setup_metrics()
        self._start_server()

    def _setup_metrics(self):
        """Initialize Prometheus metrics."""
        # Tool execution metrics
        self._metrics["tool_execution_duration"] = Histogram(
            "computer_use_tool_execution_duration_seconds",
            "Duration of tool executions",
            ["tool_name", "action"],
        )

        self._metrics["tool_execution_total"] = Counter(
            "computer_use_tool_execution_total",
            "Total number of tool executions",
            ["tool_name", "action", "status"],
        )

        # Resource metrics
        self._metrics["resource_usage"] = Gauge(
            "computer_use_resource_usage", "Resource usage metrics", ["resource_type"]
        )

        # Pattern metrics
        self._metrics["pattern_detection_total"] = Counter(
            "computer_use_pattern_detection_total",
            "Total number of patterns detected",
            ["pattern_type"],
        )

        # Error metrics
        self._metrics["error_total"] = Counter(
            "computer_use_error_total",
            "Total number of errors",
            ["tool_name", "error_type"],
        )

    def _start_server(self):
        """Start Prometheus metrics server in a separate thread."""

        def run_server():
            start_http_server(self.port)
            while True:
                time.sleep(1)

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()

    def record_tool_execution(
        self, tool_name: str, action: str, duration: float, status: str = "success"
    ):
        """Record tool execution metrics."""
        self._metrics["tool_execution_duration"].labels(
            tool_name=tool_name, action=action
        ).observe(duration)

        self._metrics["tool_execution_total"].labels(
            tool_name=tool_name, action=action, status=status
        ).inc()

    def record_resource_usage(self, resource_type: str, value: float):
        """Record resource usage metrics."""
        self._metrics["resource_usage"].labels(resource_type=resource_type).set(value)

    def record_pattern_detection(self, pattern_type: str):
        """Record pattern detection metrics."""
        self._metrics["pattern_detection_total"].labels(pattern_type=pattern_type).inc()

    def record_error(self, tool_name: str, error_type: str):
        """Record error metrics."""
        self._metrics["error_total"].labels(
            tool_name=tool_name, error_type=error_type
        ).inc()


class MonitoringIntegration:
    """High-level monitoring integration for the computer use demo."""

    _instance: Optional["MonitoringIntegration"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.prometheus = PrometheusMonitoring()
            self.initialized = True

    def record_tool_metrics(self, tool_name: str, metrics_data: Dict):
        """Record tool execution metrics."""
        # Record execution metrics
        if "operation_duration" in metrics_data:
            duration = metrics_data["operation_duration"].get("value", 0)
            action = metrics_data["operation_duration"].get("operation", "unknown")
            self.prometheus.record_tool_execution(tool_name, action, duration)

        # Record resource usage
        if "resource_usage" in metrics_data:
            for resource_type, value in metrics_data["resource_usage"].items():
                self.prometheus.record_resource_usage(resource_type, value)

    def record_pattern_metrics(self, patterns: list):
        """Record pattern detection metrics."""
        for pattern in patterns:
            pattern_type = pattern.get("type", "unknown")
            self.prometheus.record_pattern_detection(pattern_type)

    def record_error(self, tool_name: str, error: str):
        """Record error metrics."""
        self.prometheus.record_error(tool_name, "execution_error")
