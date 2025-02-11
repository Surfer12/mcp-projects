"""
Core package for MCP (Modular Control Platform).
Contains base classes, cognitive tools, and analysis components.
"""

from .base import BaseCognitiveTool, CognitiveToolResult
from .collection import CognitiveToolCollection, MetaCognitiveToolCollection
from .evolution import CognitiveEvolutionTool
from .meta_analysis import MetaAnalysisTool
from .mojo_tools import MojoStructureTool

__all__ = [
    'BaseCognitiveTool',
    'CognitiveToolResult',
    'CognitiveToolCollection',
    'MetaCognitiveToolCollection',
    'CognitiveEvolutionTool',
    'MetaAnalysisTool',
    'MojoStructureTool',
]