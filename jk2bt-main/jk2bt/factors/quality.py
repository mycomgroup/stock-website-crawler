"""
factors/quality.py
质量/杠杆因子模块。

实现：
- debt_to_assets           资产负债率
- equity_to_asset_ratio    权益资产比
- leverage                 杠杆率
- super_quick_ratio        超速动比率
- current_ratio            流动比率
- liquidity                流动性指标

数据来源：AkShare 资产负债表数据
"""

import warnings
from typing import Optional, Union
import pandas as pd
import numpy as np

from .base import (
    global_factor_registry,
    safe_divide,
)
from .fundamentals import (
    _get_balance_sheet,
    _normalize_balance,
)


def _get_balance_data(
    symbol: str, cache_dir: str = "stock_cache", force_update: bool = False
) -> pd.DataFrame:
    """获取并标准化资产负债表数据。"""
    raw = _get_balance_sheet(symbol, cache_dir, force_update)
    return _normalize_balance(raw)


def compute_debt_to_assets(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 debt_to_assets（资产负债率）因子。

    公式：总负债 / 总资产
    """
    df = _get_balance_data(symbol, cache_dir, force_update)

    if df.empty:
        return np.nan

    if "total_liabilities" not in df.columns or "total_assets" not in df.columns:
        return np.nan

    df = df.set_index("date")
    ratio = safe_divide(df["total_liabilities"], df["total_assets"])

    if end_date:
        ratio = ratio[ratio.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        ratio = ratio.tail(count)

    if len(ratio) == 1:
        return float(ratio.iloc[-1])

    ratio.index = ratio.index.strftime("%Y-%m-%d")
    return ratio


def compute_equity_to_asset_ratio(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 equity_to_asset_ratio（权益资产比）因子。

    公式：所有者权益 / 总资产
    """
    df = _get_balance_data(symbol, cache_dir, force_update)

    if df.empty:
        return np.nan

    if "total_equity" not in df.columns or "total_assets" not in df.columns:
        return np.nan

    df = df.set_index("date")
    ratio = safe_divide(df["total_equity"], df["total_assets"])

    if end_date:
        ratio = ratio[ratio.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        ratio = ratio.tail(count)

    if len(ratio) == 1:
        return float(ratio.iloc[-1])

    ratio.index = ratio.index.strftime("%Y-%m-%d")
    return ratio


def compute_leverage(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 leverage（杠杆率）因子。

    公式：总资产 / 净资产
    """
    df = _get_balance_data(symbol, cache_dir, force_update)

    if df.empty:
        return np.nan

    if "total_assets" not in df.columns or "total_equity" not in df.columns:
        return np.nan

    df = df.set_index("date")
    ratio = safe_divide(df["total_assets"], df["total_equity"])

    if end_date:
        ratio = ratio[ratio.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        ratio = ratio.tail(count)

    if len(ratio) == 1:
        return float(ratio.iloc[-1])

    ratio.index = ratio.index.strftime("%Y-%m-%d")
    return ratio


def compute_super_quick_ratio(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 super_quick_ratio（超速动比率）因子。

    公式：(流动资产 - 存货) / 流动负债
    """
    df = _get_balance_data(symbol, cache_dir, force_update)

    if df.empty:
        return np.nan

    required = ["current_assets", "current_liabilities"]
    if not all(c in df.columns for c in required):
        return np.nan

    df = df.set_index("date")
    current_assets = df["current_assets"]
    current_liabilities = df["current_liabilities"]
    inventory = df.get("inventory", pd.Series(0, index=df.index))

    quick_assets = current_assets - inventory
    ratio = safe_divide(quick_assets, current_liabilities)

    if end_date:
        ratio = ratio[ratio.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        ratio = ratio.tail(count)

    if len(ratio) == 1:
        return float(ratio.iloc[-1])

    ratio.index = ratio.index.strftime("%Y-%m-%d")
    return ratio


def compute_current_ratio(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 current_ratio（流动比率）因子。

    公式：流动资产 / 流动负债
    """
    df = _get_balance_data(symbol, cache_dir, force_update)

    if df.empty:
        return np.nan

    if "current_assets" not in df.columns or "current_liabilities" not in df.columns:
        return np.nan

    df = df.set_index("date")
    ratio = safe_divide(df["current_assets"], df["current_liabilities"])

    if end_date:
        ratio = ratio[ratio.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        ratio = ratio.tail(count)

    if len(ratio) == 1:
        return float(ratio.iloc[-1])

    ratio.index = ratio.index.strftime("%Y-%m-%d")
    return ratio


def compute_liquidity(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 liquidity（流动性）因子。

    与 current_ratio 同义。
    """
    return compute_current_ratio(
        symbol, end_date, count, cache_dir, force_update, **kwargs
    )


def compute_long_term_debt_to_asset_ratio(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 long_term_debt_to_asset_ratio（长期负债资产比）因子。

    公式：长期负债 / 总资产
    近似实现：使用非流动负债 / 总资产
    """
    df = _get_balance_data(symbol, cache_dir, force_update)

    if df.empty or "total_assets" not in df.columns:
        return np.nan

    df = df.set_index("date")
    total_assets = df["total_assets"]

    # 尝试获取长期负债或非流动负债
    long_term_debt = df.get("long_term_debt")
    if long_term_debt is None:
        # 近似：总负债 - 流动负债
        total_liab = df.get("total_liabilities", pd.Series(np.nan, index=df.index))
        current_liab = df.get("current_liabilities", pd.Series(0, index=df.index))
        long_term_debt = total_liab - current_liab

    ratio = safe_divide(long_term_debt, total_assets)

    if end_date:
        ratio = ratio[ratio.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        ratio = ratio.tail(count)

    if len(ratio) == 1:
        return float(ratio.iloc[-1])

    ratio.index = ratio.index.strftime("%Y-%m-%d")
    return ratio


def compute_financial_liability(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 financial_liability（金融负债）因子。

    近似实现：有息负债 / 总资产
    有息负债 ≈ 短期借款 + 长期借款 + 应付债券
    简化版本使用：(总负债 - 应付账款 - 预收款项) / 总资产
    """
    df = _get_balance_data(symbol, cache_dir, force_update)

    if df.empty or "total_assets" not in df.columns:
        return np.nan

    df = df.set_index("date")
    total_assets = df["total_assets"]
    total_liab = df.get("total_liabilities", pd.Series(np.nan, index=df.index))

    # 近似：总负债 - 经营性负债
    accounts_payable = df.get("accounts_payable", pd.Series(0, index=df.index))
    financial_liab = total_liab - accounts_payable

    ratio = safe_divide(financial_liab, total_assets)

    if end_date:
        ratio = ratio[ratio.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        ratio = ratio.tail(count)

    if len(ratio) == 1:
        return float(ratio.iloc[-1])

    ratio.index = ratio.index.strftime("%Y-%m-%d")
    return ratio


def _register_factors():
    """向全局注册表注册质量/杠杆因子。"""
    registry = global_factor_registry

    registry.register(
        "debt_to_assets", compute_debt_to_assets, window=1, dependencies=["balance"]
    )
    registry.register(
        "equity_to_asset_ratio",
        compute_equity_to_asset_ratio,
        window=1,
        dependencies=["balance"],
    )
    registry.register("leverage", compute_leverage, window=1, dependencies=["balance"])
    registry.register(
        "super_quick_ratio",
        compute_super_quick_ratio,
        window=1,
        dependencies=["balance"],
    )
    registry.register(
        "current_ratio", compute_current_ratio, window=1, dependencies=["balance"]
    )
    registry.register(
        "liquidity", compute_liquidity, window=1, dependencies=["balance"]
    )
    registry.register(
        "long_term_debt_to_asset_ratio",
        compute_long_term_debt_to_asset_ratio,
        window=1,
        dependencies=["balance"],
    )
    registry.register(
        "financial_liability",
        compute_financial_liability,
        window=1,
        dependencies=["balance"],
    )


_register_factors()


__all__ = [
    "compute_debt_to_assets",
    "compute_equity_to_asset_ratio",
    "compute_leverage",
    "compute_super_quick_ratio",
    "compute_current_ratio",
    "compute_liquidity",
    "compute_long_term_debt_to_asset_ratio",
    "compute_financial_liability",
]
