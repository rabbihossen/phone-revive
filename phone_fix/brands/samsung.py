"""
Samsung (OneUI) profile for PhoneFix.
"""

from typing import List
from phone_fix.brands.base import BaseBrandProfile, BloatwareItem

class SamsungProfile(BaseBrandProfile):
    @property
    def brand_name(self) -> str:
        return "Samsung Galaxy"

    def get_bloatware_candidates(self) -> List[BloatwareItem]:
        return [
            BloatwareItem(
                package_name="com.samsung.android.bixby.agent",
                label="Bixby Voice Agent",
                description="Samsung voice assistant background daemon.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.samsung.android.bixby.service",
                label="Bixby Service",
                description="Bixby system listener.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.samsung.android.app.spage",
                label="Samsung Free / Daily",
                description="Feed page on left of home screen; delivers sponsored content.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.samsung.android.game.gametools",
                label="Game Optimizing Service / Tools",
                description="Known to throttle CPU/GPU performance on Galaxy devices.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.samsung.android.game.gamehome",
                label="Samsung Game Launcher",
                description="Game center with ads and sponsored recommendations.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.sec.android.app.samsungapps",
                label="Galaxy Store",
                description="Samsung's secondary app store; frequent push notifications.",
                risk_level="USER_DECISION"
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
                description="Preloaded Facebook background process.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.google.android.videos",
                label="Google TV",
                description="Preinstalled movie store.",
                risk_level="USER_DECISION"
            ),
        ]
