"""
Generic Android brand profile fallback for PhoneFix.
"""

from typing import List
from phone_fix.brands.base import BaseBrandProfile, BloatwareItem

class GenericProfile(BaseBrandProfile):
    @property
    def brand_name(self) -> str:
        return "Generic Android"

    def get_bloatware_candidates(self) -> List[BloatwareItem]:
        return [
            BloatwareItem(
                package_name="com.facebook.services",
                label="Facebook Background Service",
                description="Preloaded Facebook background tracking daemon.",
                risk_level="SAFE"
            ),
            BloatwareItem(
                package_name="com.facebook.appmanager",
                label="Facebook App Manager",
                description="Preloaded Facebook silent updater.",
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
