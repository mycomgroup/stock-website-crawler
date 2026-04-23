from __future__ import annotations

import pandas as pd

from .allocator import FourTierAllocator
from .config import FourTierConfig, RF7UniverseConfig
from .selector import RF7Selector


class RF7Pipeline:
    """Formal RF7 production-caliber pipeline:
    PB10 main + PB20 secondary + RFScore==7 + four-tier holdings + hard filters + industry cap + keep cash.
    """

    def __init__(
        self,
        universe_config: RF7UniverseConfig | None = None,
        tier_config: FourTierConfig | None = None,
    ) -> None:
        self.universe_config = universe_config or RF7UniverseConfig()
        self.tier_config = tier_config or FourTierConfig()
        self.selector = RF7Selector(self.universe_config)
        self.allocator = FourTierAllocator(self.universe_config, self.tier_config)

    def run(self, universe_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        artifacts = self.selector.select(universe_df)
        allocation = self.allocator.allocate(artifacts.selected)
        return artifacts.selected, allocation
