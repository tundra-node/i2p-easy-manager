"""
Open configuration file in editor
"""

import os
import sys
import subprocess
from rich.console import Console

console = Console()


def run(managers):
    """Open configuration file in default editor"""
    config = managers["config"]
    config_path = config.get_config_path()

    console.print("\n[blue]Opening config in default editor...[/blue]\n")
    console.print(f"[dim]Config file: {config_path}[/dim]\n")

    # Get default editor
    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL")

    if not editor:
        if sys.platform == "win32":
            editor = "notepad"
        else:
            editor = "nano"

    try:
        subprocess.run([editor, str(config_path)])
        console.print("[green]✓ Config editor closed[/green]\n")
    except Exception as e:
        console.print(f"[red]Error opening editor:[/red] {e}")
        console.print(f"\n[yellow]Manually edit:[/yellow] {config_path}\n")
