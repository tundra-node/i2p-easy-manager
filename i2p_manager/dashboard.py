"""
Interactive Dashboard UI
Clean, simple interface for managing I2P
"""

import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text

console = Console()


class Dashboard:
    def __init__(self, managers):
        self.config = managers["config"]
        self.i2pd = managers["i2pd"]
        self.firefox = managers["firefox"]
        self.running = True
        self.status_data = None

    def create_layout(self) -> Layout:
        """Create the dashboard layout"""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3),
        )

        layout["body"].split_row(
            Layout(name="status", ratio=1), Layout(name="network", ratio=1)
        )

        return layout

    def render_header(self) -> Panel:
        """Render the header"""
        title = Text(
            "I2P EASY MANAGER v0.1.0", style="bold white on blue", justify="center"
        )
        return Panel(title, border_style="blue")

    def render_status(self) -> Panel:
        """Render connection status"""
        if not self.status_data:
            return Panel(
                "[yellow]Checking status...[/yellow]",
                title="Connection Status",
                border_style="cyan",
            )

        content = Text()

        if self.status_data.get("running"):
            peers = self.status_data.get("peers", 0)

            # Determine status color and text
            if peers < 10:
                status_color = "yellow"
                status_text = "● CONNECTING"
            elif peers < 50:
                status_color = "yellow"
                status_text = "● INTEGRATING"
            else:
                status_color = "green"
                status_text = "● CONNECTED"

            content.append("\nStatus: ", style="white")
            content.append(f"{status_text}\n\n", style=status_color)
            content.append("Router: ", style="white")
            content.append("Running\n", style="green")

            cfg = self.config.load()
            proxy_addr = f"{cfg['i2pd']['host']}:{cfg['i2pd']['http_port']}"
            content.append("Proxy: ", style="white")
            content.append(f"{proxy_addr}\n", style="cyan")
            content.append("Console: ", style="white")
            content.append(
                f"http://127.0.0.1:{cfg['i2pd']['console_port']}", style="cyan"
            )
        else:
            content.append("\nStatus: ", style="white")
            content.append("● DISCONNECTED\n\n", style="red")
            content.append("Router: ", style="white")
            content.append("Stopped\n", style="red")
            content.append("Proxy: ", style="white")
            content.append("Unavailable\n", style="dim")
            content.append("Console: ", style="white")
            content.append("Unavailable", style="dim")

        return Panel(content, title="Connection Status", border_style="cyan")

    def render_network(self) -> Panel:
        """Render network info"""
        if not self.status_data or not self.status_data.get("running"):
            content = Text()
            content.append("\nKnown Peers: ", style="white")
            content.append("N/A\n\n", style="dim")
            content.append("Active Tunnels: ", style="white")
            content.append("N/A\n\n", style="dim")
            content.append("I2P is not running", style="dim")
            return Panel(content, title="Network Info", border_style="cyan")

        peers = self.status_data.get("peers", 0)
        tunnels = self.status_data.get("tunnels", 0)

        content = Text()
        content.append("\nKnown Peers: ", style="white")
        content.append(f"{peers}\n\n", style="yellow")
        content.append("Active Tunnels: ", style="white")
        content.append(f"{tunnels}\n\n", style="yellow")

        if peers < 10:
            content.append("⚠ Building connections...\n", style="yellow")
            content.append("(10-30 min on first run)", style="dim")
        elif peers < 50:
            content.append("⏳ Integrating...\n", style="yellow")
            content.append("(May take a few minutes)", style="dim")
        else:
            content.append("✓ Fully Integrated\n", style="green")
            content.append("Ready to browse I2P", style="dim")

        return Panel(content, title="Network Info", border_style="cyan")

    def render_menu(self) -> Panel:
        """Render menu options"""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", no_wrap=True)
        table.add_column(style="white")
        table.add_column(style="cyan", no_wrap=True)
        table.add_column(style="white")

        table.add_row("[1]", "Start I2P", "[5]", "View Configuration")
        table.add_row("[2]", "Stop I2P", "[6]", "View Logs")
        table.add_row("[3]", "Restart I2P", "[7]", "Reset Everything")
        table.add_row("[4]", "Launch Browser", "[8]", "Help & About")
        table.add_row("", "")
        table.add_row("[R]", "Refresh Status", "[Q]", "Quit")

        return Panel(table, title="Quick Actions", border_style="green")

    def update_display(self, layout: Layout):
        """Update all dashboard components"""
        layout["header"].update(self.render_header())
        layout["body"]["status"].update(self.render_status())
        layout["body"]["network"].update(self.render_network())
        layout["footer"].update(Layout(self.render_menu(), size=10))

    def update_status(self):
        """Update I2P status data"""
        try:
            cfg = self.config.load()
            self.status_data = self.i2pd.get_status(cfg["i2pd"]["console_port"])
        except Exception:
            self.status_data = {"running": False}

    def handle_input(self, key: str) -> bool:
        """Handle keyboard input. Returns False if should quit."""
        if key.lower() == "q":
            return False
        elif key == "1":
            self.action_start()
        elif key == "2":
            self.action_stop()
        elif key == "3":
            self.action_restart()
        elif key == "4":
            self.action_browser()
        elif key == "5":
            self.action_config()
        elif key == "6":
            self.action_logs()
        elif key == "7":
            self.action_reset()
        elif key == "8":
            self.action_help()
        elif key.lower() == "r":
            pass  # Refresh happens automatically

        return True

    def action_start(self):
        """Start I2P"""
        console.clear()
        console.print("[blue]Starting I2P...[/blue]")

        if self.status_data and self.status_data.get("running"):
            console.print("[yellow]I2P is already running[/yellow]")
            time.sleep(2)
            return

        try:
            self.i2pd.start()
            time.sleep(3)

            cfg = self.config.load()
            self.firefox.launch(cfg["firefox"]["profile_name"])

            console.print("[green]✓ I2P started successfully![/green]")
            console.print("[green]✓ Firefox launched[/green]")
            console.print("[yellow]Wait 10-30 minutes for network integration[/yellow]")
            time.sleep(3)
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]")
            time.sleep(3)

    def action_stop(self):
        """Stop I2P"""
        console.clear()
        console.print("[blue]Stopping I2P...[/blue]")

        try:
            self.i2pd.stop()
            console.print("[green]✓ I2P stopped[/green]")
            time.sleep(2)
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]")
            time.sleep(3)

    def action_restart(self):
        """Restart I2P"""
        self.action_stop()
        time.sleep(2)
        self.action_start()

    def action_browser(self):
        """Launch browser"""
        console.clear()
        console.print("[blue]Launching Firefox...[/blue]")

        try:
            cfg = self.config.load()
            self.firefox.launch(cfg["firefox"]["profile_name"])
            console.print("[green]✓ Firefox launched[/green]")
            time.sleep(2)
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]")
            time.sleep(3)

    def action_config(self):
        """Show config location"""
        console.clear()
        console.print("[blue]Configuration File:[/blue]")
        console.print(f"  {self.config.get_config_path()}")
        console.print("\n[yellow]Edit with: i2p-manager config[/yellow]")
        input("\nPress Enter to continue...")

    def action_logs(self):
        """Show logs info"""
        console.clear()
        console.print("[blue]View Logs:[/blue]")
        console.print("  i2p-manager logs")
        console.print("  i2p-manager logs -f  (follow)")
        input("\nPress Enter to continue...")

    def action_reset(self):
        """Reset warning"""
        console.clear()
        console.print("[red]Reset requires confirmation.[/red]")
        console.print("[yellow]Use: i2p-manager reset[/yellow]")
        input("\nPress Enter to continue...")

    def action_help(self):
        """Show help"""
        console.clear()
        console.print("[blue bold]I2P Easy Manager - Help[/blue bold]\n")
        console.print("[cyan]Dashboard Keys:[/cyan]")
        console.print("  1-8: Quick actions")
        console.print("  R: Refresh status")
        console.print("  Q: Quit dashboard\n")
        console.print("[cyan]Command-line usage:[/cyan]")
        console.print("  i2p-manager <command>\n")
        console.print("[cyan]Resources:[/cyan]")
        console.print("  Router Console: http://127.0.0.1:7070")
        console.print("  I2P Forum: http://i2pforum.i2p")
        console.print("  Planet I2P: http://planet.i2p")
        input("\nPress Enter to continue...")


def launch_dashboard(managers):
    """Launch the interactive dashboard"""
    # Platform-specific imports
    if sys.platform == "win32":
        import msvcrt
    else:
        import select

    dashboard = Dashboard(managers)

    # Initial status update
    dashboard.update_status()

    layout = dashboard.create_layout()

    # For non-blocking keyboard input
    def get_key():
        """Get a single keypress"""
        if sys.platform == "win32":
            if msvcrt.kbhit():
                return msvcrt.getch().decode("utf-8")
        else:
            if select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.read(1)
        return None

    try:
        console.clear()
        last_update = time.time()

        while dashboard.running:
            # Update status every 5 seconds
            if time.time() - last_update > 5:
                dashboard.update_status()
                last_update = time.time()

            # Update display
            dashboard.update_display(layout)
            console.clear()
            console.print(layout)

            # Check for input
            time.sleep(0.1)
            key = get_key()

            if key:
                if not dashboard.handle_input(key):
                    break

    except KeyboardInterrupt:
        pass
    finally:
        console.clear()
        console.print("[yellow]Dashboard closed[/yellow]")
