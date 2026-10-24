"""
Network, DNS, and privacy analyzer for PhoneFix.
"""

from dataclasses import dataclass
from typing import Optional

from phone_fix.core.adb import AdbBridge

@dataclass
class NetworkReport:
    private_dns_mode: str
    private_dns_specifier: Optional[str]
    wifi_ip: Optional[str]
    dns_latency_ms: Optional[float]

class NetworkAnalyzer:
    """Analyzes device network settings, private DNS mode, and latency."""

    def __init__(self, adb: AdbBridge):
        self.adb = adb

    def analyze(self) -> NetworkReport:
        dns_mode = self.adb.shell_safe("settings get global private_dns_mode").strip()
        dns_spec = self.adb.shell_safe("settings get global private_dns_specifier").strip()
        if dns_spec == "null":
            dns_spec = None

        # Wi-Fi IP
        ip_out = self.adb.shell_safe("ip -f inet addr show wlan0")
        wifi_ip = None
        for line in ip_out.splitlines():
            line = line.strip()
            if line.startswith("inet "):
                parts = line.split()
                if len(parts) >= 2:
                    wifi_ip = parts[1].split("/")[0]

        # Latency check
        latency = None
        target_host = dns_spec or "1.1.1.1"
        try:
            ping_out = self.adb.shell_safe(f"ping -c 2 {target_host}")
            for line in ping_out.splitlines():
                if "rtt min/avg/max" in line or "round-trip min/avg/max" in line:
                    val = line.split("=")[1].strip().split("/")[1]
                    latency = float(val)
        except Exception:
            pass

        return NetworkReport(
            private_dns_mode=dns_mode,
            private_dns_specifier=dns_spec,
            wifi_ip=wifi_ip,
            dns_latency_ms=latency
        )
