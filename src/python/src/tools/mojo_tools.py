from typing import Any, Dict, Optional

from .base import BaseCognitiveTool, CognitiveToolResult


class MojoStructureTool(BaseCognitiveTool):
    """Tool for working with Mojo data structures."""

    name = "mojo_structure"
    description = (
        "Manages and manipulates Mojo data structures for cognitive processing."
    )

    def __init__(self, type_registry: Dict[str, Any]):
        self.type_registry = type_registry

    def __call__(
        self,
        *,
        operation: str,
        structure_type: str,
        data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> CognitiveToolResult:
        try:
            if not self.validate_args(
                operation=operation, structure_type=structure_type, data=data, **kwargs
            ):
                return CognitiveToolResult(
                    success=False, error="Invalid arguments provided"
                )

            result = self._process_operation(operation, structure_type, data, **kwargs)

            return CognitiveToolResult(
                success=True,
                data=result,
                metadata={"operation": operation, "structure_type": structure_type},
            )
        except Exception as e:
            return CognitiveToolResult(success=False, error=str(e))

    def to_anthropic_param(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "The operation to perform",
                            "enum": ["create", "validate", "transform", "analyze"],
                        },
                        "structure_type": {
                            "type": "string",
                            "description": "The type of Mojo structure to work with",
                            "enum": list(self.type_registry.keys()),
                        },
                        "data": {
                            "type": "object",
                            "description": "The data to process (optional for some operations)",
                        },
                    },
                    "required": ["operation", "structure_type"],
                },
            },
        }

    def validate_args(self, **kwargs) -> bool:
        # Check required arguments
        required = {"operation", "structure_type"}
        if not all(arg in kwargs for arg in required):
            return False

        # Validate operation
        valid_operations = {"create", "validate", "transform", "analyze"}
        if kwargs["operation"] not in valid_operations:
            return False

        # Validate structure type
        if kwargs["structure_type"] not in self.type_registry:
            return False

        # Validate data if provided
        if "data" in kwargs and kwargs["data"] is not None:
            if not isinstance(kwargs["data"], dict):
                return False

        return True

    def _process_operation(
        self,
        operation: str,
        structure_type: str,
        data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Process the requested operation on Mojo structures."""
        operations = {
            "create": self._create_structure,
            "validate": self._validate_structure,
            "transform": self._transform_structure,
            "analyze": self._analyze_structure,
        }

        return operations[operation](structure_type, data, **kwargs)

    def _create_structure(
        self, structure_type: str, data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Dict[str, Any]:
        """Create a new Mojo structure instance."""
        structure_class = self.type_registry[structure_type]
        if data is None:
            # Create empty structure
            return {"type": structure_type, "data": {}}

        # Validate and create structure with data
        return {
            "type": structure_type,
            "data": structure_class.validate_and_create(data),
        }

    def _validate_structure(
        self, structure_type: str, data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Dict[str, Any]:
        """Validate a Mojo structure."""
        if data is None:
            raise ValueError("Data is required for validation")

        structure_class = self.type_registry[structure_type]
        validation_result = structure_class.validate(data)

        return {
            "type": structure_type,
            "is_valid": validation_result.is_valid,
            "errors": validation_result.errors,
        }

    def _transform_structure(
        self,
        structure_type: str,
        data: Optional[Dict[str, Any]] = None,
        target_type: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Transform a Mojo structure to another type or format."""
        if data is None:
            raise ValueError("Data is required for transformation")

        if target_type is None:
            raise ValueError("Target type is required for transformation")

        source_class = self.type_registry[structure_type]
        target_class = self.type_registry[target_type]

        transformed_data = source_class.transform_to(data, target_class)

        return {
            "source_type": structure_type,
            "target_type": target_type,
            "data": transformed_data,
        }

    def _analyze_structure(
        self,
        structure_type: str,
        data: Optional[Dict[str, Any]] = None,
        analysis_type: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Analyze a Mojo structure."""
        if data is None:
            raise ValueError("Data is required for analysis")

        structure_class = self.type_registry[structure_type]

        analysis_types = {
            "complexity": structure_class.analyze_complexity,
            "relationships": structure_class.analyze_relationships,
            "patterns": structure_class.analyze_patterns,
        }

        if analysis_type is None or analysis_type not in analysis_types:
            # Perform all analyses
            return {
                "type": structure_type,
                "analyses": {
                    name: analyzer(data) for name, analyzer in analysis_types.items()
                },
            }

        return {
            "type": structure_type,
            "analysis_type": analysis_type,
            "result": analysis_types[analysis_type](data),
        }
