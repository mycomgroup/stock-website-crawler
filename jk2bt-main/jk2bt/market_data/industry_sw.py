"""
market_data/industry_sw.py
申万行业数据获取模块。

主要功能：
1. 申万行业分类查询 - finance.STK_INDUSTRY_SW
2. FinanceQuery 类提供 finance.run_query 兼容接口

数据字段：
- code: 股票代码（聚宽格式）
- industry_name: 行业名称
- industry_code: 行业代码
- level: 行业层级（一级/二级/三级）

缓存策略:
- DuckDB 缓存（优先）：存储在 data/industry_sw.db 中
- 按季度缓存：静态数据
"""

import os
import pandas as pd
from datetime import datetime
from typing import Optional, List, Union
import logging
import warnings

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


DEFAULT_INDUSTRY_SCHEMA = {
    "level1_code": "",
    "level1_name": "",
    "level2_code": "",
    "level2_name": "",
    "level3_code": "",
    "level3_name": "",
}


class RobustResult:
    """稳健结果类"""

    def __init__(
        self,
        success: bool = True,
        data=None,
        reason: str = "",
        source: str = "network",
    ):
        self.success = success
        self.data = data if data is not None else pd.DataFrame()
        self.reason = reason
        self.source = source

    def __bool__(self):
        return self.success

    def __repr__(self):
        status = "SUCCESS" if self.success else "FAILED"
        return f"RobustResult({status}, source={self.source}, reason={self.reason})"

    def is_empty(self) -> bool:
        if self.data is None:
            return True
        if isinstance(self.data, pd.DataFrame):
            return self.data.empty
        if isinstance(self.data, (list, dict)):
            return len(self.data) == 0
        return False


class SWIndustryCache:
    """申万行业缓存管理类"""

    _instance = None
    CACHE_DIR = "finance_cache/industry_sw"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._cache = {}
            cls._instance._init_cache_dir()
        return cls._instance

    def _init_cache_dir(self):
        os.makedirs(self.CACHE_DIR, exist_ok=True)

    def _get_cache_path(self, cache_type: str) -> str:
        return os.path.join(self.CACHE_DIR, f"{cache_type}.pkl")

    def get(self, key: str):
        return self._cache.get(key)

    def set(self, key: str, data):
        self._cache[key] = data

    def clear(self):
        self._cache.clear()


_INDUSTRY_SW_SCHEMA = [
    "code",
    "industry_name",
    "industry_code",
    "level",
]


