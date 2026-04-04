"""
market_data/option.py
期权数据获取模块。

主要功能：
1. 期权列表查询 - ETF期权、股指期权
2. 期权行情查询 - 实时行情数据
3. 期权希腊字母 - Delta, Gamma, Theta, Vega
4. FinanceQuery 类提供 finance.run_query 兼容接口

数据字段（JoinQuant 对齐）：
- option_code: 期权代码
- option_name: 期权名称
- underlying_code: 标的代码（JoinQuant 标准字段）
- underlying: 标的代码（兼容别名）
- underlying_name: 标的名称
- strike: 行权价
- expiry_date: 到期日
- option_type: 期权类型（看涨/看跌，Call/Put）
- contract_unit: 合约单位
- exercise_type: 行权类型（欧式）
- listing_date: 上市日期
- close: 收盘价
- volume: 成交量
- date: 日期

缓存策略:
- DuckDB 缓存（优先）：存储在 data/option.db 中
- 按日缓存：实时数据
"""

__all__ = [
    "get_option_list",
    "get_option_price",
    "get_option_quote",
    "get_option_greeks",
    "get_option_chain",
    "get_option",
    "query_option",
    "get_option_info",
    "get_option_daily",
    "RobustResult",
    "FinanceQuery",
    "finance",
    "run_query_simple",
    "OptionDBManager",
    "OPTION_SCHEMA",
    "OPTION_BASIC_SCHEMA",
    "OPTION_DAILY_SCHEMA",
    "GREEKS_SCHEMA",
]

import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Union
import logging
import pickle

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


_OPTION_SCHEMA = [
    "option_code",
    "option_name",
    "underlying_code",
    "underlying",
    "underlying_name",
    "strike",
    "expiry_date",
    "option_type",
    "contract_unit",
    "exercise_type",
    "listing_date",
    "close",
    "volume",
    "date",
]

_OPTION_BASIC_SCHEMA = [
    "option_code",
    "option_name",
    "underlying_code",
    "underlying_name",
    "strike",
    "expiry_date",
    "option_type",
    "contract_unit",
    "exercise_type",
    "listing_date",
]

_OPTION_DAILY_SCHEMA = [
    "option_code",
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "amount",
    "pre_close",
    "implied_vol",
]

_GREEKS_SCHEMA = [
    "option_code",
    "option_name",
    "delta",
    "gamma",
    "theta",
    "vega",
    "implied_vol",
    "strike",
    "last_price",
    "theoretical_value",
    "date",
]

OPTION_SCHEMA = _OPTION_SCHEMA
OPTION_BASIC_SCHEMA = _OPTION_BASIC_SCHEMA
OPTION_DAILY_SCHEMA = _OPTION_DAILY_SCHEMA
GREEKS_SCHEMA = _GREEKS_SCHEMA


class RobustResult:
    """稳健结果类"""

    def __init__(
        self, success: bool = True, data=None, reason: str = "", source: str = "network"
    ):
        self.success = success
        self.data = data if data is not None else pd.DataFrame()
        self.reason = reason
        self.source = source

    def __bool__(self):
        return self.success


