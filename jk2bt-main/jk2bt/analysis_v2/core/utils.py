"""
工具函数模块
"""
from typing import Union, Optional
from datetime import datetime
import numpy as np
import pandas as pd


def safe_divide(
    a: Union[pd.Series, np.ndarray, float],
    b: Union[pd.Series, np.ndarray, float],
    fill_value: float = np.nan
) -> Union[pd.Series, np.ndarray, float]:
    """
    安全除法，避免除零错误
    
    Args:
        a: 被除数
        b: 除数
        fill_value: 除零时的填充值
    
    Returns:
        计算结果，除零时返回fill_value
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        if isinstance(a, pd.Series) and isinstance(b, pd.Series):
            result = a / b
            result = result.where(np.isfinite(result), fill_value)
        elif isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
            result = np.divide(a, b)
            result = np.where(np.isfinite(result), result, fill_value)
        else:
            result = a / b if b != 0 else fill_value
            if not np.isfinite(result):
                result = fill_value
    return result


def validate_ohlcv(df: pd.DataFrame) -> bool:
    """
    验证OHLCV数据格式
    
    Args:
        df: 待验证的DataFrame
    
    Returns:
        是否包含必需的列
    """
    if df.empty:
        return False
    required_cols = {'open', 'high', 'low', 'close', 'volume'}
    df_cols = set(col.lower() for col in df.columns)
    return required_cols.issubset(df_cols)


def extract_ohlcv(df: pd.DataFrame) -> dict[str, pd.Series]:
    """
    从DataFrame提取OHLCV列
    
    自动处理列名大小写差异
    
    Args:
        df: 包含OHLCV数据的DataFrame
    
    Returns:
        包含各列的字典
    """
    result = {}
    col_map = {col.lower(): col for col in df.columns}
    
    for name in ['open', 'high', 'low', 'close', 'volume']:
        if name in col_map:
            result[name] = df[col_map[name]]
    
    return result


def normalize_date(
    date: Union[str, pd.Timestamp, datetime, None]
) -> Optional[pd.Timestamp]:
    """
    统一日期格式
    
    Args:
        date: 日期字符串、Timestamp或datetime对象
    
    Returns:
        统一的pd.Timestamp对象
    """
    if date is None:
        return None
    if isinstance(date, str):
        return pd.Timestamp(date)
    return pd.Timestamp(date)


def ensure_dataframe(
    data: Union[pd.DataFrame, pd.Series, dict]
) -> pd.DataFrame:
    """
    确保返回DataFrame
    
    Args:
        data: 数据
    
    Returns:
        DataFrame
    """
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, pd.Series):
        return data.to_frame()
    elif isinstance(data, dict):
        return pd.DataFrame(data)
    else:
        raise ValueError(f"Cannot convert {type(data)} to DataFrame")


def rolling_window(
    data: pd.Series,
    window: int
) -> np.ndarray:
    """
    创建滚动窗口视图（不复制数据）
    
    Args:
        data: 数据序列
        window: 窗口大小
    
    Returns:
        滚动窗口数组
    """
    if len(data) < window:
        return np.array([])
    return np.lib.stride_tricks.sliding_window_view(data.values, window)


def compute_returns(
    prices: pd.Series,
    method: str = "simple"
) -> pd.Series:
    """
    计算收益率
    
    Args:
        prices: 价格序列
        method: "simple" 或 "log"
    
    Returns:
        收益率序列
    """
    if method == "log":
        return np.log(prices / prices.shift(1))
    else:
        return prices.pct_change()