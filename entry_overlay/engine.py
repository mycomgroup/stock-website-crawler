from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd

from .factors import compute_15_ta_factors
from .profiles import build_profile_weights


class EntryMode(str, Enum):
    RANK_FILTER = "rank_filter"  # 用于选股最终排序过滤
    TIMING_ONLY = "timing_only"  # 必买，仅挑最佳买入时间


@dataclass
class EntryOverlayConfig:
    mode: EntryMode = EntryMode.RANK_FILTER
    profile: str = "general"
    min_score_to_buy: float = 0.58
    bar_count: int = 240
    top_k_minutes: int = 5
    wait_minutes_open: int = 3


@dataclass
class EntryDecision:
    score: float
    should_buy: bool
    best_times: List[Tuple[pd.Timestamp, float]]
    factor_contrib: Dict[str, float]


class EntryOverlayEngine:
    """通用买点叠加引擎。

    - RANK_FILTER: 返回分数用于重排和过滤
    - TIMING_ONLY: 默认 should_buy=True，但提供最佳时点
    """

    def __init__(self, conf: Optional[EntryOverlayConfig] = None, weights: Optional[Dict[str, float]] = None):
        self.conf = conf or EntryOverlayConfig()
        self.weights = weights or build_profile_weights(self.conf.profile, normalize=True)

    def score_latest(self, bars: pd.DataFrame) -> Tuple[float, Dict[str, float]]:
        factors = compute_15_ta_factors(bars.tail(self.conf.bar_count))
        row = factors.iloc[-1]
        contrib = {k: float(row.get(k, 0.5)) * w for k, w in self.weights.items()}
        score = sum(contrib.values()) / (sum(self.weights.values()) or 1.0)
        return score, contrib

    def rank_candidate_times(self, bars: pd.DataFrame, candidate_idx: Optional[Iterable[pd.Timestamp]] = None):
        factors = compute_15_ta_factors(bars.tail(self.conf.bar_count))
        if candidate_idx is None:
            candidate_idx = factors.index

        scores = []
        denom = sum(self.weights.values()) or 1.0
        for ts in candidate_idx:
            if ts not in factors.index:
                continue
            row = factors.loc[ts]
            s = sum(float(row.get(k, 0.5)) * w for k, w in self.weights.items()) / denom
            scores.append((ts, s))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[: self.conf.top_k_minutes]

    def decide(self, bars: pd.DataFrame, candidate_idx: Optional[Iterable[pd.Timestamp]] = None) -> EntryDecision:
        score, contrib = self.score_latest(bars)
        best_times = self.rank_candidate_times(bars, candidate_idx)

        if self.conf.mode == EntryMode.TIMING_ONLY:
            should_buy = True
        else:
            should_buy = score >= self.conf.min_score_to_buy

        return EntryDecision(
            score=score,
            should_buy=should_buy,
            best_times=best_times,
            factor_contrib=contrib,
        )
