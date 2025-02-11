#!/usr/bin/env python3
"""
Script for visualization operations using VisualizationTool.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from mcp.tools.integrated import VisualizationTool


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MCP Visualization Tools")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Dashboard command
    dashboard_parser = subparsers.add_parser("dashboard", help="Run dashboard")
    dashboard_parser.add_argument(
        "data",
        help="JSON data to visualize or '-' for stdin"
    )
    dashboard_parser.add_argument(
        "--title",
        default="MCP Dashboard",
        help="Dashboard title"
    )
    dashboard_parser.add_argument(
        "--description",
        help="Dashboard description"
    )

    # Pattern command
    pattern_parser = subparsers.add_parser("pattern", help="Visualize pattern")
    pattern_parser.add_argument(
        "data",
        help="JSON data to visualize or '-' for stdin"
    )
    pattern_parser.add_argument(
        "--type",
        required=True,
        help="Pattern type to visualize"
    )
    pattern_parser.add_argument(
        "--title",
        help="Visualization title"
    )
    pattern_parser.add_argument(
        "--description",
        help="Visualization description"
    )

    # Save command
    save_parser = subparsers.add_parser("save", help="Save visualization")
    save_parser.add_argument(
        "data",
        help="JSON data to visualize or '-' for stdin"
    )
    save_parser.add_argument(
        "--format",
        choices=["html", "png", "svg"],
        default="html",
        help="Output format"
    )
    save_parser.add_argument(
        "--title",
        help="Visualization title"
    )

    # Common options
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory"
    )

    return parser.parse_args()


def read_data(data_arg: str) -> Any:
    """Read data from argument or stdin."""
    if data_arg == "-":
        return json.load(sys.stdin)
    return json.loads(data_arg)


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Initialize tool
    viz_tool = VisualizationTool(
        output_dir=args.output_dir
    ) if args.output_dir else VisualizationTool()

    try:
        # Read data
        try:
            data = read_data(args.data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}", file=sys.stderr)
            return 1

        if args.command == "dashboard":
            result = viz_tool(
                operation="dashboard",
                data=data,
                title=args.title,
                description=args.description or ""
            )

            if result.success:
                print("Dashboard started successfully")
                print(f"Data file: {result.data['data_file']}")
                return 0
            else:
                print(f"Error: {result.error}", file=sys.stderr)
                return 1

        elif args.command == "pattern":
            result = viz_tool(
                operation="pattern",
                data=data,
                pattern_type=args.type,
                title=args.title or "",
                description=args.description or ""
            )

            if result.success:
                print("Pattern visualization generated successfully")
                print(f"Output file: {result.data['output_file']}")
                if "visualization" in result.data:
                    print("\nVisualization data:")
                    print(json.dumps(result.data["visualization"], indent=2))
                return 0
            else:
                print(f"Error: {result.error}", file=sys.stderr)
                return 1

        elif args.command == "save":
            result = viz_tool(
                operation="save",
                data=data,
                output_format=args.format,
                title=args.title or ""
            )

            if result.success:
                print("Visualization saved successfully")
                print(f"Format: {result.data['format']}")
                print(f"Output file: {result.data['output_file']}")
                return 0
            else:
                print(f"Error: {result.error}", file=sys.stderr)
                return 1

        else:
            print("No command specified", file=sys.stderr)
            return 1

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())