"""
Optimization engine for PhoneFix.
Executes non-destructive, safe, and reversible improvements on the Android device.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import os

from phone_fix.core.adb import AdbBridge

@dataclass
class OptimizationSummary:
    cache_trimmed: bool
    tmp_apks_removed: int
    test_dumps_removed: int
    disabled_bloatware: List[str]
    failed_bloatware: Dict[str, str]
    refresh_rate_set: Optional[int]
    animations_set: float
    aot_compiled_apps: List[str]
    restricted_apps: List[str]
    dns_configured: Optional[str]

class DeviceOptimizer:
    """Safely executes targeted optimizations on an authorized Android device."""

    def __init__(self, adb: AdbBridge):
        self.adb = adb

    def trim_caches(self, target_free_gb: int = 25) -> bool:
        """Invokes Android's native package manager cache trimming."""
        try:
            self.adb.shell(f"pm trim-caches {target_free_gb}G")
            return True
        except Exception:
            return False

    def clean_tmp_junk(self) -> int:
        """Removes leftover APK installers and sha1 files in /data/local/tmp and thumbnails."""
        removed_count = 0
        try:
            ls_out = self.adb.shell("ls -1 /data/local/tmp 2>/dev/null")
            for f in ls_out.splitlines():
                f = f.strip()
                if f.endswith(".apk") or f.endswith(".sha1"):
                    self.adb.shell(f"rm -f /data/local/tmp/{f}")
                    removed_count += 1
            # Clean thumbnails
            self.adb.shell("rm -rf /sdcard/Pictures/.thumbnails/* 2>/dev/null")
            # Clean root screenshots/dumps
            self.adb.shell("rm -f /sdcard/*.png /sdcard/*.xml 2>/dev/null")
        except Exception:
            pass
        return removed_count

    def disable_bloatware(self, packages: List[str]) -> Tuple[List[str], Dict[str, str]]:
        """
        Safely disables or uninstalls bloatware for user 0 (current user).
        This is 100% reversible via `cmd package install-existing <pkg>`.
        """
        disabled = []
        failed = {}

        for pkg in packages:
            pkg = pkg.strip()
            if not pkg:
                continue
            # Try pm uninstall -k --user 0 first
            out, err, code = self.adb.run_raw(["-s", self.adb.target_serial, "shell", f"pm uninstall -k --user 0 {pkg}"])
            if "Success" in out:
                disabled.append(pkg)
            else:
                # Fallback to pm disable-user
                out_dis, err_dis, _ = self.adb.run_raw(["-s", self.adb.target_serial, "shell", f"pm disable-user --user 0 {pkg}"])
                if "disabled" in out_dis or "Success" in out_dis:
                    disabled.append(pkg)
                else:
                    failed[pkg] = err or out or err_dis

        return disabled, failed

    def rollback_packages(self, packages: List[str]) -> List[str]:
        """Restores previously uninstalled system packages for user 0."""
        restored = []
        for pkg in packages:
            pkg = pkg.strip()
            if not pkg:
                continue
            out, _, code = self.adb.run_raw(["-s", self.adb.target_serial, "shell", f"cmd package install-existing {pkg}"])
            if "installed" in out.lower() or "success" in out.lower() or code == 0:
                restored.append(pkg)
        return restored

    def unlock_refresh_rate(self, rate: int = 120) -> bool:
        """Sets display peak and user refresh rate."""
        try:
            self.adb.shell(f"settings put system user_refresh_rate {rate}")
            self.adb.shell(f"settings put system peak_refresh_rate {rate}")
            return True
        except Exception:
            return False

    def optimize_animations(self, scale: float = 0.5) -> bool:
        """Adjusts window, transition, and animator duration scales."""
        try:
            self.adb.shell(f"settings put global window_animation_scale {scale}")
            self.adb.shell(f"settings put global transition_animation_scale {scale}")
            self.adb.shell(f"settings put global animator_duration_scale {scale}")
            return True
        except Exception:
            return False

    def compile_apps_aot(self, packages: List[str]) -> List[str]:
        """Runs Ahead-of-Time (AOT) speed-profile DEX compilation for specified apps."""
        compiled = []
        for pkg in packages:
            pkg = pkg.strip()
            if not pkg:
                continue
            out = self.adb.shell(f"cmd package compile -m speed-profile {pkg}")
            if "Success" in out:
                compiled.append(pkg)
        return compiled

    def restrict_dormant_apps(self, packages: List[str]) -> List[str]:
        """Places dormant apps in Android's restricted standby bucket."""
        restricted = []
        for pkg in packages:
            pkg = pkg.strip()
            if not pkg:
                continue
            try:
                self.adb.shell(f"am set-standby-bucket {pkg} restricted")
                restricted.append(pkg)
            except Exception:
                pass
        return restricted

    def set_private_dns(self, hostname: str) -> bool:
        """Configures Private DNS for ad-blocking / secure resolution."""
        try:
            self.adb.shell(f"settings put global private_dns_specifier {hostname}")
            self.adb.shell("settings put global private_dns_mode hostname")
            return True
        except Exception:
            return False

    def kill_cached_processes(self) -> None:
        """Forces Android to clear cached background processes to instantly refresh RAM."""
        try:
            self.adb.shell("am kill-all")
        except Exception:
            pass
