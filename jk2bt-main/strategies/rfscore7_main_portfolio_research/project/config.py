from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class RF7UniverseConfig:
    """Hard-frozen universe rules for RF7 formal version."""

    pb_main_threshold: float = 0.10
    pb_secondary_threshold: float = 0.20
    rfscore_exact: int = 7
    industry_max_weight: float = 0.35
    max_positions: int = 20
    min_cash_ratio: float = 0.0
    hard_filter_column: str = "hard_filter_pass"


@dataclass(frozen=True)
class FourTierConfig:
    """Four-tier position sizing configuration.

    Each tier is an absolute target position cap per symbol before normalization.
    """

    tier_weights: Dict[str, float] = field(
        default_factory=lambda: {
            "tier_1": 0.08,
            "tier_2": 0.06,
            "tier_3": 0.04,
            "tier_4": 0.02,
        }
    )

    def validate(self) -> None:
        if len(self.tier_weights) != 4:
            raise ValueError("Four-tier config must contain exactly 4 tiers.")
        if any(w <= 0 for w in self.tier_weights.values()):
            raise ValueError("All tier weights must be > 0.")
