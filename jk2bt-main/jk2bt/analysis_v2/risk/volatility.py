"""
波动率风控模块
"""
from typing import Optional
import pandas as pd
import numpy as np

from ..core.indicators import atr
from ..data.fetcher import get_ohlcv


def compute_volatility(
    symbol: str,
    window: int = 20,
    end_date: Optional[str] = None,
    annualize: bool = True
) -> dict:
    """
    计算波动率指标
    
    Args:
        symbol: 股票代码
        window: 窗口大小
        end_date: 结束日期
        annualize: 是否年化
    
    Returns:
        包含 volatility, atr, atr_ratio 的字典
    """
    df = get_ohlcv(symbol, end_date=end_date, count=window + 10)
    
    if df.empty or len(df) < window:
        return {
            'volatility': np.nan,
            'atr': np.nan,
            'atr_ratio': np.nan
        }
    
    close = df['close']
    high = df['high']
    low = df['low']
    
    # 历史波动率
    returns = close.pct_change()
    volatility = returns.rolling(window=window).std().iloc[-1]
    if annualize:
        volatility = volatility * np.sqrt(252)
    
    # ATR
    atr_value = atr(high, low, close, window).iloc[-1]
    
    # ATR占比
    atr_ratio = atr_value / close.iloc[-1] if close.iloc[-1] > 0 else np.nan
    
    return {
        'volatility': volatility,
        'atr': atr_value,
        'atr_ratio': atr_ratio
    }


def compute_volatility_adjusted_position(
    symbol: str,
    target_volatility: float = 0.15,
    end_date: Optional[str] = None
) -> float:
    """
    根据波动率计算建议仓位
    
    Args:
        symbol: 股票代码
        target_volatility: 目标年化波动率
        end_date: 结束日期
    
    Returns:
        建议仓位比例 (0-1)
    """
    vol_data = compute_volatility(symbol, end_date=end_date)
    current_vol = vol_data['volatility']
    
    if np.isnan(current_vol) or current_vol == 0:
        return 0.0
    
    position = target_volatility / current_vol
    return min(max(position, 0.0), 1.0)


def compute_atr_stop_loss(
    symbol: str,
    multiplier: float = 2.0,
    window: int = 14,
    end_date: Optional[str] = None
) -> dict:
    """
    基于ATR计算止损价格
    
    Args:
        symbol: 股票代码
        multiplier: ATR倍数
        window: ATR窗口
        end_date: 结束日期
    
    Returns:
        包含 stop_loss_price, current_price, atr 的字典
    """
    df = get_ohlcv(symbol, end_date=end_date, count=window + 10)
    
    if df.empty:
        return {
            'stop_loss_price': np.nan,
            'current_price': np.nan,
            'atr': np.nan
        }
    
    close = df['close']
    high = df['high']
    low = df['low']
    
    current_price = close.iloc[-1]
    atr_value = atr(high, low, close, window).iloc[-1]
    stop_loss_price = current_price - multiplier * atr_value
    
    return {
        'stop_loss_price': stop_loss_price,
        'current_price': current_price,
        'atr': atr_value
    }