"""
Core tag types and functionality for meta-analysis framework.

This module defines the various tag types used in meta-analysis operations.
"""

struct Tag:
    """Base class for all tag types."""

    var name: String
    var content: String

    fn __init__(inout self, name: String, content: String = ""):
        """Initialize a new Tag instance.

        Args:
            name: The name of the tag.
            content: The content within the tag. Defaults to empty string.
        """
        self.name = name
        self.content = content

struct MetaTag(Tag):
    """Tag for meta-analysis operations."""

    var layer: Int

    fn __init__(inout self, name: String, layer: Int, content: String = ""):
        """Initialize a new MetaTag instance.

        Args:
            name: The name of the tag.
            layer: The analysis layer this tag belongs to.
            content: The content within the tag. Defaults to empty string.
        """
        super().__init__(name, content)
        self.layer = layer

struct ThinkingTag(MetaTag):
    """Tag for thinking process analysis."""

    var thinking_type: String

    fn __init__(inout self, thinking_type: String, layer: Int, content: String = ""):
        """Initialize a new ThinkingTag instance.

        Args:
            thinking_type: The type of thinking process.
            layer: The analysis layer this tag belongs to.
            content: The content within the tag. Defaults to empty string.
        """
        super().__init__("thinking", layer, content)
        self.thinking_type = thinking_type
