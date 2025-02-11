# MCP (Modular Control Platform)

An integrated AI and cognitive tools framework that combines multiple AI providers, web tools, and visualization capabilities.

## Features

- **Integrated AI Tools**: Support for Anthropic and OpenAI models
- **Web & API Tools**: Built-in web scraping and Google API integration
- **Cognitive Framework**: Advanced pattern analysis and evolution capabilities
- **Real-time Visualization**: Interactive dashboard for monitoring and analysis
- **Meta-cognitive Capabilities**: Self-analysis and adaptation

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp.git
cd mcp

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .[dev]
```

## Configuration

Create a `.env` file in the `config` directory:

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```

## Usage

### Command Line Interface

```bash
# Run AI tool
mcp ai "Your prompt here" --provider anthropic --reasoning-type analytical

# Run with web search
mcp ai "Research this topic" --web-search '{"url": "https://example.com"}'

# Run visualization dashboard
mcp dashboard --port 8501
```

### Python API

```python
from mcp.tools import IntegratedAITool

async def main():
    tool = IntegratedAITool()
    try:
        response = await tool.generateResponse({
            'prompt': 'Your prompt',
            'provider': 'anthropic',
            'reasoningType': 'analytical'
        })
        print(f"Response: {response.text}")
        print(f"Visualization URL: {response.visualizationUrl}")
    finally:
        await tool.cleanup()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Project Structure

```
mcp/
├── src/
│   ├── core/           # Core framework components
│   ├── tools/          # External API integrations
│   ├── visualization/  # Dashboard and visualizations
│   └── cli/           # Command-line interface
├── tests/             # Test suite
├── examples/          # Usage examples
├── docs/             # Documentation
└── config/           # Configuration files
```

## Development

```bash
# Run tests
pytest

# Format code
black src/ tests/

# Type checking
mypy src/

# Lint code
flake8 src/ tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.