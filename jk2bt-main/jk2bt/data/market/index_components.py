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
- Parquet 缓存：存储在 data/index_components_parquet 中
- 按季度缓存
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

from jk2bt.utils.date_utils import parse_date as _parse_date, filter_by_date_range

_PARQUET_AVAILABLE = False
try:
    from jk2bt.data.storage.parquet_adapter import ParquetAdapter

    _PARQUET_AVAILABLE = True
except ImportError:
    try:
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        _PARQUET_AVAILABLE = True
    except ImportError:
        logger.warning("ParquetAdapter 模块不可用，将使用 pickle 缓存")


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


class IndexComponentsDBManager:
    """指数成分股 DuckDB 管理器（延迟初始化）"""

    _instance = None
    _initialized = False

    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._manager = None
            cls._instance._db_path = None
        return cls._instance

    def _ensure_initialized(self, db_path: str = None):
        """延迟初始化：只在首次使用时才初始化"""
        if self._initialized:
            return

        if not _PARQUET_AVAILABLE:
            self._manager = None
            self._initialized = True
            return

        if db_path is None:
            db_path = "data_cache/index_components_parquet"

        self._db_path = db_path
        self._manager = None

        try:
            self._manager = ParquetAdapter(db_path=db_path, read_only=False)
            self._init_tables()
        except Exception as e:
            logger.warning(f"DuckDB 初始化失败: {e}")
            self._manager = None

        self._initialized = True

    def _init_tables(self):
        if self._manager is None:
            return
        try:
            if hasattr(self._manager, "_init_database"):
                self._manager._init_database()
            logger.info("指数成分股缓存初始化完成")
        except Exception as e:
            logger.warning(f"初始化缓存失败: {e}")

    def _df_to_parquet_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """将 DataFrame 列名映射到 parquet cache 的 INDEX_COMPONENTS schema"""
        df = df.copy()
        col_map = {}
        if "code" in df.columns and "symbol" not in df.columns:
            col_map["code"] = "symbol"
        if "effective_date" in df.columns and "date" not in df.columns:
            col_map["effective_date"] = "date"
        if col_map:
            df = df.rename(columns=col_map)
        if "date" in df.columns:
            try:
                df["date"] = pd.to_datetime(df["date"]).dt.date
            except Exception:
                pass
        return df

    def _df_from_parquet_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """将 parquet cache 的 DataFrame 列名映射回原有 schema"""
        df = df.copy()
        col_map = {}
        if "symbol" in df.columns and "code" not in df.columns:
            col_map["symbol"] = "code"
        if "date" in df.columns and "effective_date" not in df.columns:
            col_map["date"] = "effective_date"
        if col_map:
            df = df.rename(columns=col_map)
        return df

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
            pq_df = self._df_to_parquet_schema(df)
            self._manager.cache_manager.put("index_components", pq_df)
            logger.info(f"插入/更新 {len(df)} 条指数成分股信息")
        except Exception as e:
            logger.warning(f"插入指数成分股信息失败: {e}")

    def get_index_components(self, index_code: str) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)

        try:
            df = self._manager.query(
                "index_components", where={"index_code": index_code}
            )
            if df.empty:
                return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)
            df = self._df_from_parquet_schema(df)
            if "weight" in df.columns:
                df = df.sort_values("weight", ascending=False)
            return df
        except Exception as e:
            logger.warning(f"查询指数成分股信息失败: {e}")
            return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)

    def is_cache_valid(self, index_code: str, cache_days: int = 90) -> bool:
        if self._manager is None:
            return False

        try:
            df = self._manager.query(
                "index_components", where={"index_code": index_code}
            )
            if df.empty or "date" not in df.columns:
                return False
            max_date = pd.to_datetime(df["date"]).max()
            return (datetime.now() - pd.to_datetime(max_date)).days < cache_days
        except Exception as e:
            logger.warning(f"检查缓存有效性失败: {e}")
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


def _get_db_manager():
    """获取数据库管理器单例（延迟初始化）"""
    if not _PARQUET_AVAILABLE:
        return None
    manager = IndexComponentsDBManager()
    manager._ensure_initialized()
    return manager


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


def _get_cache_days(index_code: str) -> int:
    """根据指数类型返回缓存天数"""
    code_num = index_code.split(".")[0] if "." in index_code else index_code
    code_num = code_num.zfill(6).replace("sh", "").replace("sz", "")
    return _INDEX_CACHE_DAYS.get(code_num, 90)


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


