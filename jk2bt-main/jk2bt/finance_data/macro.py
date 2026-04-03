"""
finance_data/macro.py
宏观经济数据获取模块。

主要功能：
1. 宏观数据查询 - finance.MACRO_CHINA_*
2. FinanceQuery 类提供 finance.run_query 兼容接口
3. get_macro_indicator() - 统一接口，返回 RobustResult
4. get_macro_gdp/cpi/ppi/m2/interest_rate() - 各类宏观数据获取

数据字段：
- indicator: 指标名称
- value: 指标值
- date: 日期
- unit: 单位

缓存策略:
- DuckDB 缓存（优先）：存储在 data/macro.db 中
- 按发布周期缓存（30天）
"""

import os
import pandas as pd
from datetime import datetime
from typing import Optional, List, Union
import logging

logger = logging.getLogger(__name__)

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

_ROBUST_RESULT_AVAILABLE = False
try:
    from ..index_fundamentals_robust import RobustResult

    _ROBUST_RESULT_AVAILABLE = True
except ImportError:
    try:
        from index_fundamentals_robust import RobustResult

        _ROBUST_RESULT_AVAILABLE = True
    except ImportError:
        pass

if not _ROBUST_RESULT_AVAILABLE:

    class RobustResult:
        """稳健结果封装类"""

        def __init__(self, success=True, data=None, reason="", source="network"):
            self.success = success
            self.data = data if data is not None else pd.DataFrame()
            self.reason = reason
            self.source = source

        def __bool__(self):
            return self.success

        def __repr__(self):
            status = "OK" if self.success else "FAIL"
            return (
                f"<RobustResult[{status}] source={self.source} reason='{self.reason}'>"
            )


_MACRO_SCHEMA = [
    "indicator",
    "date",
    "value",
    "unit",
    "YoY",
    "MoM",
]


class MacroDBManager:
    """宏观数据 DuckDB 管理器"""

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
            db_path = os.path.join(base_dir, "data", "macro.db")

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
                    CREATE TABLE IF NOT EXISTS macro (
                        indicator VARCHAR NOT NULL,
                        date DATE NOT NULL,
                        value DOUBLE,
                        unit VARCHAR,
                        yoy DOUBLE,
                        mom DOUBLE,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (indicator, date)
                    )
                """)
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_macro_ind ON macro(indicator)"
                )
                conn.execute("CREATE INDEX IF NOT EXISTS idx_macro_date ON macro(date)")
                logger.info("宏观数据表结构初始化完成")
        except Exception as e:
            logger.warning(f"初始化表结构失败: {e}")

    def insert_macro(self, df: pd.DataFrame):
        if self._manager is None or df.empty:
            return

        df = df.copy()
        for col in _MACRO_SCHEMA:
            if col not in df.columns:
                df[col] = None

        if "update_time" not in df.columns:
            df["update_time"] = datetime.now()

        cols = _MACRO_SCHEMA + ["update_time"]
        df = df[cols]

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("INSERT OR REPLACE INTO macro SELECT * FROM df")
                logger.info(f"插入/更新 {len(df)} 条宏观数据")
        except Exception as e:
            logger.warning(f"插入宏观数据失败: {e}")

    def get_macro(
        self, indicator: str, start_date: str = None, end_date: str = None
    ) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_MACRO_SCHEMA)

        try:
            with self._manager._get_connection(read_only=True) as conn:
                if start_date and end_date:
                    df = conn.execute(
                        "SELECT * FROM macro WHERE indicator = ? AND date >= ? AND date <= ? ORDER BY date DESC",
                        [indicator, start_date, end_date],
                    ).fetchdf()
                else:
                    df = conn.execute(
                        "SELECT * FROM macro WHERE indicator = ? ORDER BY date DESC",
                        [indicator],
                    ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询宏观数据失败: {e}")
            return pd.DataFrame(columns=_MACRO_SCHEMA)

    def is_cache_valid(self, indicator: str, cache_days: int = 30) -> bool:
        if self._manager is None:
            return False

        try:
            with self._manager._get_connection(read_only=True) as conn:
                result = conn.execute(
                    "SELECT MAX(update_time) FROM macro WHERE indicator = ?",
                    [indicator],
                ).fetchone()
                if result and result[0]:
                    update_time = pd.to_datetime(result[0])
                    return (datetime.now() - update_time).days < cache_days
                return False
        except Exception:
            return False


_db_manager = MacroDBManager() if _DUCKDB_AVAILABLE else None


def _parse_num(value) -> Optional[float]:
    if value is None or value == "" or value == "-":
        return None
    try:
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        return float(value)
    except (ValueError, TypeError):
        return None


def _parse_date(date_str) -> Optional[str]:
    if not date_str or pd.isna(date_str):
        return None
    date_str = str(date_str).strip()
    for fmt in ["%Y-%m-%d", "%Y%m%d", "%Y/%m/%d", "%Y年%m月"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    if len(date_str) >= 6:
        try:
            year = int(date_str[:4])
            month = int(date_str[4:6])
            return f"{year}-{month:02d}-01"
        except Exception:
            pass
    return None


def get_macro_china_gdp(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取GDP数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame
    """
    df = get_macro_gdp(force_update=force_update)
    if not df.empty:
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
    return df


