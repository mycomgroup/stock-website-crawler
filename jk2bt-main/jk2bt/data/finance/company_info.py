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
- Parquet 缓存：存储在 data/company_info_parquet 中
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
import random

from jk2bt.utils.result import RobustResult
from jk2bt.utils.symbol import extract_code_num, ak_code_to_jq

logger = logging.getLogger(__name__)


def _parse_date(val):
    """Parse date value, returning None for invalid values."""
    if val is None or pd.isna(val):
        return None
    val = str(val).strip()
    if not val or val in ("None", "nan", "NaT", ""):
        return None
    try:
        return pd.to_datetime(val).strftime("%Y-%m-%d")
    except Exception:
        return val


_MAX_RETRY_ATTEMPTS = 3
_RETRY_DELAY_SECONDS = 2
_RETRY_JITTER = 2


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
                delay = _RETRY_DELAY_SECONDS + random.uniform(0, _RETRY_JITTER)
                logger.warning(
                    f"[retry] {func.__name__} 第 {attempt + 1} 次失败: {e}, "
                    f"等待 {delay:.1f}s 后重试"
                )
                time.sleep(delay)
            else:
                logger.error(
                    f"[retry] {func.__name__} 重试 {max_attempts} 次后仍失败: {e}"
                )
    return None


_CACHE_AVAILABLE = False
_CACHE_ERROR_MSG = ""
try:
    from jk2bt.cache import get_cache_manager

    _CACHE_AVAILABLE = True
except ImportError as e:
    _CACHE_ERROR_MSG = str(e)
    logger.warning(f"parquet_cache 模块不可用（{e}）")


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

_MANAGEMENT_INFO_SCHEMA = [
    "code",
    "person_id",
    "title_class_id",
    "title_class",
    "title",
    "name",
    "position",
    "gender",
    "birth_year",
    "highest_degree",
    "title_level",
    "profession_certificate",
    "nationality",
    "resume",
    "education",
    "start_date",
    "end_date",
    "leave_date",
    "leave_reason",
    "on_job",
    "shares_held",
    "compensation",
    "relationship",
    "direct_shares",
    "indirect_shares",
    "option_shares",
]

_EMPLOYEE_INFO_SCHEMA = [
    # JQData standard fields
    "company_id",
    "code",
    "name",
    "end_date",
    "pub_date",
    "employee",
    "retirement",
    "graduate_rate",
    "college_rate",
    "middle_rate",
    # akshare detailed fields (kept for backward compatibility)
    "report_date",
    "employee_count",
    "professional_count",
    "production_count",
    "sales_count",
    "finance_count",
    "admin_count",
    "education_bachelor",
    "education_master",
    "education_phd",
]

_NAME_HISTORY_SCHEMA = [
    "code",
    "name",
    "start_date",
    "end_date",
    "change_reason",
]


