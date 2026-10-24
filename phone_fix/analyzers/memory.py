"""
Memory and RAM analyzer for PhoneFix.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import re

from phone_fix.core.adb import AdbBridge

@dataclass
class ProcessMemoryItem:
    process_name: str
    pid: int
    rss_kb: int

    @property
    def rss_mb(self) -> float:
        return self.rss_kb / 1024.0

@dataclass
class MemoryReport:
    total_ram_mb: float
    free_ram_mb: float
    available_ram_mb: float
    swap_total_mb: float
    swap_free_mb: float
    swap_used_mb: float
    pressure_level: str
    top_processes: List[ProcessMemoryItem]

class MemoryAnalyzer:
    """Analyzes system RAM, swap/ZRAM pressure, and top memory-consuming processes."""

    def __init__(self, adb: AdbBridge):
        self.adb = adb

    def analyze(self) -> MemoryReport:
        meminfo = self.adb.shell("cat /proc/meminfo")
        data = {}
        for line in meminfo.splitlines():
            line = line.strip()
            if ":" in line:
                k, v = line.split(":", 1)
                num = "".join(filter(str.isdigit, v))
                if num:
                    data[k] = int(num)

        total_kb = data.get("MemTotal", 0)
        free_kb = data.get("MemFree", 0)
        avail_kb = data.get("MemAvailable", free_kb)
        swap_total_kb = data.get("SwapTotal", 0)
        swap_free_kb = data.get("SwapFree", 0)
        swap_used_kb = swap_total_kb - swap_free_kb

        # Pressure assessment
        if total_kb > 0:
            free_ratio = avail_kb / total_kb
            if free_ratio < 0.15:
                pressure = "CRITICAL"
            elif free_ratio < 0.30:
                pressure = "MODERATE"
            else:
                pressure = "HEALTHY"
        else:
            pressure = "UNKNOWN"

        # Top processes from dumpsys meminfo
        top_procs = []
        try:
            memdump = self.adb.shell("dumpsys meminfo | head -n 45")
            # Parse '458,364K: system (pid 2429)'
            for line in memdump.splitlines():
                line = line.strip()
                m = re.search(r"([0-9,]+)K:\s+([a-zA-Z0-9_\.:]+)\s+\(pid\s+([0-9]+)", line)
                if m:
                    rss_str = m.group(1).replace(",", "")
                    p_name = m.group(2)
                    pid_str = m.group(3)
                    top_procs.append(ProcessMemoryItem(
                        process_name=p_name,
                        pid=int(pid_str),
                        rss_kb=int(rss_str)
                    ))
        except Exception:
            pass

        return MemoryReport(
            total_ram_mb=round(total_kb / 1024.0, 1),
            free_ram_mb=round(free_kb / 1024.0, 1),
            available_ram_mb=round(avail_kb / 1024.0, 1),
            swap_total_mb=round(swap_total_kb / 1024.0, 1),
            swap_free_mb=round(swap_free_kb / 1024.0, 1),
            swap_used_mb=round(swap_used_kb / 1024.0, 1),
            pressure_level=pressure,
            top_processes=top_procs
        )
