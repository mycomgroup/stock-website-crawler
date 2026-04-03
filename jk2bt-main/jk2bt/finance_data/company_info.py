"""
finance_data/company_info.py
上市公司基本信息与状态变动数据获取模块。

支持:
- get_company_info(code): 获取公司基本信息
- get_company_info_robust(code): 稳健版获取公司基本信息（返回 RobustResult）
- get_security_status(code, date): 获取指定日期的证券状态
- finance.STK_COMPANY_BASIC_INFO: 公司基本信息表查询
- finance.STK_STATUS_CHANGE: 公司状态变动查询（停牌、复牌、退市等）

数据字段:
- 公司代码、公司名称、成立日期、上市日期
- 主营业务、所属行业、注册地址
- 公司状态（正常、停牌、退市等）
- 状态变动日期、变动类型

缓存策略:
- DuckDB 缓存（优先）：存储在 data/market.db 的 company_info 表中
- Pickle 缓存（备用）：存储在 finance_cache 目录
- 静态数据缓存有效期：90天（按季度缓存）

稳健性:
- 支持 RobustResult 封装，明确返回成功/失败状态和原因
- 空结果返回带 schema 的 DataFrame
- 支持批量查询
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Union
import logging
import time

logger = logging.getLogger(__name__)

CACHE_EXPIRE_DAYS = 90
_MAX_RETRY_ATTEMPTS = 3
_RETRY_DELAY_SECONDS = 1


def _retry_akshare_call(func, *args, max_attempts=_MAX_RETRY_ATTEMPTS, **kwargs):
    """
    AkShare 接口重试机制

    参数
    ----
    func : callable - AkShare 函数
    max_attempts : int - 最大重试次数
    *args, **kwargs - 函数参数

    返回
    ----
    DataFrame 或 None
    """
    last_error = None
    for attempt in range(max_attempts):
        try:
            result = func(*args, **kwargs)
            if result is not None and not result.empty:
                return result
        except Exception as e:
            last_error = e
            if attempt < max_attempts - 1:
                logger.warning(
                    f"[retry] {func.__name__} 第 {attempt + 1} 次失败: {e}, "
                    f"等待 {_RETRY_DELAY_SECONDS}s 后重试"
                )
                time.sleep(_RETRY_DELAY_SECONDS)
            else:
                logger.error(
                    f"[retry] {func.__name__} 重试 {max_attempts} 次后仍失败: {e}"
                )
    return None


class RobustResult:
    """
    稳健结果封装类，用于统一处理API返回结果。

    属性:
        success: bool - 是否成功获取数据
        data: Any - 返回的数据（DataFrame等）
        reason: str - 失败原因或成功说明
        source: str - 数据来源（'cache'/'network'/'fallback'）

    用法:
        result = get_company_info_robust('600519.XSHG')
        if result.success:
            df = result.data
        else:
            log.warn(f"获取失败: {result.reason}")
    """

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


_DUCKDB_AVAILABLE = False
_DUCKDB_ERROR_MSG = ""
try:
    from ..db.duckdb_manager import DuckDBManager

    _DUCKDB_AVAILABLE = True
except ImportError as e:
    _DUCKDB_ERROR_MSG = str(e)
    try:
        from jk2bt.db.duckdb_manager import DuckDBManager

        _DUCKDB_AVAILABLE = True
    except ImportError as e2:
        _DUCKDB_ERROR_MSG = str(e2)
        logger.warning(
            f"DuckDB 模块不可用（{e2}），将使用 pickle 缓存。"
            "安装 DuckDB 可提升性能: pip install duckdb"
        )


_COMPANY_BASIC_INFO_SCHEMA = [
    "code",
    "company_name",
    "establish_date",
    "list_date",
    "main_business",
    "industry",
    "registered_address",
    "company_status",
    "status_change_date",
    "change_type",
]

_STATUS_CHANGE_SCHEMA = [
    "code",
    "status_date",
    "status_type",
    "reason",
]


class CompanyInfoDBManager:
    """公司信息 DuckDB 管理器"""

    _instance = None
    _lock = None

    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._lock = cls._instance._init_manager(db_path)
        return cls._instance

    def _init_manager(self, db_path: str = None):
        if not _DUCKDB_AVAILABLE:
            logger.info(
                "DuckDB 不可用，使用 pickle 缓存（性能较低）。"
                f"原因: {_DUCKDB_ERROR_MSG}"
            )
            return None

        if db_path is None:
            base_dir = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            db_path = os.path.join(base_dir, "data", "company_info.db")

        self.db_path = db_path
        self._manager = None

        try:
            self._manager = DuckDBManager(db_path=db_path, read_only=False)
            self._init_tables()
            logger.info(f"DuckDB 初始化成功: {db_path}")
        except Exception as e:
            logger.warning(
                f"DuckDB 初始化失败: {e}, 将使用 pickle 缓存。检查路径权限: {db_path}"
            )
            self._manager = None

        return self._manager

    def _init_tables(self):
        if self._manager is None:
            return

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS company_info (
                        code VARCHAR NOT NULL,
                        company_name VARCHAR,
                        establish_date DATE,
                        list_date DATE,
                        main_business VARCHAR,
                        industry VARCHAR,
                        registered_address VARCHAR,
                        company_status VARCHAR,
                        status_change_date DATE,
                        change_type VARCHAR,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (code)
                    )
                """)

                conn.execute("""
                    CREATE TABLE IF NOT EXISTS status_change (
                        code VARCHAR NOT NULL,
                        status_date DATE NOT NULL,
                        status_type VARCHAR,
                        reason VARCHAR,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (code, status_date)
                    )
                """)

                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_company_code ON company_info(code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_status_code ON status_change(code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_status_date ON status_change(status_date)"
                )

                logger.info("公司信息表结构初始化完成")
        except Exception as e:
            logger.warning(f"初始化表结构失败: {e}")

    def get_manager(self):
        return self._manager

    def insert_company_info(self, df: pd.DataFrame):
        if self._manager is None or df.empty:
            return

        df = df.copy()

        # 确保所有必需字段都存在，缺失的用None填充
        for col in _COMPANY_BASIC_INFO_SCHEMA:
            if col not in df.columns:
                df[col] = None

        if "update_time" not in df.columns:
            df["update_time"] = datetime.now()

        # 按照表结构顺序选择列
        cols = _COMPANY_BASIC_INFO_SCHEMA + ["update_time"]
        df = df[cols]

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO company_info 
                    (code, company_name, establish_date, list_date, main_business, 
                     industry, registered_address, company_status, status_change_date, 
                     change_type, update_time)
                    SELECT * FROM df
                """)
                logger.info(f"插入/更新 {len(df)} 条公司信息")
        except Exception as e:
            logger.warning(f"插入公司信息失败: {e}")

    def get_company_info(self, code: str) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

        try:
            with self._manager._get_connection(read_only=True) as conn:
                df = conn.execute(
                    "SELECT * FROM company_info WHERE code = ?", [code]
                ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询公司信息失败: {e}")
            return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

    def insert_status_change(self, df: pd.DataFrame):
        if self._manager is None or df.empty:
            return

        df = df.copy()
        if "update_time" not in df.columns:
            df["update_time"] = datetime.now()

        cols = [c for c in _STATUS_CHANGE_SCHEMA if c in df.columns] + ["update_time"]
        df = df[cols]

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO status_change
                    SELECT * FROM df
                """)
                logger.info(f"插入/更新 {len(df)} 条状态变动")
        except Exception as e:
            logger.warning(f"插入状态变动失败: {e}")

    def get_status_change(
        self, code: str, start_date: str = None, end_date: str = None
    ) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)

        try:
            with self._manager._get_connection(read_only=True) as conn:
                if start_date and end_date:
                    df = conn.execute(
                        "SELECT * FROM status_change WHERE code = ? AND status_date >= ? AND status_date <= ? ORDER BY status_date",
                        [code, start_date, end_date],
                    ).fetchdf()
                else:
                    df = conn.execute(
                        "SELECT * FROM status_change WHERE code = ? ORDER BY status_date",
                        [code],
                    ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询状态变动失败: {e}")
            return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)


