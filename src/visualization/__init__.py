"""
Visualization package for MCP (Modular Control Platform).
Contains dashboard and pattern visualization components.
"""

from .dashboard import main as run_dashboard
from .pattern_viz import PatternVisualizer

__all__ = [
    'run_dashboard',
    'PatternVisualizer',
]
