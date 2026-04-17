"""
finance_data/unlock.py
限售解禁数据获取模块。

主要功能：
1. 限售解禁查询 - finance.STK_RESTRICTED_RELEASE
2. FinanceQuery 类提供 finance.run_query 兼容接口

数据字段：
- code: 股票代码（聚宽格式）
- unlock_date: 解禁日期
- unlock_amount: 解禁数量（股）
- unlock_ratio: 解禁比例（占总股本）
- unlock_type: 解禁类型
- holder_type: 持股人类型

缓存策略:
- Parquet 缓存：存储在 data/unlock_parquet 中
- 按周缓存：动态数据
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Union
import logging

logger = logging.getLogger(__name__)

from jk2bt.utils.result import RobustResult
from jk2bt.utils.symbol import extract_code_num, ak_code_to_jq
from jk2bt.utils.date_utils import (
    parse_ratio as _parse_ratio,
    parse_date as _parse_date,
    parse_int,
    filter_by_date_range,
)


_CACHE_AVAILABLE = False
try:
    from jk2bt.cache import get_cache_manager

    _CACHE_AVAILABLE = True
except ImportError:
    logger.warning("parquet_cache 模块不可用")


_UNLOCK_SCHEMA = [
    "code",
    "unlock_date",
    "unlock_amount",
    "unlock_ratio",
    "unlock_type",
    "holder_type",
]


class UnlockCacheManager:
    """限售解禁 parquet_cache 管理器"""

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

    def insert_unlock(self, df: pd.DataFrame):
        if self._cache is None or df.empty:
            return

        df = df.copy()
        rename_map = {
            "code": "symbol",
            "unlock_amount": "unlock_count",
        }
        df = df.rename(columns=rename_map)

        for col in [
            "symbol",
            "announce_date",
            "unlock_date",
            "unlock_count",
            "unlock_ratio",
            "unlock_type",
        ]:
            if col not in df.columns:
                df[col] = None
        if "announce_date" not in df.columns and "unlock_date" in df.columns:
            df["announce_date"] = df["unlock_date"]

        cols = [
            "symbol",
            "announce_date",
            "unlock_date",
            "unlock_count",
            "unlock_ratio",
            "unlock_type",
        ]
        df = df[cols]

        try:
            if "announce_date" in df.columns:
                for value, group in df.groupby("announce_date"):
                    self._cache.put("unlock", group, partition_value=str(value))
            else:
                self._cache.put("unlock", df)
            logger.info(f"插入/更新 {len(df)} 条限售解禁信息")
        except Exception as e:
            logger.warning(f"插入限售解禁信息失败: {e}")

    def get_unlock(
        self, code: str, start_date: str = None, end_date: str = None
    ) -> pd.DataFrame:
        if self._cache is None:
            return pd.DataFrame(columns=_UNLOCK_SCHEMA)

        try:
            result = self._cache.get("unlock", where={"symbol": code})
            if result is not None and not result.empty:
                rename_map = {
                    "symbol": "code",
                    "unlock_count": "unlock_amount",
                }
                result = result.rename(columns=rename_map)
                for col in _UNLOCK_SCHEMA:
                    if col not in result.columns:
                        result[col] = None
                result = result[_UNLOCK_SCHEMA]
                if start_date and end_date and "unlock_date" in result.columns:
                    result = result[
                        (result["unlock_date"] >= start_date)
                        & (result["unlock_date"] <= end_date)
                    ]
                return result.sort_values("unlock_date")
            return pd.DataFrame(columns=_UNLOCK_SCHEMA)
        except Exception as e:
            logger.warning(f"查询限售解禁信息失败: {e}")
            return pd.DataFrame(columns=_UNLOCK_SCHEMA)

    def is_cache_valid(self, code: str, cache_days: int = 7) -> bool:
        if self._cache is None:
            return False
        try:
            result = self._cache.get("unlock", where={"symbol": code})
            return result is not None and not result.empty
        except Exception:
            return False


_db_manager = UnlockCacheManager() if _CACHE_AVAILABLE else None


def get_unlock(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取限售解禁信息。

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
    - unlock_date: 解禁日期
    - unlock_amount: 解禁数量
    - unlock_ratio: 解禁比例
    - unlock_type: 解禁类型
    - holder_type: 持股人类型
    """
    jq_code = ak_code_to_jq(symbol)

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(jq_code, cache_days=7):
            df_cached = _db_manager.get_unlock(jq_code, start_date, end_date)
            if not df_cached.empty:
                return df_cached[_UNLOCK_SCHEMA]

    from jk2bt.data.sources import get_adapter

    try:
        results = []

        data_sources = get_adapter().get_unlock_with_fallback(
            symbol=extract_code_num(symbol)
        )
        for source_name, df in data_sources:
            if source_name == "sina_queue":
                for _, row in df.iterrows():
                    record = _parse_queue_row(row, jq_code)
                    if record:
                        results.append(record)
            elif source_name == "em_summary":
                for _, row in df.iterrows():
                    record = _parse_summary_row(row, jq_code)
                    if record:
                        results.append(record)

        if results:
            result_df = pd.DataFrame(results)
            result_df = result_df.drop_duplicates(
                subset=["code", "unlock_date"], keep="first"
            )
            result_df = result_df.sort_values("unlock_date")
            if use_duckdb and _db_manager is not None:
                _db_manager.insert_unlock(result_df)
            if start_date is None and end_date is None:
                return result_df
            return filter_by_date_range(
                result_df, start_date, end_date, date_col="unlock_date"
            )

    except Exception as e:
        logger.warning(f"[unlock] 获取限售解禁失败 {symbol}: {e}")

    return pd.DataFrame(columns=_UNLOCK_SCHEMA)