_db_manager = CompanyInfoDBManager() if _DUCKDB_AVAILABLE else None


def get_company_info(
    symbol, cache_dir="finance_cache", force_update=False, use_duckdb=True
) -> pd.DataFrame:
    """
    获取上市公司基本信息。

    参数
    ----
    symbol     : 股票代码，支持 '600519.XSHG', '000001.XSHE', 'sh600519', 'sz000001', '600519' 等格式
    cache_dir  : pickle 缓存目录（备用）
    force_update: True 时强制重新下载
    use_duckdb : 是否使用 DuckDB 缓存（优先）

    返回
    ----
    pandas DataFrame，标准化字段：
    - code: 股票代码（聚宽格式）
    - company_name: 公司名称
    - establish_date: 成立日期
    - list_date: 上市日期
    - main_business: 主营业务
    - industry: 所属行业
    - registered_address: 注册地址
    - company_status: 公司状态（正常、停牌、退市等）
    """
    code_num = _extract_code_num(symbol)
    jq_code = _normalize_to_jq(symbol)

    if use_duckdb and _db_manager is not None and not force_update:
        df_cached = _db_manager.get_company_info(jq_code)
        if not df_cached.empty:
            return df_cached[_COMPANY_BASIC_INFO_SCHEMA]

    cache_file = os.path.join(cache_dir, f"company_info_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < CACHE_EXPIRE_DAYS:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_company_info(cached_df)
                return cached_df
            need_download = True
        except Exception:
            need_download = True

    if need_download:
        try:
            df_profile = _fetch_company_profile(code_num)
            df_industry = _fetch_company_industry(code_num)

            result = _merge_and_normalize(df_profile, df_industry, jq_code)

            if not result.empty:
                result.to_pickle(cache_file)
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_company_info(result)
                return result
            else:
                return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

        except Exception as e:
            print(f"[company_info] 获取公司信息失败 {symbol}: {e}")
            return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

    return (
        cached_df
        if not cached_df.empty
        else pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)
    )


