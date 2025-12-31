"""
CLI Entry Point
Command-line interface for I2P Easy Manager
"""

import sys
import click
from rich.console import Console

from . import __version__
from .config import ConfigManager
from .firefox import FirefoxManager
from .i2pd import I2PdManager
from .dashboard import launch_dashboard
from .commands import (
    cmd_init,
    cmd_start,
    cmd_stop,
    cmd_status,
    cmd_restart,
    cmd_browser,
    cmd_config,
    cmd_logs,
    cmd_reset,
)

console = Console()


def get_managers():
    """Create and return manager instances"""
    config = ConfigManager()
    return {
        "config": config,
        "firefox": FirefoxManager(config),
        "i2pd": I2PdManager(config),
    }


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="i2p-manager")
@click.pass_context
def main(ctx):
    """
    I2P Easy Manager - Simplified I2P network access

    Run without arguments to launch the interactive dashboard.
    """
    if ctx.invoked_subcommand is None:
        try:
            managers = get_managers()
            launch_dashboard(managers)
        except KeyboardInterrupt:
            console.print("\n[yellow]Dashboard closed[/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)


@main.command("init")
@click.option("--force", "-f", is_flag=True, help="Force reinitialize")
def initialize(force):
    """Initialize I2P Firefox profile and configuration"""
    try:
        managers = get_managers()
        cmd_init.run(managers, force=force)
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        sys.exit(1)


@main.command("start")
@click.option("--no-browser", is_flag=True, help="Don't launch Firefox")
def start(no_browser):
    """Start I2Pd and launch Firefox"""
    try:
        managers = get_managers()
        cmd_start.run(managers, browser=not no_browser)
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        sys.exit(1)


@main.command("stop")
def stop():
    """Stop I2Pd daemon"""
    try:
        managers = get_managers()
        cmd_stop.run(managers)
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        sys.exit(1)


@main.command("status")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed info")
def status(verbose):
    """Check I2P connection status"""
    try:
        managers = get_managers()
        cmd_status.run(managers, verbose=verbose)
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        sys.exit(1)


@main.command("restart")
def restart():
    """Restart I2Pd daemon"""
    try:
        managers = get_managers()
        cmd_restart.run(managers)
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        sys.exit(1)


@main.command("browser")
def browser():
    """Launch Firefox with I2P profile"""
    try:
        managers = get_managers()
        cmd_browser.run(managers)
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        sys.exit(1)


@main.command("config")
def config_edit():
    """Edit configuration file"""
    try:
        managers = get_managers()
        cmd_config.run(managers)
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        sys.exit(1)


@main.command("logs")
@click.option("--follow", "-f", is_flag=True, help="Follow log output")
@click.option("--lines", "-n", default=50, help="Number of lines", type=int)
def logs(follow, lines):
    """Show I2Pd logs"""
    try:
        managers = get_managers()
        cmd_logs.run(managers, follow=follow, lines=lines)
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        sys.exit(1)


@main.command("reset")
@click.option("--keep-i2pd-data", is_flag=True, help="Keep I2Pd data")
@click.confirmation_option(prompt="Reset everything?")
def reset(keep_i2pd_data):
    """Remove I2P profile and configuration"""
    try:
        managers = get_managers()
        cmd_reset.run(managers, keep_i2pd_data=keep_i2pd_data)
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
