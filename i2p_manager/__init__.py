"""
I2P Easy Manager
A lightweight tool for managing I2P network access with Firefox
"""

__version__ = "0.1.0"
__author__ = "eliasz130"
__license__ = "GPL-3.0-or-later"

from .config import ConfigManager
from .firefox import FirefoxManager
from .i2pd import I2PdManager

__all__ = [
    "ConfigManager",
    "FirefoxManager",
    "I2PdManager",
    "__version__",
]