class OptionDBManager:
    """期权 DuckDB 管理器（延迟初始化）"""

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
            db_path = os.path.join(base_dir, "data", "option.db")

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
                    CREATE TABLE IF NOT EXISTS option (
                        option_code VARCHAR NOT NULL,
                        option_name VARCHAR,
                        underlying_code VARCHAR,
                        underlying VARCHAR,
                        underlying_name VARCHAR,
                        strike DOUBLE,
                        expiry_date DATE,
                        option_type VARCHAR,
                        contract_unit BIGINT,
                        exercise_type VARCHAR,
                        listing_date DATE,
                        close DOUBLE,
                        volume BIGINT,
                        date DATE NOT NULL,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (option_code, date)
                    )
                """)
                # 检查并添加缺失的列
                try:
                    conn.execute("SELECT underlying_code FROM option LIMIT 1")
                except Exception:
                    # underlying_code 列不存在，添加它
                    try:
                        conn.execute("ALTER TABLE option ADD COLUMN underlying_code VARCHAR")
                    except Exception:
                        pass
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS option_greeks (
                        option_code VARCHAR NOT NULL,
                        option_name VARCHAR,
                        delta DOUBLE,
                        gamma DOUBLE,
                        theta DOUBLE,
                        vega DOUBLE,
                        implied_vol DOUBLE,
                        strike DOUBLE,
                        last_price DOUBLE,
                        theoretical_value DOUBLE,
                        date DATE NOT NULL,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (option_code, date)
                    )
                """)
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_opt_code ON option(option_code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_opt_underlying_code ON option(underlying_code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_opt_underlying ON option(underlying)"
                )
                conn.execute("CREATE INDEX IF NOT EXISTS idx_opt_date ON option(date)")
                logger.info("期权表结构初始化完成")
        except Exception as e:
            logger.warning(f"初始化表结构失败: {e}")

    def insert_option(self, df: pd.DataFrame):
        if self._manager is None or df.empty:
            return

        df = df.copy()
        for col in _OPTION_SCHEMA:
            if col not in df.columns:
                df[col] = None

        if "update_time" not in df.columns:
            df["update_time"] = datetime.now()

        cols = _OPTION_SCHEMA + ["update_time"]
        df = df[cols]

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("INSERT OR REPLACE INTO option SELECT * FROM df")
                logger.info(f"插入/更新 {len(df)} 条期权信息")
        except Exception as e:
            logger.warning(f"插入期权信息失败: {e}")

    def insert_greeks(self, df: pd.DataFrame):
        if self._manager is None or df.empty:
            return

        df = df.copy()
        for col in _GREEKS_SCHEMA:
            if col not in df.columns:
                df[col] = None

        if "update_time" not in df.columns:
            df["update_time"] = datetime.now()

        cols = _GREEKS_SCHEMA + ["update_time"]
        df = df[cols]

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("INSERT OR REPLACE INTO option_greeks SELECT * FROM df")
                logger.info(f"插入/更新 {len(df)} 条希腊字母信息")
        except Exception as e:
            logger.warning(f"插入希腊字母信息失败: {e}")

    def get_option(self, option_code: str) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_OPTION_SCHEMA)

        try:
            with self._manager._get_connection(read_only=True) as conn:
                df = conn.execute(
                    "SELECT * FROM option WHERE option_code = ? ORDER BY date DESC",
                    [option_code],
                ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询期权信息失败: {e}")
            return pd.DataFrame(columns=_OPTION_SCHEMA)

    def get_greeks(self, option_code: str) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_GREEKS_SCHEMA)

        try:
            with self._manager._get_connection(read_only=True) as conn:
                df = conn.execute(
                    "SELECT * FROM option_greeks WHERE option_code = ? ORDER BY date DESC",
                    [option_code],
                ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询希腊字母失败: {e}")
            return pd.DataFrame(columns=_GREEKS_SCHEMA)

    def is_cache_valid(self, date_str: str, cache_days: int = 1) -> bool:
        if self._manager is None:
            return False

        try:
            with self._manager._get_connection(read_only=True) as conn:
                result = conn.execute(
                    "SELECT MAX(update_time) FROM option WHERE date = ?",
                    [date_str],
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
    manager = OptionDBManager()
    manager._ensure_initialized()
    return manager

_db_manager = None  # 延迟初始化，避免导入时副作用


def _parse_num(value) -> Optional[float]:
    if value is None or value == "" or value == "-":
        return None
    try:
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        return float(value)
    except (ValueError, TypeError):
        return None


def _parse_int(value) -> Optional[int]:
    if value is None or value == "" or value == "-":
        return None
    try:
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        return int(float(value))
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


def _load_pickle_cache(
    cache_file: str, max_age_hours: int = 24
) -> Optional[pd.DataFrame]:
    """加载 pickle 缓存"""
    if not os.path.exists(cache_file):
        return None
    try:
        file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if (datetime.now() - file_mtime).total_seconds() < max_age_hours * 3600:
            return pd.read_pickle(cache_file)
    except Exception:
        pass
    return None


def _save_pickle_cache(cache_file: str, df: pd.DataFrame):
    """保存 pickle 缓存"""
    try:
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        df.to_pickle(cache_file)
    except Exception as e:
        logger.warning(f"保存缓存失败: {e}")


def get_option_list(
    underlying: str = "sse",
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
    use_cache: bool = True,
) -> RobustResult:
    """
    获取期权列表。

    参数
    ----
    underlying  : 标的类型 ('sse' 上交所ETF期权, 'szse' 深交所ETF期权, 'cffex' 中金所股指期权)
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存
    use_cache   : 是否使用缓存

    返回
    ----
    RobustResult，data 包含期权列表信息
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    cache_file = os.path.join(cache_dir, f"option_list_{underlying}.pkl")

    if use_cache and not force_update:
        cached_df = _load_pickle_cache(cache_file, max_age_hours=24)
        if cached_df is not None and not cached_df.empty:
            return RobustResult(success=True, data=cached_df, source="cache")

    results = []

    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        if underlying == "sse":
            df = ak.option_current_day_sse()
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    record = _parse_sse_option_row(row, date_str)
                    if record:
                        results.append(record)
        elif underlying == "szse":
            df = ak.option_current_day_szse()
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    record = _parse_szse_option_row(row, date_str)
                    if record:
                        results.append(record)
        elif underlying == "cffex":
            df = ak.option_cffex_hs300_spot_sina()
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    call_record = _parse_cffex_option_row(row, date_str, "call")
                    put_record = _parse_cffex_option_row(row, date_str, "put")
                    if call_record:
                        results.append(call_record)
                    if put_record:
                        results.append(put_record)
        elif underlying == "all":
            for ex in ["sse", "szse", "cffex"]:
                result = get_option_list(
                    underlying=ex,
                    cache_dir=cache_dir,
                    force_update=force_update,
                    use_duckdb=False,
                    use_cache=False,
                )
                if result.success and not result.data.empty:
                    results.extend(result.data.to_dict("records"))
        else:
            return RobustResult(
                success=False,
                reason=f"不支持的标的类型: {underlying}，支持: sse, szse, cffex, all",
            )

        if results:
            result_df = pd.DataFrame(results)
            result_df = result_df.drop_duplicates(subset=["option_code"], keep="first")
            _save_pickle_cache(cache_file, result_df)
            if use_duckdb:
                db_manager = _get_db_manager()
                if db_manager is not None:
                    db_manager.insert_option(result_df)
            return RobustResult(success=True, data=result_df, source="network")

        return RobustResult(success=False, reason="未获取到期权数据")

    except Exception as e:
        logger.warning(f"[get_option_list] 获取期权列表失败: {e}")
        return RobustResult(success=False, reason=str(e))


def _parse_sse_option_row(row, date_str: str) -> Optional[dict]:
    """解析上交所期权数据行"""
    try:
        option_name = str(row.get("合约简称", ""))
        option_type = "看涨" if "购" in option_name else "看跌"

        underlying_str = str(row.get("标的券名称及代码", ""))
        underlying_code = ""
        underlying_name = ""
        if "(" in underlying_str and ")" in underlying_str:
            underlying_code = underlying_str.split("(")[-1].replace(")", "")
            underlying_name = underlying_str.split("(")[0].strip()

        return {
            "option_code": str(row.get("合约编码", "")),
            "option_name": option_name,
            "underlying_code": underlying_code,
            "underlying": underlying_code,
            "underlying_name": underlying_name,
            "strike": _parse_num(row.get("行权价", 0)),
            "expiry_date": _parse_date(row.get("到期日", None)),
            "option_type": option_type,
            "contract_unit": _parse_int(row.get("合约单位", 0)),
            "exercise_type": "欧式",
            "listing_date": None,
            "close": None,
            "volume": None,
            "date": date_str,
            "trade_code": str(row.get("合约交易代码", "")),
        }
    except Exception:
        return None


def _parse_szse_option_row(row, date_str: str) -> Optional[dict]:
    """解析深交所期权数据行"""
    try:
        option_name = str(row.get("合约简称", ""))
        option_type = "看涨" if "购" in option_name else "看跌"

        underlying_str = str(row.get("标的证券简称(代码)", ""))
        underlying_code = ""
        underlying_name = ""
        if "(" in underlying_str and ")" in underlying_str:
            underlying_code = underlying_str.split("(")[-1].replace(")", "")
            underlying_name = underlying_str.split("(")[0].strip()

        return {
            "option_code": str(row.get("合约编码", "")),
            "option_name": option_name,
            "underlying_code": underlying_code,
            "underlying": underlying_code,
            "underlying_name": underlying_name,
            "strike": _parse_num(row.get("行权价", 0)),
            "expiry_date": _parse_date(row.get("到期日", None)),
            "option_type": option_type,
            "contract_unit": _parse_int(row.get("合约单位", 0)),
            "exercise_type": "欧式",
            "listing_date": None,
            "close": _parse_num(row.get("前结算价", 0)),
            "volume": _parse_int(row.get("合约总持仓", 0)),
            "date": date_str,
            "trade_code": str(row.get("合约代码", "")),
        }
    except Exception:
        return None


def _parse_cffex_option_row(row, date_str: str, opt_type: str) -> Optional[dict]:
    """解析中金所期权数据行"""
    try:
        prefix = "看涨合约" if opt_type == "call" else "看跌合约"

        option_id = str(row.get(f"{prefix}-标识", ""))
        if not option_id or option_id == "0":
            return None

        option_name = option_id
        option_type = "看涨" if opt_type == "call" else "看跌"

        return {
            "option_code": option_id,
            "option_name": option_name,
            "underlying_code": "IF",
            "underlying": "IF",
            "underlying_name": "沪深300股指",
            "strike": _parse_num(row.get("行权价", 0)),
            "expiry_date": None,
            "option_type": option_type,
            "contract_unit": None,
            "exercise_type": "欧式",
            "listing_date": None,
            "close": _parse_num(row.get(f"{prefix}-最新价", 0)),
            "volume": _parse_int(row.get(f"{prefix}-持仓量", 0)),
            "date": date_str,
        }
    except Exception:
        return None


def get_option_price(
    option_code: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_cache: bool = True,
) -> RobustResult:
    """
    获取期权实时行情。

    参数
    ----
    option_code : 期权代码
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_cache   : 是否使用缓存

    返回
    ----
    RobustResult，data 包含期权行情信息
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    cache_file = os.path.join(cache_dir, f"option_price_{option_code}.pkl")

    if use_cache and not force_update:
        cached_df = _load_pickle_cache(cache_file, max_age_hours=1)
        if cached_df is not None and not cached_df.empty:
            return RobustResult(success=True, data=cached_df, source="cache")

    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df_list = ak.option_current_day_sse()
        if df_list is not None and not df_list.empty:
            df_filtered = df_list[df_list["合约编码"].astype(str) == str(option_code)]
            if not df_filtered.empty:
                row = df_filtered.iloc[0]
                result = {
                    "option_code": str(option_code),
                    "option_name": str(row.get("合约简称", "")),
                    "trade_code": str(row.get("合约交易代码", "")),
                    "underlying": str(row.get("标的券名称及代码", "")),
                    "option_type": "看涨"
                    if "购" in str(row.get("合约简称", ""))
                    else "看跌",
                    "strike": _parse_num(row.get("行权价", 0)),
                    "contract_unit": _parse_int(row.get("合约单位", 0)),
                    "expiry_date": _parse_date(row.get("到期日", None)),
                    "date": date_str,
                }
                result_df = pd.DataFrame([result])
                _save_pickle_cache(cache_file, result_df)
                return RobustResult(success=True, data=result_df, source="network")

        df_szse = ak.option_current_day_szse()
        if df_szse is not None and not df_szse.empty:
            df_filtered = df_szse[df_szse["合约编码"].astype(str) == str(option_code)]
            if not df_filtered.empty:
                row = df_filtered.iloc[0]
                result = {
                    "option_code": str(option_code),
                    "option_name": str(row.get("合约简称", "")),
                    "trade_code": str(row.get("合约代码", "")),
                    "underlying": str(row.get("标的证券简称(代码)", "")),
                    "option_type": "看涨"
                    if "购" in str(row.get("合约简称", ""))
                    else "看跌",
                    "strike": _parse_num(row.get("行权价", 0)),
                    "contract_unit": _parse_int(row.get("合约单位", 0)),
                    "expiry_date": _parse_date(row.get("到期日", None)),
                    "date": date_str,
                }
                result_df = pd.DataFrame([result])
                _save_pickle_cache(cache_file, result_df)
                return RobustResult(success=True, data=result_df, source="network")

        return RobustResult(success=False, reason=f"未找到期权代码: {option_code}")

    except Exception as e:
        logger.warning(f"[get_option_price] 获取期权行情失败: {e}")
        return RobustResult(success=False, reason=str(e))


def get_option_greeks(
    option_code: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_cache: bool = True,
) -> RobustResult:
    """
    获取期权希腊字母。

    参数
    ----
    option_code : 期权代码
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_cache   : 是否使用缓存

    返回
    ----
    RobustResult，data 包含希腊字母信息 (Delta, Gamma, Theta, Vega, 隐含波动率)
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    cache_file = os.path.join(cache_dir, f"option_greeks_{option_code}.pkl")

    if use_cache and not force_update:
        cached_df = _load_pickle_cache(cache_file, max_age_hours=24)
        if cached_df is not None and not cached_df.empty:
            return RobustResult(success=True, data=cached_df, source="cache")

    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.option_sse_greeks_sina(symbol=str(option_code))
        if df is not None and not df.empty:
            greeks_dict = dict(zip(df["字段"], df["值"]))

            result = {
                "option_code": str(option_code),
                "option_name": str(greeks_dict.get("期权合约简称", "")),
                "delta": _parse_num(greeks_dict.get("Delta")),
                "gamma": _parse_num(greeks_dict.get("Gamma")),
                "theta": _parse_num(greeks_dict.get("Theta")),
                "vega": _parse_num(greeks_dict.get("Vega")),
                "implied_vol": _parse_num(greeks_dict.get("隐含波动率")),
                "strike": _parse_num(greeks_dict.get("行权价")),
                "last_price": _parse_num(greeks_dict.get("最新价")),
                "theoretical_value": _parse_num(greeks_dict.get("理论价值")),
                "volume": _parse_int(greeks_dict.get("成交量")),
                "date": date_str,
            }

            result_df = pd.DataFrame([result])
            _save_pickle_cache(cache_file, result_df)

            db_manager = _get_db_manager()
            if db_manager is not None:
                db_manager.insert_greeks(result_df)

            return RobustResult(success=True, data=result_df, source="network")

        return RobustResult(
            success=False, reason=f"未获取到期权 {option_code} 的希腊字母数据"
        )

    except Exception as e:
        logger.warning(f"[get_option_greeks] 获取希腊字母失败: {e}")
        return RobustResult(success=False, reason=str(e))


def get_option_info(
    option_code: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_cache: bool = True,
) -> RobustResult:
    """
    获取期权合约详情。

    参数
    ----
    option_code : 期权代码
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_cache   : 是否使用缓存

    返回
    ----
    RobustResult，data 包含期权合约详细信息
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    cache_file = os.path.join(cache_dir, f"option_info_{option_code}.pkl")

    if use_cache and not force_update:
        cached_df = _load_pickle_cache(cache_file, max_age_hours=24)
        if cached_df is not None and not cached_df.empty:
            return RobustResult(success=True, data=cached_df, source="cache")

    try:
        list_result = get_option_list(
            underlying="all", cache_dir=cache_dir, force_update=False, use_cache=True
        )
        if list_result.success and not list_result.data.empty:
            df = list_result.data
            df_filtered = df[df["option_code"].astype(str) == str(option_code)]
            if not df_filtered.empty:
                row = df_filtered.iloc[0]
                result = {
                    "option_code": str(option_code),
                    "option_name": row.get("option_name", ""),
                    "underlying": row.get("underlying", ""),
                    "strike": row.get("strike"),
                    "expiry_date": row.get("expiry_date"),
                    "option_type": row.get("option_type", ""),
                    "trade_code": row.get("trade_code", ""),
                    "contract_unit": row.get("contract_unit"),
                    "date": date_str,
                }
                result_df = pd.DataFrame([result])
                _save_pickle_cache(cache_file, result_df)
                return RobustResult(success=True, data=result_df, source="network")

        return RobustResult(success=False, reason=f"未找到期权代码: {option_code}")

    except Exception as e:
        logger.warning(f"[get_option_info] 获取期权详情失败: {e}")
        return RobustResult(success=False, reason=str(e))


def get_option_daily(
    option_code: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_cache: bool = True,
) -> RobustResult:
    """
    获取期权日线数据。

    参数
    ----
    option_code : 期权代码
    start_date  : 起始日期 'YYYY-MM-DD'
    end_date    : 结束日期 'YYYY-MM-DD'
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_cache   : 是否使用缓存

    返回
    ----
    RobustResult，data 包含 OHLCV、隐含波动率等日线数据
    """
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    cache_file = os.path.join(cache_dir, f"option_daily_{option_code}.pkl")

    if use_cache and not force_update:
        cached_df = _load_pickle_cache(cache_file, max_age_hours=24)
        if cached_df is not None and not cached_df.empty:
            if "date" in cached_df.columns or "日期" in cached_df.columns:
                return RobustResult(success=True, data=cached_df, source="cache")

    try:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        df = ak.option_sse_daily_sina(symbol=str(option_code))

        if df is not None and not df.empty:
            df = df.copy()
            df.columns = ["date", "open", "high", "low", "close", "volume"]

            df["date"] = pd.to_datetime(df["date"])
            df["option_code"] = str(option_code)

            for col in ["open", "high", "low", "close", "volume"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            df = df[(df["date"] >= start_dt) & (df["date"] <= end_dt)]

            df = df.sort_values("date").reset_index(drop=True)

            _save_pickle_cache(cache_file, df)

            db_manager = _get_db_manager()
            if db_manager is not None:
                insert_df = df.copy()
                insert_df["option_name"] = ""
                insert_df["underlying"] = ""
                insert_df["strike"] = None
                insert_df["expiry_date"] = None
                insert_df["option_type"] = ""
                db_manager.insert_option(insert_df)

            return RobustResult(success=True, data=df, source="network")

        return RobustResult(
            success=False, reason=f"未获取到期权 {option_code} 的日线数据"
        )

    except Exception as e:
        logger.warning(f"[get_option_daily] 获取期权日线失败: {e}")
        return RobustResult(success=False, reason=str(e))


def calculate_option_implied_vol(
    option_code: str,
    price: float,
    underlying_price: float = None,
    risk_free_rate: float = 0.03,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> dict:
    """
    计算期权隐含波动率（使用 Black-Scholes 模型）。

    参数
    ----
    option_code    : 期权代码
    price          : 期权当前价格
    underlying_price: 标的资产价格（可选，自动获取）
    risk_free_rate : 无风险利率（默认3%）
    cache_dir      : 缓存目录
    force_update   : 强制更新

    返回
    ----
    dict，包含 implied_vol、delta、gamma、theta、vega
    """
    import math

    def norm_cdf(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

    def norm_pdf(x):
        return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)

    def black_scholes_greeks(S, K, T, r, sigma, option_type="call"):
        if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
            return None

        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        if option_type == "call":
            delta = norm_cdf(d1)
            theta = (
                -S * norm_pdf(d1) * sigma / (2 * math.sqrt(T))
                - r * K * math.exp(-r * T) * norm_cdf(d2)
            ) / 365
        else:
            delta = norm_cdf(d1) - 1
            theta = (
                -S * norm_pdf(d1) * sigma / (2 * math.sqrt(T))
                + r * K * math.exp(-r * T) * norm_cdf(-d2)
            ) / 365

        gamma = norm_pdf(d1) / (S * sigma * math.sqrt(T))
        vega = S * norm_pdf(d1) * math.sqrt(T) / 100

        return {"delta": delta, "gamma": gamma, "theta": theta, "vega": vega}

    def implied_volatility(price, S, K, T, r, option_type="call", max_iter=100):
        if T <= 0 or S <= 0 or K <= 0 or price <= 0:
            return None

        sigma = 0.3
        for _ in range(max_iter):
            d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
            d2 = d1 - sigma * math.sqrt(T)

            if option_type == "call":
                model_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
            else:
                model_price = K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

            diff = model_price - price
            if abs(diff) < 0.0001:
                return sigma

            vega = S * norm_pdf(d1) * math.sqrt(T)
            if vega == 0:
                break
            sigma = sigma - diff / vega

            if sigma <= 0:
                sigma = 0.01

        return sigma

    try:
        info_result = get_option_info(
            option_code, cache_dir=cache_dir, force_update=force_update
        )
        if not info_result.success or info_result.data.empty:
            return {"success": False, "reason": "无法获取期权信息", "implied_vol": None}

        info = info_result.data.iloc[0]
        strike = info.get("strike")
        expiry_date = info.get("expiry_date")
        option_type_str = info.get("option_type", "")
        option_type = (
            "call" if "购" in option_type_str or "看涨" in option_type_str else "put"
        )

        if strike is None:
            return {"success": False, "reason": "无法获取行权价", "implied_vol": None}

        if expiry_date is None:
            return {"success": False, "reason": "无法获取到期日", "implied_vol": None}

        expiry_dt = pd.to_datetime(expiry_date)
        T = (expiry_dt - datetime.now()).days / 365.0
        if T <= 0:
            return {"success": False, "reason": "期权已到期", "implied_vol": None}

        if underlying_price is None:
            greeks_result = get_option_greeks(
                option_code, cache_dir=cache_dir, force_update=force_update
            )
            if greeks_result.success and not greeks_result.data.empty:
                greeks_row = greeks_result.data.iloc[0]
                existing_iv = greeks_row.get("implied_vol")
                if existing_iv is not None and existing_iv > 0:
                    iv = existing_iv
                else:
                    iv = implied_volatility(
                        price,
                        underlying_price or strike,
                        strike,
                        T,
                        risk_free_rate,
                        option_type,
                    )
            else:
                iv = implied_volatility(
                    price,
                    underlying_price or strike,
                    strike,
                    T,
                    risk_free_rate,
                    option_type,
                )
        else:
            iv = implied_volatility(
                price, underlying_price, strike, T, risk_free_rate, option_type
            )

        if iv is None:
            return {
                "success": False,
                "reason": "无法计算隐含波动率",
                "implied_vol": None,
            }

        S = underlying_price or strike
        greeks = black_scholes_greeks(S, strike, T, risk_free_rate, iv, option_type)

        result = {
            "success": True,
            "option_code": option_code,
            "price": price,
            "strike": strike,
            "underlying_price": S,
            "time_to_expiry": round(T, 4),
            "implied_vol": round(iv, 4),
            "risk_free_rate": risk_free_rate,
        }

        if greeks:
            result["delta"] = round(greeks["delta"], 4)
            result["gamma"] = round(greeks["gamma"], 4)
            result["theta"] = round(greeks["theta"], 4)
            result["vega"] = round(greeks["vega"], 4)

        return result

    except Exception as e:
        logger.warning(f"[calculate_option_implied_vol] 计算隐含波动率失败: {e}")
        return {"success": False, "reason": str(e), "implied_vol": None}


def get_option_chain(
    underlying: str,
    expiry_date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> RobustResult:
    """
    获取期权链数据。

    参数
    ----
    underlying  : 标的代码 (如 '510050', '159915')
    expiry_date : 到期日筛选 (可选)
    cache_dir   : 缓存目录
    force_update: 强制更新

    返回
    ----
    RobustResult，data 包含期权链数据
    """
    result = get_option_list(
        underlying="sse",
        cache_dir=cache_dir,
        force_update=force_update,
        use_cache=not force_update,
    )

    if not result.success:
        return result

    df = result.data

    filter_col = "underlying_code" if "underlying_code" in df.columns else "underlying"
    if filter_col in df.columns:
        df = df[df[filter_col].str.contains(underlying, na=False)]

    if expiry_date and "expiry_date" in df.columns:
        df = df[df["expiry_date"] == expiry_date]

    return RobustResult(success=True, data=df)


def get_option(
    option_code: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取单只期权信息（兼容旧接口）。

    参数
    ----
    option_code : 期权代码
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，单只期权信息
    """
    result = get_option_price(
        option_code, cache_dir=cache_dir, force_update=force_update
    )
    return result.data if result.success else pd.DataFrame(columns=_OPTION_SCHEMA)


def query_option(
    option_codes: List[str],
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    批量查询期权（finance.STK_OPTION_DAILY）。
    """
    if option_codes is None or len(option_codes) == 0:
        return pd.DataFrame(columns=_OPTION_SCHEMA)

    dfs = []
    for code in option_codes:
        df = get_option(code, cache_dir=cache_dir, force_update=force_update)
        if not df.empty:
            dfs.append(df)

    if not dfs:
        return pd.DataFrame(columns=_OPTION_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


class FinanceQuery:
    """聚宽 finance 模块模拟器"""

    class STK_OPTION_DAILY:
        option_code = None
        option_name = None
        underlying_code = None
        underlying = None
        strike = None
        expiry_date = None
        option_type = None
        close = None
        volume = None
        date = None

    class STK_OPTION_BASIC:
        option_code = None
        option_name = None
        underlying_code = None
        underlying_name = None
        strike = None
        expiry_date = None
        option_type = None
        contract_unit = None
        exercise_type = None
        listing_date = None

    class OPTION_CONTRACTS:
        option_code = None
        option_name = None
        underlying_code = None
        underlying_name = None
        strike = None
        expiry_date = None
        option_type = None
        contract_unit = None
        exercise_type = None
        listing_date = None
        call_code = None
        put_code = None

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
                conditions["option_code"] = query_obj.right

        if table_name == "STK_OPTION_DAILY":
            if "option_code" in conditions:
                return get_option(
                    conditions["option_code"],
                    cache_dir=cache_dir,
                    use_duckdb=use_duckdb,
                )
            result = get_option_list(cache_dir=cache_dir, use_duckdb=use_duckdb)
            if result.success and not result.data.empty:
                return result.data
            return pd.DataFrame(columns=_OPTION_DAILY_SCHEMA)
        elif table_name == "STK_OPTION_BASIC":
            result = get_option_list(
                cache_dir=cache_dir, force_update=force_update, use_duckdb=use_duckdb
            )
            if result.success and not result.data.empty:
                basic_df = result.data.copy()
                for col in _OPTION_BASIC_SCHEMA:
                    if col not in basic_df.columns:
                        if col == "underlying_code":
                            basic_df[col] = basic_df.get("underlying", "")
                        elif col == "underlying_name":
                            basic_df[col] = basic_df.get("option_name", "").apply(
                                lambda x: str(x).split("-")[0] if "-" in str(x) else ""
                            )
                        elif col == "exercise_type":
                            basic_df[col] = "欧式"
                        elif col == "listing_date":
                            basic_df[col] = None
                return basic_df
            return pd.DataFrame(columns=_OPTION_BASIC_SCHEMA)
        elif table_name == "OPTION_CONTRACTS":
            if "option_code" in conditions:
                info_result = get_option_info(
                    conditions["option_code"],
                    cache_dir=cache_dir,
                    force_update=force_update,
                )
                if info_result.success and not info_result.data.empty:
                    return info_result.data
                return pd.DataFrame(columns=_OPTION_BASIC_SCHEMA)
            result = get_option_list(
                cache_dir=cache_dir, force_update=force_update, use_duckdb=use_duckdb
            )
            if result.success and not result.data.empty:
                contracts_df = result.data.copy()
                for col in _OPTION_BASIC_SCHEMA:
                    if col not in contracts_df.columns:
                        if col == "underlying_code":
                            contracts_df[col] = contracts_df.get("underlying", "")
                        elif col == "underlying_name":
                            contracts_df[col] = contracts_df.get(
                                "option_name", ""
                            ).apply(
                                lambda x: str(x).split("-")[0] if "-" in str(x) else ""
                            )
                        elif col == "exercise_type":
                            contracts_df[col] = "欧式"
                        elif col == "listing_date":
                            contracts_df[col] = None
                return contracts_df
            return pd.DataFrame(
                columns=[
                    "option_code",
                    "option_name",
                    "underlying_code",
                    "strike",
                    "expiry_date",
                    "option_type",
                    "call_code",
                    "put_code",
                ]
            )
        else:
            raise ValueError(f"不支持的表: {table_name}")


finance = FinanceQuery()


def get_option_quote(
    option_code: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """获取期权行情数据（兼容旧接口）"""
    return get_option(option_code, cache_dir=cache_dir, force_update=force_update)


def run_query_simple(
    table: str,
    option_code: str = None,
    underlying_code: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """简化的查询接口"""
    if table == "STK_OPTION_DAILY":
        if option_code:
            return get_option(
                option_code, cache_dir=cache_dir, force_update=force_update
            )
        result = get_option_list(cache_dir=cache_dir, force_update=force_update)
        if result.success and not result.data.empty:
            df = result.data
            if underlying_code:
                filter_col = (
                    "underlying_code"
                    if "underlying_code" in df.columns
                    else "underlying"
                )
                if filter_col in df.columns:
                    df = df[df[filter_col].str.contains(underlying_code, na=False)]
            return df
        return pd.DataFrame(columns=_OPTION_DAILY_SCHEMA)
    elif table == "STK_OPTION_BASIC":
        result = get_option_list(cache_dir=cache_dir, force_update=force_update)
        if result.success and not result.data.empty:
            basic_df = result.data.copy()
            for col in _OPTION_BASIC_SCHEMA:
                if col not in basic_df.columns:
                    if col == "underlying_code":
                        basic_df[col] = basic_df.get("underlying", "")
                    elif col == "underlying_name":
                        basic_df[col] = basic_df.get("option_name", "").apply(
                            lambda x: str(x).split("-")[0] if "-" in str(x) else ""
                        )
                    elif col == "exercise_type":
                        basic_df[col] = "欧式"
                    elif col == "listing_date":
                        basic_df[col] = None
            if underlying_code:
                filter_col = (
                    "underlying_code"
                    if "underlying_code" in basic_df.columns
                    else "underlying"
                )
                if filter_col in basic_df.columns:
                    basic_df = basic_df[
                        basic_df[filter_col].str.contains(underlying_code, na=False)
                    ]
            return basic_df
        return pd.DataFrame(columns=_OPTION_BASIC_SCHEMA)
    else:
        raise ValueError(f"不支持的表: {table}")
