#!/usr/bin/env python3
"""
Script to run MCP test suite with different configurations and generate reports.
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from mcp.tools.integrated import AdvancedDeveloperTools, MemoryTool


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run MCP test suite")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run only quick tests (no slow/integration/e2e)"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run all tests including slow, integration, and e2e"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "--lint",
        action="store_true",
        help="Run linting checks"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate HTML test report"
    )
    parser.add_argument(
        "--container",
        action="store_true",
        help="Run tests in container"
    )
    return parser.parse_args()


def run_test_suite(args: argparse.Namespace) -> bool:
    """Run the test suite with specified configuration."""
    workspace = Path.cwd()
    memory_tool = MemoryTool()
    adv_tool = AdvancedDeveloperTools(
        workspace_root=workspace,
        memory_tool=memory_tool
    )

    timestamp = datetime.utcnow().isoformat()
    success = True

    try:
        # Run linting if requested
        if args.lint:
            print("Running linting checks...")
            result = adv_tool(
                operation="lint",
                lint_type="all",
                store_results=True
            )
            success = success and result.success

        # Determine test arguments
        test_args = []
        if args.quick:
            test_args.extend(["-m", "not (slow or integration or e2e)"])
        elif args.full:
            test_args.extend(["--run-slow", "--run-integration", "--run-e2e"])

        if args.coverage:
            test_args.extend(["--cov=src", "--cov-report=html"])

        if args.report:
            test_args.extend(["--html=reports/report.html"])

        # Run tests
        if args.container:
            print("Running tests in container...")
            result = adv_tool(
                operation="container",
                container_op="test",
                extra_args=test_args
            )
        else:
            print("Running tests...")
            result = adv_tool(
                operation="test",
                test_type="coverage" if args.coverage else "pytest",
                extra_args=test_args,
                store_results=True
            )

        success = success and result.success

        # Store test results
        memory_tool(
            operation="store",
            key=f"test_run_{timestamp}",
            data={
                "args": vars(args),
                "result": result.data,
                "success": success
            },
            tags=["test_run", timestamp[:10]]
        )

        return success

    except Exception as e:
        print(f"Error running tests: {e}", file=sys.stderr)
        return False


def main() -> int:
    """Main entry point."""
    args = parse_args()
    success = run_test_suite(args)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())