def get_macro_china_cpi(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取CPI数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame
    """
    df = get_macro_cpi(force_update=force_update)
    if not df.empty:
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
    return df


def get_macro_china_ppi(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取PPI数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame
    """
    df = get_macro_ppi(force_update=force_update)
    if not df.empty:
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
    return df


def get_macro_china_pmi(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取PMI数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame
    """
    cache_dir = "finance_cache"
    indicator = "PMI"

    if _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=30):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    cache_file = os.path.join(cache_dir, "macro_pmi.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 30:
                if _db_manager is not None:
                    _db_manager.insert_macro(cached_df)
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
            df = ak.macro_china_pmi()
            if df is not None and not df.empty:
                result = _normalize_macro_data(df, indicator, "%")
                if not result.empty:
                    result.to_pickle(cache_file)
                    if _db_manager is not None:
                        _db_manager.insert_macro(result)
                    return result
        except Exception as e:
            logger.warning(f"[macro_pmi] 获取PMI数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def get_macro_china_interest_rate(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取利率数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame，包含LPR等利率数据
    """
    df = get_macro_interest_rate(force_update=force_update)
    if not df.empty:
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
    return df


def get_macro_china_exchange_rate(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取汇率数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame，包含人民币汇率数据
    """
    cache_dir = "finance_cache"
    indicator = "EXCHANGE_RATE"

    if _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=7):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    cache_file = os.path.join(cache_dir, "macro_exchange_rate.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 7:
                if _db_manager is not None:
                    _db_manager.insert_macro(cached_df)
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
            df = ak.macro_china_rmb()
            if df is not None and not df.empty:
                result = _normalize_macro_data(df, indicator, "")
                if not result.empty:
                    result.to_pickle(cache_file)
                    if _db_manager is not None:
                        _db_manager.insert_macro(result)
                    return result
        except Exception as e:
            logger.warning(f"[macro_exchange_rate] 获取汇率数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def query_macro_data(
    indicator: str = None,
    start_date: str = None,
    end_date: str = None,
) -> pd.DataFrame:
    """
    查询宏观经济数据（finance.MACRO_ECONOMIC_DATA 表兼容接口）。

    参数
    ----
    indicator  : 指标类型（可选，不指定则返回全部）
    start_date : 起始日期
    end_date   : 结束日期

    返回
    ----
    DataFrame
    """
    if _db_manager is None:
        return pd.DataFrame(columns=_MACRO_SCHEMA)

    try:
        with _db_manager._manager._get_connection(read_only=True) as conn:
            sql = "SELECT * FROM macro WHERE 1=1"
            params = []

            if indicator:
                sql += " AND indicator = ?"
                params.append(indicator.upper())

            if start_date:
                sql += " AND date >= ?"
                params.append(start_date)

            if end_date:
                sql += " AND date <= ?"
                params.append(end_date)

            sql += " ORDER BY indicator, date"
            df = conn.execute(sql, params).fetchdf()
            df = df.rename(columns={"yoy": "YoY", "mom": "MoM"})
            return df
    except Exception as e:
        logger.warning(f"查询宏观数据失败: {e}")
        return pd.DataFrame(columns=_MACRO_SCHEMA)


def get_macro_cpi(
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取中国CPI数据。

    参数
    ----
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，CPI数据
    """
    indicator = "CPI"

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=30):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    cache_file = os.path.join(cache_dir, "macro_cpi.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 30:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_macro(cached_df)
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
            df = ak.macro_china_cpi()
            if df is not None and not df.empty:
                result = _normalize_macro_data(df, indicator, "%")
                if not result.empty:
                    result.to_pickle(cache_file)
                    if use_duckdb and _db_manager is not None:
                        _db_manager.insert_macro(result)
                    return result
        except Exception as e:
            logger.warning(f"[macro_cpi] 获取CPI数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def get_macro_ppi(
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取中国PPI数据。
    """
    indicator = "PPI"

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=30):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    cache_file = os.path.join(cache_dir, "macro_ppi.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 30:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_macro(cached_df)
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
            df = ak.macro_china_ppi()
            if df is not None and not df.empty:
                result = _normalize_macro_data(df, indicator, "%")
                if not result.empty:
                    result.to_pickle(cache_file)
                    if use_duckdb and _db_manager is not None:
                        _db_manager.insert_macro(result)
                    return result
        except Exception as e:
            logger.warning(f"[macro_ppi] 获取PPI数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def get_macro_gdp(
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取中国GDP数据。
    """
    indicator = "GDP"

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=90):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    cache_file = os.path.join(cache_dir, "macro_gdp.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 90:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_macro(cached_df)
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
            df = ak.macro_china_gdp()
            if df is not None and not df.empty:
                result = _normalize_macro_data(df, indicator, "亿元")
                if not result.empty:
                    result.to_pickle(cache_file)
                    if use_duckdb and _db_manager is not None:
                        _db_manager.insert_macro(result)
                    return result
        except Exception as e:
            logger.warning(f"[macro_gdp] 获取GDP数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def _normalize_macro_data(df: pd.DataFrame, indicator: str, unit: str) -> pd.DataFrame:
    """标准化宏观数据"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_MACRO_SCHEMA)

    result = pd.DataFrame()

    result["indicator"] = [indicator] * len(df)

    value_col = None
    for col in ["数值", "value", "当月", "当月值"]:
        if col in df.columns:
            value_col = col
            break
    if value_col:
        result["value"] = df[value_col].apply(_parse_num)
    else:
        result["value"] = None

    date_col = None
    for col in ["日期", "date", "月份", "统计时间"]:
        if col in df.columns:
            date_col = col
            break
    if date_col:
        result["date"] = df[date_col].apply(_parse_date)
    else:
        result["date"] = None

    result["unit"] = [unit] * len(df)

    yoy_col = None
    for col in ["同比增长", "YoY", "同比", "同比增速"]:
        if col in df.columns:
            yoy_col = col
            break
    if yoy_col:
        result["YoY"] = df[yoy_col].apply(_parse_num)
    else:
        result["YoY"] = None

    mom_col = None
    for col in ["环比增长", "MoM", "环比", "环比增速"]:
        if col in df.columns:
            mom_col = col
            break
    if mom_col:
        result["MoM"] = df[mom_col].apply(_parse_num)
    else:
        result["MoM"] = None

    result = result.dropna(subset=["date"])
    return result


def get_macro_m2(
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取中国M2货币供应量数据。

    参数
    ----
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，M2数据
    """
    indicator = "M2"

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=30):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    cache_file = os.path.join(cache_dir, "macro_m2.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 30:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_macro(cached_df)
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
            df = ak.macro_china_m2_yearly()
            if df is not None and not df.empty:
                result = _normalize_macro_data(df, indicator, "亿元")
                if not result.empty:
                    result.to_pickle(cache_file)
                    if use_duckdb and _db_manager is not None:
                        _db_manager.insert_macro(result)
                    return result
        except Exception as e:
            logger.warning(f"[macro_m2] 获取M2数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def get_macro_interest_rate(
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取中国利率数据（央行基准利率）。

    参数
    ----
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，利率数据
    """
    indicator = "INTEREST_RATE"

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=30):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    cache_file = os.path.join(cache_dir, "macro_interest_rate.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 30:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_macro(cached_df)
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
            df = ak.macro_bank_china_interest_rate()
            if df is not None and not df.empty:
                result = _normalize_macro_data(df, indicator, "%")
                if not result.empty:
                    result.to_pickle(cache_file)
                    if use_duckdb and _db_manager is not None:
                        _db_manager.insert_macro(result)
                    return result
        except Exception as e:
            logger.warning(f"[macro_interest_rate] 获取利率数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def query_macro(
    indicators: List[str],
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    批量查询宏观数据。

    参数
    ----
    indicators  : 指标列表 ['CPI', 'PPI', 'GDP', 'M2', 'INTEREST_RATE']
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，宏观数据
    """
    if indicators is None or len(indicators) == 0:
        return pd.DataFrame(columns=_MACRO_SCHEMA)

    dfs = []

    for indicator in indicators:
        try:
            result = get_macro_indicator_robust(
                indicator,
                cache_dir=cache_dir,
                force_update=force_update,
                use_duckdb=use_duckdb,
            )
            if result.success and not result.data.empty:
                dfs.append(result.data)
        except Exception as e:
            logger.warning(f"[query_macro] 获取 {indicator} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_MACRO_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


def get_macro_indicator_robust(
    indicator_name: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> RobustResult:
    """
    统一接口：获取宏观经济指标数据（返回 RobustResult）。

    参数
    ----
    indicator_name: 指标名称，支持: 'GDP', 'CPI', 'PPI', 'M2', 'INTEREST_RATE'
    cache_dir     : 缓存目录
    force_update  : 强制更新
    use_duckdb    : 是否使用 DuckDB 缓存

    返回
    ----
    RobustResult，包含：
        - success: bool - 是否成功
        - data: DataFrame - 指标数据
        - reason: str - 失败原因或成功说明
        - source: str - 数据来源（'cache'/'network'/'error'）
    """
    indicator_map = {
        "GDP": (get_macro_gdp, "亿元"),
        "CPI": (get_macro_cpi, "%"),
        "PPI": (get_macro_ppi, "%"),
        "M2": (get_macro_m2, "亿元"),
        "INTEREST_RATE": (get_macro_interest_rate, "%"),
    }

    if indicator_name is None:
        return RobustResult(
            success=False,
            data=pd.DataFrame(columns=_MACRO_SCHEMA),
            reason="指标名称不能为空",
            source="error",
        )

    indicator_upper = indicator_name.upper().strip()
    if indicator_upper not in indicator_map:
        return RobustResult(
            success=False,
            data=pd.DataFrame(columns=_MACRO_SCHEMA),
            reason=f"不支持的指标: {indicator_name}。支持的指标: {', '.join(indicator_map.keys())}",
            source="error",
        )

    func, unit = indicator_map[indicator_upper]

    try:
        df = func(cache_dir=cache_dir, force_update=force_update, use_duckdb=use_duckdb)
        if df is not None and not df.empty:
            return RobustResult(
                success=True,
                data=df,
                reason=f"获取{indicator_upper}数据成功，共{len(df)}条记录",
                source="network",
            )
        else:
            return RobustResult(
                success=False,
                data=pd.DataFrame(columns=_MACRO_SCHEMA),
                reason=f"{indicator_upper}数据为空，请检查数据源或稍后重试",
                source="network",
            )
    except Exception as e:
        logger.error(f"获取{indicator_upper}数据异常: {e}")
        return RobustResult(
            success=False,
            data=pd.DataFrame(columns=_MACRO_SCHEMA),
            reason=f"获取{indicator_upper}数据失败: {str(e)}",
            source="error",
        )


class FinanceQuery:
    """聚宽 finance 模块模拟器"""

    class MACRO_ECONOMIC_DATA:
        indicator = None
        date = None
        value = None
        unit = None
        yoy = None
        mom = None

    class MACRO_CHINA_CPI:
        indicator = None
        value = None
        date = None
        unit = None

    class MACRO_CHINA_PPI:
        indicator = None
        value = None
        date = None
        unit = None

    class MACRO_CHINA_GDP:
        indicator = None
        value = None
        date = None
        unit = None

    class MACRO_CHINA_PMI:
        indicator = None
        value = None
        date = None
        unit = None

    def run_query(
        self,
        query_obj,
        cache_dir="finance_cache",
        force_update=False,
        use_duckdb=True,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:
        table_name = None

        if hasattr(query_obj, "__name__"):
            table_name = query_obj.__name__
        elif hasattr(query_obj, "__class__"):
            table_name = query_obj.__class__.__name__

        if hasattr(query_obj, "left") and hasattr(query_obj, "right"):
            if hasattr(query_obj.left, "__name__"):
                table_name = query_obj.left.__name__
            elif hasattr(query_obj.left, "__class__"):
                table_name = query_obj.left.__class__.__name__

        if table_name == "MACRO_ECONOMIC_DATA":
            return query_macro_data(start_date=start_date, end_date=end_date)
        elif table_name == "MACRO_CHINA_CPI":
            return get_macro_china_cpi(start_date, end_date, force_update)
        elif table_name == "MACRO_CHINA_PPI":
            return get_macro_china_ppi(start_date, end_date, force_update)
        elif table_name == "MACRO_CHINA_GDP":
            return get_macro_china_gdp(start_date, end_date, force_update)
        elif table_name == "MACRO_CHINA_PMI":
            return get_macro_china_pmi(start_date, end_date, force_update)
        else:
            raise ValueError(f"不支持的表: {table_name}")


finance = FinanceQuery()


def get_macro_data(
    indicator_type: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取宏观经济指标数据（统一接口）。

    参数
    ----
    indicator_type : 指标类型，支持 cpi, ppi, gdp, m2, interest_rate
    start_date     : 起始日期
    end_date       : 结束日期
    cache_dir      : 缓存目录
    force_update   : 强制更新

    返回
    ----
    DataFrame
    """
    result = get_macro_indicator_robust(indicator_type, cache_dir, force_update)
    df = result.data
    if not df.empty and "date" in df.columns:
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
    return df


def get_macro_series(
    indicator_type: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """获取宏观时间序列数据"""
    df = get_macro_data(indicator_type, cache_dir, force_update)
    if df.empty or "date" not in df.columns:
        return df

    if start_date:
        df["_date"] = pd.to_datetime(df["date"])
        df = df[df["_date"] >= pd.to_datetime(start_date)]
        df = df.drop(columns=["_date"])

    if end_date:
        df["_date"] = pd.to_datetime(df["date"])
        df = df[df["_date"] <= pd.to_datetime(end_date)]
        df = df.drop(columns=["_date"])

    return df.sort_values("date", ascending=True).reset_index(drop=True)


def get_macro_indicators() -> pd.DataFrame:
    """
    获取可用的宏观指标列表。

    返回
    ----
    DataFrame: 包含指标代码、名称、频率、描述
    """
    data = [
        {"code": "GDP", "name": "GDP", "frequency": "季度", "desc": "国内生产总值"},
        {"code": "CPI", "name": "CPI", "frequency": "月度", "desc": "消费者物价指数"},
        {"code": "PPI", "name": "PPI", "frequency": "月度", "desc": "生产者物价指数"},
        {"code": "PMI", "name": "PMI", "frequency": "月度", "desc": "采购经理指数"},
        {"code": "M2", "name": "M2", "frequency": "月度", "desc": "广义货币供应量"},
        {
            "code": "INTEREST_RATE",
            "name": "利率",
            "frequency": "不定期",
            "desc": "央行基准利率",
        },
        {
            "code": "EXCHANGE_RATE",
            "name": "汇率",
            "frequency": "日度",
            "desc": "人民币汇率",
        },
    ]
    return pd.DataFrame(data)


def get_gdp_data(start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    获取GDP数据。

    参数
    ----
    start_date : 起始日期
    end_date   : 结束日期

    返回
    ----
    DataFrame，包含日期、数值
    """
    return get_macro_china_gdp(start_date=start_date, end_date=end_date)


def get_cpi_data(start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    获取CPI数据。

    参数
    ----
    start_date : 起始日期
    end_date   : 结束日期

    返回
    ----
    DataFrame，包含日期、数值
    """
    return get_macro_china_cpi(start_date=start_date, end_date=end_date)


def get_pmi_data(start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    获取PMI数据。

    参数
    ----
    start_date : 起始日期
    end_date   : 结束日期

    返回
    ----
    DataFrame，包含日期、数值
    """
    return get_macro_china_pmi(start_date=start_date, end_date=end_date)


def get_interest_rate(start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    获取利率数据（包含SHIBOR、LPR等）。

    参数
    ----
    start_date : 起始日期
    end_date   : 结束日期

    返回
    ----
    DataFrame，包含利率数据
    """
    return get_macro_china_interest_rate(start_date=start_date, end_date=end_date)


def get_macro_indicator(
    indicator_name: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> RobustResult:
    """
    统一接口：获取宏观经济指标数据（返回 RobustResult）。

    参数
    ----
    indicator_name: 指标名称，支持: 'GDP', 'CPI', 'PPI', 'M2', 'INTEREST_RATE'
    cache_dir     : 缓存目录
    force_update  : 强制更新

    返回
    ----
    RobustResult，包含：
        - success: bool - 是否成功
        - data: DataFrame - 指标数据
        - reason: str - 失败原因或成功说明
        - source: str - 数据来源
    """
    return get_macro_indicator_robust(
        indicator_name, cache_dir, force_update, use_duckdb=True
    )


def run_query_simple(
    table: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    start_date: str = None,
    end_date: str = None,
) -> pd.DataFrame:
    """简化的查询接口"""
    if table == "MACRO_ECONOMIC_DATA":
        return query_macro_data(start_date=start_date, end_date=end_date)
    elif table == "MACRO_CHINA_CPI":
        return get_macro_china_cpi(start_date, end_date, force_update)
    elif table == "MACRO_CHINA_PPI":
        return get_macro_china_ppi(start_date, end_date, force_update)
    elif table == "MACRO_CHINA_GDP":
        return get_macro_china_gdp(start_date, end_date, force_update)
    elif table == "MACRO_CHINA_PMI":
        return get_macro_china_pmi(start_date, end_date, force_update)
    elif table == "MACRO_CHINA_M2":
        return get_macro_m2(cache_dir=cache_dir, force_update=force_update)
    elif table == "MACRO_CHINA_INTEREST_RATE":
        return get_macro_interest_rate(cache_dir=cache_dir, force_update=force_update)
    else:
        raise ValueError(f"不支持的表: {table}")
