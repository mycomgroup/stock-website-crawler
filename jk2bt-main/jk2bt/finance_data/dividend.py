"""
finance_data/dividend.py
分红送股数据获取模块。

主要功能：
1. get_dividend_info() - 获取分红送股信息
2. get_dividend_history() - 获取历史分红记录
3. get_adjust_factor() - 计算复权因子
4. get_dividend_by_date() - 按报告期获取分红数据
5. calculate_ex_rights_price() - 计算除权价
6. get_stock_bonus() - 获取送股信息
7. finance.run_query 兼容接口（STK_XR_XD、STK_DIVIDEND_INFO）

数据字段：
- code: 股票代码（聚宽格式）
- board_plan_pub_date: 董事会预案公告日期
- bonus_ratio_rmb: 每股派息(元)
- transfer_ratio: 转增比例
- bonus_share_ratio: 送股比例
- ex_dividend_date: 除权除息日
- record_date: 股权登记日
- adjust_factor: 复权因子

缓存策略:
- DuckDB 缓存（优先）：存储在 data/dividend.db 中
- Pickle 缓存（备用）：按季度缓存（90天有效期）
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Union, Dict
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

_DIVIDEND_SCHEMA = [
    "code",
    "board_plan_pub_date",
    "bonus_ratio_rmb",
    "transfer_ratio",
    "bonus_share_ratio",
    "ex_dividend_date",
    "record_date",
    "pay_date",
    "report_date",
    "adjust_factor",
    "dividend_type",
    "company_name",
]

_DIVIDEND_HISTORY_SCHEMA = [
    "code",
    "year",
    "dividend_count",
    "total_dividend",
    "avg_dividend",
    "max_dividend",
    "min_dividend",
]


class DividendDBManager:
    """分红送股 DuckDB 管理器"""

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
            db_path = os.path.join(base_dir, "data", "dividend.db")

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
                    CREATE TABLE IF NOT EXISTS dividend (
                        code VARCHAR NOT NULL,
                        board_plan_pub_date DATE,
                        bonus_ratio_rmb DOUBLE,
                        transfer_ratio DOUBLE,
                        bonus_share_ratio DOUBLE,
                        ex_dividend_date DATE,
                        record_date DATE,
                        pay_date DATE,
                        report_date VARCHAR,
                        adjust_factor DOUBLE,
                        dividend_type VARCHAR,
                        company_name VARCHAR,
                        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (code, ex_dividend_date)
                    )
                """)
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_div_code ON dividend(code)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_div_date ON dividend(ex_dividend_date)"
                )
                logger.info("分红送股表结构初始化完成")
        except Exception as e:
            logger.warning(f"初始化表结构失败: {e}")

    def insert_dividend(self, df: pd.DataFrame):
        if self._manager is None or df.empty:
            return

        df = df.copy()
        for col in _DIVIDEND_SCHEMA:
            if col not in df.columns:
                df[col] = None

        if "update_time" not in df.columns:
            df["update_time"] = datetime.now()

        cols = _DIVIDEND_SCHEMA + ["update_time"]
        df = df[cols]

        try:
            with self._manager._get_connection(read_only=False) as conn:
                conn.execute("INSERT OR REPLACE INTO dividend SELECT * FROM df")
                logger.info(f"插入/更新 {len(df)} 条分红送股信息")
        except Exception as e:
            logger.warning(f"插入分红送股信息失败: {e}")

    def get_dividend(
        self, code: str, start_date: str = None, end_date: str = None
    ) -> pd.DataFrame:
        if self._manager is None:
            return pd.DataFrame(columns=_DIVIDEND_SCHEMA)

        try:
            with self._manager._get_connection(read_only=True) as conn:
                if start_date and end_date:
                    df = conn.execute(
                        "SELECT * FROM dividend WHERE code = ? AND ex_dividend_date >= ? AND ex_dividend_date <= ? ORDER BY ex_dividend_date DESC",
                        [code, start_date, end_date],
                    ).fetchdf()
                else:
                    df = conn.execute(
                        "SELECT * FROM dividend WHERE code = ? ORDER BY ex_dividend_date DESC",
                        [code],
                    ).fetchdf()
                return df
        except Exception as e:
            logger.warning(f"查询分红送股信息失败: {e}")
            return pd.DataFrame(columns=_DIVIDEND_SCHEMA)

    def is_cache_valid(self, code: str, cache_days: int = 90) -> bool:
        if self._manager is None:
            return False

        try:
            with self._manager._get_connection(read_only=True) as conn:
                result = conn.execute(
                    "SELECT MAX(update_time) FROM dividend WHERE code = ?",
                    [code],
                ).fetchone()
                if result and result[0]:
                    update_time = pd.to_datetime(result[0])
                    return (datetime.now() - update_time).days < cache_days
                return False
        except Exception:
            return False


