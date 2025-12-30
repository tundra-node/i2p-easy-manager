"""
Launch Firefox with I2P profile
"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def run(managers):
    """Launch Firefox with I2P profile"""
    config = managers["config"]
    i2pd = managers["i2pd"]
    firefox = managers["firefox"]

    console.print("\n[blue bold]🌐 Launching I2P Browser[/blue bold]\n")

    cfg = config.load()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        task = progress.add_task("Checking I2P status...", total=None)

        if not i2pd.is_running(cfg["i2pd"]["console_port"]):
            progress.stop()
            console.print("[yellow]⚠ I2P is not running[/yellow]")
            console.print(
                "\n[yellow]Browser will open but can't access I2P sites.[/yellow]"
            )
            console.print("[cyan]Start I2P first: i2p-manager start[/cyan]\n")

            # Ask if they want to continue
            try:
                response = input("Launch browser anyway? (y/N): ").strip().lower()
                if response not in ("y", "yes"):
                    console.print("[dim]Cancelled[/dim]\n")
                    return
            except KeyboardInterrupt:
                console.print("\n[dim]Cancelled[/dim]\n")
                return
        else:
            progress.update(task, description="[green]I2P is running[/green]")

        progress.update(task, description="Launching Firefox...")

        try:
            firefox.launch(cfg["firefox"]["profile_name"])
            progress.update(task, description="[green]Firefox launched[/green]")
        except Exception as e:
            progress.stop()
            console.print(f"[red]✗ Failed to launch Firefox:[/red] {e}")
            return

    console.print("\n[green bold]✓ Browser launched![/green bold]\n")
    console.print("Try these I2P sites:")
    console.print("  [cyan]• http://planet.i2p[/cyan] - News aggregator")
    console.print("  [cyan]• http://i2pforum.i2p[/cyan] - Community forum")
    console.print(
        f"  [cyan]• http://127.0.0.1:{cfg['i2pd']['console_port']}[/cyan] - Router console"
    )
    console.print()
