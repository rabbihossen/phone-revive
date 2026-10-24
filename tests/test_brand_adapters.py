"""
Tests for Brand Profiles and auto-detection.
"""

from phone_fix.brands import get_brand_profile
from phone_fix.brands.xiaomi import XiaomiProfile
from phone_fix.brands.samsung import SamsungProfile
from phone_fix.brands.realme_oppo_vivo import RealMeOppoVivoProfile
from phone_fix.brands.pixel import PixelProfile
from phone_fix.brands.generic import GenericProfile

def test_brand_detection_xiaomi():
    p1 = get_brand_profile("Redmi", "Xiaomi")
    assert isinstance(p1, XiaomiProfile)

    p2 = get_brand_profile("POCO", "Xiaomi")
    assert isinstance(p2, XiaomiProfile)

    candidates = [c.package_name for c in p1.get_bloatware_candidates()]
    assert "com.miui.msa.global" in candidates
    assert "com.miui.analytics" in candidates

def test_brand_detection_samsung():
    p = get_brand_profile("samsung", "samsung")
    assert isinstance(p, SamsungProfile)
    candidates = [c.package_name for c in p.get_bloatware_candidates()]
    assert "com.samsung.android.bixby.agent" in candidates

def test_brand_detection_bbk():
    p1 = get_brand_profile("realme", "realme")
    assert isinstance(p1, RealMeOppoVivoProfile)

    p2 = get_brand_profile("OnePlus", "OnePlus")
    assert isinstance(p2, RealMeOppoVivoProfile)

def test_brand_detection_pixel():
    p = get_brand_profile("Google", "Google")
    assert isinstance(p, PixelProfile)

def test_brand_detection_generic():
    p = get_brand_profile("Motorola", "Motorola")
    assert isinstance(p, GenericProfile)