_db_manager = DividendDBManager() if _DUCKDB_AVAILABLE else None


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


def _parse_ratio(value) -> Optional[float]:
    if value is None or value == "" or value == "-":
        return None
    try:
        if isinstance(value, str):
            value = value.replace("%", "").strip()
        return float(value)
    except (ValueError, TypeError):
        return None


def _calculate_adjust_factor(
    bonus_ratio_rmb: float, transfer_ratio: float, bonus_share_ratio: float
) -> float:
    bonus = bonus_ratio_rmb or 0
    transfer = transfer_ratio or 0
    bonus_share = bonus_share_ratio or 0

    denominator = 1 + transfer / 10 + bonus_share / 10
    numerator = 1 - bonus / 10

    if denominator <= 0:
        return 1.0

    return numerator / denominator


def get_dividend_info(
    security: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取分红送股信息。

    参数
    ----
    security      : 股票代码
    start_date    : 起始日期（除权除息日）
    end_date      : 结束日期
    cache_dir     : 缓存目录
    force_update  : 强制更新
    use_duckdb    : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，标准化字段：
    - code: 股票代码（聚宽格式）
    - board_plan_pub_date: 董事会预案公告日期
    - bonus_ratio_rmb: 每股派息(元)
    - transfer_ratio: 转增比例
    - bonus_share_ratio: 送股比例
    - ex_dividend_date: 除权除息日
    - record_date: 股权登记日
    - adjust_factor: 复权因子
    """
    code_num = _extract_code_num(security)
    jq_code = _normalize_to_jq(security)

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(jq_code, cache_days=90):
            df_cached = _db_manager.get_dividend(jq_code, start_date, end_date)
            if not df_cached.empty:
                return df_cached[_DIVIDEND_SCHEMA]

    cache_file = os.path.join(cache_dir, f"dividend_{code_num}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 90:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_dividend(cached_df)
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
                df_fhps = ak.stock_fhps_em(symbol=code_num)
                if df_fhps is not None and not df_fhps.empty:
                    for _, row in df_fhps.iterrows():
                        record = _parse_fhps_row(row, jq_code)
                        if record:
                            results.append(record)
            except Exception as e:
                logger.debug(f"stock_fhps_em 失败: {e}")

            try:
                df_dividend = ak.stock_dividend_cninfo(symbol=code_num)
                if df_dividend is not None and not df_dividend.empty:
                    for _, row in df_dividend.iterrows():
                        record = _parse_dividend_row(row, jq_code)
                        if record:
                            results.append(record)
            except Exception as e:
                logger.debug(f"stock_dividend_cninfo 失败: {e}")

            if results:
                result_df = pd.DataFrame(results)
                result_df = result_df.drop_duplicates(
                    subset=["code", "ex_dividend_date"], keep="first"
                )
                result_df = result_df.sort_values("ex_dividend_date", ascending=False)
                result_df.to_pickle(cache_file)
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_dividend(result_df)
                if start_date is None and end_date is None:
                    return result_df
                return _filter_by_date_range(result_df, start_date, end_date)

        except Exception as e:
            logger.warning(f"[get_dividend_info] 获取分红送股失败 {security}: {e}")

    return pd.DataFrame(columns=_DIVIDEND_SCHEMA)


def _parse_fhps_row(row, jq_code: str) -> Optional[dict]:
    try:
        bonus_ratio_rmb = _parse_ratio(row.get("每股派息", 0))
        transfer_ratio = _parse_ratio(row.get("每股转增", 0))
        bonus_share_ratio = _parse_ratio(row.get("每股送股", 0))

        adjust_factor = _calculate_adjust_factor(
            bonus_ratio_rmb, transfer_ratio, bonus_share_ratio
        )

        return {
            "code": jq_code,
            "board_plan_pub_date": _parse_date(row.get("董事会预案公告日期", None)),
            "bonus_ratio_rmb": bonus_ratio_rmb,
            "transfer_ratio": transfer_ratio,
            "bonus_share_ratio": bonus_share_ratio,
            "ex_dividend_date": _parse_date(row.get("除权除息日", None)),
            "record_date": _parse_date(row.get("股权登记日", None)),
            "pay_date": _parse_date(row.get("派息日", None)),
            "report_date": _parse_date(row.get("报告期", None)),
            "adjust_factor": adjust_factor,
            "dividend_type": str(row.get("分红类型", "")),
            "company_name": str(row.get("公司名称", "")),
        }
    except Exception:
        return None


def _parse_dividend_row(row, jq_code: str) -> Optional[dict]:
    try:
        bonus_ratio_rmb = _parse_ratio(row.get("派息", 0))
        transfer_ratio = _parse_ratio(row.get("转增", 0))
        bonus_share_ratio = _parse_ratio(row.get("送股", 0))

        adjust_factor = _calculate_adjust_factor(
            bonus_ratio_rmb, transfer_ratio, bonus_share_ratio
        )

        return {
            "code": jq_code,
            "board_plan_pub_date": _parse_date(row.get("公告日期", None)),
            "bonus_ratio_rmb": bonus_ratio_rmb,
            "transfer_ratio": transfer_ratio,
            "bonus_share_ratio": bonus_share_ratio,
            "ex_dividend_date": _parse_date(row.get("除权日", None)),
            "record_date": _parse_date(row.get("登记日", None)),
            "pay_date": _parse_date(row.get("派息日", None)),
            "report_date": _parse_date(row.get("实施日期", None)),
            "adjust_factor": adjust_factor,
            "dividend_type": str(row.get("分红类型", "")),
            "company_name": str(row.get("公司名称", "")),
        }
    except Exception:
        return None


def _filter_by_date_range(
    df: pd.DataFrame, start_date: str, end_date: str
) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()

    if "ex_dividend_date" not in df.columns:
        return df

    df["_date"] = pd.to_datetime(df["ex_dividend_date"])

    if start_date:
        start_dt = pd.Timestamp(start_date)
        df = df[df["_date"] >= start_dt]

    if end_date:
        end_dt = pd.Timestamp(end_date)
        df = df[df["_date"] <= end_dt]

    return df.drop(columns=["_date"]).reset_index(drop=True)


def get_dividend_history(
    security: str,
    years: int = 5,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取历史分红记录。

    参数
    ----
    security      : 股票代码
    years         : 查询年数
    cache_dir     : 缓存目录
    force_update  : 强制更新

    返回
    ----
    pandas DataFrame，包含年度分红统计：
    - code: 股票代码（聚宽格式）
    - year: 年度
    - dividend_count: 分红次数
    - total_dividend: 年度总分红金额（每股）
    - avg_dividend: 平均每股分红
    - max_dividend: 最大每股分红
    - min_dividend: 最小每股分红
    """
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=years * 365)).strftime("%Y-%m-%d")

    df_dividend = get_dividend_info(
        security,
        start_date=start_date,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
    )

    if df_dividend.empty:
        return pd.DataFrame(columns=_DIVIDEND_HISTORY_SCHEMA)

    jq_code = _normalize_to_jq(security)

    df_dividend["_year"] = pd.to_datetime(df_dividend["ex_dividend_date"]).dt.year

    yearly_stats = []
    for year, group in df_dividend.groupby("_year"):
        bonus_values = group["bonus_ratio_rmb"].dropna()
        yearly_stats.append(
            {
                "code": jq_code,
                "year": int(year),
                "dividend_count": len(group),
                "total_dividend": bonus_values.sum() if len(bonus_values) > 0 else 0,
                "avg_dividend": bonus_values.mean() if len(bonus_values) > 0 else 0,
                "max_dividend": bonus_values.max() if len(bonus_values) > 0 else 0,
                "min_dividend": bonus_values.min() if len(bonus_values) > 0 else 0,
            }
        )

    if yearly_stats:
        return pd.DataFrame(yearly_stats).sort_values("year", ascending=False)

    return pd.DataFrame(columns=_DIVIDEND_HISTORY_SCHEMA)


