"""
I2Pd Daemon Control
Manages I2Pd router lifecycle across platforms
"""

import sys
import subprocess
import shutil
import requests
import re
from pathlib import Path
from typing import Dict, Optional


class I2PdManager:
    """Controls I2Pd daemon lifecycle"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.platform = sys.platform

    # === Status Checks ===

    def is_installed(self) -> bool:
        """Check if I2Pd is installed"""
        if shutil.which("i2pd"):
            return True

        # Windows: check common paths
        if self.platform == "win32":
            return self._find_i2pd_windows() is not None

        return False

    def is_running(self, console_port: Optional[int] = None) -> bool:
        """Check if I2Pd is running"""
        if console_port is None:
            console_port = self.config.get("i2pd.console_port", 7070)

        try:
            response = requests.get(f"http://127.0.0.1:{console_port}", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    # === Daemon Control ===

    def start(self):
        """Start I2Pd daemon"""
        if self.platform == "darwin":
            self._start_macos()
        elif self.platform == "win32":
            self._start_windows()
        else:
            self._start_linux()

    def stop(self):
        """Stop I2Pd daemon"""
        if self.platform == "darwin":
            self._stop_macos()
        elif self.platform == "win32":
            self._stop_windows()
        else:
            self._stop_linux()

    def restart(self):
        """Restart I2Pd daemon"""
        self.stop()
        import time

        time.sleep(2)
        self.start()

    # === Status Information ===

    def get_status(self, console_port: Optional[int] = None) -> Dict:
        """Get I2Pd status with network stats"""
        if console_port is None:
            console_port = self.config.get("i2pd.console_port", 7070)

        if not self.is_running(console_port):
            return {"running": False, "tunnels": 0, "peers": 0, "uptime": 0}

        try:
            response = requests.get(
                f"http://127.0.0.1:{console_port}/?page=status", timeout=5
            )

            if response.status_code == 200:
                html = response.text

                tunnels = self._extract_stat(html, r"Client Tunnels[^\d]*(\d+)")
                peers = self._extract_stat(html, r"Known Routers[^\d]*(\d+)")

                return {
                    "running": True,
                    "tunnels": tunnels,
                    "peers": peers,
                    "uptime": "unknown",
                }
        except Exception:
            pass

        return {"running": True, "tunnels": 0, "peers": 0, "uptime": "unknown"}

    def get_logs(self, lines: int = 50) -> str:
        """Get I2Pd log content"""
        log_path = self._get_log_path()

        if not log_path or not log_path.exists():
            return "Log file not found"

        try:
            if self.platform == "win32":
                with open(log_path, "r") as f:
                    all_lines = f.readlines()
                    return "".join(all_lines[-lines:])
            else:
                result = subprocess.run(
                    ["tail", "-n", str(lines), str(log_path)],
                    capture_output=True,
                    text=True,
                )
                return result.stdout
        except Exception as e:
            return f"Error reading logs: {e}"

    # === Platform-Specific Start/Stop ===

    def _start_macos(self):
        """Start I2Pd on macOS via Homebrew"""
        try:
            # Try brew
            subprocess.run(
                ["brew", "services", "start", "i2pd"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            # Fallback to manual
            subprocess.Popen(
                ["i2pd", "--daemon"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    def _start_windows(self):
        """Start I2Pd on Windows"""
        i2pd_path = self._find_i2pd_windows()
        if not i2pd_path:
            raise FileNotFoundError("I2Pd not found")

        subprocess.Popen(
            [i2pd_path, "--daemon"],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _start_linux(self):
        """Start I2Pd on Linux"""
        try:
            # Try systemd
            subprocess.run(
                ["sudo", "systemctl", "start", "i2pd"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            # Fallback to manual
            subprocess.Popen(
                ["i2pd", "--daemon"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    def _stop_macos(self):
        """Stop I2Pd on macOS"""
        subprocess.run(
            ["brew", "services", "stop", "i2pd"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _stop_windows(self):
        """Stop I2Pd on Windows"""
        subprocess.run(
            ["taskkill", "/F", "/IM", "i2pd.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _stop_linux(self):
        """Stop I2Pd on Linux"""
        try:
            subprocess.run(
                ["sudo", "systemctl", "stop", "i2pd"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            subprocess.run(
                ["pkill", "i2pd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

    # === Helpers ===

    def _get_log_path(self) -> Optional[Path]:
        """Get platform-specific log path"""
        if self.platform == "darwin":
            return Path("/usr/local/var/log/i2pd/i2pd.log")

        elif self.platform == "win32":
            paths = [
                Path(r"C:\ProgramData\i2pd\i2pd.log"),
                Path.home() / "AppData" / "Roaming" / "i2pd" / "i2pd.log",
            ]
            for path in paths:
                if path.exists():
                    return path
            return None

        else:  # Linux
            paths = [
                Path("/var/log/i2pd/i2pd.log"),
                Path.home() / ".i2pd" / "i2pd.log",
            ]
            for path in paths:
                if path.exists():
                    return path
            return None

    def _find_i2pd_windows(self) -> Optional[str]:
        """Find I2Pd executable on Windows"""
        paths = [
            r"C:\Program Files\i2pd\i2pd.exe",
            r"C:\Program Files (x86)\i2pd\i2pd.exe",
            Path.home() / "AppData" / "Local" / "i2pd" / "i2pd.exe",
        ]

        for path in paths:
            if Path(path).exists():
                return str(path)

        result = shutil.which("i2pd")
        return result

    def _extract_stat(self, html: str, pattern: str) -> int:
        """Extract numeric stat from HTML"""
        match = re.search(pattern, html, re.IGNORECASE)
        return int(match.group(1)) if match else 0
