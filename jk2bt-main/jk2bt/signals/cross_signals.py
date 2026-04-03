"""
signals/cross_signals.py
交叉类信号检测模块。

交叉类信号：从"没交叉"变"交叉"的状态变化

信号返回值：
- 1: 金叉/上穿（看涨信号）
- -1: 死叉/下穿（看跌信号）
- 0: 无交叉

输出格式：DataFrame
- date: 日期
- signal: 信号值 (1/-1/0)
- type: 信号类型 ('ma_golden_cross', 'ma_dead_cross', ...)
"""

import warnings
from typing import Optional, Union
import pandas as pd
import numpy as np

try:
    from ..factors.technical import _get_daily_ohlcv, _compute_ma, _compute_ema, safe_divide
except ImportError:
    from jk2bt.factors.technical import _get_daily_ohlcv, _compute_ma, _compute_ema
    # 定义safe_divide的本地版本
    def safe_divide(a, b, fill_value=np.nan):
        """安全除法，避免除零错误"""
        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.divide(a, b)
            result = np.where(np.isfinite(result), result, fill_value)
        if isinstance(a, pd.Series):
            return pd.Series(result, index=a.index)
        return result


# =====================================================================
# MA 交叉信号
# =====================================================================


def detect_ma_cross(
    symbol: str,
    fast: int = 5,
    slow: int = 20,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 MA 金叉/死叉信号。

    金叉：快线上穿慢线
    死叉：快线下穿慢线

    Parameters
    ----------
    symbol : str
        股票代码
    fast : int
        快线周期（默认5日）
    slow : int
        慢线周期（默认20日）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type
        signal: 1 (金叉), -1 (死叉), 0 (无交叉)
    """
    need_count = slow + 20
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return pd.DataFrame(columns=["date", "signal", "type"])

    df = df.copy()
    close = df["close"].astype(float)

    # 计算快慢均线
    ma_fast = _compute_ma(close, fast)
    ma_slow = _compute_ma(close, slow)

    # 计算交叉
    diff = ma_fast - ma_slow
    diff_prev = diff.shift(1)

    # 金叉：快线从下方穿越到上方
    golden_cross = (diff > 0) & (diff_prev <= 0)
    # 死叉：快线从上方穿越到下方
    dead_cross = (diff < 0) & (diff_prev >= 0)

    signal = pd.Series(0, index=df.index)
    signal[golden_cross] = 1
    signal[dead_cross] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
    })

    # 添加信号类型
    result.loc[result["signal"] == 1, "type"] = f"ma_{fast}_{slow}_golden_cross"
    result.loc[result["signal"] == -1, "type"] = f"ma_{fast}_{slow}_dead_cross"
    result.loc[result["signal"] == 0, "type"] = "no_signal"

    # 过滤掉无信号的记录（可选）
    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# MACD 交叉信号
# =====================================================================


def detect_macd_cross(
    symbol: str,
    fast: int = 12,
    slow: int = 26,
    signal_period: int = 9,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 MACD 金叉/死叉信号。

    金叉：DIF上穿DEA
    死叉：DIF下穿DEA

    Parameters
    ----------
    symbol : str
        股票代码
    fast : int
        快线EMA周期（默认12）
    slow : int
        慢线EMA周期（默认26）
    signal_period : int
        DEA周期（默认9）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, macd_value
    """
    need_count = slow + signal_period + 20
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return pd.DataFrame(columns=["date", "signal", "type"])

    df = df.copy()
    close = df["close"].astype(float)

    # 计算MACD
    ema_fast = _compute_ema(close, fast)
    ema_slow = _compute_ema(close, slow)
    dif = ema_fast - ema_slow
    dea = _compute_ema(dif, signal_period)
    macd = 2 * (dif - dea)

    # 计算交叉
    diff = dif - dea
    diff_prev = diff.shift(1)

    # 金叉
    golden_cross = (diff > 0) & (diff_prev <= 0)
    # 死叉
    dead_cross = (diff < 0) & (diff_prev >= 0)

    signal = pd.Series(0, index=df.index)
    signal[golden_cross] = 1
    signal[dead_cross] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "macd_value": macd.values,
    })

    result.loc[result["signal"] == 1, "type"] = "macd_golden_cross"
    result.loc[result["signal"] == -1, "type"] = "macd_dead_cross"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# KDJ 交叉信号
# =====================================================================