def _parse_summary_row(row, jq_code: str) -> Optional[dict]:
    """解析汇总数据行"""
    try:
        return {
            "code": jq_code,
            "unlock_date": _parse_date(row.get("解禁日期", None)),
            "unlock_amount": parse_int(row.get("解禁数量", 0)),
            "unlock_ratio": _parse_ratio(row.get("解禁比例", 0)),
            "unlock_type": str(row.get("解禁类型", "")),
            "holder_type": str(row.get("限售股类型", "")),
        }
    except Exception:
        return None


def _parse_queue_row(row, jq_code: str) -> Optional[dict]:
    """解析新浪排队数据行"""
    try:
        unlock_amount = parse_int(row.get("解禁数量", 0))
        return {
            "code": jq_code,
            "unlock_date": _parse_date(row.get("解禁日期", None)),
            "unlock_amount": unlock_amount,
            "unlock_ratio": None,
            "unlock_type": str(row.get("上市批次", "")),
            "holder_type": str(row.get("名称", "")),
        }
    except Exception:
        return None


def _parse_detail_row(row, jq_code: str) -> Optional[dict]:
    """解析明细数据行"""
    try:
        return {
            "code": jq_code,
            "unlock_date": _parse_date(row.get("解禁日期", None)),
            "unlock_amount": parse_int(row.get("解禁股数", 0)),
            "unlock_ratio": _parse_ratio(row.get("占总股本比例", 0)),
            "unlock_type": str(row.get("解禁类型", "")),
            "holder_type": str(row.get("股东名称", "")),
        }
    except Exception:
        return None


