"""
Storage and junk analyzer for PhoneFix.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import re

from phone_fix.core.adb import AdbBridge

@dataclass
class AppStorageItem:
    package_name: str
    app_size_bytes: int
    data_size_bytes: int
    cache_size_bytes: int

    @property
    def cache_size_mb(self) -> float:
        return self.cache_size_bytes / (1024 * 1024)

    @property
    def data_size_mb(self) -> float:
        return self.data_size_bytes / (1024 * 1024)

@dataclass
class StorageReport:
    total_gb: float
    used_gb: float
    free_gb: float
    percent_used: int
    total_app_cache_bytes: int
    total_app_data_bytes: int
    top_cache_apps: List[AppStorageItem]
    top_data_apps: List[AppStorageItem]
    removable_tmp_apks: List[str]
    removable_tmp_bytes: int
    thumbnail_cache_bytes: int
    removable_test_dumps: List[str]

    @property
    def total_cleanable_mb(self) -> float:
        total_b = self.total_app_cache_bytes + self.removable_tmp_bytes + self.thumbnail_cache_bytes
        return total_b / (1024 * 1024)

class StorageAnalyzer:
    """Analyzes device storage, partition usage, app caches, and identifies safe cleanable junk."""

    def __init__(self, adb: AdbBridge):
        self.adb = adb

    def analyze(self) -> StorageReport:
        df_out = self.adb.shell("df -h /data")
        total_gb = 0.0
        used_gb = 0.0
        free_gb = 0.0
        pct_used = 0

        for line in df_out.splitlines():
            if "/data" in line:
                parts = line.split()
                if len(parts) >= 5:
                    def parse_size(s: str) -> float:
                        s = s.upper().replace("G", "").replace("M", "").replace("K", "").replace("B", "")
                        return float(s) if s.replace(".", "").isdigit() else 0.0

                    # Standard df: Filesystem Size Used Avail Use% Mounted
                    total_gb = parse_size(parts[1])
                    used_gb = parse_size(parts[2])
                    free_gb = parse_size(parts[3])
                    pct_str = parts[4].replace("%", "")
                    pct_used = int(pct_str) if pct_str.isdigit() else 0

        # Diskstats
        diskstats_raw = self.adb.shell("dumpsys diskstats")
        pkg_names = []
        app_sizes = []
        data_sizes = []
        cache_sizes = []

        for line in diskstats_raw.splitlines():
            line = line.strip()
            if line.startswith("Package Names:"):
                try:
                    pkg_names = json.loads(line[len("Package Names:"):].strip())
                except Exception:
                    pass
            elif line.startswith("App Sizes:"):
                try:
                    app_sizes = json.loads(line[len("App Sizes:"):].strip())
                except Exception:
                    pass
            elif line.startswith("App Data Sizes:"):
                try:
                    data_sizes = json.loads(line[len("App Data Sizes:"):].strip())
                except Exception:
                    pass
            elif line.startswith("Cache Sizes:"):
                try:
                    cache_sizes = json.loads(line[len("Cache Sizes:"):].strip())
                except Exception:
                    pass

        app_items = []
        for i in range(len(pkg_names)):
            pkg = pkg_names[i]
            a_sz = app_sizes[i] if i < len(app_sizes) else 0
            d_sz = data_sizes[i] if i < len(data_sizes) else 0
            c_sz = cache_sizes[i] if i < len(cache_sizes) else 0
            app_items.append(AppStorageItem(
                package_name=pkg,
                app_size_bytes=a_sz,
                data_size_bytes=d_sz,
                cache_size_bytes=c_sz,
            ))

        top_cache = sorted(app_items, key=lambda x: x.cache_size_bytes, reverse=True)[:20]
        top_data = sorted(app_items, key=lambda x: x.data_size_bytes, reverse=True)[:15]
        total_cache_b = sum(a.cache_size_bytes for a in app_items)
        total_data_b = sum(a.data_size_bytes for a in app_items)

        # Inspect /data/local/tmp APKs
        tmp_apks = []
        tmp_bytes = 0
        tmp_ls = self.adb.shell_safe("ls -l /data/local/tmp 2>/dev/null")
        for line in tmp_ls.splitlines():
            if ".apk" in line:
                parts = line.split()
                if len(parts) >= 9:
                    size_str = parts[4]
                    filename = parts[-1]
                    if size_str.isdigit():
                        tmp_bytes += int(size_str)
                    tmp_apks.append(f"/data/local/tmp/{filename}")

        # Thumbnail cache
        thumb_bytes = 0
        thumb_out = self.adb.shell_safe("du -sb /sdcard/Pictures/.thumbnails 2>/dev/null")
        if thumb_out:
            parts = thumb_out.split()
            if parts and parts[0].isdigit():
                thumb_bytes = int(parts[0])

        # Test dumps in /sdcard root
        test_dumps = []
        sdcard_ls = self.adb.shell_safe("ls -1 /sdcard/*.png /sdcard/*.xml 2>/dev/null")
        for f in sdcard_ls.splitlines():
            f = f.strip()
            if f and not f.startswith("ls:") and "No such file" not in f:
                test_dumps.append(f)

        return StorageReport(
            total_gb=total_gb,
            used_gb=used_gb,
            free_gb=free_gb,
            percent_used=pct_used,
            total_app_cache_bytes=total_cache_b,
            total_app_data_bytes=total_data_b,
            top_cache_apps=top_cache,
            top_data_apps=top_data,
            removable_tmp_apks=tmp_apks,
            removable_tmp_bytes=tmp_bytes,
            thumbnail_cache_bytes=thumb_bytes,
            removable_test_dumps=test_dumps
        )
