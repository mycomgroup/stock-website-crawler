"""
缓存与性能优化模块（权威文件）

从 optimizations.py 拆出，包含：
1. 当前数据缓存（CurrentDataCache）
2. 批量数据加载（BatchDataLoader、DataPreloader）
3. 内存管理（get_memory_usage、cleanup_memory）
"""

import pandas as pd
import warnings
import threading
from datetime import datetime
from functools import lru_cache


class CurrentDataCache:
    """
    get_current_data 结果缓存器
    避免重复查询同一股票的数据
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._cache = {}
                    cls._instance._timestamps = {}
                    cls._instance._ttl_seconds = 60
        return cls._instance

    def get(self, code, bt_strategy=None):
        """从缓存获取数据"""
        now = datetime.now()

        if code in self._cache:
            cached_time = self._timestamps.get(code)
            if cached_time and (now - cached_time).total_seconds() < self._ttl_seconds:
                return self._cache[code]

        from jk2bt.core.strategy_base import get_current_data

        entry = get_current_data(bt_strategy)[code]

        self._cache[code] = entry
        self._timestamps[code] = now

        return entry

    def invalidate(self, code=None):
        """清除缓存"""
        if code is None:
            self._cache.clear()
            self._timestamps.clear()
        else:
            self._cache.pop(code, None)
            self._timestamps.pop(code, None)

    def set_ttl(self, seconds):
        """设置缓存过期时间"""
        self._ttl_seconds = seconds


def get_current_data_cached(code, bt_strategy=None):
    """
    带缓存的 get_current_data

    参数:
        code: 股票代码
        bt_strategy: Backtrader 策略实例

    返回:
        _CurrentDataEntry 对象
    """
    cache = CurrentDataCache()
    return cache.get(code, bt_strategy)


def get_current_data_batch(codes, bt_strategy=None, use_cache=True):
    """
    批量获取当前数据

    参数:
        codes: 股票代码列表
        bt_strategy: Backtrader 策略实例
        use_cache: 是否使用缓存

    返回:
        dict {股票代码: _CurrentDataEntry 对象}
    """
    if use_cache:
        cache = CurrentDataCache()
        return {code: cache.get(code, bt_strategy) for code in codes}
    else:
        from jk2bt.core.strategy_base import get_current_data

        current_data = get_current_data(bt_strategy)
        return {code: current_data[code] for code in codes}


class BatchDataLoader:
    """批量数据加载器"""

    def __init__(self, cache_dir="batch_cache"):
        self._cache_dir = cache_dir
        self._data_cache = {}

    def load_stocks(self, symbols, start_date, end_date, fields=None, adjust="qfq"):
        """批量加载股票历史数据"""
        from jk2bt.core.strategy_base import get_price

        result = {}
        for symbol in symbols:
            try:
                df = get_price(
                    symbol,
                    start_date=start_date,
                    end_date=end_date,
                    fields=fields,
                    adjust=adjust,
                )
                result[symbol] = df
            except Exception as e:
                warnings.warn(f"{symbol} 数据加载失败: {e}")
                result[symbol] = pd.DataFrame()

        return result

    def preload_index_stocks(self, index_code, start_date, end_date):
        """预加载指数成分股数据"""
        from jk2bt.core.strategy_base import get_index_stocks

        stocks = get_index_stocks(index_code)
        return self.load_stocks(stocks, start_date, end_date)

    def clear_cache(self):
        """清除缓存数据"""
        self._data_cache.clear()


def preload_data_for_strategy(stock_pool, start_date, end_date):
    """为策略预加载所有必要数据"""
    loader = BatchDataLoader()
    return loader.load_stocks(stock_pool, start_date, end_date)


@lru_cache(maxsize=1000)
def cached_get_security_info(code):
    """带缓存的证券信息查询"""
    from jk2bt.core.strategy_base import get_security_info_jq

    return get_security_info_jq(code)


@lru_cache(maxsize=100)
def cached_get_index_stocks(index_code, date=None):
    """带缓存的指数成分股查询"""
    from jk2bt.core.strategy_base import get_index_stocks

    return tuple(get_index_stocks(index_code, date))


def optimize_dataframe_memory(df):
    """优化 DataFrame 内存使用"""
    for col in df.columns:
        col_type = df[col].dtype

        if col_type == "object":
            if df[col].nunique() / len(df[col]) < 0.5:
                df[col] = df[col].astype("category")
        elif col_type == "float64":
            df[col] = pd.to_numeric(df[col], downcast="float")
        elif col_type == "int64":
            df[col] = pd.to_numeric(df[col], downcast="integer")

    return df


def batch_get_fundamentals(query_obj, symbols, date=None):
    """批量获取财务数据"""
    from jk2bt.core.strategy_base import get_fundamentals

    if hasattr(query_obj, "_symbols"):
        query_obj._symbols = symbols

    return get_fundamentals(query_obj, date=date)


class DataPreloader:
    """数据预加载器"""

    def __init__(self):
        self._loaded_data = {}

    def preload_market_data(self, symbols, start_date, end_date):
        """预加载市场数据"""
        loader = BatchDataLoader()
        self._loaded_data["market"] = loader.load_stocks(symbols, start_date, end_date)

    def preload_fundamentals(self, symbols, fields):
        """预加载财务数据"""
        from jk2bt.core.strategy_base import get_fundamentals, query, valuation

        if "valuation" in fields:
            q = query(valuation).filter(valuation.code.in_(symbols))
            self._loaded_data["valuation"] = get_fundamentals(q)

    def preload_indicators(self, symbols, fields):
        """预加载指标数据"""
        from indicator_fields import get_indicator_batch

        self._loaded_data["indicator"] = get_indicator_batch(symbols, fields=fields)

    def get_loaded_data(self, data_type):
        """获取预加载的数据"""
        return self._loaded_data.get(data_type)

    def clear(self):
        """清除所有预加载数据"""
        self._loaded_data.clear()


def warm_up_cache(symbols, date=None):
    """
    预热缓存

    参数:
        symbols: 股票代码列表
        date: 查询日期
    """
    cache = CurrentDataCache()

    for symbol in symbols:
        try:
            cache.get(symbol)
        except Exception:
            pass

    for symbol in symbols:
        try:
            cached_get_security_info(symbol)
        except Exception:
            pass


def get_memory_usage():
    """获取当前内存使用情况"""
    import psutil
    import os

    process = psutil.Process(os.getpid())

    return {
        "rss": process.memory_info().rss / 1024 / 1024,
        "vms": process.memory_info().vms / 1024 / 1024,
        "percent": process.memory_percent(),
    }


def cleanup_memory():
    """清理内存，清除不必要的缓存和临时数据"""
    cache = CurrentDataCache()
    cache.invalidate()

    cached_get_security_info.cache_clear()
    cached_get_index_stocks.cache_clear()

    import gc

    gc.collect()


__all__ = [
    # 缓存类
    "CurrentDataCache",
    # 带缓存的数据获取
    "get_current_data_cached",
    "get_current_data_batch",
    "cached_get_security_info",
    "cached_get_index_stocks",
    # 批量加载
    "BatchDataLoader",
    "DataPreloader",
    "preload_data_for_strategy",
    "batch_get_fundamentals",
    # 缓存预热
    "warm_up_cache",
    # 内存管理
    "get_memory_usage",
    "cleanup_memory",
    "optimize_dataframe_memory",
]