def get_security_status(
    symbol, date=None, cache_dir="finance_cache", force_update=False, use_duckdb=True
) -> pd.DataFrame:
    """
    获取指定日期的证券状态（停牌、复牌、退市等）。

    参数
    ----
    symbol     : 股票代码
    date       : 查询日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'，默认最近交易日
    cache_dir  : pickle 缓存目录（备用）
    force_update: True 时强制重新下载
    use_duckdb : 是否使用 DuckDB 缓存（优先）

    返回
    ----
    pandas DataFrame，标准化字段：
    - code: 股票代码（聚宽格式）
    - status_date: 状态日期
    - status_type: 状态类型（正常交易、停牌、复牌、退市等）
    - reason: 状态变动原因
    """
    code_num = _extract_code_num(symbol)
    jq_code = _normalize_to_jq(symbol)

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    date_str = _normalize_date(date)

    if use_duckdb and _db_manager is not None and not force_update:
        df_cached = _db_manager.get_status_change(jq_code, date_str, date_str)
        if not df_cached.empty:
            return df_cached[_STATUS_CHANGE_SCHEMA]

    cache_file = os.path.join(cache_dir, f"suspension_{date_str.replace('-', '')}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            result = _filter_status_for_symbol(cached_df, code_num, jq_code)
            if use_duckdb and _db_manager is not None and not result.empty:
                _db_manager.insert_status_change(result)
            return result
        except Exception:
            need_download = True

    if need_download:
        try:
            df_all = _fetch_suspension_data(date_str)
            if df_all is not None and not df_all.empty:
                df_all.to_pickle(cache_file)
                result = _filter_status_for_symbol(df_all, code_num, jq_code)
                if use_duckdb and _db_manager is not None and not result.empty:
                    _db_manager.insert_status_change(result)
                return result
        except Exception as e:
            print(f"[security_status] 获取状态失败 {symbol}: {e}")

    return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)


def _fetch_company_profile(code_num: str) -> Optional[pd.DataFrame]:
    """从 AkShare 获取公司基本信息（带重试机制）"""
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")
    try:
        df = _retry_akshare_call(ak.stock_individual_info_em, symbol=code_num)
        return df
    except Exception as e:
        logger.error(f"[company_profile] 获取失败 {code_num}: {e}")
        return None


def _fetch_company_industry(code_num: str) -> Optional[pd.DataFrame]:
    """从 AkShare 获取公司行业信息（带重试机制）"""
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")
    try:
        df = _retry_akshare_call(ak.stock_board_industry_name_em, symbol=code_num)
        return df
    except Exception as e:
        logger.warning(f"[company_industry] 获取失败 {code_num}: {e}")
        return None


def _merge_and_normalize(df_profile, df_industry, jq_code: str) -> pd.DataFrame:
    """合并并标准化数据"""
    result = pd.DataFrame()
    result["code"] = [jq_code]

    result["company_name"] = [None]
    result["establish_date"] = [None]
    result["list_date"] = [None]
    result["main_business"] = [None]
    result["registered_address"] = [None]

    if df_profile is not None and not df_profile.empty:
        profile_dict = _parse_profile_df(df_profile)
        result["company_name"] = [profile_dict.get("公司名称", None)]
        result["establish_date"] = [profile_dict.get("成立日期", None)]
        result["list_date"] = [profile_dict.get("上市时间", None)]
        result["main_business"] = [profile_dict.get("主营业务", None)]
        result["registered_address"] = [profile_dict.get("注册地址", None)]

    if df_industry is not None and not df_industry.empty:
        if "行业板块" in df_industry.columns:
            result["industry"] = [df_industry.iloc[0]["行业板块"]]
        elif "板块名称" in df_industry.columns:
            result["industry"] = [df_industry.iloc[0]["板块名称"]]
        else:
            result["industry"] = [None]
    else:
        result["industry"] = [None]

    result["company_status"] = ["正常交易"]
    result["status_change_date"] = [None]
    result["change_type"] = [None]

    return result


