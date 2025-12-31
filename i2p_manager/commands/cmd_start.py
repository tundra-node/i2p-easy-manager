"""
Start I2Pd and launch Firefox with I2P profile
"""

import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def run(managers, browser=True):
    """Start I2P and optionally launch browser"""
    config = managers["config"]
    i2pd = managers["i2pd"]
    firefox = managers["firefox"]

    console.print("\n[blue bold]🚀 Starting I2P Manager[/blue bold]\n")

    cfg = config.load()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        task = progress.add_task("Checking I2Pd status...", total=None)

        running = i2pd.is_running(cfg["i2pd"]["console_port"])

        if running:
            progress.update(task, description="[green]I2Pd is already running[/green]")
        else:
            progress.update(task, description="Starting I2Pd...")
            try:
                i2pd.start()
                time.sleep(3)

                if i2pd.is_running(cfg["i2pd"]["console_port"]):
                    progress.update(
                        task, description="[green]I2Pd started successfully[/green]"
                    )
                else:
                    progress.stop()
                    console.print("[red]✗ I2Pd failed to start[/red]")
                    console.print("\n[yellow]Try starting manually:[/yellow]")
                    console.print("  macOS: brew services start i2pd")
                    console.print("  Linux: sudo systemctl start i2pd")
                    console.print("  Windows: Run i2pd.exe")
                    console.print("\n[yellow]Check logs: i2p-manager logs[/yellow]\n")
                    return
            except Exception as e:
                progress.stop()
                console.print(f"[red]✗ Error starting I2Pd:[/red] {e}")
                return

        if browser:
            progress.update(task, description="Launching Firefox...")
            try:
                firefox.launch(cfg["firefox"]["profile_name"])
                progress.update(task, description="[green]Firefox launched[/green]")
            except Exception as e:
                progress.stop()
                console.print(f"[red]✗ Failed to launch Firefox:[/red] {e}")
                return

    console.print("\n[green bold]✓ I2P is running![/green bold]\n")
    console.print(
        f"Router console: [cyan]http://127.0.0.1:{cfg['i2pd']['console_port']}[/cyan]"
    )
    console.print("\n[yellow]First time?[/yellow]")
    console.print("  • Wait 10-30 minutes for network integration")
    console.print("  • Check status: [cyan]i2p-manager status[/cyan]")
    console.print("  • Try visiting: [cyan]http://planet.i2p[/cyan]\n")
