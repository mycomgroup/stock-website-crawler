"""
market_data/index_components.py
指数成分股数据获取模块。

主要功能：
1. 指数成分股查询 - finance.STK_INDEX_WEIGHTS, finance.STK_INDEX_COMPONENTS
2. 成分股权重查询
3. 成分股变动历史查询
4. FinanceQuery 类提供 finance.run_query 兼容接口

数据字段：
- index_code: 指数代码
- code: 成分股代码（聚宽格式）
- weight: 权重
- effective_date: 生效日期
- stock_name: 股票名称
- in_date: 纳入日期
- out_date: 剔除日期

缓存策略:
- DuckDB 缓存（优先）：存储在 data/index_components.db 中
- 按季度缓存
"""

import os
import pandas as pd
from datetime import datetime
from typing import Optional, List
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


_INDEX_COMPONENTS_SCHEMA = [
    "index_code",
    "code",
    "stock_name",
    "weight",
    "effective_date",
]

_INDEX_HISTORY_SCHEMA = [
    "index_code",
    "code",
    "stock_name",
    "in_date",
    "out_date",
    "change_type",
]

_INDEX_CACHE_DAYS = {
    "000300": 180,
    "000905": 180,
    "000016": 180,
    "000852": 180,
    "399006": 90,
    "399001": 90,
    "000001": 180,
}

_INDEX_SOURCE_MAP = {
    "000300": "csindex",
    "000905": "csindex",
    "000016": "csindex",
    "000852": "csindex",
    "399006": "sina",
    "399001": "sina",
    "000001": "sina",
}


