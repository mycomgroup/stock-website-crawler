"""
signals/extreme_signals.py
极值类信号检测模块。

极值类信号：从"正常"变"极端"的状态变化

信号返回值：
- 1: 进入超买区（看涨过度，可能回调）
- -1: 进入超卖区（看跌过度，可能反弹）
- 0: 正常区域

输出格式：DataFrame
- date: 日期
- signal: 信号值 (1/-1/0)
- type: 信号类型
- indicator_value: 指标值
"""

import warnings
from typing import Optional, Union
import pandas as pd
import numpy as np

try:
    from ..factors.technical import _get_daily_ohlcv, _compute_ema, _compute_ma, safe_divide
except ImportError:
    from jk2bt.factors.technical import _get_daily_ohlcv, _compute_ema, _compute_ma
    def safe_divide(a, b, fill_value=np.nan):
        """安全除法，避免除零错误"""
        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.divide(a, b)
            result = np.where(np.isfinite(result), result, fill_value)
        if isinstance(a, pd.Series):
            return pd.Series(result, index=a.index)
        return result


# =====================================================================
# RSI 超买超卖信号
# =====================================================================


def detect_rsi_extreme(
    symbol: str,
    window: int = 14,
    upper: float = 70.0,
    lower: float = 30.0,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 RSI 超买超卖信号。

    超买：RSI > upper（通常70）
    超卖：RSI < lower（通常30）

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        RSI计算周期（默认14）
    upper : float
        超买阈值（默认70）
    lower : float
        超卖阈值（默认30）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, rsi_value
    """
    need_count = window + 20
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return pd.DataFrame(columns=["date", "signal", "type", "rsi_value"])

    df = df.copy()
    close = df["close"].astype(float)

    # 计算RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = (-delta).where(delta < 0, 0)

    avg_gain = gain.ewm(span=window, adjust=False).mean()
    avg_loss = loss.ewm(span=window, adjust=False).mean()

    rs = safe_divide(avg_gain, avg_loss)
    rsi = 100 - safe_divide(100, 1 + rs)

    # 检测超买超卖
    rsi_prev = rsi.shift(1)

    # 进入超买区：RSI从下方穿越upper
    enter_overbought = (rsi > upper) & (rsi_prev <= upper)
    # 离开超买区：RSI从上方穿越upper
    exit_overbought = (rsi < upper) & (rsi_prev >= upper)
    # 进入超卖区：RSI从上方穿越lower
    enter_oversold = (rsi < lower) & (rsi_prev >= lower)
    # 离开超卖区：RSI从下方穿越lower
    exit_oversold = (rsi > lower) & (rsi_prev <= lower)

    signal = pd.Series(0, index=df.index)
    signal[enter_overbought] = 1
    signal[enter_oversold] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "rsi_value": rsi.values,
    })

    result.loc[result["signal"] == 1, "type"] = "rsi_overbought"
    result.loc[result["signal"] == -1, "type"] = "rsi_oversold"

    # 只返回有信号的记录
    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# CCI 极端信号
# =====================================================================


def detect_cci_extreme(
    symbol: str,
    window: int = 10,
    upper: float = 100.0,
    lower: float = -100.0,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 CCI 极端超买超卖信号。

    极端超买：CCI > upper（通常100）
    极端超卖：CCI < lower（通常-100）

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        CCI计算周期（默认10）
    upper : float
        超买阈值（默认100）
    lower : float
        超卖阈值（默认-100）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, cci_value
    """
    need_count = window + 20
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return pd.DataFrame(columns=["date", "signal", "type", "cci_value"])

    df = df.copy()
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)

    # 计算CCI
    tp = (high + low + close) / 3
    ma_tp = _compute_ma(tp, window)
    md = tp.rolling(window=window, min_periods=window).apply(
        lambda x: np.abs(x - x.mean()).mean()
    )
    cci = safe_divide(tp - ma_tp, 0.015 * md)

    # 检测极端区域
    cci_prev = cci.shift(1)

    # 进入极端超买区
    enter_overbought = (cci > upper) & (cci_prev <= upper)
    # 进入极端超卖区
    enter_oversold = (cci < lower) & (cci_prev >= lower)

    signal = pd.Series(0, index=df.index)
    signal[enter_overbought] = 1
    signal[enter_oversold] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "cci_value": cci.values,
    })

    result.loc[result["signal"] == 1, "type"] = "cci_extreme_overbought"
    result.loc[result["signal"] == -1, "type"] = "cci_extreme_oversold"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# BIAS 极端偏离信号