class CompanyInfoCacheManager:
    """公司信息 parquet_cache 管理器"""

    _instance = None
    _lock = None

    def __new__(cls, base_dir: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._lock = cls._instance._init_manager(base_dir)
        return cls._instance

    def _init_manager(self, base_dir: str = None):
        if not _CACHE_AVAILABLE:
            self._cache = None
            return None

        if base_dir is None:
            from jk2bt.utils.paths import resolve_cache_path

            base_dir = resolve_cache_path("data_cache/cache")

        self.base_dir = base_dir
        self._cache = None

        try:
            self._cache = get_cache_manager(base_dir=base_dir)
            logger.info(f"parquet_cache 初始化成功: {base_dir}")
        except Exception as e:
            logger.warning(f"parquet_cache 初始化失败: {e}")
            self._cache = None

        return self._cache

    def get_cache(self):
        return self._cache

    def insert_company_info(self, df: pd.DataFrame):
        if self._cache is None or df.empty:
            return

        df = df.copy()

        # 如果 establish_date 存在且 list_date 为空，用 establish_date 填充
        if "establish_date" in df.columns and "list_date" in df.columns:
            df["list_date"] = df["list_date"].fillna(df["establish_date"])
            df = df.drop(columns=["establish_date"])

        rename_map = {
            "code": "symbol",
            "company_name": "name",
        }
        df = df.rename(columns=rename_map)

        for col in ["symbol", "name", "industry", "area", "list_date", "market"]:
            if col not in df.columns:
                df[col] = None

        # 转换 list_date 为日期类型
        if "list_date" in df.columns:
            df["list_date"] = pd.to_datetime(
                df["list_date"].astype(str), format="%Y%m%d", errors="coerce"
            )

        cols = ["symbol", "name", "industry", "area", "list_date", "market"]
        df = df[cols]

        try:
            self._cache.put("company_info", df)
            logger.info(f"插入/更新 {len(df)} 条公司信息")
        except Exception as e:
            logger.warning(f"插入公司信息失败: {e}")

    def get_company_info(self, code: str) -> pd.DataFrame:
        if self._cache is None:
            return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

        try:
            result = self._cache.get("company_info", where={"symbol": code})
            if result is not None and not result.empty:
                rename_map = {
                    "symbol": "code",
                    "name": "company_name",
                    "list_date": "establish_date",
                }
                result = result.rename(columns=rename_map)
                for col in _COMPANY_BASIC_INFO_SCHEMA:
                    if col not in result.columns:
                        result[col] = None
                return result[_COMPANY_BASIC_INFO_SCHEMA]
            return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)
        except Exception as e:
            logger.warning(f"查询公司信息失败: {e}")
            return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

    def insert_status_change(self, df: pd.DataFrame):
        if self._cache is None or df.empty:
            return

        df = df.copy()
        if "symbol" not in df.columns and "code" in df.columns:
            df = df.rename(columns={"code": "symbol"})

        for col in ["symbol", "status_date", "status_type", "reason"]:
            if col not in df.columns:
                df[col] = None

        cols = ["symbol", "status_date", "status_type", "reason"]
        df = df[cols]

        try:
            self._cache.put("status_change", df)
            logger.info(f"插入/更新 {len(df)} 条状态变动")
        except Exception as e:
            logger.warning(f"插入状态变动失败: {e}")

    def get_status_change(
        self, code: str, start_date: str = None, end_date: str = None
    ) -> pd.DataFrame:
        if self._cache is None:
            return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)

        try:
            where = {"symbol": code}
            result = self._cache.get("status_change", where=where)
            if result is not None and not result.empty:
                if start_date and end_date:
                    result = result[
                        (result["status_date"] >= start_date)
                        & (result["status_date"] <= end_date)
                    ]
                result = result.sort_values("status_date")
                if "code" not in result.columns:
                    result = result.rename(columns={"symbol": "code"})
                for col in _STATUS_CHANGE_SCHEMA:
                    if col not in result.columns:
                        result[col] = None
                return result[_STATUS_CHANGE_SCHEMA]
            return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)
        except Exception as e:
            logger.warning(f"查询状态变动失败: {e}")
            return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)

    def insert_management_info(self, df: pd.DataFrame):
        if self._cache is None or df.empty:
            return
        df_copy = df.copy()
        if "code" in df_copy.columns and "symbol" not in df_copy.columns:
            df_copy = df_copy.rename(columns={"code": "symbol"})
        try:
            self._cache.put("management_info", df_copy)
            logger.info(f"插入/更新 {len(df_copy)} 条管理人员信息")
        except Exception as e:
            logger.warning(f"插入管理人员信息失败: {e}")

    def get_management_info(self, code: str) -> pd.DataFrame:
        if self._cache is None:
            return pd.DataFrame(columns=_MANAGEMENT_INFO_SCHEMA)
        try:
            result = self._cache.get("management_info", where={"symbol": code})
            if result is not None and not result.empty:
                if "code" not in result.columns:
                    result = result.rename(columns={"symbol": "code"})
                for col in _MANAGEMENT_INFO_SCHEMA:
                    if col not in result.columns:
                        result[col] = None
                return result[_MANAGEMENT_INFO_SCHEMA]
            return pd.DataFrame(columns=_MANAGEMENT_INFO_SCHEMA)
        except Exception as e:
            logger.warning(f"查询管理人员信息失败: {e}")
            return pd.DataFrame(columns=_MANAGEMENT_INFO_SCHEMA)

    def insert_employee_info(self, df: pd.DataFrame):
        if self._cache is None or df.empty:
            return
        df_copy = df.copy()
        if "code" in df_copy.columns and "symbol" not in df_copy.columns:
            df_copy = df_copy.rename(columns={"code": "symbol"})
        try:
            self._cache.put("employee_info", df_copy)
            logger.info(f"插入/更新 {len(df_copy)} 条员工信息")
        except Exception as e:
            logger.warning(f"插入员工信息失败: {e}")

    def get_employee_info(self, code: str) -> pd.DataFrame:
        if self._cache is None:
            return pd.DataFrame(columns=_EMPLOYEE_INFO_SCHEMA)
        try:
            result = self._cache.get("employee_info", where={"symbol": code})
            if result is not None and not result.empty:
                if "code" not in result.columns:
                    result = result.rename(columns={"symbol": "code"})
                for col in _EMPLOYEE_INFO_SCHEMA:
                    if col not in result.columns:
                        result[col] = None
                return result[_EMPLOYEE_INFO_SCHEMA]
            return pd.DataFrame(columns=_EMPLOYEE_INFO_SCHEMA)
        except Exception as e:
            logger.warning(f"查询员工信息失败: {e}")
            return pd.DataFrame(columns=_EMPLOYEE_INFO_SCHEMA)

    def insert_name_history(self, df: pd.DataFrame):
        if self._cache is None or df.empty:
            return
        df_copy = df.copy()
        if "code" in df_copy.columns and "symbol" not in df_copy.columns:
            df_copy = df_copy.rename(columns={"code": "symbol"})
        try:
            self._cache.put("name_history", df_copy)
            logger.info(f"插入/更新 {len(df_copy)} 条名称变更历史")
        except Exception as e:
            logger.warning(f"插入名称变更历史失败: {e}")

    def get_name_history(self, code: str) -> pd.DataFrame:
        if self._cache is None:
            return pd.DataFrame(columns=_NAME_HISTORY_SCHEMA)
        try:
            result = self._cache.get("name_history", where={"symbol": code})
            if result is not None and not result.empty:
                if "code" not in result.columns:
                    result = result.rename(columns={"symbol": "code"})
                for col in _NAME_HISTORY_SCHEMA:
                    if col not in result.columns:
                        result[col] = None
                return result[_NAME_HISTORY_SCHEMA]
            return pd.DataFrame(columns=_NAME_HISTORY_SCHEMA)
        except Exception as e:
            logger.warning(f"查询名称变更历史失败: {e}")
            return pd.DataFrame(columns=_NAME_HISTORY_SCHEMA)


