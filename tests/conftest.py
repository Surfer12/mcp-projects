"""
Pytest configuration and shared fixtures for MCP tests.
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator, Any

import docker
import pytest
from _pytest.fixtures import FixtureRequest
from playwright.sync_api import Page, Browser, BrowserContext

from mcp.tools.integrated import (
    DeveloperTool,
    AdvancedDeveloperTools,
    ComputerControlTool,
    MemoryTool,
    VisualizationTool
)


@pytest.fixture(scope="session")
def workspace_root() -> Path:
    """Provide a temporary workspace root directory for tests."""
    temp_dir = tempfile.mkdtemp(prefix="mcp_test_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def memory_storage(workspace_root: Path) -> Path:
    """Provide a temporary memory storage directory."""
    storage_dir = workspace_root / "memory"
    storage_dir.mkdir(parents=True, exist_ok=True)
    return storage_dir


@pytest.fixture(scope="session")
def viz_output(workspace_root: Path) -> Path:
    """Provide a temporary visualization output directory."""
    output_dir = workspace_root / "viz"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


@pytest.fixture
def dev_tool(workspace_root: Path) -> DeveloperTool:
    """Provide a configured DeveloperTool instance."""
    return DeveloperTool(workspace_root=workspace_root)


@pytest.fixture
def memory_tool(memory_storage: Path) -> MemoryTool:
    """Provide a configured MemoryTool instance."""
    return MemoryTool(storage_dir=memory_storage)


@pytest.fixture
def viz_tool(viz_output: Path) -> VisualizationTool:
    """Provide a configured VisualizationTool instance."""
    return VisualizationTool(output_dir=viz_output)


@pytest.fixture
def adv_tool(workspace_root: Path, memory_tool: MemoryTool) -> AdvancedDeveloperTools:
    """Provide a configured AdvancedDeveloperTools instance."""
    return AdvancedDeveloperTools(
        workspace_root=workspace_root,
        memory_tool=memory_tool
    )


@pytest.fixture
def ctrl_tool(workspace_root: Path) -> ComputerControlTool:
    """Provide a configured ComputerControlTool instance."""
    return ComputerControlTool(cache_dir=workspace_root / "cache")


@pytest.fixture(scope="session")
def docker_client() -> docker.DockerClient:
    """Provide a Docker client for container tests."""
    return docker.from_env()


@pytest.fixture
def mock_web_api(requests_mock: Any) -> Generator[Any, None, None]:
    """Mock external web API calls."""
    yield requests_mock


@pytest.fixture
def mock_async_web_api(aioresponses: Any) -> Generator[Any, None, None]:
    """Mock external async web API calls."""
    with aioresponses() as mock:
        yield mock


@pytest.fixture(scope="session")
def browser_context(
    browser: Browser,
    browser_context_args: dict,
) -> Generator[BrowserContext, None, None]:
    """Provide a browser context for E2E tests."""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture
def page(browser_context: BrowserContext) -> Generator[Page, None, None]:
    """Provide a browser page for E2E tests."""
    page = browser_context.new_page()
    yield page
    page.close()


def pytest_addoption(parser: Any) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--run-slow",
        action="store_true",
        default=False,
        help="run slow tests"
    )
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests"
    )
    parser.addoption(
        "--run-e2e",
        action="store_true",
        default=False,
        help="run end-to-end tests"
    )


def pytest_collection_modifyitems(config: Any, items: list) -> None:
    """Skip tests based on markers and command line options."""
    skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
    skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
    skip_e2e = pytest.mark.skip(reason="need --run-e2e option to run")

    for item in items:
        if "slow" in item.keywords and not config.getoption("--run-slow"):
            item.add_marker(skip_slow)
        if "integration" in item.keywords and not config.getoption("--run-integration"):
            item.add_marker(skip_integration)
        if "e2e" in item.keywords and not config.getoption("--run-e2e"):
            item.add_marker(skip_e2e)