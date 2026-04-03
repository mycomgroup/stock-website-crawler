"""
market_data/fund_of.py
场外基金（OF）净值数据获取模块。

场外基金不在交易所交易，只有每日净值数据。
本模块使用 akshare 的 fund_etf_fund_info_em 接口获取历史净值。

标准字段：
- datetime: 净值日期
- unit_nav: 单位净值
- acc_nav: 累计净值
- daily_growth_rate: 日增长率
- purchase_status: 申购状态
- redeem_status: 赎回状态
"""

import logging
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)


def standardize_fund_nav(df: pd.DataFrame) -> pd.DataFrame:
    """
    标准化场外基金净值数据。

    参数
    ----
    df : pd.DataFrame
        原始净值数据

    返回
    ----
    pd.DataFrame
        标准化后的净值数据，字段：
        datetime, unit_nav, acc_nav, daily_growth_rate, purchase_status, redeem_status
    """
    df = df.copy()

    columns_map = {
        "净值日期": "datetime",
        "单位净值": "unit_nav",
        "累计净值": "acc_nav",
        "日增长率": "daily_growth_rate",
        "申购状态": "purchase_status",
        "赎回状态": "redeem_status",
    }

    for old_col, new_col in columns_map.items():
        if old_col in df.columns:
            df[new_col] = df[old_col]

    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
        df = df.dropna(subset=["datetime"])
        df = df.sort_values("datetime").reset_index(drop=True)

    numeric_cols = ["unit_nav", "acc_nav", "daily_growth_rate"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    result_cols = [
        "datetime",
        "unit_nav",
        "acc_nav",
        "daily_growth_rate",
        "purchase_status",
        "redeem_status",
    ]
    df = df[[col for col in result_cols if col in df.columns]]

    return df


def get_fund_of_nav(
    symbol: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取场外基金历史净值数据。

    参数
    ----
    symbol : str
        基金代码，如 '000001'（华夏成长混合）
    start : str, optional
        资始日期 'YYYY-MM-DD'，不指定则返回全部历史
    end : str, optional
        结束日期 'YYYY-MM-DD'，不指定则返回至最新
    force_update : bool
        强制重新获取（暂无缓存机制）

    返回
    ----
    pd.DataFrame
        标准化后的净值数据

    异常
    ----
    ValueError
        数据获取失败或返回空数据
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    try:
        logger.info(f"{symbol}: 从 akshare 获取场外基金净值数据")
        raw_df = ak.fund_etf_fund_info_em(fund=symbol)

        if raw_df is None or raw_df.empty:
            raise ValueError(f"{symbol}: 基金净值数据为空")

        logger.info(f"{symbol}: 成功获取净值数据，共 {len(raw_df)} 条记录")

        df = standardize_fund_nav(raw_df)

        if start is not None:
            df = df[df["datetime"] >= pd.to_datetime(start)]
        if end is not None:
            df = df[df["datetime"] <= pd.to_datetime(end)]

        if df.empty:
            logger.warning(f"{symbol}: 在指定时间范围内无数据")
        else:
            logger.info(f"{symbol}: 返回 {len(df)} 条净值记录")

        return df.reset_index(drop=True)

    except Exception as e:
        logger.error(f"{symbol}: 场外基金净值获取失败 - {str(e)[:100]}")
        raise ValueError(f"{symbol}: 场外基金净值获取失败 - {str(e)[:100]}")


def get_fund_of_daily_list() -> pd.DataFrame:
    """
    获取所有场外基金的当日净值列表。

    返回
    ----
    pd.DataFrame
        当日所有场外基金的净值数据
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    try:
        df = ak.fund_open_fund_daily_em()
        logger.info(f"获取场外基金当日净值列表，共 {len(df)} 只基金")
        return df
    except Exception as e:
        logger.error(f"场外基金当日净值列表获取失败: {e}")
        raise


def get_fund_of_info(symbol: str) -> dict:
    """
    获取场外基金的基本信息。

    参数
    ----
    symbol : str
        基金代码

    返回
    ----
    dict
        基金基本信息，如基金名称、类型、管理人等
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    try:
        df = ak.fund_open_fund_info_em(symbol=symbol)
        if df is None or df.empty:
            return {}

        info = {}
        if "基金简称" in df.columns:
            info["name"] = df.iloc[0]["基金简称"]
        if "基金类型" in df.columns:
            info["type"] = df.iloc[0]["基金类型"]

        logger.info(f"{symbol}: 获取基金基本信息")
        return info

    except Exception as e:
        logger.warning(f"{symbol}: 基金基本信息获取失败 - {str(e)[:100]}")
        return {}