class IndexComponentsDBManager:
    """指数成分股 DuckDB 管理器"""

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
            db_path = os.path.join(base_dir, "data", "index_components.db")

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
                    CREATE TABLE IF NOT EXISTS index_components (
                        index_code VARCHAR NOT NULL,
                        code VARCHAR NOT NULL,
                        stock_name VARCHAR,
                        weight DOUBLE,
                        effective_date DATE NOT NULL,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (index_code, code, effective_date)
                    )
                """)
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_idx_comp_index ON index_components(index_code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_idx_comp_code ON index_components(code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_idx_comp_date ON index_components(effective_date)"
                )

                conn.execute("""
                    CREATE TABLE IF NOT EXISTS index_history (
                        index_code VARCHAR NOT NULL,
                        code VARCHAR NOT NULL,
                        stock_name VARCHAR,
                        in_date DATE,
                        out_date DATE,
                        change_type VARCHAR,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (index_code, code, in_date)
                    )
                """)
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_idx_hist_index ON index_history(index_code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_idx_hist_date ON index_history(in_date)"
                )
                logger.info("指数成分股表结构初始化完成")
        except Exception as e:
            logger.warning(f"初始化表结构失败: {e}")

    def insert_index_components(self, df: pd.DataFrame):
        if self._manager is None or df.empty:
            return

        df = df.copy()
        for col in _INDEX_COMPONENTS_SCHEMA:
            if col not in df.columns:
                df[col] = None

        if "update_time" not in df.columns:
            df["update_time"] = datetime.now()

        cols = _INDEX_COMPONENTS_SCHEMA + ["update_time"]
        df = df[cols]

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("INSERT OR REPLACE INTO index_components SELECT * FROM df")
                logger.info(f"插入/更新 {len(df)} 条指数成分股信息")
        except Exception as e:
            logger.warning(f"插入指数成分股信息失败: {e}")

    def get_index_components(self, index_code: str) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)

        try:
            with self._manager._get_connection(read_only=True) as conn:
                df = conn.execute(
                    "SELECT * FROM index_components WHERE index_code = ? ORDER BY weight DESC",
                    [index_code],
                ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询指数成分股信息失败: {e}")
            return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)

    def is_cache_valid(self, index_code: str, cache_days: int = 90) -> bool:
        if self._manager is None:
            return False

        try:
            with self._manager._get_connection(read_only=True) as conn:
                result = conn.execute(
                    "SELECT MAX(update_time) FROM index_components WHERE index_code = ?",
                    [index_code],
                ).fetchone()
                if result and result[0]:
                    update_time = pd.to_datetime(result[0])
                    return (datetime.now() - update_time).days < cache_days
                return False
        except Exception:
            return False


_db_manager = IndexComponentsDBManager() if _DUCKDB_AVAILABLE else None


_INDEX_CODE_MAP = {
    "000300.XSHG": "000300",
    "000016.XSHG": "000016",
    "000905.XSHG": "000905",
    "000852.XSHG": "000852",
    "399006.XSHE": "399006",
}


def _normalize_index_code(symbol: str) -> str:
    """标准化指数代码"""
    if ".XSHG" in symbol or ".XSHE" in symbol:
        return symbol
    if symbol.startswith("sh"):
        return symbol[2:] + ".XSHG"
    if symbol.startswith("sz"):
        return symbol[2:] + ".XSHE"
    code = symbol.zfill(6)
    if code.startswith("0") or code.startswith("3"):
        if code.startswith("39"):
            return code + ".XSHE"
        return code + ".XSHG"
    return code + ".XSHG"


def _normalize_stock_code(symbol: str) -> str:
    """标准化股票代码为聚宽格式"""
    if ".XSHG" in symbol or ".XSHE" in symbol:
        return symbol
    code = str(symbol).zfill(6)
    if code.startswith("6"):
        return code + ".XSHG"
    return code + ".XSHE"


def _parse_weight(value) -> Optional[float]:
    if value is None or value == "" or value == "-" or pd.isna(value):
        return None
    try:
        if isinstance(value, str):
            value = value.replace("%", "").strip()
            return float(value) / 100 if float(value) > 1 else float(value)
        return float(value)
    except (ValueError, TypeError):
        return None


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


def _get_cache_days(index_code: str) -> int:
    """根据指数类型返回缓存天数"""
    code_num = index_code.split(".")[0] if "." in index_code else index_code
    code_num = code_num.zfill(6).replace("sh", "").replace("sz", "")
    return _INDEX_CACHE_DAYS.get(code_num, 90)


def _get_index_source(index_code: str) -> str:
    """根据指数类型返回数据源类型"""
    code_num = index_code.split(".")[0] if "." in index_code else index_code
    code_num = code_num.zfill(6).replace("sh", "").replace("sz", "")
    return _INDEX_SOURCE_MAP.get(code_num, "csindex")


def _normalize_weights(df: pd.DataFrame) -> pd.DataFrame:
    """标准化权重，确保总和为100%"""
    if df.empty or "weight" not in df.columns:
        return df

    weights = df["weight"].dropna()
    if len(weights) == 0:
        return df

    total = weights.sum()
    if total > 0 and abs(total - 100.0) > 0.1:
        df = df.copy()
        df["weight"] = df["weight"] * (100.0 / total)
        logger.info(f"权重标准化: {total:.2f}% -> 100.00%")

    return df


def _fetch_from_csindex(index_num: str) -> pd.DataFrame:
    """从中证指数公司获取成分股及权重"""
    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.index_stock_cons_weight_csindex(symbol=index_num)
        if df is not None and not df.empty:
            logger.info(f"[csindex] 成功获取 {index_num} 成分股: {len(df)} 只")
            return df
    except Exception as e:
        logger.warning(f"[csindex] 获取失败 {index_num}: {e}")
    return pd.DataFrame()


def _fetch_from_sina(index_num: str) -> pd.DataFrame:
    """从新浪财经获取成分股（无权重，使用等权重）"""
    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.index_stock_cons(symbol=index_num)
        if df is not None and not df.empty:
            df = df.copy()
            df["权重"] = 100.0 / len(df)
            logger.info(f"[sina] 成功获取 {index_num} 成分股: {len(df)} 只 (等权重)")
            return df
    except Exception as e:
        logger.warning(f"[sina] 获取失败 {index_num}: {e}")
    return pd.DataFrame()


def get_index_components(
    symbol: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取指数成分股及权重信息。

    参数
    ----
    symbol      : 指数代码，支持 '000300.XSHG', '000905.XSHG' 等格式
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，标准化字段：
    - index_code: 指数代码（聚宽格式）
    - code: 成分股代码（聚宽格式）
    - weight: 权重（已标准化，总和为100%）
    - effective_date: 生效日期
    """
    jq_index_code = _normalize_index_code(symbol)

    index_num = symbol.split(".")[0] if "." in symbol else symbol
    index_num = index_num.zfill(6).replace("sh", "").replace("sz", "")

    cache_days = _get_cache_days(index_num)

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(jq_index_code, cache_days=cache_days):
            df_cached = _db_manager.get_index_components(jq_index_code)
            if not df_cached.empty:
                return _normalize_weights(df_cached[_INDEX_COMPONENTS_SCHEMA])

    cache_file = os.path.join(cache_dir, f"index_components_{index_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < cache_days:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_index_components(cached_df)
                return _normalize_weights(cached_df)
            need_download = True
        except Exception:
            need_download = True

    if need_download:
        source = _get_index_source(index_num)

        df = pd.DataFrame()

        if source == "csindex":
            df = _fetch_from_csindex(index_num)
            if df.empty:
                logger.info(f"[fallback] 尝试备用数据源 sina")
                df = _fetch_from_sina(index_num)
        else:
            df = _fetch_from_sina(index_num)
            if df.empty:
                logger.info(f"[fallback] 尝试备用数据源 csindex")
                df = _fetch_from_csindex(index_num)

        if df is not None and not df.empty:
            result = _normalize_index_components(df, jq_index_code)
            if not result.empty:
                result = _normalize_weights(result)
                result.to_pickle(cache_file)
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_index_components(result)
                return result

    return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)


