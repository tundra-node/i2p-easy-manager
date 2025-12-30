"""
Remove I2P profile and configuration
"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def run(managers, keep_i2pd_data=False):
    """Remove I2P profile and configuration"""
    config = managers["config"]
    firefox = managers["firefox"]
    i2pd = managers["i2pd"]

    console.print("\n[red bold]⚠️  Reset I2P Manager[/red bold]\n")
    console.print("[yellow]This will remove:[/yellow]")
    console.print("  • Firefox I2P profile")
    console.print("  • Configuration file")
    if not keep_i2pd_data:
        console.print("  • I2Pd network data")
    console.print()

    cfg = config.load()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        task = progress.add_task("Stopping I2Pd...", total=None)

        # Stop I2Pd
        if i2pd.is_running(cfg["i2pd"]["console_port"]):
            try:
                i2pd.stop()
                progress.update(task, description="[green]I2Pd stopped[/green]")
            except Exception:
                progress.update(
                    task, description="[yellow]Could not stop I2Pd[/yellow]"
                )
        else:
            progress.update(task, description="[yellow]I2Pd not running[/yellow]")

        # Remove Firefox profile
        progress.update(task, description="Removing Firefox profile...")
        profile_name = cfg["firefox"]["profile_name"]

        if firefox.profile_exists(profile_name):
            try:
                firefox.delete_profile(profile_name)
                progress.update(
                    task, description="[green]Firefox profile removed[/green]"
                )
            except Exception as e:
                progress.update(
                    task, description=f"[yellow]Could not remove profile: {e}[/yellow]"
                )
        else:
            progress.update(task, description="[yellow]Profile not found[/yellow]")

        # Remove config
        progress.update(task, description="Removing configuration...")
        config_path = config.get_config_path()

        if config_path.exists():
            try:
                config_path.unlink()
                progress.update(
                    task, description="[green]Configuration removed[/green]"
                )
            except Exception as e:
                progress.update(
                    task, description=f"[yellow]Could not remove config: {e}[/yellow]"
                )

    console.print("\n[green bold]✓ Reset complete[/green bold]\n")
    console.print("Run [cyan]i2p-manager init[/cyan] to set up again.\n")
