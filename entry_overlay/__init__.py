"""通用买点叠加能力（可在线/离线复用）."""

from .data_sources import AkshareAdapter, JQDataAdapter, MarketDataAdapter, PandasAdapter
from .engine import EntryDecision, EntryOverlayConfig, EntryOverlayEngine, EntryMode
from .factors import compute_15_ta_factors
from .offline import BacktestConfig, BacktestReport, grid_search_params, run_event_backtest
from .profiles import PROFILE_LIBRARY, build_profile_weights

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
]