def query_unlock(
    symbols: List[str],
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    批量查询限售解禁（finance.STK_RESTRICTED_RELEASE）。
    """
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_UNLOCK_SCHEMA)

    dfs = []
    for symbol in symbols:
        try:
            df = get_unlock(
                symbol,
                start_date=start_date,
                end_date=end_date,
                force_update=force_update,
                use_duckdb=use_duckdb,
            )
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            logger.warning(f"[query_unlock] 获取 {symbol} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_UNLOCK_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


def get_unlock_calendar(
    date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取指定日期的全市场解禁日历。

    参数
    ----
    date        : 查询日期，默认今天
    force_update: 强制更新

    返回
    ----
    DataFrame，包含当天解禁的所有股票
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    from jk2bt.data.sources import get_adapter

    try:
        date_num = date.replace("-", "")
        df = get_adapter().get_unlock_detail_em(start_date=date_num, end_date=date_num)
        if df is not None and not df.empty:
            result = pd.DataFrame()
            code_col = "股票代码" if "股票代码" in df.columns else "code"
            result["code"] = df[code_col].apply(
                lambda x: ak_code_to_jq(str(x).zfill(6)) if pd.notna(x) else ""
            )
            result["unlock_date"] = [date] * len(df)
            amount_col = "实际解禁数量" if "实际解禁数量" in df.columns else "解禁数量"
            result["unlock_amount"] = pd.to_numeric(
                df.get(amount_col, 0), errors="coerce"
            )
            ratio_col = (
                "占解禁前流通市值比例"
                if "占解禁前流通市值比例" in df.columns
                else "解禁比例"
            )
            result["unlock_ratio"] = pd.to_numeric(
                df.get(ratio_col, 0), errors="coerce"
            )
            type_col = "限售股类型" if "限售股类型" in df.columns else "解禁类型"
            result["unlock_type"] = df.get(type_col, "")
            result["holder_type"] = ""
            return result
    except Exception as e:
        logger.warning(f"[unlock_calendar] 获取解禁日历失败 {date}: {e}")

    return pd.DataFrame(columns=_UNLOCK_SCHEMA)


_LOCK_SHARE_SCHEMA = [
    "code",
    "unlock_date",
    "lock_amount",
    "lock_type",
    "shareholder_name",
    "shareholder_type",
]


class FinanceQuery:
    """聚宽 finance 模块模拟器"""

    class STK_RESTRICTED_RELEASE:
        code = None
        unlock_date = None
        unlock_amount = None
        unlock_ratio = None
        unlock_type = None
        holder_type = None

    class STK_UNLOCK_INFO:
        code = None
        unlock_date = None
        unlock_amount = None
        unlock_ratio = None
        unlock_type = None
        holder_type = None

    class STK_LOCK_UNLOCK:
        code = None
        unlock_date = None
        unlock_amount = None
        unlock_ratio = None
        unlock_type = None
        holder_type = None

    class STK_UNLOCK_DATE:
        code = None
        unlock_date = None
        unlock_amount = None
        unlock_ratio = None
        unlock_type = None
        holder_type = None

    class STK_LOCK_SHARE:
        code = None
        unlock_date = None
        lock_amount = None
        lock_type = None
        shareholder_name = None
        shareholder_type = None

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

        if table_name in [
            "STK_RESTRICTED_RELEASE",
            "STK_UNLOCK_INFO",
            "STK_LOCK_UNLOCK",
            "STK_UNLOCK_DATE",
        ]:
            if "code" in conditions:
                return get_unlock(conditions["code"], use_duckdb=use_duckdb)
            return pd.DataFrame(columns=_UNLOCK_SCHEMA)
        elif table_name == "STK_LOCK_SHARE":
            if "code" in conditions:
                return query_lock_share(conditions["code"], force_update=force_update)
            return pd.DataFrame(columns=_LOCK_SHARE_SCHEMA)
        else:
            raise ValueError(f"不支持的表: {table_name}")


finance = FinanceQuery()


def get_unlock_schedule(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取解禁时间表（别名接口）。

    参数
    ----
    symbol       : 股票代码
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame
    """
    return get_unlock(
        symbol,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
    )


def get_unlock_pressure(
    symbol: str,
    days_ahead: int = 30,
    force_update: bool = False,
) -> dict:
    """
    计算解禁压力指标。

    参数
    ----
    symbol       : 股票代码
    days_ahead   : 未来多少天
    force_update : 强制更新

    返回
    ----
    dict，包含：
    - code: 股票代码
    - total_unlock_amount: 解禁总量
    - total_unlock_value: 解禁总市值
    - pressure_level: 压力等级
    """
    from datetime import datetime, timedelta

    today = datetime.now()
    future_date = (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")

    df = get_unlock(
        symbol,
        start_date=today_str,
        end_date=future_date,
        force_update=force_update,
    )

    jq_code = ak_code_to_jq(symbol) if "normalize_to_jq" in dir() else symbol

    if df.empty:
        return {
            "code": jq_code,
            "total_unlock_amount": 0,
            "total_unlock_value": 0,
            "pressure_level": "none",
        }

    total_amount = 0
    total_value = 0

    if "unlock_amount" in df.columns:
        total_amount = df["unlock_amount"].sum()
    if "unlock_market_value" in df.columns:
        total_value = df["unlock_market_value"].sum()

    max_ratio = 0
    if "unlock_ratio_total" in df.columns:
        max_ratio = df["unlock_ratio_total"].max()

    if max_ratio >= 0.1:
        pressure_level = "high"
    elif max_ratio >= 0.05:
        pressure_level = "medium"
    elif max_ratio > 0:
        pressure_level = "low"
    else:
        pressure_level = "none"

    return {
        "code": jq_code,
        "total_unlock_amount": float(total_amount) if pd.notna(total_amount) else 0,
        "total_unlock_value": float(total_value) if pd.notna(total_value) else 0,
        "pressure_level": pressure_level,
    }


def run_query_simple(
    table: str,
    code: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """简化的查询接口"""
    if table == "STK_RESTRICTED_RELEASE":
        if code:
            return get_unlock(code, force_update=force_update)
        return pd.DataFrame(columns=_UNLOCK_SCHEMA)
    else:
        raise ValueError(f"不支持的表: {table}")


def get_unlock_info(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> RobustResult:
    """
    稳健版限售解禁信息获取，返回 RobustResult。

    获取指定股票的限售股解禁数据，包括解禁日期、解禁股数、解禁比例等。
    使用 akshare 的 stock_restricted_release_summary_em 或 stock_restricted_release_detail_em 接口。

    参数
    ----
    symbol      : 股票代码，支持多种格式（600519.XSHG, sh600519, 600519 等）
    start_date  : 起始日期（可选）
    end_date    : 结束日期（可选）
    force_update: 强制更新

    返回
    ----
    RobustResult，包含：
    - success: 是否成功获取数据
    - data: DataFrame，字段：
        - code: 股票代码（聚宽格式）
        - unlock_date: 解禁日期
        - unlock_amount: 解禁数量（股）
        - unlock_ratio: 解禁比例（占总股本）
        - unlock_type: 解禁类型
        - holder_type: 持股人类型/限售股类型
    - reason: 失败原因或成功说明
    - source: 数据来源（'cache'/'network'/'fallback'）

    缓存策略
    --------
    - 7天缓存（动态数据）
    - 网络失败时使用缓存兜底

    示例
    ----
    >>> result = get_unlock_info('600519.XSHG')
    >>> if result.success:
    >>>     df = result.data
    >>>     print(f"获取到 {len(df)} 条解禁记录")
    >>> else:
    >>>     print(f"获取失败: {result.reason}")
    """
    jq_code = ak_code_to_jq(symbol)

    from jk2bt.data.sources import get_adapter

    try:
        results = []

        data_sources = get_adapter().get_unlock_with_fallback(
            symbol=extract_code_num(symbol)
        )
        for source_name, df in data_sources:
            if source_name == "sina_queue":
                for _, row in df.iterrows():
                    record = _parse_queue_row(row, jq_code)
                    if record:
                        results.append(record)
            elif source_name == "em_summary":
                for _, row in df.iterrows():
                    record = _parse_summary_row(row, jq_code)
                    if record:
                        results.append(record)

        if results:
            result_df = pd.DataFrame(results)
            result_df = result_df.drop_duplicates(
                subset=["code", "unlock_date"], keep="first"
            )
            result_df = result_df.sort_values("unlock_date").reset_index(drop=True)

            df_filtered = filter_by_date_range(
                result_df, start_date, end_date, date_col="unlock_date"
            )
            if not df_filtered.empty or (start_date is None and end_date is None):
                return RobustResult(
                    success=True,
                    data=df_filtered if not df_filtered.empty else result_df,
                    reason=f"成功获取 {len(result_df)} 条解禁记录",
                    source="network",
                )
            else:
                return RobustResult(
                    success=False,
                    data=pd.DataFrame(columns=_UNLOCK_SCHEMA),
                    reason=f"指定日期范围无解禁记录",
                    source="network",
                )

    except Exception as e:
        logger.warning(f"[get_unlock_info] 获取失败: {e}")

    return RobustResult(
        success=False,
        data=pd.DataFrame(columns=_UNLOCK_SCHEMA),
        reason=f"无法获取解禁信息 (股票: {symbol})",
        source="error",
    )


def get_upcoming_unlocks(
    days: int = 30,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取即将解禁的股票列表。

    参数
    ----
    days        : 未来天数，默认30天
    force_update: 强制更新

    返回
    ----
    DataFrame，包含：
    - code: 股票代码（聚宽格式）
    - unlock_date: 解禁日期
    - unlock_amount: 解禁数量（股）
    - unlock_ratio: 解禁比例
    - unlock_type: 解禁类型
    - unlock_market_value: 解禁市值（如有）
    """
    today = datetime.now()
    start_date = today.strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=days)).strftime("%Y-%m-%d")

    from jk2bt.data.sources import get_adapter

    try:
        start_num = start_date.replace("-", "")
        end_num = end_date.replace("-", "")
        df = get_adapter().get_unlock_detail_em(start_date=start_num, end_date=end_num)
        if df is not None and not df.empty:
            result = pd.DataFrame()
            code_col = "股票代码" if "股票代码" in df.columns else "code"
            result["code"] = df[code_col].apply(
                lambda x: ak_code_to_jq(str(x).zfill(6)) if pd.notna(x) else ""
            )
            date_col = "解禁日期" if "解禁日期" in df.columns else "unlock_date"
            result["unlock_date"] = (
                df[date_col].apply(_parse_date) if date_col in df.columns else None
            )
            amount_col = "实际解禁数量" if "实际解禁数量" in df.columns else "解禁数量"
            result["unlock_amount"] = pd.to_numeric(
                df.get(amount_col, 0), errors="coerce"
            )
            ratio_col = (
                "占解禁前流通市值比例"
                if "占解禁前流通市值比例" in df.columns
                else "解禁比例"
            )
            result["unlock_ratio"] = pd.to_numeric(
                df.get(ratio_col, 0), errors="coerce"
            )
            type_col = "限售股类型" if "限售股类型" in df.columns else "解禁类型"
            result["unlock_type"] = df.get(type_col, "")
            value_col = (
                "解禁市值" if "解禁市值" in df.columns else "unlock_market_value"
            )
            if value_col in df.columns:
                result["unlock_market_value"] = pd.to_numeric(
                    df[value_col], errors="coerce"
                )
            else:
                result["unlock_market_value"] = None
            result = result.dropna(subset=["code"])
            return result
    except Exception as e:
        logger.warning(f"[get_upcoming_unlocks] 获取即将解禁股票失败: {e}")

    return pd.DataFrame(columns=_UNLOCK_SCHEMA + ["unlock_market_value"])


def get_unlock_history(
    security: str,
    years: int = 3,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取历史解禁记录。

    参数
    ----
    security    : 股票代码
    years       : 查询年数，默认3年
    force_update: 强制更新

    返回
    ----
    DataFrame，包含历次解禁信息：
    - code: 股票代码（聚宽格式）
    - unlock_date: 解禁日期
    - unlock_amount: 解禁数量
    - unlock_ratio: 解禁比例
    - unlock_type: 解禁类型
    - holder_type: 持股人类型
    """
    today = datetime.now()
    start_date = (today - timedelta(days=years * 365)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    return get_unlock(
        security,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
    )


def query_lock_share(
    symbol: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    查询限售股份信息（finance.STK_LOCK_SHARE）。

    参数
    ----
    symbol       : 股票代码
    force_update : 强制更新

    返回
    ----
    DataFrame，包含：
    - code: 股票代码（聚宽格式）
    - unlock_date: 解禁日期
    - lock_amount: 限售股数量
    - lock_type: 限售类型
    - shareholder_name: 股东名称
    - shareholder_type: 股东类型
    """
    jq_code = ak_code_to_jq(symbol)

    from jk2bt.data.sources import get_adapter

    try:
        results = []

        data_sources = get_adapter().get_unlock_with_fallback(
            symbol=extract_code_num(symbol)
        )
        for source_name, df in data_sources:
            if source_name == "sina_queue":
                for _, row in df.iterrows():
                    record = _parse_lock_share_row(row, jq_code)
                    if record:
                        results.append(record)
            elif source_name == "em_summary":
                for _, row in df.iterrows():
                    record = _parse_lock_share_summary_row(row, jq_code)
                    if record:
                        results.append(record)

        if results:
            result_df = pd.DataFrame(results)
            result_df = result_df.drop_duplicates(
                subset=["code", "unlock_date"], keep="first"
            )
            result_df = result_df.sort_values("unlock_date")
            return result_df
    except Exception as e:
        logger.warning(f"[query_lock_share] 获取限售股份信息失败 {symbol}: {e}")

    return pd.DataFrame(columns=_LOCK_SHARE_SCHEMA)


def _parse_lock_share_row(row, jq_code: str) -> Optional[dict]:
    """解析限售股份信息行（新浪）"""
    try:
        return {
            "code": jq_code,
            "unlock_date": _parse_date(row.get("解禁日期", None)),
            "lock_amount": parse_int(row.get("解禁数量", 0)),
            "lock_type": str(row.get("上市批次", "")),
            "shareholder_name": str(row.get("名称", "")),
            "shareholder_type": str(row.get("限售股类型", "")),
        }
    except Exception:
        return None


def _parse_lock_share_summary_row(row, jq_code: str) -> Optional[dict]:
    """解析限售股份汇总信息行（东方财富）"""
    try:
        return {
            "code": jq_code,
            "unlock_date": _parse_date(row.get("解禁日期", None)),
            "lock_amount": parse_int(row.get("解禁数量", 0)),
            "lock_type": str(row.get("解禁类型", "")),
            "shareholder_name": "",
            "shareholder_type": str(row.get("限售股类型", "")),
        }
    except Exception:
        return None


def analyze_unlock_impact(
    security: str,
    force_update: bool = False,
) -> dict:
    """
    分析解禁对股价的影响。

    参数
    ----
    security    : 股票代码
    force_update: 强制更新

    返回
    ----
    dict，包含影响分析：
    - code: 股票代码
    - upcoming_unlocks: 即将解禁数量（未来30天）
    - total_unlock_amount: 解禁总量
    - avg_unlock_ratio: 平均解禁比例
    - impact_level: 影响等级（high/medium/low/none）
    - risk_factors: 风险因素列表
    - historical_impact: 历史解禁影响分析
    """
    code_num = extract_code_num(security)
    jq_code = ak_code_to_jq(security)

    result = {
        "code": jq_code,
        "upcoming_unlocks": 0,
        "total_unlock_amount": 0,
        "avg_unlock_ratio": 0.0,
        "impact_level": "none",
        "risk_factors": [],
        "historical_impact": None,
    }

    today = datetime.now()
    future_30 = (today + timedelta(days=30)).strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")

    df_future = get_unlock(
        security,
        start_date=today_str,
        end_date=future_30,
        force_update=force_update,
    )

    df_history = get_unlock_history(
        security,
        years=3,
        force_update=force_update,
    )

    if not df_future.empty:
        result["upcoming_unlocks"] = len(df_future)
        if "unlock_amount" in df_future.columns:
            result["total_unlock_amount"] = float(df_future["unlock_amount"].sum())
        if "unlock_ratio" in df_future.columns:
            ratios = df_future["unlock_ratio"].dropna()
            if not ratios.empty:
                result["avg_unlock_ratio"] = float(ratios.mean())

    if result["avg_unlock_ratio"] >= 0.05:
        result["impact_level"] = "high"
        result["risk_factors"].append("解禁比例超过5%")
    elif result["avg_unlock_ratio"] >= 0.02:
        result["impact_level"] = "medium"
        result["risk_factors"].append("解禁比例超过2%")
    elif result["avg_unlock_ratio"] > 0:
        result["impact_level"] = "low"
        result["risk_factors"].append("存在解禁计划")

    if result["upcoming_unlocks"] > 3:
        result["risk_factors"].append("短期内多次解禁")

    if not df_history.empty and len(df_history) > 0:
        historical = {
            "total_events": len(df_history),
            "max_unlock_ratio": 0.0,
            "avg_unlock_amount": 0.0,
        }
        if "unlock_ratio" in df_history.columns:
            ratios = df_history["unlock_ratio"].dropna()
            if not ratios.empty:
                historical["max_unlock_ratio"] = float(ratios.max())
        if "unlock_amount" in df_history.columns:
            amounts = df_history["unlock_amount"].dropna()
            if not amounts.empty:
                historical["avg_unlock_amount"] = float(amounts.mean())
        result["historical_impact"] = historical

    return result


def get_unlock_info_batch(
    codes: List[str],
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> RobustResult:
    """
    批量获取限售解禁信息，返回 RobustResult。

    参数
    ----
    codes       : 股票代码列表
    start_date  : 起始日期（可选）
    end_date    : 结束日期（可选）
    force_update: 强制更新

    返回
    ----
    RobustResult，包含：
    - success: 是否全部成功
    - data: DataFrame，合并所有股票的解禁信息
    - reason: 结果说明
    - source: 数据来源

    示例
    ----
    >>> result = get_unlock_info_batch(['600519', '000001'], '2024-01-01', '2024-12-31')
    >>> if result.success:
    >>>     print(f"共获取 {len(result.data)} 条解禁记录")
    """
    if not codes:
        return RobustResult(
            success=False,
            data=pd.DataFrame(columns=_UNLOCK_SCHEMA),
            reason="股票代码列表为空",
            source="input",
        )

    all_results = []
    success_count = 0
    fail_count = 0
    sources = {"cache": 0, "network": 0, "fallback": 0}

    for code in codes:
        try:
            result = get_unlock_info(
                code,
                start_date=start_date,
                end_date=end_date,
                force_update=force_update,
            )
            if result.success and not result.is_empty():
                all_results.append(result.data)
                success_count += 1
            else:
                fail_count += 1
            sources[result.source] = sources.get(result.source, 0) + 1
        except Exception as e:
            logger.warning(f"[get_unlock_info_batch] 获取 {code} 失败: {e}")
            fail_count += 1

    if not all_results:
        return RobustResult(
            success=False,
            data=pd.DataFrame(columns=_UNLOCK_SCHEMA),
            reason=f"批量查询失败: 0/{len(codes)} 成功",
            source="network",
        )

    combined_df = pd.concat(all_results, ignore_index=True)

    primary_source = max(sources, key=sources.get)
    all_success = fail_count == 0

    return RobustResult(
        success=all_success,
        data=combined_df,
        reason=f"批量查询完成: {success_count}/{len(codes)} 成功，共 {len(combined_df)} 条记录",
        source=primary_source,
    )


# 向后兼容导出
from jk2bt.utils.symbol import extract_code_num as _extract_code_num

UNLOCK_CACHE_DAYS = 7
from jk2bt.utils.symbol import ak_code_to_jq as _normalize_to_jq
from jk2bt.utils.date_utils import parse_int as _parse_num
from jk2bt.utils.date_utils import filter_by_date_range as _filter_by_date_range
