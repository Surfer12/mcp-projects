from datetime import datetime
from typing import Dict, List

import pytest
from cognitive_framework.tools import ToolResult
from cognitive_framework.tools.meta_cognitive import (
    MetaCognitiveState,
    MetaCognitiveToolCollection,
    MetaComputerTool,
    ToolVisitor,
)


@pytest.fixture
def meta_config() -> Dict:
    return {
        "observation": {"state_tracking": True, "pattern_analysis": True},
        "adaptation": {"enabled": True, "threshold": 0.7},
    }


@pytest.fixture
def meta_tool_collection(meta_config) -> MetaCognitiveToolCollection:
    return MetaCognitiveToolCollection(MetaComputerTool(), config=meta_config)


@pytest.fixture
def sample_tool_result() -> ToolResult:
    return ToolResult(
        success=True,
        output="Test output",
        error=None,
        metadata={"duration": 0.5, "resource_usage": {"memory": 100, "cpu": 50}},
    )


@pytest.fixture
def sample_state_history() -> List[Dict]:
    return [
        {
            "timestamp": datetime.now().isoformat(),
            "memory_usage": 100,
            "active_processes": ["process1", "process2"],
        },
        {
            "timestamp": datetime.now().isoformat(),
            "memory_usage": 120,
            "active_processes": ["process1", "process2", "process3"],
        },
    ]


def test_meta_cognitive_state_initialization():
    """Test MetaCognitiveState initialization and defaults"""
    state = MetaCognitiveState()

    assert isinstance(state.patterns, list)
    assert isinstance(state.adaptations, list)
    assert isinstance(state.metrics, dict)
    assert isinstance(state.timestamp, str)


def test_tool_visitor():
    """Test ToolVisitor functionality"""
    visitor = ToolVisitor()
    result = ToolResult(success=True, output="test", error=None)

    processed_result = visitor.visit_tool_execution(result)
    assert processed_result is not None
    assert processed_result.success


def test_meta_cognitive_tool_collection_initialization(
    meta_tool_collection, meta_config
):
    """Test MetaCognitiveToolCollection initialization"""
    assert meta_tool_collection.config == meta_config
    assert meta_tool_collection.cognitive_state is not None
    assert len(meta_tool_collection.observers) == 3
    assert meta_tool_collection.shared_context is not None


@pytest.mark.asyncio
async def test_meta_cognitive_tool_collection_run(
    meta_tool_collection, sample_tool_result
):
    """Test MetaCognitiveToolCollection run method"""
    tool_input = {"action": "test_action"}

    # Mock the super().run() to return our sample result
    meta_tool_collection._run_original = meta_tool_collection.run
    meta_tool_collection.run = lambda name, tool_input: sample_tool_result

    result = await meta_tool_collection.run("test_tool", tool_input)

    assert result is not None
    assert result.success
    assert meta_tool_collection.cognitive_state.timestamp is not None


def test_meta_computer_tool_initialization():
    """Test MetaComputerTool initialization"""
    tool = MetaComputerTool()

    assert isinstance(tool.state_history, list)
    assert isinstance(tool.pattern_history, list)
    assert len(tool.state_history) == 0
    assert len(tool.pattern_history) == 0


@pytest.mark.asyncio
async def test_meta_computer_tool_execute():
    """Test MetaComputerTool execute method"""
    tool = MetaComputerTool()

    # Mock super().execute()
    tool._execute_original = tool.execute
    tool.execute = lambda **kwargs: ToolResult(success=True, output="test", error=None)

    result = await tool.execute(action="test_action")

    assert result is not None
    assert result.success
    assert hasattr(result, "patterns")
    assert hasattr(result, "metrics")


def test_meta_computer_tool_state_capture(sample_state_history):
    """Test MetaComputerTool state capture and analysis"""
    tool = MetaComputerTool()
    tool.state_history = sample_state_history

    state = tool._capture_state()
    assert isinstance(state, dict)
    assert "timestamp" in state
    assert "memory_usage" in state
    assert "active_processes" in state


def test_meta_computer_tool_pattern_analysis(sample_state_history, sample_tool_result):
    """Test MetaComputerTool pattern analysis"""
    tool = MetaComputerTool()

    patterns = tool._analyze_patterns(
        sample_state_history[0], sample_state_history[1], sample_tool_result
    )

    assert isinstance(patterns, list)
    assert len(patterns) > 0
    assert all(isinstance(p, dict) for p in patterns)


def test_meta_computer_tool_metrics(sample_state_history):
    """Test MetaComputerTool metrics calculation"""
    tool = MetaComputerTool()
    tool.state_history = sample_state_history

    metrics = tool._calculate_metrics()

    assert isinstance(metrics, dict)
    assert "state_change_frequency" in metrics
    assert "pattern_diversity" in metrics
    assert "execution_stability" in metrics


def test_cognitive_state_updates(meta_tool_collection, sample_tool_result):
    """Test cognitive state updates with tool results"""
    # Add patterns and metrics to the result
    sample_tool_result.patterns = [{"type": "test_pattern"}]
    sample_tool_result.metrics = {"test_metric": 0.8}

    meta_tool_collection._update_cognitive_state(
        sample_tool_result, adaptations=[{"type": "test_adaptation"}]
    )

    assert len(meta_tool_collection.cognitive_state.patterns) > 0
    assert len(meta_tool_collection.cognitive_state.adaptations) > 0
    assert len(meta_tool_collection.cognitive_state.metrics) > 0


def test_shared_context_updates(meta_tool_collection, sample_tool_result):
    """Test shared context updates during tool execution"""
    meta_tool_collection.shared_context.update(
        {
            "tool_result": sample_tool_result,
            "cognitive_state": meta_tool_collection.cognitive_state,
        }
    )

    context_data = meta_tool_collection.shared_context.get_data()
    assert "tool_result" in context_data
    assert "cognitive_state" in context_data


@pytest.mark.asyncio
async def test_observer_integration(meta_tool_collection):
    """Test observer integration during tool execution"""
    tool_input = {"action": "test_action"}

    # Mock the observers
    state_observations = []
    transform_observations = []

    meta_tool_collection.observers[
        "state"
    ].observe_pre_execution = lambda name, input: state_observations.append(
        (name, input)
    )

    meta_tool_collection.observers[
        "transform"
    ].observe_transformation = lambda result: transform_observations.append(result)

    await meta_tool_collection.run("test_tool", tool_input)

    assert len(state_observations) > 0
    assert len(transform_observations) > 0


def test_visitor_integration(meta_tool_collection, sample_tool_result):
    """Test visitor integration with tool execution"""
    visitor = meta_tool_collection.visitor_coordinator.create_visitor(ToolVisitor)

    processed_result = visitor.visit_tool_execution(sample_tool_result)
    assert processed_result is not None
    assert processed_result.success