_db_manager = CompanyInfoCacheManager() if _CACHE_AVAILABLE else None

# Baostock 连接池（避免频繁 login/logout）
_bs_connected = False


def _bs_login():
    """获取 Baostock 连接（单例模式）"""
    global _bs_connected
    if not _bs_connected:
        try:
            import baostock as bs

            lg = bs.login()
            if lg.error_code == "0":
                _bs_connected = True
                return True
        except Exception:
            pass
    return _bs_connected


def _bs_logout():
    """关闭 Baostock 连接"""
    global _bs_connected
    if _bs_connected:
        try:
            import baostock as bs

            bs.logout()
        except Exception:
            pass
        _bs_connected = False


import atexit

atexit.register(_bs_logout)


def get_company_info(symbol, force_update=False, use_duckdb=True) -> pd.DataFrame:
    """
    获取上市公司基本信息。

    参数
    ----
    symbol     : 股票代码，支持 '600519.XSHG', '000001.XSHE', 'sh600519', 'sz000001', '600519' 等格式
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
    jq_code = ak_code_to_jq(symbol)

    if use_duckdb and _db_manager is not None and not force_update:
        df_cached = _db_manager.get_company_info(jq_code)
        if not df_cached.empty:
            return df_cached[_COMPANY_BASIC_INFO_SCHEMA]

    try:
        df_profile = _fetch_company_profile(extract_code_num(symbol))
        df_industry = _fetch_company_industry(extract_code_num(symbol))

        result = _merge_and_normalize(df_profile, df_industry, jq_code)

        if not result.empty:
            if use_duckdb and _db_manager is not None:
                _db_manager.insert_company_info(result)
            return result
        else:
            return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

    except Exception as e:
        print(f"[company_info] 获取公司信息失败 {symbol}: {e}")
        return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)


def get_security_status(
    symbol, date=None, force_update=False, use_duckdb=True
) -> pd.DataFrame:
    """
    获取指定日期的证券状态（停牌、复牌、退市等）。

    参数
    ----
    symbol     : 股票代码
    date       : 查询日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'，默认最近交易日
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
    jq_code = ak_code_to_jq(symbol)

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    date_str = _normalize_date(date)

    if use_duckdb and _db_manager is not None and not force_update:
        df_cached = _db_manager.get_status_change(jq_code, date_str, date_str)
        if not df_cached.empty:
            return df_cached[_STATUS_CHANGE_SCHEMA]

    try:
        df_all = _fetch_suspension_data(date_str)
        if df_all is not None and not df_all.empty:
            result = _filter_status_for_symbol(
                df_all, extract_code_num(symbol), jq_code
            )
            if use_duckdb and _db_manager is not None and not result.empty:
                _db_manager.insert_status_change(result)
            return result
    except Exception as e:
        print(f"[security_status] 获取状态失败 {symbol}: {e}")

    return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)


def _fetch_company_profile(code_num: str) -> Optional[pd.DataFrame]:
    """从 Baostock 获取公司基本信息（优先），AkShare 作为备用"""
    # 优先使用 Baostock（稳定快速，无网络限制）
    try:
        df = _fetch_company_profile_baostock(code_num)
        if df is not None and not df.empty:
            return df
    except Exception as e:
        logger.warning(f"[company_profile] Baostock 获取失败 {code_num}: {e}")

    # 备用：AkShare
    logger.info(f"[company_profile] 尝试 AkShare 获取 {code_num}")
    try:
        from jk2bt.data.sources import get_adapter

        df = _retry_akshare_call(get_adapter().get_company_info, symbol=code_num)
        if df is not None and not df.empty:
            return df
    except Exception as e:
        logger.error(f"[company_profile] AkShare 获取失败 {code_num}: {e}")

    return None


def _fetch_company_profile_baostock(code_num: str) -> Optional[pd.DataFrame]:
    """从 Baostock 获取公司基本信息（使用全局连接）"""
    try:
        import baostock as bs

        if not _bs_login():
            return None

        bs_code = f"sh.{code_num}" if code_num.startswith("6") else f"sz.{code_num}"

        rs = bs.query_stock_basic(code=bs_code)
        if rs.error_code != "0":
            return None

        fields = rs.fields
        rows = []
        while (rs.error_code == "0") and rs.next():
            row_data = rs.get_row_data()
            row_dict = dict(zip(fields, row_data))
            rows.append(row_dict)

        if not rows:
            return None

        row = rows[0]
        items = []
        items.append({"item": "公司名称", "value": row.get("code_name", "")})
        items.append({"item": "上市时间", "value": row.get("ipoDate", "")})
        items.append({"item": "所属行业", "value": row.get("industry", "")})
        items.append(
            {"item": "行业分类", "value": row.get("industryClassification", "")}
        )

        return pd.DataFrame(items)

    except ImportError:
        return None
    except Exception as e:
        logger.error(f"[baostock] 获取公司信息失败 {code_num}: {e}")
        return None


