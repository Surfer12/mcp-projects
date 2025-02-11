# Visualization Components

This directory contains visualization tools and components for analyzing cognitive patterns, tool usage, and system performance.

## Components

### 1. Pattern Visualizer (`pattern_viz.py`)

A class that provides various visualization methods for analyzing patterns in the system:

- Tool usage heatmaps
- Cognitive network visualizations
- Performance analysis plots

### 2. Interactive Dashboard (`dashboard.py`)

A Streamlit-based dashboard that provides an interactive interface for exploring visualizations:

- Navigation between different visualization types
- Interactive controls for customizing visualizations
- Export functionality (planned)

## Setup Instructions

1. Install required dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run the dashboard:
   ```bash
   streamlit run src/visualization/dashboard.py
   ```

## Usage Examples

### Creating a Tool Usage Heatmap

```python
from visualization.pattern_viz import PatternVisualizer

# Initialize visualizer
viz = PatternVisualizer()

# Create and display a heatmap
viz.plot_tool_usage_heatmap(usage_data, title="Tool Usage Over Time")
```

### Visualizing a Cognitive Network

```python
# Define nodes and edges
nodes = ['Concept A', 'Concept B', 'Concept C']
edges = [('Concept A', 'Concept B'), ('Concept B', 'Concept C')]

# Create network visualization
fig = viz.create_cognitive_network(nodes, edges)
fig.show()
```

### Analyzing Tool Performance

```python
# Create performance visualization
viz.plot_tool_performance(performance_data, metric='execution_time')
```

## Testing

Run the tests using pytest:

```bash
pytest tests/test_visualization/
```

## Contributing

When adding new visualizations:

1. Add the visualization method to `PatternVisualizer` class
2. Create corresponding tests in `tests/test_visualization/`
3. Update the dashboard if applicable
4. Document the new functionality in this README

## Dependencies

- matplotlib
- seaborn
- plotly
- networkx
- pandas
- streamlit
