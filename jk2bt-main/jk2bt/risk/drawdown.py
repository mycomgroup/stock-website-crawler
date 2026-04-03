"""
risk/drawdown.py
回撤风控模块。

用途：监控回撤，触发风控动作。
"""

import warnings
from typing import Optional, Union, Dict
import pandas as pd
import numpy as np

try:
    from ..factors.technical import _get_daily_ohlcv
except ImportError:
    from jk2bt.factors.technical import _get_daily_ohlcv


# =====================================================================
# 回撤计算
# =====================================================================


def compute_max_drawdown(prices: pd.Series) -> float:
    """
    计算最大回撤。

    Parameters
    ----------
    prices : pd.Series
        价格序列

    Returns
    -------
    float
        最大回撤（正数，如0.2表示20%回撤）
    """
    if prices is None or len(prices) == 0:
        return np.nan

    # 计算累计最高点
    cummax = prices.cummax()

    # 计算回撤
    drawdown = (cummax - prices) / cummax

    return float(drawdown.max())


def compute_drawdown(prices: pd.Series) -> pd.Series:
    """
    计算时点回撤序列。

    Parameters
    ----------
    prices : pd.Series
        价格序列

    Returns
    -------
    pd.Series
        各时点的回撤值
    """
    if prices is None or len(prices) == 0:
        return pd.Series()

    cummax = prices.cummax()
    drawdown = (cummax - prices) / cummax

    return drawdown


# =====================================================================
# 回撤预警
# =====================================================================


def check_drawdown_alert(
    prices: pd.Series,
    warning_level: float = 0.10,
    critical_level: float = 0.20,
) -> Dict:
    """
    回撤预警检测。

    Parameters
    ----------
    prices : pd.Series
        价格序列
    warning_level : float
        警告级别回撤（默认10%）
    critical_level : float
        危险级别回撤（默认20%）

    Returns
    -------
    dict
        {
            'current_drawdown': 当前回撤,
            'max_drawdown': 最大回撤,
            'status': 'normal' / 'warning' / 'critical',
            'action': 建议动作
        }
    """
    if prices is None or len(prices) == 0:
        return {
            "current_drawdown": np.nan,
            "max_drawdown": np.nan,
            "status": "normal",
            "action": "无数据",
        }

    drawdown = compute_drawdown(prices)
    current_dd = float(drawdown.iloc[-1])
    max_dd = float(drawdown.max())

    if current_dd >= critical_level:
        status = "critical"
        action = "建议减仓或止损"
    elif current_dd >= warning_level:
        status = "warning"
        action = "建议降低仓位或设置止损"
    else:
        status = "normal"
        action = "继续持有"

    return {
        "current_drawdown": current_dd,
        "max_drawdown": max_dd,
        "status": status,
        "action": action,
    }


# =====================================================================
# 股票回撤监控
# =====================================================================


def monitor_stock_drawdown(
    symbol: str,
    window: int = 60,
    warning_level: float = 0.10,
    critical_level: float = 0.20,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> Dict:
    """
    监控股票回撤。

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        回看窗口（默认60日）
    warning_level : float
        警告级别
    critical_level : float
        危险级别
    end_date : str, optional
        截止日期

    Returns
    -------
    dict
        回撤监控结果
    """
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=window + 10,
    )

    if df.empty or "close" not in df.columns:
        return {
            "symbol": symbol,
            "current_drawdown": np.nan,
            "max_drawdown": np.nan,
            "status": "normal",
            "action": "无数据",
        }

    df = df.set_index("date")
    close = df["close"].astype(float)

    # 只取最近window天的数据
    if len(close) > window:
        close = close.tail(window)

    result = check_drawdown_alert(close, warning_level, critical_level)
    result["symbol"] = symbol
    result["window"] = window

    return result


# =====================================================================
# 回撤恢复时间
# =====================================================================


def compute_recovery_time(prices: pd.Series) -> Dict:
    """
    计算回撤恢复时间。

    Parameters
    ----------
    prices : pd.Series
        价格序列

    Returns
    -------
    dict
        {
            'max_recovery_days': 最长恢复天数,
            'current_recovery_days': 当前恢复天数（若在回撤中）,
            'in_drawdown': 是否在回撤中
        }
    """
    if prices is None or len(prices) == 0:
        return {
            "max_recovery_days": np.nan,
            "current_recovery_days": 0,
            "in_drawdown": False,
        }

    cummax = prices.cummax()
    drawdown = (cummax - prices) / cummax

    # 找到新高点
    new_high = prices == cummax

    # 计算恢复时间
    recovery_days = []
    current_recovery = 0
    max_recovery = 0

    for i in range(len(prices)):
        if new_high.iloc[i]:
            if current_recovery > max_recovery:
                max_recovery = current_recovery
            recovery_days.append(current_recovery)
            current_recovery = 0
        else:
            current_recovery += 1
            recovery_days.append(current_recovery)

    # 当前是否在回撤中
    in_drawdown = drawdown.iloc[-1] > 0.001

    return {
        "max_recovery_days": max_recovery,
        "current_recovery_days": current_recovery if in_drawdown else 0,
        "in_drawdown": in_drawdown,
    }


# =====================================================================
# 回撤统计
# =====================================================================


def compute_drawdown_statistics(
    symbol: str,
    window: int = 252,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> Dict:
    """
    计算回撤统计信息。

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        回看窗口（默认252日）
    end_date : str, optional
        截止日期

    Returns
    -------
    dict
        回撤统计信息
    """
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=window + 10,
    )

    if df.empty or "close" not in df.columns:
        return {
            "symbol": symbol,
            "max_drawdown": np.nan,
            "avg_drawdown": np.nan,
            "current_drawdown": np.nan,
            "drawdown_days": 0,
        }

    df = df.set_index("date")
    close = df["close"].astype(float)

    if len(close) > window:
        close = close.tail(window)

    drawdown = compute_drawdown(close)

    # 统计回撤天数
    dd_days = (drawdown > 0.01).sum()

    return {
        "symbol": symbol,
        "max_drawdown": float(drawdown.max()),
        "avg_drawdown": float(drawdown.mean()),
        "current_drawdown": float(drawdown.iloc[-1]),
        "drawdown_days": int(dd_days),
        "window": window,
    }


__all__ = [
    "compute_max_drawdown",
    "compute_drawdown",
    "check_drawdown_alert",
    "monitor_stock_drawdown",
    "compute_recovery_time",
    "compute_drawdown_statistics",
]