def _fetch_company_industry(code_num: str) -> Optional[pd.DataFrame]:
    """从 Baostock 获取公司行业信息（使用全局连接）"""
    try:
        import baostock as bs

        if not _bs_login():
            return None

        bs_code = f"sh.{code_num}" if code_num.startswith("6") else f"sz.{code_num}"

        rs = bs.query_stock_industry(code=bs_code)
        if rs.error_code != "0":
            return None

        fields = rs.fields
        rows = []
        while (rs.error_code == "0") and rs.next():
            row_data = rs.get_row_data()
            row_dict = dict(zip(fields, row_data))
            rows.append(row_dict)

        if not rows:
            return None

        industry_name = rows[0].get("industry", "")
        if industry_name:
            return pd.DataFrame({"行业板块": [industry_name]})

        return None

    except ImportError:
        return None
    except Exception as e:
        logger.warning(f"[company_industry] Baostock 获取失败 {code_num}: {e}")
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

    # 检查是否有有效数据（除了 code 之外的字段）
    has_data = (
        result["company_name"].notna().any()
        or result["list_date"].notna().any()
        or result["industry"].notna().any()
    )

    if not has_data:
        return pd.DataFrame()

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
    from jk2bt.data.sources import get_adapter

    try:
        date_num = date_str.replace("-", "")
        df = _retry_akshare_call(get_adapter().get_suspension_em, date=date_num)
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


def _normalize_date(date_str: str) -> str:
    """标准化日期为 YYYY-MM-DD"""
    if "-" in date_str:
        return date_str
    if len(date_str) == 8:
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    return date_str


