#!/usr/bin/env python3
"""
Script for common development operations using DeveloperTool.
"""

import argparse
import sys
from pathlib import Path

from mcp.tools.integrated import DeveloperTool


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MCP Development Tools")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Shell command
    shell_parser = subparsers.add_parser("shell", help="Execute shell command")
    shell_parser.add_argument("cmd", help="Command to execute")

    # Edit file
    edit_parser = subparsers.add_parser("edit", help="Edit file")
    edit_parser.add_argument("file", help="File to edit")
    edit_parser.add_argument("content", help="New content")

    # Run tests
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument(
        "path",
        nargs="?",
        default="tests",
        help="Test path (default: tests)"
    )
    test_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    # Common options
    parser.add_argument(
        "--workspace",
        type=Path,
        help="Workspace root directory"
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Initialize tool
    dev_tool = DeveloperTool(
        workspace_root=args.workspace or Path.cwd()
    )

    try:
        if args.command == "shell":
            result = dev_tool(
                operation="shell",
                command=args.cmd
            )
            if result.success:
                print(result.data["stdout"])
                if result.data["stderr"]:
                    print(result.data["stderr"], file=sys.stderr)
                return result.data["returncode"]
            else:
                print(f"Error: {result.error}", file=sys.stderr)
                return 1

        elif args.command == "edit":
            result = dev_tool(
                operation="edit",
                file_path=args.file,
                content=args.content
            )
            if result.success:
                print(f"Successfully edited {result.data['path']}")
                print(f"File size: {result.data['size']} bytes")
                return 0
            else:
                print(f"Error: {result.error}", file=sys.stderr)
                return 1

        elif args.command == "test":
            extra_args = ["-v"] if args.verbose else []
            result = dev_tool(
                operation="test",
                extra_args=[args.path, *extra_args]
            )
            if result.success:
                print(result.data["stdout"])
                if result.data["stderr"]:
                    print(result.data["stderr"], file=sys.stderr)
                return result.data["returncode"]
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