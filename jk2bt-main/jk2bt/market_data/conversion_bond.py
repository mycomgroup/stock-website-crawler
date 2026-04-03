"""
market_data/conversion_bond.py
可转债数据获取模块。

主要功能：
1. 可转债行情查询 - finance.STK_CB_DAILY
2. FinanceQuery 类提供 finance.run_query 兼容接口
3. RobustResult 稳健接口

数据字段：
- bond_code: 可转债代码
- bond_name: 可转债名称
- stock_code: 正股代码（聚宽格式）
- close: 收盘价
- conversion_price: 转股价
- conversion_ratio: 转股比例
- premium_rate: 转股溢价率

缓存策略:
- DuckDB 缓存（优先）：存储在 data/conversion_bond.db 中
- 按日缓存：实时数据（1天）
"""

import os
import pandas as pd
from datetime import datetime
from typing import Optional, List, Union
import logging

logger = logging.getLogger(__name__)


class RobustResult:
    """稳健结果封装类"""

    def __init__(
        self, success: bool = True, data=None, reason: str = "", source: str = "network"
    ):
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


_CB_SCHEMA = [
    "bond_code",
    "bond_name",
    "stock_code",
    "close",
    "conversion_price",
    "conversion_ratio",
    "premium_rate",
    "date",
]


class ConversionBondDBManager:
    """可转债 DuckDB 管理器"""

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
            db_path = os.path.join(base_dir, "data", "conversion_bond.db")

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
                    CREATE TABLE IF NOT EXISTS conversion_bond (
                        bond_code VARCHAR NOT NULL,
                        bond_name VARCHAR,
                        stock_code VARCHAR,
                        close DOUBLE,
                        conversion_price DOUBLE,
                        conversion_ratio DOUBLE,
                        premium_rate DOUBLE,
                        date DATE NOT NULL,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (bond_code, date)
                    )
                """)
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_cb_code ON conversion_bond(bond_code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_cb_stock ON conversion_bond(stock_code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_cb_date ON conversion_bond(date)"
                )
                logger.info("可转债表结构初始化完成")
        except Exception as e:
            logger.warning(f"初始化表结构失败: {e}")

    def insert_cb(self, df: pd.DataFrame):
        if self._manager is None or df.empty:
            return

        df = df.copy()
        for col in _CB_SCHEMA:
            if col not in df.columns:
                df[col] = None

        if "update_time" not in df.columns:
            df["update_time"] = datetime.now()

        cols = _CB_SCHEMA + ["update_time"]
        df = df[cols]

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("INSERT OR REPLACE INTO conversion_bond SELECT * FROM df")
                logger.info(f"插入/更新 {len(df)} 条可转债信息")
        except Exception as e:
            logger.warning(f"插入可转债信息失败: {e}")

    def get_cb(self, bond_code: str) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_CB_SCHEMA)

        try:
            with self._manager._get_connection(read_only=True) as conn:
                df = conn.execute(
                    "SELECT * FROM conversion_bond WHERE bond_code = ? ORDER BY date DESC",
                    [bond_code],
                ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询可转债信息失败: {e}")
            return pd.DataFrame(columns=_CB_SCHEMA)

    def is_cache_valid(self, date_str: str, cache_days: int = 1) -> bool:
        if self._manager is None:
            return False

        try:
            with self._manager._get_connection(read_only=True) as conn:
                result = conn.execute(
                    "SELECT MAX(update_time) FROM conversion_bond WHERE date = ?",
                    [date_str],
                ).fetchone()
                if result and result[0]:
                    update_time = pd.to_datetime(result[0])
                    return (datetime.now() - update_time).days < cache_days
                return False
        except Exception:
            return False


_db_manager = ConversionBondDBManager() if _DUCKDB_AVAILABLE else None


def _normalize_stock_code(symbol: str) -> str:
    """标准化股票代码为聚宽格式"""
    if ".XSHG" in symbol or ".XSHE" in symbol:
        return symbol
    code = str(symbol).zfill(6)
    if code.startswith("6"):
        return code + ".XSHG"
    return code + ".XSHE"


def _parse_num(value) -> Optional[float]:
    if value is None or value == "" or value == "-":
        return None
    try:
        if isinstance(value, str):
            value = value.replace(",", "").replace("%", "").strip()
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


def get_conversion_bond_list(
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取可转债列表。

    参数
    ----
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，所有可转债基本信息
    """
    date_str = datetime.now().strftime("%Y-%m-%d")

    cache_file = os.path.join(cache_dir, "conversion_bond_list.pkl")
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
            try:
                import akshare as ak
            except ImportError:
                raise ImportError("请安装 akshare: pip install akshare")

            results = []

            try:
                df_jsl = ak.bond_cb_jsl()
                if df_jsl is not None and not df_jsl.empty:
                    for _, row in df_jsl.iterrows():
                        record = _parse_jsl_row(row, date_str)
                        if record:
                            results.append(record)
            except Exception as e:
                logger.debug(f"bond_cb_jsl 失败: {e}")

            try:
                df_cov = ak.bond_zh_cov()
                if df_cov is not None and not df_cov.empty:
                    for _, row in df_cov.iterrows():
                        record = _parse_cov_row(row, date_str)
                        if record:
                            results.append(record)
            except Exception as e:
                logger.debug(f"bond_zh_cov 失败: {e}")

            if results:
                result_df = pd.DataFrame(results)
                result_df = result_df.drop_duplicates(
                    subset=["bond_code"], keep="first"
                )
                result_df.to_pickle(cache_file)
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_cb(result_df)
                return result_df

        except Exception as e:
            logger.warning(f"[conversion_bond] 获取可转债列表失败: {e}")

    return pd.DataFrame(columns=_CB_SCHEMA)


