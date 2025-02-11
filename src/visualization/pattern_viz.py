"""
Pattern visualization module for analyzing and
visualizing cognitive patterns and tool usage.
"""

from typing import Any, Dict, List, Literal, Optional

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns

StyleType = Literal["white", "dark", "whitegrid", "darkgrid", "ticks"]


class PatternVisualizer:
    """Visualizer for cognitive patterns and tool usage analysis."""

    def __init__(self, style: StyleType = "whitegrid"):
        """
        Initialize the visualizer with style settings.

        Args:
            style: The style theme to use ('whitegrid', 'darkgrid',
                   'white', 'dark', 'ticks')
        """
        # Set up seaborn style
        try:
            sns.set_theme(style=style)
        except Exception as e:
            error_msg = f"Warning: Could not set seaborn style: {e}"
            print(error_msg)
            # Fall back to default matplotlib style
            plt.style.use("default")

        # Configure default plot settings
        plt.rcParams.update(
            {
                "figure.figsize": (10, 6),
                "axes.titlesize": 14,
                "axes.labelsize": 12,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
            }
        )

    def plot_tool_usage_heatmap(
        self,
        usage_data: pd.DataFrame,
        title: str = "Tool Usage Patterns",
        figsize: tuple = (12, 8),
    ) -> None:
        """
        Create a heatmap visualization of tool usage patterns.

        Args:
            usage_data: DataFrame with tool usage data
            title: Plot title
            figsize: Figure size tuple (width, height)

        Raises:
            ValueError: If usage_data is empty or has invalid structure
        """
        if usage_data.empty:
            raise ValueError("Usage data cannot be empty")

        if not all(usage_data.dtypes.map(lambda x: issubclass(x.type, np.number))):
            raise ValueError("All data must be numeric for heatmap visualization")

        # Create new figure with specified size
        plt.figure(figsize=figsize)

        try:
            # Create heatmap
            sns.heatmap(
                usage_data,
                annot=True,
                cmap="YlOrRd",
                fmt=".2f",
                cbar_kws={"label": "Usage Frequency"},
            )

            # Customize plot
            plt.title(title, pad=20)
            plt.xlabel("Time Period", labelpad=10)
            plt.ylabel("Tool Name", labelpad=10)

            # Adjust layout
            plt.tight_layout()
        except Exception as e:
            print(f"Error creating heatmap: {e}")
            plt.close()  # Clean up the figure on error
            raise

    def create_cognitive_network(
        self,
        nodes: List[str],
        edges: List[tuple],
        node_attrs: Optional[Dict[str, Any]] = None,
    ) -> go.Figure:
        """
        Create an interactive network visualization of cognitive patterns.

        Args:
            nodes: List of node names
            edges: List of (source, target) tuples
            node_attrs: Optional dictionary of node attributes

        Returns:
            Plotly figure object

        Raises:
            ValueError: If nodes or edges are empty, or if edges reference
                non-existent nodes
        """
        if not nodes:
            raise ValueError("Node list cannot be empty")

        if not edges:
            raise ValueError("Edge list cannot be empty")

        # Validate edges reference existing nodes
        all_nodes = set(nodes)
        for source, target in edges:
            if source not in all_nodes or target not in all_nodes:
                raise ValueError(
                    f"Edge ({source}, {target}) references non-existent node"
                )

        try:
            # Create network graph
            G = nx.Graph()
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)

            if node_attrs:
                nx.set_node_attributes(G, node_attrs)

            # Calculate layout
            pos = nx.spring_layout(G, k=1, iterations=50)

            # Create edge trace
            edge_x = []
            edge_y = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

            edge_trace = go.Scatter(
                x=edge_x,
                y=edge_y,
                line=dict(width=0.8, color="#888"),
                hoverinfo="none",
                mode="lines",
            )

            # Create node trace
            node_x = []
            node_y = []
            node_text = []
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(node)

            node_trace = go.Scatter(
                x=node_x,
                y=node_y,
                text=node_text,
                mode="markers+text",
                hoverinfo="text",
                textposition="top center",
                marker=dict(
                    showscale=True,
                    colorscale="YlOrRd",
                    size=20,
                    colorbar=dict(
                        thickness=15,
                        title="Node Connections",
                        xanchor="left",
                        titleside="right",
                    ),
                ),
            )

            # Create figure
            fig = go.Figure(
                data=[edge_trace, node_trace],
                layout=go.Layout(
                    title="Cognitive Pattern Network",
                    showlegend=False,
                    hovermode="closest",
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    plot_bgcolor="white",
                ),
            )

            return fig
        except Exception as e:
            print(f"Error creating network visualization: {e}")
            raise

    def plot_tool_performance(
        self,
        performance_data: pd.DataFrame,
        metric: str = "execution_time",
        figsize: tuple = (10, 6),
    ) -> None:
        """
        Create a box plot visualization of tool performance metrics.

        Args:
            performance_data: DataFrame with tool performance data
            metric: Performance metric to visualize
            figsize: Figure size tuple (width, height)

        Raises:
            ValueError: If performance_data is empty or missing required columns
        """
        if performance_data.empty:
            raise ValueError("Performance data cannot be empty")

        required_columns = {"tool_name", metric}
        missing_columns = required_columns - set(performance_data.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        try:
            plt.figure(figsize=figsize)

            # Create box plot with updated API usage
            sns.boxplot(
                data=performance_data,
                x="tool_name",
                y=metric,
                hue="tool_name",  # Add hue parameter
                legend=False,  # Hide legend since it's redundant
                palette="YlOrRd",
            )

            # Customize plot
            plt.title(f"Tool Performance Analysis: {metric}", pad=20)
            plt.xlabel("Tool Name", labelpad=10)
            plt.ylabel(metric.replace("_", " ").title(), labelpad=10)

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha="right")

            # Adjust layout
            plt.tight_layout()
        except Exception as e:
            print(f"Error creating performance plot: {e}")
            plt.close()  # Clean up the figure on error
            raise

    def save_figure(self, filename: str, dpi: int = 300) -> None:
        """
        Save the current figure to a file.

        Args:
            filename: Output filename
            dpi: Resolution in dots per inch

        Raises:
            ValueError: If filename is empty or invalid
        """
        if not filename:
            raise ValueError("Filename cannot be empty")

        try:
            plt.savefig(filename, dpi=dpi, bbox_inches="tight")
        except Exception as e:
            print(f"Error saving figure: {e}")
            raise
