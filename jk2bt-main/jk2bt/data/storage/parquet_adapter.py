"""
db/parquet_adapter.py
Parquet 缓存适配层，完全模拟 DuckDBManager 的公开接口。
内部委托给 parquet_cache，实现最小化代码迁移。
"""

import logging
import os
import threading
from typing import Optional, List

import pandas as pd

from jk2bt.cache import get_cache_manager, CacheManager
from jk2bt.utils.symbol import ak_code_to_jq as normalize_to_jq_format

logger = logging.getLogger(__name__)

_PROCESS_SINGLETONS = {}
_SINGLETON_LOCK = threading.Lock()

_TABLE_MAP = {
    "stock_daily": "stock_daily",
    "etf_daily": "etf_daily",
    "lof_daily": "etf_daily",
    "index_daily": "index_daily",
    "stock_minute": "stock_minute",
    "etf_minute": "etf_minute",
}


class ParquetAdapter:
    def __init__(self, db_path=None, read_only=False, use_cache=True):
        if db_path is None:
            try:
                from jk2bt.utils.config import get_config

                config = get_config()
                base_dir = config.cache.parquet_cache_dir
            except Exception:
                base_dir = os.path.join(
                    os.path.dirname(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    ),
                    "data",
                    "parquet_cache",
                )
        else:
            base_dir = db_path

        self.db_path = db_path
        self.read_only = read_only
        self.use_cache = use_cache
        self._cache_manager: Optional[CacheManager] = None
        self._base_dir = base_dir

    @property
    def cache_manager(self) -> CacheManager:
        if self._cache_manager is None:
            self._cache_manager = get_cache_manager(base_dir=self._base_dir)
        return self._cache_manager

    def _init_database(self):
        """初始化数据库表结构（对于ParquetAdapter，确保缓存目录存在）"""
        os.makedirs(self._base_dir, exist_ok=True)
        os.makedirs(os.path.join(self._base_dir, "meta"), exist_ok=True)
        os.makedirs(os.path.join(self._base_dir, "daily"), exist_ok=True)

    def _to_jq(self, symbol: str) -> str:
        return normalize_to_jq_format(symbol)

    def _rename_to_date(self, df: pd.DataFrame) -> pd.DataFrame:
        if "datetime" in df.columns and "date" not in df.columns:
            df = df.rename(columns={"datetime": "date"})
        if "date" in df.columns:
            try:
                if df["date"].isna().all():
                    df["date"] = df["date"].astype(object)
                else:
                    df["date"] = pd.to_datetime(df["date"]).dt.date
            except Exception:
                pass
        return df

    def _rename_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        if "date" in df.columns and "datetime" not in df.columns:
            df = df.rename(columns={"date": "datetime"})
        return df

    def _ensure_amount(self, df: pd.DataFrame) -> pd.DataFrame:
        if "amount" not in df.columns:
            df["amount"] = 0
        return df

    def _ensure_money(self, df: pd.DataFrame) -> pd.DataFrame:
        if "money" not in df.columns:
            df["money"] = df.get("amount", 0)
        return df

    def _select_columns(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        return df[[c for c in columns if c in df.columns]]

    def _put_partitioned(self, table: str, df: pd.DataFrame, partition_col: str):
        """按分区列分组写入 parquet_cache"""
        if partition_col in df.columns:
            for value, group in df.groupby(partition_col):
                self.cache_manager.put(table, group, partition_value=str(value))
        else:
            self.cache_manager.put(table, df)

    def insert_stock_daily(self, symbol: str, df: pd.DataFrame, adjust: str = "qfq"):
        if df is None or df.empty:
            logger.warning(f"{symbol}: 无数据需要插入")
            return

        jq_symbol = self._to_jq(symbol)
        df = df.copy()
        df["symbol"] = jq_symbol
        df["adjust"] = adjust
        df = self._rename_to_date(df)
        df = self._ensure_amount(df)
        df = self._select_columns(
            df,
            [
                "symbol",
                "date",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "amount",
                "adjust",
            ],
        )

        self._put_partitioned("stock_daily", df, "date")
        logger.info(f"{jq_symbol} ({adjust}): 插入 {len(df)} 条数据")

    def insert_etf_daily(self, symbol: str, df: pd.DataFrame):
        if df is None or df.empty:
            logger.warning(f"{symbol}: 无数据需要插入")
            return

        jq_symbol = self._to_jq(symbol)
        df = df.copy()
        df["symbol"] = jq_symbol
        df = self._rename_to_date(df)
        df = self._ensure_amount(df)
        df = self._select_columns(
            df, ["symbol", "date", "open", "high", "low", "close", "volume", "amount"]
        )

        self._put_partitioned("etf_daily", df, "date")
        logger.info(f"{jq_symbol}: 插入 {len(df)} 条数据")

    def insert_lof_daily(self, symbol: str, df: pd.DataFrame):
        if df is None or df.empty:
            logger.warning(f"{symbol}: 无数据需要插入")
            return

        jq_symbol = self._to_jq(symbol)
        df = df.copy()
        df["symbol"] = jq_symbol
        df = self._rename_to_date(df)
        df = self._ensure_amount(df)
        df = self._select_columns(
            df, ["symbol", "date", "open", "high", "low", "close", "volume", "amount"]
        )

        self._put_partitioned("etf_daily", df, "date")
        logger.info(f"{jq_symbol}: 插入 {len(df)} 条数据")

    def insert_index_daily(self, symbol: str, df: pd.DataFrame):
        if df is None or df.empty:
            logger.warning(f"{symbol}: 无数据需要插入")
            return

        jq_symbol = self._to_jq(symbol)
        df = df.copy()
        df["symbol"] = jq_symbol
        df = self._rename_to_date(df)
        df = self._ensure_amount(df)
        df = self._select_columns(
            df, ["symbol", "date", "open", "high", "low", "close", "volume", "amount"]
        )

        self._put_partitioned("index_daily", df, "date")
        logger.info(f"{jq_symbol}: 插入 {len(df)} 条数据")

    def insert_stock_minute(
        self, symbol: str, period: str, df: pd.DataFrame, adjust: str = "qfq"
    ):
        if df is None or df.empty:
            logger.warning(f"{symbol} ({period}): 无数据需要插入")
            return

        jq_symbol = self._to_jq(symbol)
        df = df.copy()
        df["symbol"] = jq_symbol
        df["period"] = period
        df["adjust"] = adjust
        df = self._ensure_money(df)
        df = self._select_columns(
            df,
            [
                "symbol",
                "datetime",
                "period",
                "adjust",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "money",
            ],
        )

        if "datetime" in df.columns:
            df["week"] = pd.to_datetime(df["datetime"]).dt.strftime("%Y-W%W")

        self._put_partitioned("stock_minute", df, "week")
        logger.info(f"{jq_symbol} ({period} {adjust}): 插入 {len(df)} 条分钟数据")

    def insert_etf_minute(self, symbol: str, period: str, df: pd.DataFrame):
        if df is None or df.empty:
            logger.warning(f"{symbol} ({period}): 无数据需要插入")
            return

        jq_symbol = self._to_jq(symbol)
        df = df.copy()
        df["symbol"] = jq_symbol
        df["period"] = period
        df = self._ensure_money(df)
        df = self._select_columns(
            df,
            [
                "symbol",
                "datetime",
                "period",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "money",
            ],
        )

        if "datetime" in df.columns:
            df["week"] = pd.to_datetime(df["datetime"]).dt.strftime("%Y-W%W")

        self._put_partitioned("etf_minute", df, "week")
        logger.info(f"{jq_symbol} ({period}): 插入 {len(df)} 条分钟数据")

    def get_stock_daily(
        self,
        symbol: str,
        start: str,
        end: str,
        adjust: str = "qfq",
        use_cache: bool = None,
    ) -> pd.DataFrame:
        if use_cache is None:
            use_cache = self.use_cache

        jq_symbol = self._to_jq(symbol)
        where = {"symbol": jq_symbol, "adjust": adjust, "date": (start, end)}
        columns = ["date", "open", "high", "low", "close", "volume", "amount"]

        result = self.cache_manager.get(
            "stock_daily",
            where=where,
            columns=columns,
            order_by=["date"],
            force_refresh=not use_cache,
        )

        if result is None or result.empty:
            logger.warning(f"{jq_symbol} ({adjust}): 数据库中无数据")
            return pd.DataFrame()

        result = self._rename_to_datetime(result)
        logger.info(
            f"{jq_symbol} ({adjust}): 查询到 {len(result)} 条数据 ({start} ~ {end})"
        )
        return result

    def get_etf_daily(
        self, symbol: str, start: str, end: str, use_cache: bool = None
    ) -> pd.DataFrame:
        if use_cache is None:
            use_cache = self.use_cache

        jq_symbol = self._to_jq(symbol)
        where = {"symbol": jq_symbol, "date": (start, end)}
        columns = ["date", "open", "high", "low", "close", "volume", "amount"]

        result = self.cache_manager.get(
            "etf_daily",
            where=where,
            columns=columns,
            order_by=["date"],
            force_refresh=not use_cache,
        )

        if result is None or result.empty:
            logger.warning(f"{jq_symbol}: 数据库中无数据")
            return pd.DataFrame()

        result = self._rename_to_datetime(result)
        logger.info(f"{jq_symbol}: 查询到 {len(result)} 条数据 ({start} ~ {end})")
        return result

    def get_lof_daily(
        self, symbol: str, start: str, end: str, use_cache: bool = None
    ) -> pd.DataFrame:
        if use_cache is None:
            use_cache = self.use_cache

        jq_symbol = self._to_jq(symbol)
        where = {"symbol": jq_symbol, "date": (start, end)}
        columns = ["date", "open", "high", "low", "close", "volume", "amount"]

        result = self.cache_manager.get(
            "etf_daily",
            where=where,
            columns=columns,
            order_by=["date"],
            force_refresh=not use_cache,
        )

        if result is None or result.empty:
            logger.warning(f"{jq_symbol}: 数据库中无数据")
            return pd.DataFrame()

        result = self._rename_to_datetime(result)
        logger.info(f"{jq_symbol}: 查询到 {len(result)} 条数据 ({start} ~ {end})")
        return result

    def get_index_daily(
        self, symbol: str, start: str, end: str, use_cache: bool = None
    ) -> pd.DataFrame:
        if use_cache is None:
            use_cache = self.use_cache

        jq_symbol = self._to_jq(symbol)
        where = {"symbol": jq_symbol, "date": (start, end)}
        columns = ["date", "open", "high", "low", "close", "volume", "amount"]

        result = self.cache_manager.get(
            "index_daily",
            where=where,
            columns=columns,
            order_by=["date"],
            force_refresh=not use_cache,
        )

        if result is None or result.empty:
            logger.warning(f"{jq_symbol}: 数据库中无数据")
            return pd.DataFrame()

        result = self._rename_to_datetime(result)
        logger.info(f"{jq_symbol}: 查询到 {len(result)} 条数据 ({start} ~ {end})")
        return result

    def get_stock_minute(
        self,
        symbol: str,
        period: str,
        start: str,
        end: str,
        adjust: str = "qfq",
        use_cache: bool = None,
    ) -> pd.DataFrame:
        if use_cache is None:
            use_cache = self.use_cache

        jq_symbol = self._to_jq(symbol)
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
        where = {
            "symbol": jq_symbol,
            "period": period,
            "adjust": adjust,
            "datetime": (start_dt, end_dt),
        }
        columns = ["datetime", "open", "high", "low", "close", "volume", "money"]

        result = self.cache_manager.get(
            "stock_minute",
            where=where,
            columns=columns,
            order_by=["datetime"],
            force_refresh=not use_cache,
        )

        if result is None or result.empty:
            logger.warning(f"{jq_symbol} ({period} {adjust}): 数据库中无分钟数据")
            return pd.DataFrame()

        logger.info(f"{jq_symbol} ({period} {adjust}): 查询到 {len(result)} 条分钟数据")
        return result

    def get_etf_minute(
        self, symbol: str, period: str, start: str, end: str, use_cache: bool = None
    ) -> pd.DataFrame:
        if use_cache is None:
            use_cache = self.use_cache

        jq_symbol = self._to_jq(symbol)
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
        where = {"symbol": jq_symbol, "period": period, "datetime": (start_dt, end_dt)}
        columns = ["datetime", "open", "high", "low", "close", "volume", "money"]

        result = self.cache_manager.get(
            "etf_minute",
            where=where,
            columns=columns,
            order_by=["datetime"],
            force_refresh=not use_cache,
        )

        if result is None or result.empty:
            logger.warning(f"{jq_symbol} ({period}): 数据库中无分钟数据")
            return pd.DataFrame()

        logger.info(f"{jq_symbol} ({period}): 查询到 {len(result)} 条分钟数据")
        return result

    def has_data(
        self,
        table: str,
        symbol: str,
        start: str,
        end: str,
        adjust: str = None,
        period: str = None,
    ) -> bool:
        jq_symbol = self._to_jq(symbol)
        pc_table = _TABLE_MAP.get(table, table)

        where = {"symbol": jq_symbol}
        if adjust is not None:
            where["adjust"] = adjust
        if period is not None:
            where["period"] = period

        result = self.cache_manager.get(
            pc_table,
            where=where,
            columns=["date"] if "minute" not in table else ["datetime"],
            order_by=["date"] if "daily" in table else ["datetime"],
        )

        if result is None or result.empty:
            return False

        date_col = "date" if "date" in result.columns else "datetime"
        min_date = pd.to_datetime(result[date_col].min())
        max_date = pd.to_datetime(result[date_col].max())
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)

        return min_date <= start_dt and max_date >= end_dt

    def count_records(self, table: str, symbol: str = None, adjust: str = None) -> int:
        pc_table = _TABLE_MAP.get(table, table)
        where = {}
        if symbol is not None:
            where["symbol"] = self._to_jq(symbol)
        if adjust is not None:
            where["adjust"] = adjust

        return self.cache_manager.query_engine.count(
            pc_table,
            self.cache_manager.registry.get(pc_table).storage_layer,
            partition_by=self.cache_manager.registry.get(pc_table).partition_by,
            where=where if where else None,
        )

    def query(self, table: str, where: dict = None) -> pd.DataFrame:
        """兼容 cache_status.py 等旧代码的查询接口"""
        pc_table = _TABLE_MAP.get(table, table)
        result = self.cache_manager.get(pc_table, where=where)
        if result is None or result.empty:
            return pd.DataFrame()
        return self._rename_to_datetime(result)

    def get_symbols(self, table: str) -> List[str]:
        pc_table = _TABLE_MAP.get(table, table)
        result = self.cache_manager.get(pc_table, columns=["symbol"])
        if result is None or result.empty:
            return []
        return sorted(result["symbol"].unique().tolist())

    def clear_cache(self):
        self.cache_manager.memory_cache.invalidate()
        logger.info("本地缓存已清除")

    def close(self):
        self.clear_cache()

    def __del__(self):
        pass


