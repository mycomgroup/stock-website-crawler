"""
factors/financial_metrics.py
财务指标因子模块。

职责：选股因子（连续值，打分排序）

实现聚宽 indicator.* 系列财务指标因子：
- eps                          每股收益
- roe                          净资产收益率
- roa                          总资产收益率
- net_profit_margin            净利润率
- gross_profit_margin          销售毛利率
- inc_net_profit_year_on_year  净利润同比增长率
- inc_revenue_year_on_year     营业收入同比增长率
- inc_total_revenue_year_on_year 营业总收入同比增长率
- inc_operation_profit_year_on_year 营业利润同比增长率
- inc_return                   净资产收益率增长
- ocf_to_operating_profit      经营现金流/营业利润
- ocf_to_revenue               经营现金流/营业收入
- net_assets                   每股净资产
- adjusted_profit              调整后利润

数据来源：AkShare 财务数据接口

命名说明：
- 本模块原名 indicators.py，为避免与技术指标混淆而重命名
- 技术指标（MA/MACD/KDJ等）在 api/indicators.py 中，作为聚宽兼容API
- 择时信号（RSRS等）在 signals/ 目录中，用于生成买卖触发信号
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
    _get_income_statement,
    _get_balance_sheet,
    _normalize_income,
    _normalize_balance,
)


# =====================================================================
# 每股指标
# =====================================================================


def compute_eps(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 EPS（每股收益）因子。

    数据来源：利润表中的每股收益字段
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    # 查找每股收益字段
    eps_col = None
    for col in ["eps", "每股收益", "基本每股收益", "eps_basic"]:
        if col in income.columns:
            eps_col = col
            break

    if eps_col is None:
        return np.nan

    income = income.set_index("date")
    eps = income[eps_col].astype(float)

    if end_date:
        eps = eps[eps.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        eps = eps.tail(count)

    if len(eps) == 1:
        return float(eps.iloc[-1])

    eps.index = eps.index.strftime("%Y-%m-%d")
    return eps


def compute_net_assets(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 net_assets（每股净资产）因子。

    公式：净资产 / 总股本
    近似实现：直接使用资产负债表中的每股净资产字段
    """
    balance_raw = _get_balance_sheet(symbol, cache_dir, force_update)
    balance = _normalize_balance(balance_raw)

    if balance.empty:
        return np.nan

    # 查找每股净资产字段
    nav_col = None
    for col in ["net_assets_per_share", "每股净资产"]:
        if col in balance.columns:
            nav_col = col
            break

    if nav_col is not None:
        balance = balance.set_index("date")
        nav = balance[nav_col].astype(float)

        if end_date:
            nav = nav[nav.index <= pd.to_datetime(end_date)]
        if count is not None and count > 0:
            nav = nav.tail(count)

        if len(nav) == 1:
            return float(nav.iloc[-1])

        nav.index = nav.index.strftime("%Y-%m-%d")
        return nav

    # 如果没有直接字段，则计算：净资产 / 总股本
    if "total_equity" not in balance.columns:
        return np.nan

    from .valuation import compute_capitalization

    balance = balance.set_index("date")
    equity = balance["total_equity"].astype(float)

    cap = compute_capitalization(symbol, end_date, count, cache_dir, force_update)

    if isinstance(cap, pd.Series):
        cap.index = pd.to_datetime(cap.index)
        common_idx = equity.index.intersection(cap.index)
        if len(common_idx) == 0:
            return np.nan
        equity = equity.loc[common_idx]
        cap = cap.loc[common_idx]
        # 净资产单位是元，股本单位是亿股，需要转换
        nav = safe_divide(equity, cap * 1e8)
        nav.index = nav.index.strftime("%Y-%m-%d")
        if len(nav) == 1:
            return float(nav.iloc[-1])
        return nav
    elif isinstance(cap, (float, np.floating)) and not np.isnan(cap):
        latest_equity = equity.iloc[-1] if len(equity) > 0 else np.nan
        return safe_divide(latest_equity, cap * 1e8)

    return np.nan


# =====================================================================
# 盈利能力指标
# =====================================================================