def _normalize_index_components(df: pd.DataFrame, jq_index_code: str) -> pd.DataFrame:
    """标准化指数成分股数据"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)

    result = pd.DataFrame()
    result["index_code"] = [jq_index_code] * len(df)

    code_col = None
    for col in ["成分券代码", "成分股代码", "股票代码", "品种代码", "code"]:
        if col in df.columns:
            code_col = col
            break
    if code_col:
        result["code"] = df[code_col].apply(_normalize_stock_code)
    else:
        result["code"] = ""

    name_col = None
    for col in ["成分券名称", "成分股名称", "股票名称", "品种名称", "name", "名称"]:
        if col in df.columns:
            name_col = col
            break
    if name_col:
        result["stock_name"] = df[name_col]
    else:
        result["stock_name"] = ""

    weight_col = None
    for col in ["权重", "weight", "占比"]:
        if col in df.columns:
            weight_col = col
            break
    if weight_col:
        result["weight"] = df[weight_col].apply(_parse_weight)
    else:
        result["weight"] = None

    date_col = None
    for col in ["日期", "生效日期", "纳入日期", "date"]:
        if col in df.columns:
            date_col = col
            break
    if date_col:
        result["effective_date"] = df[date_col].apply(_parse_date)
    else:
        result["effective_date"] = datetime.now().strftime("%Y-%m-%d")

    return result


def query_index_components(
    symbols: List[str],
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    批量查询指数成分股（finance.STK_INDEX_WEIGHTS）。
    """
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)

    dfs = []
    for symbol in symbols:
        try:
            df = get_index_components(
                symbol,
                cache_dir=cache_dir,
                force_update=force_update,
                use_duckdb=use_duckdb,
            )
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            logger.warning(f"[query_index_components] 获取 {symbol} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


def get_index_component_history(
    index_code: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取指数成分股历史变化。

    参数
    ----
    index_code   : 指数代码
    start_date   : 起始日期 (YYYY-MM-DD)
    end_date     : 结束日期 (YYYY-MM-DD)
    cache_dir    : 缓存目录
    force_update : 强制更新

    返回
    ----
    DataFrame，包含:
    - index_code: 指数代码
    - code: 股票代码
    - stock_name: 股票名称
    - in_date: 纳入日期
    - out_date: 剔除日期
    - change_type: 变动类型 (in/out)
    """
    jq_index_code = _normalize_index_code(index_code)
    index_num = index_code.split(".")[0] if "." in index_code else index_code
    index_num = index_num.zfill(6)

    cache_file = os.path.join(cache_dir, f"index_history_{index_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 90:
                return _filter_history_by_date(cached_df, start_date, end_date)
            need_download = True
        except Exception:
            need_download = True

    if need_download:
        try:
            try:
                import akshare as ak
            except ImportError:
                raise ImportError("请安装 akshare: pip install akshare")

            df_current = ak.index_stock_cons_weight_csindex(symbol=index_num)
            if df_current is not None and not df_current.empty:
                result = _normalize_index_history(df_current, jq_index_code)
                if not result.empty:
                    result.to_pickle(cache_file)
                    return _filter_history_by_date(result, start_date, end_date)
        except Exception as e:
            logger.warning(
                f"[get_index_component_history] 获取成分股历史失败 {index_code}: {e}"
            )

    return pd.DataFrame(columns=_INDEX_HISTORY_SCHEMA)


def _normalize_index_history(df: pd.DataFrame, jq_index_code: str) -> pd.DataFrame:
    """标准化成分股历史变动数据"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_INDEX_HISTORY_SCHEMA)

    result = pd.DataFrame()
    result["index_code"] = [jq_index_code] * len(df)

    code_col = None
    for col in ["成分券代码", "成分股代码", "股票代码", "code"]:
        if col in df.columns:
            code_col = col
            break
    if code_col:
        result["code"] = df[code_col].apply(_normalize_stock_code)
    else:
        result["code"] = ""

    name_col = None
    for col in ["成分券名称", "成分股名称", "股票名称", "name", "名称"]:
        if col in df.columns:
            name_col = col
            break
    if name_col:
        result["stock_name"] = df[name_col]
    else:
        result["stock_name"] = ""

    date_col = None
    for col in ["日期", "生效日期", "纳入日期", "date"]:
        if col in df.columns:
            date_col = col
            break
    if date_col:
        result["in_date"] = df[date_col].apply(_parse_date)
    else:
        result["in_date"] = datetime.now().strftime("%Y-%m-%d")

    result["out_date"] = None
    result["change_type"] = "current"

    return result


def _filter_history_by_date(
    df: pd.DataFrame, start_date: str = None, end_date: str = None
) -> pd.DataFrame:
    """按日期筛选历史记录"""
    if df.empty:
        return df

    if start_date is None and end_date is None:
        return df

    df = df.copy()
    if "in_date" in df.columns:
        df["in_date_dt"] = pd.to_datetime(df["in_date"], errors="coerce")

        if start_date:
            start_dt = pd.to_datetime(start_date)
            df = df[df["in_date_dt"] >= start_dt]

        if end_date:
            end_dt = pd.to_datetime(end_date)
            df = df[df["in_date_dt"] <= end_dt]

        df = df.drop(columns=["in_date_dt"])

    return df


def get_index_stocks(
    symbol: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> List[str]:
    """
    获取指数成分股列表。

    参数
    ----
    symbol       : 指数代码，支持 '000300.XSHG', '000905.XSHG' 等格式
    cache_dir    : 缓存目录
    force_update : 强制更新
    use_duckdb   : 是否使用 DuckDB 缓存

    返回
    ----
    list: 股票代码列表（聚宽格式），如 ['600519.XSHG', '000858.XSHE', ...]
    """
    df = get_index_components(
        symbol, cache_dir=cache_dir, force_update=force_update, use_duckdb=use_duckdb
    )

    if df.empty:
        return []

    if "code" in df.columns:
        return df["code"].dropna().tolist()

    return []


class FinanceQuery:
    """聚宽 finance 模块模拟器"""

    class STK_INDEX_WEIGHTS:
        index_code = None
        code = None
        weight = None
        effective_date = None

    class STK_INDEX_COMPONENTS:
        index_code = None
        code = None
        weight = None
        pub_date = None
        in_date = None
        out_date = None

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
                conditions["index_code"] = query_obj.right

        if hasattr(query_obj, "index_code") and query_obj.index_code:
            conditions["index_code"] = query_obj.index_code

        if table_name == "STK_INDEX_WEIGHTS":
            if "index_code" in conditions:
                return get_index_components(
                    conditions["index_code"], cache_dir=cache_dir, use_duckdb=use_duckdb
                )
            return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)
        elif table_name == "STK_INDEX_COMPONENTS":
            if "index_code" in conditions:
                return get_index_components(
                    conditions["index_code"],
                    cache_dir=cache_dir,
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
            return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)
        else:
            raise ValueError(f"不支持的表: {table_name}")


finance = FinanceQuery()


def run_query_simple(
    table: str,
    index_code: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """简化的查询接口"""
    if table == "STK_INDEX_WEIGHTS":
        if index_code:
            return get_index_components(
                index_code, cache_dir=cache_dir, force_update=force_update
            )
        return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)
    elif table == "STK_INDEX_COMPONENTS":
        if index_code:
            return get_index_components(
                index_code, cache_dir=cache_dir, force_update=force_update
            )
        return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)
    else:
        raise ValueError(f"不支持的表: {table}")


def get_index_weights(
    index_code: str,
    date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取指数成分股权重。

    参数
    ----
    index_code   : 指数代码，如 '000300'、'000905'
    date         : 查询日期 (YYYY-MM-DD)，默认最新
    cache_dir    : 缓存目录
    force_update : 强制更新
    use_duckdb   : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，包含 stock_code, weight, stock_name 字段
    """
    df = get_index_components(
        index_code,
        cache_dir=cache_dir,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )
    if df.empty:
        return pd.DataFrame(columns=["stock_code", "weight", "stock_name"])

    result = pd.DataFrame()
    result["stock_code"] = df.get("code", "")
    result["weight"] = df.get("weight", 0)
    result["stock_name"] = ""

    return result


_INDEX_INFO_CACHE = None


def get_index_info(index_code: str = None) -> pd.DataFrame:
    """
    获取指数基本信息。

    参数
    ----
    index_code : str, optional
        指数代码，如 '000300'、'000905'。如果不指定，返回所有指数信息

    返回
    ----
    pd.DataFrame
        指数信息表，包含：
        - index_code: 指数代码
        - index_name: 指数名称
        - publish_date: 发布日期
    """
    global _INDEX_INFO_CACHE

    if _INDEX_INFO_CACHE is None:
        try:
            try:
                import akshare as ak
            except ImportError:
                raise ImportError("请安装 akshare: pip install akshare")

            df = ak.index_stock_info()
            if df is not None and not df.empty:
                df = df.rename(
                    columns={
                        "index_code": "index_code",
                        "display_name": "index_name",
                        "publish_date": "publish_date",
                    }
                )
                _INDEX_INFO_CACHE = df
        except Exception as e:
            logger.warning(f"获取指数信息失败: {e}")
            return pd.DataFrame(columns=["index_code", "index_name", "publish_date"])

    if _INDEX_INFO_CACHE is None:
        return pd.DataFrame(columns=["index_code", "index_name", "publish_date"])

    if index_code is None:
        return _INDEX_INFO_CACHE.copy()

    code = index_code.replace(".XSHG", "").replace(".XSHE", "").zfill(6)
    result = _INDEX_INFO_CACHE[_INDEX_INFO_CACHE["index_code"] == code]

    if result.empty:
        logger.warning(f"未找到指数 {index_code} 的信息")

    return result


def get_industry_index_stocks(industry_code: str) -> List[str]:
    """
    获取行业指数成分股。

    参数
    ----
    industry_code : str
        行业代码，如 '801010' (农林牧渔)、'801030' (基础化工) 等
        或行业名称如 '农林牧渔'、'基础化工'

    返回
    ----
    List[str]
        股票代码列表（聚宽格式）
    """
    from .industry import SW_LEVEL1_CODES

    code = industry_code
    if industry_code in SW_LEVEL1_CODES:
        code = SW_LEVEL1_CODES[industry_code]

    if not code.startswith("80"):
        for name, c in SW_LEVEL1_CODES.items():
            if industry_code in name or name in industry_code:
                code = c
                break

    if not code.startswith("80"):
        logger.warning(f"未找到行业 {industry_code} 对应的代码")
        return []

    code_clean = code.replace(".SI", "")

    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.index_component_sw(symbol=code_clean)
        if df is not None and not df.empty:
            stocks = []
            for stock_code in df["证券代码"]:
                code_str = str(stock_code).zfill(6)
                if code_str.startswith("6"):
                    stocks.append(f"{code_str}.XSHG")
                else:
                    stocks.append(f"{code_str}.XSHE")
            return stocks
    except Exception as e:
        logger.warning(f"获取行业指数成分股失败 {industry_code}: {e}")

    return []


__all__ = [
    "get_index_components",
    "get_index_stocks",
    "get_index_weights",
    "get_index_info",
    "get_industry_index_stocks",
    "get_index_component_history",
    "query_index_components",
    "run_query_simple",
    "FinanceQuery",
    "finance",
]