def _parse_profile_df(df: pd.DataFrame) -> dict:
    """解析 profile DataFrame 为字典"""
    result = {}
    if "item" in df.columns and "value" in df.columns:
        for _, row in df.iterrows():
            item = str(row.get("item", ""))
            value = row.get("value", "")
            result[item] = value
    return result


def _fetch_suspension_data(date_str: str) -> Optional[pd.DataFrame]:
    """获取停牌数据（带重试机制）"""
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")
    try:
        date_num = date_str.replace("-", "")
        df = _retry_akshare_call(ak.stock_tfp_em, date=date_num)
        return df
    except Exception as e:
        logger.error(f"[suspension] 获取停牌数据失败 {date_str}: {e}")
        return None


def _filter_status_for_symbol(
    df_all: pd.DataFrame, code_num: str, jq_code: str
) -> pd.DataFrame:
    """筛选指定股票的状态"""
    code_col = "代码" if "代码" in df_all.columns else "股票代码"

    df_filtered = df_all[df_all[code_col].astype(str).str.zfill(6) == code_num]

    if df_filtered.empty:
        result = pd.DataFrame()
        result["code"] = [jq_code]
        result["status_date"] = [datetime.now().strftime("%Y-%m-%d")]
        result["status_type"] = ["正常交易"]
        result["reason"] = [""]
        return result

    result = pd.DataFrame()
    row = df_filtered.iloc[0]
    result["code"] = [jq_code]

    date_col = "停牌日期" if "停牌日期" in df_filtered.columns else "日期"
    result["status_date"] = [row.get(date_col, datetime.now().strftime("%Y-%m-%d"))]

    status_col = "停牌类型" if "停牌类型" in df_filtered.columns else "状态"
    result["status_type"] = [row.get(status_col, "停牌")]

    reason_col = "停牌原因" if "停牌原因" in df_filtered.columns else "原因"
    result["reason"] = [row.get(reason_col, "")]

    return result


def _extract_code_num(symbol: str) -> str:
    """提取6位代码数字"""
    if symbol.startswith("sh") or symbol.startswith("sz"):
        return symbol[2:].zfill(6)
    if ".XSHG" in symbol or ".XSHE" in symbol:
        return symbol.split(".")[0].zfill(6)
    return symbol.zfill(6)


def _normalize_to_jq(symbol: str) -> str:
    """转换为聚宽格式"""
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


def _normalize_date(date_str: str) -> str:
    """标准化日期为 YYYY-MM-DD"""
    if "-" in date_str:
        return date_str
    if len(date_str) == 8:
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    return date_str


