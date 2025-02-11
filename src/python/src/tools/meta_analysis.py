from typing import Any, Dict, List, Optional
from .base import BaseCognitiveTool, CognitiveToolResult

class MetaAnalysisTool(BaseCognitiveTool):
    """Tool for performing meta-analysis on cognitive processing results."""

    name = "meta_analysis"
    description = "Analyzes patterns and relationships across multiple cognitive processing results."

    def __init__(self, analysis_config: Dict[str, Any]):
        self.config = analysis_config
        self.analysis_history: List[Dict[str, Any]] = []

    def __call__(
        self,
        *,
        operation: str,
        data: List[Dict[str, Any]],
        analysis_type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> CognitiveToolResult:
        try:
            if not self.validate_args(
                operation=operation,
                data=data,
                analysis_type=analysis_type,
                context=context,
                **kwargs
            ):
                return CognitiveToolResult(
                    success=False,
                    error="Invalid arguments provided"
                )

            result = self._process_operation(
                operation,
                data,
                analysis_type,
                context,
                **kwargs
            )

            # Store analysis result in history
            self.analysis_history.append({
                "operation": operation,
                "analysis_type": analysis_type,
                "result": result,
                "context": context
            })

            return CognitiveToolResult(
                success=True,
                data=result,
                metadata={
                    "operation": operation,
                    "analysis_type": analysis_type,
                    "history_size": len(self.analysis_history)
                }
            )
        except Exception as e:
            return CognitiveToolResult(
                success=False,
                error=str(e)
            )

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
                            "enum": [
                                "pattern_analysis",
                                "trend_analysis",
                                "relationship_mapping",
                                "cognitive_evolution",
                                "framework_synthesis"
                            ]
                        },
                        "data": {
                            "type": "array",
                            "description": "List of cognitive processing results to analyze",
                            "items": {
                                "type": "object"
                            }
                        },
                        "analysis_type": {
                            "type": "string",
                            "description": "Specific type of analysis to perform",
                            "enum": [
                                "temporal",
                                "structural",
                                "semantic",
                                "emergent",
                                "comparative"
                            ]
                        },
                        "context": {
                            "type": "object",
                            "description": "Additional context for the analysis"
                        }
                    },
                    "required": ["operation", "data"]
                }
            }
        }

    def validate_args(self, **kwargs) -> bool:
        # Check required arguments
        required = {"operation", "data"}
        if not all(arg in kwargs for arg in required):
            return False

        # Validate operation
        valid_operations = {
            "pattern_analysis",
            "trend_analysis",
            "relationship_mapping",
            "cognitive_evolution",
            "framework_synthesis"
        }
        if kwargs["operation"] not in valid_operations:
            return False

        # Validate data
        if not isinstance(kwargs["data"], list):
            return False
        if not all(isinstance(item, dict) for item in kwargs["data"]):
            return False

        # Validate analysis_type if provided
        if "analysis_type" in kwargs and kwargs["analysis_type"] is not None:
            valid_types = {
                "temporal",
                "structural",
                "semantic",
                "emergent",
                "comparative"
            }
            if kwargs["analysis_type"] not in valid_types:
                return False

        # Validate context if provided
        if "context" in kwargs and kwargs["context"] is not None:
            if not isinstance(kwargs["context"], dict):
                return False

        return True

    def _process_operation(
        self,
        operation: str,
        data: List[Dict[str, Any]],
        analysis_type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Process the requested meta-analysis operation."""
        operations = {
            "pattern_analysis": self._analyze_patterns,
            "trend_analysis": self._analyze_trends,
            "relationship_mapping": self._map_relationships,
            "cognitive_evolution": self._analyze_evolution,
            "framework_synthesis": self._synthesize_framework
        }

        return operations[operation](data, analysis_type, context, **kwargs)

    def _analyze_patterns(
        self,
        data: List[Dict[str, Any]],
        analysis_type: Optional[str],
        context: Optional[Dict[str, Any]],
        **kwargs
    ) -> Dict[str, Any]:
        """Analyze patterns in cognitive processing results."""
        patterns = {
            "recurring_concepts": self._find_recurring_concepts(data),
            "structural_patterns": self._find_structural_patterns(data),
            "interaction_patterns": self._find_interaction_patterns(data)
        }

        if analysis_type:
            return {
                "type": "pattern_analysis",
                "analysis_type": analysis_type,
                "patterns": patterns.get(analysis_type, {})
            }

        return {
            "type": "pattern_analysis",
            "patterns": patterns
        }

    def _analyze_trends(
        self,
        data: List[Dict[str, Any]],
        analysis_type: Optional[str],
        context: Optional[Dict[str, Any]],
        **kwargs
    ) -> Dict[str, Any]:
        """Analyze trends in cognitive processing results."""
        trends = {
            "temporal": self._analyze_temporal_trends(data),
            "complexity": self._analyze_complexity_trends(data),
            "effectiveness": self._analyze_effectiveness_trends(data)
        }

        if analysis_type:
            return {
                "type": "trend_analysis",
                "analysis_type": analysis_type,
                "trends": trends.get(analysis_type, {})
            }

        return {
            "type": "trend_analysis",
            "trends": trends
        }

    def _map_relationships(
        self,
        data: List[Dict[str, Any]],
        analysis_type: Optional[str],
        context: Optional[Dict[str, Any]],
        **kwargs
    ) -> Dict[str, Any]:
        """Map relationships between cognitive processing results."""
        relationships = {
            "concept_relationships": self._map_concept_relationships(data),
            "process_relationships": self._map_process_relationships(data),
            "outcome_relationships": self._map_outcome_relationships(data)
        }

        if analysis_type:
            return {
                "type": "relationship_mapping",
                "analysis_type": analysis_type,
                "relationships": relationships.get(analysis_type, {})
            }

        return {
            "type": "relationship_mapping",
            "relationships": relationships
        }

    def _analyze_evolution(
        self,
        data: List[Dict[str, Any]],
        analysis_type: Optional[str],
        context: Optional[Dict[str, Any]],
        **kwargs
    ) -> Dict[str, Any]:
        """Analyze cognitive evolution patterns."""
        evolution = {
            "concept_evolution": self._analyze_concept_evolution(data),
            "process_evolution": self._analyze_process_evolution(data),
            "framework_evolution": self._analyze_framework_evolution(data)
        }

        if analysis_type:
            return {
                "type": "cognitive_evolution",
                "analysis_type": analysis_type,
                "evolution": evolution.get(analysis_type, {})
            }

        return {
            "type": "cognitive_evolution",
            "evolution": evolution
        }

    def _synthesize_framework(
        self,
        data: List[Dict[str, Any]],
        analysis_type: Optional[str],
        context: Optional[Dict[str, Any]],
        **kwargs
    ) -> Dict[str, Any]:
        """Synthesize a new framework from analysis results."""
        synthesis = {
            "concepts": self._synthesize_concepts(data),
            "processes": self._synthesize_processes(data),
            "relationships": self._synthesize_relationships(data),
            "evolution": self._synthesize_evolution(data)
        }

        if analysis_type:
            return {
                "type": "framework_synthesis",
                "analysis_type": analysis_type,
                "synthesis": synthesis.get(analysis_type, {})
            }

        return {
            "type": "framework_synthesis",
            "synthesis": synthesis
        }

    # Helper methods for pattern analysis
    def _find_recurring_concepts(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find recurring concepts in the data."""
        concept_frequency = {}
        concept_contexts = {}

        for item in data:
            if "concepts" not in item:
                continue

            for concept in item["concepts"]:
                name = concept.get("name")
                if not name:
                    continue

                concept_frequency[name] = concept_frequency.get(name, 0) + 1
                if name not in concept_contexts:
                    concept_contexts[name] = []
                concept_contexts[name].append({
                    "context": item.get("context"),
                    "timestamp": item.get("timestamp"),
                    "type": item.get("type")
                })

        # Filter based on minimum frequency threshold
        min_frequency = self.config.get("pattern_analysis", {}).get("min_pattern_frequency", 2)
        recurring_concepts = {
            name: {
                "frequency": freq,
                "contexts": concept_contexts[name]
            }
            for name, freq in concept_frequency.items()
            if freq >= min_frequency
        }

        return {
            "recurring_concepts": recurring_concepts,
            "total_concepts": len(concept_frequency),
            "recurring_count": len(recurring_concepts)
        }

    def _find_structural_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find structural patterns in the data."""
        structure_patterns = {}
        relationship_patterns = {}
        hierarchy_patterns = {}

        max_depth = self.config.get("pattern_analysis", {}).get("max_pattern_depth", 3)

        for item in data:
            # Analyze structure patterns
            structure = self._extract_structure(item, max_depth)
            structure_key = str(structure)
            structure_patterns[structure_key] = structure_patterns.get(structure_key, 0) + 1

            # Analyze relationship patterns
            if "relationships" in item:
                for rel in item["relationships"]:
                    rel_type = rel.get("type")
                    if rel_type:
                        relationship_patterns[rel_type] = relationship_patterns.get(rel_type, 0) + 1

            # Analyze hierarchy patterns
            if "hierarchy" in item:
                hierarchy = self._extract_hierarchy(item["hierarchy"], max_depth)
                for path in hierarchy:
                    hierarchy_patterns[path] = hierarchy_patterns.get(path, 0) + 1

        return {
            "structure_patterns": {
                k: v for k, v in structure_patterns.items()
                if v >= self.config.get("pattern_analysis", {}).get("min_pattern_frequency", 2)
            },
            "relationship_patterns": relationship_patterns,
            "hierarchy_patterns": hierarchy_patterns
        }

    def _find_interaction_patterns(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find interaction patterns in the data."""
        interaction_types = {}
        interaction_flows = {}
        component_interactions = {}

        for item in data:
            if "interactions" not in item:
                continue

            for interaction in item["interactions"]:
                # Analyze interaction types
                int_type = interaction.get("type")
                if int_type:
                    interaction_types[int_type] = interaction_types.get(int_type, 0) + 1

                # Analyze interaction flows
                source = interaction.get("source")
                target = interaction.get("target")
                if source and target:
                    flow_key = f"{source}->{target}"
                    interaction_flows[flow_key] = interaction_flows.get(flow_key, 0) + 1

                # Analyze component interactions
                components = interaction.get("components", [])
                for comp in components:
                    component_interactions[comp] = component_interactions.get(comp, 0) + 1

        min_frequency = self.config.get("pattern_analysis", {}).get("min_pattern_frequency", 2)

        return {
            "interaction_types": {
                k: v for k, v in interaction_types.items()
                if v >= min_frequency
            },
            "interaction_flows": {
                k: v for k, v in interaction_flows.items()
                if v >= min_frequency
            },
            "component_interactions": {
                k: v for k, v in component_interactions.items()
                if v >= min_frequency
            }
        }

    def _extract_structure(self, item: Dict[str, Any], max_depth: int, current_depth: int = 0) -> Dict[str, Any]:
        """Extract structural patterns from an item up to max_depth."""
        if current_depth >= max_depth:
            return {"type": "truncated"}

        structure = {"type": item.get("type", "unknown")}

        if "components" in item:
            structure["components"] = [
                self._extract_structure(comp, max_depth, current_depth + 1)
                for comp in item["components"]
            ]

        return structure

    def _extract_hierarchy(self, hierarchy: Dict[str, Any], max_depth: int) -> List[str]:
        """Extract hierarchy paths from a hierarchy structure."""
        paths = []

        def traverse(node: Dict[str, Any], current_path: List[str]):
            if len(current_path) >= max_depth:
                return

            node_type = node.get("type", "unknown")
            current_path.append(node_type)
            paths.append("->".join(current_path))

            for child in node.get("children", []):
                traverse(child, current_path.copy())

        traverse(hierarchy, [])
        return paths

    # Helper methods for trend analysis
    def _analyze_temporal_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze temporal trends in the data."""
        # Sort data by timestamp
        sorted_data = sorted(
            [d for d in data if "timestamp" in d],
            key=lambda x: x["timestamp"]
        )

        if not sorted_data:
            return {"error": "No temporal data available"}

        window_size = self.config.get("trend_analysis", {}).get("window_size", 5)
        min_trend_strength = self.config.get("trend_analysis", {}).get("min_trend_strength", 0.7)

        # Analyze trends in different aspects
        trends = {
            "complexity": self._analyze_window_trend(sorted_data, "complexity", window_size),
            "interaction_count": self._analyze_window_trend(sorted_data, "interaction_count", window_size),
            "concept_count": self._analyze_window_trend(sorted_data, "concept_count", window_size)
        }

        # Filter significant trends
        significant_trends = {
            k: v for k, v in trends.items()
            if abs(v.get("trend_strength", 0)) >= min_trend_strength
        }

        return {
            "time_range": {
                "start": sorted_data[0]["timestamp"],
                "end": sorted_data[-1]["timestamp"]
            },
            "trends": trends,
            "significant_trends": significant_trends
        }

    def _analyze_complexity_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze complexity trends in the data."""
        complexity_metrics = {}

        for item in data:
            timestamp = item.get("timestamp")
            if not timestamp:
                continue

            # Calculate complexity metrics
            metrics = {
                "structural": self._calculate_structural_complexity(item),
                "interaction": self._calculate_interaction_complexity(item),
                "conceptual": self._calculate_conceptual_complexity(item)
            }

            complexity_metrics[timestamp] = metrics

        # Analyze trends in each complexity dimension
        trends = {}
        for dimension in ["structural", "interaction", "conceptual"]:
            dimension_data = [
                {"timestamp": ts, "value": metrics[dimension]}
                for ts, metrics in complexity_metrics.items()
            ]
            trends[dimension] = self._analyze_window_trend(
                dimension_data,
                "value",
                self.config.get("trend_analysis", {}).get("window_size", 5)
            )

        return {
            "complexity_metrics": complexity_metrics,
            "trends": trends
        }

    def _analyze_effectiveness_trends(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze effectiveness trends in the data."""
        effectiveness_metrics = {}

        for item in data:
            timestamp = item.get("timestamp")
            if not timestamp:
                continue

            # Calculate effectiveness metrics
            metrics = {
                "accuracy": self._calculate_accuracy(item),
                "coverage": self._calculate_coverage(item),
                "efficiency": self._calculate_efficiency(item)
            }

            effectiveness_metrics[timestamp] = metrics

        # Analyze trends in each effectiveness dimension
        trends = {}
        for dimension in ["accuracy", "coverage", "efficiency"]:
            dimension_data = [
                {"timestamp": ts, "value": metrics[dimension]}
                for ts, metrics in effectiveness_metrics.items()
            ]
            trends[dimension] = self._analyze_window_trend(
                dimension_data,
                "value",
                self.config.get("trend_analysis", {}).get("window_size", 5)
            )

        return {
            "effectiveness_metrics": effectiveness_metrics,
            "trends": trends
        }

    def _analyze_window_trend(
        self,
        data: List[Dict[str, Any]],
        value_key: str,
        window_size: int
    ) -> Dict[str, Any]:
        """Analyze trend in a sliding window of data."""
        if len(data) < window_size:
            return {"error": "Insufficient data for trend analysis"}

        windows = [
            data[i:i + window_size]
            for i in range(len(data) - window_size + 1)
        ]

        window_trends = []
        for window in windows:
            values = [item.get(value_key, 0) for item in window]

            # Calculate basic statistics
            avg = sum(values) / len(values)
            min_val = min(values)
            max_val = max(values)

            # Calculate trend direction and strength
            if len(values) >= 2:
                first_half = sum(values[:len(values)//2]) / (len(values)//2)
                second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
                trend_strength = (second_half - first_half) / max(abs(first_half), 1)
            else:
                trend_strength = 0

            window_trends.append({
                "start": window[0]["timestamp"],
                "end": window[-1]["timestamp"],
                "average": avg,
                "min": min_val,
                "max": max_val,
                "trend_strength": trend_strength
            })

        # Aggregate trends across windows
        avg_trend_strength = sum(w["trend_strength"] for w in window_trends) / len(window_trends)

        return {
            "window_trends": window_trends,
            "overall_trend": {
                "direction": "increasing" if avg_trend_strength > 0 else "decreasing",
                "strength": abs(avg_trend_strength)
            }
        }

    def _calculate_structural_complexity(self, item: Dict[str, Any]) -> float:
        """Calculate structural complexity metric."""
        complexity = 0

        # Count components
        components = item.get("components", [])
        complexity += len(components)

        # Count relationships
        relationships = item.get("relationships", [])
        complexity += len(relationships) * 1.5  # Relationships weighted more heavily

        # Count hierarchy levels
        if "hierarchy" in item:
            complexity += self._calculate_hierarchy_depth(item["hierarchy"])

        return complexity

    def _calculate_interaction_complexity(self, item: Dict[str, Any]) -> float:
        """Calculate interaction complexity metric."""
        complexity = 0

        interactions = item.get("interactions", [])

        # Count interaction types
        interaction_types = set(i.get("type") for i in interactions if i.get("type"))
        complexity += len(interaction_types)

        # Count unique components involved
        components = set()
        for interaction in interactions:
            components.update(interaction.get("components", []))
        complexity += len(components)

        # Count bidirectional interactions
        bidirectional = sum(
            1 for i in interactions
            if i.get("bidirectional", False)
        )
        complexity += bidirectional * 1.5

        return complexity

    def _calculate_conceptual_complexity(self, item: Dict[str, Any]) -> float:
        """Calculate conceptual complexity metric."""
        complexity = 0

        # Count concepts
        concepts = item.get("concepts", [])
        complexity += len(concepts)

        # Count concept relationships
        for concept in concepts:
            complexity += len(concept.get("relationships", []))

        # Count concept attributes
        for concept in concepts:
            complexity += len(concept.get("attributes", []))

        return complexity

    def _calculate_hierarchy_depth(self, hierarchy: Dict[str, Any]) -> int:
        """Calculate the maximum depth of a hierarchy."""
        def get_depth(node: Dict[str, Any]) -> int:
            if not node.get("children"):
                return 1
            return 1 + max(get_depth(child) for child in node["children"])

        return get_depth(hierarchy)

    def _calculate_accuracy(self, item: Dict[str, Any]) -> float:
        """Calculate accuracy metric."""
        metrics = item.get("metrics", {})
        return metrics.get("accuracy", 0.0)

    def _calculate_coverage(self, item: Dict[str, Any]) -> float:
        """Calculate coverage metric."""
        metrics = item.get("metrics", {})
        return metrics.get("coverage", 0.0)

    def _calculate_efficiency(self, item: Dict[str, Any]) -> float:
        """Calculate efficiency metric."""
        metrics = item.get("metrics", {})
        return metrics.get("efficiency", 0.0)

    # Helper methods for relationship mapping
    def _map_concept_relationships(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Map relationships between concepts."""
        raise NotImplementedError

    def _map_process_relationships(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Map relationships between processes."""
        raise NotImplementedError

    def _map_outcome_relationships(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Map relationships between outcomes."""
        raise NotImplementedError

    # Helper methods for evolution analysis
    def _analyze_concept_evolution(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze evolution of concepts."""
        raise NotImplementedError

    def _analyze_process_evolution(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze evolution of processes."""
        raise NotImplementedError

    def _analyze_framework_evolution(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze evolution of the framework."""
        raise NotImplementedError

    # Helper methods for framework synthesis
    def _synthesize_concepts(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize concepts from analysis results."""
        raise NotImplementedError

    def _synthesize_processes(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize processes from analysis results."""
        raise NotImplementedError

    def _synthesize_relationships(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize relationships from analysis results."""
        raise NotImplementedError

    def _synthesize_evolution(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize evolution patterns from analysis results."""
        raise NotImplementedError
```
