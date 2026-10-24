"""
ADB wrapper for PhoneFix.
Manages ADB discovery, device enumeration, wireless connections, and command execution.
"""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Optional, Tuple

from phone_fix.core.exceptions import (
    AdbNotFoundError,
    CommandExecutionError,
    DeviceNotFoundError,
    DeviceUnauthorizedError,
    MultipleDevicesError,
)

@dataclass
class ConnectedDevice:
    serial: str
    state: str
    product: Optional[str] = None
    model: Optional[str] = None
    device: Optional[str] = None
    transport_id: Optional[str] = None

    @property
    def is_authorized(self) -> bool:
        return self.state == "device"

class AdbBridge:
    """Provides high-level interface to the Android Debug Bridge (ADB)."""

    COMMON_ADB_PATHS = [
        os.path.expanduser("~/Library/Android/sdk/platform-tools/adb"),
        os.path.expanduser("~/Android/Sdk/platform-tools/adb"),
        "/opt/android-sdk/platform-tools/adb",
        "/usr/local/bin/adb",
        "/usr/bin/adb",
    ]

    def __init__(self, adb_path: Optional[str] = None, target_serial: Optional[str] = None):
        self.adb_path = adb_path or self._discover_adb()
        self.target_serial = target_serial

    def _discover_adb(self) -> str:
        """Find ADB binary in PATH or common SDK paths."""
        found = shutil.which("adb")
        if found:
            return found

        for candidate in self.COMMON_ADB_PATHS:
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate

        raise AdbNotFoundError(
            "Android Debug Bridge (ADB) not found. "
            "Please install Android Platform Tools or add 'adb' to your system PATH."
        )

    def run_raw(self, args: List[str], timeout: int = 45) -> Tuple[str, str, int]:
        """Execute a raw ADB command with arguments."""
        cmd = [self.adb_path] + args
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return res.stdout.strip(), res.stderr.strip(), res.returncode
        except subprocess.TimeoutExpired:
            raise CommandExecutionError(" ".join(cmd), -1, f"Timed out after {timeout} seconds")
        except Exception as e:
            raise CommandExecutionError(" ".join(cmd), -1, str(e))

    def run(self, args: List[str], timeout: int = 45) -> str:
        """Execute ADB command targeted to the configured device."""
        target_args = []
        if self.target_serial:
            target_args = ["-s", self.target_serial]
        
        stdout, stderr, code = self.run_raw(target_args + args, timeout=timeout)
        if code != 0:
            raise CommandExecutionError(f"adb {' '.join(args)}", code, stderr or stdout)
        return stdout

    def shell(self, shell_cmd: str, timeout: int = 45) -> str:
        """Run an adb shell command."""
        return self.run(["shell", shell_cmd], timeout=timeout)

    def shell_safe(self, shell_cmd: str, default: str = "", timeout: int = 45) -> str:
        """Run an adb shell command and return output even if exit code is non-zero."""
        target_args = []
        if self.target_serial:
            target_args = ["-s", self.target_serial]
        stdout, stderr, _ = self.run_raw(target_args + ["shell", shell_cmd], timeout=timeout)
        return stdout or default

    def list_devices(self) -> List[ConnectedDevice]:
        """List all currently attached ADB devices with metadata."""
        stdout, _, _ = self.run_raw(["devices", "-l"])
        devices = []
        lines = stdout.splitlines()

        for line in lines[1:]:  # skip 'List of devices attached'
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 2:
                serial = parts[0]
                state = parts[1]
                meta = {}
                for item in parts[2:]:
                    if ":" in item:
                        k, v = item.split(":", 1)
                        meta[k] = v
                devices.append(ConnectedDevice(
                    serial=serial,
                    state=state,
                    product=meta.get("product"),
                    model=meta.get("model"),
                    device=meta.get("device"),
                    transport_id=meta.get("transport_id"),
                ))
        return devices

    def select_device(self, preferred_serial: Optional[str] = None) -> ConnectedDevice:
        """
        Auto-select or validate target device.
        Raises DeviceNotFoundError if none, or DeviceUnauthorizedError if not authorized.
        """
        devices = self.list_devices()
        if not devices:
            raise DeviceNotFoundError(
                "No Android device detected. "
                "Ensure your phone is connected via USB or Wi-Fi, and Developer Options is ON."
            )

        if preferred_serial:
            matched = [d for d in devices if d.serial == preferred_serial]
            if not matched:
                raise DeviceNotFoundError(f"Device with serial '{preferred_serial}' not found.")
            selected = matched[0]
        elif len(devices) == 1:
            selected = devices[0]
        else:
            # If multiple devices, pick the authorized one or first
            authorized = [d for d in devices if d.is_authorized]
            if len(authorized) == 1:
                selected = authorized[0]
            elif len(authorized) > 1:
                # Default to the first authorized device
                selected = authorized[0]
            else:
                selected = devices[0]

        if not selected.is_authorized:
            raise DeviceUnauthorizedError(
                f"Device '{selected.serial}' is unauthorized. "
                "Please check your phone screen and tap 'Allow USB debugging'."
            )

        self.target_serial = selected.serial
        return selected

    def enable_tcpip(self, port: int = 5555) -> str:
        """Restart adbd in TCP/IP mode for wireless connection."""
        return self.run(["tcpip", str(port)])

    def connect_wifi(self, ip_port: str) -> str:
        """Connect to device over Wi-Fi (e.g. 192.168.0.100:5555)."""
        stdout, stderr, _ = self.run_raw(["connect", ip_port])
        return stdout or stderr

    def pair_wifi(self, ip_port: str, pairing_code: str) -> str:
        """Pair device with pairing code over Android 11+ wireless debugging."""
        stdout, stderr, _ = self.run_raw(["pair", ip_port, pairing_code])
        return stdout or stderr
