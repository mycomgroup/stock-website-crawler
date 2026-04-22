"""
纯技术指标计算模块

设计原则:
1. 所有函数只接收 DataFrame/Series，不负责数据获取
2. 返回计算结果，不负责数据存储
3. 无外部依赖，可独立测试

所有指标函数都是纯函数，给定相同输入必定返回相同输出。
"""
from typing import Optional, Tuple
import pandas as pd
import numpy as np


# ==================== 移动平均类 ====================

def ma(series: pd.Series, window: int) -> pd.Series:
    """
    简单移动平均线
    
    Args:
        series: 数据序列
        window: 窗口大小
    
    Returns:
        移动平均序列
    """
    return series.rolling(window=window).mean()


def ema(series: pd.Series, span: int) -> pd.Series:
    """
    指数移动平均线
    
    Args:
        series: 数据序列
        span: 周期
    
    Returns:
        EMA序列
    """
    return series.ewm(span=span, adjust=False).mean()


def sma(series: pd.Series, window: int) -> pd.Series:
    """
    简单移动平均（与ma相同，保留别名）
    """
    return ma(series, window)


def wma(series: pd.Series, window: int) -> pd.Series:
    """
    加权移动平均
    
    Args:
        series: 数据序列
        window: 窗口大小
    
    Returns:
        WMA序列
    """
    weights = np.arange(1, window + 1)
    return series.rolling(window=window).apply(
        lambda x: np.dot(x, weights) / weights.sum(),
        raw=True
    )


# ==================== 趋势类 ====================

