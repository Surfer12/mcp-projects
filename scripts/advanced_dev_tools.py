#!/usr/bin/env python3
"""
Script for advanced development operations using AdvancedDeveloperTools.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from mcp.tools.integrated import AdvancedDeveloperTools, MemoryTool


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MCP Advanced Development Tools")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument(
        "--type",
        choices=["tox", "coverage", "e2e"],
        default="coverage",
        help="Type of test to run"
    )
    test_parser.add_argument(
        "--args",
        nargs="+",
        help="Additional test arguments"
    )

    # Lint command
    lint_parser = subparsers.add_parser("lint", help="Run linting")
    lint_parser.add_argument(
        "--type",
        choices=["black", "flake8", "mypy", "all"],
        default="all",
        help="Type of linting to run"
    )
    lint_parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix issues where possible"
    )

    # Docs command
    docs_parser = subparsers.add_parser("docs", help="Build documentation")
    docs_parser.add_argument(
        "--type",
        choices=["sphinx", "mkdocs"],
        default="sphinx",
        help="Type of documentation to build"
    )
    docs_parser.add_argument(
        "--serve",
        action="store_true",
        help="Serve documentation after building"
    )

    # Container command
    container_parser = subparsers.add_parser("container", help="Container operations")
    container_parser.add_argument(
        "--op",
        choices=["build", "test", "run"],
        default="build",
        help="Container operation to perform"
    )
    container_parser.add_argument(
        "--args",
        nargs="+",
        help="Additional container arguments"
    )

    # Common options
    parser.add_argument(
        "--workspace",
        type=Path,
        help="Workspace root directory"
    )
    parser.add_argument(
        "--memory-dir",
        type=Path,
        help="Memory storage directory"
    )
    parser.add_argument(
        "--store-results",
        action="store_true",
        help="Store operation results"
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Initialize tools
    memory_tool = MemoryTool(
        storage_dir=args.memory_dir
    ) if args.memory_dir else MemoryTool()

    adv_tool = AdvancedDeveloperTools(
        workspace_root=args.workspace or Path.cwd(),
        memory_tool=memory_tool
    )

    timestamp = datetime.utcnow().isoformat()

    try:
        if args.command == "test":
            result = adv_tool(
                operation="test",
                test_type=args.type,
                extra_args=args.args or [],
                store_results=args.store_results
            )

        elif args.command == "lint":
            result = adv_tool(
                operation="lint",
                lint_type=args.type,
                extra_args=["--fix"] if args.fix else [],
                store_results=args.store_results
            )

        elif args.command == "docs":
            result = adv_tool(
                operation="docs",
                doc_type=args.type,
                extra_args=["--serve"] if args.serve else []
            )

        elif args.command == "container":
            result = adv_tool(
                operation="container",
                container_op=args.op,
                extra_args=args.args or []
            )

        else:
            print("No command specified", file=sys.stderr)
            return 1

        # Handle result
        if result.success:
            print("Operation completed successfully")

            # Print operation-specific results
            if args.command == "test":
                if "coverage" in result.data:
                    print(f"\nCoverage report: {result.data['coverage_report']}")
                if "tox" in result.data:
                    print("\nTox Results:")
                    print(result.data["tox"]["stdout"])

            elif args.command == "lint":
                for linter, data in result.data.items():
                    print(f"\n{linter.upper()} Results:")
                    print(data["stdout"])
                    if data["stderr"]:
                        print("Errors:", file=sys.stderr)
                        print(data["stderr"], file=sys.stderr)

            elif args.command == "docs":
                if "docs_path" in result.data:
                    print(f"\nDocumentation built at: {result.data['docs_path']}")
                    if args.serve:
                        print("Documentation server started")

            elif args.command == "container":
                print(f"\n{args.op.title()} Results:")
                print(result.data[args.op]["stdout"])
                if result.data[args.op]["stderr"]:
                    print("Errors:", file=sys.stderr)
                    print(result.data[args.op]["stderr"], file=sys.stderr)

            # Store results if requested
            if args.store_results:
                memory_tool(
                    operation="store",
                    key=f"{args.command}_{args.type}_{timestamp}",
                    data=result.data,
                    tags=[args.command, args.type, timestamp[:10]]
                )
                print(f"\nResults stored with key: {args.command}_{args.type}_{timestamp}")

            return 0
        else:
            print(f"Error: {result.error}", file=sys.stderr)
            return 1

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())