def _parse_jsl_row(row, date_str: str) -> Optional[dict]:
    """解析 bond_cb_jsl 数据行"""
    try:
        stock_code = str(row.get("正股代码", ""))
        if stock_code:
            stock_code = _normalize_stock_code(stock_code)

        return {
            "bond_code": str(row.get("转债代码", "")),
            "bond_name": str(row.get("转债名称", "")),
            "stock_code": stock_code,
            "close": _parse_num(row.get("现价", 0)),
            "conversion_price": _parse_num(row.get("转股价", 0)),
            "conversion_ratio": _parse_num(row.get("转股比例", 0)),
            "premium_rate": _parse_num(row.get("溢价率", 0)),
            "date": date_str,
        }
    except Exception:
        return None


def _parse_cov_row(row, date_str: str) -> Optional[dict]:
    """解析 bond_zh_cov 数据行"""
    try:
        stock_code = str(row.get("正股代码", ""))
        if stock_code:
            stock_code = _normalize_stock_code(stock_code)

        return {
            "bond_code": str(row.get("债券代码", "")),
            "bond_name": str(row.get("债券名称", "")),
            "stock_code": stock_code,
            "close": _parse_num(row.get("收盘价", 0)),
            "conversion_price": _parse_num(row.get("转股价格", 0)),
            "conversion_ratio": None,
            "premium_rate": None,
            "date": date_str,
        }
    except Exception:
        return None


