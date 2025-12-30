"""
Firefox Profile Management
Creates and configures hardened Firefox profiles for I2P
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Dict


class FirefoxManager:
    """Manages Firefox profile creation and configuration"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.platform = sys.platform

    # === Directory Paths ===

    def get_profiles_dir(self) -> Path:
        """Get Firefox profiles directory"""
        home = Path.home()

        if self.platform == "darwin":
            return home / "Library" / "Application Support" / "Firefox" / "Profiles"
        elif self.platform == "win32":
            return home / "AppData" / "Roaming" / "Mozilla" / "Firefox" / "Profiles"
        else:  # Linux
            return home / ".mozilla" / "firefox"

    def get_firefox_executable(self) -> str:
        """Get Firefox executable path"""
        if self.platform == "darwin":
            path = "/Applications/Firefox.app/Contents/MacOS/firefox"
            if not os.path.exists(path):
                raise FileNotFoundError(
                    "Firefox not found at /Applications/Firefox.app"
                )
            return path

        elif self.platform == "win32":
            paths = [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
            raise FileNotFoundError("Firefox not installed")

        else:  # Linux
            result = shutil.which("firefox")
            if not result:
                raise FileNotFoundError("Firefox not found in PATH")
            return result

    # === Profile Management ===

    def profile_exists(self, profile_name: str) -> bool:
        """Check if profile exists"""
        profile_path = self.get_profiles_dir() / f"{profile_name}.default"
        return profile_path.exists()

    def create_profile(self, profile_name: str) -> Dict[str, str]:
        """Create new Firefox profile"""
        firefox_exe = self.get_firefox_executable()
        profiles_dir = self.get_profiles_dir()
        profiles_dir.mkdir(parents=True, exist_ok=True)

        profile_path = profiles_dir / f"{profile_name}.default"

        # Create via Firefox CLI
        try:
            subprocess.run(
                [firefox_exe, "-CreateProfile", f"{profile_name} {profile_path}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
            )
        except Exception:
            pass  # Profile might exist

        profile_path.mkdir(parents=True, exist_ok=True)

        return {"name": profile_name, "path": str(profile_path)}

    def delete_profile(self, profile_name: str):
        """Delete Firefox profile"""
        profile_path = self.get_profiles_dir() / f"{profile_name}.default"
        if profile_path.exists():
            shutil.rmtree(profile_path)

    # === Configuration ===

    def apply_hardening(self, profile_path: str):
        """Apply Arkenfox hardening"""
        profile_dir = Path(profile_path)
        user_js = profile_dir / "user.js"

        # Get template from package data
        template_path = Path(__file__).parent / "data" / "user.js"

        if template_path.exists():
            shutil.copy(template_path, user_js)
        else:
            # Fallback: minimal hardening
            self._create_minimal_config(user_js)

    def configure_proxy(self, profile_path: str):
        """Configure I2P proxy settings"""
        profile_dir = Path(profile_path)
        user_js = profile_dir / "user.js"

        i2pd_config = self.config.load()["i2pd"]

        proxy_config = f"""
// I2P Proxy Configuration
user_pref("network.proxy.type", 1);
user_pref("network.proxy.http", "{i2pd_config['host']}");
user_pref("network.proxy.http_port", {i2pd_config['http_port']});
user_pref("network.proxy.ssl", "{i2pd_config['host']}");
user_pref("network.proxy.ssl_port", {i2pd_config['https_port']});
user_pref("network.proxy.socks", "{i2pd_config['host']}");
user_pref("network.proxy.socks_port", {i2pd_config['socks_port']});
user_pref("network.proxy.socks_version", 5);
user_pref("network.proxy.no_proxies_on", "");
user_pref("network.proxy.socks_remote_dns", true);
user_pref("media.peerconnection.ice.proxy_only", true);
"""

        with open(user_js, "a") as f:
            f.write(proxy_config)

    # === Launch ===

    def launch(self, profile_name: str):
        """Launch Firefox with profile"""
        firefox_exe = self.get_firefox_executable()

        cmd = [firefox_exe, "-P", profile_name, "-no-remote"]

        if self.platform == "win32":
            subprocess.Popen(
                cmd,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            subprocess.Popen(
                cmd,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    # === Helpers ===

    def _create_minimal_config(self, user_js_path: Path):
        """Create minimal hardening config if template missing"""
        config = """
// Minimal I2P Firefox Hardening
user_pref("privacy.resistFingerprinting", true);
user_pref("privacy.trackingprotection.enabled", true);
user_pref("media.peerconnection.enabled", false);
user_pref("webgl.disabled", true);
user_pref("geo.enabled", false);
user_pref("network.dns.disablePrefetch", true);
user_pref("network.prefetch-next", false);
user_pref("toolkit.telemetry.enabled", false);
user_pref("datareporting.healthreport.uploadEnabled", false);
user_pref("dom.security.https_only_mode", true);
"""
        user_js_path.write_text(config)