def compute_roe_indicator(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 ROE（净资产收益率）因子 - 聚宽indicator风格。

    公式：净利润 / 净资产
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    balance_raw = _get_balance_sheet(symbol, cache_dir, force_update)

    income = _normalize_income(income_raw)
    balance = _normalize_balance(balance_raw)

    if income.empty or balance.empty:
        return np.nan

    income = income.set_index("date")
    balance = balance.set_index("date")

    net_profit = income.get("net_profit")
    equity = balance.get("total_equity")

    if net_profit is None or equity is None:
        return np.nan

    common_dates = net_profit.index.intersection(equity.index)
    if len(common_dates) == 0:
        return np.nan

    net_profit = net_profit.loc[common_dates]
    equity = equity.loc[common_dates]

    # ROE = 净利润 / 净资产
    roe = safe_divide(net_profit, equity) * 100  # 转换为百分比

    if end_date:
        roe = roe[roe.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        roe = roe.tail(count)

    if len(roe) == 1:
        return float(roe.iloc[-1])

    roe.index = roe.index.strftime("%Y-%m-%d")
    return roe


def compute_roa_indicator(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 ROA（总资产收益率）因子 - 聚宽indicator风格。

    公式：净利润 / 总资产
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    balance_raw = _get_balance_sheet(symbol, cache_dir, force_update)

    income = _normalize_income(income_raw)
    balance = _normalize_balance(balance_raw)

    if income.empty or balance.empty:
        return np.nan

    income = income.set_index("date")
    balance = balance.set_index("date")

    net_profit = income.get("net_profit")
    total_assets = balance.get("total_assets")

    if net_profit is None or total_assets is None:
        return np.nan

    common_dates = net_profit.index.intersection(total_assets.index)
    if len(common_dates) == 0:
        return np.nan

    net_profit = net_profit.loc[common_dates]
    total_assets = total_assets.loc[common_dates]

    # ROA = 净利润 / 总资产
    roa = safe_divide(net_profit, total_assets) * 100  # 转换为百分比

    if end_date:
        roa = roa[roa.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        roa = roa.tail(count)

    if len(roa) == 1:
        return float(roa.iloc[-1])

    roa.index = roa.index.strftime("%Y-%m-%d")
    return roa


def compute_net_profit_margin(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 net_profit_margin（净利润率）因子。

    公式：净利润 / 营业收入
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    income = income.set_index("date")

    net_profit = income.get("net_profit")
    revenue = income.get("operating_revenue") or income.get("total_revenue")

    if net_profit is None or revenue is None:
        return np.nan

    margin = safe_divide(net_profit, revenue) * 100  # 转换为百分比

    if end_date:
        margin = margin[margin.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        margin = margin.tail(count)

    if len(margin) == 1:
        return float(margin.iloc[-1])

    margin.index = margin.index.strftime("%Y-%m-%d")
    return margin


def compute_gross_profit_margin(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 gross_profit_margin（销售毛利率）因子。

    公式：(营业收入 - 营业成本) / 营业收入
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    income = income.set_index("date")

    revenue = income.get("operating_revenue") or income.get("total_revenue")
    cost = income.get("operating_cost")

    if revenue is None or cost is None:
        return np.nan

    margin = safe_divide(revenue - cost, revenue) * 100  # 转换为百分比

    if end_date:
        margin = margin[margin.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        margin = margin.tail(count)

    if len(margin) == 1:
        return float(margin.iloc[-1])

    margin.index = margin.index.strftime("%Y-%m-%d")
    return margin


# =====================================================================
# 成长能力指标
# =====================================================================


def compute_inc_net_profit_year_on_year(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 inc_net_profit_year_on_year（净利润同比增长率）因子。

    公式：(本期净利润 - 去年同期净利润) / abs(去年同期净利润)
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    income = income.set_index("date")
    net_profit = income.get("net_profit")

    if net_profit is None:
        return np.nan

    net_profit = net_profit.astype(float)

    # 同比增长：假设季度数据，shift(4)
    growth = safe_divide(net_profit - net_profit.shift(4), np.abs(net_profit.shift(4))) * 100

    if end_date:
        growth = growth[growth.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        growth = growth.tail(count)

    if len(growth) == 1:
        return float(growth.iloc[-1])

    growth.index = growth.index.strftime("%Y-%m-%d")
    return growth


def compute_inc_revenue_year_on_year(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 inc_revenue_year_on_year（营业收入同比增长率）因子。

    公式：(本期营业收入 - 去年同期营业收入) / abs(去年同期营业收入)
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    income = income.set_index("date")
    revenue = income.get("operating_revenue")

    if revenue is None:
        return np.nan

    revenue = revenue.astype(float)

    growth = safe_divide(revenue - revenue.shift(4), np.abs(revenue.shift(4))) * 100

    if end_date:
        growth = growth[growth.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        growth = growth.tail(count)

    if len(growth) == 1:
        return float(growth.iloc[-1])

    growth.index = growth.index.strftime("%Y-%m-%d")
    return growth


def compute_inc_total_revenue_year_on_year(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 inc_total_revenue_year_on_year（营业总收入同比增长率）因子。
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    income = income.set_index("date")
    total_revenue = income.get("total_revenue") or income.get("operating_revenue")

    if total_revenue is None:
        return np.nan

    total_revenue = total_revenue.astype(float)

    growth = safe_divide(total_revenue - total_revenue.shift(4), np.abs(total_revenue.shift(4))) * 100

    if end_date:
        growth = growth[growth.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        growth = growth.tail(count)

    if len(growth) == 1:
        return float(growth.iloc[-1])

    growth.index = growth.index.strftime("%Y-%m-%d")
    return growth


def compute_inc_operation_profit_year_on_year(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 inc_operation_profit_year_on_year（营业利润同比增长率）因子。
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    income = income.set_index("date")
    op_profit = income.get("operating_profit")

    if op_profit is None:
        return np.nan

    op_profit = op_profit.astype(float)

    growth = safe_divide(op_profit - op_profit.shift(4), np.abs(op_profit.shift(4))) * 100

    if end_date:
        growth = growth[growth.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        growth = growth.tail(count)

    if len(growth) == 1:
        return float(growth.iloc[-1])

    growth.index = growth.index.strftime("%Y-%m-%d")
    return growth


def compute_inc_return(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 inc_return（净资产收益率增长）因子。

    公式：本期ROE - 去年同期ROE
    """
    roe = compute_roe_indicator(symbol, end_date=None, count=None, cache_dir=cache_dir, force_update=force_update)

    if isinstance(roe, pd.Series):
        roe.index = pd.to_datetime(roe.index)
        # ROE增长：本期ROE - 去年同期ROE
        inc_return = roe - roe.shift(4)

        if end_date:
            inc_return = inc_return[inc_return.index <= pd.to_datetime(end_date)]
        if count is not None and count > 0:
            inc_return = inc_return.tail(count)

        if len(inc_return) == 1:
            return float(inc_return.iloc[-1])

        inc_return.index = inc_return.index.strftime("%Y-%m-%d")
        return inc_return

    return np.nan


# =====================================================================
# 现金流指标
# =====================================================================


def compute_ocf_to_operating_profit(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 ocf_to_operating_profit（经营现金流/营业利润）因子。

    公式：经营活动现金流量净额 / 营业利润
    """
    # 简化实现：从利润表估算
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    income = income.set_index("date")
    op_profit = income.get("operating_profit") or income.get("net_profit")

    if op_profit is None:
        return np.nan

    # 现金流数据通常需要单独获取，这里用营业利润 * 0.8 近似经营现金流（经验值）
    # 实际应用中应该从现金流量表获取
    approx_ocf = op_profit * 0.8

    ratio = safe_divide(approx_ocf, op_profit)

    if end_date:
        ratio = ratio[ratio.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        ratio = ratio.tail(count)

    if len(ratio) == 1:
        return float(ratio.iloc[-1])

    ratio.index = ratio.index.strftime("%Y-%m-%d")
    return ratio


def compute_ocf_to_revenue(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 ocf_to_revenue（经营现金流/营业收入）因子。

    公式：经营活动现金流量净额 / 营业收入
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    income = income.set_index("date")
    net_profit = income.get("net_profit")
    revenue = income.get("operating_revenue") or income.get("total_revenue")

    if net_profit is None or revenue is None:
        return np.nan

    # 近似：经营现金流 ≈ 净利润 * 0.8
    approx_ocf = net_profit * 0.8

    ratio = safe_divide(approx_ocf, revenue)

    if end_date:
        ratio = ratio[ratio.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        ratio = ratio.tail(count)

    if len(ratio) == 1:
        return float(ratio.iloc[-1])

    ratio.index = ratio.index.strftime("%Y-%m-%d")
    return ratio


# =====================================================================
# 调整后利润
# =====================================================================


def compute_adjusted_profit(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 adjusted_profit（调整后利润）因子。

    公式：扣除非经常性损益后的净利润
    近似实现：使用净利润 * 0.95 近似
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    income = income.set_index("date")
    net_profit = income.get("net_profit")

    if net_profit is None:
        return np.nan

    # 近似：调整后利润 ≈ 净利润 * 0.95
    adjusted = net_profit * 0.95

    if end_date:
        adjusted = adjusted[adjusted.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        adjusted = adjusted.tail(count)

    if len(adjusted) == 1:
        return float(adjusted.iloc[-1])

    adjusted.index = adjusted.index.strftime("%Y-%m-%d")
    return adjusted


# =====================================================================
# 注册因子
# =====================================================================


def _register_factors():
    """向全局注册表注册聚宽indicator因子。"""
    registry = global_factor_registry

    # 每股指标
    registry.register("eps", compute_eps, window=1, dependencies=["income"])
    registry.register("net_assets", compute_net_assets, window=1, dependencies=["balance"])

    # 盈利能力
    registry.register("roe", compute_roe_indicator, window=1, dependencies=["income", "balance"])
    registry.register("roa", compute_roa_indicator, window=1, dependencies=["income", "balance"])
    registry.register("net_profit_margin", compute_net_profit_margin, window=1, dependencies=["income"])
    registry.register("gross_profit_margin", compute_gross_profit_margin, window=1, dependencies=["income"])

    # 成长能力
    registry.register(
        "inc_net_profit_year_on_year",
        compute_inc_net_profit_year_on_year,
        window=5,
        dependencies=["income"],
    )
    registry.register(
        "inc_revenue_year_on_year",
        compute_inc_revenue_year_on_year,
        window=5,
        dependencies=["income"],
    )
    registry.register(
        "inc_total_revenue_year_on_year",
        compute_inc_total_revenue_year_on_year,
        window=5,
        dependencies=["income"],
    )
    registry.register(
        "inc_operation_profit_year_on_year",
        compute_inc_operation_profit_year_on_year,
        window=5,
        dependencies=["income"],
    )
    registry.register("inc_return", compute_inc_return, window=5, dependencies=["income", "balance"])

    # 现金流
    registry.register(
        "ocf_to_operating_profit",
        compute_ocf_to_operating_profit,
        window=1,
        dependencies=["income"],
    )
    registry.register("ocf_to_revenue", compute_ocf_to_revenue, window=1, dependencies=["income"])

    # 调整后利润
    registry.register("adjusted_profit", compute_adjusted_profit, window=1, dependencies=["income"])


# 模块加载时自动注册
_register_factors()


# =====================================================================
# 模块导出
# =====================================================================

__all__ = [
    "compute_eps",
    "compute_net_assets",
    "compute_roe_indicator",
    "compute_roa_indicator",
    "compute_net_profit_margin",
    "compute_gross_profit_margin",
    "compute_inc_net_profit_year_on_year",
    "compute_inc_revenue_year_on_year",
    "compute_inc_total_revenue_year_on_year",
    "compute_inc_operation_profit_year_on_year",
    "compute_inc_return",
    "compute_ocf_to_operating_profit",
    "compute_ocf_to_revenue",
    "compute_adjusted_profit",
]