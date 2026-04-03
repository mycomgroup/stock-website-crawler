"""
signals/breakthrough_signals.py
突破类信号检测模块。

突破类信号：从"没突破"变"突破"的状态变化

信号返回值：
- 1: 突破信号（向上突破）
- -1: 跌破信号（向下突破）
- 0: 无突破

输出格式：DataFrame
- date: 日期
- signal: 信号值 (1/-1/0)
- type: 信号类型
"""

import warnings
from typing import Optional, Union
import pandas as pd
import numpy as np

try:
    from ..factors.technical import _get_daily_ohlcv, _compute_ma, _compute_std, safe_divide
except ImportError:
    from jk2bt.factors.technical import _get_daily_ohlcv, _compute_ma, _compute_std
    def safe_divide(a, b, fill_value=np.nan):
        """安全除法，避免除零错误"""
        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.divide(a, b)
            result = np.where(np.isfinite(result), result, fill_value)
        if isinstance(a, pd.Series):
            return pd.Series(result, index=a.index)
        return result


# =====================================================================
# 价格突破信号
# =====================================================================


def detect_price_breakout(
    symbol: str,
    window: int = 20,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测价格突破N日新高/新低信号。

    突破新高：收盘价 > 过去N天最高价
    跌破新低：收盘价 < 过去N天最低价

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        回看窗口（默认20日）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, close, high_n, low_n
    """
    need_count = window + 10
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
    high = df["high"].astype(float)
    low = df["low"].astype(float)

    # 计算过去N天的最高价和最低价（不包含当天）
    high_n = high.shift(1).rolling(window=window, min_periods=window).max()
    low_n = low.shift(1).rolling(window=window, min_periods=window).min()

    # 检测突破
    break_high = close > high_n
    break_low = close < low_n

    signal = pd.Series(0, index=df.index)
    signal[break_high] = 1
    signal[break_low] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "close": close.values,
        "high_n": high_n.values,
        "low_n": low_n.values,
    })

    result.loc[result["signal"] == 1, "type"] = f"price_breakout_high_{window}d"
    result.loc[result["signal"] == -1, "type"] = f"price_breakout_low_{window}d"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# 成交量突破信号
# =====================================================================


def detect_volume_breakout(
    symbol: str,
    window: int = 20,
    multiplier: float = 2.0,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测放量/缩量信号。

    放量：成交量 > N日均量 × multiplier
    缩量：成交量 < N日均量 / multiplier

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        均量计算窗口（默认20日）
    multiplier : float
        放量/缩量倍数（默认2倍）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, volume, avg_volume
    """
    need_count = window + 10
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

    # 计算N日均量
    avg_volume = _compute_ma(volume, window)

    # 检测放量/缩量
    volume_high = volume > avg_volume * multiplier
    volume_low = volume < avg_volume / multiplier

    signal = pd.Series(0, index=df.index)
    signal[volume_high] = 1
    signal[volume_low] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "volume": volume.values,
        "avg_volume": avg_volume.values,
        "volume_ratio": safe_divide(volume, avg_volume).values,
    })

    result.loc[result["signal"] == 1, "type"] = f"volume_breakout_high_{multiplier}x"
    result.loc[result["signal"] == -1, "type"] = f"volume_breakout_low_{multiplier}x"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# 布林带突破信号
# =====================================================================


def detect_boll_breakout(
    symbol: str,
    window: int = 20,
    num_std: float = 2.0,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测布林带突破信号。

    上穿布林上轨：收盘价 > boll_up
    下穿布林下轨：收盘价 < boll_down

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        布林带计算窗口（默认20日）
    num_std : float
        标准差倍数（默认2）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, close, boll_up, boll_down
    """
    need_count = window + 10
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

    # 计算布林带
    ma = _compute_ma(close, window)
    std = _compute_std(close, window)

    boll_up = ma + num_std * std
    boll_down = ma - num_std * std

    # 检测突破
    close_prev = close.shift(1)
    boll_up_prev = boll_up.shift(1)
    boll_down_prev = boll_down.shift(1)

    # 上穿布林上轨
    break_up = (close > boll_up) & (close_prev <= boll_up_prev)
    # 下穿布林下轨
    break_down = (close < boll_down) & (close_prev >= boll_down_prev)

    signal = pd.Series(0, index=df.index)
    signal[break_up] = 1
    signal[break_down] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "close": close.values,
        "boll_up": boll_up.values,
        "boll_down": boll_down.values,
        "boll_ma": ma.values,
    })

    result.loc[result["signal"] == 1, "type"] = "boll_breakout_up"
    result.loc[result["signal"] == -1, "type"] = "boll_breakout_down"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# 均线突破信号
# =====================================================================


def detect_ma_breakout(
    symbol: str,
    window: int = 20,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测均线突破信号。

    上穿均线：收盘价 > MA(window)
    下穿均线：收盘价 < MA(window)

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        均线周期（默认20日）
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, close, ma
    """
    need_count = window + 10
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

    # 计算均线
    ma = _compute_ma(close, window)

    # 检测突破
    close_prev = close.shift(1)
    ma_prev = ma.shift(1)

    # 上穿均线
    break_up = (close > ma) & (close_prev <= ma_prev)
    # 下穿均线
    break_down = (close < ma) & (close_prev >= ma_prev)

    signal = pd.Series(0, index=df.index)
    signal[break_up] = 1
    signal[break_down] = -1

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "close": close.values,
        f"ma_{window}": ma.values,
    })

    result.loc[result["signal"] == 1, "type"] = f"ma_{window}_breakout_up"
    result.loc[result["signal"] == -1, "type"] = f"ma_{window}_breakout_down"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# 批量检测突破信号
# =====================================================================


def detect_all_breakthrough_signals(
    symbol: str,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    检测所有突破类信号。

    Parameters
    ----------
    symbol : str
        股票代码
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        所有突破信号汇总
    """
    signals = []

    # 价格突破
    try:
        price_signals = detect_price_breakout(symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update)
        if not price_signals.empty:
            signals.append(price_signals)
    except Exception as e:
        warnings.warn(f"价格突破检测失败: {e}")

    # 成交量突破
    try:
        volume_signals = detect_volume_breakout(symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update)
        if not volume_signals.empty:
            signals.append(volume_signals)
    except Exception as e:
        warnings.warn(f"成交量突破检测失败: {e}")

    # 布林带突破
    try:
        boll_signals = detect_boll_breakout(symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update)
        if not boll_signals.empty:
            signals.append(boll_signals)
    except Exception as e:
        warnings.warn(f"布林带突破检测失败: {e}")

    if not signals:
        return pd.DataFrame(columns=["date", "signal", "type"])

    result = pd.concat(signals, ignore_index=True)
    result = result.sort_values("date").reset_index(drop=True)

    return result


__all__ = [
    "detect_price_breakout",
    "detect_volume_breakout",
    "detect_boll_breakout",
    "detect_ma_breakout",
    "detect_all_breakthrough_signals",
]