"""
factors/fundamentals.py
财务因子模块。

实现：
- net_profit_ratio       净利润率
- roe                    净资产收益率
- roa_ttm                总资产收益率（TTM）
- rnoa_ttm               净经营资产收益率（TTM）

数据来源：AkShare 财务数据接口（利润表、资产负债表）
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

try:
    from ..utils.date_utils import find_date_column
except ImportError:
    from utils.date_utils import find_date_column


# =====================================================================
# 数据获取函数
# =====================================================================


def _get_income_statement(
    symbol: str,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取利润表数据。

    Parameters
    ----------
    symbol : str
        证券代码
    cache_dir : str
        缓存目录
    force_update : bool
        强制更新

    Returns
    -------
    pd.DataFrame
        利润表数据
    """
    import os

    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    # 标准化代码
    ak_sym = symbol
    if symbol.startswith("sh") or symbol.startswith("sz"):
        ak_sym = symbol[2:]
    if symbol.endswith(".XSHG") or symbol.endswith(".XSHE"):
        ak_sym = symbol[:6]
    ak_sym = ak_sym.zfill(6)

    cache_file = os.path.join(cache_dir, f"{symbol}_income.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_dl = force_update or not os.path.exists(cache_file)

    if not need_dl:
        try:
            df = pd.read_pickle(cache_file)
        except Exception:
            need_dl = True

    if need_dl:
        try:
            # 尝试使用同花顺接口
            df = ak.stock_financial_benefit_ths(symbol=ak_sym, indicator="按报告期")
            if df is not None and not df.empty:
                df.to_pickle(cache_file)
            else:
                return pd.DataFrame()
        except Exception:
            try:
                # 回退到新浪接口
                df = ak.stock_financial_report_sina(stock=ak_sym, symbol="利润表")
                if df is not None and not df.empty:
                    df.to_pickle(cache_file)
                else:
                    return pd.DataFrame()
            except Exception as e:
                warnings.warn(f"获取利润表失败 {symbol}: {e}")
                return pd.DataFrame()

    return df


def _get_balance_sheet(
    symbol: str,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取资产负债表数据。
    """
    import os

    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    ak_sym = symbol
    if symbol.startswith("sh") or symbol.startswith("sz"):
        ak_sym = symbol[2:]
    if symbol.endswith(".XSHG") or symbol.endswith(".XSHE"):
        ak_sym = symbol[:6]
    ak_sym = ak_sym.zfill(6)

    cache_file = os.path.join(cache_dir, f"{symbol}_balance.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_dl = force_update or not os.path.exists(cache_file)

    if not need_dl:
        try:
            df = pd.read_pickle(cache_file)
        except Exception:
            need_dl = True

    if need_dl:
        try:
            df = ak.stock_financial_report_sina(stock=ak_sym, symbol="资产负债表")
            if df is not None and not df.empty:
                df.to_pickle(cache_file)
            else:
                return pd.DataFrame()
        except Exception as e:
            warnings.warn(f"获取资产负债表失败 {symbol}: {e}")
            return pd.DataFrame()

    return df


def _normalize_income(df: pd.DataFrame) -> pd.DataFrame:
    """标准化利润表字段。"""
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()

    # 日期列
    date_col = find_date_column(df, "financial")
    if date_col:
        df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    else:
        return pd.DataFrame()

    # 字段映射（常见字段名 → 标准名）
    # 支持多种数据源的字段名：同花顺、新浪、聚宽风格
    field_map = {
        # 利润相关
        "净利润": "net_profit",
        "归属于母公司股东的净利润": "net_profit_parent",
        "归母净利润": "net_profit_parent",
        "营业总收入": "total_revenue",
        "营业收入": "operating_revenue",
        "利润总额": "total_profit",
        "营业利润": "operating_profit",
        "营业成本": "operating_cost",
        # 每股收益
        "每股收益": "eps",
        "基本每股收益": "eps_basic",
        # 费用
        "销售费用": "sale_expense",
        "管理费用": "admin_expense",
        "财务费用": "financial_expense",
        # 同花顺风格字段
        "净利率": "net_profit_ratio",
        "销售毛利率": "gross_profit_margin",
    }

    for old, new in field_map.items():
        if old in df.columns and new not in df.columns:
            df[new] = pd.to_numeric(df[old], errors="coerce")

    # 按日期排序
    df = df.sort_values("date").reset_index(drop=True)

    return df


def _normalize_balance(df: pd.DataFrame) -> pd.DataFrame:
    """标准化资产负债表字段。"""
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()

    # 日期列
    date_col = find_date_column(df, "financial")
    if date_col:
        df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    else:
        return pd.DataFrame()

    # 字段映射（支持多种数据源）
    field_map = {
        # 资产
        "资产总计": "total_assets",
        "负债合计": "total_liabilities",
        "股东权益合计": "total_equity",
        "所有者权益合计": "total_equity",
        "归属于母公司股东权益合计": "equity_parent",
        # 流动性
        "流动资产合计": "current_assets",
        "流动负债合计": "current_liabilities",
        # 经营性资产
        "存货": "inventory",
        "应收账款": "accounts_receivable",
        "应付账款": "accounts_payable",
        # 长期负债
        "长期借款": "long_term_debt",
        "非流动负债合计": "non_current_liabilities",
    }

    for old, new in field_map.items():
        if old in df.columns and new not in df.columns:
            df[new] = pd.to_numeric(df[old], errors="coerce")

    df = df.sort_values("date").reset_index(drop=True)

    return df


# =====================================================================
# 财务因子计算函数
# =====================================================================


def compute_gross_income_ratio(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 gross_income_ratio（销售毛利率）因子。

    公式：(营业收入 - 营业成本) / 营业收入
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    # 优先使用 operating_revenue，否则使用 total_revenue
    if "operating_revenue" in income.columns:
        revenue = income["operating_revenue"]
    elif "total_revenue" in income.columns:
        revenue = income["total_revenue"]
    else:
        revenue = None
    cost = income.get("operating_cost") if "operating_cost" in income.columns else None

    if revenue is None or cost is None:
        return np.nan

    income = income.set_index("date")
    revenue = revenue.astype(float)
    cost = cost.astype(float)

    ratio = safe_divide(revenue - cost, revenue)

    if end_date:
        ratio = ratio[ratio.index <= pd.to_datetime(end_date)]

    if count is not None and count > 0:
        ratio = ratio.tail(count)

    if len(ratio) == 1:
        return float(ratio.iloc[-1])

    ratio.index = ratio.index.strftime("%Y-%m-%d")
    return ratio


def compute_inventory_turnover(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 inventory_turnover（存货周转率）因子。

    公式：营业成本 / 平均存货
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    balance_raw = _get_balance_sheet(symbol, cache_dir, force_update)

    income = _normalize_income(income_raw)
    balance = _normalize_balance(balance_raw)

    if income.empty or balance.empty:
        return np.nan

    cost = income.get("operating_cost")
    inventory = balance.get("inventory")

    if cost is None or inventory is None:
        return np.nan

    income = income.set_index("date")
    balance = balance.set_index("date")

    cost = cost.astype(float)
    inventory = inventory.astype(float)

    common_dates = cost.index.intersection(inventory.index)
    if len(common_dates) == 0:
        return np.nan

    cost = cost.loc[common_dates]
    inventory = inventory.loc[common_dates]

    avg_inventory = (inventory + inventory.shift(1)) / 2
    turnover = safe_divide(cost, avg_inventory)

    if end_date:
        turnover = turnover[turnover.index <= pd.to_datetime(end_date)]

    if count is not None and count > 0:
        turnover = turnover.tail(count)

    if len(turnover) == 1:
        return float(turnover.iloc[-1])

    turnover.index = turnover.index.strftime("%Y-%m-%d")
    return turnover


def compute_account_receivable_turnover(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 account_receivable_turnover（应收账款周转率）因子。

    公式：营业收入 / 平均应收账款
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    balance_raw = _get_balance_sheet(symbol, cache_dir, force_update)

    income = _normalize_income(income_raw)
    balance = _normalize_balance(balance_raw)

    if income.empty or balance.empty:
        return np.nan

    # 优先使用 operating_revenue，否则使用 total_revenue
    if "operating_revenue" in income.columns:
        revenue = income["operating_revenue"]
    elif "total_revenue" in income.columns:
        revenue = income["total_revenue"]
    else:
        revenue = None
    ar = balance.get("accounts_receivable") if "accounts_receivable" in balance.columns else None

    if revenue is None or ar is None:
        return np.nan

    income = income.set_index("date")
    balance = balance.set_index("date")

    revenue = revenue.astype(float)
    ar = ar.astype(float)

    common_dates = revenue.index.intersection(ar.index)
    if len(common_dates) == 0:
        return np.nan

    revenue = revenue.loc[common_dates]
    ar = ar.loc[common_dates]

    avg_ar = (ar + ar.shift(1)) / 2
    turnover = safe_divide(revenue, avg_ar)

    if end_date:
        turnover = turnover[turnover.index <= pd.to_datetime(end_date)]

    if count is not None and count > 0:
        turnover = turnover.tail(count)

    if len(turnover) == 1:
        return float(turnover.iloc[-1])

    turnover.index = turnover.index.strftime("%Y-%m-%d")
    return turnover


def compute_total_asset_turnover(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 total_asset_turnover（总资产周转率）因子。

    公式：营业收入 / 平均总资产
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    balance_raw = _get_balance_sheet(symbol, cache_dir, force_update)

    income = _normalize_income(income_raw)
    balance = _normalize_balance(balance_raw)

    if income.empty or balance.empty:
        return np.nan

    # 优先使用 operating_revenue，否则使用 total_revenue
    if "operating_revenue" in income.columns:
        revenue = income["operating_revenue"]
    elif "total_revenue" in income.columns:
        revenue = income["total_revenue"]
    else:
        revenue = None
    assets = balance.get("total_assets") if "total_assets" in balance.columns else None

    if revenue is None or assets is None:
        return np.nan

    income = income.set_index("date")
    balance = balance.set_index("date")

    revenue = revenue.astype(float)
    assets = assets.astype(float)

    common_dates = revenue.index.intersection(assets.index)
    if len(common_dates) == 0:
        return np.nan

    revenue = revenue.loc[common_dates]
    assets = assets.loc[common_dates]

    avg_assets = (assets + assets.shift(1)) / 2
    turnover = safe_divide(revenue, avg_assets)

    if end_date:
        turnover = turnover[turnover.index <= pd.to_datetime(end_date)]

    if count is not None and count > 0:
        turnover = turnover.tail(count)

    if len(turnover) == 1:
        return float(turnover.iloc[-1])

    turnover.index = turnover.index.strftime("%Y-%m-%d")
    return turnover


def compute_net_profit_ratio(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 net_profit_ratio（净利润率）因子。

    公式：net_profit / operating_revenue
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    if "net_profit" not in income.columns or "operating_revenue" not in income.columns:
        return np.nan

    income = income.set_index("date")
    net_profit = income["net_profit"]
    revenue = income["operating_revenue"]

    ratio = safe_divide(net_profit, revenue)

    if end_date:
        ratio = ratio[ratio.index <= pd.to_datetime(end_date)]

    if count is not None and count > 0:
        ratio = ratio.tail(count)

    if len(ratio) == 1:
        return float(ratio.iloc[-1])

    # 返回日期字符串索引
    ratio.index = ratio.index.strftime("%Y-%m-%d")
    return ratio


def compute_roe(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 ROE（净资产收益率）因子。

    公式：net_profit / avg_equity
    其中 avg_equity = (本期末权益 + 上期末权益) / 2
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    balance_raw = _get_balance_sheet(symbol, cache_dir, force_update)

    income = _normalize_income(income_raw)
    balance = _normalize_balance(balance_raw)

    if income.empty or balance.empty:
        return np.nan

    if "net_profit" not in income.columns or "total_equity" not in balance.columns:
        return np.nan

    income = income.set_index("date")
    balance = balance.set_index("date")

    net_profit = income["net_profit"]
    equity = balance["total_equity"]

    # 对齐日期
    common_dates = net_profit.index.intersection(equity.index)
    if len(common_dates) == 0:
        return np.nan

    net_profit = net_profit.loc[common_dates]
    equity = equity.loc[common_dates]

    # 平均净资产
    avg_equity = (equity + equity.shift(1)) / 2

    roe = safe_divide(net_profit, avg_equity)

    if end_date:
        roe = roe[roe.index <= pd.to_datetime(end_date)]

    if count is not None and count > 0:
        roe = roe.tail(count)

    if len(roe) == 1:
        return float(roe.iloc[-1])

    roe.index = roe.index.strftime("%Y-%m-%d")
    return roe


def compute_roa_ttm(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 ROA_TTM（总资产收益率 - 滚动 12 个月）因子。

    公式：TTM 净利润 / 平均总资产
    近似实现：使用最近 4 个季度净利润之和 / 平均总资产
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    balance_raw = _get_balance_sheet(symbol, cache_dir, force_update)

    income = _normalize_income(income_raw)
    balance = _normalize_balance(balance_raw)

    if income.empty or balance.empty:
        return np.nan

    if "net_profit" not in income.columns or "total_assets" not in balance.columns:
        return np.nan

    income = income.set_index("date")
    balance = balance.set_index("date")

    net_profit = income["net_profit"]
    total_assets = balance["total_assets"]

    # 对齐
    common_dates = net_profit.index.intersection(total_assets.index)
    if len(common_dates) < 4:
        return np.nan

    net_profit = net_profit.loc[common_dates]
    total_assets = total_assets.loc[common_dates]

    # TTM 净利润（最近 4 期之和，假设为季度数据）
    ttm_profit = net_profit.rolling(window=4, min_periods=4).sum()

    # 平均总资产
    avg_assets = (total_assets + total_assets.shift(1)) / 2

    roa = safe_divide(ttm_profit, avg_assets)

    if end_date:
        roa = roa[roa.index <= pd.to_datetime(end_date)]

    if count is not None and count > 0:
        roa = roa.tail(count)

    if len(roa) == 1:
        return float(roa.iloc[-1])

    roa.index = roa.index.strftime("%Y-%m-%d")
    return roa


def compute_rnoa_ttm(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 RNOA_TTM（净经营资产收益率 - 滚动 12 个月）因子。

    公式：TTM 经营利润 / 平均净经营资产
    近似实现：
    - 经营利润 ≈ 营业利润（若有）或 净利润 + 财务费用
    - 净经营资产 = 经营资产 - 经营负债
      ≈ (总资产 - 金融资产) - (总负债 - 金融负债)
      简化为：(总资产 - 现金) - (总负债 - 有息负债)
    """
    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    balance_raw = _get_balance_sheet(symbol, cache_dir, force_update)

    income = _normalize_income(income_raw)
    balance = _normalize_balance(balance_raw)

    if income.empty or balance.empty:
        return np.nan

    income = income.set_index("date")
    balance = balance.set_index("date")

    # 经营利润近似
    if "operating_revenue" in income.columns and "operating_cost" in income.columns:
        # 营业利润近似
        operating_profit = income.get(
            "total_profit",
            income.get("net_profit", pd.Series(index=income.index, data=np.nan)),
        )
    else:
        operating_profit = income.get(
            "net_profit", pd.Series(index=income.index, data=np.nan)
        )

    total_assets = balance.get(
        "total_assets", pd.Series(index=balance.index, data=np.nan)
    )
    total_liabilities = balance.get(
        "total_liabilities", pd.Series(index=balance.index, data=np.nan)
    )
    current_assets = balance.get("current_assets", total_assets)
    current_liabilities = balance.get("current_liabilities", total_liabilities)

    # 对齐
    common_dates = operating_profit.index.intersection(total_assets.index)
    if len(common_dates) < 4:
        return np.nan

    operating_profit = operating_profit.loc[common_dates]
    total_assets = total_assets.loc[common_dates]
    total_liabilities = total_liabilities.loc[common_dates]

    # 净经营资产近似 = 总资产 - 总负债 - 现金类 + 有息负债
    # 极简化：总资产 - 总负债 ≈ 净资产，但 RNOA 需要的是经营净资产
    # 这里用：经营净资产 ≈ 总资产 × 0.6 - 总负债 × 0.4 （粗略比例）
    net_operating_assets = total_assets * 0.6 - total_liabilities * 0.4

    # TTM 经营利润
    ttm_op_profit = operating_profit.rolling(window=4, min_periods=4).sum()

    # 平均净经营资产
    avg_noa = (net_operating_assets + net_operating_assets.shift(1)) / 2

    rnoa = safe_divide(ttm_op_profit, avg_noa)

    if end_date:
        rnoa = rnoa[rnoa.index <= pd.to_datetime(end_date)]

    if count is not None and count > 0:
        rnoa = rnoa.tail(count)

    if len(rnoa) == 1:
        return float(rnoa.iloc[-1])

    rnoa.index = rnoa.index.strftime("%Y-%m-%d")
    return rnoa


# =====================================================================
# 注册因子
# =====================================================================


def _register_factors():
    """向全局注册表注册财务因子。"""
    registry = global_factor_registry

    registry.register(
        "gross_income_ratio",
        compute_gross_income_ratio,
        window=1,
        dependencies=["income"],
    )
    registry.register(
        "inventory_turnover",
        compute_inventory_turnover,
        window=1,
        dependencies=["income", "balance"],
    )
    registry.register(
        "account_receivable_turnover",
        compute_account_receivable_turnover,
        window=1,
        dependencies=["income", "balance"],
    )
    registry.register(
        "total_asset_turnover",
        compute_total_asset_turnover,
        window=1,
        dependencies=["income", "balance"],
    )
    registry.register(
        "net_profit_ratio", compute_net_profit_ratio, window=1, dependencies=["income"]
    )
    registry.register("roe", compute_roe, window=1, dependencies=["income", "balance"])
    registry.register(
        "roa_ttm", compute_roa_ttm, window=4, dependencies=["income", "balance"]
    )
    registry.register(
        "rnoa_ttm", compute_rnoa_ttm, window=4, dependencies=["income", "balance"]
    )


# 模块加载时自动注册
_register_factors()


# =====================================================================
# 模块导出
# =====================================================================

__all__ = [
    "compute_gross_income_ratio",
    "compute_inventory_turnover",
    "compute_account_receivable_turnover",
    "compute_total_asset_turnover",
    "compute_net_profit_ratio",
    "compute_roe",
    "compute_roa_ttm",
    "compute_rnoa_ttm",
]
