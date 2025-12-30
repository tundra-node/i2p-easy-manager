"""
Check I2P connection status
"""

from rich.console import Console
from rich.table import Table

console = Console()


def run(managers, verbose=False):
    """Check I2P connection status"""
    config = managers["config"]
    i2pd = managers["i2pd"]

    console.print("\n[blue bold]📊 I2P Manager Status[/blue bold]\n")

    cfg = config.load()
    status = i2pd.get_status(cfg["i2pd"]["console_port"])

    if status["running"]:
        console.print("[green bold]● I2Pd is running[/green bold]\n")

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Property", style="cyan")
        table.add_column("Value")

        peers = status.get("peers", 0)
        tunnels = status.get("tunnels", 0)

        # Determine connection quality
        if peers < 10:
            status_text = "[yellow]Connecting[/yellow]"
        elif peers < 50:
            status_text = "[yellow]Integrating[/yellow]"
        else:
            status_text = "[green]Connected[/green]"

        table.add_row("Status", status_text)
        table.add_row(
            "Router Console", f"http://127.0.0.1:{cfg['i2pd']['console_port']}"
        )
        table.add_row("HTTP Proxy", f"{cfg['i2pd']['host']}:{cfg['i2pd']['http_port']}")
        table.add_row("Known Peers", str(peers))
        table.add_row("Active Tunnels", str(tunnels))

        console.print(table)

        # Status message
        if peers < 10:
            console.print("\n[yellow]⚠️  Building connections...[/yellow]")
            console.print("[dim]This takes 10-30 minutes on first run[/dim]")
        elif peers < 50:
            console.print("\n[yellow]⏳ Network integration in progress...[/yellow]")
            console.print("[dim]Should be ready soon[/dim]")
        else:
            console.print("\n[green]✓ Fully integrated into I2P network[/green]")
            console.print("[dim]Ready to browse I2P sites[/dim]")

        if verbose:
            console.print("\n[cyan]Verbose Info:[/cyan]")
            console.print(f"  Config: {config.get_config_path()}")
            console.print(f"  Profile: {cfg['firefox']['profile_name']}")
            console.print(
                f"  Arkenfox: {'enabled' if cfg['firefox']['harden_with_arkenfox'] else 'disabled'}"
            )
    else:
        console.print("[red bold]● I2Pd is not running[/red bold]")
        console.print(
            "\n[yellow]Start I2P with:[/yellow] [cyan]i2p-manager start[/cyan]"
        )

    console.print()