def query_company_basic_info(
    symbols, force_update=False, use_duckdb=True
) -> pd.DataFrame:
    """
    批量查询公司基本信息（finance.STK_COMPANY_BASIC_INFO）。

    参数
    ----
    symbols    : 股票代码列表
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
        jq_code = ak_code_to_jq(symbol)

        if use_duckdb and _db_manager is not None and not force_update:
            df_cached = _db_manager.get_company_info(jq_code)
            if not df_cached.empty:
                dfs.append(df_cached[_COMPANY_BASIC_INFO_SCHEMA])
                continue

        try:
            df = get_company_info(
                symbol,
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
        jq_code = ak_code_to_jq(symbol)

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
                        force_update=force_update,
                        use_duckdb=use_duckdb,
                    )
                    if not df.empty:
                        dfs.append(df)
                    current_dt += timedelta(days=1)
            else:
                df = get_security_status(
                    symbol,
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

    class STK_LIST:
        """上市信息表"""

        id = None
        code = None
        name = None
        short_name = None
        category = None
        exchange = None
        start_date = None
        end_date = None
        company_id = None
        company_name = None
        ipo_shares = None
        book_price = None
        par_value = None
        state_id = None
        state = None

    class STK_NAME_HISTORY:
        """简称变更表"""

        id = None
        code = None
        company_id = None
        new_name = None
        new_spelling = None
        org_name = None
        org_spelling = None
        start_date = None
        pub_date = None
        reason = None

    class STK_COMPANY_INFO:
        """公司基本信息表"""

        id = None
        company_id = None
        code = None
        full_name = None
        short_name = None
        a_code = None
        b_code = None
        h_code = None
        fullname_en = None
        shortname_en = None
        legal_representative = None
        register_location = None
        office_address = None
        zipcode = None
        register_capital = None
        currency = None
        establish_date = None
        website = None
        email = None
        main_business = None
        province = None
        city = None
        industry_id = None
        industry_1 = None
        industry_2 = None
        ceo = None
        comments = None

    class STK_MANAGEMENT_INFO:
        """管理人员任职情况表"""

        code = None
        person_id = None
        title_class_id = None
        title_class = None
        title = None
        name = None
        position = None
        gender = None
        birth_year = None
        highest_degree = None
        title_level = None
        profession_certificate = None
        nationality = None
        resume = None
        education = None
        start_date = None
        end_date = None
        leave_date = None
        leave_reason = None
        on_job = None
        shares_held = None
        compensation = None
        relationship = None
        direct_shares = None
        indirect_shares = None
        option_shares = None

    class STK_EMPLOYEE_INFO:
        """员工情况信息表"""

        company_id = None
        code = None
        name = None
        end_date = None
        pub_date = None
        employee = None
        retirement = None
        graduate_rate = None
        college_rate = None
        middle_rate = None
        report_date = None
        employee_count = None
        professional_count = None
        production_count = None
        sales_count = None
        finance_count = None
        admin_count = None
        education_bachelor = None
        education_master = None
        education_phd = None

    STK_LIST_SCHEMA = [
        "id",
        "code",
        "name",
        "short_name",
        "category",
        "exchange",
        "start_date",
        "end_date",
        "company_id",
        "company_name",
        "ipo_shares",
        "book_price",
        "par_value",
        "state_id",
        "state",
    ]

    STK_NAME_HISTORY_SCHEMA = [
        "id",
        "code",
        "company_id",
        "new_name",
        "new_spelling",
        "org_name",
        "org_spelling",
        "start_date",
        "pub_date",
        "reason",
    ]

    STK_COMPANY_INFO_SCHEMA = [
        "id",
        "company_id",
        "code",
        "full_name",
        "short_name",
        "a_code",
        "b_code",
        "h_code",
        "fullname_en",
        "shortname_en",
        "legal_representative",
        "register_location",
        "office_address",
        "zipcode",
        "register_capital",
        "currency",
        "establish_date",
        "website",
        "email",
        "main_business",
        "province",
        "city",
        "industry_id",
        "industry_1",
        "industry_2",
        "ceo",
        "comments",
    ]

    STK_MANAGEMENT_INFO_SCHEMA = _MANAGEMENT_INFO_SCHEMA

    STK_EMPLOYEE_INFO_SCHEMA = _EMPLOYEE_INFO_SCHEMA

    def run_query(self, query_obj, force_update=False, use_duckdb=True) -> pd.DataFrame:
        """
        执行查询（模拟聚宽 finance.run_query）。

        参数
        ----
        query_obj    : 查询对象（表对象或查询表达式）
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
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
            else:
                return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)

        elif table_name == "STK_STATUS_CHANGE":
            if "code" in conditions:
                return get_security_status(
                    conditions["code"],
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
            else:
                return pd.DataFrame(columns=_STATUS_CHANGE_SCHEMA)

        elif table_name == "STK_LIST":
            if "code" in conditions:
                return get_listing_info(conditions["code"])
            return pd.DataFrame(columns=self.STK_LIST_SCHEMA)

        elif table_name == "STK_NAME_HISTORY":
            if "code" in conditions:
                return get_name_history(conditions["code"])
            return pd.DataFrame(columns=self.STK_NAME_HISTORY_SCHEMA)

        elif table_name == "STK_COMPANY_INFO":
            if "code" in conditions:
                return get_company_info(
                    conditions["code"],
                    force_update=force_update,
                    use_duckdb=use_duckdb,
                )
            return pd.DataFrame(columns=self.STK_COMPANY_INFO_SCHEMA)

        elif table_name == "STK_MANAGEMENT_INFO":
            if "code" in conditions:
                return get_management_info(conditions["code"])
            return pd.DataFrame(columns=self.STK_MANAGEMENT_INFO_SCHEMA)

        elif table_name == "STK_EMPLOYEE_INFO":
            if "code" in conditions:
                return get_employee_info(conditions["code"])
            return pd.DataFrame(columns=self.STK_EMPLOYEE_INFO_SCHEMA)

        else:
            raise ValueError(f"不支持的表: {table_name}")


finance = FinanceQuery()


def run_query_simple(
    table: str,
    code: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    简化的查询接口（不依赖查询表达式）。

    参数
    ----
    table       : 表名 ('STK_COMPANY_BASIC_INFO' 或 'STK_STATUS_CHANGE')
    code        : 股票代码
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
            return get_company_info(code, force_update=force_update)
        else:
            return pd.DataFrame(columns=_COMPANY_BASIC_INFO_SCHEMA)
    elif table == "STK_STATUS_CHANGE":
        if code:
            return get_security_status(code, force_update=force_update)
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
    force_update=False,
) -> pd.DataFrame:
    """
    获取股票上市信息（STK_LIST）。

    参数
    ----
    symbol      : 单个股票代码
    symbols     : 多个股票代码列表
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

    from jk2bt.data.sources import get_adapter

    try:
        df_sh = get_adapter().get_stock_info_sh_name_code(symbol="sh")
        df_sz = get_adapter().get_stock_info_sz_name_code(symbol="sz")
        df_all = pd.concat([df_sh, df_sz], ignore_index=True)
    except Exception as e:
        logger.warning(f"[listing_info] 获取上市信息失败: {e}")
        return pd.DataFrame(columns=_LISTING_INFO_SCHEMA)

    if df_all is None or df_all.empty:
        return pd.DataFrame(columns=_LISTING_INFO_SCHEMA)

    results = []
    for sym in symbols:
        code_num = extract_code_num(sym)
        jq_code = ak_code_to_jq(sym)
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


def get_name_history(code: str, force_update: bool = False) -> pd.DataFrame:
    """
    获取股票名称变更历史（STK_NAME_HISTORY）。

    参数
    ----
    code        : 股票代码（聚宽格式或纯数字）
    force_update: 强制更新

    返回
    ----
    pandas DataFrame，字段：
    - id: 主键ID
    - code: 股票代码（聚宽格式）
    - company_id: 公司ID
    - new_name: 新名称
    - new_spelling: 新名称拼音
    - org_name: 原名称
    - org_spelling: 原名称拼音
    - start_date: 变更日期
    - pub_date: 公告日期
    - reason: 变更原因
    """
    code_num = extract_code_num(code)
    jq_code = ak_code_to_jq(code)

    try:
        import akshare as ak

        df = ak.stock_info_change_name(symbol=code_num)
        if df is not None and not df.empty:
            rename_map = {}
            for col in df.columns:
                if "变更日期" in col or "date" in col.lower():
                    rename_map[col] = "start_date"
                elif "股票简称" in col or "简称" in col or "名称" in col:
                    rename_map[col] = "new_name"
                elif "拼音" in col or "spelling" in col.lower():
                    if "原" in col or "old" in col.lower() or "org" in col.lower():
                        rename_map[col] = "org_spelling"
                    else:
                        rename_map[col] = "new_spelling"
                elif "公告" in col or "pub" in col.lower():
                    rename_map[col] = "pub_date"
                elif "原因" in col or "reason" in col.lower():
                    rename_map[col] = "reason"
                elif "原" in col or "old" in col.lower() or "org" in col.lower():
                    if "名称" in col or "name" in col.lower():
                        rename_map[col] = "org_name"

            df = df.rename(columns=rename_map)

            result = pd.DataFrame()
            result["id"] = range(len(df))
            result["code"] = jq_code
            result["company_id"] = None
            result["new_name"] = df.get("new_name", "")
            result["new_spelling"] = df.get("new_spelling", None)
            result["org_name"] = df.get("org_name", None)
            result["org_spelling"] = df.get("org_spelling", None)
            result["start_date"] = df.get("start_date", None)
            result["pub_date"] = df.get("pub_date", None)
            result["reason"] = df.get("reason", None)

            return result

    except Exception as e:
        logger.warning(f"[name_history] 获取 {code} 名称变更历史失败: {e}")

    return pd.DataFrame(columns=FinanceQuery.STK_NAME_HISTORY_SCHEMA)


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
    force_update: bool = False,
    use_duckdb: bool = True,
) -> RobustResult:
    """
    稳健版获取公司基本信息，返回 RobustResult。

    参数
    ----
    symbol      : 股票代码（单个或列表）
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
        return _get_company_info_batch_robust(symbol, force_update, use_duckdb)

    try:
        df = get_company_info(
            symbol,
            force_update=force_update,
            use_duckdb=use_duckdb,
        )

        if df is None or df.empty:
            jq_code = ak_code_to_jq(symbol)
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
    force_update: bool = False,
    use_duckdb: bool = True,
) -> RobustResult:
    """
    稳健版批量查询公司基本信息。

    参数
    ----
    symbols     : 股票代码列表
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    RobustResult
    """
    return get_company_info_robust(
        symbols,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )


