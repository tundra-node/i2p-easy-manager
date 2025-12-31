"""Pytest configuration and shared fixtures"""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config_dir(temp_dir, monkeypatch):
    """Mock config directory to use temp directory"""

    def mock_get_config_dir():
        return temp_dir / "config"

    from i2p_manager import config

    monkeypatch.setattr(config.ConfigManager, "get_config_dir", mock_get_config_dir)

    return temp_dir / "config"


@pytest.fixture
def mock_firefox_profiles_dir(temp_dir, monkeypatch):
    """Mock Firefox profiles directory"""
    profiles_dir = temp_dir / "firefox_profiles"
    profiles_dir.mkdir()

    def mock_get_profiles_dir(self):
        return profiles_dir

    from i2p_manager import firefox

    monkeypatch.setattr(
        firefox.FirefoxManager, "get_profiles_dir", mock_get_profiles_dir
    )

    return profiles_dir
