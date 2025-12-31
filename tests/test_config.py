"""Tests for configuration management"""

import pytest
import json
from pathlib import Path
from i2p_manager.config import ConfigManager


class TestConfigManager:
    """Test ConfigManager class"""

    def test_default_config_structure(self):
        """Test default configuration has correct structure"""
        config = ConfigManager()
        default = config.DEFAULT_CONFIG

        assert "i2pd" in default
        assert "firefox" in default
        assert "dashboard" in default
        assert "version" in default

    def test_default_i2pd_config(self):
        """Test default I2Pd configuration"""
        config = ConfigManager()
        assert config.DEFAULT_CONFIG["i2pd"]["host"] == "127.0.0.1"
        assert config.DEFAULT_CONFIG["i2pd"]["http_port"] == 4444
        assert config.DEFAULT_CONFIG["i2pd"]["console_port"] == 7070

    def test_default_firefox_config(self):
        """Test default Firefox configuration"""
        config = ConfigManager()
        assert config.DEFAULT_CONFIG["firefox"]["profile_name"] == "i2p-secure"
        assert config.DEFAULT_CONFIG["firefox"]["harden_with_arkenfox"] is True

    def test_get_config_dir(self):
        """Test config directory path"""
        config = ConfigManager()
        config_dir = config.get_config_dir()

        assert isinstance(config_dir, Path)
        assert "i2p-manager" in str(config_dir)

    def test_get_config_path(self):
        """Test config file path"""
        config = ConfigManager()
        config_path = config.get_config_path()

        assert isinstance(config_path, Path)
        assert config_path.name == "config.json"

    def test_get_nested_value(self):
        """Test getting nested config values"""
        config = ConfigManager()
        config._config_cache = config.DEFAULT_CONFIG.copy()

        port = config.get("i2pd.http_port")
        assert port == 4444

        profile = config.get("firefox.profile_name")
        assert profile == "i2p-secure"

    def test_get_with_default(self):
        """Test get with default value for missing keys"""
        config = ConfigManager()
        config._config_cache = config.DEFAULT_CONFIG.copy()

        value = config.get("nonexistent.key", "default")
        assert value == "default"

    def test_merge_configs(self):
        """Test configuration merging"""
        config = ConfigManager()

        default = {"a": 1, "b": {"c": 2, "d": 3}}
        custom = {"b": {"c": 99}, "e": 4}

        merged = config._merge(default, custom)

        assert merged["a"] == 1
        assert merged["b"]["c"] == 99  # Custom overrides
        assert merged["b"]["d"] == 3  # Default preserved
        assert merged["e"] == 4  # New key added

    def test_set_nested_value(self, tmp_path):
        """Test setting nested config values"""
        # Use temporary config directory
        config = ConfigManager()

        # Mock config path to temp directory
        original_get_config_dir = config.get_config_dir
        config.get_config_dir = lambda: tmp_path

        # Initialize config
        config.init()

        # Set new value
        config.set("i2pd.http_port", 8080)

        # Verify it was set
        assert config.get("i2pd.http_port") == 8080

        # Restore original method
        config.get_config_dir = original_get_config_dir
