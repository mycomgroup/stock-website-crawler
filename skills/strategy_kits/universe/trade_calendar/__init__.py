"""
交易日历与基础池选择器

目标：让新策略可以统一拿交易日和基础池，不再在各策略里重复处理调仓日逻辑。
"""

from .trade_calendar import (
    get_trade_days,
    shift_trade_day,
    previous_trade_day,
    next_trade_day,
    set_trade_cal_source,
    get_all_trade_days,
    is_trade_cal_initialized,
    init_trade_cal_from_gateway,
    init_trade_cal_from_csv,
)
from .rebalance_schedule import get_rebalance_dates, get_rolling_window_bounds
from .universe_selector import resolve_base_universe, UniverseType

__all__ = [
    "set_trade_cal_source",
    "get_all_trade_days",
    "is_trade_cal_initialized",
    "init_trade_cal_from_gateway",
    "init_trade_cal_from_csv",
    "get_trade_days",
    "shift_trade_day",
    "previous_trade_day",
    "next_trade_day",
    "get_rebalance_dates",
    "get_rolling_window_bounds",
    "resolve_base_universe",
    "UniverseType",
]
