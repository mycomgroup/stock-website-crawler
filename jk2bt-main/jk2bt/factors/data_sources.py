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

from jk2bt.utils.symbol import normalize_symbol


class DataSource(Enum):
    BAIDU = "baidu"
    EASTMONEY = "eastmoney"
    THS = "ths"
    AKSHARE_DEFAULT = "akshare"


from jk2bt.core.exceptions import DataSourceError


class DataQualityError(Exception):
    """数据质量异常"""

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


__all__ = [
    "DataSource",
    "DataQualityError",
    "DataSourceError",
    "validate_valuation_data",
    "validate_turnover_data",
    "retry_on_failure",
    "normalize_symbol",
]