def get_shared_read_only_manager(
    db_path=None, use_cache: bool = True
) -> "ParquetAdapter":
    cache_key = f"ro:{db_path}:{use_cache}"
    global _PROCESS_SINGLETONS, _SINGLETON_LOCK
    with _SINGLETON_LOCK:
        if cache_key not in _PROCESS_SINGLETONS:
            _PROCESS_SINGLETONS[cache_key] = ParquetAdapter(
                db_path=db_path, read_only=True, use_cache=use_cache
            )
        return _PROCESS_SINGLETONS[cache_key]


def get_writer_manager(db_path=None, use_cache: bool = False) -> "ParquetAdapter":
    cache_key = f"rw:{db_path}:{use_cache}"
    global _PROCESS_SINGLETONS, _SINGLETON_LOCK
    with _SINGLETON_LOCK:
        if cache_key not in _PROCESS_SINGLETONS:
            _PROCESS_SINGLETONS[cache_key] = ParquetAdapter(
                db_path=db_path, read_only=False, use_cache=use_cache
            )
        return _PROCESS_SINGLETONS[cache_key]


def get_manager(
    db_path=None, read_only: bool = False, use_cache: bool = True
) -> "ParquetAdapter":
    if read_only:
        return get_shared_read_only_manager(db_path=db_path, use_cache=use_cache)
    else:
        return get_writer_manager(db_path=db_path, use_cache=use_cache)


# 兼容旧测试用例的 LocalCache 存根
class LocalCache:
    """兼容旧 DuckDBManager.LocalCache 的存根类"""

    def __init__(self, max_size: int = 1000):
        self._max_size = max_size

    def get(self, *args, **kwargs):
        return None

    def set(self, *args, **kwargs):
        pass

    def invalidate(self, *args, **kwargs):
        pass

    def clear(self):
        pass


def clear_global_cache():
    """兼容旧 duckdb_manager.clear_global_cache()"""
    global _PROCESS_SINGLETONS
    _PROCESS_SINGLETONS.clear()
