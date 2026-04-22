"""
回撤风控模块
"""
from typing import Optional
import pandas as pd
import numpy as np

from ..data.fetcher import get_ohlcv


def compute_drawdown(prices: pd.Series) -> pd.Series:
    """
    计算回撤序列
    
    Args:
        prices: 价格序列
    
    Returns:
        回撤序列（正值表示回撤幅度）
    """
    cummax = prices.cummax()
    drawdown = (cummax - prices) / cummax
    return drawdown


def compute_max_drawdown(prices: pd.Series) -> dict:
    """
    计算最大回撤
    
    Args:
        prices: 价格序列
    
    Returns:
        包含 max_drawdown, start_date, end_date 的字典
    """
    drawdown = compute_drawdown(prices)
    max_dd = drawdown.max()
    
    if max_dd == 0:
        return {
            'max_drawdown': 0.0,
            'start_date': None,
            'end_date': None,
            'recovery_days': 0
        }
    
    # 找到最大回撤结束点
    end_idx = drawdown.idxmax()
    
    # 找到最大回撤开始点（在此之前的高点）
    end_loc = prices.index.get_loc(end_idx)
    cummax_until_end = prices.iloc[:end_loc + 1].cummax()
    start_idx = cummax_until_end.idxmax()
    
    # 计算恢复天数
    if end_loc < len(prices) - 1:
        # 检查是否恢复
        recovery_idx = prices.iloc[end_loc + 1:][prices.iloc[end_loc + 1:] >= cummax_until_end.iloc[end_loc]]
        if len(recovery_idx) > 0:
            recovery_days = (recovery_idx.index[0] - end_idx).days
        else:
            recovery_days = -1  # 未恢复
    else:
        recovery_days = 0
    
    return {
        'max_drawdown': max_dd,
        'start_date': start_idx,
        'end_date': end_idx,
        'recovery_days': recovery_days
    }


def compute_recovery_time(prices: pd.Series) -> dict:
    """
    计算回撤恢复时间
    
    Args:
        prices: 价格序列
    
    Returns:
        包含 max_recovery_days, current_recovery_days, in_drawdown 的字典
    """
    drawdown = compute_drawdown(prices)
    cummax = prices.cummax()
    
    # 检查是否在回撤中
    in_drawdown = drawdown.iloc[-1] > 0.001
    
    # 计算当前回撤天数
    if in_drawdown:
        last_high_idx = prices[prices == cummax.iloc[-1]].index[0]
        current_recovery = (prices.index[-1] - last_high_idx).days
    else:
        current_recovery = 0
    
    # 计算历史最大恢复时间
    max_recovery = 0
    in_dd = False
    dd_start = None
    
    for i in range(len(prices)):
        if drawdown.iloc[i] > 0.001 and not in_dd:
            in_dd = True
            dd_start = cummax.iloc[:i+1].idxmax()
        elif drawdown.iloc[i] < 0.001 and in_dd:
            in_dd = False
            if dd_start is not None:
                recovery_days = (prices.index[i] - dd_start).days
                max_recovery = max(max_recovery, recovery_days)
                dd_start = None
    
    # 如果还在回撤中
    if in_dd and dd_start is not None:
        recovery_days = (prices.index[-1] - dd_start).days
        max_recovery = max(max_recovery, recovery_days)
    
    return {
        'max_recovery_days': max_recovery,
        'current_recovery_days': current_recovery if in_drawdown else 0,
        'in_drawdown': in_drawdown
    }


def monitor_drawdown(
    symbol: str,
    threshold: float = 0.1,
    end_date: Optional[str] = None
) -> dict:
    """
    监控股票回撤
    
    Args:
        symbol: 股票代码
        threshold: 回撤警戒阈值
        end_date: 结束日期
    
    Returns:
        回撤监控结果
    """
    df = get_ohlcv(symbol, end_date=end_date, count=250)
    
    if df.empty:
        return {
            'symbol': symbol,
            'current_drawdown': np.nan,
            'max_drawdown': np.nan,
            'exceeds_threshold': False,
            'alert': False
        }
    
    prices = df['close']
    drawdown = compute_drawdown(prices)
    current_dd = drawdown.iloc[-1]
    max_dd = drawdown.max()
    
    return {
        'symbol': symbol,
        'current_drawdown': current_dd,
        'max_drawdown': max_dd,
        'exceeds_threshold': current_dd > threshold,
        'alert': current_dd > threshold
    }