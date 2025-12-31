"""Tests for utility functions"""

import pytest
from pathlib import Path


def test_get_platform():
    """Test platform detection"""
    from i2p_manager.utils import get_platform

    platform = get_platform()
    assert platform in ("darwin", "linux", "win32")
