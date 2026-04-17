"""
finance_data/share_change.py
股东变动数据获取模块。

主要功能：
1. 股东变动查询 - finance.STK_SHAREHOLDER_CHANGE
2. FinanceQuery 类提供 finance.run_query 兼容接口

数据字段：
- code: 股票代码（聚宽格式）
- shareholder_name: 股东名称
- change_date: 变动日期
- change_type: 变动类型（增持/减持）
- change_amount: 变动数量
- change_ratio: 变动比例
- hold_amount_after: 变动后持股数量
- hold_ratio_after: 变动后持股比例

缓存策略:
- Parquet 缓存：存储在 data/share_change_parquet 中
- 按周缓存：动态数据
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Union, Dict
import logging

logger = logging.getLogger(__name__)

from jk2bt.utils.result import RobustResult
from jk2bt.utils.symbol import extract_code_num, ak_code_to_jq
from jk2bt.utils.date_utils import (
    parse_ratio as _parse_ratio,
    parse_date as _parse_date,
    parse_num,
    parse_int,
    filter_by_date_range,
)


SHARE_CHANGE_CACHE_DAYS = 7

_CACHE_AVAILABLE = False
try:
    from jk2bt.cache import get_cache_manager

    _CACHE_AVAILABLE = True
except ImportError:
    logger.warning("parquet_cache 模块不可用")


_SHARE_CHANGE_SCHEMA = [
    "code",
    "shareholder_name",
    "change_date",
    "change_type",
    "change_amount",
    "change_ratio",
    "hold_amount_after",
    "hold_ratio_after",
]


class ShareChangeCacheManager:
    """股东变动 parquet_cache 管理器"""

    _instance = None

    def __new__(cls, base_dir: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_manager(base_dir)
        return cls._instance

    def _init_manager(self, base_dir: str = None):
        if not _CACHE_AVAILABLE:
            self._cache = None
            return

        if base_dir is None:
            base_dir = os.path.join(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                ),
                "data",
                "cache",
            )

        self.base_dir = base_dir
        self._cache = None

        try:
            self._cache = get_cache_manager(base_dir=base_dir)
        except Exception as e:
            logger.warning(f"parquet_cache 初始化失败: {e}")
            self._cache = None

    def insert_share_change(self, df: pd.DataFrame):
        if self._cache is None or df.empty:
            return

        df = df.copy()
        rename_map = {
            "code": "symbol",
            "change_date": "announce_date",
            "change_amount": "total_shares",
        }
        df = df.rename(columns=rename_map)

        for col in [
            "symbol",
            "announce_date",
            "total_shares",
            "circulating_shares",
            "change_type",
        ]:
            if col not in df.columns:
                df[col] = None

        cols = [
            "symbol",
            "announce_date",
            "total_shares",
            "circulating_shares",
            "change_type",
        ]
        df = df[cols]

        try:
            if "announce_date" in df.columns:
                for value, group in df.groupby("announce_date"):
                    self._cache.put("share_change", group, partition_value=str(value))
            else:
                self._cache.put("share_change", df)
            logger.info(f"插入/更新 {len(df)} 条股东变动信息")
        except Exception as e:
            logger.warning(f"插入股东变动信息失败: {e}")

    def get_share_change(
        self, code: str, start_date: str = None, end_date: str = None
    ) -> pd.DataFrame:
        if self._cache is None:
            return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)

        try:
            result = self._cache.get("share_change", where={"symbol": code})
            if result is not None and not result.empty:
                rename_map = {
                    "symbol": "code",
                    "announce_date": "change_date",
                    "total_shares": "change_amount",
                }
                result = result.rename(columns=rename_map)
                for col in _SHARE_CHANGE_SCHEMA:
                    if col not in result.columns:
                        result[col] = None
                result = result[_SHARE_CHANGE_SCHEMA]
                if start_date and end_date and "change_date" in result.columns:
                    result = result[
                        (result["change_date"] >= start_date)
                        & (result["change_date"] <= end_date)
                    ]
                return result.sort_values("change_date", ascending=False)
            return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)
        except Exception as e:
            logger.warning(f"查询股东变动信息失败: {e}")
            return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)

    def is_cache_valid(self, code: str, cache_days: int = 7) -> bool:
        if self._cache is None:
            return False
        try:
            result = self._cache.get("share_change", where={"symbol": code})
            return result is not None and not result.empty
        except Exception:
            return False


_db_manager = ShareChangeCacheManager() if _CACHE_AVAILABLE else None


def get_share_change(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取股东变动信息。

    参数
    ----
    symbol      : 股票代码
    start_date  : 起始日期
    end_date    : 结束日期
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，标准化字段：
    - code: 股票代码（聚宽格式）
    - shareholder_name: 股东名称
    - change_date: 变动日期
    - change_type: 变动类型（增持/减持）
    - change_amount: 变动数量
    - change_ratio: 变动比例
    - hold_amount_after: 变动后持股数量
    - hold_ratio_after: 变动后持股比例
    """
    code_num = extract_code_num(symbol)
    jq_code = ak_code_to_jq(symbol)

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(jq_code, cache_days=7):
            df_cached = _db_manager.get_share_change(jq_code, start_date, end_date)
            if not df_cached.empty:
                return df_cached[_SHARE_CHANGE_SCHEMA]

    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_shareholder_change_ths(symbol=code_num)
        if df is not None and not df.empty:
            result = _normalize_share_change(df, jq_code)
            if not result.empty:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_share_change(result)
                if start_date is None and end_date is None:
                    return result
                return filter_by_date_range(
                    result, start_date, end_date, date_col="change_date"
                )
    except Exception as e:
        logger.warning(f"[share_change] 获取股东变动失败 {symbol}: {e}")

    return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)


