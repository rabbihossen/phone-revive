"""
Tests for all analyzers (storage, memory, apps, display, network).
"""

from unittest.mock import MagicMock
from phone_fix.analyzers.storage import StorageAnalyzer
from phone_fix.analyzers.memory import MemoryAnalyzer
from phone_fix.analyzers.apps import AppAnalyzer
from phone_fix.analyzers.display import DisplayAnalyzer
from phone_fix.analyzers.network import NetworkAnalyzer
from tests.conftest import (
    MOCK_DF_OUTPUT,
    MOCK_MEMINFO_OUTPUT,
    MOCK_DISKSTATS_OUTPUT
)

def test_storage_analyzer(mock_adb):
    mock_adb.shell.side_effect = lambda cmd: MOCK_DF_OUTPUT if "df" in cmd else (MOCK_DISKSTATS_OUTPUT if "diskstats" in cmd else "")
    mock_adb.shell_safe.return_value = ""

    analyzer = StorageAnalyzer(mock_adb)
    report = analyzer.analyze()

    assert report.total_gb == 48.0
    assert report.used_gb == 33.0
    assert report.free_gb == 15.0
    assert report.percent_used == 69
    assert len(report.top_cache_apps) == 2
    assert report.total_app_cache_bytes == 250000000

def test_memory_analyzer(mock_adb):
    mock_adb.shell.side_effect = lambda cmd: MOCK_MEMINFO_OUTPUT if "cat /proc/meminfo" in cmd else ""
    analyzer = MemoryAnalyzer(mock_adb)
    report = analyzer.analyze()

    assert report.total_ram_mb == 5639.2
    assert report.available_ram_mb == 2774.2
    assert report.pressure_level in ["HEALTHY", "MODERATE"]

def test_display_analyzer(mock_adb):
    def fake_shell_safe(cmd, default=""):
        if "peak_refresh_rate" in cmd:
            return "60"
        elif "window_animation_scale" in cmd:
            return "1.0"
        return "1.0"

    mock_adb.shell_safe.side_effect = fake_shell_safe
    analyzer = DisplayAnalyzer(mock_adb)
    report = analyzer.analyze()

    assert report.peak_refresh_rate == 60.0
    assert report.window_animation_scale == 1.0
    assert report.can_unlock_high_refresh is True

def test_network_analyzer(mock_adb):
    def fake_shell_safe(cmd, default=""):
        if "private_dns_mode" in cmd:
            return "hostname"
        elif "private_dns_specifier" in cmd:
            return "high.kahfguard.com"
        elif "wlan0" in cmd:
            return "inet 192.168.0.100/24 brd 192.168.0.255"
        elif "ping" in cmd:
            return "rtt min/avg/max/mdev = 3.2/4.5/6.0/1.0 ms"
        return ""

    mock_adb.shell_safe.side_effect = fake_shell_safe
    analyzer = NetworkAnalyzer(mock_adb)
    report = analyzer.analyze()

    assert report.private_dns_mode == "hostname"
    assert report.private_dns_specifier == "high.kahfguard.com"
    assert report.wifi_ip == "192.168.0.100"
    assert report.dns_latency_ms == 4.5
