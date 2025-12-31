"""Tests for I2Pd daemon control"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from i2p_manager.i2pd import I2PdManager
from i2p_manager.config import ConfigManager


class TestI2PdManager:
    """Test I2PdManager class"""

    @pytest.fixture
    def config_manager(self):
        """Create ConfigManager fixture"""
        return ConfigManager()

    @pytest.fixture
    def i2pd_manager(self, config_manager):
        """Create I2PdManager fixture"""
        return I2PdManager(config_manager)

    def test_init(self, i2pd_manager):
        """Test I2PdManager initialization"""
        assert i2pd_manager.config is not None
        assert i2pd_manager.platform is not None

    @patch("i2p_manager.i2pd.shutil.which")
    def test_is_installed_true(self, mock_which, i2pd_manager):
        """Test I2Pd is detected when installed"""
        mock_which.return_value = "/usr/bin/i2pd"
        assert i2pd_manager.is_installed() is True

    @patch("i2p_manager.i2pd.shutil.which")
    def test_is_installed_false(self, mock_which, i2pd_manager):
        """Test I2Pd is not detected when not installed"""
        mock_which.return_value = None
        assert i2pd_manager.is_installed() is False

    @patch("i2p_manager.i2pd.requests.get")
    def test_is_running_true(self, mock_get, i2pd_manager):
        """Test I2Pd running detection"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        assert i2pd_manager.is_running(7070) is True

    @patch("i2p_manager.i2pd.requests.get")
    def test_is_running_false(self, mock_get, i2pd_manager):
        """Test I2Pd not running detection"""
        mock_get.side_effect = Exception("Connection refused")

        assert i2pd_manager.is_running(7070) is False

    @patch("i2p_manager.i2pd.requests.get")
    def test_get_status_running(self, mock_get, i2pd_manager):
        """Test status when I2Pd is running"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Client Tunnels: 8\nKnown Routers: 156"
        mock_get.return_value = mock_response

        status = i2pd_manager.get_status(7070)

        assert status["running"] is True
        assert status["tunnels"] == 8
        assert status["peers"] == 156

    @patch("i2p_manager.i2pd.requests.get")
    def test_get_status_not_running(self, mock_get, i2pd_manager):
        """Test status when I2Pd is not running"""
        mock_get.side_effect = Exception("Connection refused")

        status = i2pd_manager.get_status(7070)

        assert status["running"] is False
        assert status["tunnels"] == 0
        assert status["peers"] == 0

    def test_extract_stat(self, i2pd_manager):
        """Test extracting stats from HTML"""
        html = "Client Tunnels: 8\nKnown Routers: 156"

        tunnels = i2pd_manager._extract_stat(html, r"Client Tunnels[^\d]*(\d+)")
        peers = i2pd_manager._extract_stat(html, r"Known Routers[^\d]*(\d+)")

        assert tunnels == 8
        assert peers == 156

    def test_extract_stat_not_found(self, i2pd_manager):
        """Test extracting non-existent stat"""
        html = "Some text"
        result = i2pd_manager._extract_stat(html, r"Nonexistent[^\d]*(\d+)")
        assert result == 0