def query_company_basic_info(
    symbols, cache_dir="finance_cache", force_update=False, use_duckdb=True
) -> pd.DataFrame:
    """
    批量查询公司基本信息（finance.STK_COMPANY_BASIC_INFO）。

    参数
    ----
    symbols    : 股票代码列表
    cache_dir  : pickle 缓存目录（备用）
    force_update: 强制更新
    use_duckdb : 是否使用 DuckDB 缓存（优先）

    返回
    ----
    DataFrame，每个股票一条记录
    """
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

    dfs = []
    for symbol in symbols:
        jq_code = _normalize_to_jq(symbol)

        if use_duckdb and _db_manager is not None and not force_update:
            df_cached = _db_manager.get_company_info(jq_code)
            if not df_cached.empty:
                dfs.append(df_cached[_COMPANY_BASIC_INFO_SCHEMA])
                continue

        try:
            df = get_company_info(
                symbol,
                cache_dir=cache_dir,
                force_update=force_update,
                use_duckdb=use_duckdb,
            )
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            print(f"[query_company_basic_info] 获取 {symbol} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

    result = pd.concat(dfs, ignore_index=True)
    return result


def query_status_change(
    symbols,
    start_date=None,
    end_date=None,
    cache_dir="finance_cache",
    force_update=False,
    use_duckdb=True,
) -> pd.DataFrame:
    """
    批量查询公司状态变动（finance.STK_STATUS_CHANGE）。

    参数
    ----
    symbols    : 股票代码列表
    start_date : 起始日期 'YYYY-MM-DD'
    end_date   : 结束日期 'YYYY-MM-DD'
    cache_dir  : pickle 缓存目录（备用）
    force_update: 强制更新
    use_duckdb : 是否使用 DuckDB 缓存（优先）

    返回
    ----
    DataFrame，每个状态变动一条记录
    """
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)

    dfs = []
    for symbol in symbols:
        jq_code = _normalize_to_jq(symbol)

        if (
            use_duckdb
            and _db_manager is not None
            and not force_update
            and start_date
            and end_date
        ):
            df_cached = _db_manager.get_status_change(jq_code, start_date, end_date)
            if not df_cached.empty:
                dfs.append(df_cached[_STATUS_CHANGE_SCHEMA])
                continue

        try:
            if start_date and end_date:
                start_dt = datetime.strptime(_normalize_date(start_date), "%Y-%m-%d")
                end_dt = datetime.strptime(_normalize_date(end_date), "%Y-%m-%d")
                current_dt = start_dt
                while current_dt <= end_dt:
                    date_str = current_dt.strftime("%Y-%m-%d")
                    df = get_security_status(
                        symbol,
                        date=date_str,
                        cache_dir=cache_dir,
                        force_update=force_update,
                        use_duckdb=use_duckdb,
                    )
                    if not df.empty:
                        dfs.append(df)
                    current_dt += timedelta(days=1)
            else:
                df = get_security_status(
                    symbol,
                    cache_dir=cache_dir,
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
                if not df.empty:
                    dfs.append(df)
        except Exception as e:
            print(f"[query_status_change] 获取 {symbol} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)

    result = pd.concat(dfs, ignore_index=True)
    return result


class FinanceQuery:
    """
    聚宽 finance 模块模拟器。
    提供 finance.run_query 兼容的查询接口。

    使用示例：
    >>> finance = FinanceQuery()
    >>> df = finance.run_query(finance.STK_COMPANY_BASIC_INFO.code == '600000.XSHG')
    >>> df = finance.run_query(finance.STK_STATUS_CHANGE.code == '000001.XSHE')
    """

    class STK_COMPANY_BASIC_INFO:
        """公司基本信息表"""

        code = None
        company_name = None
        establish_date = None
        list_date = None
        main_business = None
        industry = None
        registered_address = None
        company_status = None
        status_change_date = None
        change_type = None

    class STK_STATUS_CHANGE:
        """状态变动表"""

        code = None
        status_date = None
        status_type = None
        reason = None

    def run_query(
        self, query_obj, cache_dir="finance_cache", force_update=False, use_duckdb=True
    ) -> pd.DataFrame:
        """
        执行查询（模拟聚宽 finance.run_query）。

        参数
        ----
        query_obj    : 查询对象（表对象或查询表达式）
        cache_dir    : pickle 缓存目录
        force_update : 强制更新
        use_duckdb   : 是否使用 DuckDB 缓存

        返回
        ----
        pd.DataFrame，查询结果

        示例
        ----
        >>> finance = FinanceQuery()
        >>> # 查询单家公司信息
        >>> df = finance.run_query(finance.STK_COMPANY_BASIC_INFO.code == '600000.XSHG')
        >>> # 查询多家公司状态变动
        >>> df = finance.run_query(finance.STK_STATUS_CHANGE.code.in_(['000001.XSHE', '000002.XSHE']))
        """
        table_name = None
        conditions = {}

        if hasattr(query_obj, "__class__"):
            table_name = query_obj.__class__.__name__

        if hasattr(query_obj, "left") and hasattr(query_obj, "right"):
            if hasattr(query_obj.left, "__class__"):
                table_name = query_obj.left.__class__.__name__
            field_name = None
            if hasattr(query_obj.left, "name"):
                field_name = query_obj.left.name
            elif hasattr(query_obj, "left"):
                for attr in ["code", "company_name", "status_date", "status_type"]:
                    if (
                        hasattr(query_obj.left, attr)
                        and query_obj.left.__dict__.get(attr) is not None
                    ):
                        field_name = attr
                        break

            if field_name and hasattr(query_obj, "right"):
                conditions[field_name] = query_obj.right

        if table_name == "STK_COMPANY_BASIC_INFO":
            if "code" in conditions:
                return get_company_info(
                    conditions["code"],
                    cache_dir=cache_dir,
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
            else:
                return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

        elif table_name == "STK_STATUS_CHANGE":
            if "code" in conditions:
                return get_security_status(
                    conditions["code"],
                    cache_dir=cache_dir,
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
            else:
                return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)

        else:
            raise ValueError(f"不支持的表: {table_name}")


finance = FinanceQuery()


def run_query_simple(
    table: str,
    code: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    简化的查询接口（不依赖查询表达式）。

    参数
    ----
    table       : 表名 ('STK_COMPANY_BASIC_INFO' 或 'STK_STATUS_CHANGE')
    code        : 股票代码
    cache_dir   : 缓存目录
    force_update: 强制更新

    返回
    ----
    pd.DataFrame

    示例
    ----
    >>> df = run_query_simple('STK_COMPANY_BASIC_INFO', code='600000.XSHG')
    >>> df = run_query_simple('STK_STATUS_CHANGE', code='000001.XSHE')
    """
    if table == "STK_COMPANY_BASIC_INFO":
        if code:
            return get_company_info(
                code, cache_dir=cache_dir, force_update=force_update
            )
        else:
            return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)
    elif table == "STK_STATUS_CHANGE":
        if code:
            return get_security_status(
                code, cache_dir=cache_dir, force_update=force_update
            )
        else:
            return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)
    else:
        raise ValueError(f"不支持的表: {table}")


_LISTING_INFO_SCHEMA = [
    "code",
    "name",
    "start_date",
    "state_id",
    "state",
]


def get_listing_info(
    symbol=None,
    symbols=None,
    cache_dir="finance_cache",
    force_update=False,
) -> pd.DataFrame:
    """
    获取股票上市信息（STK_LIST）。

    参数
    ----
    symbol      : 单个股票代码
    symbols     : 多个股票代码列表
    cache_dir   : 缓存目录
    force_update: 强制更新

    返回
    ----
    pandas DataFrame，字段：
    - code: 股票代码（聚宽格式）
    - name: 股票名称
    - start_date: 上市日期
    - state_id: 状态代码 (301001=正常上市, 301002=停牌, 301003=退市)
    - state: 状态描述
    """
    if symbols is None:
        if symbol is None:
            return pd.DataFrame(columns=_LISTING_INFO_SCHEMA)
        symbols = [symbol]

    cache_file = os.path.join(cache_dir, "listing_info_all.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            df_all = pd.read_pickle(cache_file)
        except Exception:
            need_download = True

    if need_download:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        try:
            df_sh = ak.stock_info_sh_name_code(symbol="sh")
            df_sz = ak.stock_info_sz_name_code(symbol="sz")
            df_all = pd.concat([df_sh, df_sz], ignore_index=True)
            df_all.to_pickle(cache_file)
        except Exception as e:
            logger.warning(f"[listing_info] 获取上市信息失败: {e}")
            return pd.DataFrame(columns=_LISTING_INFO_SCHEMA)

    if df_all is None or df_all.empty:
        return pd.DataFrame(columns=_LISTING_INFO_SCHEMA)

    results = []
    for sym in symbols:
        code_num = _extract_code_num(sym)
        jq_code = _normalize_to_jq(sym)
        market = _get_market(sym)

        if market == "sh":
            code_col = "证券代码"
            name_col = "证券简称"
            date_col = "上市日期"
        else:
            code_col = "A股代码"
            name_col = "A股简称"
            date_col = "A股上市日期"

        df_filtered = df_all[df_all[code_col] == code_num]
        if df_filtered.empty:
            continue

        row = df_filtered.iloc[0]
        result = pd.DataFrame()
        result["code"] = [jq_code]
        result["name"] = [row.get(name_col, "")]
        result["start_date"] = [_parse_date(str(row.get(date_col, "")))]
        result["state_id"] = [301001]
        result["state"] = ["正常上市"]
        results.append(result)

    if not results:
        return pd.DataFrame(columns=_LISTING_INFO_SCHEMA)

    return pd.concat(results, ignore_index=True)


def _parse_date_for_listing(date_str: str) -> Optional[datetime]:
    """解析日期字符串"""
    if not date_str:
        return None
    date_str = str(date_str).strip()
    for fmt in ["%Y-%m-%d", "%Y%m%d", "%Y/%m/%d", "%Y年%m月%d日"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def _get_market(symbol: str) -> str:
    """判断市场：sh 或 sz"""
    if "XSHG" in symbol or symbol.startswith("6") or symbol.startswith("sh"):
        return "sh"
    return "sz"


_COMPANY_INFO_ROBUST_SCHEMA = [
    "code",
    "company_name",
    "establish_date",
    "list_date",
    "main_business",
    "industry",
    "registered_address",
    "company_status",
    "status_change_date",
    "change_type",
]


def _create_empty_company_info_df() -> pd.DataFrame:
    """创建带 schema 的空公司信息 DataFrame"""
    return pd.DataFrame(columns=_COMPANY_INFO_ROBUST_SCHEMA)


def get_company_info_robust(
    symbol: Union[str, List[str]],
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> RobustResult:
    """
    稳健版获取公司基本信息，返回 RobustResult。

    参数
    ----
    symbol      : 股票代码（单个或列表）
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    RobustResult:
        - success: 是否成功
        - data: DataFrame（带 schema）
        - reason: 成功/失败原因
        - source: 数据来源
    """
    if symbol is None:
        return RobustResult(
            success=False,
            data=_create_empty_company_info_df(),
            reason="股票代码为空",
            source="input",
        )

    if isinstance(symbol, list):
        if len(symbol) == 0:
            return RobustResult(
                success=False,
                data=_create_empty_company_info_df(),
                reason="股票代码列表为空",
                source="input",
            )
        return _get_company_info_batch_robust(
            symbol, cache_dir, force_update, use_duckdb
        )

    try:
        df = get_company_info(
            symbol,
            cache_dir=cache_dir,
            force_update=force_update,
            use_duckdb=use_duckdb,
        )

        if df is None or df.empty:
            jq_code = _normalize_to_jq(symbol)
            return RobustResult(
                success=False,
                data=_create_empty_company_info_df(),
                reason=f"未找到股票 {jq_code} 的公司信息（可能为无效代码或数据源暂无数据）",
                source="network",
            )

        for col in _COMPANY_INFO_ROBUST_SCHEMA:
            if col not in df.columns:
                df[col] = None

        return RobustResult(
            success=True,
            data=df,
            reason=f"成功获取 {symbol} 的公司信息",
            source="network",
        )

    except Exception as e:
        logger.warning(f"[get_company_info_robust] 获取 {symbol} 失败: {e}")
        return RobustResult(
            success=False,
            data=_create_empty_company_info_df(),
            reason=f"获取公司信息异常: {str(e)[:100]}",
            source="network",
        )


def _get_company_info_batch_robust(
    symbols: List[str],
    cache_dir: str,
    force_update: bool,
    use_duckdb: bool,
) -> RobustResult:
    """批量获取公司信息（稳健版）"""
    dfs = []
    errors = []

    for symbol in symbols:
        try:
            df = get_company_info(
                symbol,
                cache_dir=cache_dir,
                force_update=force_update,
                use_duckdb=use_duckdb,
            )
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            errors.append(f"{symbol}: {str(e)[:50]}")
            logger.warning(f"[batch] 获取 {symbol} 失败: {e}")

    if not dfs:
        return RobustResult(
            success=False,
            data=_create_empty_company_info_df(),
            reason=f"批量查询失败，共 {len(symbols)} 只股票，错误: {errors[:3]}",
            source="network",
        )

    result_df = pd.concat(dfs, ignore_index=True)

    for col in _COMPANY_INFO_ROBUST_SCHEMA:
        if col not in result_df.columns:
            result_df[col] = None

    reason = f"成功获取 {len(dfs)}/{len(symbols)} 只股票的公司信息"
    if errors:
        reason += f"，失败 {len(errors)} 只"

    return RobustResult(
        success=len(dfs) > 0,
        data=result_df,
        reason=reason,
        source="network",
    )


def query_company_info_robust(
    symbols: List[str],
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> RobustResult:
    """
    稳健版批量查询公司基本信息。

    参数
    ----
    symbols     : 股票代码列表
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    RobustResult
    """
    return get_company_info_robust(
        symbols,
        cache_dir=cache_dir,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )


def get_security_status_robust(
    symbol: Union[str, List[str]],
    date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> RobustResult:
    """
    稳健版获取证券状态。

    参数
    ----
    symbol      : 股票代码
    date        : 查询日期
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB

    返回
    ----
    RobustResult
    """
    _STATUS_SCHEMA = ["code", "status_date", "status_type", "reason"]

    if symbol is None:
        return RobustResult(
            success=False,
            data=pd.DataFrame(columns=_STATUS_SCHEMA),
            reason="股票代码为空",
            source="input",
        )

    try:
        df = get_security_status(
            symbol,
            date=date,
            cache_dir=cache_dir,
            force_update=force_update,
            use_duckdb=use_duckdb,
        )

        if df is None or df.empty:
            return RobustResult(
                success=False,
                data=pd.DataFrame(columns=_STATUS_SCHEMA),
                reason=f"未找到股票 {symbol} 的状态信息",
                source="network",
            )

        for col in _STATUS_SCHEMA:
            if col not in df.columns:
                df[col] = None

        return RobustResult(
            success=True,
            data=df,
            reason=f"成功获取 {symbol} 的证券状态",
            source="network",
        )

    except Exception as e:
        logger.warning(f"[get_security_status_robust] 获取 {symbol} 失败: {e}")
        return RobustResult(
            success=False,
            data=pd.DataFrame(columns=_STATUS_SCHEMA),
            reason=f"获取证券状态异常: {str(e)[:100]}",
            source="network",
        )


_INDUSTY_INFO_SCHEMA = [
    "code",
    "industry_code",
    "industry_name",
    "industry_level",
]


def get_company_info_list(
    securities: List[str],
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> Dict[str, pd.DataFrame]:
    """
    批量获取公司信息，返回字典格式。

    参数
    ----
    securities  : 股票代码列表，如 ['600000.XSHG', '000001.XSHE']
    cache_dir   : pickle 缓存目录（备用）
    force_update: True 时强制重新下载
    use_duckdb  : 是否使用 DuckDB 缓存（优先）

    返回
    ----
    dict{security: DataFrame}，每个股票对应一个 DataFrame

    示例
    ----
    >>> result = get_company_info_list(['600519.XSHG', '000001.XSHE'])
    >>> df_600519 = result['600519.XSHG']
    >>> df_000001 = result['000001.XSHE']
    """
    if securities is None or len(securities) == 0:
        return {}

    result_dict = {}
    for security in securities:
        jq_code = _normalize_to_jq(security)
        try:
            df = get_company_info(
                security,
                cache_dir=cache_dir,
                force_update=force_update,
                use_duckdb=use_duckdb,
            )
            result_dict[jq_code] = df
        except Exception as e:
            logger.warning(f"[get_company_info_list] 获取 {security} 失败: {e}")
            result_dict[jq_code] = pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

    return result_dict


def get_industry_info(
    security: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取行业信息。

    参数
    ----
    security    : 股票代码，如 '600000.XSHG'
    cache_dir   : 缓存目录
    force_update: 强制更新

    返回
    ----
    pandas DataFrame，字段：
    - code: 股票代码（聚宽格式）
    - industry_code: 行业代码
    - industry_name: 行业名称
    - industry_level: 行业层级

    示例
    ----
    >>> df = get_industry_info('600519.XSHG')
    >>> print(df['industry_name'])
    """
    code_num = _extract_code_num(security)
    jq_code = _normalize_to_jq(security)

    cache_file = os.path.join(cache_dir, f"industry_info_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < CACHE_EXPIRE_DAYS:
                return cached_df
            need_download = True
        except Exception:
            need_download = True

    if need_download:
        try:
            df_raw = _fetch_company_industry(code_num)
            if df_raw is not None and not df_raw.empty:
                result = _normalize_industry_info(df_raw, jq_code)
                if not result.empty:
                    result.to_pickle(cache_file)
                    return result
        except Exception as e:
            logger.warning(f"[get_industry_info] 获取 {security} 行业信息失败: {e}")

    return pd.DataFrame(columns=_INDUSTY_INFO_SCHEMA)


def _normalize_industry_info(df_raw: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    """标准化行业信息数据"""
    if df_raw is None or df_raw.empty:
        return pd.DataFrame(columns=_INDUSTY_INFO_SCHEMA)

    result = pd.DataFrame()
    result["code"] = [jq_code]

    industry_name = None
    for col in ["行业板块", "板块名称", "industry_name", "行业"]:
        if col in df_raw.columns:
            industry_name = df_raw.iloc[0].get(col)
            break

    result["industry_code"] = [None]
    result["industry_name"] = [industry_name]
    result["industry_level"] = [1]

    return result


def prewarm_company_info_cache(
    securities: List[str] = None,
    cache_dir: str = "finance_cache",
    max_workers: int = 5,
    use_duckdb: bool = True,
) -> Dict[str, bool]:
    """
    缓存预热机制：提前下载并缓存公司信息。

    参数
    ----
    securities  : 需要预热的股票代码列表，默认预热沪深300主要成分股
    cache_dir   : 缓存目录
    max_workers : 并发下载的最大线程数（暂不支持并发，预留）
    use_duckdb  : 是否写入 DuckDB 缓存

    返回
    ----
    dict{security: bool}，表示每只股票是否成功预热

    示例
    ----
    >>> result = prewarm_company_info_cache(['600519.XSHG', '000001.XSHE'])
    >>> print(f"成功预热: {sum(result.values())} 只股票")
    """
    if securities is None:
        securities = _get_default_prewarm_stocks()

    result = {}
    total = len(securities)

    logger.info(f"开始预热公司信息缓存，共 {total} 只股票")

    for i, security in enumerate(securities):
        try:
            df = get_company_info(
                security,
                cache_dir=cache_dir,
                force_update=True,
                use_duckdb=use_duckdb,
            )
            result[security] = not df.empty
            if (i + 1) % 10 == 0:
                logger.info(f"预热进度: {i + 1}/{total}")
        except Exception as e:
            logger.warning(f"[prewarm] 预热 {security} 失败: {e}")
            result[security] = False

    success_count = sum(result.values())
    logger.info(f"预热完成: 成功 {success_count}/{total}")

    return result


def _get_default_prewarm_stocks() -> List[str]:
    """获取默认预热股票列表（沪深300主要成分股）"""
    return [
        "600519.XSHG",
        "600036.XSHG",
        "601318.XSHG",
        "600030.XSHG",
        "601166.XSHG",
        "600276.XSHG",
        "600887.XSHG",
        "601398.XSHG",
        "600000.XSHG",
        "601288.XSHG",
        "000001.XSHE",
        "000002.XSHE",
        "000858.XSHE",
        "002594.XSHE",
        "000333.XSHE",
        "000651.XSHE",
        "002415.XSHE",
        "000725.XSHE",
        "002352.XSHE",
        "000568.XSHE",
    ]
