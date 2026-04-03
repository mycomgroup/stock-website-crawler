"""
risk/position_sizing.py
仓位管理模块。

用途：计算各标的的目标仓位。
"""

import warnings
from typing import Optional, Union, Dict, List
import pandas as pd
import numpy as np

try:
    from .volatility import compute_volatility
except ImportError:
    from risk.volatility import compute_volatility


# =====================================================================
# 凯利公式
# =====================================================================


def kelly_criterion(
    win_rate: float,
    win_loss_ratio: float,
    fraction: float = 1.0,
) -> float:
    """
    凯利公式计算最优仓位。

    f = p - (1-p)/b
    其中 p=胜率, b=盈亏比

    Parameters
    ----------
    win_rate : float
        胜率（0-1之间）
    win_loss_ratio : float
        盈亏比（平均盈利/平均亏损）
    fraction : float
        凯利比例（默认1.0=全凯利，0.5=半凯利）

    Returns
    -------
    float
        最优仓位比例
    """
    if win_rate <= 0 or win_rate >= 1:
        return 0.0

    if win_loss_ratio <= 0:
        return 0.0

    # 凯利公式
    kelly = win_rate - (1 - win_rate) / win_loss_ratio

    # 应用比例
    kelly = kelly * fraction

    # 限制范围
    return max(0.0, min(kelly, 1.0))


# =====================================================================
# 风险平价
# =====================================================================


def risk_parity_position(
    volatilities: Dict[str, float],
    target_vol: float = 0.10,
    max_position: float = 1.0,
) -> Dict[str, float]:
    """
    风险平价仓位计算。

    根据各资产的波动率倒数分配仓位，使每个资产的风险贡献相等。

    Parameters
    ----------
    volatilities : dict
        {symbol: volatility}
    target_vol : float
        目标组合波动率
    max_position : float
        单个资产最大仓位

    Returns
    -------
    dict
        {symbol: position_weight}
    """
    if not volatilities:
        return {}

    # 计算波动率倒数
    inv_vols = {}
    for symbol, vol in volatilities.items():
        if vol > 0:
            inv_vols[symbol] = 1 / vol
        else:
            inv_vols[symbol] = 0

    # 归一化
    total_inv_vol = sum(inv_vols.values())
    if total_inv_vol == 0:
        return {s: 1 / len(volatilities) for s in volatilities}

    positions = {}
    for symbol, inv_vol in inv_vols.items():
        pos = inv_vol / total_inv_vol
        positions[symbol] = min(pos, max_position)

    return positions


# =====================================================================
# 等风险贡献
# =====================================================================


def equal_risk_contribution(
    symbols: List[str],
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> Dict[str, float]:
    """
    等风险贡献仓位。

    每个资产的风险贡献相等。

    Parameters
    ----------
    symbols : list
        股票代码列表
    end_date : str, optional
        截止日期

    Returns
    -------
    dict
        {symbol: position_weight}
    """
    if not symbols:
        return {}

    # 计算各资产波动率
    vols = {}
    for symbol in symbols:
        try:
            vol = compute_volatility(
                symbol,
                window=20,
                annualized=True,
                end_date=end_date,
                cache_dir=cache_dir,
                force_update=force_update,
            )
            if not np.isnan(vol) and vol > 0:
                vols[symbol] = vol
        except Exception as e:
            warnings.warn(f"{symbol} 波动率计算失败: {e}")

    if not vols:
        return {s: 1 / len(symbols) for s in symbols}

    return risk_parity_position(vols)


# =====================================================================
# 波动率目标仓位
# =====================================================================


def volatility_target_position(
    symbol: str,
    target_vol: float = 0.15,
    base_position: float = 1.0,
    window: int = 20,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> Dict:
    """
    波动率目标仓位计算。

    根据目标波动率调整仓位。

    Parameters
    ----------
    symbol : str
        股票代码
    target_vol : float
        目标波动率
    base_position : float
        基础仓位
    window : int
        波动率计算窗口
    end_date : str, optional
        截止日期

    Returns
    -------
    dict
        仓位计算结果
    """
    from .volatility import compute_volatility_adjusted_position

    return compute_volatility_adjusted_position(
        symbol,
        base_position=base_position,
        target_vol=target_vol,
        window=window,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# =====================================================================
# ATR仓位计算
# =====================================================================


def atr_based_position_size(
    symbol: str,
    total_capital: float,
    risk_per_trade: float = 0.02,
    atr_window: int = 14,
    atr_multiplier: float = 2.0,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> Dict:
    """
    基于ATR的仓位计算。

    根据ATR确定每股风险，结合账户风险比例计算仓位。

    Parameters
    ----------
    symbol : str
        股票代码
    total_capital : float
        总资金
    risk_per_trade : float
        单笔交易风险比例（默认2%）
    atr_window : int
        ATR窗口
    atr_multiplier : float
        ATR倍数
    end_date : str, optional
        截止日期

    Returns
    -------
    dict
        仓位计算结果
    """
    from .volatility import compute_atr_based_stop_loss

    stop_info = compute_atr_based_stop_loss(
        symbol,
        atr_window=atr_window,
        atr_multiplier=atr_multiplier,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
    )

    if np.isnan(stop_info["risk_per_share"]) or stop_info["risk_per_share"] <= 0:
        return {
            "symbol": symbol,
            "shares": 0,
            "position_value": 0,
            "risk_amount": 0,
            "current_price": stop_info["current_price"],
        }

    # 计算可承受的风险金额
    risk_amount = total_capital * risk_per_trade

    # 计算可买入股数
    shares = int(risk_amount / stop_info["risk_per_share"])

    # 计算仓位市值
    position_value = shares * stop_info["current_price"]

    return {
        "symbol": symbol,
        "shares": shares,
        "position_value": position_value,
        "risk_amount": risk_amount,
        "current_price": stop_info["current_price"],
        "stop_loss_price": stop_info["stop_loss_price"],
        "atr_value": stop_info["atr_value"],
    }


# =====================================================================
# 组合仓位优化
# =====================================================================


def optimize_portfolio_positions(
    symbols: List[str],
    total_capital: float,
    method: str = "risk_parity",
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> Dict:
    """
    优化组合仓位。

    Parameters
    ----------
    symbols : list
        股票代码列表
    total_capital : float
        总资金
    method : str
        优化方法：
        - 'equal_weight': 等权重
        - 'risk_parity': 风险平价
        - 'min_variance': 最小方差（待实现）
    end_date : str, optional
        截止日期

    Returns
    -------
    dict
        组合仓位配置
    """
    if not symbols:
        return {"positions": {}, "total_capital": total_capital}

    if method == "equal_weight":
        positions = {s: 1 / len(symbols) for s in symbols}
    elif method == "risk_parity":
        positions = equal_risk_contribution(
            symbols,
            end_date=end_date,
            cache_dir=cache_dir,
            force_update=force_update,
        )
    else:
        positions = {s: 1 / len(symbols) for s in symbols}

    # 计算各资产分配金额
    allocation = {
        symbol: {
            "weight": weight,
            "capital": total_capital * weight,
        }
        for symbol, weight in positions.items()
    }

    return {
        "positions": positions,
        "allocation": allocation,
        "total_capital": total_capital,
        "method": method,
    }


__all__ = [
    "kelly_criterion",
    "risk_parity_position",
    "equal_risk_contribution",
    "volatility_target_position",
    "atr_based_position_size",
    "optimize_portfolio_positions",
]