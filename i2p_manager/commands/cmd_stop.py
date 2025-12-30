"""
Stop I2Pd daemon
"""

import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def run(managers):
    """Stop I2Pd daemon"""
    config = managers["config"]
    i2pd = managers["i2pd"]

    console.print("\n[blue bold]🛑 Stopping I2P Manager[/blue bold]\n")

    cfg = config.load()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        task = progress.add_task("Checking I2Pd status...", total=None)

        if not i2pd.is_running(cfg["i2pd"]["console_port"]):
            progress.update(task, description="[yellow]I2Pd is not running[/yellow]")
            console.print()
            return

        progress.update(task, description="Stopping I2Pd...")
        try:
            i2pd.stop()
            time.sleep(2)

            if not i2pd.is_running(cfg["i2pd"]["console_port"]):
                progress.update(
                    task, description="[green]I2Pd stopped successfully[/green]"
                )
            else:
                progress.update(
                    task, description="[yellow]I2Pd may still be running[/yellow]"
                )
        except Exception as e:
            progress.stop()
            console.print(f"[red]✗ Error stopping I2Pd:[/red] {e}")
            return

    console.print()
