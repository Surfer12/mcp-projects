import asyncio
from dataclasses import dataclass
from typing import Any
from typing import Dict as _Dict
from typing import Optional

from anthropic.types import MessageParam

from anthropic import Anthropic

try:
    from cognitive_framework.models import Concept, EmergentFramework, StageAnalysisItem
    from cognitive_framework.tools import CognitiveToolCollection
except ImportError:
    print("Warning: cognitive_framework package not found. This is an example file.")

    # Define stub classes for example purposes
    @dataclass
    class ToolResult:
        success: bool
        data: Optional[Any] = None
        error: Optional[str] = None

    @dataclass
    class Concept:
        id: int
        name: str
        relevant_input_excerpt: str

    @dataclass
    class EmergentFramework:
        id: int
        name: str

    @dataclass
    class StageAnalysisItem:
        id: int
        stage: str

    class CognitiveToolCollection:
        @classmethod
        def create_default_collection(cls, **kwargs):
            return cls()

        def execute_tool(self, *args, **kwargs) -> ToolResult:
            return ToolResult(success=True, data={})

        def to_anthropic_params(self):
            return []

        def get_tool_history(self):
            return []


async def main():
    # Initialize Anthropic client
    client = Anthropic(api_key="your-api-key")

    # Create tool collection
    mojo_type_registry = {
        "Concept": Concept,
        "StageAnalysisItem": StageAnalysisItem,
        "EmergentFramework": EmergentFramework,
    }

    analysis_config = {
        "pattern_analysis": {"min_pattern_frequency": 2, "max_pattern_depth": 3},
        "trend_analysis": {"window_size": 5, "min_trend_strength": 0.7},
    }

    tools = CognitiveToolCollection.create_default_collection(
        mojo_type_registry=mojo_type_registry, analysis_config=analysis_config
    )

    # Example: Create a concept using the Mojo structure tool
    concept_data = {
        "id": 1,
        "name": "Fluid Learning Paradigm",
        "relevant_input_excerpt": "...emphasizing conceptual exploration and flexible thinking...",
    }

    result = tools.execute_tool(
        "mojo_structure",
        operation="create",
        structure_type="Concept",
        data=concept_data,
    )

    if result.success:
        print("Created concept:", result.data)
    else:
        print("Error creating concept:", result.error)

    # Example: Analyze patterns using the meta-analysis tool
    analysis_data = [
        {"type": "concept", "data": concept_data, "timestamp": "2024-01-15T10:00:00Z"},
        # Add more data points for analysis
    ]

    result = tools.execute_tool(
        "meta_analysis",
        operation="pattern_analysis",
        data=analysis_data,
        analysis_type="structural",
    )

    if result.success:
        print("Pattern analysis result:", result.data)
    else:
        print("Error in pattern analysis:", result.error)

    # Example: Use tools with Claude
    messages: list[MessageParam] = [
        {"role": "user", "content": "Analyze this concept and suggest improvements."}
    ]

    # Use await to properly handle the async call
    response = await client.messages.create(
        model="claude-3-opus-20240229",
        messages=messages,
        tools=tools.to_anthropic_params(),
        max_tokens=1000,
    )

    print("Claude's response:", response.content)

    # Example: Process Claude's tool calls
    for tool_call in response.tool_calls:
        result = tools.execute_tool(tool_call.name, **tool_call.parameters)

        print(
            f"Tool '{tool_call.name}' result:",
            result.data if result.success else result.error,
        )

    # Example: Review tool execution history
    history = tools.get_tool_history()
    print("\nTool execution history:")
    for entry in history:
        print(f"- {entry['tool']}: {'Success' if entry['success'] else 'Failed'}")
        if not entry['success']:
            print(f"  Error: {entry['error']}")


if __name__ == "__main__":
    asyncio.run(main())
