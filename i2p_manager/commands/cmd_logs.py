"""
Show I2Pd logs
"""

import sys
import subprocess
from rich.console import Console

console = Console()


def run(managers, follow=False, lines=50):
    """Show I2Pd logs"""
    i2pd = managers["i2pd"]

    console.print("\n[blue bold]📋 I2Pd Logs[/blue bold]\n")

    if follow and sys.platform != "win32":
        console.print("[dim]Following logs... Press Ctrl+C to exit[/dim]\n")
        log_path = i2pd._get_log_path()

        if log_path and log_path.exists():
            try:
                subprocess.run(["tail", "-f", str(log_path)])
            except KeyboardInterrupt:
                console.print("\n[dim]Stopped following logs[/dim]\n")
        else:
            console.print("[yellow]Log file not found[/yellow]\n")
    else:
        log_content = i2pd.get_logs(lines)
        console.print(log_content)
        console.print()
