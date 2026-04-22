"""
类型定义模块
"""
from typing import TypedDict, Literal, Optional, Any
from datetime import datetime
import pandas as pd


class OHLCV(TypedDict):
    """标准OHLCV数据结构"""
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class IndicatorResult(TypedDict):
    """指标计算结果"""
    value: float
    status: Literal["success", "insufficient_data", "error"]
    message: Optional[str]


class Signal(TypedDict):
    """信号结构"""
    date: datetime
    signal_type: str
    direction: Literal["buy", "sell", "hold"]
    strength: float
    metadata: dict[str, Any]


class FactorValue(TypedDict):
    """因子值"""
    date: datetime
    factor_name: str
    value: float


class VolatilityResult(TypedDict):
    """波动率结果"""
    volatility: float
    atr: float
    atr_ratio: float


class DrawdownResult(TypedDict):
    """回撤结果"""
    max_drawdown: float
    max_drawdown_date: datetime
    current_drawdown: float
    in_drawdown: bool
    recovery_days: int