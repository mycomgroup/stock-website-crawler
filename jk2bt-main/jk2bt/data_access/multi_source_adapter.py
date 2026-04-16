"""
data_access/multi_source_adapter.py
统一多数据源切换适配器

对外提供统一接口，内部封装多数据源自动切换逻辑。
使用 data_source_backup 中的 fallback 函数作为底层实现。

使用方式:
    adapter = get_adapter()
    df = adapter.get_stock_daily('sh600000', '2020-01-01', '2020-12-31', 'qfq')
    etf_df = adapter.get_etf_daily('sh510300', '2020-01-01', '2020-12-31')
"""

import logging
from typing import Optional, List, Union
from datetime import date, datetime

import pandas as pd

from jk2bt.utils.data_source_backup import (
    get_stock_daily_with_fallback,
    get_etf_daily_with_fallback,
    DEFAULT_STOCK_DAILY_SOURCES,
    DEFAULT_ETF_DAILY_SOURCES,
    set_tushare_token,
)
from .cache_manager import get_cache

logger = logging.getLogger(__name__)


class MultiSourceAdapter:
    """
    多数据源切换适配器

    封装多数据源自动切换逻辑，对外提供统一接口。
    内部使用 data_source_backup 模块的 fallback 函数实现数据源切换。

    支持的数据源:
        - sina: 新浪财经 (优先)
        - east_money: 东方财富
        - tushare: Tushare (需要配置 token)
        - baostock: Baostock (免费)

    特性:
        1. 自动切换 - 某个数据源失败时自动切换到下一个
        2. 缓存支持 - 结果自动缓存
        3. 错误恢复 - 连续失败后会临时禁用数据源
    """

    def __init__(
        self,
        use_cache: bool = True,
        cache_ttl_hours: int = 24,
    ):
        """
        初始化 MultiSourceAdapter

        Args:
            use_cache: 是否使用缓存
            cache_ttl_hours: 缓存有效期 (小时)
        """
        self._use_cache = use_cache
        self._cache_ttl_hours = cache_ttl_hours

    def get_stock_daily(
        self,
        symbol: str,
        start: Union[str, date, datetime],
        end: Union[str, date, datetime],
        adjust: str = "qfq",
        sources: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        获取股票日线数据（自动切换数据源）

        数据源优先级: sina > east_money > tushare > baostock

        Args:
            symbol: 股票代码，支持 sh600000/sz000001/600000.XSHG 等格式
            start: 开始日期
            end: 结束日期
            adjust: 复权类型，qfq/hfq/none
            sources: 数据源列表，默认使用 DEFAULT_STOCK_DAILY_SOURCES

        Returns:
            DataFrame with columns: datetime, open, high, low, close, volume, amount
        """
        start_str = self._normalize_date(start)
        end_str = self._normalize_date(end)
        symbol_norm = self._normalize_symbol(symbol)

        cache_key = {
            "symbol": symbol_norm,
            "adjust": adjust,
            "start": start_str,
            "end": end_str,
        }

        if self._use_cache:
            cached = self._get_from_cache("stock_daily", **cache_key)
            if cached is not None and not cached.empty:
                logger.debug(f"[cache] {symbol_norm}: 使用缓存数据")
                return cached

        df = get_stock_daily_with_fallback(
            symbol=symbol_norm,
            start=start_str,
            end=end_str,
            adjust=adjust,
            sources=sources or DEFAULT_STOCK_DAILY_SOURCES,
            fallback_to_cache=False,
        )

        if self._use_cache and df is not None and not df.empty:
            self._set_to_cache("stock_daily", df, **cache_key)

        return df if df is not None else pd.DataFrame()

    def get_etf_daily(
        self,
        symbol: str,
        start: Union[str, date, datetime],
        end: Union[str, date, datetime],
        sources: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        获取 ETF 日线数据（自动切换数据源）

        数据源优先级: sina > east_money > tushare

        Args:
            symbol: ETF 代码，支持 sh510300/sz159915 等格式
            start: 开始日期
            end: 结束日期
            sources: 数据源列表，默认使用 DEFAULT_ETF_DAILY_SOURCES

        Returns:
            DataFrame with columns: datetime, open, high, low, close, volume, amount
        """
        start_str = self._normalize_date(start)
        end_str = self._normalize_date(end)
        symbol_norm = self._normalize_symbol(symbol)

        cache_key = {
            "symbol": symbol_norm,
            "start": start_str,
            "end": end_str,
        }

        if self._use_cache:
            cached = self._get_from_cache("etf_daily", **cache_key)
            if cached is not None and not cached.empty:
                logger.debug(f"[cache] {symbol_norm}: 使用缓存数据")
                return cached

        df = get_etf_daily_with_fallback(
            symbol=symbol_norm,
            start=start_str,
            end=end_str,
            sources=sources or DEFAULT_ETF_DAILY_SOURCES,
            fallback_to_cache=False,
        )

        if self._use_cache and df is not None and not df.empty:
            self._set_to_cache("etf_daily", df, **cache_key)

        return df if df is not None else pd.DataFrame()

    def _normalize_date(self, d: Union[str, date, datetime]) -> str:
        """标准化日期格式"""
        if isinstance(d, str):
            return d
        if isinstance(d, datetime):
            return d.strftime("%Y-%m-%d")
        if isinstance(d, date):
            return d.strftime("%Y-%m-%d")
        return str(d)

    def _normalize_symbol(self, symbol: str) -> str:
        """标准化代码格式"""
        symbol = str(symbol)
        if symbol.startswith("sh") or symbol.startswith("sz"):
            return symbol
        if ".XSHG" in symbol:
            return "sh" + symbol.replace(".XSHG", "")
        if ".XSHE" in symbol:
            return "sz" + symbol.replace(".XSHE", "")
        if symbol.startswith("6"):
            return "sh" + symbol.zfill(6)
        if symbol.startswith("0") or symbol.startswith("3"):
            return "sz" + symbol.zfill(6)
        return symbol

    def _get_from_cache(
        self,
        table: str,
        **conditions,
    ) -> Optional[pd.DataFrame]:
        """从缓存获取数据"""
        if not self._use_cache:
            return None
        cache = get_cache()
        return cache.get("multi_source", table, **conditions)

    def _set_to_cache(
        self,
        table: str,
        df: pd.DataFrame,
        **conditions,
    ):
        """写入缓存"""
        if not self._use_cache or df.empty:
            return
        cache = get_cache()
        cache.set("multi_source", table, df, **conditions)


_multi_source_adapter = None


def get_multi_source_adapter() -> MultiSourceAdapter:
    """获取全局 MultiSourceAdapter 单例"""
    global _multi_source_adapter
    if _multi_source_adapter is None:
        _multi_source_adapter = MultiSourceAdapter()
    return _multi_source_adapter


__all__ = [
    "MultiSourceAdapter",
    "get_multi_source_adapter",
    "set_tushare_token",
]
