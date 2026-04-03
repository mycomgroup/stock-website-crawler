"""
factors/growth.py
成长因子模块。

实现：
- np_parent_company_owners_growth_rate   归母净利润增长率
- operating_revenue_growth_rate          营业收入增长率
- earnings_growth                        利润增速（与上述口径统一）

数据来源：AkShare 利润表数据
"""

import warnings
from typing import Optional, Union
import pandas as pd
import numpy as np

from .base import (
    global_factor_registry,
    safe_divide,
    load_factor_cache,
    save_factor_cache,
)

from .fundamentals import (
    _get_income_statement,
    _normalize_income,
)


# =====================================================================
# 成长因子计算函数
# =====================================================================


def compute_np_parent_company_owners_growth_rate(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 np_parent_company_owners_growth_rate（归母净利润增长率）因子。

    公式：(本期归母净利润 - 去年同期归母净利润) / abs(去年同期归母净利润)
    注意：需要同比数据，因此至少需要 5 个报告期（假设为季度）
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    # 归母净利润字段
    np_col = None
    for col in ["net_profit_parent", "归属于母公司股东的净利润", "归母净利润"]:
        if col in income.columns:
            np_col = col
            break
    if np_col is None and "net_profit" in income.columns:
        np_col = "net_profit"

    if np_col is None:
        return np.nan

    income = income.set_index("date")
    net_profit = income[np_col].astype(float)

    # 同比增长率：与去年同期比较（假设报告期为季度，shift(4)）
    growth = safe_divide(net_profit - net_profit.shift(4), np.abs(net_profit.shift(4)))

    if end_date:
        growth = growth[growth.index <= pd.to_datetime(end_date)]

    if count is not None and count > 0:
        growth = growth.tail(count)

    if len(growth) == 1:
        return float(growth.iloc[-1])

    growth.index = growth.index.strftime("%Y-%m-%d")
    return growth


def compute_operating_revenue_growth_rate(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 operating_revenue_growth_rate（营业收入增长率）因子。

    公式：(本期营业收入 - 去年同期营业收入) / abs(去年同期营业收入)
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    rev_col = None
    for col in ["operating_revenue", "营业收入", "营业总收入"]:
        if col in income.columns:
            rev_col = col
            break
    if rev_col is None and "total_revenue" in income.columns:
        rev_col = "total_revenue"

    if rev_col is None:
        return np.nan

    income = income.set_index("date")
    revenue = income[rev_col].astype(float)

    # 同比
    growth = safe_divide(revenue - revenue.shift(4), np.abs(revenue.shift(4)))

    if end_date:
        growth = growth[growth.index <= pd.to_datetime(end_date)]

    if count is not None and count > 0:
        growth = growth.tail(count)

    if len(growth) == 1:
        return float(growth.iloc[-1])

    growth.index = growth.index.strftime("%Y-%m-%d")
    return growth


def compute_earnings_growth(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 earnings_growth（利润增速）因子。

    与 np_parent_company_owners_growth_rate 口径一致。
    """
    return compute_np_parent_company_owners_growth_rate(
        symbol,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
        **kwargs,
    )


# =====================================================================
# 注册因子
# =====================================================================


def _register_factors():
    """向全局注册表注册成长因子。"""
    registry = global_factor_registry

    registry.register(
        "np_parent_company_owners_growth_rate",
        compute_np_parent_company_owners_growth_rate,
        window=5,
        dependencies=["income"],
    )
    registry.register(
        "operating_revenue_growth_rate",
        compute_operating_revenue_growth_rate,
        window=5,
        dependencies=["income"],
    )
    registry.register(
        "earnings_growth", compute_earnings_growth, window=5, dependencies=["income"]
    )


# 模块加载时自动注册
_register_factors()


# =====================================================================
# 模块导出
# =====================================================================

__all__ = [
    "compute_np_parent_company_owners_growth_rate",
    "compute_operating_revenue_growth_rate",
    "compute_earnings_growth",
]
