"""
Base brand profile and bloatware definitions for PhoneFix.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class BloatwareItem:
    package_name: str
    label: str
    description: str
    risk_level: str  # 'SAFE', 'MODERATE', 'USER_DECISION'
    is_installed: bool = False
    is_disabled: bool = False

class BaseBrandProfile(ABC):
    """Abstract base class for brand-specific bloatware and optimization profiles."""

    @property
    @abstractmethod
    def brand_name(self) -> str:
        pass

    @abstractmethod
    def get_bloatware_candidates(self) -> List[BloatwareItem]:
        """Returns list of brand-specific known bloatware/telemetry packages."""
        pass