def detect_kdj_cross(
    symbol: str,
    n: int = 9,
    m1: int = 3,
    m2: int = 3,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 KDJ 金叉/死叉信号。

    金叉：K线上穿D线
    死叉：K线下穿D线

    Parameters
    ----------
    symbol : str
        股票代码
    n : int
        RSV计算周期（默认9）
    m1 : int
        K值平滑周期（默认3）
    m2 : int
        D值平滑周期（默认3）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, k_value, d_value
    """
    need_count = n + m1 + m2 + 20
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return pd.DataFrame(columns=["date", "signal", "type"])

    df = df.copy()
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)

    # 计算RSV
    low_n = low.rolling(window=n, min_periods=n).min()
    high_n = high.rolling(window=n, min_periods=n).max()

    rsv = safe_divide(close - low_n, high_n - low_n) * 100

    # 计算K和D
    k = rsv.ewm(span=m1, adjust=False).mean()
    d = k.ewm(span=m2, adjust=False).mean()

    # 计算交叉
    diff = k - d
    diff_prev = diff.shift(1)

    # 金叉
    golden_cross = (diff > 0) & (diff_prev <= 0)
    # 死叉
    dead_cross = (diff < 0) & (diff_prev >= 0)

    signal = pd.Series(0, index=df.index)
    signal[golden_cross] = 1
    signal[dead_cross] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "k_value": k.values,
        "d_value": d.values,
    })

    result.loc[result["signal"] == 1, "type"] = "kdj_golden_cross"
    result.loc[result["signal"] == -1, "type"] = "kdj_dead_cross"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# EMA 交叉信号
# =====================================================================


def detect_ema_cross(
    symbol: str,
    fast: int = 10,
    slow: int = 20,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 EMA 金叉/死叉信号。

    金叉：快线EMA上穿慢线EMA
    死叉：快线EMA下穿慢线EMA

    Parameters
    ----------
    symbol : str
        股票代码
    fast : int
        快线周期（默认10日）
    slow : int
        慢线周期（默认20日）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type
    """
    need_count = slow + 20
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return pd.DataFrame(columns=["date", "signal", "type"])

    df = df.copy()
    close = df["close"].astype(float)

    # 计算快慢EMA
    ema_fast = _compute_ema(close, fast)
    ema_slow = _compute_ema(close, slow)

    # 计算交叉
    diff = ema_fast - ema_slow
    diff_prev = diff.shift(1)

    golden_cross = (diff > 0) & (diff_prev <= 0)
    dead_cross = (diff < 0) & (diff_prev >= 0)

    signal = pd.Series(0, index=df.index)
    signal[golden_cross] = 1
    signal[dead_cross] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
    })

    result.loc[result["signal"] == 1, "type"] = f"ema_{fast}_{slow}_golden_cross"
    result.loc[result["signal"] == -1, "type"] = f"ema_{fast}_{slow}_dead_cross"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# VMACD 翻红翻绿信号
# =====================================================================


def detect_vmacd_cross(
    symbol: str,
    fast: int = 12,
    slow: int = 26,
    signal_period: int = 9,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 VMACD 翻红/翻绿信号。

    翻红：VMACD柱由负转正
    翻绿：VMACD柱由正转负

    Parameters
    ----------
    symbol : str
        股票代码
    fast : int
        快线EMA周期（默认12）
    slow : int
        慢线EMA周期（默认26）
    signal_period : int
        DEA周期（默认9）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type
    """
    need_count = slow + signal_period + 20
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return pd.DataFrame(columns=["date", "signal", "type"])

    df = df.copy()
    volume = df["volume"].astype(float)

    # 计算VMACD（基于成交量的MACD）
    ema_fast = _compute_ema(volume, fast)
    ema_slow = _compute_ema(volume, slow)
    dif = ema_fast - ema_slow
    dea = _compute_ema(dif, signal_period)
    vmacd = 2 * (dif - dea)

    # 检测翻红翻绿
    vmacd_prev = vmacd.shift(1)

    # 翻红：由负转正
    turn_red = (vmacd > 0) & (vmacd_prev <= 0)
    # 翻绿：由正转负
    turn_green = (vmacd < 0) & (vmacd_prev >= 0)

    signal = pd.Series(0, index=df.index)
    signal[turn_red] = 1
    signal[turn_green] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "vmacd_value": vmacd.values,
    })

    result.loc[result["signal"] == 1, "type"] = "vmacd_turn_red"
    result.loc[result["signal"] == -1, "type"] = "vmacd_turn_green"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# 批量检测交叉信号
# =====================================================================


def detect_all_cross_signals(
    symbol: str,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    检测所有交叉类信号。

    Parameters
    ----------
    symbol : str
        股票代码
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        所有交叉信号汇总
    """
    signals = []

    # MA交叉
    try:
        ma_signals = detect_ma_cross(symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update)
        if not ma_signals.empty:
            signals.append(ma_signals)
    except Exception as e:
        warnings.warn(f"MA交叉检测失败: {e}")

    # MACD交叉
    try:
        macd_signals = detect_macd_cross(symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update)
        if not macd_signals.empty:
            signals.append(macd_signals)
    except Exception as e:
        warnings.warn(f"MACD交叉检测失败: {e}")

    # KDJ交叉
    try:
        kdj_signals = detect_kdj_cross(symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update)
        if not kdj_signals.empty:
            signals.append(kdj_signals)
    except Exception as e:
        warnings.warn(f"KDJ交叉检测失败: {e}")

    if not signals:
        return pd.DataFrame(columns=["date", "signal", "type"])

    result = pd.concat(signals, ignore_index=True)
    result = result.sort_values("date").reset_index(drop=True)

    return result


__all__ = [
    "detect_ma_cross",
    "detect_macd_cross",
    "detect_kdj_cross",
    "detect_ema_cross",
    "detect_vmacd_cross",
    "detect_all_cross_signals",
]