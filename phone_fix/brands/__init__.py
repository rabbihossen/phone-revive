"""
Brand profiles registry for PhoneFix.
Auto-detects device brand and returns appropriate profile.
"""

from typing import Dict, Type
from phone_fix.brands.base import BaseBrandProfile, BloatwareItem
from phone_fix.brands.xiaomi import XiaomiProfile
from phone_fix.brands.samsung import SamsungProfile
from phone_fix.brands.realme_oppo_vivo import RealMeOppoVivoProfile
from phone_fix.brands.pixel import PixelProfile
from phone_fix.brands.generic import GenericProfile

def get_brand_profile(brand: str, manufacturer: str) -> BaseBrandProfile:
    b = (brand or "").lower()
    m = (manufacturer or "").lower()

    if any(k in b or k in m for k in ["xiaomi", "redmi", "poco"]):
        return XiaomiProfile()
    elif any(k in b or k in m for k in ["samsung"]):
        return SamsungProfile()
    elif any(k in b or k in m for k in ["realme", "oppo", "vivo", "oneplus"]):
        return RealMeOppoVivoProfile()
    elif any(k in b or k in m for k in ["google", "pixel"]):
        return PixelProfile()
    else:
        return GenericProfile()
