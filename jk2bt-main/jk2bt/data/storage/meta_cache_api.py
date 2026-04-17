"""
db/meta_cache_api.py
元数据缓存 API - 使用 parquet_cache 提供元数据获取功能。

使用方式:
    from .meta_cache_api import (
        get_trade_days_from_cache,
        get_securities_from_cache,
        get_security_info_from_cache,
    )
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Union
import pandas as pd

from jk2bt.cache import get_cache_manager
from .cache_config import init_default_cache
from jk2bt.utils.init_helper import LazyInitSingleton

logger = logging.getLogger(__name__)


class _MetaCacheInitializer(LazyInitSingleton):
    """元数据缓存初始化器"""

    def _do_init(self):
        init_default_cache()


_meta_initializer = _MetaCacheInitializer()


def _ensure_initialized():
    """确保缓存已初始化"""
    _meta_initializer.ensure_initialized()


def get_trade_days_from_cache(
    force_update: bool = False,
    use_duckdb: bool = True,
) -> List[datetime]:
    """
    从缓存获取交易日历。

    Args:
        force_update: 是否强制更新
        use_duckdb: 是否使用 parquet_cache（保留参数名以兼容）

    Returns:
        交易日列表 (pd.Timestamp)
    """
    _ensure_initialized()
    cache = get_cache_manager()

    if use_duckdb and not force_update:
        df = cache.get("trade_calendar")
        if not df.empty:
            return pd.to_datetime(df["date"]).tolist()

    logger.info("从 akshare 获取交易日历...")
    try:
        from jk2bt.data.sources import get_adapter

        df = get_adapter().get_trade_dates()
        df = df.rename(columns={"trade_date": "date"})
        df["date"] = pd.to_datetime(df["date"]).dt.date
        if "is_trading_day" not in df.columns:
            df["is_trading_day"] = True

        if use_duckdb:
            cache.put("trade_calendar", df)

        return pd.to_datetime(df["date"]).tolist()
    except Exception as e:
        logger.error(f"获取交易日历失败: {e}")
        return []


def get_securities_from_cache(
    types: List[str] = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    从缓存获取证券列表。

    Args:
        types: 证券类型列表，默认 ["stock"]
        force_update: 是否强制更新
        use_duckdb: 是否使用 parquet_cache

    Returns:
        DataFrame: 证券列表
    """
    _ensure_initialized()
    cache = get_cache_manager()

    if types is None:
        types = ["stock"]

    if use_duckdb and not force_update:
        df = cache.get("securities")
        if not df.empty:
            if "type" in df.columns:
                df = df[df["type"].isin(types)]
            return df

    logger.info("从 akshare 获取证券列表...")
    try:
        from jk2bt.data.sources import get_adapter

        df = get_adapter().get_securities_code_name()

        df["code"] = df["code"].apply(
            lambda x: (
                "sz" + x
                if x.startswith(("0", "3"))
                else ("sh" + x if x.startswith("6") else x)
            )
        )

        df["jq_code"] = df["code"].apply(
            lambda x: (
                x[2:]
                + (
                    ".XSHE"
                    if x.startswith("sz")
                    else ".XSHG"
                    if x.startswith("sh")
                    else ""
                )
            )
        )

        df["type"] = "stock"
        df["display_name"] = df["name"]
        df["start_date"] = None
        df["end_date"] = None
        df["update_time"] = pd.Timestamp.now()

        if use_duckdb:
            cache.put("securities", df)

        return df[df["type"].isin(types)]
    except Exception as e:
        logger.error(f"获取证券列表失败: {e}")
        return pd.DataFrame()


def get_security_info_from_cache(
    code: str,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> Dict:
    """
    从缓存获取证券详细信息。

    Args:
        code: 证券代码（支持多种格式）
        force_update: 是否强制更新
        use_duckdb: 是否使用 parquet_cache

    Returns:
        Dict: 证券信息
    """
    _ensure_initialized()
    cache = get_cache_manager()

    code_num = code.replace(".XSHG", "").replace(".XSHE", "")
    if code.startswith("sh"):
        code_num = code[2:]
    elif code.startswith("sz"):
        code_num = code[2:]

    code_with_prefix = ("sh" if code_num.startswith("6") else "sz") + code_num

    if use_duckdb and not force_update:
        df = cache.get("company_info", where={"symbol": code_with_prefix})
        if not df.empty:
            row = df.iloc[0]
            return {
                "code": code_with_prefix,
                "name": row.get("name", code_num),
                "display_name": row.get("name", code_num),
                "industry": row.get("industry", ""),
                "area": row.get("area", ""),
                "list_date": row.get("list_date"),
                "market": row.get("market", ""),
                "type": "stock",
            }

        df = cache.get("company_info", where={"symbol": code})
        if not df.empty:
            row = df.iloc[0]
            return {
                "code": code,
                "name": row.get("name", code_num),
                "display_name": row.get("name", code_num),
                "industry": row.get("industry", ""),
                "area": row.get("area", ""),
                "list_date": row.get("list_date"),
                "market": row.get("market", ""),
                "type": "stock",
            }

    securities = get_securities_from_cache(use_duckdb=use_duckdb)

    row = securities[securities["code"] == code_with_prefix]
    if row.empty:
        row = securities[securities["jq_code"] == code]
    if row.empty:
        row = securities[securities["code"] == code_num]

    if row.empty:
        result = {
            "code": code_with_prefix,
            "display_name": code_num,
            "name": code_num,
            "start_date": None,
            "end_date": None,
            "type": "stock",
        }
    else:
        row = row.iloc[0]
        result = {
            "code": row["code"],
            "display_name": row.get("display_name", row.get("name", "")),
            "name": row.get("display_name", row.get("name", "")),
            "start_date": row.get("start_date"),
            "end_date": row.get("end_date"),
            "type": row.get("type", "stock"),
            "jq_code": row.get("jq_code", ""),
        }

    if use_duckdb:
        df = pd.DataFrame(
            [
                {
                    "symbol": code_with_prefix,
                    "name": result.get("display_name", result.get("name", "")),
                    "industry": result.get("industry", ""),
                    "area": result.get("area", ""),
                    "list_date": result.get("start_date"),
                    "market": result.get("market", ""),
                }
            ]
        )
        cache.put("company_info", df)

    return result


def prewarm_meta_cache(
    force_update: bool = False,
    include_trade_days: bool = True,
    include_securities: bool = True,
) -> Dict:
    """
    预热元数据缓存。

    Args:
        force_update: 是否强制更新
        include_trade_days: 是否预热交易日历
        include_securities: 是否预热证券列表

    Returns:
        Dict: 预热结果统计
    """
    _ensure_initialized()
    results = {}

    if include_trade_days:
        days = get_trade_days_from_cache(force_update=force_update)
        results["trade_days"] = len(days)

    if include_securities:
        securities = get_securities_from_cache(force_update=force_update)
        results["securities"] = len(securities)

    return results


def check_meta_cache_status() -> Dict:
    """
    检查元数据缓存状态。

    Returns:
        Dict: 缓存状态
    """
    _ensure_initialized()
    cache = get_cache_manager()

    return {
        "trade_calendar": cache.get("trade_calendar").shape[0]
        if cache.get("trade_calendar") is not None
        else 0,
        "securities": cache.get("securities").shape[0]
        if cache.get("securities") is not None
        else 0,
        "company_info": cache.get("company_info").shape[0]
        if cache.get("company_info") is not None
        else 0,
    }
