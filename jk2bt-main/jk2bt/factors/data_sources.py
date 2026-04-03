"""
factors/data_sources.py
多数据源管理模块。

支持数据源：
1. AkShare（主数据源）
   - stock_zh_valuation_baidu: 百度估值数据
   - stock_a_lg_indicator: 东财估值数据
   - stock_zh_a_spot_em: 实时行情数据
2. 东财数据源（备用）
   - 通过 AkShare 封装东财接口
3. 同花顺数据源（备用）
   - 通过 AkShare 封装同花顺接口

功能：
- 数据源优先级管理
- 自动切换备用数据源
- 数据质量检查
- 异常处理和重试机制
"""

import os
import time
import warnings
import functools
from typing import Dict, List, Optional, Union, Callable
from enum import Enum
import pandas as pd
import numpy as np

try:
    from ..utils.date_utils import find_date_column
except ImportError:
    from utils.date_utils import find_date_column

# =====================================================================
# 底层数据源实现模块
# 注意：本模块是数据源的底层实现，直接使用 akshare 作为数据获取引擎。
# 其他上层模块（如 factors/valuation.py, factors/technical.py）应优先使用
# market_data 或 finance_data 模块，而不是直接依赖此模块的 akshare 导入。
# =====================================================================

try:
    import akshare as ak
except ImportError:
    raise ImportError("请安装 akshare: pip install akshare")


class DataSource(Enum):
    BAIDU = "baidu"
    EASTMONEY = "eastmoney"
    THS = "ths"
    AKSHARE_DEFAULT = "akshare"


DATA_SOURCE_PRIORITY = [
    DataSource.BAIDU,
    DataSource.EASTMONEY,
    DataSource.THS,
]


class DataQualityError(Exception):
    """数据质量异常"""

    pass


class DataSourceError(Exception):
    """数据源异常"""

    pass


def validate_valuation_data(
    df: pd.DataFrame,
    symbol: str,
    strict: bool = False,
) -> Dict[str, Union[bool, str, List[str]]]:
    """
    验证估值数据质量。

    Parameters
    ----------
    df : pd.DataFrame
        估值数据表
    symbol : str
        证券代码
    strict : bool
        是否严格模式（严格模式下空数据会抛异常）

    Returns
    -------
    dict
        包含 is_valid, message, issues 等字段
    """
    result = {
        "is_valid": True,
        "message": "",
        "issues": [],
        "missing_rate": {},
        "data_count": 0,
    }

    if df is None or df.empty:
        result["is_valid"] = False
        result["message"] = f"{symbol}: 数据为空"
        result["issues"].append("empty_data")
        if strict:
            raise DataQualityError(result["message"])
        return result

    result["data_count"] = len(df)

    required_cols = ["date", "market_cap", "pe_ratio", "pb_ratio"]
    optional_cols = ["circulating_market_cap", "ps_ratio"]

    for col in required_cols:
        if col not in df.columns:
            result["issues"].append(f"missing_col_{col}")
            result["is_valid"] = False

    for col in df.columns:
        if col != "date":
            missing_count = df[col].isna().sum()
            missing_rate = missing_count / len(df)
            result["missing_rate"][col] = missing_rate
            if missing_rate > 0.5:
                result["issues"].append(f"high_missing_{col}")
                result["is_valid"] = False

    if "pe_ratio" in df.columns:
        pe = df["pe_ratio"].dropna()
        if len(pe) > 0:
            if (pe < 0).any():
                result["issues"].append("negative_pe")
            if (pe > 1000).any():
                result["issues"].append("extreme_pe")

    if "pb_ratio" in df.columns:
        pb = df["pb_ratio"].dropna()
        if len(pb) > 0:
            if (pb < -10).any() or (pb > 100).any():
                result["issues"].append("extreme_pb")

    if "market_cap" in df.columns:
        mc = df["market_cap"].dropna()
        if len(mc) > 0:
            if (mc <= 0).any():
                result["issues"].append("invalid_market_cap")

    if result["issues"]:
        result["message"] = f"{symbol}: 发现 {len(result['issues'])} 个问题"
        if strict and not result["is_valid"]:
            raise DataQualityError(result["message"])

    return result


