"""
App usage stats and dormancy analyzer for PhoneFix.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import re

from phone_fix.core.adb import AdbBridge

@dataclass
class AppUsageItem:
    package_name: str
    last_used_str: Optional[str]
    days_since_used: Optional[int]
    category: str  # 'active', 'inactive', 'dormant', 'never'

@dataclass
class AppUsageReport:
    total_installed: int
    third_party_count: int
    disabled_count: int
    active_apps: List[AppUsageItem]       # < 7 days
    inactive_apps: List[AppUsageItem]     # 7 - 30 days
    dormant_apps: List[AppUsageItem]      # > 30 days
    never_used_apps: List[AppUsageItem]   # never opened / no record

class AppAnalyzer:
    """Analyzes app installation and usage statistics to identify unused and dormant apps."""

    def __init__(self, adb: AdbBridge):
        self.adb = adb

    def analyze(self) -> AppUsageReport:
        # Get packages
        pkgs_raw = self.adb.shell("pm list packages -3").splitlines()
        third_party = [p.replace("package:", "").strip() for p in pkgs_raw if p.strip()]

        all_pkgs = [p.replace("package:", "").strip() for p in self.adb.shell("pm list packages -u").splitlines() if p.strip()]
        disabled_pkgs = [p.replace("package:", "").strip() for p in self.adb.shell("pm list packages -d").splitlines() if p.strip()]

        # Usage stats
        usage_raw = self.adb.shell("dumpsys usagestats")
        pkg_last_used: Dict[str, str] = {}
        current_pkg = None

        for line in usage_raw.splitlines():
            line = line.strip()
            m_pkg = re.search(r"package=([a-zA-Z0-9_\.]+)", line)
            if m_pkg:
                current_pkg = m_pkg.group(1)

            m_time = re.search(r"lastTimeUsed=\"([^\"]+)\"", line) or re.search(r"lastTime=\"([^\"]+)\"", line)
            if m_time and current_pkg:
                pkg_last_used[current_pkg] = m_time.group(1)

        # Categorize
        now = datetime.now()
        active = []
        inactive = []
        dormant = []
        never = []

        for pkg in sorted(third_party):
            last_str = pkg_last_used.get(pkg)
            if not last_str or last_str.startswith("1970"):
                never.append(AppUsageItem(
                    package_name=pkg,
                    last_used_str=None,
                    days_since_used=None,
                    category="never"
                ))
                continue

            try:
                dt = datetime.strptime(last_str[:19], "%Y-%m-%d %H:%M:%S")
                days_ago = max(0, (now - dt).days)
                if days_ago <= 7:
                    active.append(AppUsageItem(pkg, last_str, days_ago, "active"))
                elif days_ago <= 30:
                    inactive.append(AppUsageItem(pkg, last_str, days_ago, "inactive"))
                else:
                    dormant.append(AppUsageItem(pkg, last_str, days_ago, "dormant"))
            except Exception:
                never.append(AppUsageItem(pkg, last_str, None, "never"))

        active.sort(key=lambda x: x.days_since_used or 0)
        inactive.sort(key=lambda x: x.days_since_used or 0)
        dormant.sort(key=lambda x: x.days_since_used or 0, reverse=True)

        return AppUsageReport(
            total_installed=len(all_pkgs),
            third_party_count=len(third_party),
            disabled_count=len(disabled_pkgs),
            active_apps=active,
            inactive_apps=inactive,
            dormant_apps=dormant,
            never_used_apps=never
        )
