"""
BBK Brands (Realme, Oppo, Vivo, OnePlus) profile for PhoneFix.
"""

from typing import List
from phone_fix.brands.base import BaseBrandProfile, BloatwareItem

class RealMeOppoVivoProfile(BaseBrandProfile):
    @property
    def brand_name(self) -> str:
        return "Realme / Oppo / Vivo / OnePlus"

    def get_bloatware_candidates(self) -> List[BloatwareItem]:
        return [
            BloatwareItem(
                package_name="com.heytap.mcs",
                label="HeyTap Push Service",
                description="ColorOS / RealmeUI push messaging service.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.coloros.gamespace",
                label="Game Space",
                description="Game optimizer with promotional notifications.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.vivo.appstore",
                label="V-Appstore",
                description="Vivo proprietary store; intrusive ads.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.vivo.magazine",
                label="Lockscreen Magazine",
                description="Lockscreen promotional wallpapers and ads.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.facebook.services",
                label="Facebook Background Service",
                description="Preloaded Facebook tracking service.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.facebook.appmanager",
                label="Facebook App Manager",
                description="Preloaded Facebook updater.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.facebook.system",
                label="Facebook System Service",
                description="Preloaded Facebook system process.",
                risk_level="SAFE"
            ),
        ]
