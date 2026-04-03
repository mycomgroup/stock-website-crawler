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
- DuckDB 缓存（优先）：存储在 data/share_change.db 中
- 按周缓存：动态数据
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Union, Dict
import logging
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

try:
    from ..index_fundamentals_robust import RobustResult
except ImportError:
    try:
        from index_fundamentals_robust import RobustResult
    except ImportError:

        class RobustResult:
            def __init__(self, success=True, data=None, reason="", source="network"):
                self.success = success
                self.data = data if data is not None else pd.DataFrame()
                self.reason = reason
                self.source = source

            def __bool__(self):
                return self.success

            def __repr__(self):
                status = "SUCCESS" if self.success else "FAILED"
                return f"<RobustResult[{status}] source={self.source} reason='{self.reason}' data_type={type(self.data).__name__}>"

            def is_empty(self):
                if isinstance(self.data, pd.DataFrame):
                    return self.data.empty
                elif isinstance(self.data, (list, tuple)):
                    return len(self.data) == 0
                return self.data is None


SHARE_CHANGE_CACHE_DAYS = 7

_DUCKDB_AVAILABLE = False
try:
    from ..db.duckdb_manager import DuckDBManager

    _DUCKDB_AVAILABLE = True
except ImportError:
    try:
        from jk2bt.db.duckdb_manager import DuckDBManager

        _DUCKDB_AVAILABLE = True
    except ImportError:
        logger.warning("DuckDB 模块不可用，将使用 pickle 缓存")


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


