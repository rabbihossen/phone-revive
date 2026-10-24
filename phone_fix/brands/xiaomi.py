"""
Xiaomi / Redmi / POCO (MIUI & HyperOS) profile for PhoneFix.
"""

from typing import List
from phone_fix.brands.base import BaseBrandProfile, BloatwareItem

class XiaomiProfile(BaseBrandProfile):
    @property
    def brand_name(self) -> str:
        return "Xiaomi / Redmi / POCO"

    def get_bloatware_candidates(self) -> List[BloatwareItem]:
        return [
            BloatwareItem(
                package_name="com.miui.msa.global",
                label="MIUI System Ads (MSA)",
                description="Core background advertising daemon across MIUI/HyperOS apps.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.miui.analytics",
                label="MIUI Analytics",
                description="Aggressive telemetry and analytics logger sending usage data to Xiaomi.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.miui.daemon",
                label="Xiaomi Background Daemon",
                description="Background telemetry service running continuously in RAM.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.xiaomi.mipicks",
                label="GetApps App Store",
                description="Xiaomi's proprietary app store; causes push spam and background downloads.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.xiaomi.glgm",
                label="Xiaomi Games Center",
                description="Unnecessary gaming bloatware and ad promotions.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.miui.yellowpage",
                label="MIUI YellowPage",
                description="Caller directory lookup service primarily targeted outside global regions.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.xiaomi.payment",
                label="Mi Pay Service",
                description="Payment daemon; unused if not actively using Mi Pay.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.miui.bugreport",
                label="MIUI Bug Reporter",
                description="Continuous crash log collector running in background.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.miui.android.fashiongallery",
                label="Glance Wallpaper Carousel",
                description="Lockscreen promotional news and wallpaper downloader; drains data and battery.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.facebook.services",
                label="Facebook Background Service",
                description="Preloaded Facebook background tracking daemon.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.facebook.appmanager",
                label="Facebook App Manager",
                description="Preloaded Facebook silent installer/updater.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.facebook.system",
                label="Facebook System Service",
                description="Preloaded Facebook system service running persistently in RAM.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.google.android.videos",
                label="Google TV",
                description="Preinstalled movie store; rarely used if streaming on other apps.",
                risk_level="USER_DECISION"
            ),
            BloatwareItem(
                package_name="com.google.android.apps.youtube.music",
                label="YouTube Music",
                description="Preinstalled music streaming app.",
                risk_level="USER_DECISION"
            ),
            BloatwareItem(
                package_name="com.google.android.apps.tachyon",
                label="Google Meet",
                description="Preinstalled video calling service.",
                risk_level="USER_DECISION"
            ),
            BloatwareItem(
                package_name="com.miui.player",
                label="Mi Music",
                description="Xiaomi stock music player with streaming ads.",
                risk_level="USER_DECISION"
            ),
        ]
