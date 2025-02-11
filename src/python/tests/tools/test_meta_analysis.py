from datetime import datetime, timedelta
from typing import Dict, List

import pytest
from cognitive_framework.tools import MetaAnalysisTool


@pytest.fixture
def analysis_config() -> Dict:
    return {
        "pattern_analysis": {"min_pattern_frequency": 2, "max_pattern_depth": 3},
        "trend_analysis": {"window_size": 3, "min_trend_strength": 0.7},
    }


@pytest.fixture
def meta_analysis_tool(analysis_config) -> MetaAnalysisTool:
    return MetaAnalysisTool(analysis_config)


@pytest.fixture
def sample_data() -> List[Dict]:
    base_time = datetime.now()
    return [
        {
            "timestamp": (base_time + timedelta(hours=i)).isoformat(),
            "type": "concept",
            "concepts": [
                {
                    "name": "Fluid Learning",
                    "attributes": ["adaptive", "flexible"],
                    "relationships": ["connects_to:Pattern Recognition"],
                },
                {
                    "name": "Pattern Recognition",
                    "attributes": ["analytical", "recursive"],
                    "relationships": ["connects_to:Fluid Learning"],
                },
            ],
            "interactions": [
                {
                    "type": "bidirectional",
                    "source": "Fluid Learning",
                    "target": "Pattern Recognition",
                    "components": ["learning_flow", "pattern_detection"],
                }
            ],
            "metrics": {
                "accuracy": 0.85 + (i * 0.05),
                "coverage": 0.75 + (i * 0.05),
                "efficiency": 0.90 + (i * 0.02),
            },
        }
        for i in range(5)
    ]


def test_tool_initialization(meta_analysis_tool):
    assert meta_analysis_tool.name == "meta_analysis"
    assert isinstance(meta_analysis_tool.config, dict)
    assert len(meta_analysis_tool.analysis_history) == 0


def test_validate_args_valid(meta_analysis_tool):
    valid_args = {
        "operation": "pattern_analysis",
        "data": [{"type": "test"}],
        "analysis_type": "structural",
    }
    assert meta_analysis_tool.validate_args(**valid_args)


def test_validate_args_invalid_operation(meta_analysis_tool):
    invalid_args = {"operation": "invalid_operation", "data": [{"type": "test"}]}
    assert not meta_analysis_tool.validate_args(**invalid_args)


def test_validate_args_invalid_data(meta_analysis_tool):
    invalid_args = {"operation": "pattern_analysis", "data": "not_a_list"}
    assert not meta_analysis_tool.validate_args(**invalid_args)


def test_pattern_analysis(meta_analysis_tool, sample_data):
    result = meta_analysis_tool(
        operation="pattern_analysis", data=sample_data, analysis_type="structural"
    )

    assert result.success
    assert "patterns" in result.data
    assert isinstance(result.data["patterns"], dict)


def test_trend_analysis(meta_analysis_tool, sample_data):
    result = meta_analysis_tool(operation="trend_analysis", data=sample_data)

    assert result.success
    assert "trends" in result.data
    assert isinstance(result.data["trends"], dict)


def test_relationship_mapping(meta_analysis_tool, sample_data):
    result = meta_analysis_tool(
        operation="relationship_mapping",
        data=sample_data,
        analysis_type="concept_relationships",
    )

    assert result.success
    assert "relationships" in result.data
    assert isinstance(result.data["relationships"], dict)


def test_cognitive_evolution(meta_analysis_tool, sample_data):
    result = meta_analysis_tool(
        operation="cognitive_evolution",
        data=sample_data,
        analysis_type="concept_evolution",
    )

    assert result.success
    assert "evolution" in result.data
    assert isinstance(result.data["evolution"], dict)


def test_framework_synthesis(meta_analysis_tool, sample_data):
    result = meta_analysis_tool(operation="framework_synthesis", data=sample_data)

    assert result.success
    assert "synthesis" in result.data
    assert isinstance(result.data["synthesis"], dict)


def test_temporal_trend_analysis(meta_analysis_tool, sample_data):
    result = meta_analysis_tool._analyze_temporal_trends(sample_data)

    assert "time_range" in result
    assert "trends" in result
    assert "significant_trends" in result


def test_complexity_trend_analysis(meta_analysis_tool, sample_data):
    result = meta_analysis_tool._analyze_complexity_trends(sample_data)

    assert "complexity_metrics" in result
    assert "trends" in result


def test_effectiveness_trend_analysis(meta_analysis_tool, sample_data):
    result = meta_analysis_tool._analyze_effectiveness_trends(sample_data)

    assert "effectiveness_metrics" in result
    assert "trends" in result


def test_tool_history(meta_analysis_tool, sample_data):
    # Perform multiple operations
    meta_analysis_tool(operation="pattern_analysis", data=sample_data)
    meta_analysis_tool(operation="trend_analysis", data=sample_data)

    history = meta_analysis_tool.analysis_history
    assert len(history) == 2
    assert all(isinstance(entry, dict) for entry in history)


def test_error_handling(meta_analysis_tool):
    result = meta_analysis_tool(
        operation="pattern_analysis", data=[]  # Empty data should cause an error
    )

    assert not result.success
    assert result.error is not None


def test_anthropic_param_conversion(meta_analysis_tool):
    param = meta_analysis_tool.to_anthropic_param()

    assert isinstance(param, dict)
    assert param["type"] == "function"
    assert "function" in param
    assert "parameters" in param["function"]