class ShareChangeDBManager:
    """股东变动 DuckDB 管理器"""

    _instance = None

    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_manager(db_path)
        return cls._instance

    def _init_manager(self, db_path: str = None):
        if not _DUCKDB_AVAILABLE:
            self._manager = None
            return

        if db_path is None:
            base_dir = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            db_path = os.path.join(base_dir, "data", "share_change.db")

        self.db_path = db_path
        self._manager = None

        try:
            self._manager = DuckDBManager(db_path=db_path, read_only=False)
            self._init_tables()
        except Exception as e:
            logger.warning(f"DuckDB 初始化失败: {e}")
            self._manager = None

    def _init_tables(self):
        if self._manager is None:
            return

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS share_change (
                        code VARCHAR NOT NULL,
                        shareholder_name VARCHAR,
                        change_date DATE NOT NULL,
                        change_type VARCHAR,
                        change_amount BIGINT,
                        change_ratio DOUBLE,
                        hold_amount_after BIGINT,
                        hold_ratio_after DOUBLE,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (code, shareholder_name, change_date)
                    )
                """)
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_shchg_code ON share_change(code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_shchg_date ON share_change(change_date)"
                )
                logger.info("股东变动表结构初始化完成")
        except Exception as e:
            logger.warning(f"初始化表结构失败: {e}")

    def insert_share_change(self, df: pd.DataFrame):
        if self._manager is None or df.empty:
            return

        df = df.copy()
        for col in _SHARE_CHANGE_SCHEMA:
            if col not in df.columns:
                df[col] = None

        if "update_time" not in df.columns:
            df["update_time"] = datetime.now()

        cols = _SHARE_CHANGE_SCHEMA + ["update_time"]
        df = df[cols]

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("INSERT OR REPLACE INTO share_change SELECT * FROM df")
                logger.info(f"插入/更新 {len(df)} 条股东变动信息")
        except Exception as e:
            logger.warning(f"插入股东变动信息失败: {e}")

    def get_share_change(
        self, code: str, start_date: str = None, end_date: str = None
    ) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)

        try:
            with self._manager._get_connection(read_only=True) as conn:
                if start_date and end_date:
                    df = conn.execute(
                        "SELECT * FROM share_change WHERE code = ? AND change_date >= ? AND change_date <= ? ORDER BY change_date DESC",
                        [code, start_date, end_date],
                    ).fetchdf()
                else:
                    df = conn.execute(
                        "SELECT * FROM share_change WHERE code = ? ORDER BY change_date DESC",
                        [code],
                    ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询股东变动信息失败: {e}")
            return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)

    def is_cache_valid(self, code: str, cache_days: int = 7) -> bool:
        if self._manager is None:
            return False

        try:
            with self._manager._get_connection(read_only=True) as conn:
                result = conn.execute(
                    "SELECT MAX(update_time) FROM share_change WHERE code = ?",
                    [code],
                ).fetchone()
                if result and result[0]:
                    update_time = pd.to_datetime(result[0])
                    return (datetime.now() - update_time).days < cache_days
                return False
        except Exception:
            return False


_db_manager = ShareChangeDBManager() if _DUCKDB_AVAILABLE else None


def _extract_code_num(symbol: str) -> str:
    if symbol.startswith("sh") or symbol.startswith("sz"):
        return symbol[2:].zfill(6)
    if ".XSHG" in symbol or ".XSHE" in symbol:
        return symbol.split(".")[0].zfill(6)
    return symbol.zfill(6)


def _normalize_to_jq(symbol: str) -> str:
    if ".XSHG" in symbol or ".XSHE" in symbol:
        return symbol
    if symbol.startswith("sh"):
        return symbol[2:] + ".XSHG"
    if symbol.startswith("sz"):
        return symbol[2:] + ".XSHE"
    code = symbol.zfill(6)
    if code.startswith("6"):
        return code + ".XSHG"
    return code + ".XSHE"


def _parse_date(date_str) -> Optional[str]:
    if not date_str or pd.isna(date_str):
        return None
    date_str = str(date_str).strip()
    for fmt in ["%Y-%m-%d", "%Y%m%d", "%Y/%m/%d"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def _parse_num(value) -> Optional[int]:
    if value is None or value == "" or value == "-":
        return None
    try:
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        return int(float(value))
    except (ValueError, TypeError):
        return None


def _parse_ratio(value) -> Optional[float]:
    if value is None or value == "" or value == "-":
        return None
    try:
        if isinstance(value, str):
            value = value.replace("%", "").strip()
            return float(value) / 100 if float(value) > 1 else float(value)
        return float(value)
    except (ValueError, TypeError):
        return None


def get_share_change(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
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
    cache_dir   : 缓存目录
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
    code_num = _extract_code_num(symbol)
    jq_code = _normalize_to_jq(symbol)

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(jq_code, cache_days=7):
            df_cached = _db_manager.get_share_change(jq_code, start_date, end_date)
            if not df_cached.empty:
                return df_cached[_SHARE_CHANGE_SCHEMA]

    cache_file = os.path.join(cache_dir, f"share_change_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 7:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_share_change(cached_df)
                if start_date is None and end_date is None:
                    return cached_df
                return _filter_by_date_range(cached_df, start_date, end_date)
            need_download = True
        except Exception:
            need_download = True

    if need_download:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        try:
            df = ak.stock_shareholder_change_ths(symbol=code_num)
            if df is not None and not df.empty:
                result = _normalize_share_change(df, jq_code)
                if not result.empty:
                    result.to_pickle(cache_file)
                    if use_duckdb and _db_manager is not None:
                        _db_manager.insert_share_change(result)
                    if start_date is None and end_date is None:
                        return result
                    return _filter_by_date_range(result, start_date, end_date)
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


def _filter_by_date_range(
    df: pd.DataFrame, start_date: str, end_date: str
) -> pd.DataFrame:
    """按日期范围筛选数据"""
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


def query_share_change(
    symbols: List[str],
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
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
                cache_dir=cache_dir,
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

    def run_query(
        self, query_obj, cache_dir="finance_cache", force_update=False, use_duckdb=True
    ) -> pd.DataFrame:
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
                return get_share_change(
                    conditions["code"], cache_dir=cache_dir, use_duckdb=use_duckdb
                )
            return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)
        else:
            raise ValueError(f"不支持的表: {table_name}")


finance = FinanceQuery()


def run_query_simple(
    table: str,
    code: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """简化的查询接口"""
    if table == "STK_SHAREHOLDER_CHANGE":
        if code:
            return get_share_change(
                code, cache_dir=cache_dir, force_update=force_update
            )
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
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """获取股权质押信息"""
    code_num = _extract_code_num(symbol)
    jq_code = _normalize_to_jq(symbol)

    cache_file = os.path.join(cache_dir, f"pledge_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 7:
                return cached_df
            need_download = True
        except Exception:
            need_download = True

    if need_download:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        try:
            df_raw = ak.stock_gpzy_pledge_ratio_em(symbol=code_num)
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
                result.to_pickle(cache_file)
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
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """获取重要股东交易信息"""
    return get_share_change(symbol, cache_dir=cache_dir, force_update=force_update)


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
    cache_dir: str = "finance_cache",
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
    cache_dir    : 缓存目录
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

    code_num = _extract_code_num(code)
    jq_code = _normalize_to_jq(code)

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

    cache_file = os.path.join(cache_dir, f"shareholder_changes_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < SHARE_CHANGE_CACHE_DAYS:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_share_change(cached_df)
                if start_date is None and end_date is None:
                    df_result = cached_df.copy()
                    if "change_reason" not in df_result.columns:
                        df_result["change_reason"] = None
                    return RobustResult(
                        success=True,
                        data=df_result[_SHAREHOLDER_CHANGES_SCHEMA],
                        reason=f"从缓存获取{len(df_result)}条股东变动记录",
                        source="cache",
                    )
                df_filtered = _filter_by_date_range(cached_df, start_date, end_date)
                if "change_reason" not in df_filtered.columns:
                    df_filtered["change_reason"] = None
                return RobustResult(
                    success=True,
                    data=df_filtered[_SHAREHOLDER_CHANGES_SCHEMA],
                    reason=f"从缓存获取{len(df_filtered)}条股东变动记录",
                    source="cache",
                )
            need_download = True
        except Exception as e:
            logger.warning(f"读取缓存失败: {e}")
            need_download = True

    if need_download:
        try:
            df = _fetch_shareholder_changes_from_akshare(code_num, jq_code)
            if df is not None and not df.empty:
                df_result = df.copy()
                if "change_reason" not in df_result.columns:
                    df_result["change_reason"] = None
                df_to_cache = df_result[_SHAREHOLDER_CHANGES_SCHEMA].copy()
                df_to_cache.to_pickle(cache_file)
                if use_duckdb and _db_manager is not None:
                    cache_df = df_to_cache.copy()
                    cache_df = cache_df[
                        [c for c in cache_df.columns if c != "change_reason"]
                    ]
                    _db_manager.insert_share_change(cache_df)

                if start_date or end_date:
                    df_result = _filter_by_date_range(df_result, start_date, end_date)
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

    if os.path.exists(cache_file):
        try:
            cached_df = pd.read_pickle(cache_file)
            if "change_reason" not in cached_df.columns:
                cached_df["change_reason"] = None
            if start_date or end_date:
                cached_df = _filter_by_date_range(cached_df, start_date, end_date)
            return RobustResult(
                success=True,
                data=cached_df[_SHAREHOLDER_CHANGES_SCHEMA],
                reason=f"网络失败，使用缓存兜底获取{len(cached_df)}条记录",
                source="fallback",
            )
        except Exception as e:
            logger.warning(f"读取缓存兜底失败: {e}")

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
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")
    try:
        df = ak.stock_gdfx_holding_change_em(symbol=code_num)
        if df is not None and not df.empty:
            return _normalize_shareholder_changes(df, jq_code)
    except Exception as e:
        logger.warning(f"ak.stock_gdfx_holding_change_em 失败: {e}")

    try:
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
        df = ak.stock_share_change_cninfo(
            symbol=code_num, start_date=start_date, end_date=end_date
        )
        if df is not None and not df.empty:
            return _normalize_shareholder_changes_from_cninfo(df, jq_code)
    except Exception as e:
        logger.warning(f"ak.stock_share_change_cninfo 失败: {e}")

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
        cache_dir: str = "finance_cache",
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
                    cache_dir=cache_dir,
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
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取高管增减持信息。

    参数
    ----
    security    : 股票代码
    start_date  : 起始日期
    end_date    : 结束日期
    cache_dir   : 缓存目录
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
    code_num = _extract_code_num(security)
    jq_code = _normalize_to_jq(security)

    cache_file = os.path.join(cache_dir, f"insider_trading_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < SHARE_CHANGE_CACHE_DAYS:
                if start_date is None and end_date is None:
                    return cached_df
                return _filter_by_date_range(cached_df, start_date, end_date)
            need_download = True
        except Exception:
            need_download = True

    if need_download:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        try:
            df_raw = None
            try:
                df_raw = ak.stock_gdfx_holding_change_em(symbol=code_num)
            except Exception as e1:
                logger.warning(f"stock_gdfx_holding_change_em 失败: {e1}")
                try:
                    end_date_str = datetime.now().strftime("%Y%m%d")
                    start_date_str = (datetime.now() - timedelta(days=365)).strftime(
                        "%Y%m%d"
                    )
                    df_raw = ak.stock_share_change_cninfo(
                        symbol=code_num,
                        start_date=start_date_str,
                        end_date=end_date_str,
                    )
                except Exception as e2:
                    logger.warning(f"stock_share_change_cninfo 失败: {e2}")

            if df_raw is not None and not df_raw.empty:
                result = _normalize_insider_trading(df_raw, jq_code)
                if not result.empty:
                    result.to_pickle(cache_file)
                    if start_date is None and end_date is None:
                        return result
                    return _filter_by_date_range(result, start_date, end_date)
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
    cache_dir: str = "finance_cache",
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
    cache_dir   : 缓存目录
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
        cache_dir=cache_dir,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )


def analyze_share_change_trend(
    security: str,
    period_days: int = 90,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> Dict:
    """
    分析股东变动趋势。

    参数
    ----
    security    : 股票代码
    period_days : 分析周期（天数），默认90天
    cache_dir   : 缓存目录
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
            cache_dir=cache_dir,
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
            cache_dir=cache_dir,
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
        cache_dir: str = "finance_cache",
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
                    cache_dir=cache_dir,
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
            return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)
        elif table_name == "STK_SHAREHOLDER_CHANGE":
            if "code" in conditions:
                return get_shareholder_changes(
                    conditions["code"],
                    cache_dir=cache_dir,
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
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取股份冻结信息。

    参数
    ----
    symbol      : 股票代码
    cache_dir   : 缓存目录
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
    code_num = _extract_code_num(symbol)
    jq_code = _normalize_to_jq(symbol)

    cache_file = os.path.join(cache_dir, f"freeze_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < SHARE_CHANGE_CACHE_DAYS:
                return cached_df
            need_download = True
        except Exception:
            need_download = True

    if need_download:
        try:
            df_raw = _fetch_freeze_data_from_akshare(code_num)
            if df_raw is not None and not df_raw.empty:
                result = _normalize_freeze_data(df_raw, jq_code)
                if not result.empty:
                    result.to_pickle(cache_file)
                    return result
        except Exception as e:
            logger.warning(f"[get_freeze_info] 获取冻结信息失败 {symbol}: {e}")

    return pd.DataFrame(columns=_FREEZE_SCHEMA)


def _fetch_freeze_data_from_akshare(code_num: str) -> Optional[pd.DataFrame]:
    """从 akshare 获取冻结数据"""
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")
    try:
        df = ak.stock_cg_equity_mortgage_cninfo(symbol=code_num)
        if df is not None and not df.empty:
            return df
    except Exception as e:
        logger.warning(f"stock_cg_equity_mortgage_cninfo 失败: {e}")

    try:
        df = ak.stock_shareholder_change_ths(symbol=code_num)
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
    "change_type",
    "change_amount",
    "change_date",
    "change_reason",
    "total_capital_before",
    "total_capital_after",
    "circulating_capital_before",
    "circulating_capital_after",
]


def get_capital_change(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
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
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，包含股本变动信息：
    - code: 股票代码（聚宽格式）
    - change_type: 变动类型
    - change_amount: 变动数量
    - change_date: 变动日期
    - change_reason: 变动原因
    - total_capital_before: 变动前总股本
    - total_capital_after: 变动后总股本
    - circulating_capital_before: 变动前流通股本
    - circulating_capital_after: 变动后流通股本
    """
    code_num = _extract_code_num(symbol)
    jq_code = _normalize_to_jq(symbol)

    cache_file = os.path.join(cache_dir, f"capital_change_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < SHARE_CHANGE_CACHE_DAYS:
                if start_date is None and end_date is None:
                    return cached_df
                return _filter_capital_by_date(cached_df, start_date, end_date)
            need_download = True
        except Exception:
            need_download = True

    if need_download:
        try:
            df_raw = _fetch_capital_change_from_akshare(code_num, start_date, end_date)
            if df_raw is not None and not df_raw.empty:
                result = _normalize_capital_change(df_raw, jq_code)
                if not result.empty:
                    result.to_pickle(cache_file)
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
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")
    try:
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365 * 3)).strftime("%Y%m%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        df = ak.stock_share_change_cninfo(
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
        "变动类型": "change_type",
        "变动股份数量": "change_amount",
        "变动数量": "change_amount",
        "公告日期": "change_date",
        "变动日期": "change_date",
        "变动原因": "change_reason",
        "变动前总股本": "total_capital_before",
        "变动后总股本": "total_capital_after",
        "变动前流通股": "circulating_capital_before",
        "变动后流通股": "circulating_capital_after",
    }

    for src, target in col_map.items():
        if src in df.columns:
            if target == "change_date":
                result[target] = df[src].apply(_parse_date)
            elif target in [
                "change_amount",
                "total_capital_before",
                "total_capital_after",
                "circulating_capital_before",
                "circulating_capital_after",
            ]:
                result[target] = df[src].apply(_parse_num)
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
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取前十大股东变动信息。

    参数
    ----
    symbol      : 股票代码
    start_date  : 起始日期
    end_date    : 结束日期
    cache_dir   : 缓存目录
    force_update: 强制更新

    返回
    ----
    DataFrame，包含前十大股东变动信息
    """
    code_num = _extract_code_num(symbol)
    jq_code = _normalize_to_jq(symbol)

    cache_file = os.path.join(cache_dir, f"topholder_change_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < SHARE_CHANGE_CACHE_DAYS:
                if start_date is None and end_date is None:
                    return cached_df
                return _filter_by_date_range(cached_df, start_date, end_date)
            need_download = True
        except Exception:
            need_download = True

    if need_download:
        try:
            df_raw = _fetch_topholder_change_from_akshare(code_num)
            if df_raw is not None and not df_raw.empty:
                result = _normalize_topholder_change(df_raw, jq_code)
                if not result.empty:
                    result.to_pickle(cache_file)
                    if start_date is None and end_date is None:
                        return result
                    return _filter_by_date_range(result, start_date, end_date)
        except Exception as e:
            logger.warning(
                f"[get_topholder_change] 获取前十大股东变动失败 {symbol}: {e}"
            )

    return pd.DataFrame(columns=_TOPHOLDER_CHANGE_SCHEMA)


def _fetch_topholder_change_from_akshare(code_num: str) -> Optional[pd.DataFrame]:
    """从 akshare 获取前十大股东变动数据"""
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")
    try:
        df = ak.stock_gdfx_holding_change_em(date=datetime.now().strftime("%Y%m%d"))
        if df is not None and not df.empty:
            code_filter = (
                df[df["股票代码"] == code_num] if "股票代码" in df.columns else df
            )
            return code_filter if not code_filter.empty else None
    except Exception as e:
        logger.warning(f"stock_gdfx_holding_change_em 失败: {e}")

    try:
        df = ak.stock_shareholder_change_ths(symbol=code_num)
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
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    批量查询质押信息。

    参数
    ----
    symbols     : 股票代码列表
    cache_dir   : 缓存目录
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
            df = get_pledge_info(symbol, cache_dir=cache_dir, force_update=force_update)
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
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    批量查询冻结信息。

    参数
    ----
    symbols     : 股票代码列表
    cache_dir   : 缓存目录
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
            df = get_freeze_info(symbol, cache_dir=cache_dir, force_update=force_update)
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
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    批量查询股本变动信息。

    参数
    ----
    symbols     : 股票代码列表
    start_date  : 起始日期
    end_date    : 结束日期
    cache_dir   : 缓存目录
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
                cache_dir=cache_dir,
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
        change_type = None
        change_amount = None
        change_date = None
        change_reason = None
        total_capital_before = None
        total_capital_after = None

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
        cache_dir: str = "finance_cache",
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
                return get_pledge_info(
                    conditions["code"], cache_dir=cache_dir, force_update=force_update
                )
            return pd.DataFrame(columns=_PLEDGE_SCHEMA)
        elif table_name == "STK_SHARE_FREEZE":
            if "code" in conditions:
                return get_freeze_info(
                    conditions["code"], cache_dir=cache_dir, force_update=force_update
                )
            return pd.DataFrame(columns=_FREEZE_SCHEMA)
        elif table_name == "STK_TOPHOLDER_CHANGE":
            if "code" in conditions:
                return get_topholder_change(
                    conditions["code"], cache_dir=cache_dir, force_update=force_update
                )
            return pd.DataFrame(columns=_TOPHOLDER_CHANGE_SCHEMA)
        elif table_name == "STK_CAPITAL_CHANGE":
            if "code" in conditions:
                return get_capital_change(
                    conditions["code"], cache_dir=cache_dir, force_update=force_update
                )
            return pd.DataFrame(columns=_CAPITAL_CHANGE_SCHEMA)
        elif table_name == "STK_SHARE_CHANGE":
            if "code" in conditions:
                return get_share_change(
                    conditions["code"],
                    cache_dir=cache_dir,
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
            return pd.DataFrame(columns=_SHARE_CHANGE_SCHEMA)
        elif table_name == "STK_SHAREHOLDER_CHANGE":
            if "code" in conditions:
                return get_shareholder_changes(
                    conditions["code"],
                    cache_dir=cache_dir,
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
