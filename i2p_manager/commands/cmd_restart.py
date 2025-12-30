"""
Restart I2Pd daemon
"""

import time
from rich.console import Console

from . import cmd_stop, cmd_start

console = Console()


def run(managers):
    """Restart I2Pd daemon"""
    console.print("\n[blue bold]🔄 Restarting I2P Manager[/blue bold]\n")

    cmd_stop.run(managers)
    time.sleep(2)
    cmd_start.run(managers, browser=False)

    console.print("[green]✓ Restart complete[/green]\n")
