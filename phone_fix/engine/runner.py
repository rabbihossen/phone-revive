"""
Orchestrator runner that executes all analyzers and produces a unified HealthReport.
"""

from dataclasses import dataclass
from typing import List

from phone_fix.core.adb import AdbBridge
from phone_fix.core.device import DeviceInfo, DeviceInspector
from phone_fix.analyzers.storage import StorageAnalyzer, StorageReport
from phone_fix.analyzers.memory import MemoryAnalyzer, MemoryReport
from phone_fix.analyzers.apps import AppAnalyzer, AppUsageReport
from phone_fix.analyzers.display import DisplayAnalyzer, DisplayReport
from phone_fix.analyzers.network import NetworkAnalyzer, NetworkReport
from phone_fix.brands import get_brand_profile
from phone_fix.brands.base import BloatwareItem

@dataclass
class HealthReport:
    device: DeviceInfo
    storage: StorageReport
    memory: MemoryReport
    apps: AppUsageReport
    display: DisplayReport
    network: NetworkReport
    detected_bloatware: List[BloatwareItem]
    health_score: int
    health_grade: str
    action_items: List[str]

class DiagnosticRunner:
    """Executes all non-destructive diagnostics and evaluates device health."""

    def __init__(self, adb: AdbBridge):
        self.adb = adb

    def run(self) -> HealthReport:
        device_inspector = DeviceInspector(self.adb)
        device_info = device_inspector.inspect()

        storage_analyzer = StorageAnalyzer(self.adb)
        storage_report = storage_analyzer.analyze()

        memory_analyzer = MemoryAnalyzer(self.adb)
        memory_report = memory_analyzer.analyze()

        app_analyzer = AppAnalyzer(self.adb)
        app_report = app_analyzer.analyze()

        display_analyzer = DisplayAnalyzer(self.adb)
        display_report = display_analyzer.analyze()

        network_analyzer = NetworkAnalyzer(self.adb)
        network_report = network_analyzer.analyze()

        # Brand bloatware detection
        brand_profile = get_brand_profile(device_info.brand, device_info.manufacturer)
        user_pkgs = set(self.adb.shell_safe("pm list packages").replace("package:", "").splitlines())
        all_pkgs = set(self.adb.shell_safe("pm list packages -u").replace("package:", "").splitlines())
        disabled_pkgs = set(self.adb.shell_safe("pm list packages -d").replace("package:", "").splitlines())

        detected_bloat = []
        for item in brand_profile.get_bloatware_candidates():
            if item.package_name in all_pkgs:
                item.is_installed = True
                # If package is disabled or uninstalled for current user, it is considered disabled/inactive
                item.is_disabled = (item.package_name in disabled_pkgs) or (item.package_name not in user_pkgs)
                detected_bloat.append(item)

        # Health score calculation (100 base)
        score = 100
        actions = []

        # Storage penalty
        if storage_report.percent_used >= 85:
            score -= 25
            actions.append(f"Storage is critically full ({storage_report.percent_used}%). Clean cache & junk immediately.")
        elif storage_report.percent_used >= 70:
            score -= 10
            actions.append(f"Storage is {storage_report.percent_used}% full. Reclaim ~{storage_report.total_cleanable_mb:.0f} MB junk.")

        # Memory pressure penalty
        if memory_report.pressure_level == "CRITICAL":
            score -= 20
            actions.append("RAM is under critical pressure. Disable background bloatware and kill cached processes.")
        elif memory_report.pressure_level == "MODERATE":
            score -= 10
            actions.append("RAM usage is moderately high. Background daemons are causing swap pressure.")

        # Bloatware penalty
        active_bloat = [b for b in detected_bloat if not b.is_disabled]
        if active_bloat:
            score -= min(20, len(active_bloat) * 4)
            actions.append(f"Found {len(active_bloat)} active telemetry/ad services running in background.")

        # Display penalty
        if display_report.can_unlock_high_refresh:
            score -= 5
            actions.append(f"Display is locked at {display_report.peak_refresh_rate or 60}Hz. Unlock 120Hz smooth display.")

        if display_report.window_animation_scale > 0.5:
            score -= 5
            actions.append("UI animation scale is 1.0x. Set to 0.5x for 2x faster touch response.")

        # Grade
        score = max(10, min(100, score))
        if score >= 90:
            grade = "A (Excellent)"
        elif score >= 80:
            grade = "B (Good)"
        elif score >= 65:
            grade = "C (Needs Optimization)"
        elif score >= 50:
            grade = "D (Sluggish)"
        else:
            grade = "F (Critical Bottlenecks)"

        return HealthReport(
            device=device_info,
            storage=storage_report,
            memory=memory_report,
            apps=app_report,
            display=display_report,
            network=network_report,
            detected_bloatware=detected_bloat,
            health_score=score,
            health_grade=grade,
            action_items=actions
        )
