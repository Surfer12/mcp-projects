"""
Tests for the AdvancedDeveloperTools class demonstrating various testing patterns.
"""

import json
from pathlib import Path
from typing import Any, Generator

import pytest
from _pytest.fixtures import FixtureRequest

from mcp.tools.integrated import AdvancedDeveloperTools


# Parameterized test data
TEST_CASES = [
    ("test", "tox", True, {"tox": {"returncode": 0}}),
    ("test", "coverage", True, {"coverage": {"returncode": 0}}),
    ("lint", "black", True, {"black": {"returncode": 0}}),
    ("docs", "sphinx", False, {"sphinx": {"returncode": 0}})
]


@pytest.fixture
def sample_test_file(workspace_root: Path) -> Generator[Path, None, None]:
    """Create a sample test file for testing."""
    test_file = workspace_root / "test_sample.py"
    test_file.write_text("""
def test_sample():
    assert True
""")
    yield test_file
    test_file.unlink()


@pytest.mark.parametrize("operation,op_type,store_results,expected", TEST_CASES)
def test_advanced_operations(
    adv_tool: AdvancedDeveloperTools,
    operation: str,
    op_type: str,
    store_results: bool,
    expected: dict[str, Any]
):
    """Test various advanced development operations."""
    # Arrange
    kwargs = {
        "operation": operation,
        f"{operation}_type": op_type,
        "store_results": store_results
    }

    # Act
    result = adv_tool(**kwargs)

    # Assert
    assert result.success
    for key, value in expected.items():
        assert key in result.data
        assert result.data[key]["returncode"] == value["returncode"]


@pytest.mark.integration
def test_linting_integration(
    adv_tool: AdvancedDeveloperTools,
    sample_test_file: Path
):
    """Test integrated linting workflow."""
    # Run all linters
    result = adv_tool(
        operation="lint",
        lint_type="all",
        store_results=True
    )

    assert result.success
    assert "black" in result.data
    assert "flake8" in result.data
    assert "mypy" in result.data


@pytest.mark.slow
def test_tox_multi_environment(
    adv_tool: AdvancedDeveloperTools,
    sample_test_file: Path
):
    """Test running tests in multiple Python environments."""
    result = adv_tool(
        operation="test",
        test_type="tox",
        store_results=True
    )

    assert result.success
    assert "tox" in result.data


def test_result_storage(
    adv_tool: AdvancedDeveloperTools,
    memory_tool: Any
):
    """Test that results are properly stored in memory."""
    # Run operation with result storage
    timestamp = adv_tool(
        operation="lint",
        lint_type="black",
        store_results=True
    ).data.get("timestamp")

    # Retrieve stored results
    stored_data = memory_tool(
        operation="retrieve",
        key=f"lint_results_black_{timestamp}"
    ).data

    assert stored_data is not None
    assert "black" in stored_data


@pytest.mark.e2e
def test_end_to_end_workflow(
    adv_tool: AdvancedDeveloperTools,
    workspace_root: Path,
    page: Any
):
    """Test complete end-to-end development workflow."""
    # Create test file
    test_file = workspace_root / "test_e2e.py"
    test_file.write_text("""
def test_e2e():
    assert True
""")

    try:
        # Run linting
        lint_result = adv_tool(
            operation="lint",
            lint_type="all",
            store_results=True
        )
        assert lint_result.success

        # Run tests with coverage
        test_result = adv_tool(
            operation="test",
            test_type="coverage",
            store_results=True
        )
        assert test_result.success

        # Build docs
        docs_result = adv_tool(
            operation="docs",
            doc_type="sphinx"
        )
        assert docs_result.success

        # Verify documentation was built
        docs_dir = workspace_root / "docs/build/html"
        assert docs_dir.exists()

    finally:
        test_file.unlink()


@pytest.mark.benchmark
def test_performance(benchmark: Any):
    """Test performance of development operations."""
    def run_lint():
        tool = AdvancedDeveloperTools()
        return tool(
            operation="lint",
            lint_type="black",
            store_results=False
        )

    result = benchmark(run_lint)
    assert result.success


class TestErrorHandling:
    """Test suite for error handling scenarios."""

    def test_invalid_operation(self, adv_tool: AdvancedDeveloperTools):
        """Test handling of invalid operations."""
        result = adv_tool(operation="invalid")
        assert not result.success
        assert "Unknown operation" in result.error

    def test_invalid_test_type(self, adv_tool: AdvancedDeveloperTools):
        """Test handling of invalid test types."""
        result = adv_tool(
            operation="test",
            test_type="invalid"
        )
        assert not result.success

    def test_missing_required_args(self, adv_tool: AdvancedDeveloperTools):
        """Test handling of missing required arguments."""
        result = adv_tool()
        assert not result.success
        assert "Invalid arguments" in result.error


@pytest.mark.container
class TestContainerOperations:
    """Test suite for container operations."""

    def test_build_container(
        self,
        adv_tool: AdvancedDeveloperTools,
        docker_client: Any
    ):
        """Test building a container."""
        result = adv_tool(
            operation="container",
            container_op="build"
        )
        assert result.success
        assert docker_client.images.get("mcp")

    def test_run_tests_in_container(
        self,
        adv_tool: AdvancedDeveloperTools
    ):
        """Test running tests inside a container."""
        result = adv_tool(
            operation="container",
            container_op="test",
            extra_args=["-v"]
        )
        assert result.success
        assert result.data["test"]["returncode"] == 0