def get_security_status_robust(
    symbol: Union[str, List[str]],
    date: str = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> RobustResult:
    """
    稳健版获取证券状态。

    参数
    ----
    symbol      : 股票代码
    date        : 查询日期
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
    force_update: bool = False,
    use_duckdb: bool = True,
) -> Dict[str, pd.DataFrame]:
    """
    批量获取公司信息，返回字典格式。

    参数
    ----
    securities  : 股票代码列表，如 ['600000.XSHG', '000001.XSHE']
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
        jq_code = ak_code_to_jq(security)
        try:
            df = get_company_info(
                security,
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
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取行业信息。

    参数
    ----
    security    : 股票代码，如 '600000.XSHG'
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
    jq_code = ak_code_to_jq(security)

    try:
        df_raw = _fetch_company_industry(extract_code_num(security))
        if df_raw is not None and not df_raw.empty:
            result = _normalize_industry_info(df_raw, jq_code)
            if not result.empty:
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


def get_management_info(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取上市公司管理人员任职情况。

    参数
    ----
    symbol      : 股票代码，支持 '600519.XSHG', '000001.XSHE' 等格式
    start_date  : 起始日期，格式 'YYYY-MM-DD'，可选
    end_date    : 结束日期，格式 'YYYY-MM-DD'，可选
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，字段：
    - code: 股票代码（聚宽格式）
    - name: 高管姓名
    - position: 职位
    - gender: 性别
    - education: 学历
    - start_date: 任职开始日期
    - end_date: 任职结束日期
    - shares_held: 持股数
    - compensation: 薪酬
    """
    jq_code = ak_code_to_jq(symbol)
    code_num = extract_code_num(symbol)

    if use_duckdb and _db_manager is not None and not force_update:
        df_cached = _db_manager.get_management_info(jq_code)
        if not df_cached.empty:
            result = df_cached
            if start_date:
                result = result[result["start_date"] >= start_date]
            if end_date:
                result = result[result["start_date"] <= end_date]
            return result

    try:
        import akshare as ak

        df = _retry_akshare_call(ak.stock_management_change_ths, symbol=code_num)
        if df is not None and not df.empty:
            result = _normalize_management_info(df, jq_code)
            if start_date:
                result = result[result["start_date"] >= start_date]
            if end_date:
                result = result[result["start_date"] <= end_date]
            if use_duckdb and _db_manager is not None and not result.empty:
                _db_manager.insert_management_info(result)
            return result
    except Exception as e:
        logger.warning(f"[management_info] 获取 {symbol} 管理人员信息失败: {e}")

    return pd.DataFrame(columns=_MANAGEMENT_INFO_SCHEMA)


def get_employee_info(
    symbol: str,
    year: Optional[int] = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取上市公司员工情况基本信息。

    参数
    ----
    symbol      : 股票代码，支持 '600519.XSHG', '000001.XSHE' 等格式
    year        : 查询年份，如 2023，可选（默认最新）
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，字段：
    - JQData标准字段: company_id, code, name, end_date, pub_date, employee,
      retirement, graduate_rate, college_rate, middle_rate
    - akshare详细字段: report_date, employee_count, professional_count,
      production_count, sales_count, finance_count, admin_count,
      education_bachelor, education_master, education_phd
    """
    jq_code = ak_code_to_jq(symbol)
    code_num = extract_code_num(symbol)

    if use_duckdb and _db_manager is not None and not force_update:
        df_cached = _db_manager.get_employee_info(jq_code)
        if not df_cached.empty:
            if year:
                df_cached = df_cached[
                    df_cached["end_date"].astype(str).str.startswith(str(year))
                    | df_cached["report_date"].astype(str).str.startswith(str(year))
                ]
            return df_cached

    try:
        import akshare as ak

        df = _retry_akshare_call(ak.stock_employee_info_em)
        if df is not None and not df.empty:
            result = _normalize_employee_info_v2(df, jq_code, code_num)
            if year:
                result = result[
                    result["end_date"].astype(str).str.startswith(str(year))
                    | result["report_date"].astype(str).str.startswith(str(year))
                ]
            if use_duckdb and _db_manager is not None and not result.empty:
                _db_manager.insert_employee_info(result)
            return result
    except Exception as e:
        logger.warning(f"[employee_info] 获取 {symbol} 员工信息失败: {e}")

    return pd.DataFrame(columns=_EMPLOYEE_INFO_SCHEMA)


def get_name_history(
    symbol: str,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取上市公司简称变更情况。

    参数
    ----
    symbol      : 股票代码，支持 '600519.XSHG', '000001.XSHE' 等格式
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，字段：
    - code: 股票代码（聚宽格式）
    - name: 历史名称
    - start_date: 使用开始日期
    - end_date: 使用结束日期
    - change_reason: 变更原因
    """
    jq_code = ak_code_to_jq(symbol)
    code_num = extract_code_num(symbol)

    if use_duckdb and _db_manager is not None and not force_update:
        df_cached = _db_manager.get_name_history(jq_code)
        if not df_cached.empty:
            return df_cached

    try:
        import akshare as ak

        df = _retry_akshare_call(ak.stock_info_change_name, symbol=code_num)
        if df is not None and not df.empty:
            result = _normalize_name_history(df, jq_code)
            if use_duckdb and _db_manager is not None and not result.empty:
                _db_manager.insert_name_history(result)
            return result
    except Exception as e:
        logger.warning(f"[name_history] 获取 {symbol} 名称变更历史失败: {e}")

    return pd.DataFrame(columns=_NAME_HISTORY_SCHEMA)


def _normalize_management_info(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    """标准化管理人员信息数据"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_MANAGEMENT_INFO_SCHEMA)

    result = pd.DataFrame()
    result["code"] = [jq_code] * len(df)

    col_map = {
        # JQData standard fields
        "董监高ID": "person_id",
        "人员ID": "person_id",
        "人员编号": "person_id",
        "职务类别ID": "title_class_id",
        "职务类别": "title_class",
        "职务": "title",
        "姓名": "name",
        "高管姓名": "name",
        "董监高姓名": "name",
        "变动人": "name",
        "职位": "position",
        "岗位": "position",
        "与公司高管关系": "position",
        "性别": "gender",
        "出生年份": "birth_year",
        "出生年月": "birth_year",
        "最高学历": "highest_degree",
        "学历": "highest_degree",
        "教育程度": "education",
        "文化程度": "education",
        "职务级别": "title_level",
        "职业资格证书": "profession_certificate",
        "国籍": "nationality",
        "简历": "resume",
        "个人简介": "resume",
        "任职起始日期": "start_date",
        "任职开始日期": "start_date",
        "上任日期": "start_date",
        "任职日期": "start_date",
        "变动日期": "start_date",
        "任职结束日期": "end_date",
        "离任日期": "end_date",
        "截止日期": "end_date",
        "离任日期": "leave_date",
        "解职日期": "leave_date",
        "离任原因": "leave_reason",
        "是否在职": "on_job",
        "在职状态": "on_job",
        "持股数": "shares_held",
        "持股数量": "shares_held",
        "期末持股数": "shares_held",
        "持股数量(股)": "shares_held",
        "剩余股数": "shares_held",
        "薪酬": "compensation",
        "报酬": "compensation",
        "年薪": "compensation",
        "从公司获得的税前报酬": "compensation",
        "交易均价": "compensation",
        "关系": "relationship",
        "直接持股": "direct_shares",
        "间接持股": "indirect_shares",
        "期权持股": "option_shares",
    }

    date_cols = {"start_date", "end_date", "leave_date"}
    num_cols = {
        "shares_held",
        "compensation",
        "birth_year",
        "direct_shares",
        "indirect_shares",
        "option_shares",
    }

    for src, target in col_map.items():
        if src in df.columns:
            if target in date_cols:
                result[target] = df[src].apply(_parse_date)
            elif target in num_cols:
                result[target] = pd.to_numeric(df[src], errors="coerce")
            else:
                result[target] = df[src]
        elif target not in result.columns:
            result[target] = None

    # Ensure all schema columns exist
    for col in _MANAGEMENT_INFO_SCHEMA:
        if col not in result.columns:
            result[col] = None

    return result[_MANAGEMENT_INFO_SCHEMA]


def _normalize_employee_info_v2(
    df: pd.DataFrame, jq_code: str, code_num: str
) -> pd.DataFrame:
    """标准化员工信息数据（支持 JQData 字段 + akshare 详细字段）"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_EMPLOYEE_INFO_SCHEMA)

    results = []
    for _, row in df.iterrows():
        record = {
            "company_id": None,
            "code": jq_code,
            "name": None,
            "end_date": None,
            "pub_date": None,
            "employee": None,
            "retirement": None,
            "graduate_rate": None,
            "college_rate": None,
            "middle_rate": None,
            "report_date": None,
            "employee_count": None,
            "professional_count": None,
            "production_count": None,
            "sales_count": None,
            "finance_count": None,
            "admin_count": None,
            "education_bachelor": None,
            "education_master": None,
            "education_phd": None,
        }

        # Map akshare columns
        col_map = {
            "股票代码": "code",
            "股票简称": "name",
            "公司名称": "name",
            "报告期": "end_date",
            "截止日期": "end_date",
            "发布日期": "pub_date",
            "公告日期": "pub_date",
            "员工总数": "employee",
            "员工人数": "employee",
            "employee_count": "employee",
            "退休人员": "retirement",
            "退休人数": "retirement",
            "本科及以上比例": "graduate_rate",
            "本科比例": "graduate_rate",
            "大专比例": "college_rate",
            "专科比例": "college_rate",
            "中专及以下比例": "middle_rate",
            "中专比例": "middle_rate",
            "专业人员数": "professional_count",
            "技术人员数": "professional_count",
            "研发人员数": "professional_count",
            "生产人员数": "production_count",
            "生产人员": "production_count",
            "操作人员": "production_count",
            "销售人员数": "sales_count",
            "销售人员": "sales_count",
            "营销人员": "sales_count",
            "财务人员数": "finance_count",
            "财务人员": "finance_count",
            "行政人员数": "admin_count",
            "行政人员": "admin_count",
            "管理人员": "admin_count",
            "本科人数": "education_bachelor",
            "大学本科": "education_bachelor",
            "本科学历": "education_bachelor",
            "硕士人数": "education_master",
            "硕士研究生": "education_master",
            "硕士学历": "education_master",
            "博士人数": "education_phd",
            "博士研究生": "education_phd",
            "博士学历": "education_phd",
        }

        for src, target in col_map.items():
            if src in df.columns:
                val = row.get(src)
                if val is not None and not pd.isna(val):
                    record[target] = val

        # Aliases for backward compatibility
        if record["employee"] is not None:
            record["employee_count"] = record["employee"]
        if record["end_date"] is not None:
            record["report_date"] = record["end_date"]

        results.append(record)

    if results:
        return pd.DataFrame(results)
    return pd.DataFrame(columns=_EMPLOYEE_INFO_SCHEMA)


def _normalize_employee_info(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    """标准化员工信息数据（旧版兼容）"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_EMPLOYEE_INFO_SCHEMA)

    results = []
    for _, row in df.iterrows():
        record = {"code": jq_code}

        report_date = None
        for col in ["报告期", "report_date", "日期", "统计日期", "截止日期"]:
            if col in df.columns:
                report_date = row.get(col)
                break
        record["report_date"] = report_date
        record["end_date"] = report_date

        employee_count = None
        for col in ["员工总数", "employee_count", "员工人数", "总人数"]:
            if col in df.columns:
                employee_count = row.get(col)
                break
        record["employee_count"] = employee_count
        record["employee"] = employee_count

        professional_count = None
        for col in ["专业人员数", "professional_count", "技术人员数", "研发人员数"]:
            if col in df.columns:
                professional_count = row.get(col)
                break
        record["professional_count"] = professional_count

        production_count = None
        for col in ["生产人员数", "production_count", "生产人员", "操作人员"]:
            if col in df.columns:
                production_count = row.get(col)
                break
        record["production_count"] = production_count

        sales_count = None
        for col in ["销售人员数", "sales_count", "销售人员", "营销人员"]:
            if col in df.columns:
                sales_count = row.get(col)
                break
        record["sales_count"] = sales_count

        finance_count = None
        for col in ["财务人员数", "finance_count", "财务人员"]:
            if col in df.columns:
                finance_count = row.get(col)
                break
        record["finance_count"] = finance_count

        admin_count = None
        for col in ["行政人员数", "admin_count", "行政人员", "管理人员"]:
            if col in df.columns:
                admin_count = row.get(col)
                break
        record["admin_count"] = admin_count

        education_bachelor = None
        for col in ["本科人数", "education_bachelor", "大学本科", "本科学历"]:
            if col in df.columns:
                education_bachelor = row.get(col)
                break
        record["education_bachelor"] = education_bachelor

        education_master = None
        for col in ["硕士人数", "education_master", "硕士研究生", "硕士学历"]:
            if col in df.columns:
                education_master = row.get(col)
                break
        record["education_master"] = education_master

        education_phd = None
        for col in ["博士人数", "education_phd", "博士研究生", "博士学历"]:
            if col in df.columns:
                education_phd = row.get(col)
                break
        record["education_phd"] = education_phd

        # Set JQData fields to None if not available
        for col in [
            "company_id",
            "name",
            "pub_date",
            "retirement",
            "graduate_rate",
            "college_rate",
            "middle_rate",
        ]:
            if col not in record:
                record[col] = None

        results.append(record)

    if results:
        return pd.DataFrame(results)
    return pd.DataFrame(columns=_EMPLOYEE_INFO_SCHEMA)


def _normalize_name_history(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    """标准化名称变更历史数据"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_NAME_HISTORY_SCHEMA)

    result = pd.DataFrame()

    name_col = None
    for col in ["股票简称", "简称", "名称", "new_name", "证券简称", "name"]:
        if col in df.columns:
            name_col = col
            break

    if name_col:
        result["name"] = df[name_col].values
    else:
        result["name"] = None

    start_date_col = None
    for col in ["变更日期", "start_date", "日期", "公告日期", "开始日期"]:
        if col in df.columns:
            start_date_col = col
            break
    result["start_date"] = df[start_date_col].values if start_date_col else None

    result["end_date"] = None

    reason_col = None
    for col in ["change_reason", "原因", "变更原因", "reason"]:
        if col in df.columns:
            reason_col = col
            break
    result["change_reason"] = df[reason_col].values if reason_col else None

    result.insert(0, "code", jq_code)

    return result


def prewarm_company_info_cache(
    securities: List[str] = None,
    max_workers: int = 5,
    use_duckdb: bool = True,
) -> Dict[str, bool]:
    """
    缓存预热机制：提前下载并缓存公司信息。

    参数
    ----
    securities  : 需要预热的股票代码列表，默认预热沪深300主要成分股
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


# 向后兼容导出
from jk2bt.utils.symbol import extract_code_num as _extract_code_num

CACHE_EXPIRE_DAYS = 90
from jk2bt.utils.symbol import ak_code_to_jq as _normalize_to_jq
