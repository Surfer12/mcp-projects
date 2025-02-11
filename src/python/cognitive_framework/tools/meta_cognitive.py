from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..context import SharedContext
from ..observers import (
    BoundaryObserver,
    ObservationCoordinator,
    StateObserver,
    TransformationObserver,
)
from ..visitors import (
    CompositionalVisitor,
    ParsingVisitor,
    TransformationVisitor,
    ValidationVisitor,
    VisitorCoordinator,
)
from .base import ToolCollection, ToolResult


@dataclass
class MetaCognitiveState:
    """Tracks the cognitive state of tool execution"""

    patterns: List[Dict[str, Any]] = list()
    adaptations: List[Dict[str, Any]] = list()
    metrics: Dict[str, float] = dict()
    timestamp: str = datetime.now().isoformat()


class ToolVisitor(CompositionalVisitor):
    """Visitor for tool execution analysis"""

    def __init__(self):
        self.validation_visitor = ValidationVisitor()
        self.parsing_visitor = ParsingVisitor()
        self.transformation_visitor = TransformationVisitor()

    def visit_tool_execution(self, tool_result: ToolResult) -> ToolResult:
        """Apply visitors to analyze tool execution"""
        result = self.validation_visitor.visit(tool_result)
        result = self.parsing_visitor.visit(result)
        result = self.transformation_visitor.visit(result)
        return result


class MetaCognitiveToolCollection(ToolCollection):
    """Enhanced tool collection with meta-cognitive capabilities"""

    def __init__(self, *tools, config: Optional[Dict] = None):
        super().__init__(*tools)
        self.config = config or {}

        # Initialize components
        self.visitor_coordinator = VisitorCoordinator()
        self.shared_context = SharedContext()
        self.observation_coordinator = ObservationCoordinator()

        # Setup observers
        self.observers = {
            "state": StateObserver(),
            "transform": TransformationObserver(),
            "boundary": BoundaryObserver(),
        }
        for observer in self.observers.values():
            self.observation_coordinator.register(observer)

        self.cognitive_state = MetaCognitiveState()

    async def run(self, name: str, tool_input: Dict) -> ToolResult:
        """Execute tool with meta-cognitive monitoring"""
        # Pre-execution state observation
        self.observers["state"].observe_pre_execution(name, tool_input)

        # Create and configure tool visitor
        tool_visitor = self.visitor_coordinator.create_visitor(ToolVisitor)

        # Execute tool
        result = await super().run(name, tool_input)

        # Apply visitor analysis
        result = tool_visitor.visit_tool_execution(result)

        # Post-execution observations
        self.observers["transform"].observe_transformation(result)
        adaptations = self.observers["boundary"].check_and_adapt(result)

        # Update cognitive state
        self._update_cognitive_state(result, adaptations)

        # Update shared context
        self.shared_context.update(
            {"tool_result": result, "cognitive_state": self.cognitive_state}
        )

        return result

    def _update_cognitive_state(
        self, result: ToolResult, adaptations: List[Dict]
    ) -> None:
        """Update the cognitive state with execution results"""
        # Update patterns
        if hasattr(result, "patterns"):
            self.cognitive_state.patterns.extend(result.patterns)

        # Update adaptations
        if adaptations:
            self.cognitive_state.adaptations.extend(adaptations)

        # Update metrics
        if hasattr(result, "metrics"):
            self.cognitive_state.metrics.update(result.metrics)

        self.cognitive_state.timestamp = datetime.now().isoformat()


class MetaComputerTool:
    """Enhanced computer tool with meta-cognitive capabilities"""

    def __init__(self):
        self.state_history: List[Dict] = []
        self.pattern_history: List[Dict] = []

    async def execute(self, **kwargs) -> ToolResult:
        # Record pre-execution state
        pre_state = self._capture_state()
        self.state_history.append(pre_state)

        # Execute action
        result = await super().execute(**kwargs)

        # Record post-execution state
        post_state = self._capture_state()
        self.state_history.append(post_state)

        # Analyze patterns
        patterns = self._analyze_patterns(pre_state, post_state, result)
        self.pattern_history.extend(patterns)

        # Enhance result with meta-cognitive data
        result.patterns = patterns
        result.metrics = self._calculate_metrics()

        return result

    def _capture_state(self) -> Dict:
        """Capture current tool state"""
        return {
            "timestamp": datetime.now().isoformat(),
            "memory_usage": self._get_memory_usage(),
            "active_processes": self._get_active_processes(),
        }

    def _analyze_patterns(
        self, pre_state: Dict, post_state: Dict, result: ToolResult
    ) -> List[Dict]:
        """Analyze execution patterns"""
        patterns = []

        # Analyze state changes
        state_changes = self._compute_state_changes(pre_state, post_state)
        if state_changes:
            patterns.append(
                {
                    "type": "state_change",
                    "changes": state_changes,
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Analyze result patterns
        if hasattr(result, "output"):
            output_patterns = self._analyze_output_patterns(result.output)
            patterns.extend(output_patterns)

        return patterns

    def _calculate_metrics(self) -> Dict[str, float]:
        """Calculate tool performance metrics"""
        return {
            "state_change_frequency": len(self.state_history)
            / max(1, len(self.pattern_history)),
            "pattern_diversity": len(set(p["type"] for p in self.pattern_history)),
            "execution_stability": self._calculate_stability(),
        }

    def _calculate_stability(self) -> float:
        """Calculate execution stability metric"""
        if len(self.state_history) < 2:
            return 1.0

        stability_scores = []
        for i in range(1, len(self.state_history)):
            prev_state = self.state_history[i - 1]
            curr_state = self.state_history[i]

            # Compare states and calculate stability score
            score = self._compare_states(prev_state, curr_state)
            stability_scores.append(score)

        return sum(stability_scores) / len(stability_scores)