def get_conversion_bond(
    bond_code: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取单只可转债信息。

    参数
    ----
    bond_code   : 可转债代码
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，单只可转债信息
    """
    df_list = get_conversion_bond_list(
        cache_dir=cache_dir, force_update=force_update, use_duckdb=use_duckdb
    )

    if df_list.empty:
        return pd.DataFrame(columns=_CB_SCHEMA)

    df_filtered = df_list[df_list["bond_code"] == bond_code]

    return df_filtered if not df_filtered.empty else pd.DataFrame(columns=_CB_SCHEMA)


def query_conversion_bond(
    bond_codes: List[str],
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    批量查询可转债（finance.STK_CB_DAILY）。
    """
    if bond_codes is None or len(bond_codes) == 0:
        return pd.DataFrame(columns=_CB_SCHEMA)

    df_list = get_conversion_bond_list(
        cache_dir=cache_dir, force_update=force_update, use_duckdb=use_duckdb
    )

    if df_list.empty:
        return pd.DataFrame(columns=_CB_SCHEMA)

    df_filtered = df_list[df_list["bond_code"].isin(bond_codes)]

    return df_filtered if not df_filtered.empty else pd.DataFrame(columns=_CB_SCHEMA)


class FinanceQuery:
    """聚宽 finance 模块模拟器"""

    class STK_CB_DAILY:
        bond_code = None
        bond_name = None
        stock_code = None
        close = None
        conversion_price = None
        premium_rate = None

    class STK_CONVERSION_BOND_BASIC:
        bond_code = None
        bond_name = None
        stock_code = None
        conversion_price = None
        conversion_start_date = None
        conversion_end_date = None
        list_date = None
        maturity_date = None
        coupon_rate = None

    class STK_CONVERSION_BOND_PRICE:
        bond_code = None
        date = None
        open = None
        high = None
        low = None
        close = None
        volume = None
        amount = None

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
            if hasattr(query_obj.left, "__name__"):
                table_name = query_obj.left.__name__
            elif hasattr(query_obj.left, "__class__"):
                table_name = query_obj.left.__class__.__name__
            if hasattr(query_obj, "right"):
                conditions["bond_code"] = query_obj.right

        if table_name == "STK_CB_DAILY":
            if "bond_code" in conditions:
                return get_conversion_bond(
                    conditions["bond_code"], cache_dir=cache_dir, use_duckdb=use_duckdb
                )
            return get_conversion_bond_list(cache_dir=cache_dir, use_duckdb=use_duckdb)
        elif table_name == "STK_CONVERSION_BOND_BASIC":
            bond_code = conditions.get("bond_code")
            if bond_code:
                return query_conversion_bond_basic(
                    bond_code=bond_code,
                    use_cache=use_duckdb,
                )
            return query_conversion_bond_basic(use_cache=use_duckdb)
        elif table_name == "STK_CONVERSION_BOND_PRICE":
            bond_code = conditions.get("bond_code")
            if not bond_code:
                return pd.DataFrame()
            return query_conversion_bond_price(
                bond_code=bond_code,
                use_cache=use_duckdb,
            )
        elif table_name == "CONVERSION_BOND":
            return get_conversion_bond_list(cache_dir=cache_dir, use_duckdb=use_duckdb)
        else:
            logger.warning(f"[FinanceQuery] 不支持的表: {table_name}")
            return pd.DataFrame()


finance = FinanceQuery()


def get_conversion_bond_quote(
    bond_code: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """获取可转债行情数据"""
    return get_conversion_bond(
        bond_code, cache_dir=cache_dir, force_update=force_update
    )


def get_conversion_info(
    bond_code: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> dict:
    """获取可转债基本信息"""
    df = get_conversion_bond(bond_code, cache_dir=cache_dir, force_update=force_update)
    if df.empty:
        return {}
    return df.iloc[0].to_dict() if len(df) > 0 else {}


def calculate_conversion_value(
    conversion_price: float,
    stock_price: float,
) -> float:
    """计算转股价值"""
    if conversion_price <= 0:
        return 0.0
    return (100 / conversion_price) * stock_price


def calculate_premium_rate(
    bond_price: float,
    conversion_value: float,
) -> float:
    """计算溢价率"""
    if conversion_value <= 0:
        return 0.0
    return (bond_price / conversion_value - 1) * 100


def run_query_simple(
    table: str,
    bond_code: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """简化的查询接口"""
    if table == "STK_CB_DAILY":
        if bond_code:
            return get_conversion_bond(
                bond_code, cache_dir=cache_dir, force_update=force_update
            )
        return get_conversion_bond_list(cache_dir=cache_dir, force_update=force_update)
    else:
        raise ValueError(f"不支持的表: {table}")


def _normalize_bond_code(code: str) -> str:
    """标准化可转债代码为6位数字"""
    if code is None:
        return ""
    code = str(code).strip().upper()
    if not code:
        return ""
    code = code.replace(".XSHG", "").replace(".XSHE", "")
    code = code.replace("SH", "").replace("SZ", "")
    if not code:
        return ""
    return code.zfill(6)


def get_conversion_bond_list_robust(
    force_update: bool = False,
    use_cache: bool = True,
) -> RobustResult:
    """
    获取可转债列表（稳健版）。

    参数
    ----
    force_update : bool
        强制更新
    use_cache : bool
        是否使用缓存

    返回
    ----
    RobustResult
        success: 是否成功
        data: DataFrame，可转债列表
        reason: 失败原因
        source: 数据来源（cache/network）
    """
    try:
        df = get_conversion_bond_list(force_update=force_update, use_duckdb=use_cache)
        if df is not None and not df.empty:
            return RobustResult(
                success=True,
                data=df,
                reason="",
                source="cache" if use_cache and not force_update else "network",
            )
        return RobustResult(success=False, reason="可转债列表为空", source="network")
    except Exception as e:
        logger.warning(f"[get_conversion_bond_list_robust] 获取失败: {e}")
        return RobustResult(success=False, reason=str(e), source="network")


def get_conversion_bond_price(
    code: str,
    force_update: bool = False,
    use_cache: bool = True,
) -> RobustResult:
    """
    获取可转债行情数据（稳健版）。

    参数
    ----
    code : str
        可转债代码（支持多种格式：110XXX.XSHG, sh110XXX, 110XXX）
    force_update : bool
        强制更新
    use_cache : bool
        是否使用缓存

    返回
    ----
    RobustResult
        success: 是否成功
        data: DataFrame，可转债行情
        reason: 失败原因
        source: 数据来源
    """
    bond_code = _normalize_bond_code(code)

    if not bond_code:
        return RobustResult(success=False, reason="可转债代码不能为空", source="input")

    try:
        df = get_conversion_bond(
            bond_code, force_update=force_update, use_duckdb=use_cache
        )
        if df is not None and not df.empty:
            return RobustResult(
                success=True,
                data=df,
                reason="",
                source="cache" if use_cache and not force_update else "network",
            )
        return RobustResult(
            success=False,
            reason=f"未找到可转债 {bond_code} 的行情数据",
            source="network",
        )
    except Exception as e:
        logger.warning(f"[get_conversion_bond_price] 获取失败: {e}")
        return RobustResult(success=False, reason=str(e), source="network")


def get_conversion_bond_info(
    code: str,
    force_update: bool = False,
    use_cache: bool = True,
) -> RobustResult:
    """
    获取可转债基本信息（稳健版）。

    参数
    ----
    code : str
        可转债代码（支持多种格式）
    force_update : bool
        强制更新
    use_cache : bool
        是否使用缓存

    返回
    ----
    RobustResult
        success: 是否成功
        data: dict，可转债基本信息
        reason: 失败原因
        source: 数据来源
    """
    bond_code = _normalize_bond_code(code)

    if not bond_code:
        return RobustResult(success=False, reason="可转债代码不能为空", source="input")

    try:
        result = get_conversion_bond_price(
            bond_code, force_update=force_update, use_cache=use_cache
        )
        if result.success and not result.data.empty:
            info = result.data.iloc[0].to_dict()
            return RobustResult(
                success=True, data=info, reason="", source=result.source
            )
        return RobustResult(
            success=False,
            reason=f"未找到可转债 {bond_code} 的基本信息",
            source=result.source,
        )
    except Exception as e:
        logger.warning(f"[get_conversion_bond_info] 获取失败: {e}")
        return RobustResult(success=False, reason=str(e), source="network")


def get_conversion_bond_detail(code: str, use_cache: bool = True) -> RobustResult:
    """
    获取可转债详细信息（使用 akshare bond_cb_jsl 接口）。

    参数
    ----
    code : str
        可转债代码
    use_cache : bool
        是否使用缓存

    返回
    ----
    RobustResult
        success: 是否成功
        data: dict，可转债详细信息
        reason: 失败原因
        source: 数据来源
    """
    bond_code = _normalize_bond_code(code)

    if not bond_code:
        return RobustResult(success=False, reason="可转债代码不能为空", source="input")

    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.bond_cb_jsl()
        if df is not None and not df.empty:
            df_filtered = df[df["转债代码"].astype(str).str.zfill(6) == bond_code]
            if not df_filtered.empty:
                row = df_filtered.iloc[0]
                detail = {
                    "bond_code": str(row.get("转债代码", "")),
                    "bond_name": str(row.get("转债名称", "")),
                    "stock_code": _normalize_stock_code(str(row.get("正股代码", ""))),
                    "stock_name": str(row.get("正股名称", "")),
                    "close": _parse_num(row.get("现价", 0)),
                    "conversion_price": _parse_num(row.get("转股价", 0)),
                    "conversion_ratio": _parse_num(row.get("转股比例", 0)),
                    "premium_rate": _parse_num(row.get("溢价率", 0)),
                    "bond_value": _parse_num(row.get("纯债价值", 0)),
                    "conversion_value": _parse_num(row.get("转股价值", 0)),
                    "double_low": _parse_num(row.get("双低", 0)),
                    "remain_years": _parse_num(row.get("剩余年限", 0)),
                    "list_date": _parse_date(row.get("上市日期")),
                    "maturity_date": _parse_date(row.get("到期日期")),
                }
                return RobustResult(
                    success=True, data=detail, reason="", source="network"
                )
        return RobustResult(
            success=False,
            reason=f"未找到可转债 {bond_code} 的详细信息",
            source="network",
        )
    except Exception as e:
        logger.warning(f"[get_conversion_bond_detail] 获取失败: {e}")
        return RobustResult(success=False, reason=str(e), source="network")


def get_conversion_bond_by_stock(
    stock_code: str,
    use_cache: bool = True,
) -> RobustResult:
    """
    根据正股代码查询对应的可转债。

    参数
    ----
    stock_code : str
        正股代码（支持多种格式）
    use_cache : bool
        是否使用缓存

    返回
    ----
    RobustResult
        success: 是否成功
        data: DataFrame，可转债列表
        reason: 失败原因
        source: 数据来源
    """
    normalized_stock = _normalize_stock_code(stock_code)

    if not normalized_stock:
        return RobustResult(success=False, reason="正股代码不能为空", source="input")

    try:
        result = get_conversion_bond_list_robust(use_cache=use_cache)
        if result.success and not result.data.empty:
            df = result.data[result.data["stock_code"] == normalized_stock]
            if not df.empty:
                return RobustResult(
                    success=True, data=df, reason="", source=result.source
                )
        return RobustResult(
            success=False,
            reason=f"未找到正股 {normalized_stock} 对应的可转债",
            source=result.source,
        )
    except Exception as e:
        logger.warning(f"[get_conversion_bond_by_stock] 查询失败: {e}")
        return RobustResult(success=False, reason=str(e), source="network")


class STK_CONVERSION_BOND_BASIC:
    """可转债基本信息表（finance.STK_CONVERSION_BOND_BASIC）"""

    bond_code = None
    bond_name = None
    stock_code = None
    conversion_price = None
    conversion_start_date = None
    conversion_end_date = None
    list_date = None
    maturity_date = None
    coupon_rate = None


class STK_CONVERSION_BOND_PRICE:
    """可转债行情表（finance.STK_CONVERSION_BOND_PRICE）"""

    bond_code = None
    date = None
    open = None
    high = None
    low = None
    close = None
    volume = None
    amount = None


def get_conversion_value(
    code: str,
    stock_price: float = None,
    use_cache: bool = True,
) -> RobustResult:
    """
    根据可转债代码计算转股价值。

    参数
    ----
    code : str
        可转债代码
    stock_price : float
        正股价格（可选，不传则尝试获取实时价格）
    use_cache : bool
        是否使用缓存

    返回
    ----
    RobustResult
        success: 是否成功
        data: dict，包含 conversion_value, premium_rate 等
        reason: 失败原因
        source: 数据来源
    """
    bond_code = _normalize_bond_code(code)
    if not bond_code:
        return RobustResult(success=False, reason="可转债代码不能为空", source="input")

    try:
        info_result = get_conversion_bond_detail(bond_code, use_cache=use_cache)
        if not info_result.success:
            return info_result

        info = info_result.data
        conversion_price = info.get("conversion_price", 0)

        if conversion_price <= 0:
            return RobustResult(
                success=False,
                reason=f"可转债 {bond_code} 转股价无效",
                source="data",
            )

        if stock_price is None:
            stock_price = info.get("close", 0)
            if stock_price <= 0:
                stock_price = info.get("stock_price", 0)

        if stock_price is None or stock_price <= 0:
            return RobustResult(
                success=False,
                reason=f"无法获取正股价格",
                source="data",
            )

        conversion_value = calculate_conversion_value(conversion_price, stock_price)
        bond_price = info.get("close", 0)
        premium_rate = (
            calculate_premium_rate(bond_price, conversion_value)
            if bond_price > 0
            else None
        )

        result_data = {
            "bond_code": bond_code,
            "bond_name": info.get("bond_name", ""),
            "stock_code": info.get("stock_code", ""),
            "conversion_price": conversion_price,
            "stock_price": stock_price,
            "bond_price": bond_price,
            "conversion_value": conversion_value,
            "premium_rate": premium_rate,
            "conversion_ratio": 100 / conversion_price if conversion_price > 0 else 0,
        }

        return RobustResult(
            success=True, data=result_data, reason="", source="calculated"
        )
    except Exception as e:
        logger.warning(f"[get_conversion_value] 计算失败: {e}")
        return RobustResult(success=False, reason=str(e), source="network")


def query_conversion_bond_basic(
    bond_code: str = None,
    stock_code: str = None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    查询可转债基本信息（finance.STK_CONVERSION_BOND_BASIC）。

    参数
    ----
    bond_code : str
        可转债代码（可选）
    stock_code : str
        正股代码（可选）
    use_cache : bool
        是否使用缓存

    返回
    ----
    pd.DataFrame
        可转债基本信息
    """
    result = get_conversion_bond_list_robust(use_cache=use_cache)
    if not result.success:
        return pd.DataFrame()

    df = result.data
    if bond_code:
        bond_code = _normalize_bond_code(bond_code)
        df = df[df["bond_code"] == bond_code]
    if stock_code:
        stock_code = _normalize_stock_code(stock_code)
        df = df[df["stock_code"] == stock_code]

    return df


def query_conversion_bond_price(
    bond_code: str,
    start_date: str = None,
    end_date: str = None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    查询可转债行情（finance.STK_CONVERSION_BOND_PRICE）。

    参数
    ----
    bond_code : str
        可转债代码
    start_date : str
        起始日期 YYYY-MM-DD（可选）
    end_date : str
        结束日期 YYYY-MM-DD（可选）
    use_cache : bool
        是否使用缓存

    返回
    ----
    pd.DataFrame
        可转债行情数据
    """
    result = get_conversion_bond_price(bond_code, use_cache=use_cache)
    if not result.success:
        return pd.DataFrame()

    df = result.data
    if start_date:
        df = df[df["date"] >= start_date]
    if end_date:
        df = df[df["date"] <= end_date]

    return df


def get_conversion_bond_history(
    bond_code: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取可转债历史行情数据（尝试从 akshare 获取历史数据）。

    参数
    ----
    bond_code : str
        可转债代码
    start_date : str
        聚宽日期格式 YYYY-MM-DD
    end_date : str
        聚宽日期格式 YYYY-MM-DD
    force_update : bool
        强制更新

    返回
    ----
    pd.DataFrame
        历史行情数据
    """
    bond_code = _normalize_bond_code(bond_code)
    if not bond_code:
        return pd.DataFrame()

    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        symbol_format = _get_bond_symbol_format(bond_code)
        df = ak.bond_zh_hs_daily(symbol=symbol_format)
        if df is not None and not df.empty:
            df = _standardize_bond_daily(df)
            df["datetime"] = pd.to_datetime(df["datetime"])
            if start_date:
                df = df[df["datetime"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["datetime"] <= pd.to_datetime(end_date)]
            return df
    except Exception as e:
        logger.debug(f"[get_conversion_bond_history] akshare获取失败: {e}")

    return pd.DataFrame()


def get_conversion_price(bond_code: str, use_cache: bool = True) -> Optional[float]:
    """
    获取可转债转股价。

    参数
    ----
    bond_code : str
        可转债代码（支持多种格式）
    use_cache : bool
        是否使用缓存

    返回
    ----
    float or None
        转股价，获取失败返回 None
    """
    bond_code = _normalize_bond_code(bond_code)
    if not bond_code:
        logger.warning("可转债代码不能为空")
        return None

    try:
        result = get_conversion_bond_price(bond_code, use_cache=use_cache)
        if result.success and not result.data.empty:
            conversion_price = result.data.iloc[0].get("conversion_price")
            if conversion_price is not None and conversion_price > 0:
                return float(conversion_price)
        return None
    except Exception as e:
        logger.warning(f"[get_conversion_price] 获取转股价失败: {e}")
        return None


def calculate_conversion_premium(
    bond_code: str, use_cache: bool = True
) -> Optional[float]:
    """
    计算可转债转股溢价率。

    参数
    ----
    bond_code : str
        可转债代码
    use_cache : bool
        是否使用缓存

    返回
    ----
    float or None
        溢价率（百分比），获取失败返回 None
    """
    bond_code = _normalize_bond_code(bond_code)
    if not bond_code:
        logger.warning("可转债代码不能为空")
        return None

    try:
        result = get_conversion_bond_price(bond_code, use_cache=use_cache)
        if result.success and not result.data.empty:
            premium_rate = result.data.iloc[0].get("premium_rate")
            if premium_rate is not None:
                return float(premium_rate)
        return None
    except Exception as e:
        logger.warning(f"[calculate_conversion_premium] 计算溢价率失败: {e}")
        return None


def get_conversion_bond_daily(
    bond_code: str,
    start_date: str,
    end_date: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取可转债日线行情数据。

    参数
    ----
    bond_code : str
        可转债代码
    start_date : str
        起始日期 'YYYY-MM-DD'
    end_date : str
        结束日期 'YYYY-MM-DD'
    force_update : bool
        强制更新

    返回
    ----
    pd.DataFrame
        日线数据（datetime/open/high/low/close/volume）
    """
    bond_code = _normalize_bond_code(bond_code)
    if not bond_code:
        logger.warning("可转债代码不能为空")
        return pd.DataFrame()

    cache_file = os.path.join("finance_cache", f"cb_daily_{bond_code}.pkl")
    os.makedirs("finance_cache", exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            cached_df["datetime"] = pd.to_datetime(cached_df["datetime"])
            filtered = cached_df[
                (cached_df["datetime"] >= pd.to_datetime(start_date))
                & (cached_df["datetime"] <= pd.to_datetime(end_date))
            ]
            if not filtered.empty:
                return filtered.copy()
            need_download = True
        except Exception:
            need_download = True

    if need_download:
        try:
            try:
                import akshare as ak
            except ImportError:
                raise ImportError("请安装 akshare: pip install akshare")

            symbol_format = _get_bond_symbol_format(bond_code)
            df = ak.bond_zh_hs_daily(symbol=symbol_format)

            if df is None or df.empty:
                logger.warning(f"可转债 {bond_code} 日线数据为空")
                return pd.DataFrame()

            df = _standardize_bond_daily(df)
            df.to_pickle(cache_file)

            df["datetime"] = pd.to_datetime(df["datetime"])
            filtered = df[
                (df["datetime"] >= pd.to_datetime(start_date))
                & (df["datetime"] <= pd.to_datetime(end_date))
            ]
            return filtered.copy()

        except Exception as e:
            logger.warning(f"[get_conversion_bond_daily] 获取日线数据失败: {e}")

    return pd.DataFrame()


def _get_bond_symbol_format(bond_code: str) -> str:
    """将债券代码转换为 akshare 格式"""
    code = str(bond_code).zfill(6)
    if code.startswith(("11", "13")):
        return f"sh{code}"
    elif code.startswith(("12", "14")):
        return f"sz{code}"
    return f"sh{code}"


def _standardize_bond_daily(df: pd.DataFrame) -> pd.DataFrame:
    """标准化可转债日线数据"""
    df = df.copy()
    column_map = {
        "date": "datetime",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
    }
    for old_col, new_col in column_map.items():
        if old_col in df.columns:
            df[new_col] = df[old_col]
    df["datetime"] = pd.to_datetime(df["datetime"])
    result_cols = ["datetime", "open", "high", "low", "close", "volume"]
    result_df = df[[col for col in result_cols if col in df.columns]].copy()
    for col in ["open", "high", "low", "close", "volume"]:
        if col in result_df.columns:
            result_df[col] = pd.to_numeric(result_df[col], errors="coerce")
    return result_df


class CONVERSION_BOND:
    """finance.run_query 兼容表"""

    bond_code = None
    bond_name = None
    stock_code = None
    close = None
    conversion_price = None
    premium_rate = None
    conversion_ratio = None


finance.CONVERSION_BOND = CONVERSION_BOND
finance.STK_CONVERSION_BOND_BASIC = STK_CONVERSION_BOND_BASIC
finance.STK_CONVERSION_BOND_PRICE = STK_CONVERSION_BOND_PRICE
