"""
仓位管理模块
"""
from typing import Dict, Optional
import pandas as pd
import numpy as np


def kelly_criterion(
    win_rate: float,
    win_loss_ratio: float,
    fraction: float = 1.0
) -> float:
    """
    凯利公式计算最优仓位
    
    Args:
        win_rate: 胜率 (0-1)
        win_loss_ratio: 盈亏比
        fraction: 凯利比例（保守使用，如0.5表示半凯利）
    
    Returns:
        建议仓位比例 (0-1)
    
    公式: f = (p * b - q) / b
        p = 胜率
        q = 1 - p = 败率
        b = 盈亏比
    """
    if win_rate <= 0 or win_rate >= 1:
        return 0.0
    if win_loss_ratio <= 0:
        return 0.0
    
    q = 1 - win_rate
    kelly = (win_rate * win_loss_ratio - q) / win_loss_ratio
    
    # 限制在合理范围
    kelly = max(0, min(kelly, 1))
    
    return kelly * fraction


def risk_parity_position(
    volatilities: Dict[str, float],
    target_volatility: float = 0.1
) -> Dict[str, float]:
    """
    风险平价仓位分配
    
    Args:
        volatilities: 各资产波动率字典 {symbol: volatility}
        target_volatility: 目标组合波动率
    
    Returns:
        各资产仓位字典 {symbol: weight}
    """
    if not volatilities:
        return {}
    
    # 移除无效波动率
    valid_vols = {k: v for k, v in volatilities.items() if v > 0}
    
    if not valid_vols:
        return {k: 0.0 for k in volatilities}
    
    # 计算风险倒数
    inv_vols = {k: 1/v for k, v in valid_vols.items()}
    total_inv_vol = sum(inv_vols.values())
    
    # 按风险倒数分配权重
    weights = {k: v / total_inv_vol for k, v in inv_vols.items()}
    
    # 补充缺失资产（波动率为0或无效）
    for k in volatilities:
        if k not in weights:
            weights[k] = 0.0
    
    return weights


def equal_weight_position(symbols: list) -> Dict[str, float]:
    """
    等权重仓位分配
    
    Args:
        symbols: 资产列表
    
    Returns:
        各资产仓位字典
    """
    if not symbols:
        return {}
    
    weight = 1.0 / len(symbols)
    return {s: weight for s in symbols}


def volatility_target_position(
    symbol: str,
    target_volatility: float = 0.15,
    window: int = 20,
    end_date: Optional[str] = None
) -> float:
    """
    波动率目标仓位
    
    Args:
        symbol: 股票代码
        target_volatility: 目标波动率
        window: 波动率计算窗口
        end_date: 结束日期
    
    Returns:
        建议仓位比例
    """
    from .volatility import compute_volatility
    
    vol_data = compute_volatility(symbol, window=window, end_date=end_date)
    current_vol = vol_data['volatility']
    
    if np.isnan(current_vol) or current_vol == 0:
        return 0.0
    
    position = target_volatility / current_vol
    return min(max(position, 0.0), 1.0)


def atr_position_size(
    symbol: str,
    total_capital: float,
    risk_per_trade: float = 0.02,
    atr_multiplier: float = 2.0,
    end_date: Optional[str] = None
) -> dict:
    """
    基于ATR的仓位计算
    
    Args:
        symbol: 股票代码
        total_capital: 总资金
        risk_per_trade: 单笔交易风险比例
        atr_multiplier: ATR倍数（止损距离）
        end_date: 结束日期
    
    Returns:
        包含 position_size, shares, stop_loss 的字典
    """
    from ..risk.volatility import compute_atr_stop_loss
    from ..data.fetcher import get_ohlcv
    
    df = get_ohlcv(symbol, end_date=end_date, count=30)
    
    if df.empty:
        return {
            'position_size': 0,
            'shares': 0,
            'stop_loss': np.nan
        }
    
    current_price = df['close'].iloc[-1]
    stop_loss_data = compute_atr_stop_loss(symbol, multiplier=atr_multiplier, end_date=end_date)
    stop_loss = stop_loss_data['stop_loss_price']
    
    # 计算可承受的最大亏损
    max_loss = total_capital * risk_per_trade
    
    # 计算每手风险
    risk_per_share = current_price - stop_loss
    if risk_per_share <= 0:
        risk_per_share = current_price * 0.1  # 默认10%止损
    
    # 计算股数
    shares = int(max_loss / risk_per_share)
    
    # 计算仓位金额
    position_size = shares * current_price
    
    return {
        'position_size': position_size,
        'shares': shares,
        'stop_loss': stop_loss,
        'risk_per_share': risk_per_share
    }