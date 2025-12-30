"""
Configuration Management
Handles application configuration with validation
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Manages application configuration"""

    DEFAULT_CONFIG = {
        "i2pd": {
            "host": "127.0.0.1",
            "http_port": 4444,
            "https_port": 4444,
            "socks_port": 4447,
            "console_port": 7070,
        },
        "firefox": {
            "profile_name": "i2p-secure",
            "harden_with_arkenfox": True,
        },
        "dashboard": {
            "refresh_interval": 5,
            "show_welcome": True,
        },
        "version": "0.1.0",
    }

    def __init__(self):
        self.platform = sys.platform
        self._config_cache: Optional[Dict] = None

    def get_config_dir(self) -> Path:
        """Get configuration directory"""
        home = Path.home()

        if self.platform in ("darwin", "linux") or self.platform.startswith("linux"):
            return home / ".config" / "i2p-manager"
        elif self.platform == "win32":
            return home / "AppData" / "Local" / "i2p-manager"
        else:
            return home / ".config" / "i2p-manager"

    def get_config_path(self) -> Path:
        """Get configuration file path"""
        return self.get_config_dir() / "config.json"

    def init(self) -> Dict[str, Any]:
        """Initialize configuration file"""
        config_dir = self.get_config_dir()
        config_path = self.get_config_path()

        config_dir.mkdir(parents=True, exist_ok=True)

        if config_path.exists():
            return self.load()

        with open(config_path, "w") as f:
            json.dump(self.DEFAULT_CONFIG, f, indent=2)

        self._config_cache = self.DEFAULT_CONFIG.copy()
        return self._config_cache

    def load(self) -> Dict[str, Any]:
        """Load configuration with caching"""
        if self._config_cache is not None:
            return self._config_cache

        config_path = self.get_config_path()

        try:
            if config_path.exists():
                with open(config_path, "r") as f:
                    config = json.load(f)
                self._config_cache = self._merge(self.DEFAULT_CONFIG, config)
                return self._config_cache
        except Exception:
            pass

        self._config_cache = self.DEFAULT_CONFIG.copy()
        return self._config_cache

    def save(self, config: Dict[str, Any]):
        """Save configuration"""
        config_path = self.get_config_path()
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        self._config_cache = config

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value with dot notation (e.g., 'i2pd.http_port')"""
        config = self.load()
        keys = key.split(".")

        value = config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """Set config value with dot notation"""
        config = self.load()
        keys = key.split(".")

        current = config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value
        self.save(config)

    def reset(self) -> Dict[str, Any]:
        """Reset to default configuration"""
        self.save(self.DEFAULT_CONFIG.copy())
        return self._config_cache

    def _merge(self, default: Dict, custom: Dict) -> Dict:
        """Recursively merge configurations"""
        result = default.copy()

        for key, value in custom.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge(result[key], value)
            else:
                result[key] = value

        return result
