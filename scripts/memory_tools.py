#!/usr/bin/env python3
"""
Script for memory operations using MemoryTool.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

from mcp.tools.integrated import MemoryTool


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MCP Memory Tools")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Store command
    store_parser = subparsers.add_parser("store", help="Store data")
    store_parser.add_argument("key", help="Key for the data")
    store_parser.add_argument(
        "data",
        help="JSON data to store or '-' for stdin"
    )
    store_parser.add_argument(
        "--tags",
        nargs="+",
        help="Tags for the data"
    )

    # Retrieve command
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve data")
    retrieve_parser.add_argument("key", help="Key to retrieve")
    retrieve_parser.add_argument(
        "--output",
        type=Path,
        help="Output file (default: stdout)"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List stored data")
    list_parser.add_argument(
        "--tag-filter",
        nargs="+",
        help="Filter by tags"
    )
    list_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete data")
    delete_parser.add_argument("key", help="Key to delete")

    # Common options
    parser.add_argument(
        "--storage-dir",
        type=Path,
        help="Storage directory"
    )

    return parser.parse_args()


def read_data(data_arg: str) -> Any:
    """Read data from argument or stdin."""
    if data_arg == "-":
        return json.load(sys.stdin)
    return json.loads(data_arg)


def format_entry(entry: dict) -> str:
    """Format a memory entry for text output."""
    return (
        f"Key: {entry['key']}\n"
        f"Tags: {', '.join(entry['tags'])}\n"
        f"Created: {entry['created_at']}\n"
        f"Updated: {entry['updated_at']}\n"
        f"Data: {json.dumps(entry['data'], indent=2)}\n"
    )


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Initialize tool
    memory_tool = MemoryTool(
        storage_dir=args.storage_dir
    ) if args.storage_dir else MemoryTool()

    try:
        if args.command == "store":
            # Read data
            try:
                data = read_data(args.data)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON data: {e}", file=sys.stderr)
                return 1

            # Store data
            result = memory_tool(
                operation="store",
                key=args.key,
                data=data,
                tags=args.tags or []
            )

            if result.success:
                print(f"Data stored successfully with key: {args.key}")
                if args.tags:
                    print(f"Tags: {', '.join(args.tags)}")
                print(f"Timestamp: {result.data['timestamp']}")
                return 0
            else:
                print(f"Error: {result.error}", file=sys.stderr)
                return 1

        elif args.command == "retrieve":
            result = memory_tool(
                operation="retrieve",
                key=args.key
            )

            if result.success:
                if result.data is None:
                    print(f"No data found for key: {args.key}", file=sys.stderr)
                    return 1

                # Format output
                output = json.dumps(result.data, indent=2)

                # Write to file or stdout
                if args.output:
                    args.output.write_text(output)
                    print(f"Data written to: {args.output}")
                else:
                    print(output)

                return 0
            else:
                print(f"Error: {result.error}", file=sys.stderr)
                return 1

        elif args.command == "list":
            result = memory_tool(
                operation="list",
                tag_filter=args.tag_filter or []
            )

            if result.success:
                entries = result.data
                if not entries:
                    print("No entries found")
                    return 0

                if args.format == "json":
                    print(json.dumps(entries, indent=2))
                else:
                    for entry in entries:
                        print("-" * 40)
                        print(format_entry(entry))

                return 0
            else:
                print(f"Error: {result.error}", file=sys.stderr)
                return 1

        elif args.command == "delete":
            result = memory_tool(
                operation="delete",
                key=args.key
            )

            if result.success:
                if result.data["deleted"]:
                    print(f"Successfully deleted key: {args.key}")
                    return 0
                else:
                    print(f"Key not found: {args.key}", file=sys.stderr)
                    return 1
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