def validate_turnover_data(
    df: pd.DataFrame,
    symbol: str,
    strict: bool = False,
) -> Dict[str, Union[bool, str, List[str]]]:
    """
    验证换手率数据质量。

    Parameters
    ----------
    df : pd.DataFrame
        换手率数据表
    symbol : str
        证券代码
    strict : bool
        是否严格模式

    Returns
    -------
    dict
        包含 is_valid, message, issues 等字段
    """
    result = {
        "is_valid": True,
        "message": "",
        "issues": [],
        "missing_rate": {},
        "data_count": 0,
    }

    if df is None or df.empty:
        result["is_valid"] = False
        result["message"] = f"{symbol}: 换手率数据为空"
        result["issues"].append("empty_data")
        if strict:
            raise DataQualityError(result["message"])
        return result

    result["data_count"] = len(df)

    if "turnover_rate" in df.columns:
        turnover = df["turnover_rate"].dropna()
        if len(turnover) > 0:
            if (turnover < 0).any():
                result["issues"].append("negative_turnover")
            if (turnover > 1).any():
                result["issues"].append("turnover_over_100")
            missing_rate = df["turnover_rate"].isna().sum() / len(df)
            result["missing_rate"]["turnover_rate"] = missing_rate
            if missing_rate > 0.3:
                result["issues"].append("high_missing_turnover")
                result["is_valid"] = False

    if result["issues"]:
        result["message"] = f"{symbol}: 发现 {len(result['issues'])} 个问题"

    return result


