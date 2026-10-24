"""
Device model and hardware metadata extractor for PhoneFix.
"""

from dataclasses import dataclass
from typing import Dict, Optional
import re

from phone_fix.core.adb import AdbBridge

@dataclass
class BatteryInfo:
    level: int
    scale: int
    health: str
    temperature_celsius: float
    is_charging: bool
    voltage_mv: int
    technology: str

@dataclass
class DeviceInfo:
    serial: str
    brand: str
    manufacturer: str
    model: str
    market_name: str
    device_codename: str
    android_version: str
    sdk_version: int
    security_patch: str
    build_id: str
    cpu_abi: str
    uptime: str
    battery: BatteryInfo

    @property
    def display_name(self) -> str:
        name = self.market_name or self.model
        if self.brand and self.brand.lower() not in name.lower():
            return f"{self.brand.capitalize()} {name}"
        return name

class DeviceInspector:
    """Inspects an Android device via ADB to extract comprehensive hardware and OS information."""

    def __init__(self, adb: AdbBridge):
        self.adb = adb

    def get_property(self, prop_name: str) -> str:
        try:
            return self.adb.shell(f"getprop {prop_name}").strip()
        except Exception:
            return ""

    def get_battery_info(self) -> BatteryInfo:
        out = self.adb.shell("dumpsys battery")
        level = 0
        scale = 100
        health_code = "2"
        temp = 0.0
        is_charging = False
        voltage = 0
        tech = "Li-ion"

        for line in out.splitlines():
            line = line.strip()
            if line.startswith("level:"):
                level = int(line.split(":")[1].strip())
            elif line.startswith("scale:"):
                scale = int(line.split(":")[1].strip())
            elif line.startswith("health:"):
                health_code = line.split(":")[1].strip()
            elif line.startswith("temperature:"):
                raw_temp = float(line.split(":")[1].strip())
                temp = raw_temp / 10.0 if raw_temp > 100 else raw_temp
            elif line.startswith("status:"):
                # 2 is charging
                status_code = line.split(":")[1].strip()
                is_charging = (status_code == "2")
            elif line.startswith("voltage:"):
                voltage = int(line.split(":")[1].strip())
            elif line.startswith("technology:"):
                tech = line.split(":")[1].strip()

        health_map = {
            "1": "Unknown",
            "2": "Good",
            "3": "Overheat",
            "4": "Dead",
            "5": "Over voltage",
            "6": "Unspecified failure",
            "7": "Cold"
        }
        health_str = health_map.get(health_code, f"Status ({health_code})")

        return BatteryInfo(
            level=level,
            scale=scale,
            health=health_str,
            temperature_celsius=temp,
            is_charging=is_charging,
            voltage_mv=voltage,
            technology=tech
        )

    def inspect(self) -> DeviceInfo:
        brand = self.get_property("ro.product.brand") or self.get_property("ro.product.manufacturer")
        manufacturer = self.get_property("ro.product.manufacturer")
        model = self.get_property("ro.product.model")
        market_name = (
            self.get_property("ro.product.marketname") or
            self.get_property("ro.product.odm.marketname") or
            model
        )
        device_codename = self.get_property("ro.product.device")
        android_ver = self.get_property("ro.build.version.release") or "Unknown"
        sdk_str = self.get_property("ro.build.version.sdk") or "0"
        sdk_version = int(sdk_str) if sdk_str.isdigit() else 0
        security_patch = self.get_property("ro.build.version.security_patch") or "Unknown"
        build_id = self.get_property("ro.build.display.id") or self.get_property("ro.build.id")
        cpu_abi = self.get_property("ro.product.cpu.abi") or "arm64-v8a"
        uptime = self.adb.shell("uptime")
        battery = self.get_battery_info()

        return DeviceInfo(
            serial=self.adb.target_serial or "unknown",
            brand=brand.capitalize() if brand else "Generic",
            manufacturer=manufacturer.capitalize() if manufacturer else "Generic",
            model=model,
            market_name=market_name,
            device_codename=device_codename,
            android_version=android_ver,
            sdk_version=sdk_version,
            security_patch=security_patch,
            build_id=build_id,
            cpu_abi=cpu_abi,
            uptime=uptime,
            battery=battery
        )
