"""Tests for CLI interface"""

import pytest
from click.testing import CliRunner
from i2p_manager.cli import main


class TestCLI:
    """Test CLI commands"""

    @pytest.fixture
    def runner(self):
        """Create CLI test runner"""
        return CliRunner()

    def test_version(self, runner):
        """Test --version flag"""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_help(self, runner):
        """Test --help flag"""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "I2P Easy Manager" in result.output
        assert "init" in result.output
        assert "start" in result.output

    def test_init_help(self, runner):
        """Test init command help"""
        result = runner.invoke(main, ["init", "--help"])
        assert result.exit_code == 0
        assert "Initialize" in result.output
        assert "--force" in result.output

    def test_start_help(self, runner):
        """Test start command help"""
        result = runner.invoke(main, ["start", "--help"])
        assert result.exit_code == 0
        assert "Start" in result.output
        assert "--no-browser" in result.output

    def test_status_help(self, runner):
        """Test status command help"""
        result = runner.invoke(main, ["status", "--help"])
        assert result.exit_code == 0
        assert "status" in result.output.lower()
        assert "--verbose" in result.output
