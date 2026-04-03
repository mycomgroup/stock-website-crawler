"""
db/meta_cache_api.py
元数据缓存 API - 提供使用统一缓存管理器的元数据获取功能。

使用方式:
    from jk2bt.db.meta_cache_api import (
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

from .unified_cache import UnifiedCacheManager, get_unified_cache
from .cache_config import init_default_cache

logger = logging.getLogger(__name__)

_initialized = False


def _ensure_initialized():
    """确保缓存已初始化"""
    global _initialized
    if not _initialized:
        init_default_cache()
        _initialized = True


def get_trade_days_from_cache(
    force_update: bool = False,
    use_duckdb: bool = True,
) -> List[datetime]:
    """
    从缓存获取交易日历。

    Args:
        force_update: 是否强制更新
        use_duckdb: 是否使用 DuckDB（否则 fallback 到 pickle）

    Returns:
        交易日列表 (pd.Timestamp)
    """
    _ensure_initialized()
    cache = get_unified_cache()

    if use_duckdb and not force_update:
        df = cache.get("meta", "trade_days")
        if not df.empty:
            return pd.to_datetime(df["date"]).tolist()

    logger.info("从 akshare 获取交易日历...")
    try:
        import akshare as ak
    except ImportError:
        logger.warning("akshare 未安装，无法获取交易日历")
        return []

    try:
        df = ak.tool_trade_date_hist_sina()
        df = df.rename(columns={"trade_date": "date"})
        df["date"] = pd.to_datetime(df["date"]).dt.date

        if use_duckdb:
            cache.set("meta", "trade_days", df)

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
        use_duckdb: 是否使用 DuckDB

    Returns:
        DataFrame: 证券列表
    """
    _ensure_initialized()
    cache = get_unified_cache()

    if types is None:
        types = ["stock"]

    if use_duckdb and not force_update:
        df = cache.get("meta", "securities")
        if not df.empty:
            if "type" in df.columns:
                df = df[df["type"].isin(types)]
            return df

    logger.info("从 akshare 获取证券列表...")
    try:
        import akshare as ak
    except ImportError:
        logger.warning("akshare 未安装，无法获取证券列表")
        return pd.DataFrame()

    try:
        df = ak.stock_info_a_code_name()

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
            cache.set("meta", "securities", df)

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
        use_duckdb: 是否使用 DuckDB

    Returns:
        Dict: 证券信息
    """
    _ensure_initialized()
    cache = get_unified_cache()

    code_num = code.replace(".XSHG", "").replace(".XSHE", "")
    if code.startswith("sh"):
        code_num = code[2:]
    elif code.startswith("sz"):
        code_num = code[2:]

    code_with_prefix = ("sh" if code_num.startswith("6") else "sz") + code_num

    if use_duckdb and not force_update:
        adapter = cache.get_adapter("meta")
        if adapter:
            df = adapter.query("security_info", {"code": code_with_prefix})
            if not df.empty:
                info_json = df.iloc[0]["info_json"]
                try:
                    return json.loads(info_json)
                except:
                    pass

            df = adapter.query("security_info", {"code": code})
            if not df.empty:
                info_json = df.iloc[0]["info_json"]
                try:
                    return json.loads(info_json)
                except:
                    pass

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
        info_json = json.dumps(result, ensure_ascii=False)
        df = pd.DataFrame(
            [
                {
                    "code": code_with_prefix,
                    "info_json": info_json,
                    "update_time": datetime.now(),
                }
            ]
        )
        adapter = cache.get_adapter("meta")
        if adapter:
            adapter.insert("security_info", df)

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
    cache = get_unified_cache()

    adapter = cache.get_adapter("meta")
    if not adapter:
        return {"error": "meta 数据库未注册"}

    return {
        "trade_days": adapter.count("trade_days"),
        "securities": adapter.count("securities"),
        "security_info": adapter.count("security_info"),
    }
