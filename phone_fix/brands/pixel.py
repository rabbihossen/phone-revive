"""
Google Pixel profile for PhoneFix.
"""

from typing import List
from phone_fix.brands.base import BaseBrandProfile, BloatwareItem

class PixelProfile(BaseBrandProfile):
    @property
    def brand_name(self) -> str:
        return "Google Pixel"

    def get_bloatware_candidates(self) -> List[BloatwareItem]:
        return [
            BloatwareItem(
                package_name="com.google.android.videos",
                label="Google TV",
                description="Preinstalled movie store.",
                risk_level="USER_DECISION"
            ),
            BloatwareItem(
                package_name="com.google.android.apps.youtube.music",
                label="YouTube Music",
                description="Preinstalled music streaming.",
                risk_level="USER_DECISION"
            ),
        ]