class IndustrySWDBManager:
    """申万行业 DuckDB 管理器（延迟初始化）"""

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

        if not _DUCKDB_AVAILABLE:
            self._manager = None
            self._initialized = True
            return

        if db_path is None:
            base_dir = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            db_path = os.path.join(base_dir, "data", "industry_sw.db")

        self._db_path = db_path
        self._manager = None

        try:
            self._manager = DuckDBManager(db_path=db_path, read_only=False)
            self._init_tables()
        except Exception as e:
            logger.warning(f"DuckDB 初始化失败: {e}")
            self._manager = None

        self._initialized = True

    def _init_tables(self):
        if self._manager is None:
            return

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS industry_sw (
                        code VARCHAR NOT NULL,
                        industry_name VARCHAR,
                        industry_code VARCHAR,
                        level VARCHAR,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (code, level)
                    )
                """)
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_ind_sw_code ON industry_sw(code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_ind_sw_ind ON industry_sw(industry_code)"
                )
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS sw_industry_list (
                        industry_code VARCHAR NOT NULL,
                        industry_name VARCHAR,
                        level INTEGER,
                        parent_code VARCHAR,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (industry_code, level)
                    )
                """)
                logger.info("申万行业表结构初始化完成")
        except Exception as e:
            logger.warning(f"初始化表结构失败: {e}")

    def insert_industry(self, df: pd.DataFrame):
        if self._manager is None or df.empty:
            return

        df = df.copy()
        for col in _INDUSTRY_SW_SCHEMA:
            if col not in df.columns:
                df[col] = None

        if "update_time" not in df.columns:
            df["update_time"] = datetime.now()

        cols = _INDUSTRY_SW_SCHEMA + ["update_time"]
        df = df[cols]

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("INSERT OR REPLACE INTO industry_sw SELECT * FROM df")
                logger.info(f"插入/更新 {len(df)} 条申万行业信息")
        except Exception as e:
            logger.warning(f"插入申万行业信息失败: {e}")

    def insert_industry_list(self, df: pd.DataFrame, level: int):
        if self._manager is None or df.empty:
            return

        df = df.copy()
        df["level"] = level
        df["update_time"] = datetime.now()

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("INSERT OR REPLACE INTO sw_industry_list SELECT * FROM df")
                logger.info(f"插入/更新 {len(df)} 条申万行业列表")
        except Exception as e:
            logger.warning(f"插入申万行业列表失败: {e}")

    def get_industry(self, code: str) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_INDUSTRY_SW_SCHEMA)

        try:
            with self._manager._get_connection(read_only=True) as conn:
                df = conn.execute(
                    "SELECT * FROM industry_sw WHERE code = ?",
                    [code],
                ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询申万行业信息失败: {e}")
            return pd.DataFrame(columns=_INDUSTRY_SW_SCHEMA)

    def get_industry_list(self, level: int) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame()

        try:
            with self._manager._get_connection(read_only=True) as conn:
                df = conn.execute(
                    "SELECT * FROM sw_industry_list WHERE level = ?",
                    [level],
                ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询申万行业列表失败: {e}")
            return pd.DataFrame()

    def is_cache_valid(self, code: str = None, cache_days: int = 90) -> bool:
        if self._manager is None:
            return False

        try:
            with self._manager._get_connection(read_only=True) as conn:
                if code:
                    result = conn.execute(
                        "SELECT MAX(update_time) FROM industry_sw WHERE code = ?",
                        [code],
                    ).fetchone()
                else:
                    result = conn.execute(
                        "SELECT MAX(update_time) FROM sw_industry_list"
                    ).fetchone()
                if result and result[0]:
                    update_time = pd.to_datetime(result[0])
                    return (datetime.now() - update_time).days < cache_days
                return False
        except Exception:
            return False


def _get_db_manager():
    """获取数据库管理器单例（延迟初始化）"""
    if not _DUCKDB_AVAILABLE:
        return None
    manager = IndustrySWDBManager()
    manager._ensure_initialized()
    return manager

_db_manager = None  # 延迟初始化，避免导入时副作用


def _extract_code_num(symbol: str) -> str:
    if isinstance(symbol, (int, float)):
        return str(int(symbol)).zfill(6)
    symbol = str(symbol)
    if symbol.startswith("sh") or symbol.startswith("sz"):
        return symbol[2:].zfill(6)
    if ".XSHG" in symbol or ".XSHE" in symbol:
        return symbol.split(".")[0].zfill(6)
    return symbol.zfill(6)


def _normalize_to_jq(symbol: str) -> str:
    if isinstance(symbol, (int, float)):
        symbol = str(int(symbol)).zfill(6)
    symbol = str(symbol)
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


def _normalize_stock_code(symbol: str) -> str:
    return _extract_code_num(symbol)


def get_sw_industry_list(level: int = 1) -> RobustResult:
    """
    获取申万行业列表。

    参数
    ----
    level : int
        行业级别（1/2/3），默认一级

    返回
    ----
    RobustResult，data 为 DataFrame：
    - industry_code: 行业代码
    - industry_name: 行业名称
    - level: 行业级别
    """
    if level not in [1, 2, 3]:
        return RobustResult(
            success=False,
            data=pd.DataFrame(),
            reason=f"不支持的行业级别: {level}，支持 1/2/3",
            source="error",
        )

    db_manager = _get_db_manager()
    if db_manager is not None:
        if db_manager.is_cache_valid(cache_days=90):
            df_cached = db_manager.get_industry_list(level)
            if not df_cached.empty:
                return RobustResult(success=True, data=df_cached, source="cache")

    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.stock_board_industry_name_em()
        if df is not None and not df.empty:
            result = pd.DataFrame()
            result["industry_code"] = df.get("行业代码", df.get("板块代码", ""))
            result["industry_name"] = df.get("行业名称", df.get("板块名称", ""))
            result["level"] = [level] * len(df)

            db_manager = _get_db_manager()
            if db_manager is not None:
                db_manager.insert_industry_list(result, level)

            return RobustResult(success=True, data=result, source="network")
    except Exception as e:
        logger.warning(f"[get_sw_industry_list] 获取失败: {e}")
        return RobustResult(
            success=False, data=pd.DataFrame(), reason=str(e), source="error"
        )

    return RobustResult(
        success=False, data=pd.DataFrame(), reason="无数据", source="error"
    )


def get_stock_industry(symbol: str, use_cache: bool = True) -> RobustResult:
    """
    获取股票所属行业。

    参数
    ----
    symbol   : 股票代码（支持多种格式）
    use_cache: 是否使用缓存

    返回
    ----
    RobustResult，data 为字典：
    - level1_code: 一级行业代码
    - level1_name: 一级行业名称
    - level2_code: 二级行业代码
    - level2_name: 二级行业名称
    - level3_code: 三级行业代码
    - level3_name: 三级行业名称
    """
    code_num = _extract_code_num(symbol)
    jq_code = _normalize_to_jq(symbol)

    if use_cache:
        db_manager = _get_db_manager()
        if db_manager is not None and db_manager.is_cache_valid(jq_code, cache_days=90):
            df_cached = db_manager.get_industry(jq_code)
            if not df_cached.empty:
                result = DEFAULT_INDUSTRY_SCHEMA.copy()
                for row in df_cached.itertuples():
                    level = row.level if hasattr(row, "level") else "一级"
                    if level == "一级" or "一" in str(level):
                        result["level1_code"] = row.industry_code
                        result["level1_name"] = row.industry_name
                    elif level == "二级" or "二" in str(level):
                        result["level2_code"] = row.industry_code
                        result["level2_name"] = row.industry_name
                    elif level == "三级" or "三" in str(level):
                        result["level3_code"] = row.industry_code
                        result["level3_name"] = row.industry_name
                return RobustResult(success=True, data=result, source="cache")

    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.stock_individual_info_em(symbol=code_num)
        if df is not None and not df.empty:
            result = DEFAULT_INDUSTRY_SCHEMA.copy()
            for _, row in df.iterrows():
                item = str(row.get("item", ""))
                value = str(row.get("value", ""))
                if "行业" in item:
                    result["level1_name"] = value

            df_industry = pd.DataFrame(
                [
                    {
                        "code": jq_code,
                        "industry_name": result["level1_name"],
                        "industry_code": "",
                        "level": "一级",
                    }
                ]
            )

            db_manager = _get_db_manager()
            if db_manager is not None:
                db_manager.insert_industry(df_industry)

            return RobustResult(success=True, data=result, source="network")
    except Exception as e:
        logger.warning(f"[get_stock_industry] 获取失败 {symbol}: {e}")

    return RobustResult(
        success=False,
        data=DEFAULT_INDUSTRY_SCHEMA.copy(),
        reason="未找到行业数据",
        source="error",
    )


def get_industry_stocks(
    industry_name: str,
    level: int = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取行业内股票列表（统一入口）。

    参数
    ----
    industry_name: 行业名称或行业代码
    level        : 行业层级（1/2/3），可选
    force_update : 强制更新

    返回
    ----
    DataFrame，包含以下字段：
    - code: 股票代码（聚宽格式）
    - stock_name: 股票名称
    - industry_name: 行业名称
    - industry_code: 行业代码（可选）
    - level: 行业层级（可选）
    """
    _INDUSTRY_STOCKS_SCHEMA = ["code", "stock_name", "industry_name"]
    if level:
        _INDUSTRY_STOCKS_SCHEMA.extend(["industry_code", "level"])

    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.stock_board_industry_cons_em(symbol=industry_name)
        if df is not None and not df.empty:
            result = pd.DataFrame()
            code_col = "代码" if "代码" in df.columns else "股票代码"
            name_col = "名称" if "名称" in df.columns else "股票名称"
            result["code"] = df[code_col].apply(lambda x: _normalize_to_jq(str(x)))
            result["industry_name"] = [industry_name] * len(df)
            if name_col in df.columns:
                result["stock_name"] = df[name_col]
            else:
                result["stock_name"] = ""
            if level:
                result["level"] = level
                result["industry_code"] = ""
            return result
    except Exception as e:
        logger.warning(f"[get_industry_stocks] 获取失败 {industry_name}: {e}")

    return pd.DataFrame(columns=_INDUSTRY_STOCKS_SCHEMA)


def get_industry_performance(industry_code: str = None) -> RobustResult:
    """
    获取行业表现数据。

    参数
    ----
    industry_code: 行业代码（可选，不传则返回所有行业）

    返回
    ----
    RobustResult，data 为 DataFrame：
    - industry_code: 行业代码
    - industry_name: 行业名称
    - pct_change: 涨跌幅
    """
    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.stock_board_industry_name_em()
        if df is not None and not df.empty:
            result = pd.DataFrame()
            result["industry_code"] = df.get("行业代码", df.get("板块代码", ""))
            result["industry_name"] = df.get("行业名称", df.get("板块名称", ""))
            result["pct_change"] = df.get("涨跌幅", df.get("板块涨跌幅", 0))

            if industry_code:
                result = result[result["industry_code"] == industry_code]

            return RobustResult(success=True, data=result, source="network")
    except Exception as e:
        logger.warning(f"[get_industry_performance] 获取失败: {e}")
        return RobustResult(
            success=False, data=pd.DataFrame(), reason=str(e), source="error"
        )

    return RobustResult(
        success=False, data=pd.DataFrame(), reason="无数据", source="error"
    )


get_industry_sw = get_stock_industry


def get_industry_classify(security, level: int = 1) -> pd.DataFrame:
    """
    获取股票所属行业。

    参数
    ----
    security : str
        股票代码（支持多种格式）
    level : int
        行业层级（1/2/3），默认一级

    返回
    ----
    pd.DataFrame
        包含行业代码、行业名称
    """
    result = get_stock_industry(security, use_cache=True)
    if not result.success:
        return pd.DataFrame(columns=["industry_code", "industry_name"])

    level_key = f"level{level}_code"
    level_name_key = f"level{level}_name"

    industry_code = result.data.get(level_key, "")
    industry_name = result.data.get(level_name_key, "")

    return pd.DataFrame(
        {"industry_code": [industry_code], "industry_name": [industry_name]}
    )


def get_all_industries(level: int = 1) -> pd.DataFrame:
    """
    获取所有行业列表。

    参数
    ----
    level : int
        行业层级（1/2/3），默认一级

    返回
    ----
    pd.DataFrame
        包含行业代码、名称
    """
    result = get_sw_industry_list(level)
    if result.success:
        return result.data
    return pd.DataFrame(columns=["industry_code", "industry_name", "level"])


def get_industry_sw_batch(codes: List[str], use_cache: bool = True) -> RobustResult:
    """批量查询股票行业分类"""
    if not codes or len(codes) == 0:
        return RobustResult(
            success=False,
            data=pd.DataFrame(),
            reason="股票代码列表为空",
            source="error",
        )

    dfs = []
    for code in codes:
        try:
            result = get_stock_industry(code, use_cache=use_cache)
            if result.success:
                df_row = pd.DataFrame([result.data])
                df_row["code"] = _normalize_to_jq(code)
                dfs.append(df_row)
        except Exception:
            continue

    if not dfs:
        return RobustResult(success=False, reason="No data found")

    result_df = pd.concat(dfs, ignore_index=True)
    return RobustResult(success=True, data=result_df)


def filter_stocks_by_industry(
    industry_name: str,
    codes: List[str] = None,
    level: int = 1,
) -> RobustResult:
    """
    按行业筛选股票。

    参数
    ----
    industry_name: 行业名称
    codes        : 股票池（可选）
    level        : 行业级别

    返回
    ----
    RobustResult，data 为股票代码列表
    """
    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.stock_board_industry_cons_em(symbol=industry_name)
        if df is not None and not df.empty:
            stocks = []
            code_col = "代码" if "代码" in df.columns else "股票代码"
            for code in df[code_col]:
                jq_code = _normalize_to_jq(str(code))
                if codes is None or jq_code in codes:
                    stocks.append(jq_code)
            return RobustResult(success=True, data=stocks, source="network")
    except Exception as e:
        logger.warning(f"[filter_stocks_by_industry] 获取失败: {e}")
        return RobustResult(success=False, data=[], reason=str(e), source="error")

    return RobustResult(success=False, data=[], reason="无数据", source="error")


def get_industry_stocks_sw(industry_name: str) -> RobustResult:
    """
    获取行业内股票列表（返回 RobustResult）。

    参数
    ----
    industry_name: 行业名称或行业代码

    返回
    ----
    RobustResult，data 为股票代码列表（聚宽格式）
    """
    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.stock_board_industry_cons_em(symbol=industry_name)
        if df is not None and not df.empty:
            stocks = []
            code_col = "代码" if "代码" in df.columns else "股票代码"
            for code in df[code_col]:
                stocks.append(_normalize_to_jq(str(code)))
            return RobustResult(success=True, data=stocks, source="network")
    except Exception as e:
        logger.warning(f"[get_industry_stocks_sw] 获取失败 {industry_name}: {e}")
        return RobustResult(success=False, data=[], reason=str(e), source="error")

    return RobustResult(success=False, data=[], reason="无数据", source="error")


def get_all_industry_mapping(level: int = 1) -> RobustResult:
    """获取行业映射"""
    return get_sw_industry_list(level)


def get_industry_performance_sw(date: str = None) -> RobustResult:
    """获取行业表现"""
    return get_industry_performance()


def get_sw_level1() -> pd.DataFrame:
    """获取申万一级行业列表"""
    result = get_sw_industry_list(1)
    return result.data if result.success else pd.DataFrame()


def get_sw_level2() -> pd.DataFrame:
    """获取申万二级行业列表"""
    result = get_sw_industry_list(2)
    return result.data if result.success else pd.DataFrame()


def get_sw_level3() -> pd.DataFrame:
    """获取申万三级行业列表"""
    result = get_sw_industry_list(3)
    return result.data if result.success else pd.DataFrame()


class FinanceQuery:
    """聚宽 finance 模块模拟器"""

    class STK_INDUSTRY_SW:
        code = None
        industry_name = None
        industry_code = None
        level = None

    class STK_SW_INDUSTRY:
        code = None
        industry_name = None
        industry_code = None
        level = None

    class STK_SW_INDUSTRY_STOCK:
        industry_code = None
        industry_name = None
        code = None
        level = None

    def run_query(
        self, query_obj, cache_dir="finance_cache", force_update=False, use_duckdb=True
    ) -> pd.DataFrame:
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

        if table_name == "STK_INDUSTRY_SW" or table_name == "STK_SW_INDUSTRY":
            if "code" in conditions:
                result = get_stock_industry(conditions["code"], use_cache=use_duckdb)
                if result.success:
                    return pd.DataFrame([result.data])
                return pd.DataFrame(columns=list(DEFAULT_INDUSTRY_SCHEMA.keys()))
            return pd.DataFrame(columns=list(DEFAULT_INDUSTRY_SCHEMA.keys()))
        elif table_name == "STK_SW_INDUSTRY_STOCK":
            if "industry_name" in conditions:
                return get_industry_stocks(conditions["industry_name"])
            elif "industry_code" in conditions:
                return get_industry_stocks(conditions["industry_code"])
            return pd.DataFrame(columns=["code", "industry_name"])
        else:
            raise ValueError(f"不支持的表: {table_name}")


finance = FinanceQuery()

STK_INDUSTRY_SW = FinanceQuery.STK_INDUSTRY_SW
STK_SW_INDUSTRY = FinanceQuery.STK_SW_INDUSTRY
STK_SW_INDUSTRY_STOCK = FinanceQuery.STK_SW_INDUSTRY_STOCK


def run_query_simple(
    table: str,
    code: str = None,
    industry_code: str = None,
    industry_name: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """简化的查询接口"""
    if table == "STK_INDUSTRY_SW" or table == "STK_SW_INDUSTRY":
        if code:
            result = get_stock_industry(code, use_cache=True)
            if result.success:
                return pd.DataFrame([result.data])
            return pd.DataFrame(columns=list(DEFAULT_INDUSTRY_SCHEMA.keys()))
        return pd.DataFrame(columns=list(DEFAULT_INDUSTRY_SCHEMA.keys()))
    elif table == "STK_SW_INDUSTRY_STOCK":
        if industry_name:
            return get_industry_stocks(industry_name)
        elif industry_code:
            return get_industry_stocks(industry_code)
        return pd.DataFrame(columns=["code", "industry_name"])
    else:
        raise ValueError(f"不支持的表: {table}")


def query_industry_sw(
    symbols: List[str],
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """批量查询申万行业（finance.STK_INDUSTRY_SW）"""
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=list(DEFAULT_INDUSTRY_SCHEMA.keys()))

    dfs = []
    for symbol in symbols:
        try:
            result = get_stock_industry(symbol, use_cache=use_duckdb)
            if result.success:
                df_row = pd.DataFrame([result.data])
                df_row["code"] = _normalize_to_jq(symbol)
                dfs.append(df_row)
        except Exception as e:
            logger.warning(f"[query_industry_sw] 获取 {symbol} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=list(DEFAULT_INDUSTRY_SCHEMA.keys()))

    return pd.concat(dfs, ignore_index=True)


def get_industry_category(
    symbol: str,
    level: int = 1,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取股票的行业分类（兼容旧接口）。

    参数
    ----
    symbol      : 股票代码
    level       : 行业级别
    force_update: 强制更新

    返回
    ----
    DataFrame，包含 industry_code, industry_name 等字段
    """
    result = get_stock_industry(symbol, use_cache=not force_update)
    if result.success:
        df = pd.DataFrame([result.data])
        df["code"] = _normalize_to_jq(symbol)
        return df
    return pd.DataFrame(columns=list(DEFAULT_INDUSTRY_SCHEMA.keys()))


def get_all_industries(level: int = 1) -> pd.DataFrame:
    """
    获取所有行业列表（兼容旧接口）。

    参数
    ----
    level: 行业级别（1/2/3）

    返回
    ----
    DataFrame，包含 industry_code, industry_name 字段
    """
    result = get_sw_industry_list(level)
    if result.success:
        return result.data
    return pd.DataFrame()


__all__ = [
    "get_sw_industry_list",
    "get_stock_industry",
    "get_industry_stocks",
    "get_industry_performance",
    "get_industry_sw",
    "query_industry_sw",
    "get_industry_sw_batch",
    "filter_stocks_by_industry",
    "get_industry_stocks_sw",
    "get_all_industry_mapping",
    "get_industry_performance_sw",
    "get_sw_level1",
    "get_sw_level2",
    "get_sw_level3",
    "get_industry_category",
    "get_all_industries",
    "RobustResult",
    "SWIndustryCache",
    "DEFAULT_INDUSTRY_SCHEMA",
    "finance",
    "FinanceQuery",
    "run_query_simple",
    "STK_INDUSTRY_SW",
    "STK_SW_INDUSTRY",
    "STK_SW_INDUSTRY_STOCK",
]
