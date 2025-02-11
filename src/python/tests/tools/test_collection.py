import pytest
from datetime import datetime
from typing import Dict, List
from cognitive_framework.tools import (
    CognitiveToolCollection,
    MetaAnalysisTool,
    CognitiveEvolutionTool
)

@pytest.fixture
def tool_configs() -> Dict:
    return {
        "mojo_type_registry": {
            "Concept": dict,
            "Process": dict,
            "Framework": dict
        },
        "analysis_config": {
            "pattern_analysis": {
                "min_pattern_frequency": 2,
                "max_pattern_depth": 3
            },
            "trend_analysis": {
                "window_size": 3,
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
        }
    }

@pytest.fixture
def tool_collection(tool_configs) -> CognitiveToolCollection:
    collection = CognitiveToolCollection()

    # Register tools
    collection.register_tool(
        MetaAnalysisTool(tool_configs["analysis_config"])
    )
    collection.register_tool(
        CognitiveEvolutionTool(tool_configs["evolution_config"])
    )

    return collection

@pytest.fixture
def sample_data() -> Dict:
    return {
        "concept": {
            "name": "Fluid Learning",
            "type": "concept",
            "attributes": [
                {"name": "adaptability", "value": 0.8},
                {"name": "flexibility", "value": 0.7}
            ],
            "relationships": [
                {"type": "depends_on", "target": "Pattern Recognition"}
            ],
            "timestamp": datetime.now().isoformat()
        },
        "analysis_data": [
            {
                "type": "concept",
                "concepts": [
                    {
                        "name": "Fluid Learning",
                        "attributes": ["adaptive", "flexible"]
                    }
                ],
                "timestamp": datetime.now().isoformat()
            }
        ]
    }

def test_collection_initialization(tool_collection):
    """Test tool collection initialization."""
    assert isinstance(tool_collection.tools, dict)
    assert len(tool_collection.tools) == 2
    assert len(tool_collection.tool_history) == 0

def test_register_tool(tool_collection, tool_configs):
    """Test tool registration."""
    new_tool = MetaAnalysisTool(tool_configs["analysis_config"])

    # Should raise error for duplicate name
    with pytest.raises(ValueError):
        tool_collection.register_tool(new_tool)

def test_get_tool(tool_collection):
    """Test getting tools by name."""
    meta_tool = tool_collection.get_tool("meta_analysis")
    evolution_tool = tool_collection.get_tool("cognitive_evolution")

    assert isinstance(meta_tool, MetaAnalysisTool)
    assert isinstance(evolution_tool, CognitiveEvolutionTool)

    with pytest.raises(KeyError):
        tool_collection.get_tool("nonexistent_tool")

def test_list_tools(tool_collection):
    """Test listing registered tools."""
    tools = tool_collection.list_tools()

    assert len(tools) == 2
    assert all(isinstance(tool, dict) for tool in tools)
    assert all("name" in tool for tool in tools)
    assert all("description" in tool for tool in tools)
    assert all("version" in tool for tool in tools)

def test_to_anthropic_params(tool_collection):
    """Test conversion to Anthropic tool parameters."""
    params = tool_collection.to_anthropic_params()

    assert isinstance(params, list)
    assert len(params) == 2
    assert all(param["type"] == "function" for param in params)

def test_execute_meta_analysis(tool_collection, sample_data):
    """Test executing meta-analysis tool."""
    result = tool_collection.execute_tool(
        "meta_analysis",
        operation="pattern_analysis",
        data=sample_data["analysis_data"]
    )

    assert result.success
    assert isinstance(result.data, dict)
    assert len(tool_collection.tool_history) == 1

def test_execute_evolution(tool_collection, sample_data):
    """Test executing evolution tool."""
    result = tool_collection.execute_tool(
        "cognitive_evolution",
        operation="mutate",
        target="concept",
        data=sample_data["concept"]
    )

    assert result.success
    assert isinstance(result.data, dict)
    assert len(tool_collection.tool_history) == 1

def test_tool_history(tool_collection, sample_data):
    """Test tool execution history tracking."""
    # Execute multiple tools
    tool_collection.execute_tool(
        "meta_analysis",
        operation="pattern_analysis",
        data=sample_data["analysis_data"]
    )
    tool_collection.execute_tool(
        "cognitive_evolution",
        operation="mutate",
        target="concept",
        data=sample_data["concept"]
    )

    history = tool_collection.get_tool_history()
    assert len(history) == 2
    assert all(isinstance(entry, dict) for entry in history)
    assert all("tool" in entry for entry in history)
    assert all("success" in entry for entry in history)

def test_error_handling(tool_collection):
    """Test error handling in tool execution."""
    # Test with invalid tool name
    with pytest.raises(KeyError):
        tool_collection.execute_tool(
            "nonexistent_tool",
            operation="test"
        )

    # Test with invalid arguments
    result = tool_collection.execute_tool(
        "meta_analysis",
        operation="invalid_operation",
        data=[]
    )
    assert not result.success
    assert result.error is not None

def test_create_default_collection(tool_configs):
    """Test creating default tool collection."""
    collection = CognitiveToolCollection.create_default_collection(
        mojo_type_registry=tool_configs["mojo_type_registry"],
        analysis_config=tool_configs["analysis_config"]
    )

    assert isinstance(collection, CognitiveToolCollection)
    assert len(collection.tools) == 2
    assert "meta_analysis" in collection.tools
    assert "mojo_structure" in collection.tools

def test_integrated_workflow(tool_collection, sample_data):
    """Test integrated workflow using multiple tools."""
    # First, analyze patterns
    analysis_result = tool_collection.execute_tool(
        "meta_analysis",
        operation="pattern_analysis",
        data=sample_data["analysis_data"]
    )
    assert analysis_result.success

    # Then, evolve the concept based on analysis
    evolution_result = tool_collection.execute_tool(
        "cognitive_evolution",
        operation="adapt",
        target="concept",
        data=sample_data["concept"],
        context={"analysis_result": analysis_result.data}
    )
    assert evolution_result.success

    # Verify history contains both operations
    history = tool_collection.get_tool_history()
    assert len(history) == 2
    assert history[0]["tool"] == "meta_analysis"
    assert history[1]["tool"] == "cognitive_evolution"
```