def calculate_ex_rights_price(
    price: float,
    dividend_info: Union[Dict, pd.DataFrame, pd.Series],
) -> float:
    """
    计算除权价。

    参数
    ----
    price         : 原价（收盘价）
    dividend_info : 分红信息（字典、DataFrame 或 Series）

    返回
    ----
    float - 除权价

    公式
    ----
    除权价 = (原价 - 每股派息) / (1 + 每股送股 + 每股转增)
    """
    if price <= 0:
        return price

    bonus_ratio_rmb = 0
    bonus_share_ratio = 0
    transfer_ratio = 0

    if isinstance(dividend_info, dict):
        bonus_ratio_rmb = dividend_info.get("bonus_ratio_rmb", 0) or 0
        bonus_share_ratio = dividend_info.get("bonus_share_ratio", 0) or 0
        transfer_ratio = dividend_info.get("transfer_ratio", 0) or 0
    elif isinstance(dividend_info, pd.DataFrame):
        if not dividend_info.empty:
            row = dividend_info.iloc[0]
            bonus_ratio_rmb = row.get("bonus_ratio_rmb", 0) or 0
            bonus_share_ratio = row.get("bonus_share_ratio", 0) or 0
            transfer_ratio = row.get("transfer_ratio", 0) or 0
    elif isinstance(dividend_info, pd.Series):
        bonus_ratio_rmb = dividend_info.get("bonus_ratio_rmb", 0) or 0
        bonus_share_ratio = dividend_info.get("bonus_share_ratio", 0) or 0
        transfer_ratio = dividend_info.get("transfer_ratio", 0) or 0

    denominator = 1 + bonus_share_ratio / 10 + transfer_ratio / 10

    if denominator <= 0:
        return price

    ex_rights_price = (price - bonus_ratio_rmb / 10) / denominator

    return max(0, ex_rights_price)


