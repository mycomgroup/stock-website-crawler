from __future__ import annotations

from typing import List

import pandas as pd

from .config import FourTierConfig, RF7UniverseConfig


class FourTierAllocator:
    def __init__(self, universe_config: RF7UniverseConfig, tier_config: FourTierConfig) -> None:
        self.universe_config = universe_config
        self.tier_config = tier_config
        self.tier_config.validate()

    def allocate(self, selected: pd.DataFrame) -> pd.DataFrame:
        if selected.empty:
            return pd.DataFrame(columns=["date", "asset", "target_weight", "cash_ratio", "tier", "industry"])

        out: List[pd.DataFrame] = []
        tier_names = list(self.tier_config.tier_weights.keys())
        tier_values = list(self.tier_config.tier_weights.values())

        for date, g in selected.groupby("date", sort=True):
            g = g.sort_values(["pool_type", "alpha_rank"]).head(self.universe_config.max_positions).copy()
            g["tier"] = [tier_names[i % 4] for i in range(len(g))]
            g["raw_weight"] = [tier_values[i % 4] for i in range(len(g))]

            # industry cap first
            industry_sum = g.groupby("industry")["raw_weight"].sum()
            cap_ratio = (self.universe_config.industry_max_weight / industry_sum).clip(upper=1.0)
            g = g.merge(cap_ratio.rename("industry_scale"), on="industry", how="left")
            g["scaled_weight"] = g["raw_weight"] * g["industry_scale"]

            # normalize to <= 1, keep residual as cash
            weight_sum = float(g["scaled_weight"].sum())
            if weight_sum > 1.0:
                g["target_weight"] = g["scaled_weight"] / weight_sum
                cash_ratio = 0.0
            else:
                g["target_weight"] = g["scaled_weight"]
                cash_ratio = max(self.universe_config.min_cash_ratio, 1.0 - weight_sum)

            g["cash_ratio"] = cash_ratio
            g["date"] = date
            out.append(g[["date", "asset", "industry", "tier", "target_weight", "cash_ratio"]])

        return pd.concat(out, ignore_index=True)
