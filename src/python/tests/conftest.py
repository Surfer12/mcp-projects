"""
Pytest configuration and shared fixtures.
"""
import sys
from pathlib import Path

import pytest

# Add src to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture providing path to test data directory."""
    return Path(__file__).parent / "fixtures" / "data"


@pytest.fixture(scope="session")
def model_config():
    """Fixture providing standard model configuration."""
    return {
        "layers": [64, 32, 16],
        "activation": "relu",
        "dropout": 0.1,
        "learning_rate": 0.001,
    }


@pytest.fixture(scope="function")
def temp_workspace(tmp_path):
    """Fixture providing temporary workspace."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture(autouse=True)
def setup_logging():
    """Configure logging for tests."""
    import logging

    logging.basicConfig(level=logging.DEBUG)