def get_stock_bonus(
    security: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取送股信息。

    参数
    ----
    security      : 股票代码
    cache_dir     : 缓存目录
    force_update  : 强制更新

    返回
    ----
    pandas DataFrame，包含送股方案：
    - code: 股票代码
    - bonus_share_ratio: 送股比例
    - transfer_ratio: 转增比例
    - ex_dividend_date: 除权除息日
    - report_date: 报告期
    """
    df_dividend = get_dividend_info(
        security,
        cache_dir=cache_dir,
        force_update=force_update,
    )

    if df_dividend.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "bonus_share_ratio",
                "transfer_ratio",
                "ex_dividend_date",
                "report_date",
            ]
        )

    bonus_records = df_dividend[
        (
            df_dividend["bonus_share_ratio"].notna()
            & (df_dividend["bonus_share_ratio"] > 0)
        )
        | (df_dividend["transfer_ratio"].notna() & (df_dividend["transfer_ratio"] > 0))
    ].copy()

    return bonus_records[
        [
            "code",
            "bonus_share_ratio",
            "transfer_ratio",
            "ex_dividend_date",
            "report_date",
        ]
    ]


_RIGHTS_ISSUE_SCHEMA = [
    "code",
    "ex_dividend_date",
    "bonus_ratio_rmb",
    "bonus_share_ratio",
    "transfer_ratio",
    "record_date",
    "rights_issue_ratio",
]
_NEXT_DIVIDEND_SCHEMA = [
    "code",
    "report_date",
    "bonus_ratio_rmb",
    "bonus_share_ratio",
    "transfer_ratio",
    "ex_dividend_date",
    "board_plan_pub_date",
]
_ADJUST_FACTOR_SCHEMA = [
    "code",
    "ex_dividend_date",
    "adjust_factor",
    "bonus_ratio_rmb",
    "bonus_share_ratio",
    "transfer_ratio",
]


def get_adjust_factor(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取复权因子。

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
    pandas DataFrame，包含复权因子：
    - code: 股票代码
    - ex_dividend_date: 除权除息日
    - adjust_factor: 复权因子
    - bonus_ratio_rmb: 每股派息(元)
    - bonus_share_ratio: 送股比例
    - transfer_ratio: 转增比例
    """
    df = get_dividend_info(
        symbol,
        start_date=start_date,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )

    if df.empty:
        return pd.DataFrame(columns=_ADJUST_FACTOR_SCHEMA)

    result = pd.DataFrame()
    result["code"] = df["code"]
    result["ex_dividend_date"] = df["ex_dividend_date"]

    bonus_ratio_rmb = df.get("bonus_ratio_rmb", pd.Series([0] * len(df)))
    bonus_share_ratio = df.get("bonus_share_ratio", pd.Series([0] * len(df)))
    transfer_ratio = df.get("transfer_ratio", pd.Series([0] * len(df)))

    bonus_ratio_rmb = pd.to_numeric(bonus_ratio_rmb, errors="coerce").fillna(0)
    bonus_share_ratio = pd.to_numeric(bonus_share_ratio, errors="coerce").fillna(0)
    transfer_ratio = pd.to_numeric(transfer_ratio, errors="coerce").fillna(0)

    bonus_per_share = bonus_ratio_rmb / 10.0
    bonus_share_per_share = bonus_share_ratio / 10.0
    transfer_per_share = transfer_ratio / 10.0

    total_adjustment = bonus_share_per_share + transfer_per_share

    denominator = 1.0 + total_adjustment
    numerator = 1.0 - bonus_per_share

    result["adjust_factor"] = numerator / denominator
    result.loc[total_adjustment == 0, "adjust_factor"] = 1.0 - bonus_per_share

    result["bonus_ratio_rmb"] = bonus_ratio_rmb
    result["bonus_share_ratio"] = bonus_share_ratio
    result["transfer_ratio"] = transfer_ratio

    return result


def get_dividend_by_date(
    report_date: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    按报告期获取分红数据。

    参数
    ----
    report_date   : 报告期（如 '20231231'）
    cache_dir     : 缓存目录
    force_update  : 强制更新

    返回
    ----
    pandas DataFrame，包含该报告期的所有分红信息：
    - code: 股票代码
    - company_name: 公司名称
    - bonus_ratio_rmb: 每股派息
    - transfer_ratio: 转增比例
    - bonus_share_ratio: 送股比例
    - ex_dividend_date: 除权除息日
    """
    cache_file = os.path.join(cache_dir, f"dividend_report_{report_date}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            cached_df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days < 365:
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
            df_raw = ak.stock_fhps_em(date=report_date)
            if df_raw is not None and not df_raw.empty:
                results = []
                for _, row in df_raw.iterrows():
                    code_num = _extract_code_num(str(row.get("代码", "")))
                    jq_code = _normalize_to_jq(code_num)

                    bonus_ratio_rmb = _parse_ratio(row.get("现金分红-现金分红比例", 0))
                    transfer_ratio = _parse_ratio(row.get("送转股份-转股比例", 0))
                    bonus_share_ratio = _parse_ratio(row.get("送转股份-送转比例", 0))
                    adjust_factor = _calculate_adjust_factor(
                        bonus_ratio_rmb, transfer_ratio, bonus_share_ratio
                    )

                    results.append(
                        {
                            "code": jq_code,
                            "company_name": str(row.get("名称", "")),
                            "bonus_ratio_rmb": bonus_ratio_rmb,
                            "transfer_ratio": transfer_ratio,
                            "bonus_share_ratio": bonus_share_ratio,
                            "ex_dividend_date": _parse_date(
                                row.get("除权除息日", None)
                            ),
                            "board_plan_pub_date": _parse_date(
                                row.get("预案公告日", None)
                            ),
                            "record_date": _parse_date(row.get("股权登记日", None)),
                            "report_date": report_date,
                            "adjust_factor": adjust_factor,
                        }
                    )

                if results:
                    result_df = pd.DataFrame(results)
                    result_df.to_pickle(cache_file)
                    return result_df
        except Exception as e:
            logger.warning(
                f"[get_dividend_by_date] 获取报告期分红数据失败 {report_date}: {e}"
            )

    return pd.DataFrame(columns=_DIVIDEND_SCHEMA)


def query_dividend(
    symbols: List[str],
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    批量查询分红送股（finance.STK_XR_XD）。

    参数
    ----
    symbols       : 股票代码列表
    start_date    : 起始日期
    end_date      : 结束日期
    cache_dir     : 缓存目录
    force_update  : 强制更新
    use_duckdb    : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，每条分红记录
    """
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_DIVIDEND_SCHEMA)

    dfs = []
    for symbol in symbols:
        try:
            df = get_dividend_info(
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
            logger.warning(f"[query_dividend] 获取 {symbol} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_DIVIDEND_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


class FinanceQuery:
    """
    聚宽 finance 模块模拟器。
    提供 finance.run_query 兼容的查询接口。
    """

    class STK_XR_XD:
        code = None
        board_plan_pub_date = None
        bonus_ratio_rmb = None
        transfer_ratio = None
        bonus_share_ratio = None
        ex_dividend_date = None
        record_date = None
        pay_date = None
        report_date = None
        adjust_factor = None
        dividend_type = None
        company_name = None

    class STK_DIVIDEND_INFO:
        code = None
        board_plan_pub_date = None
        bonus_ratio_rmb = None
        transfer_ratio = None
        bonus_share_ratio = None
        ex_dividend_date = None
        record_date = None
        pay_date = None
        report_date = None
        adjust_factor = None
        dividend_type = None
        company_name = None

    class STK_DIVIDEND_RIGHT:
        code = None
        pub_date = None
        ex_dividend_date = None
        bonus_per_share = None
        bonus_per_share_taxed = None
        transfer_per_share = None
        rights_issue_per_share = None
        rights_issue_price = None
        bonus_amount = None

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

        if table_name in ("STK_XR_XD", "STK_DIVIDEND_INFO"):
            if "code" in conditions:
                return get_dividend_info(
                    conditions["code"], cache_dir=cache_dir, use_duckdb=use_duckdb
                )
            return pd.DataFrame(columns=_DIVIDEND_SCHEMA)
        elif table_name == "STK_DIVIDEND_RIGHT":
            if "code" in conditions:
                df = get_dividend_info(
                    conditions["code"], cache_dir=cache_dir, use_duckdb=use_duckdb
                )
                return _convert_to_dividend_right(df)
            return pd.DataFrame(columns=_DIVIDEND_SCHEMA)
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
    if table in ("STK_XR_XD", "STK_DIVIDEND_INFO"):
        if code:
            return get_dividend_info(
                code, cache_dir=cache_dir, force_update=force_update
            )
        return pd.DataFrame(columns=_DIVIDEND_SCHEMA)
    elif table == "STK_DIVIDEND_RIGHT":
        if code:
            df = get_dividend_info(code, cache_dir=cache_dir, force_update=force_update)
            return _convert_to_dividend_right(df)
        return pd.DataFrame(columns=_DIVIDEND_SCHEMA)
    else:
        raise ValueError(f"不支持的表: {table}")


def get_dividend(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """获取分红送股数据（兼容旧接口）"""
    return get_dividend_info(
        symbol,
        start_date=start_date,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )


def get_rights_issue(
    symbol: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取配股信息。

    参数
    ----
    symbol      : 股票代码
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，包含配股方案：
    - code: 股票代码
    - ex_dividend_date: 除权除息日
    - bonus_ratio_rmb: 每股派息(元)
    - bonus_share_ratio: 送股比例
    - transfer_ratio: 转增比例
    - record_date: 股权登记日
    - rights_issue_ratio: 配股比例（暂不支持）
    """
    df = get_dividend_info(
        symbol, cache_dir=cache_dir, force_update=force_update, use_duckdb=use_duckdb
    )

    if df.empty:
        return pd.DataFrame(columns=_RIGHTS_ISSUE_SCHEMA)

    bonus_ratio_rmb_col = df.get("bonus_ratio_rmb", pd.Series([None] * len(df)))
    bonus_share_ratio_col = df.get("bonus_share_ratio", pd.Series([None] * len(df)))
    transfer_ratio_col = df.get("transfer_ratio", pd.Series([None] * len(df)))

    bonus_ratio_rmb_col = pd.to_numeric(bonus_ratio_rmb_col, errors="coerce")
    bonus_share_ratio_col = pd.to_numeric(bonus_share_ratio_col, errors="coerce")
    transfer_ratio_col = pd.to_numeric(transfer_ratio_col, errors="coerce")

    has_rights = (
        (bonus_ratio_rmb_col.notna() & (bonus_ratio_rmb_col > 0))
        | (bonus_share_ratio_col.notna() & (bonus_share_ratio_col > 0))
        | (transfer_ratio_col.notna() & (transfer_ratio_col > 0))
    )

    rights_df = df[has_rights].copy()

    if rights_df.empty:
        return pd.DataFrame(columns=_RIGHTS_ISSUE_SCHEMA)

    result = pd.DataFrame()
    result["code"] = rights_df["code"]
    result["ex_dividend_date"] = rights_df["ex_dividend_date"]
    result["bonus_ratio_rmb"] = bonus_ratio_rmb_col[has_rights]
    result["bonus_share_ratio"] = bonus_share_ratio_col[has_rights]
    result["transfer_ratio"] = transfer_ratio_col[has_rights]
    result["record_date"] = rights_df.get("record_date", None)
    result["rights_issue_ratio"] = None

    return result


def get_next_dividend(
    symbol: str,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取下次分红信息（已公告但未实施的分红）。

    参数
    ----
    symbol      : 股票代码
    cache_dir   : 缓存目录
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，包含下次分红信息：
    - code: 股票代码
    - report_date: 报告期
    - bonus_ratio_rmb: 每股派息(元)
    - bonus_share_ratio: 送股比例
    - transfer_ratio: 转增比例
    - ex_dividend_date: 除权除息日
    - board_plan_pub_date: 董事会预案公告日期
    """
    df = get_dividend_info(
        symbol, cache_dir=cache_dir, force_update=force_update, use_duckdb=use_duckdb
    )

    if df.empty:
        return pd.DataFrame(columns=_NEXT_DIVIDEND_SCHEMA)

    today = datetime.now()

    df_future = df[
        (df["ex_dividend_date"].isna())
        | (
            pd.to_datetime(df["ex_dividend_date"], errors="coerce")
            > pd.Timestamp(today)
        )
    ]

    if df_future.empty:
        return pd.DataFrame(columns=_NEXT_DIVIDEND_SCHEMA)

    df_future = df_future.sort_values(
        "board_plan_pub_date", ascending=False, na_position="last"
    )

    result = pd.DataFrame()
    row = df_future.iloc[0]
    result["code"] = [row.get("code", None)]
    result["report_date"] = [row.get("report_date", None)]
    result["bonus_ratio_rmb"] = [row.get("bonus_ratio_rmb", None)]
    result["bonus_share_ratio"] = [row.get("bonus_share_ratio", None)]
    result["transfer_ratio"] = [row.get("transfer_ratio", None)]
    result["ex_dividend_date"] = [row.get("ex_dividend_date", None)]
    result["board_plan_pub_date"] = [row.get("board_plan_pub_date", None)]

    return result


def query_dividend_right(
    symbols: List[str],
    start_date: str = None,
    end_date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """批量查询分红权利信息"""
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_DIVIDEND_SCHEMA)

    dfs = []
    for symbol in symbols:
        try:
            df = get_dividend_info(
                symbol,
                start_date=start_date,
                end_date=end_date,
                cache_dir=cache_dir,
                force_update=force_update,
                use_duckdb=use_duckdb,
            )
            if not df.empty:
                right_df = _convert_to_dividend_right(df)
                if not right_df.empty:
                    dfs.append(right_df)
        except Exception as e:
            logger.warning(f"[query_dividend_right] 获取 {symbol} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_DIVIDEND_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


def _convert_to_dividend_right(df: pd.DataFrame) -> pd.DataFrame:
    """将分红信息转换为分红权利格式"""
    result = pd.DataFrame()
    result["code"] = df["code"]
    result["pub_date"] = df["report_date"]
    result["ex_dividend_date"] = df["ex_dividend_date"]

    if "bonus_ratio_rmb" in df.columns:
        result["bonus_per_share"] = df["bonus_ratio_rmb"]
        result["bonus_per_share_taxed"] = result["bonus_per_share"] * 0.9
    else:
        result["bonus_per_share"] = None
        result["bonus_per_share_taxed"] = None

    if "transfer_ratio" in df.columns:
        result["transfer_per_share"] = df["transfer_ratio"] / 10.0
    else:
        result["transfer_per_share"] = None

    if "bonus_share_ratio" in df.columns:
        result["rights_issue_per_share"] = df["bonus_share_ratio"] / 10.0
    else:
        result["rights_issue_per_share"] = None

    result["rights_issue_price"] = None
    result["bonus_amount"] = df.get("bonus_ratio_rmb", None)

    return result


def calculate_adjust_price(
    symbol: str,
    original_price: float,
    adjust_type: str = "qfq",
    date: str = None,
    cache_dir: str = "finance_cache",
    force_update: bool = False,
) -> float:
    """计算复权价格"""
    df = get_dividend_info(symbol, cache_dir=cache_dir, force_update=force_update)

    if df.empty:
        return original_price

    df = df[df["ex_dividend_date"].notna()]
    if df.empty:
        return original_price

    df["date"] = pd.to_datetime(df["ex_dividend_date"])
    df = df.sort_values("date")

    if date:
        df = df[pd.to_datetime(df["date"]) <= pd.Timestamp(date)]

    if df.empty:
        return original_price

    cumulative_factor = 1.0

    for _, row in df.iterrows():
        bonus_share = row.get("bonus_share_ratio", 0) or 0
        transfer = row.get("transfer_ratio", 0) or 0

        bonus_per_share = bonus_share / 10.0
        transfer_per_share = transfer / 10.0

        adjustment = bonus_per_share + transfer_per_share

        if adjustment > 0:
            if adjust_type == "qfq":
                cumulative_factor = cumulative_factor / (1.0 + adjustment)
            else:
                cumulative_factor = cumulative_factor * (1.0 + adjustment)

    return original_price * cumulative_factor