def _normalize_share_change(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    """标准化股东变动数据"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)

    result = pd.DataFrame()
    result["code"] = [jq_code] * len(df)

    col_map = {
        "股东名称": "shareholder_name",
        "变动日期": "change_date",
        "增减": "change_type",
        "变动数量": "change_amount",
        "变动比例": "change_ratio",
        "持股数量": "hold_amount_after",
        "持股比例": "hold_ratio_after",
    }

    for src, target in col_map.items():
        if src in df.columns:
            if target in ["change_date"]:
                result[target] = df[src].apply(_parse_date)
            elif target in ["change_amount", "hold_amount_after"]:
                result[target] = df[src].apply(_parse_num)
            elif target in ["change_ratio", "hold_ratio_after"]:
                result[target] = df[src].apply(_parse_ratio)
            else:
                result[target] = df[src]
        else:
            result[target] = None

    return result


def query_share_change(
    symbols: List[str],
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    批量查询股东变动（finance.STK_SHAREHOLDER_CHANGE）。
    """
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)

    dfs = []
    for symbol in symbols:
        try:
            df = get_share_change(
                symbol,
                start_date=start_date,
                end_date=end_date,
                force_update=force_update,
                use_duckdb=use_duckdb,
            )
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            logger.warning(f"[query_share_change] 获取 {symbol} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


class FinanceQuery:
    """聚宽 finance 模块模拟器"""

    class STK_SHAREHOLDER_CHANGE:
        code = None
        shareholder_name = None
        change_date = None
        change_type = None
        change_amount = None
        change_ratio = None

    def run_query(self, query_obj, force_update=False, use_duckdb=True) -> pd.DataFrame:
        table_name = None
        conditions = {}

        if hasattr(query_obj, "__class__"):
            table_name = query_obj.__class__.__name__

        if hasattr(query_obj, "left") and hasattr(query_obj, "right"):
            if hasattr(query_obj.left, "__class__"):
                table_name = query_obj.left.__class__.__name__
            if hasattr(query_obj, "right"):
                conditions["code"] = query_obj.right

        if table_name == "STK_SHAREHOLDER_CHANGE":
            if "code" in conditions:
                return get_share_change(conditions["code"], use_duckdb=use_duckdb)
            return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)
        else:
            raise ValueError(f"不支持的表: {table_name}")


finance = FinanceQuery()


def run_query_simple(
    table: str,
    code: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """简化的查询接口"""
    if table == "STK_SHAREHOLDER_CHANGE":
        if code:
            return get_share_change(code, force_update=force_update)
        return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)
    else:
        raise ValueError(f"不支持的表: {table}")


_PLEDGE_SCHEMA = [
    "code",
    "pledge_date",
    "pledgor",
    "pledgee",
    "pledge_amount",
    "pledge_ratio",
]


