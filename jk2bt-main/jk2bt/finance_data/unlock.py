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
- DuckDB 缓存（优先）：存储在 data/unlock.db 中
- 按周缓存：动态数据
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Union
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


UNLOCK_CACHE_DAYS = 7

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


_UNLOCK_SCHEMA = [
    "code",
    "unlock_date",
    "unlock_amount",
    "unlock_ratio",
    "unlock_type",
    "holder_type",
]


class UnlockDBManager:
    """限售解禁 DuckDB 管理器"""

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
            db_path = os.path.join(base_dir, "data", "unlock.db")

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
                    CREATE TABLE IF NOT EXISTS unlock (
                        code VARCHAR NOT NULL,
                        unlock_date DATE NOT NULL,
                        unlock_amount BIGINT,
                        unlock_ratio DOUBLE,
                        unlock_type VARCHAR,
                        holder_type VARCHAR,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (code, unlock_date)
                    )
                """)
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_unlock_code ON unlock(code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_unlock_date ON unlock(unlock_date)"
                )
                logger.info("限售解禁表结构初始化完成")
        except Exception as e:
            logger.warning(f"初始化表结构失败: {e}")

    def insert_unlock(self, df: pd.DataFrame):
        if self._manager is None or df.empty:
            return

        df = df.copy()
        for col in _UNLOCK_SCHEMA:
            if col not in df.columns:
                df[col] = None

        if "update_time" not in df.columns:
            df["update_time"] = datetime.now()

        cols = _UNLOCK_SCHEMA + ["update_time"]
        df = df[cols]

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("INSERT OR REPLACE INTO unlock SELECT * FROM df")
                logger.info(f"插入/更新 {len(df)} 条限售解禁信息")
        except Exception as e:
            logger.warning(f"插入限售解禁信息失败: {e}")

    def get_unlock(
        self, code: str, start_date: str = None, end_date: str = None
    ) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_UNLOCK_SCHEMA)

        try:
            with self._manager._get_connection(read_only=True) as conn:
                if start_date and end_date:
                    df = conn.execute(
                        "SELECT * FROM unlock WHERE code = ? AND unlock_date >= ? AND unlock_date <= ? ORDER BY unlock_date",
                        [code, start_date, end_date],
                    ).fetchdf()
                else:
                    df = conn.execute(
                        "SELECT * FROM unlock WHERE code = ? ORDER BY unlock_date",
                        [code],
                    ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询限售解禁信息失败: {e}")
            return pd.DataFrame(columns=_UNLOCK_SCHEMA)

    def is_cache_valid(self, code: str, cache_days: int = 7) -> bool:
        if self._manager is None:
            return False

        try:
            with self._manager._get_connection(read_only=True) as conn:
                result = conn.execute(
                    "SELECT MAX(update_time) FROM unlock WHERE code = ?",
                    [code],
                ).fetchone()
                if result and result[0]:
                    update_time = pd.to_datetime(result[0])
                    return (datetime.now() - update_time).days < cache_days
                return False
        except Exception:
            return False


_db_manager = UnlockDBManager() if _DUCKDB_AVAILABLE else None


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


def get_unlock(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
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
    cache_dir   : 缓存目录
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
    code_num = _extract_code_num(symbol)
    jq_code = _normalize_to_jq(symbol)

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(jq_code, cache_days=7):
            df_cached = _db_manager.get_unlock(jq_code, start_date, end_date)
            if not df_cached.empty:
                return df_cached[_UNLOCK_SCHEMA]

    cache_file = os.path.join(cache_dir, f"unlock_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 7:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_unlock(cached_df)
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
            results = []

            try:
                df_queue = ak.stock_restricted_release_queue_sina(symbol=code_num)
                if df_queue is not None and not df_queue.empty:
                    for _, row in df_queue.iterrows():
                        record = _parse_queue_row(row, jq_code)
                        if record:
                            results.append(record)
            except Exception as e:
                logger.debug(f"stock_restricted_release_queue_sina 失败: {e}")

            try:
                df_summary = ak.stock_restricted_release_summary_em(symbol=code_num)
                if df_summary is not None and not df_summary.empty:
                    for _, row in df_summary.iterrows():
                        record = _parse_summary_row(row, jq_code)
                        if record:
                            results.append(record)
            except Exception as e:
                logger.debug(f"stock_restricted_release_summary_em 失败: {e}")

            if results:
                result_df = pd.DataFrame(results)
                result_df = result_df.drop_duplicates(
                    subset=["code", "unlock_date"], keep="first"
                )
                result_df = result_df.sort_values("unlock_date")
                result_df.to_pickle(cache_file)
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_unlock(result_df)
                if start_date is None and end_date is None:
                    return result_df
                return _filter_by_date_range(result_df, start_date, end_date)

        except Exception as e:
            logger.warning(f"[unlock] 获取限售解禁失败 {symbol}: {e}")

    return pd.DataFrame(columns=_UNLOCK_SCHEMA)


def _parse_summary_row(row, jq_code: str) -> Optional[dict]:
    """解析汇总数据行"""
    try:
        return {
            "code": jq_code,
            "unlock_date": _parse_date(row.get("解禁日期", None)),
            "unlock_amount": _parse_num(row.get("解禁数量", 0)),
            "unlock_ratio": _parse_ratio(row.get("解禁比例", 0)),
            "unlock_type": str(row.get("解禁类型", "")),
            "holder_type": str(row.get("限售股类型", "")),
        }
    except Exception:
        return None


def _parse_queue_row(row, jq_code: str) -> Optional[dict]:
    """解析新浪排队数据行"""
    try:
        unlock_amount = _parse_num(row.get("解禁数量", 0))
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
            "unlock_amount": _parse_num(row.get("解禁股数", 0)),
            "unlock_ratio": _parse_ratio(row.get("占总股本比例", 0)),
            "unlock_type": str(row.get("解禁类型", "")),
            "holder_type": str(row.get("股东名称", "")),
        }
    except Exception:
        return None


def _filter_by_date_range(
    df: pd.DataFrame, start_date: str, end_date: str
) -> pd.DataFrame:
    """按日期范围筛选数据"""
    if df.empty:
        return df

    df = df.copy()

    if "unlock_date" not in df.columns:
        return df

    df["_date"] = pd.to_datetime(df["unlock_date"])

    if start_date:
        start_dt = pd.Timestamp(start_date)
        df = df[df["_date"] >= start_dt]

    if end_date:
        end_dt = pd.Timestamp(end_date)
        df = df[df["_date"] <= end_dt]

    return df.drop(columns=["_date"]).reset_index(drop=True)


def query_unlock(
    symbols: List[str],
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
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
                cache_dir=cache_dir,
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
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取指定日期的全市场解禁日历。

    参数
    ----
    date        : 查询日期，默认今天
    cache_dir   : 缓存目录
    force_update: 强制更新

    返回
    ----
    DataFrame，包含当天解禁的所有股票
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    cache_file = os.path.join(cache_dir, f"unlock_calendar_{date.replace('-', '')}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            return cached_df
        except Exception:
            need_download = True

    if need_download:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        try:
            date_num = date.replace("-", "")
            df = ak.stock_restricted_release_detail_em(
                start_date=date_num, end_date=date_num
            )
            if df is not None and not df.empty:
                result = pd.DataFrame()
                code_col = "股票代码" if "股票代码" in df.columns else "code"
                result["code"] = df[code_col].apply(
                    lambda x: _normalize_to_jq(str(x).zfill(6)) if pd.notna(x) else ""
                )
                result["unlock_date"] = [date] * len(df)
                amount_col = (
                    "实际解禁数量" if "实际解禁数量" in df.columns else "解禁数量"
                )
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
                result.to_pickle(cache_file)
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

        if table_name in [
            "STK_RESTRICTED_RELEASE",
            "STK_UNLOCK_INFO",
            "STK_LOCK_UNLOCK",
            "STK_UNLOCK_DATE",
        ]:
            if "code" in conditions:
                return get_unlock(
                    conditions["code"], cache_dir=cache_dir, use_duckdb=use_duckdb
                )
            return pd.DataFrame(columns=_UNLOCK_SCHEMA)
        elif table_name == "STK_LOCK_SHARE":
            if "code" in conditions:
                return query_lock_share(
                    conditions["code"], cache_dir=cache_dir, force_update=force_update
                )
            return pd.DataFrame(columns=_LOCK_SHARE_SCHEMA)
        else:
            raise ValueError(f"不支持的表: {table_name}")


finance = FinanceQuery()


def get_unlock_schedule(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取解禁时间表（别名接口）。

    参数
    ----
    symbol       : 股票代码
    start_date   : 起始日期
    end_date     : 结束日期
    cache_dir    : 缓存目录
    force_update : 强制更新

    返回
    ----
    DataFrame
    """
    return get_unlock(
        symbol,
        start_date=start_date,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def get_unlock_pressure(
    symbol: str,
    days_ahead: int = 30,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> dict:
    """
    计算解禁压力指标。

    参数
    ----
    symbol       : 股票代码
    days_ahead   : 未来多少天
    cache_dir    : 缓存目录
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
        cache_dir=cache_dir,
        force_update=force_update,
    )

    jq_code = _normalize_to_jq(symbol) if "normalize_to_jq" in dir() else symbol

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
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """简化的查询接口"""
    if table == "STK_RESTRICTED_RELEASE":
        if code:
            return get_unlock(code, cache_dir=cache_dir, force_update=force_update)
        return pd.DataFrame(columns=_UNLOCK_SCHEMA)
    else:
        raise ValueError(f"不支持的表: {table}")


def get_unlock_info(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
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
    cache_dir   : 缓存目录
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
    code_num = _extract_code_num(symbol)
    jq_code = _normalize_to_jq(symbol)

    cache_file = os.path.join(cache_dir, f"unlock_robust_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))
    cached_df = None
    cache_valid = False
    cache_age_days = 0

    if os.path.exists(cache_file):
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            cache_age_days = (datetime.now() - file_mtime).days
            if cache_age_days < UNLOCK_CACHE_DAYS:
                cache_valid = True
                if not need_download:
                    df_filtered = _filter_by_date_range(cached_df, start_date, end_date)
                    if not df_filtered.empty or (
                        start_date is None and end_date is None
                    ):
                        return RobustResult(
                            success=True,
                            data=df_filtered if not df_filtered.empty else cached_df,
                            reason=f"从缓存获取解禁信息（缓存有效期: {cache_age_days}天）",
                            source="cache",
                        )
            need_download = True
        except Exception as e:
            logger.warning(f"[get_unlock_info] 读取缓存失败: {e}")
            need_download = True

    if need_download:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        try:
            results = []
            source_used = "network"

            try:
                df_queue = ak.stock_restricted_release_queue_sina(symbol=code_num)
                if df_queue is not None and not df_queue.empty:
                    for _, row in df_queue.iterrows():
                        record = _parse_queue_row(row, jq_code)
                        if record:
                            results.append(record)
            except Exception as e1:
                logger.debug(f"stock_restricted_release_queue_sina 失败: {e1}")

            try:
                df_summary = ak.stock_restricted_release_summary_em(symbol=code_num)
                if df_summary is not None and not df_summary.empty:
                    for _, row in df_summary.iterrows():
                        record = _parse_summary_row(row, jq_code)
                        if record:
                            results.append(record)
            except Exception as e2:
                logger.debug(f"stock_restricted_release_summary_em 失败: {e2}")
                logger.debug(f"stock_restricted_release_detail_em 失败: {e2}")

            if not results and cached_df is not None and not cached_df.empty:
                results = cached_df.to_dict("records")
                source_used = "fallback"
                logger.info(f"[get_unlock_info] 使用缓存兜底")

            if results:
                result_df = pd.DataFrame(results)
                result_df = result_df.drop_duplicates(
                    subset=["code", "unlock_date"], keep="first"
                )
                result_df = result_df.sort_values("unlock_date").reset_index(drop=True)
                result_df.to_pickle(cache_file)

                df_filtered = _filter_by_date_range(result_df, start_date, end_date)
                if not df_filtered.empty or (start_date is None and end_date is None):
                    return RobustResult(
                        success=True,
                        data=df_filtered if not df_filtered.empty else result_df,
                        reason=f"成功获取 {len(result_df)} 条解禁记录",
                        source=source_used,
                    )
                else:
                    return RobustResult(
                        success=False,
                        data=pd.DataFrame(columns=_UNLOCK_SCHEMA),
                        reason=f"指定日期范围无解禁记录",
                        source=source_used,
                    )

        except Exception as e:
            logger.warning(f"[get_unlock_info] 网络获取失败: {e}")
            if cached_df is not None and not cached_df.empty:
                df_filtered = _filter_by_date_range(cached_df, start_date, end_date)
                if not df_filtered.empty:
                    return RobustResult(
                        success=True,
                        data=df_filtered,
                        reason=f"网络失败，使用缓存兜底（缓存已过期 {cache_age_days} 天）",
                        source="fallback",
                    )
                elif start_date is None and end_date is None:
                    return RobustResult(
                        success=True,
                        data=cached_df,
                        reason=f"网络失败，使用缓存兜底",
                        source="fallback",
                    )

    return RobustResult(
        success=False,
        data=pd.DataFrame(columns=_UNLOCK_SCHEMA),
        reason=f"无法获取解禁信息 (股票: {symbol})",
        source="fallback",
    )


def get_upcoming_unlocks(
    days: int = 30,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取即将解禁的股票列表。

    参数
    ----
    days        : 未来天数，默认30天
    cache_dir   : 缓存目录
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

    cache_file = os.path.join(
        cache_dir,
        f"upcoming_unlocks_{start_date.replace('-', '')}_{end_date.replace('-', '')}.pkl",
    )
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 1:
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
            start_num = start_date.replace("-", "")
            end_num = end_date.replace("-", "")
            df = ak.stock_restricted_release_detail_em(
                start_date=start_num, end_date=end_num
            )
            if df is not None and not df.empty:
                result = pd.DataFrame()
                code_col = "股票代码" if "股票代码" in df.columns else "code"
                result["code"] = df[code_col].apply(
                    lambda x: _normalize_to_jq(str(x).zfill(6)) if pd.notna(x) else ""
                )
                date_col = "解禁日期" if "解禁日期" in df.columns else "unlock_date"
                result["unlock_date"] = (
                    df[date_col].apply(_parse_date) if date_col in df.columns else None
                )
                amount_col = (
                    "实际解禁数量" if "实际解禁数量" in df.columns else "解禁数量"
                )
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
                result.to_pickle(cache_file)
                return result
        except Exception as e:
            logger.warning(f"[get_upcoming_unlocks] 获取即将解禁股票失败: {e}")

    return pd.DataFrame(columns=_UNLOCK_SCHEMA + ["unlock_market_value"])


def get_unlock_history(
    security: str,
    years: int = 3,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取历史解禁记录。

    参数
    ----
    security    : 股票代码
    years       : 查询年数，默认3年
    cache_dir   : 缓存目录
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
        cache_dir=cache_dir,
        force_update=force_update,
    )


def query_lock_share(
    symbol: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    查询限售股份信息（finance.STK_LOCK_SHARE）。

    参数
    ----
    symbol       : 股票代码
    cache_dir    : 缓存目录
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
    code_num = _extract_code_num(symbol)
    jq_code = _normalize_to_jq(symbol)

    cache_file = os.path.join(cache_dir, f"lock_share_{code_num}.pkl")
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
            results = []
            try:
                df_queue = ak.stock_restricted_release_queue_sina(symbol=code_num)
                if df_queue is not None and not df_queue.empty:
                    for _, row in df_queue.iterrows():
                        record = _parse_lock_share_row(row, jq_code)
                        if record:
                            results.append(record)
            except Exception as e:
                logger.debug(f"stock_restricted_release_queue_sina 失败: {e}")

            try:
                df_summary = ak.stock_restricted_release_summary_em(symbol=code_num)
                if df_summary is not None and not df_summary.empty:
                    for _, row in df_summary.iterrows():
                        record = _parse_lock_share_summary_row(row, jq_code)
                        if record:
                            results.append(record)
            except Exception as e:
                logger.debug(f"stock_restricted_release_summary_em 失败: {e}")

            if results:
                result_df = pd.DataFrame(results)
                result_df = result_df.drop_duplicates(
                    subset=["code", "unlock_date"], keep="first"
                )
                result_df = result_df.sort_values("unlock_date")
                result_df.to_pickle(cache_file)
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
            "lock_amount": _parse_num(row.get("解禁数量", 0)),
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
            "lock_amount": _parse_num(row.get("解禁数量", 0)),
            "lock_type": str(row.get("解禁类型", "")),
            "shareholder_name": "",
            "shareholder_type": str(row.get("限售股类型", "")),
        }
    except Exception:
        return None


def analyze_unlock_impact(
    security: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> dict:
    """
    分析解禁对股价的影响。

    参数
    ----
    security    : 股票代码
    cache_dir   : 缓存目录
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
    code_num = _extract_code_num(security)
    jq_code = _normalize_to_jq(security)

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
        cache_dir=cache_dir,
        force_update=force_update,
    )

    df_history = get_unlock_history(
        security,
        years=3,
        cache_dir=cache_dir,
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
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> RobustResult:
    """
    批量获取限售解禁信息，返回 RobustResult。

    参数
    ----
    codes       : 股票代码列表
    start_date  : 起始日期（可选）
    end_date    : 结束日期（可选）
    cache_dir   : 缓存目录
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
                cache_dir=cache_dir,
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