def retry_on_failure(
    max_retries: int = 3,
    retry_delay: float = 1.0,
    exceptions: tuple = (Exception,),
):
    """
    重试装饰器。

    Parameters
    ----------
    max_retries : int
        最大重试次数
    retry_delay : float
        重试间隔（秒）
    exceptions : tuple
        需要重试的异常类型
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay * (attempt + 1))
                        warnings.warn(
                            f"{func.__name__} 第 {attempt + 1} 次尝试失败: {e}, 正在重试..."
                        )
            raise DataSourceError(
                f"{func.__name__} 重试 {max_retries} 次后仍失败: {last_exception}"
            )

        return wrapper

    return decorator


def normalize_symbol(symbol: str) -> str:
    """
    标准化证券代码格式。

    Parameters
    ----------
    symbol : str
        原始代码，如 'sh600519', '600519.XSHG'

    Returns
    -------
    str
        6位数字代码，如 '600519'
    """
    ak_sym = symbol
    if symbol.startswith("sh") or symbol.startswith("sz"):
        ak_sym = symbol[2:]
    if symbol.endswith(".XSHG") or symbol.endswith(".XSHE"):
        ak_sym = symbol[:6]
    return ak_sym.zfill(6)


class ValuationDataSource:
    """估值数据源管理器"""

    def __init__(self, cache_dir: str = "stock_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, symbol: str, source: DataSource) -> str:
        """获取缓存文件路径"""
        return os.path.join(self.cache_dir, f"{symbol}_valuation_{source.value}.pkl")

    def _load_cache(self, symbol: str, source: DataSource) -> Optional[pd.DataFrame]:
        """加载缓存"""
        cache_path = self._get_cache_path(symbol, source)
        if os.path.exists(cache_path):
            try:
                return pd.read_pickle(cache_path)
            except Exception:
                return None
        return None

    def _save_cache(self, df: pd.DataFrame, symbol: str, source: DataSource) -> None:
        """保存缓存"""
        if df is not None and not df.empty:
            cache_path = self._get_cache_path(symbol, source)
            df.to_pickle(cache_path)

    @retry_on_failure(max_retries=2, retry_delay=1.0)
    def fetch_from_baidu(self, symbol: str) -> pd.DataFrame:
        """
        从百度估值接口获取数据。

        AkShare: stock_zh_valuation_baidu
        """
        ak_sym = normalize_symbol(symbol)
        dfs = []

        indicators = [
            ("总市值", "market_cap"),
            ("市净率", "pb_ratio"),
            ("市盈率", "pe_ratio"),
        ]

        for indicator, col_name in indicators:
            try:
                df = ak.stock_zh_valuation_baidu(symbol=ak_sym, indicator=indicator)
                if df is not None and not df.empty:
                    df = df.rename(columns={"value": col_name})
                    dfs.append(df)
            except Exception as e:
                warnings.warn(f"百度接口获取 {indicator} 失败: {e}")

        if not dfs:
            return pd.DataFrame()

        from functools import reduce

        df = reduce(lambda x, y: pd.merge(x, y, on="date", how="outer"), dfs)
        return df

    @retry_on_failure(max_retries=2, retry_delay=1.0)
    def fetch_from_eastmoney(self, symbol: str) -> pd.DataFrame:
        """
        从东财接口获取估值数据。

        AkShare: stock_a_lg_indicator (东财估值指标)
        """
        ak_sym = normalize_symbol(symbol)

        try:
            df = ak.stock_a_lg_indicator(symbol=ak_sym)
            if df is None or df.empty:
                return pd.DataFrame()

            col_map = {
                "pe": "pe_ratio",
                "pe_ttm": "pe_ratio_ttm",
                "pb": "pb_ratio",
                "总市值": "market_cap",
                "流通市值": "circulating_market_cap",
            }

            for old, new in col_map.items():
                if old in df.columns:
                    df[new] = df[old]

            if "date" not in df.columns:
                date_col = find_date_column(df, "market")
                if date_col:
                    df["date"] = pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d")

            return df
        except Exception as e:
            warnings.warn(f"东财接口获取估值数据失败: {e}")
            return pd.DataFrame()

    @retry_on_failure(max_retries=2, retry_delay=1.0)
    def fetch_from_ths(self, symbol: str) -> pd.DataFrame:
        """
        从同花顺接口获取估值数据。

        AkShare: stock_zh_a_spot_em (包含部分估值字段)
        """
        ak_sym = normalize_symbol(symbol)

        try:
            df = ak.stock_individual_info_em(symbol=ak_sym)
            if df is None or df.empty:
                return pd.DataFrame()

            result = {}
            for _, row in df.iterrows():
                item = row.get("item", "")
                value = row.get("value", "")
                if item == "总市值":
                    result["market_cap"] = value
                elif item == "市盈率":
                    result["pe_ratio"] = value
                elif item == "市净率":
                    result["pb_ratio"] = value
                elif item == "流通市值":
                    result["circulating_market_cap"] = value

            if not result:
                return pd.DataFrame()

            return pd.DataFrame([result])
        except Exception as e:
            warnings.warn(f"同花顺接口获取估值数据失败: {e}")
            return pd.DataFrame()

    def fetch_with_fallback(
        self,
        symbol: str,
        force_update: bool = False,
        validate: bool = True,
    ) -> pd.DataFrame:
        """
        按优先级依次尝试各数据源，直到获取有效数据。

        Parameters
        ----------
        symbol : str
            证券代码
        force_update : bool
            是否强制更新（忽略缓存）
        validate : bool
            是否进行数据质量验证

        Returns
        -------
        pd.DataFrame
            估值数据表
        """
        fetch_methods = {
            DataSource.BAIDU: self.fetch_from_baidu,
            DataSource.EASTMONEY: self.fetch_from_eastmoney,
            DataSource.THS: self.fetch_from_ths,
        }

        for source in DATA_SOURCE_PRIORITY:
            if not force_update:
                cached = self._load_cache(symbol, source)
                if cached is not None and not cached.empty:
                    if validate:
                        validation = validate_valuation_data(
                            cached, symbol, strict=False
                        )
                        if validation["is_valid"]:
                            return cached
                    else:
                        return cached

            try:
                df = fetch_methods[source](symbol)
                if df is not None and not df.empty:
                    if "date" in df.columns:
                        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
                    df = df.sort_values("date").reset_index(drop=True)

                    if validate:
                        validation = validate_valuation_data(df, symbol, strict=False)
                        if validation["is_valid"]:
                            self._save_cache(df, symbol, source)
                            return df
                        else:
                            warnings.warn(
                                f"{source.value} 数据源质量检查未通过: {validation['message']}"
                            )
                    else:
                        self._save_cache(df, symbol, source)
                        return df
            except DataSourceError as e:
                warnings.warn(f"{source.value} 数据源失败: {e}")
                continue

        warnings.warn(f"{symbol} 所有数据源均无法获取有效估值数据")
        return pd.DataFrame()

    def merge_from_sources(
        self,
        symbol: str,
        force_update: bool = False,
    ) -> pd.DataFrame:
        """
        从多个数据源合并数据，取最优值。

        Parameters
        ----------
        symbol : str
            证券代码
        force_update : bool
            是否强制更新

        Returns
        -------
        pd.DataFrame
            合并后的估值数据表
        """
        dfs = {}
        fetch_methods = {
            DataSource.BAIDU: self.fetch_from_baidu,
            DataSource.EASTMONEY: self.fetch_from_eastmoney,
        }

        for source, method in fetch_methods.items():
            try:
                df = method(symbol)
                if df is not None and not df.empty:
                    dfs[source] = df
            except Exception:
                continue

        if not dfs:
            return pd.DataFrame()

        merged = None
        for source, df in dfs.items():
            if merged is None:
                merged = df
            else:
                merged = pd.merge(
                    merged,
                    df,
                    on="date",
                    how="outer",
                    suffixes=("", f"_{source.value}"),
                )

        if merged is None:
            return pd.DataFrame()

        cols_to_merge = ["pe_ratio", "pb_ratio", "market_cap", "circulating_market_cap"]
        for col in cols_to_merge:
            if col in merged.columns:
                for source in dfs.keys():
                    alt_col = f"{col}_{source.value}"
                    if alt_col in merged.columns:
                        merged[col] = merged[col].fillna(merged[alt_col])
                        merged = merged.drop(columns=[alt_col])

        if "date" in merged.columns:
            merged["date"] = pd.to_datetime(merged["date"]).dt.strftime("%Y-%m-%d")
            merged = merged.sort_values("date").reset_index(drop=True)

        return merged


class TurnoverDataSource:
    """换手率数据源管理器"""

    def __init__(self, cache_dir: str = "stock_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, symbol: str) -> str:
        return os.path.join(self.cache_dir, f"{symbol}_turnover.pkl")

    @retry_on_failure(max_retries=2, retry_delay=1.0)
    def fetch_from_akshare(self, symbol: str) -> pd.DataFrame:
        """
        从 AkShare 获取换手率数据。

        使用 stock_zh_a_hist 接口获取日线数据，计算换手率。
        """
        ak_sym = normalize_symbol(symbol)

        try:
            df = ak.stock_zh_a_hist(symbol=ak_sym, period="daily", adjust="qfq")
            if df is None or df.empty:
                return pd.DataFrame()

            if "换手率" in df.columns:
                df["turnover_rate"] = df["换手率"] / 100

            date_col = find_date_column(df, "market")
            if date_col:
                df["date"] = pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d")

            keep_cols = ["date", "turnover_rate", "成交量", "成交额", "收盘"]
            keep_cols = [c for c in keep_cols if c in df.columns]

            return df[keep_cols].sort_values("date").reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"获取换手率数据失败: {e}")
            return pd.DataFrame()

    @retry_on_failure(max_retries=2, retry_delay=1.0)
    def fetch_from_eastmoney_spot(self, symbol: str) -> pd.DataFrame:
        """
        从东财实时数据获取换手率。

        AkShare: stock_zh_a_spot_em
        """
        ak_sym = normalize_symbol(symbol)

        try:
            df = ak.stock_zh_a_spot_em()
            if df is None or df.empty:
                return pd.DataFrame()

            row = df[df["代码"] == ak_sym]
            if row.empty:
                return pd.DataFrame()

            result = {
                "date": pd.Timestamp.now().strftime("%Y-%m-%d"),
            }

            if "换手率" in row.columns:
                result["turnover_rate"] = float(row["换手率"].iloc[0]) / 100

            return pd.DataFrame([result])
        except Exception as e:
            warnings.warn(f"东财实时数据获取换手率失败: {e}")
            return pd.DataFrame()

    def fetch_turnover(
        self,
        symbol: str,
        force_update: bool = False,
    ) -> pd.DataFrame:
        """
        获取换手率数据。

        Parameters
        ----------
        symbol : str
            证券代码
        force_update : bool
            是否强制更新

        Returns
        -------
        pd.DataFrame
            换手率数据表
        """
        cache_path = self._get_cache_path(symbol)

        if not force_update and os.path.exists(cache_path):
            try:
                cached = pd.read_pickle(cache_path)
                if cached is not None and not cached.empty:
                    validation = validate_turnover_data(cached, symbol, strict=False)
                    if validation["is_valid"]:
                        return cached
            except Exception:
                pass

        df = self.fetch_from_akshare(symbol)

        if df is not None and not df.empty:
            validation = validate_turnover_data(df, symbol, strict=False)
            if validation["is_valid"]:
                df.to_pickle(cache_path)
                return df

        return pd.DataFrame()


valuation_data_source = ValuationDataSource()
turnover_data_source = TurnoverDataSource()


__all__ = [
    "DataSource",
    "DATA_SOURCE_PRIORITY",
    "DataQualityError",
    "DataSourceError",
    "validate_valuation_data",
    "validate_turnover_data",
    "retry_on_failure",
    "normalize_symbol",
    "ValuationDataSource",
    "TurnoverDataSource",
    "valuation_data_source",
    "turnover_data_source",
]
