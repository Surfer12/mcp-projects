#!/usr/bin/env python3

def main():
    print("Hello from Magic Python! 🪄")
    print("Testing our MCP environment...")

    # Try importing some of our dependencies
    try:
        import anthropic
        print("✓ anthropic package available")
    except ImportError:
        print("× anthropic package not found")

    try:
        import openai
        print("✓ openai package available")
    except ImportError:
        print("× openai package not found")

if __name__ == "__main__":
    main()