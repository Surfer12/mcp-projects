#!/usr/bin/env python3
"""
Main CLI entry point for MCP (Modular Control Platform).
"""
import argparse
import asyncio
import logging
from pathlib import Path

from mcp.tools import IntegratedAITool
from mcp.visualization import run_dashboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_ai_tool(args):
    """Run the integrated AI tool."""
    tool = IntegratedAITool()
    try:
        response = await tool.generateResponse({
            'prompt': args.prompt,
            'provider': args.provider,
            'reasoningType': args.reasoning_type,
            'web_search': args.web_search,
            'google_search': args.google_search,
            'mojo_operation': args.mojo_operation
        })
        print(f"Response: {response.text}")
        print(f"Meta-analysis: {response.metaAnalysis}")
        print(f"Visualization URL: {response.visualizationUrl}")
    finally:
        await tool.cleanup()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='MCP (Modular Control Platform) CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # AI tool command
    ai_parser = subparsers.add_parser('ai', help='Run AI tool')
    ai_parser.add_argument('prompt', help='Input prompt')
    ai_parser.add_argument('--provider', default='anthropic', choices=['anthropic', 'openai'],
                          help='AI provider to use')
    ai_parser.add_argument('--reasoning-type', default='auto',
                          choices=['auto', 'step_by_step', 'tree_of_thought',
                                 'chain_of_thought', 'fast', 'analytical', 'creative'],
                          help='Reasoning type to use')
    ai_parser.add_argument('--web-search', help='Web search parameters (JSON)')
    ai_parser.add_argument('--google-search', help='Google search parameters (JSON)')
    ai_parser.add_argument('--mojo-operation', help='Mojo operation parameters (JSON)')

    # Dashboard command
    dash_parser = subparsers.add_parser('dashboard', help='Run visualization dashboard')
    dash_parser.add_argument('--port', type=int, default=8501,
                           help='Port to run dashboard on')

    args = parser.parse_args()

    if args.command == 'ai':
        asyncio.run(run_ai_tool(args))
    elif args.command == 'dashboard':
        run_dashboard()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()