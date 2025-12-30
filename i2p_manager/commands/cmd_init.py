"""
Initialize I2P Firefox profile and configuration
"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def run(managers, force=False):
    """Initialize I2P profile and configuration"""
    config = managers["config"]
    firefox = managers["firefox"]
    i2pd = managers["i2pd"]

    console.print("\n[blue bold]🔧 I2P Easy Manager - Initialization[/blue bold]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        # Check dependencies
        task = progress.add_task("Checking dependencies...", total=None)

        firefox_installed = False
        i2pd_installed = False

        try:
            firefox.get_firefox_executable()
            firefox_installed = True
        except FileNotFoundError:
            pass

        i2pd_installed = i2pd.is_installed()

        if not firefox_installed:
            progress.stop()
            console.print("[red]✗ Firefox not found[/red]")
            console.print("\n[yellow]Please install Firefox:[/yellow]")
            console.print("  macOS: Download from https://mozilla.org/firefox/")
            console.print("  Linux: sudo apt install firefox")
            console.print("  Windows: Download from https://mozilla.org/firefox/")
            return

        if not i2pd_installed:
            progress.update(
                task, description="[yellow]I2Pd not found (optional)[/yellow]"
            )
            console.print("\n[yellow]Warning: I2Pd not found[/yellow]")
            console.print("Install I2Pd:")
            console.print("  macOS: brew install i2pd")
            console.print("  Linux: sudo apt install i2pd")
            console.print("  Windows: Download from i2pd.website")
            console.print("\nContinuing without I2Pd...\n")
        else:
            progress.update(task, description="[green]Dependencies found[/green]")

        # Initialize config
        progress.update(task, description="Creating configuration...")
        config.init()
        cfg = config.load()
        progress.update(task, description="[green]Configuration created[/green]")

        # Check if profile exists
        profile_name = cfg["firefox"]["profile_name"]

        if firefox.profile_exists(profile_name) and not force:
            progress.stop()
            console.print("[yellow]⚠ I2P profile already exists[/yellow]")
            console.print("\nUse --force to reinitialize\n")
            return

        # Create Firefox profile
        progress.update(task, description="Creating Firefox profile...")
        profile = firefox.create_profile(profile_name)
        progress.update(
            task, description=f"[green]Profile created: {profile['name']}[/green]"
        )

        # Apply Arkenfox hardening
        if cfg["firefox"]["harden_with_arkenfox"]:
            progress.update(task, description="Applying Arkenfox hardening...")
            firefox.apply_hardening(profile["path"])
            progress.update(
                task, description="[green]Arkenfox settings applied[/green]"
            )

        # Configure I2P proxy
        progress.update(task, description="Configuring I2P proxy...")
        firefox.configure_proxy(profile["path"])
        progress.update(task, description="[green]I2P proxy configured[/green]")

    # Success message
    console.print("\n[green bold]✓ Initialization complete![/green bold]\n")
    console.print("Next steps:")
    console.print("  [cyan]1.[/cyan] Start I2P: [white]i2p-manager start[/white]")
    console.print("  [cyan]2.[/cyan] Check status: [white]i2p-manager status[/white]")
    console.print("  [cyan]3.[/cyan] Wait 10-30 minutes for I2P network integration")
    console.print("  [cyan]4.[/cyan] Visit I2P sites (e.g., http://planet.i2p)")
    console.print()
