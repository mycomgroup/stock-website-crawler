"""兼容层：保留旧导入路径 strategies.enhancements.ta_entry_overlay。"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd

from entry_overlay import (
    AkshareAdapter,
    BacktestConfig,
    BacktestReport,
    EntryDecision,
    EntryMode,
    EntryOverlayConfig,
    EntryOverlayEngine,
    JQDataAdapter,
    MarketDataAdapter,
    PandasAdapter,
    PROFILE_LIBRARY,
    build_profile_weights,
    compute_15_ta_factors,
    grid_search_params,
    run_event_backtest,
)


def score_entry_signal(minute_bars: pd.DataFrame, conf: Optional[EntryOverlayConfig] = None):
    engine = EntryOverlayEngine(conf)
    return engine.score_latest(minute_bars)


def select_better_entry_time(
    minute_bars: pd.DataFrame,
    candidate_idx: Optional[Iterable[pd.Timestamp]] = None,
    conf: Optional[EntryOverlayConfig] = None,
) -> List[Tuple[pd.Timestamp, float]]:
    engine = EntryOverlayEngine(conf)
    return engine.rank_candidate_times(minute_bars, candidate_idx)


__all__ = [
    "MarketDataAdapter",
    "JQDataAdapter",
    "AkshareAdapter",
    "PandasAdapter",
    "EntryMode",
    "EntryOverlayConfig",
    "EntryOverlayEngine",
    "EntryDecision",
    "compute_15_ta_factors",
    "PROFILE_LIBRARY",
    "build_profile_weights",
    "BacktestConfig",
    "BacktestReport",
    "run_event_backtest",
    "grid_search_params",
    "score_entry_signal",
    "select_better_entry_time",
]
