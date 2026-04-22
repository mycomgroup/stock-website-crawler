"""
Data 模块 - 数据适配层

此模块是唯一依赖 jk2bt.data 的地方。
"""

from .adapter import Jk2btDataAdapter, init_data_source
from .fetcher import get_ohlcv, get_ohlcv_batch, get_index_daily, get_valuation

__all__ = [
    "Jk2btDataAdapter",
    "init_data_source",
    "get_ohlcv",
    "get_ohlcv_batch",
    "get_index_daily",
    "get_valuation",
]