def macd(
    close: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    MACD指标
    
    Args:
        close: 收盘价序列
        fast: 快线周期
        slow: 慢线周期
        signal: 信号线周期
    
    Returns:
        (DIF, DEA, MACD柱)
    """
    ema_fast = ema(close, fast)
    ema_slow = ema(close, slow)
    dif = ema_fast - ema_slow
    dea = ema(dif, signal)
    macd_hist = (dif - dea) * 2
    return dif, dea, macd_hist


def boll(
    close: pd.Series,
    window: int = 20,
    num_std: float = 2.0
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    布林带
    
    Args:
        close: 收盘价序列
        window: 窗口大小
        num_std: 标准差倍数
    
    Returns:
        (上轨, 中轨, 下轨)
    """
    mid = ma(close, window)
    std = close.rolling(window=window).std()
    upper = mid + num_std * std
    lower = mid - num_std * std
    return upper, mid, lower


def sar(
    high: pd.Series,
    low: pd.Series,
    af_start: float = 0.02,
    af_increment: float = 0.02,
    af_max: float = 0.2
) -> pd.Series:
    """
    抛物线SAR
    
    Args:
        high: 最高价序列
        low: 最低价序列
        af_start: 起始加速因子
        af_increment: 加速因子增量
        af_max: 最大加速因子
    
    Returns:
        SAR值序列
    """
    length = len(high)
    sar = pd.Series(np.zeros(length), index=high.index)
    ep = high.iloc[0]
    af = af_start
    trend = 1
    
    sar.iloc[0] = low.iloc[0]
    
    for i in range(1, length):
        sar.iloc[i] = sar.iloc[i-1] + af * (ep - sar.iloc[i-1])
        
        if trend == 1:
            sar.iloc[i] = min(sar.iloc[i], low.iloc[i-1], low.iloc[i] if i >= 1 else low.iloc[i-1])
            if low.iloc[i] < sar.iloc[i]:
                trend = -1
                sar.iloc[i] = ep
                ep = low.iloc[i]
                af = af_start
            else:
                if high.iloc[i] > ep:
                    ep = high.iloc[i]
                    af = min(af + af_increment, af_max)
        else:
            sar.iloc[i] = max(sar.iloc[i], high.iloc[i-1], high.iloc[i] if i >= 1 else high.iloc[i-1])
            if high.iloc[i] > sar.iloc[i]:
                trend = 1
                sar.iloc[i] = ep
                ep = high.iloc[i]
                af = af_start
            else:
                if low.iloc[i] < ep:
                    ep = low.iloc[i]
                    af = min(af + af_increment, af_max)
    
    return sar


# ==================== 动量类 ====================

def rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """
    相对强弱指标
    
    Args:
        close: 收盘价序列
        window: 窗口大小
    
    Returns:
        RSI序列 (0-100)
    """
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi_value = 100 - (100 / (1 + rs))
    return rsi_value


def kdj(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    n: int = 9,
    m1: int = 3,
    m2: int = 3
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    KDJ随机指标
    
    Args:
        high: 最高价序列
        low: 最低价序列
        close: 收盘价序列
        n: RSV周期
        m1: K值平滑周期
        m2: D值平滑周期
    
    Returns:
        (K, D, J)
    """
    low_n = low.rolling(window=n).min()
    high_n = high.rolling(window=n).max()
    rsv = (close - low_n) / (high_n - low_n) * 100
    k = rsv.ewm(alpha=1/m1, adjust=False).mean()
    d = k.ewm(alpha=1/m2, adjust=False).mean()
    j = 3 * k - 2 * d
    return k, d, j


def wr(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    window: int = 14
) -> pd.Series:
    """
    威廉指标
    
    Args:
        high: 最高价序列
        low: 最低价序列
        close: 收盘价序列
        window: 窗口大小
    
    Returns:
        WR序列 (-100 to 0)
    """
    high_n = high.rolling(window=window).max()
    low_n = low.rolling(window=window).min()
    wr_value = (high_n - close) / (high_n - low_n) * -100
    return wr_value


def cci(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    window: int = 14
) -> pd.Series:
    """
    顺势指标
    
    Args:
        high: 最高价序列
        low: 最低价序列
        close: 收盘价序列
        window: 窗口大小
    
    Returns:
        CCI序列
    """
    tp = (high + low + close) / 3
    ma_tp = tp.rolling(window=window).mean()
    md = tp.rolling(window=window).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
    cci_value = (tp - ma_tp) / (0.015 * md)
    return cci_value


# ==================== 波动率类 ====================

def atr(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    window: int = 14
) -> pd.Series:
    """
    平均真实波幅
    
    Args:
        high: 最高价序列
        low: 最低价序列
        close: 收盘价序列
        window: 窗口大小
    
    Returns:
        ATR序列
    """
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return ma(tr, window)


def volatility(close: pd.Series, window: int = 20, annualize: bool = True) -> pd.Series:
    """
    历史波动率
    
    Args:
        close: 收盘价序列
        window: 窗口大小
        annualize: 是否年化
    
    Returns:
        波动率序列
    """
    returns = close.pct_change()
    vol = returns.rolling(window=window).std()
    if annualize:
        vol = vol * np.sqrt(252)
    return vol


# ==================== 成交量类 ====================

def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """
    能量潮指标
    
    Args:
        close: 收盘价序列
        volume: 成交量序列
    
    Returns:
        OBV序列
    """
    direction = np.sign(close.diff())
    direction.iloc[0] = 1
    return (volume * direction).cumsum()


def vwma(
    close: pd.Series,
    volume: pd.Series,
    window: int = 20
) -> pd.Series:
    """
    成交量加权移动平均
    
    Args:
        close: 收盘价序列
        volume: 成交量序列
        window: 窗口大小
    
    Returns:
        VWMA序列
    """
    pv = close * volume
    return pv.rolling(window=window).sum() / volume.rolling(window=window).sum()


def mfi(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    volume: pd.Series,
    window: int = 14
) -> pd.Series:
    """
    资金流量指标
    
    Args:
        high: 最高价序列
        low: 最低价序列
        close: 收盘价序列
        volume: 成交量序列
        window: 窗口大小
    
    Returns:
        MFI序列 (0-100)
    """
    tp = (high + low + close) / 3
    mf = tp * volume
    
    positive_mf = mf.where(tp > tp.shift(1), 0).rolling(window=window).sum()
    negative_mf = mf.where(tp < tp.shift(1), 0).rolling(window=window).sum()
    
    mfi_value = 100 - (100 / (1 + positive_mf / negative_mf))
    return mfi_value


# ==================== 形态类 ====================

def cross_up(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """
    上穿信号
    
    Args:
        series1: 序列1
        series2: 序列2
    
    Returns:
        布尔序列，True表示上穿
    """
    return (series1 > series2) & (series1.shift(1) <= series2.shift(1))


def cross_down(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """
    下穿信号
    
    Args:
        series1: 序列1
        series2: 序列2
    
    Returns:
        布尔序列，True表示下穿
    """
    return (series1 < series2) & (series1.shift(1) >= series2.shift(1))


def highest(series: pd.Series, window: int) -> pd.Series:
    """
    滚动最高值
    
    Args:
        series: 数据序列
        window: 窗口大小
    
    Returns:
        滚动最高值
    """
    return series.rolling(window=window).max()


def lowest(series: pd.Series, window: int) -> pd.Series:
    """
    滚动最低值
    
    Args:
        series: 数据序列
        window: 窗口大小
    
    Returns:
        滚动最低值
    """
    return series.rolling(window=window).min()


def hhv(high: pd.Series, window: int) -> pd.Series:
    """Highest High Value - 滚动最高价"""
    return highest(high, window)


def llv(low: pd.Series, window: int) -> pd.Series:
    """Lowest Low Value - 滚动最低价"""
    return lowest(low, window)


# ==================== 其他 ====================

def bias(close: pd.Series, window: int) -> pd.Series:
    """
    乖离率
    
    Args:
        close: 收盘价序列
        window: 窗口大小
    
    Returns:
        BIAS序列
    """
    ma_window = ma(close, window)
    return (close - ma_window) / ma_window * 100


def roc(close: pd.Series, window: int = 12) -> pd.Series:
    """
    变动率指标
    
    Args:
        close: 收盘价序列
        window: 窗口大小
    
    Returns:
        ROC序列
    """
    return (close - close.shift(window)) / close.shift(window) * 100


def momentum(close: pd.Series, window: int = 10) -> pd.Series:
    """
    动量指标
    
    Args:
        close: 收盘价序列
        window: 窗口大小
    
    Returns:
        动量序列
    """
    return close - close.shift(window)


def adx(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    window: int = 14
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    平均趋向指标
    
    Args:
        high: 最高价序列
        low: 最低价序列
        close: 收盘价序列
        window: 窗口大小
    
    Returns:
        (ADX, +DI, -DI)
    """
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low
    
    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0)
    
    tr_val = atr(high, low, close, 1) * 1  # TR = ATR with window=1
    tr_sum = tr_val.rolling(window=window).sum()
    
    plus_di = 100 * plus_dm.rolling(window=window).sum() / tr_sum
    minus_di = 100 * minus_dm.rolling(window=window).sum() / tr_sum
    
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx_val = ma(dx, window)
    
    return adx_val, plus_di, minus_di


def dmi(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    window: int = 14
) -> Tuple[pd.Series, pd.Series]:
    """
    动向指标（简化版，只返回+DI和-DI）
    
    Returns:
        (+DI, -DI)
    """
    _, plus_di, minus_di = adx(high, low, close, window)
    return plus_di, minus_di