def get_index_components(
    symbol: str,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取指数成分股及权重信息。

    参数
    ----
    symbol      : 指数代码，支持 '000300.XSHG', '000905.XSHG' 等格式
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

    if use_duckdb and not force_update:
        db_manager = _get_db_manager()
        if db_manager is not None and db_manager.is_cache_valid(
            jq_index_code, cache_days=cache_days
        ):
            df_cached = db_manager.get_index_components(jq_index_code)
            if not df_cached.empty:
                return _normalize_weights(df_cached[_INDEX_COMPONENTS_SCHEMA])

    from jk2bt.data.sources import get_adapter

    df = get_adapter().get_index_components(index_num)

    if df is not None and not df.empty:
        result = _normalize_index_components(df, jq_index_code)
        if not result.empty:
            result = _normalize_weights(result)
            if use_duckdb:
                db_manager = _get_db_manager()
                if db_manager is not None:
                    db_manager.insert_index_components(result)
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
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取指数成分股历史变化。

    参数
    ----
    index_code   : 指数代码
    start_date   : 起始日期 (YYYY-MM-DD)
    end_date     : 结束日期 (YYYY-MM-DD)
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

    try:
        from jk2bt.data.sources import get_adapter

        df_current = get_adapter().get_index_stock_cons_weight_csindex(symbol=index_num)
        if df_current is not None and not df_current.empty:
            result = _normalize_index_history(df_current, jq_index_code)
            if not result.empty:
                return filter_by_date_range(
                    result, start_date, end_date, date_col="in_date"
                )
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


def get_index_stocks(
    symbol: str,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> List[str]:
    """
    获取指数成分股列表。

    参数
    ----
    symbol       : 指数代码，支持 '000300.XSHG', '000905.XSHG' 等格式
    force_update : 强制更新
    use_duckdb   : 是否使用 DuckDB 缓存

    返回
    ----
    list: 股票代码列表（聚宽格式），如 ['600519.XSHG', '000858.XSHE', ...]
    """
    df = get_index_components(symbol, force_update=force_update, use_duckdb=use_duckdb)

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

    def run_query(self, query_obj, force_update=False, use_duckdb=True) -> pd.DataFrame:
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
                    conditions["index_code"], use_duckdb=use_duckdb
                )
            return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)
        elif table_name == "STK_INDEX_COMPONENTS":
            if "index_code" in conditions:
                return get_index_components(
                    conditions["index_code"],
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
    force_update: bool = False,
) -> pd.DataFrame:
    """简化的查询接口"""
    if table == "STK_INDEX_WEIGHTS":
        if index_code:
            return get_index_components(index_code, force_update=force_update)
        return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)
    elif table == "STK_INDEX_COMPONENTS":
        if index_code:
            return get_index_components(index_code, force_update=force_update)
        return pd.DataFrame(columns=_INDEX_COMPONENTS_SCHEMA)
    else:
        raise ValueError(f"不支持的表: {table}")


def get_index_weights(
    index_code: str,
    date: str = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取指数成分股权重。

    参数
    ----
    index_code   : 指数代码，如 '000300'、'000905'
    date         : 查询日期 (YYYY-MM-DD)，默认最新
    force_update : 强制更新
    use_duckdb   : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，包含 stock_code, weight, stock_name 字段
    """
    df = get_index_components(
        index_code,
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


def get_index_weights_history(
    index_code: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取指数成分股权重历史月度版本。

    参数
    ----
    index_code   : 指数代码，如 '000300'、'000905'
    start_date   : 起始日期 (YYYY-MM-DD)
    end_date     : 结束日期 (YYYY-MM-DD)
    force_update : 强制更新
    use_duckdb   : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，包含 date, stock_code, weight, stock_name 字段
    """
    index_num = index_code.split(".")[0] if "." in index_code else index_code
    index_num = index_num.zfill(6).replace("sh", "").replace("sz", "")

    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)

    month_dates = pd.date_range(start=start_dt, end=end_dt, freq="ME")

    all_results = []
    for month_end in month_dates:
        date_str = month_end.strftime("%Y-%m-%d")
        try:
            df = get_index_weights(
                index_code,
                date=date_str,
                force_update=force_update,
                use_duckdb=use_duckdb,
            )
            if not df.empty:
                df["date"] = date_str
                all_results.append(df)
        except Exception as e:
            logger.warning(f"[get_index_weights_history] 获取 {date_str} 权重失败: {e}")
            continue

    if not all_results:
        return pd.DataFrame(columns=["date", "stock_code", "weight", "stock_name"])

    return pd.concat(all_results, ignore_index=True)


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
            from jk2bt.data.sources import get_adapter

            df = get_adapter().get_index_stock_info()
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
        from jk2bt.data.sources import get_adapter

        df = get_adapter().get_index_component_sw(symbol=code_clean)
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
    "get_index_weights_history",
    "get_index_info",
    "get_industry_index_stocks",
    "get_index_component_history",
    "query_index_components",
    "run_query_simple",
    "FinanceQuery",
    "finance",
]