# =====================================================================


def detect_bias_extreme(
    symbol: str,
    window: int = 10,
    upper: float = 5.0,
    lower: float = -5.0,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 BIAS 极端偏离信号。

    严重超买：BIAS > upper%
    严重超卖：BIAS < lower%

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        BIAS计算周期（默认10）
    upper : float
        超买阈值百分比（默认5）
    lower : float
        超卖阈值百分比（默认-5）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, bias_value
    """
    need_count = window + 20
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return pd.DataFrame(columns=["date", "signal", "type", "bias_value"])

    df = df.copy()
    close = df["close"].astype(float)

    # 计算BIAS
    ma = _compute_ma(close, window)
    bias = safe_divide(close - ma, ma) * 100

    # 检测极端偏离
    bias_prev = bias.shift(1)

    # 进入严重超买区
    enter_overbought = (bias > upper) & (bias_prev <= upper)
    # 进入严重超卖区
    enter_oversold = (bias < lower) & (bias_prev >= lower)

    signal = pd.Series(0, index=df.index)
    signal[enter_overbought] = 1
    signal[enter_oversold] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "bias_value": bias.values,
    })

    result.loc[result["signal"] == 1, "type"] = f"bias_{window}_extreme_overbought"
    result.loc[result["signal"] == -1, "type"] = f"bias_{window}_extreme_oversold"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# KDJ 极端信号
# =====================================================================


def detect_kdj_extreme(
    symbol: str,
    n: int = 9,
    m1: int = 3,
    m2: int = 3,
    upper: float = 80.0,
    lower: float = 20.0,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 KDJ 极端区域信号。

    超买：K > 80 且 D > 80
    超卖：K < 20 且 D < 20

    Parameters
    ----------
    symbol : str
        股票代码
    n : int
        RSV计算周期
    m1 : int
        K值平滑周期
    m2 : int
        D值平滑周期
    upper : float
        超买阈值（默认80）
    lower : float
        超卖阈值（默认20）
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

    # 计算KDJ
    low_n = low.rolling(window=n, min_periods=n).min()
    high_n = high.rolling(window=n, min_periods=n).max()

    rsv = safe_divide(close - low_n, high_n - low_n) * 100
    k = rsv.ewm(span=m1, adjust=False).mean()
    d = k.ewm(span=m2, adjust=False).mean()

    # 检测极端区域
    k_prev = k.shift(1)
    d_prev = d.shift(1)

    # 进入超买区
    enter_overbought = (k > upper) & (k_prev <= upper)
    # 进入超卖区
    enter_oversold = (k < lower) & (k_prev >= lower)

    signal = pd.Series(0, index=df.index)
    signal[enter_overbought] = 1
    signal[enter_oversold] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "k_value": k.values,
        "d_value": d.values,
    })

    result.loc[result["signal"] == 1, "type"] = "kdj_overbought"
    result.loc[result["signal"] == -1, "type"] = "kdj_oversold"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# 批量检测极值信号
# =====================================================================


def detect_all_extreme_signals(
    symbol: str,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    检测所有极值类信号。

    Parameters
    ----------
    symbol : str
        股票代码
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        所有极值信号汇总
    """
    signals = []

    # RSI极值
    try:
        rsi_signals = detect_rsi_extreme(symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update)
        if not rsi_signals.empty:
            signals.append(rsi_signals)
    except Exception as e:
        warnings.warn(f"RSI极值检测失败: {e}")

    # CCI极值
    try:
        cci_signals = detect_cci_extreme(symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update)
        if not cci_signals.empty:
            signals.append(cci_signals)
    except Exception as e:
        warnings.warn(f"CCI极值检测失败: {e}")

    # BIAS极值
    try:
        bias_signals = detect_bias_extreme(symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update)
        if not bias_signals.empty:
            signals.append(bias_signals)
    except Exception as e:
        warnings.warn(f"BIAS极值检测失败: {e}")

    if not signals:
        return pd.DataFrame(columns=["date", "signal", "type"])

    result = pd.concat(signals, ignore_index=True)
    result = result.sort_values("date").reset_index(drop=True)

    return result


__all__ = [
    "detect_rsi_extreme",
    "detect_cci_extreme",
    "detect_bias_extreme",
    "detect_kdj_extreme",
    "detect_all_extreme_signals",
]