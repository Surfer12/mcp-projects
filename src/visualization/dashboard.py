"""
Interactive dashboard for visualizing cognitive patterns and tool usage.
"""

from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st

from src.visualization.pattern_viz import PatternVisualizer


def load_sample_data() -> (
    Tuple[
        Optional[pd.DataFrame],
        Optional[pd.DataFrame],
        Optional[List[str]],
        Optional[List[Tuple[str, str]]],
    ]
):
    """
    Load sample data for demonstration.

    Returns:
        Tuple containing:
        - usage_data: DataFrame with tool usage data
        - performance_data: DataFrame with performance metrics
        - nodes: List of node names
        - edges: List of edge tuples
    """
    try:
        # Tool usage data
        tools = ["Tool A", "Tool B", "Tool C", "Tool D"]
        periods = ["Period 1", "Period 2", "Period 3", "Period 4"]
        usage_data = pd.DataFrame(
            np.random.rand(len(tools), len(periods)), index=tools, columns=periods
        )

        # Performance data
        tools_perf = tools * 10
        metrics = np.random.rand(40)
        performance_data = pd.DataFrame(
            {"tool_name": tools_perf, "execution_time": metrics}
        )

        # Cognitive network data
        nodes = ["Concept A", "Concept B", "Concept C", "Concept D"]
        edges = [
            ("Concept A", "Concept B"),
            ("Concept B", "Concept C"),
            ("Concept C", "Concept D"),
            ("Concept A", "Concept D"),
        ]

        return usage_data, performance_data, nodes, edges
    except Exception as e:
        st.error(f"Error loading sample data: {str(e)}")
        return None, None, None, None


def main():
    """Main function to run the Streamlit dashboard."""
    st.set_page_config(
        page_title="Cognitive Pattern Analysis", page_icon="📊", layout="wide"
    )

    st.title("Cognitive Pattern Analysis Dashboard")

    try:
        # Initialize visualizer with error handling
        viz = PatternVisualizer(style="whitegrid")
    except Exception as e:
        st.error(f"Error initializing visualizer: {str(e)}")
        return

    # Load sample data with error handling
    data = load_sample_data()
    if not all(x is not None for x in data):
        st.error("Failed to load sample data. Please check the error message above.")
        return

    usage_data, performance_data, nodes, edges = data
    # Type assertion to satisfy mypy
    assert isinstance(usage_data, pd.DataFrame)
    assert isinstance(performance_data, pd.DataFrame)
    assert isinstance(nodes, list)
    assert isinstance(edges, list)

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a visualization:",
        ["Tool Usage Patterns", "Performance Analysis", "Cognitive Network"],
    )

    # Main content area
    if page == "Tool Usage Patterns":
        st.header("Tool Usage Patterns")
        st.write("Heatmap showing tool usage patterns over time")

        try:
            # Plot controls
            col1, col2 = st.columns([3, 1])
            with col2:
                fig_size = st.slider(
                    "Select figure size", min_value=6, max_value=20, value=12
                )

            # Plot heatmap
            with col1:
                viz.plot_tool_usage_heatmap(
                    usage_data, figsize=(fig_size, fig_size * 0.6)
                )
                st.pyplot()
        except Exception as e:
            st.error(f"Error creating heatmap visualization: {str(e)}")

    elif page == "Performance Analysis":
        st.header("Tool Performance Analysis")
        st.write("Box plot showing performance metrics for different tools")

        try:
            # Plot controls
            metric = st.selectbox("Select performance metric", ["execution_time"])

            # Plot performance
            viz.plot_tool_performance(performance_data, metric=metric)
            st.pyplot()
        except Exception as e:
            st.error(f"Error creating performance visualization: {str(e)}")

    else:  # Cognitive Network
        st.header("Cognitive Network Visualization")
        st.write("Interactive network showing relationships between concepts")

        try:
            # Create and display network
            fig = viz.create_cognitive_network(nodes, edges)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating network visualization: {str(e)}")

    # Additional options in sidebar
    st.sidebar.header("Options")

    # Export functionality
    if st.sidebar.button("Export Visualizations"):
        try:
            # Add export functionality here
            st.sidebar.info(
                "Export functionality will be implemented " "in a future update."
            )
        except Exception as e:
            st.sidebar.error(f"Error exporting visualizations: {str(e)}")

    # About section
    st.sidebar.markdown("---")
    st.sidebar.header("About")
    st.sidebar.info(
        """
        This dashboard provides interactive visualizations for
        analyzing cognitive patterns and tool usage in the system.
        Use the navigation menu to explore different aspects
        of the analysis.
        """
    )


if __name__ == "__main__":
    main()
