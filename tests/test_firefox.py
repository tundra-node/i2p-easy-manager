"""Tests for Firefox profile management"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from i2p_manager.firefox import FirefoxManager
from i2p_manager.config import ConfigManager


class TestFirefoxManager:
    """Test FirefoxManager class"""

    @pytest.fixture
    def config_manager(self):
        """Create ConfigManager fixture"""
        return ConfigManager()

    @pytest.fixture
    def firefox_manager(self, config_manager):
        """Create FirefoxManager fixture"""
        return FirefoxManager(config_manager)

    def test_init(self, firefox_manager):
        """Test FirefoxManager initialization"""
        assert firefox_manager.config is not None
        assert firefox_manager.platform is not None

    def test_get_profiles_dir_returns_path(self, firefox_manager):
        """Test profiles directory path is returned"""
        profiles_dir = firefox_manager.get_profiles_dir()
        assert isinstance(profiles_dir, Path)
        assert "Firefox" in str(profiles_dir) or "firefox" in str(profiles_dir)

    @patch("i2p_manager.firefox.os.path.exists")
    def test_get_firefox_executable_darwin(self, mock_exists, firefox_manager):
        """Test Firefox executable path on macOS"""
        firefox_manager.platform = "darwin"
        mock_exists.return_value = True

        firefox_path = firefox_manager.get_firefox_executable()
        assert "Firefox.app" in firefox_path

    @patch("i2p_manager.firefox.shutil.which")
    def test_get_firefox_executable_linux(self, mock_which, firefox_manager):
        """Test Firefox executable path on Linux"""
        firefox_manager.platform = "linux"
        mock_which.return_value = "/usr/bin/firefox"

        firefox_path = firefox_manager.get_firefox_executable()
        assert firefox_path == "/usr/bin/firefox"

    @patch("i2p_manager.firefox.os.path.exists")
    def test_get_firefox_executable_not_found(self, mock_exists, firefox_manager):
        """Test Firefox not found raises error"""
        firefox_manager.platform = "darwin"
        mock_exists.return_value = False

        with pytest.raises(FileNotFoundError):
            firefox_manager.get_firefox_executable()

    def test_profile_exists(self, firefox_manager, tmp_path):
        """Test profile existence check"""
        # Mock profiles directory
        firefox_manager.get_profiles_dir = lambda: tmp_path

        # Create fake profile
        profile_path = tmp_path / "i2p-secure.default"
        profile_path.mkdir()

        assert firefox_manager.profile_exists("i2p-secure") is True
        assert firefox_manager.profile_exists("nonexistent") is False

    @patch("i2p_manager.firefox.subprocess.run")
    def test_create_profile(self, mock_run, firefox_manager, tmp_path):
        """Test profile creation"""
        firefox_manager.get_profiles_dir = lambda: tmp_path
        firefox_manager.get_firefox_executable = lambda: "/usr/bin/firefox"

        profile = firefox_manager.create_profile("test-profile")

        assert profile["name"] == "test-profile"
        assert "test-profile.default" in profile["path"]

    def test_configure_proxy(self, firefox_manager, tmp_path):
        """Test proxy configuration"""
        profile_path = tmp_path / "profile"
        profile_path.mkdir()

        firefox_manager.configure_proxy(str(profile_path))

        user_js = profile_path / "user.js"
        assert user_js.exists()

        content = user_js.read_text()
        assert "network.proxy.type" in content
        assert "127.0.0.1" in content
        assert "4444" in content
