"""
Base classes and interfaces for meta-analysis framework.

This module provides the foundational classes and interfaces for implementing
meta-analysis capabilities.
"""

struct MetaAnalysis:
    """Base class for meta-analysis operations."""

    var layer_count: Int
    var current_layer: Int

    fn __init__(inout self, layer_count: Int = 3):
        """Initialize a new MetaAnalysis instance.

        Args:
            layer_count: Number of analysis layers to use. Defaults to 3.
        """
        self.layer_count = layer_count
        self.current_layer = 1

    fn process_layer(self, layer: Int) raises -> None:
        """Process analysis at the specified layer.

        Args:
            layer: The layer number to process.

        Raises:
            ValueError: If layer is invalid.
        """
        if layer < 1 or layer > self.layer_count:
            raise Error("Invalid layer number")
        self.current_layer = layer
