# Modular Chat Platform (MCP) Integrated Tools

This package provides a comprehensive set of integrated tools for the Modular Chat Platform (MCP), combining development, system automation, memory management, and visualization capabilities.

## Features

### Developer Tools
- Shell command execution
- Text editing and file management
- Testing framework integration (pytest)
- Code formatting and linting

### Computer Control Tools
- AppleScript automation (macOS only)
- Web search and content fetching
- Local caching system
- System automation scripts

### Memory Tools
- Persistent data storage with SQLite
- Tag-based data organization
- Flexible data retrieval
- Version tracking with timestamps

### Visualization Tools
- Interactive dashboards
- Pattern visualization
- Multiple output formats (HTML, PNG, SVG)
- Real-time data updates

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Developer Tools
```python
from mcp.tools.integrated import DeveloperTool

dev_tool = DeveloperTool()

# Run shell command
result = dev_tool(
    operation='shell',
    command='pytest tests/'
)

# Edit file
result = dev_tool(
    operation='edit',
    file_path='src/example.py',
    content='print("Hello, MCP!")'
)
```

### Computer Control Tools
```python
from mcp.tools.integrated import ComputerControlTool

ctrl_tool = ComputerControlTool()

# Web search
result = ctrl_tool(
    operation='web_search',
    query='python async programming'
)

# Cache data
result = ctrl_tool(
    operation='cache',
    cache_key='search_results',
    cache_data=search_results
)
```

### Memory Tools
```python
from mcp.tools.integrated import MemoryTool

memory_tool = MemoryTool()

# Store data with tags
result = memory_tool(
    operation='store',
    key='user_preferences',
    data={'theme': 'dark'},
    tags=['settings', 'ui']
)

# Retrieve data
result = memory_tool(
    operation='retrieve',
    key='user_preferences'
)
```

### Visualization Tools
```python
from mcp.tools.integrated import VisualizationTool

viz_tool = VisualizationTool()

# Run dashboard
result = viz_tool(
    operation='dashboard',
    data=dashboard_data,
    title='MCP Analytics'
)

# Visualize pattern
result = viz_tool(
    operation='pattern',
    data=pattern_data,
    pattern_type='temporal',
    title='Usage Patterns'
)
```

## Directory Structure
```
mcp/
├── tools/
│   ├── integrated/
│   │   ├── __init__.py
│   │   ├── dev_tools.py
│   │   ├── system_tools.py
│   │   ├── memory_tools.py
│   │   └── visualization_tools.py
│   └── base.py
├── visualization/
│   ├── __init__.py
│   ├── dashboard.py
│   └── pattern_viz.py
└── requirements.txt
```

## Configuration

Each tool can be configured with custom directories for outputs and storage:

```python
from pathlib import Path

custom_viz_dir = Path('/path/to/viz/output')
viz_tool = VisualizationTool(output_dir=custom_viz_dir)

custom_memory_dir = Path('/path/to/memory/storage')
memory_tool = MemoryTool(storage_dir=custom_memory_dir)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.