def get_pledge_info(
    symbol: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """获取股权质押信息"""
    code_num = extract_code_num(symbol)
    jq_code = ak_code_to_jq(symbol)

    from jk2bt.data.sources import get_adapter

    try:
        df_raw = get_adapter().get_pledge_ratio_em(symbol=code_num)
        if df_raw is not None and not df_raw.empty:
            result = pd.DataFrame()
            result["code"] = [jq_code] * len(df_raw)
            for col in ["质押日期", "日期"]:
                if col in df_raw.columns:
                    result["pledge_date"] = df_raw[col]
                    break
            for col in ["股东名称", "出质人"]:
                if col in df_raw.columns:
                    result["pledgor"] = df_raw[col]
                    break
            for col in ["质权人"]:
                if col in df_raw.columns:
                    result["pledgee"] = df_raw[col]
                    break
            for col in ["质押数量", "质押股数"]:
                if col in df_raw.columns:
                    result["pledge_amount"] = df_raw[col]
                    break
            for col in ["质押比例", "占股比"]:
                if col in df_raw.columns:
                    result["pledge_ratio"] = df_raw[col]
                    break
            return result
    except Exception as e:
        logger.warning(f"[get_pledge_info] 获取失败 {symbol}: {e}")

    return pd.DataFrame(columns=_PLEDGE_SCHEMA)


_HOLDER_TRADE_SCHEMA = [
    "code",
    "holder_name",
    "trade_date",
    "trade_type",
    "trade_amount",
]


def get_major_holder_trade(
    symbol: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """获取重要股东交易信息"""
    return get_share_change(symbol, force_update=force_update)


_SHAREHOLDER_CHANGES_SCHEMA = [
    "code",
    "shareholder_name",
    "change_date",
    "change_type",
    "change_amount",
    "change_ratio",
    "change_reason",
    "hold_amount_after",
    "hold_ratio_after",
]


def get_shareholder_changes(
    code: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> RobustResult:
    """
    获取股东增减持数据（稳健版）。

    参数
    ----
    code         : 股票代码
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新
    use_duckdb   : 是否使用 DuckDB 缓存

    返回
    ----
    RobustResult:
        success: 是否成功
        data: pandas DataFrame，标准化字段：
            - code: 股票代码（聚宽格式）
            - shareholder_name: 股东名称
            - change_date: 变动日期
            - change_type: 变动类型（增持/减持）
            - change_amount: 变动数量
            - change_ratio: 变动比例
            - change_reason: 变动原因
            - hold_amount_after: 变动后持股数量
            - hold_ratio_after: 变动后持股比例
        reason: 结果说明
        source: 数据来源（cache/network/fallback）
    """
    if not code:
        return RobustResult(
            success=False,
            data=pd.DataFrame(columns=_SHAREHOLDER_CHANGES_SCHEMA),
            reason="股票代码不能为空",
            source="input",
        )

    code_num = extract_code_num(code)
    jq_code = ak_code_to_jq(code)

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(jq_code, cache_days=SHARE_CHANGE_CACHE_DAYS):
            df_cached = _db_manager.get_share_change(jq_code, start_date, end_date)
            if not df_cached.empty:
                df_result = df_cached[_SHARE_CHANGE_SCHEMA].copy()
                if "change_reason" not in df_result.columns:
                    df_result["change_reason"] = None
                df_result = df_result[_SHAREHOLDER_CHANGES_SCHEMA]
                return RobustResult(
                    success=True,
                    data=df_result,
                    reason=f"从缓存获取{len(df_result)}条股东变动记录",
                    source="cache",
                )

    try:
        df = _fetch_shareholder_changes_from_akshare(code_num, jq_code)
        if df is not None and not df.empty:
            df_result = df.copy()
            if "change_reason" not in df_result.columns:
                df_result["change_reason"] = None
            df_to_cache = df_result[_SHAREHOLDER_CHANGES_SCHEMA].copy()
            if use_duckdb and _db_manager is not None:
                cache_df = df_to_cache.copy()
                cache_df = cache_df[
                    [c for c in cache_df.columns if c != "change_reason"]
                ]
                _db_manager.insert_share_change(cache_df)

            if start_date or end_date:
                df_result = filter_by_date_range(
                    df_result, start_date, end_date, date_col="change_date"
                )
                if "change_reason" not in df_result.columns:
                    df_result["change_reason"] = None

            return RobustResult(
                success=True,
                data=df_result[_SHAREHOLDER_CHANGES_SCHEMA],
                reason=f"成功获取{len(df_result)}条股东变动记录",
                source="network",
            )
    except Exception as e:
        logger.warning(f"[get_shareholder_changes] 获取股东变动失败 {code}: {e}")

    return RobustResult(
        success=False,
        data=pd.DataFrame(columns=_SHAREHOLDER_CHANGES_SCHEMA),
        reason="无股东变动数据",
        source="network",
    )


def _fetch_shareholder_changes_from_akshare(
    code_num: str, jq_code: str
) -> Optional[pd.DataFrame]:
    """从 akshare 获取股东增减持数据"""
    from jk2bt.data.sources import get_adapter

    df = get_adapter().get_shareholder_changes_with_fallback(symbol=code_num)
    if df is not None and not df.empty:
        if "change_date" in df.columns or "变动日期" in df.columns:
            return _normalize_shareholder_changes(df, jq_code)
        else:
            return _normalize_shareholder_changes_from_cninfo(df, jq_code)

    return pd.DataFrame(columns=_SHAREHOLDER_CHANGES_SCHEMA)


def _normalize_shareholder_changes(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    """标准化股东增减持数据（东方财富格式）"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_SHAREHOLDER_CHANGES_SCHEMA)

    result = pd.DataFrame()
    result["code"] = [jq_code] * len(df)

    col_map = {
        "股东名称": "shareholder_name",
        "变动日期": "change_date",
        "增减": "change_type",
        "变动数量": "change_amount",
        "变动比例": "change_ratio",
        "持股数量": "hold_amount_after",
        "持股比例": "hold_ratio_after",
        "变动原因": "change_reason",
    }

    for src, target in col_map.items():
        if src in df.columns:
            if target == "change_date":
                result[target] = df[src].apply(_parse_date)
            elif target in ["change_amount", "hold_amount_after"]:
                result[target] = df[src].apply(_parse_num)
            elif target in ["change_ratio", "hold_ratio_after"]:
                result[target] = df[src].apply(_parse_ratio)
            else:
                result[target] = df[src]
        else:
            result[target] = None

    for col in _SHAREHOLDER_CHANGES_SCHEMA:
        if col not in result.columns:
            result[col] = None

    return result[_SHAREHOLDER_CHANGES_SCHEMA]


def _normalize_shareholder_changes_from_cninfo(
    df: pd.DataFrame, jq_code: str
) -> pd.DataFrame:
    """标准化股东增减持数据（巨潮资讯格式）"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_SHAREHOLDER_CHANGES_SCHEMA)

    result = pd.DataFrame()
    result["code"] = [jq_code] * len(df)

    col_map = {
        "股东名称": "shareholder_name",
        "公告日期": "change_date",
        "变动类型": "change_type",
        "变动股份数量": "change_amount",
        "变动比例": "change_ratio",
        "变动后持股数量": "hold_amount_after",
        "变动后持股比例": "hold_ratio_after",
        "变动原因": "change_reason",
    }

    for src, target in col_map.items():
        if src in df.columns:
            if target == "change_date":
                result[target] = df[src].apply(_parse_date)
            elif target in ["change_amount", "hold_amount_after"]:
                result[target] = df[src].apply(_parse_num)
            elif target in ["change_ratio", "hold_ratio_after"]:
                result[target] = df[src].apply(_parse_ratio)
            else:
                result[target] = df[src]
        else:
            result[target] = None

    for col in _SHAREHOLDER_CHANGES_SCHEMA:
        if col not in result.columns:
            result[col] = None

    return result[_SHAREHOLDER_CHANGES_SCHEMA]


class FinanceQueryEnhanced:
    """聚宽 finance 模块模拟器（增强版，支持 RobustResult）"""

    class STK_SHAREHOLDER_CHANGE:
        code = None
        shareholder_name = None
        change_date = None
        change_type = None
        change_amount = None
        change_ratio = None
        change_reason = None

    def run_query(
        self,
        query_obj,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> Union[pd.DataFrame, RobustResult]:
        table_name = None
        conditions = {}

        if hasattr(query_obj, "__name__"):
            table_name = query_obj.__name__
        elif hasattr(query_obj, "__class__"):
            table_name = query_obj.__class__.__name__

        if hasattr(query_obj, "left") and hasattr(query_obj, "right"):
            if hasattr(query_obj.left, "__class__"):
                table_name = query_obj.left.__class__.__name__
            if hasattr(query_obj, "right"):
                conditions["code"] = query_obj.right

        if table_name == "STK_SHAREHOLDER_CHANGE":
            if "code" in conditions:
                return get_shareholder_changes(
                    conditions["code"],
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
            return RobustResult(
                success=False,
                data=pd.DataFrame(columns=_SHAREHOLDER_CHANGES_SCHEMA),
                reason="未提供股票代码",
                source="input",
            )
        else:
            raise ValueError(f"不支持的表: {table_name}")


finance_enhanced = FinanceQueryEnhanced()


_INSIDER_TRADING_SCHEMA = [
    "code",
    "insider_name",
    "position",
    "change_date",
    "change_type",
    "change_amount",
    "change_ratio",
    "hold_amount_after",
]


def get_insider_trading(
    security: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取高管增减持信息。

    参数
    ----
    security    : 股票代码
    start_date  : 起始日期
    end_date    : 结束日期
    force_update: 强制更新

    返回
    ----
    DataFrame，包含：
    - code: 股票代码（聚宽格式）
    - insider_name: 高管姓名
    - position: 职务
    - change_date: 变动日期
    - change_type: 变动类型（增持/减持）
    - change_amount: 变动数量
    - change_ratio: 变动比例
    - hold_amount_after: 变动后持股数量
    """
    code_num = extract_code_num(security)
    jq_code = ak_code_to_jq(security)

    from jk2bt.data.sources import get_adapter

    try:
        df_raw = None
        try:
            df_raw = get_adapter().get_holding_change_em(symbol=code_num)
        except Exception as e1:
            logger.warning(f"stock_gdfx_holding_change_em 失败: {e1}")
            try:
                end_date_str = datetime.now().strftime("%Y%m%d")
                start_date_str = (datetime.now() - timedelta(days=365)).strftime(
                    "%Y%m%d"
                )
                df_raw = get_adapter().get_share_change_cninfo(
                    symbol=code_num,
                    start_date=start_date_str,
                    end_date=end_date_str,
                )
            except Exception as e2:
                logger.warning(f"stock_share_change_cninfo 失败: {e2}")

        if df_raw is not None and not df_raw.empty:
            result = _normalize_insider_trading(df_raw, jq_code)
            if not result.empty:
                if start_date is None and end_date is None:
                    return result
                return filter_by_date_range(
                    result, start_date, end_date, date_col="change_date"
                )
    except Exception as e:
        logger.warning(f"[get_insider_trading] 获取高管增减持失败 {security}: {e}")

    return pd.DataFrame(columns=_INSIDER_TRADING_SCHEMA)


def _normalize_insider_trading(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    """标准化高管增减持数据"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_INSIDER_TRADING_SCHEMA)

    result = pd.DataFrame()
    result["code"] = [jq_code] * len(df)

    col_map = {
        "股东名称": "insider_name",
        "高管姓名": "insider_name",
        "姓名": "insider_name",
        "职务": "position",
        "高管职务": "position",
        "变动日期": "change_date",
        "公告日期": "change_date",
        "增减": "change_type",
        "变动类型": "change_type",
        "变动数量": "change_amount",
        "变动股份数量": "change_amount",
        "变动比例": "change_ratio",
        "持股数量": "hold_amount_after",
        "变动后持股数量": "hold_amount_after",
    }

    for src, target in col_map.items():
        if src in df.columns:
            if target == "change_date":
                result[target] = df[src].apply(_parse_date)
            elif target in ["change_amount", "hold_amount_after"]:
                result[target] = df[src].apply(_parse_num)
            elif target == "change_ratio":
                result[target] = df[src].apply(_parse_ratio)
            else:
                result[target] = df[src]

    for col in _INSIDER_TRADING_SCHEMA:
        if col not in result.columns:
            result[col] = None

    return result[_INSIDER_TRADING_SCHEMA]


def get_major_shareholder_change(
    security: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取大股东增减持信息。

    参数
    ----
    security    : 股票代码
    start_date  : 起始日期
    end_date    : 结束日期
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，包含大股东变动信息
    """
    return get_share_change(
        security,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )


def analyze_share_change_trend(
    security: str,
    period_days: int = 90,
    force_update: bool = False,
) -> Dict:
    """
    分析股东变动趋势。

    参数
    ----
    security    : 股票代码
    period_days : 分析周期（天数），默认90天
    force_update: 强制更新

    返回
    ----
    dict，包含趋势分析：
    - net_change_type: 净变动类型（增持/减持/持平）
    - total_increase_count: 增持次数
    - total_decrease_count: 减持次数
    - net_change_amount: 净变动数量
    - avg_change_ratio: 平均变动比例
    - major_shareholder_trend: 大股东变动趋势
    - insider_trend: 高管变动趋势
    - trend_signal: 趋势信号（积极/消极/中性）
    - recent_activity: 近期活跃度
    """
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=period_days)).strftime("%Y-%m-%d")

    result = {
        "net_change_type": "持平",
        "total_increase_count": 0,
        "total_decrease_count": 0,
        "total_unchanged_count": 0,
        "net_change_amount": 0,
        "avg_change_ratio": 0.0,
        "major_shareholder_trend": "无数据",
        "insider_trend": "无数据",
        "trend_signal": "中性",
        "recent_activity": "低",
        "period_days": period_days,
        "analysis_date": end_date,
    }

    try:
        df_share = get_share_change(
            security,
            start_date=start_date,
            end_date=end_date,
            force_update=force_update,
        )

        if not df_share.empty:
            if "change_type" in df_share.columns:
                increase_count = len(
                    df_share[df_share["change_type"].str.contains("增", na=False)]
                )
                decrease_count = len(
                    df_share[df_share["change_type"].str.contains("减", na=False)]
                )
                result["total_increase_count"] = increase_count
                result["total_decrease_count"] = decrease_count

                if increase_count > decrease_count:
                    result["net_change_type"] = "增持"
                    result["major_shareholder_trend"] = "增持为主"
                elif decrease_count > increase_count:
                    result["net_change_type"] = "减持"
                    result["major_shareholder_trend"] = "减持为主"
                else:
                    result["net_change_type"] = "持平"
                    result["major_shareholder_trend"] = "变动平衡"

            if "change_amount" in df_share.columns:
                amounts = df_share["change_amount"].dropna()
                if not amounts.empty:
                    result["net_change_amount"] = int(amounts.sum())

            if "change_ratio" in df_share.columns:
                ratios = df_share["change_ratio"].dropna()
                if not ratios.empty:
                    result["avg_change_ratio"] = float(ratios.mean())

        df_insider = get_insider_trading(
            security,
            start_date=start_date,
            end_date=end_date,
            force_update=force_update,
        )

        if not df_insider.empty:
            if "change_type" in df_insider.columns:
                insider_increase = len(
                    df_insider[df_insider["change_type"].str.contains("增", na=False)]
                )
                insider_decrease = len(
                    df_insider[df_insider["change_type"].str.contains("减", na=False)]
                )
                if insider_increase > insider_decrease:
                    result["insider_trend"] = "高管增持"
                elif insider_decrease > insider_increase:
                    result["insider_trend"] = "高管减持"
                else:
                    result["insider_trend"] = "高管无明显变动"

        total_activity = result["total_increase_count"] + result["total_decrease_count"]
        if total_activity >= 10:
            result["recent_activity"] = "高"
        elif total_activity >= 5:
            result["recent_activity"] = "中"
        else:
            result["recent_activity"] = "低"

        if (
            result["net_change_type"] == "增持"
            and result["insider_trend"] == "高管增持"
        ):
            result["trend_signal"] = "积极"
        elif (
            result["net_change_type"] == "减持"
            and result["insider_trend"] == "高管减持"
        ):
            result["trend_signal"] = "消极"
        elif result["net_change_type"] == "增持":
            result["trend_signal"] = "偏积极"
        elif result["net_change_type"] == "减持":
            result["trend_signal"] = "偏消极"

        return result

    except Exception as e:
        logger.warning(f"[analyze_share_change_trend] 分析失败 {security}: {e}")
        result["error"] = str(e)
        return result


class FinanceQueryV2:
    """聚宽 finance 模块模拟器（支持 STK_SHARE_CHANGE）"""

    class STK_SHARE_CHANGE:
        code = None
        shareholder_name = None
        change_date = None
        change_type = None
        change_amount = None
        change_ratio = None
        hold_amount_after = None
        hold_ratio_after = None

    class STK_SHAREHOLDER_CHANGE:
        code = None
        shareholder_name = None
        change_date = None
        change_type = None
        change_amount = None
        change_ratio = None
        hold_amount_after = None
        hold_ratio_after = None

    def run_query(
        self,
        query_obj,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        table_name = None
        conditions = {}

        if hasattr(query_obj, "__name__"):
            table_name = query_obj.__name__
        elif hasattr(query_obj, "__class__"):
            table_name = query_obj.__class__.__name__

        if hasattr(query_obj, "left") and hasattr(query_obj, "right"):
            if hasattr(query_obj.left, "__name__"):
                table_name = query_obj.left.__name__
            elif hasattr(query_obj.left, "__class__"):
                table_name = query_obj.left.__class__.__name__
            if hasattr(query_obj, "right"):
                conditions["code"] = query_obj.right

        if table_name == "STK_SHARE_CHANGE":
            if "code" in conditions:
                return get_share_change(
                    conditions["code"],
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
            return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)
        elif table_name == "STK_SHAREHOLDER_CHANGE":
            if "code" in conditions:
                return get_shareholder_changes(
                    conditions["code"],
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                ).data
            return pd.DataFrame(columns=_SHAREHOLDER_CHANGES_SCHEMA)
        else:
            raise ValueError(f"不支持的表: {table_name}")


finance_v2 = FinanceQueryV2()


_FREEZE_SCHEMA = [
    "code",
    "shareholder_name",
    "freeze_amount",
    "freeze_ratio",
    "freeze_date",
    "freeze_reason",
    "freeze_type",
    "unfreeze_date",
]


def get_freeze_info(
    symbol: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取股份冻结信息。

    参数
    ----
    symbol      : 股票代码
    force_update: 强制更新

    返回
    ----
    DataFrame，包含冻结信息：
    - code: 股票代码（聚宽格式）
    - shareholder_name: 股东名称
    - freeze_amount: 冻结股数
    - freeze_ratio: 冻结比例
    - freeze_date: 冻结日期
    - freeze_reason: 冻结原因
    - freeze_type: 冻结类型
    - unfreeze_date: 解冻日期
    """
    code_num = extract_code_num(symbol)
    jq_code = ak_code_to_jq(symbol)

    try:
        df_raw = _fetch_freeze_data_from_akshare(code_num)
        if df_raw is not None and not df_raw.empty:
            result = _normalize_freeze_data(df_raw, jq_code)
            if not result.empty:
                return result
    except Exception as e:
        logger.warning(f"[get_freeze_info] 获取冻结信息失败 {symbol}: {e}")

    return pd.DataFrame(columns=_FREEZE_SCHEMA)


def _fetch_freeze_data_from_akshare(code_num: str) -> Optional[pd.DataFrame]:
    """从 akshare 获取冻结数据"""
    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_equity_mortgage_cninfo(symbol=code_num)
        if df is not None and not df.empty:
            return df
    except Exception as e:
        logger.warning(f"stock_cg_equity_mortgage_cninfo 失败: {e}")

    try:
        df = get_adapter().get_shareholder_change_ths(symbol=code_num)
        if df is not None and not df.empty:
            freeze_cols = [c for c in df.columns if "冻结" in c or "质押" in c]
            if freeze_cols:
                return df
    except Exception as e:
        logger.warning(f"stock_shareholder_change_ths 失败: {e}")

    return None


def _normalize_freeze_data(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    """标准化冻结数据"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_FREEZE_SCHEMA)

    result = pd.DataFrame()
    result["code"] = [jq_code] * len(df)

    col_map = {
        "股东名称": "shareholder_name",
        "冻结股数": "freeze_amount",
        "冻结数量": "freeze_amount",
        "冻结比例": "freeze_ratio",
        "冻结日期": "freeze_date",
        "冻结原因": "freeze_reason",
        "冻结类型": "freeze_type",
        "解冻日期": "unfreeze_date",
    }

    for src, target in col_map.items():
        if src in df.columns:
            if target == "freeze_date" or target == "unfreeze_date":
                result[target] = df[src].apply(_parse_date)
            elif target in ["freeze_amount"]:
                result[target] = df[src].apply(_parse_num)
            elif target == "freeze_ratio":
                result[target] = df[src].apply(_parse_ratio)
            else:
                result[target] = df[src]

    for col in _FREEZE_SCHEMA:
        if col not in result.columns:
            result[col] = None

    return result[_FREEZE_SCHEMA]


_CAPITAL_CHANGE_SCHEMA = [
    "code",
    "pub_date",
    "change_date",
    "change_type",
    "change_amount",
    "change_reason",
    "total_capital_before",
    "total_capital_before_unit",
    "total_capital_after",
    "total_capital_after_unit",
    "circulating_capital_before",
    "circulating_capital_before_unit",
    "circulating_capital_after",
    "circulating_capital_after_unit",
    "total_shares_change_ratio",
    "circulating_shares_change_ratio",
]


def get_capital_change(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取股本变动信息。

    参数
    ----
    symbol      : 股票代码
    start_date  : 起始日期
    end_date    : 结束日期
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，包含股本变动信息：
    - code: 股票代码（聚宽格式）
    - pub_date: 公告日期
    - change_date: 变动日期
    - change_type: 变动类型
    - change_amount: 变动数量
    - change_reason: 变动原因
    - total_capital_before: 变动前总股本
    - total_capital_before_unit: 变动前总股本单位
    - total_capital_after: 变动后总股本
    - total_capital_after_unit: 变动后总股本单位
    - circulating_capital_before: 变动前流通股本
    - circulating_capital_before_unit: 变动前流通股本单位
    - circulating_capital_after: 变动后流通股本
    - circulating_capital_after_unit: 变动后流通股本单位
    - total_shares_change_ratio: 总股本变动比例
    - circulating_shares_change_ratio: 流通股本变动比例
    """
    code_num = extract_code_num(symbol)
    jq_code = ak_code_to_jq(symbol)

    try:
        df_raw = _fetch_capital_change_from_akshare(code_num, start_date, end_date)
        if df_raw is not None and not df_raw.empty:
            result = _normalize_capital_change(df_raw, jq_code)
            if not result.empty:
                if start_date is None and end_date is None:
                    return result
                return _filter_capital_by_date(result, start_date, end_date)
    except Exception as e:
        logger.warning(f"[get_capital_change] 获取股本变动失败 {symbol}: {e}")

    return pd.DataFrame(columns=_CAPITAL_CHANGE_SCHEMA)


def _fetch_capital_change_from_akshare(
    code_num: str, start_date: str = None, end_date: str = None
) -> Optional[pd.DataFrame]:
    """从 akshare 获取股本变动数据"""
    from jk2bt.data.sources import get_adapter

    try:
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365 * 3)).strftime("%Y%m%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        df = get_adapter().get_share_change_cninfo(
            symbol=code_num, start_date=start_date, end_date=end_date
        )
        if df is not None and not df.empty:
            return df
    except Exception as e:
        logger.warning(f"stock_share_change_cninfo 失败: {e}")

    return None


def _normalize_capital_change(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    """标准化股本变动数据"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_CAPITAL_CHANGE_SCHEMA)

    result = pd.DataFrame()
    result["code"] = [jq_code] * len(df)

    col_map = {
        "公告日期": "pub_date",
        "变动类型": "change_type",
        "变动股份数量": "change_amount",
        "变动数量": "change_amount",
        "变动日期": "change_date",
        "变更日期": "change_date",
        "变动原因": "change_reason",
        "变动前总股本": "total_capital_before",
        "变动后总股本": "total_capital_after",
        "变动前流通股": "circulating_capital_before",
        "变动后流通股": "circulating_capital_after",
        "变动前总股本单位": "total_capital_before_unit",
        "变动后总股本单位": "total_capital_after_unit",
        "变动前流通股单位": "circulating_capital_before_unit",
        "变动后流通股单位": "circulating_capital_after_unit",
        "总股本变动比例": "total_shares_change_ratio",
        "流通股本变动比例": "circulating_shares_change_ratio",
    }

    for src, target in col_map.items():
        if src in df.columns:
            if target in ["pub_date", "change_date"]:
                result[target] = df[src].apply(_parse_date)
            elif target in [
                "change_amount",
                "total_capital_before",
                "total_capital_after",
                "circulating_capital_before",
                "circulating_capital_after",
            ]:
                result[target] = df[src].apply(_parse_num)
            elif target in [
                "total_shares_change_ratio",
                "circulating_shares_change_ratio",
            ]:
                result[target] = df[src].apply(_parse_ratio)
            else:
                result[target] = df[src]

    for col in _CAPITAL_CHANGE_SCHEMA:
        if col not in result.columns:
            result[col] = None

    return result[_CAPITAL_CHANGE_SCHEMA]


def _filter_capital_by_date(
    df: pd.DataFrame, start_date: str, end_date: str
) -> pd.DataFrame:
    """按日期筛选股本变动数据"""
    if df.empty:
        return df

    df = df.copy()

    if "change_date" not in df.columns:
        return df

    df["_date"] = pd.to_datetime(df["change_date"])

    if start_date:
        start_dt = pd.Timestamp(start_date)
        df = df[df["_date"] >= start_dt]

    if end_date:
        end_dt = pd.Timestamp(end_date)
        df = df[df["_date"] <= end_dt]

    return df.drop(columns=["_date"]).reset_index(drop=True)


_TOPHOLDER_CHANGE_SCHEMA = [
    "code",
    "holder_name",
    "holder_type",
    "change_date",
    "change_type",
    "change_amount",
    "change_ratio",
    "hold_amount_after",
    "hold_ratio_after",
]


def get_topholder_change(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取前十大股东变动信息。

    参数
    ----
    symbol      : 股票代码
    start_date  : 起始日期
    end_date    : 结束日期
    force_update: 强制更新

    返回
    ----
    DataFrame，包含前十大股东变动信息
    """
    code_num = extract_code_num(symbol)
    jq_code = ak_code_to_jq(symbol)

    try:
        df_raw = _fetch_topholder_change_from_akshare(code_num)
        if df_raw is not None and not df_raw.empty:
            result = _normalize_topholder_change(df_raw, jq_code)
            if not result.empty:
                if start_date is None and end_date is None:
                    return result
                return filter_by_date_range(
                    result, start_date, end_date, date_col="change_date"
                )
    except Exception as e:
        logger.warning(f"[get_topholder_change] 获取前十大股东变动失败 {symbol}: {e}")

    return pd.DataFrame(columns=_TOPHOLDER_CHANGE_SCHEMA)


def _fetch_topholder_change_from_akshare(code_num: str) -> Optional[pd.DataFrame]:
    """从 akshare 获取前十大股东变动数据"""
    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_holding_change_em(date=datetime.now().strftime("%Y%m%d"))
        if df is not None and not df.empty:
            code_filter = (
                df[df["股票代码"] == code_num] if "股票代码" in df.columns else df
            )
            return code_filter if not code_filter.empty else None
    except Exception as e:
        logger.warning(f"stock_gdfx_holding_change_em 失败: {e}")

    try:
        df = get_adapter().get_shareholder_change_ths(symbol=code_num)
        if df is not None and not df.empty:
            return df
    except Exception as e:
        logger.warning(f"stock_shareholder_change_ths 失败: {e}")

    return None


def _normalize_topholder_change(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    """标准化前十大股东变动数据"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_TOPHOLDER_CHANGE_SCHEMA)

    result = pd.DataFrame()
    result["code"] = [jq_code] * len(df)

    col_map = {
        "股东名称": "holder_name",
        "股东类型": "holder_type",
        "变动日期": "change_date",
        "公告日期": "change_date",
        "增减": "change_type",
        "变动类型": "change_type",
        "变动数量": "change_amount",
        "变动股数": "change_amount",
        "变动比例": "change_ratio",
        "持股数量": "hold_amount_after",
        "变动后持股": "hold_amount_after",
        "持股比例": "hold_ratio_after",
    }

    for src, target in col_map.items():
        if src in df.columns:
            if target == "change_date":
                result[target] = df[src].apply(_parse_date)
            elif target in ["change_amount", "hold_amount_after"]:
                result[target] = df[src].apply(_parse_num)
            elif target in ["change_ratio", "hold_ratio_after"]:
                result[target] = df[src].apply(_parse_ratio)
            else:
                result[target] = df[src]

    for col in _TOPHOLDER_CHANGE_SCHEMA:
        if col not in result.columns:
            result[col] = None

    return result[_TOPHOLDER_CHANGE_SCHEMA]


def query_pledge_data(
    symbols: List[str],
    force_update: bool = False,
) -> pd.DataFrame:
    """
    批量查询质押信息。

    参数
    ----
    symbols     : 股票代码列表
    force_update: 强制更新

    返回
    ----
    DataFrame，包含批量质押信息
    """
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_PLEDGE_SCHEMA)

    dfs = []
    for symbol in symbols:
        try:
            df = get_pledge_info(symbol, force_update=force_update)
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            logger.warning(f"[query_pledge_data] 获取 {symbol} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_PLEDGE_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


def query_freeze_data(
    symbols: List[str],
    force_update: bool = False,
) -> pd.DataFrame:
    """
    批量查询冻结信息。

    参数
    ----
    symbols     : 股票代码列表
    force_update: 强制更新

    返回
    ----
    DataFrame，包含批量冻结信息
    """
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_FREEZE_SCHEMA)

    dfs = []
    for symbol in symbols:
        try:
            df = get_freeze_info(symbol, force_update=force_update)
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            logger.warning(f"[query_freeze_data] 获取 {symbol} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_FREEZE_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


def query_capital_change(
    symbols: List[str],
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    批量查询股本变动信息。

    参数
    ----
    symbols     : 股票代码列表
    start_date  : 起始日期
    end_date    : 结束日期
    force_update: 强制更新

    返回
    ----
    DataFrame，包含批量股本变动信息
    """
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_CAPITAL_CHANGE_SCHEMA)

    dfs = []
    for symbol in symbols:
        try:
            df = get_capital_change(
                symbol,
                start_date=start_date,
                end_date=end_date,
                force_update=force_update,
            )
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            logger.warning(f"[query_capital_change] 获取 {symbol} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_CAPITAL_CHANGE_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


class FinanceQueryV3:
    """聚宽 finance 模块模拟器（支持所有股东变动相关表）"""

    class STK_SHARE_PLEDGE:
        code = None
        pledge_date = None
        pledgor = None
        pledgee = None
        pledge_amount = None
        pledge_ratio = None

    class STK_SHARE_FREEZE:
        code = None
        shareholder_name = None
        freeze_amount = None
        freeze_ratio = None
        freeze_date = None
        freeze_reason = None

    class STK_TOPHOLDER_CHANGE:
        code = None
        holder_name = None
        holder_type = None
        change_date = None
        change_type = None
        change_amount = None
        change_ratio = None

    class STK_CAPITAL_CHANGE:
        code = None
        pub_date = None
        change_date = None
        change_type = None
        change_amount = None
        change_reason = None
        total_capital_before = None
        total_capital_before_unit = None
        total_capital_after = None
        total_capital_after_unit = None
        circulating_capital_before = None
        circulating_capital_before_unit = None
        circulating_capital_after = None
        circulating_capital_after_unit = None
        total_shares_change_ratio = None
        circulating_shares_change_ratio = None

    class STK_SHARE_CHANGE:
        code = None
        shareholder_name = None
        change_date = None
        change_type = None
        change_amount = None
        change_ratio = None

    class STK_SHAREHOLDER_CHANGE:
        code = None
        shareholder_name = None
        change_date = None
        change_type = None
        change_amount = None
        change_ratio = None

    def run_query(
        self,
        query_obj,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        table_name = None
        conditions = {}

        if hasattr(query_obj, "__name__"):
            table_name = query_obj.__name__
        elif hasattr(query_obj, "__class__"):
            table_name = query_obj.__class__.__name__

        if hasattr(query_obj, "left") and hasattr(query_obj, "right"):
            if hasattr(query_obj.left, "__name__"):
                table_name = query_obj.left.__name__
            elif hasattr(query_obj.left, "__class__"):
                table_name = query_obj.left.__class__.__name__
            if hasattr(query_obj, "right"):
                conditions["code"] = query_obj.right

        if table_name == "STK_SHARE_PLEDGE":
            if "code" in conditions:
                return get_pledge_info(conditions["code"], force_update=force_update)
            return pd.DataFrame(columns=_PLEDGE_SCHEMA)
        elif table_name == "STK_SHARE_FREEZE":
            if "code" in conditions:
                return get_freeze_info(conditions["code"], force_update=force_update)
            return pd.DataFrame(columns=_FREEZE_SCHEMA)
        elif table_name == "STK_TOPHOLDER_CHANGE":
            if "code" in conditions:
                return get_topholder_change(
                    conditions["code"], force_update=force_update
                )
            return pd.DataFrame(columns=_TOPHOLDER_CHANGE_SCHEMA)
        elif table_name == "STK_CAPITAL_CHANGE":
            if "code" in conditions:
                return get_capital_change(conditions["code"], force_update=force_update)
            return pd.DataFrame(columns=_CAPITAL_CHANGE_SCHEMA)
        elif table_name == "STK_SHARE_CHANGE":
            if "code" in conditions:
                return get_share_change(
                    conditions["code"],
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
            return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)
        elif table_name == "STK_SHAREHOLDER_CHANGE":
            if "code" in conditions:
                return get_shareholder_changes(
                    conditions["code"],
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                ).data
            return pd.DataFrame(columns=_SHAREHOLDER_CHANGES_SCHEMA)
        else:
            raise ValueError(f"不支持的表: {table_name}")


finance_v3 = FinanceQueryV3()


__all__ = [
    "get_share_change",
    "get_shareholder_changes",
    "get_insider_trading",
    "get_major_shareholder_change",
    "get_major_holder_trade",
    "get_pledge_info",
    "get_freeze_info",
    "get_capital_change",
    "get_topholder_change",
    "analyze_share_change_trend",
    "query_share_change",
    "query_pledge_data",
    "query_freeze_data",
    "query_capital_change",
    "FinanceQuery",
    "FinanceQueryEnhanced",
    "FinanceQueryV2",
    "FinanceQueryV3",
    "finance",
    "finance_enhanced",
    "finance_v2",
    "finance_v3",
    "run_query_simple",
    "RobustResult",
    "SHARE_CHANGE_CACHE_DAYS",
    "_PLEDGE_SCHEMA",
    "_FREEZE_SCHEMA",
    "_CAPITAL_CHANGE_SCHEMA",
    "_TOPHOLDER_CHANGE_SCHEMA",
]
from jk2bt.utils.symbol import extract_code_num as _extract_code_num
from jk2bt.utils.symbol import ak_code_to_jq as _normalize_to_jq
from jk2bt.utils.date_utils import parse_int as _parse_num
