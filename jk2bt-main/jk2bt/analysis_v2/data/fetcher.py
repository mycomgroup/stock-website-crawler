"""
统一数据获取函数

提供便捷的数据获取接口，内部使用 DataSourceContext
"""
from typing import List, Optional, Union
from datetime import datetime
import pandas as pd

from ..core.interface import DataSourceContext
from ..core.utils import normalize_date


def get_ohlcv(
    symbol: str,
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None,
    count: Optional[int] = None
) -> pd.DataFrame:
    """
    获取单只股票OHLCV数据
    
    Args:
        symbol: 股票代码
        start_date: 开始日期
        end_date: 结束日期
        count: 获取数据条数
    
    Returns:
        DataFrame with columns: date, open, high, low, close, volume
    
    使用示例:
        df = get_ohlcv("000001.SZ", count=100)
        df = get_ohlcv("000001.SZ", start_date="2024-01-01", end_date="2024-12-31")
    """
    ds = DataSourceContext.get_data_source()
    start = normalize_date(start_date)
    end = normalize_date(end_date)
    return ds.get_ohlcv(symbol, start, end, count)


def get_ohlcv_batch(
    symbols: List[str],
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None,
    count: Optional[int] = None
) -> dict[str, pd.DataFrame]:
    """
    批量获取OHLCV数据
    
    Args:
        symbols: 股票代码列表
        start_date: 开始日期
        end_date: 结束日期
        count: 获取数据条数
    
    Returns:
        字典: {symbol: DataFrame}
    """
    ds = DataSourceContext.get_data_source()
    start = normalize_date(start_date)
    end = normalize_date(end_date)
    return ds.get_ohlcv_batch(symbols, start, end, count)


def get_index_daily(
    symbol: str,
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None
) -> pd.DataFrame:
    """
    获取指数日线数据
    
    Args:
        symbol: 指数代码
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        DataFrame with columns: date, open, high, low, close, volume
    """
    ds = DataSourceContext.get_data_source()
    start = normalize_date(start_date)
    end = normalize_date(end_date)
    return ds.get_index_daily(symbol, start, end)


def get_valuation(
    symbol: str,
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None
) -> pd.DataFrame:
    """
    获取估值数据
    
    Args:
        symbol: 股票代码
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        DataFrame with columns: date, pe_ratio, pb_ratio, market_cap, etc.
    """
    ds = DataSourceContext.get_data_source()
    start = normalize_date(start_date)
    end = normalize_date(end_date)
    return ds.get_valuation(symbol, start, end)


def get_financial(
    symbol: str,
    table: str
) -> pd.DataFrame:
    """
    获取财务数据
    
    Args:
        symbol: 股票代码
        table: 表名 ("income", "balance", "cashflow")
    
    Returns:
        DataFrame with financial data
    """
    ds = DataSourceContext.get_data_source()
    return ds.get_financial(symbol, table)


def get_index_components(index_symbol: str) -> List[str]:
    """
    获取指数成分股
    
    Args:
        index_symbol: 指数代码
    
    Returns:
        成分股代码列表
    """
    ds = DataSourceContext.get_data_source()
    return ds.get_index_components(index_symbol)