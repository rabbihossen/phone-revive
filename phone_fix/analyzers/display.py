"""
Display and animation analyzer for PhoneFix.
"""

from dataclasses import dataclass
from typing import Optional

from phone_fix.core.adb import AdbBridge

@dataclass
class DisplayReport:
    peak_refresh_rate: Optional[float]
    user_refresh_rate: Optional[float]
    min_refresh_rate: Optional[float]
    window_animation_scale: float
    transition_animation_scale: float
    animator_duration_scale: float
    can_unlock_high_refresh: bool

class DisplayAnalyzer:
    """Analyzes refresh rate settings and UI animation scales."""

    def __init__(self, adb: AdbBridge):
        self.adb = adb

    def analyze(self) -> DisplayReport:
        def get_float_setting(namespace: str, key: str) -> Optional[float]:
            val = self.adb.shell_safe(f"settings get {namespace} {key}").strip()
            if val and val != "null" and val.replace(".", "").isdigit():
                return float(val)
            return None

        peak = get_float_setting("system", "peak_refresh_rate")
        user = get_float_setting("system", "user_refresh_rate")
        min_rate = get_float_setting("system", "min_refresh_rate")

        anim_w = get_float_setting("global", "window_animation_scale") or 1.0
        anim_t = get_float_setting("global", "transition_animation_scale") or 1.0
        anim_a = get_float_setting("global", "animator_duration_scale") or 1.0

        can_unlock = (peak is not None and peak < 120.0) or (user is not None and user < 120.0)

        return DisplayReport(
            peak_refresh_rate=peak,
            user_refresh_rate=user,
            min_refresh_rate=min_rate,
            window_animation_scale=anim_w,
            transition_animation_scale=anim_t,
            animator_duration_scale=anim_a,
            can_unlock_high_refresh=can_unlock
        )
