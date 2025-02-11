import pytest
from datetime import datetime, timedelta
from typing import Dict, List
from cognitive_framework.tools import CognitiveEvolutionTool

@pytest.fixture
def evolution_config() -> Dict:
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

@pytest.fixture
def evolution_tool(evolution_config) -> CognitiveEvolutionTool:
    return CognitiveEvolutionTool(evolution_config)

@pytest.fixture
def sample_concept() -> Dict:
    return {
        "name": "Fluid Learning",
        "type": "concept",
        "attributes": [
            {"name": "adaptability", "value": 0.8},
            {"name": "flexibility", "value": 0.7}
        ],
        "relationships": [
            {"type": "depends_on", "target": "Pattern Recognition"},
            {"type": "enhances", "target": "Learning Rate"}
        ],
        "metrics": {
            "complexity": 0.6,
            "effectiveness": 0.75
        },
        "timestamp": datetime.now().isoformat()
    }

@pytest.fixture
def sample_process() -> Dict:
    return {
        "name": "Learning Process",
        "type": "process",
        "steps": [
            {
                "name": "Input Processing",
                "type": "analysis",
                "parameters": {"depth": 2}
            },
            {
                "name": "Pattern Extraction",
                "type": "transformation",
                "parameters": {"threshold": 0.5}
            }
        ],
        "metrics": {
            "efficiency": 0.8,
            "reliability": 0.85
        },
        "timestamp": datetime.now().isoformat()
    }

def test_tool_initialization(evolution_tool):
    """Test tool initialization and configuration."""
    assert evolution_tool.name == "cognitive_evolution"
    assert isinstance(evolution_tool.config, dict)
    assert len(evolution_tool.evolution_history) == 0

def test_validate_args_valid(evolution_tool, sample_concept):
    """Test argument validation with valid inputs."""
    valid_args = {
        "operation": "mutate",
        "target": "concept",
        "data": sample_concept
    }
    assert evolution_tool.validate_args(**valid_args)

def test_validate_args_invalid_operation(evolution_tool, sample_concept):
    """Test argument validation with invalid operation."""
    invalid_args = {
        "operation": "invalid_op",
        "target": "concept",
        "data": sample_concept
    }
    assert not evolution_tool.validate_args(**invalid_args)

def test_validate_args_invalid_target(evolution_tool, sample_concept):
    """Test argument validation with invalid target."""
    invalid_args = {
        "operation": "mutate",
        "target": "invalid_target",
        "data": sample_concept
    }
    assert not evolution_tool.validate_args(**invalid_args)

def test_mutate_concept(evolution_tool, sample_concept):
    """Test concept mutation operation."""
    result = evolution_tool(
        operation="mutate",
        target="concept",
        data=sample_concept
    )

    assert result.success
    assert "original" in result.data
    assert "mutated" in result.data
    assert "mutation_info" in result.data
    assert result.data["mutated"] != result.data["original"]

def test_mutate_process(evolution_tool, sample_process):
    """Test process mutation operation."""
    result = evolution_tool(
        operation="mutate",
        target="process",
        data=sample_process
    )

    assert result.success
    assert "original" in result.data
    assert "mutated" in result.data
    assert "mutation_info" in result.data
    assert result.data["mutated"] != result.data["original"]

def test_combine_concepts(evolution_tool, sample_concept):
    """Test concept combination operation."""
    concept2 = sample_concept.copy()
    concept2["name"] = "Pattern Recognition"
    concept2["attributes"][0]["value"] = 0.6

    result = evolution_tool(
        operation="combine",
        target="concept",
        data={
            "structures": [sample_concept, concept2],
            "method": "weighted",
            "weights": [0.6, 0.4]
        }
    )

    assert result.success
    assert "original_structures" in result.data
    assert "combined" in result.data
    assert "method" in result.data

def test_adapt_concept(evolution_tool, sample_concept):
    """Test concept adaptation operation."""
    context = {
        "environment": "high_complexity",
        "constraints": {"resource_limit": 0.8}
    }

    result = evolution_tool(
        operation="adapt",
        target="concept",
        data=sample_concept,
        context=context
    )

    assert result.success
    assert "original" in result.data
    assert "adapted" in result.data
    assert "adaptations" in result.data

def test_optimize_process(evolution_tool, sample_process):
    """Test process optimization operation."""
    result = evolution_tool(
        operation="optimize",
        target="process",
        data=sample_process,
        optimization_target="efficiency",
        steps=3
    )

    assert result.success
    assert "original" in result.data
    assert "optimized" in result.data
    assert "optimization_history" in result.data
    assert len(result.data["optimization_history"]) <= 3

def test_prune_concept(evolution_tool, sample_concept):
    """Test concept pruning operation."""
    result = evolution_tool(
        operation="prune",
        target="concept",
        data=sample_concept
    )

    assert result.success
    assert "original" in result.data
    assert "pruned" in result.data
    assert "pruned_elements" in result.data

def test_evolution_history(evolution_tool, sample_concept):
    """Test evolution history tracking."""
    # Perform multiple operations
    evolution_tool(
        operation="mutate",
        target="concept",
        data=sample_concept
    )
    evolution_tool(
        operation="optimize",
        target="concept",
        data=sample_concept
    )

    history = evolution_tool.evolution_history
    assert len(history) == 2
    assert all(isinstance(entry, dict) for entry in history)
    assert all("operation" in entry for entry in history)
    assert all("timestamp" in entry for entry in history)

def test_error_handling(evolution_tool):
    """Test error handling with invalid inputs."""
    result = evolution_tool(
        operation="combine",
        target="concept",
        data={"structures": []}  # Empty structures should cause an error
    )

    assert not result.success
    assert result.error is not None
    assert "structures are required" in result.error.lower()

def test_anthropic_param_conversion(evolution_tool):
    """Test conversion to Anthropic tool parameter format."""
    param = evolution_tool.to_anthropic_param()

    assert isinstance(param, dict)
    assert param["type"] == "function"
    assert "function" in param
    assert "parameters" in param["function"]
    assert "operation" in param["function"]["parameters"]["properties"]
    assert "target" in param["function"]["parameters"]["properties"]

@pytest.mark.parametrize("operation,target", [
    ("mutate", "concept"),
    ("combine", "process"),
    ("adapt", "framework"),
    ("optimize", "interaction"),
    ("prune", "concept")
])
def test_operation_target_combinations(evolution_tool, sample_concept, operation, target):
    """Test various combinations of operations and targets."""
    data = sample_concept
    if operation == "combine":
        data = {"structures": [sample_concept, sample_concept.copy()]}

    result = evolution_tool(
        operation=operation,
        target=target,
        data=data
    )

    assert result.success
    assert isinstance(result.data, dict)
    assert result.metadata["operation"] == operation
    assert result.metadata["target"] == target
```
