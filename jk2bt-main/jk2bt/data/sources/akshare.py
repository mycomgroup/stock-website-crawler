"""
src/data_access/akshare_adapter.py
AkShare 数据源适配器 - 实现 DataSource 接口。

整合现有的 market_data 模块，提供统一的数据访问接口。
支持缓存、多数据源备份、错误重试等特性。
"""

import json
import logging
import os
import time
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union
import pandas as pd

from .base import DataSource, DataSourceError

from .error_codes import (
    ErrorCode,
    DataSourceError as DataErrorCode,
    SourceUnavailableError,
    NoDataError,
)
from .akshare_compat import get_compat_adapter, AkShareCompatAdapter
from .stats_collector import get_stats_collector, StatsCollector
from .router import MultiSourceRouter

try:
    from jk2bt.data.sources import data_source_backup
    from jk2bt.data.sources.data_source_backup import (
        DEFAULT_STOCK_DAILY_SOURCES,
        DEFAULT_ETF_DAILY_SOURCES,
    )
except ImportError:
    data_source_backup = None
    DEFAULT_STOCK_DAILY_SOURCES = ["sina", "east_money", "tushare", "baostock"]
    DEFAULT_ETF_DAILY_SOURCES = ["sina", "east_money", "tushare"]

try:
    from jk2bt.cache import get_cache_manager

    _PARQUET_CACHE_AVAILABLE = True
except ImportError:
    _PARQUET_CACHE_AVAILABLE = False

from jk2bt.utils.symbol import jq_code_to_ak as _jq_code_to_ak

from jk2bt.utils.date_utils import find_date_column

logger = logging.getLogger(__name__)


class AkShareAdapter(DataSource):
    """
    AkShare 数据源适配器。

    实现 DataSource 接口，整合现有 market_data 模块功能。
    支持缓存机制和多数据源备份。

    特性:
        1. 统一缓存 - 使用 DataAccessCacheManager
        2. 多数据源备份 - 支持 sina/eastmoney/tushare/baostock
        3. 错误重试 - 失败时自动重试备用数据源
        4. 离线模式 - 支持仅使用本地缓存

    使用方式:
        adapter = AkShareAdapter()
        df = adapter.get_daily_data('sh600000', '2020-01-01', '2020-12-31')
    """

    name = "akshare"
    source_type = "real"
    DEFAULT_DATA_SOURCES = DEFAULT_STOCK_DAILY_SOURCES

    def __init__(
        self,
        use_cache: bool = True,
        cache_ttl_hours: int = 24,
        offline_mode: bool = False,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        data_sources: List[str] = None,
    ):
        """
        初始化 AkShare 适配器。

        Args:
            use_cache: 是否使用缓存
            cache_ttl_hours: 缓存有效期 (小时)
            offline_mode: 离线模式 (仅使用缓存)
            max_retries: 最大重试次数
            retry_delay: 重试间隔 (秒)
            data_sources: 数据源优先级列表
        """
        self._use_cache = use_cache
        self._cache_ttl_hours = cache_ttl_hours
        self._offline_mode = offline_mode
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._data_sources = data_sources or self.DEFAULT_DATA_SOURCES

        # 尝试导入 akshare
        self._akshare_available = False
        try:
            import sys
            import os

            # 添加本地 akshare 项目路径到 sys.path 的最前面
            local_akshare_path = "/Users/fengzhi/Downloads/git/akshare"
            # 移除可能存在的相同路径
            if local_akshare_path in sys.path:
                sys.path.remove(local_akshare_path)
            # 插入到最前面
            sys.path.insert(0, local_akshare_path)

            import akshare

            self._akshare = akshare
            self._akshare_available = True
            logger.debug(f"akshare 从本地项目导入: {akshare.__file__}")
        except ImportError:
            logger.warning("akshare 未安装，将仅使用缓存数据")

        # 按需导入 market_data 模块
        self._market_data_loaded = False

        # AkShare version compatibility adapter (Phase 2)
        self._compat_adapter = None

        # Stats collector (Phase 2)
        self._stats = get_stats_collector()

        # Parquet cache layer
        self._parquet_cache = None
        if _PARQUET_CACHE_AVAILABLE:
            try:
                self._parquet_cache = get_cache_manager()
            except Exception as e:
                logger.warning(f"parquet_cache 初始化失败: {e}")

    def _load_market_data(self):
        """延迟加载 market_data 模块"""
        if self._market_data_loaded:
            return

        try:
            # 导入各子模块
            import sys
            import os

            # 添加路径
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if base_dir not in sys.path:
                sys.path.insert(0, base_dir)

            # 动态导入
            from market_data.stock import get_stock_daily
            from market_data.etf import get_etf_daily
            from market_data.index import get_index_daily
            from market_data.index_components import (
                get_index_components,
                get_index_stocks,
            )
            from market_data.minute import get_stock_minute, get_etf_minute
            from market_data.money_flow import get_money_flow
            from market_data.north_money import get_north_money_flow
            from market_data.industry_sw import (
                get_industry_stocks_sw,
                get_all_industry_mapping,
            )
            from market_data.call_auction import get_call_auction

            self._get_stock_daily = get_stock_daily
            self._get_etf_daily = get_etf_daily
            self._get_index_daily = get_index_daily
            self._get_index_components = get_index_components
            self._get_index_stocks = get_index_stocks
            self._get_stock_minute = get_stock_minute
            self._get_etf_minute = get_etf_minute
            self._get_money_flow = get_money_flow
            self._get_north_money_flow = get_north_money_flow
            self._get_industry_stocks_sw = get_industry_stocks_sw
            self._get_all_industry_mapping = get_all_industry_mapping
            self._get_call_auction = get_call_auction

            self._market_data_loaded = True

        except ImportError as e:
            logger.warning(f"market_data 模块导入失败: {e}")
            # 设置空函数作为备用
            self._market_data_loaded = True  # 标记为已尝试加载

    def _get_compat_adapter(self) -> AkShareCompatAdapter:
        """Lazily create and return the AkShareCompatAdapter."""
        if self._compat_adapter is None:
            self._compat_adapter = get_compat_adapter()
        return self._compat_adapter

    def _record_request(
        self, source, duration_ms, success, error_type=None, endpoint=None
    ):
        """Record a request to the stats collector."""
        self._stats.record_request(source, duration_ms, success, error_type, endpoint)

    def _record_cache_hit(self, cache_name):
        """Record a cache hit."""
        self._stats.record_cache_hit(cache_name)

    def _record_cache_miss(self, cache_name):
        """Record a cache miss."""
        self._stats.record_cache_miss(cache_name)

    def _parquet_get(
        self,
        table: str,
        where: dict = None,
        columns: list = None,
        order_by: list = None,
        limit: int = None,
    ) -> Optional[pd.DataFrame]:
        """从 parquet_cache 获取数据"""
        if not self._use_cache or self._parquet_cache is None:
            return None
        try:
            return self._parquet_cache.get(
                table,
                where=where,
                columns=columns,
                order_by=order_by,
                limit=limit,
            )
        except Exception as e:
            logger.warning(f"parquet_cache get 失败 table={table}: {e}")
            return None

    def _parquet_put(
        self,
        table: str,
        df: pd.DataFrame,
        partition_value: str = None,
    ) -> bool:
        """写入 parquet_cache"""
        if not self._use_cache or self._parquet_cache is None or df is None or df.empty:
            return False
        try:
            self._parquet_cache.put(table, df, partition_value=partition_value)
            return True
        except Exception as e:
            logger.warning(f"parquet_cache put 失败 table={table}: {e}")
            return False

    def _parquet_exists(
        self,
        table: str,
        where: dict = None,
    ) -> bool:
        """检查 parquet_cache 中是否存在数据"""
        if not self._use_cache or self._parquet_cache is None:
            return False
        try:
            return self._parquet_cache.exists(table, where=where)
        except Exception as e:
            logger.warning(f"parquet_cache exists 失败 table={table}: {e}")
            return False

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
        return _jq_code_to_ak(symbol)

    def _get_from_cache(
        self,
        domain: str,
        table: str,
        **conditions,
    ) -> Optional[pd.DataFrame]:
        """从缓存获取数据"""
        if not self._use_cache:
            return None
        from . import get_cache

        cache = get_cache()
        return cache.get(domain, table, **conditions)

    def _set_to_cache(
        self,
        domain: str,
        table: str,
        df: pd.DataFrame,
        **conditions,
    ):
        """写入缓存"""
        if not self._use_cache or df.empty:
            return
        from . import get_cache

        cache = get_cache()
        # 添加缓存所需的元数据列
        cache_df = df.copy()
        if table == "stock_daily" and "symbol" not in cache_df.columns:
            cache_df = cache_df.copy()
            cache_df["symbol"] = conditions.get("symbol", "")
            cache_df["date"] = (
                cache_df["datetime"].dt.date
                if "datetime" in cache_df.columns
                else conditions.get("start_date", "")
            )
            cache_df["adjust"] = conditions.get("adjust", "")
        cache.set(domain, table, cache_df, **conditions)

    # === 实现 DataSource 接口 ===

    def get_daily_data(
        self,
        symbol: str,
        start_date: Union[str, date, datetime],
        end_date: Union[str, date, datetime],
        adjust: str = "qfq",
        **kwargs,
    ) -> pd.DataFrame:
        """获取日线行情数据"""
        symbol = self._normalize_symbol(symbol)
        start = self._normalize_date(start_date)
        end = self._normalize_date(end_date)

        # 检查缓存
        cache_key = {
            "symbol": symbol,
            "adjust": adjust,
        }
        cached = self._get_from_cache("market", "stock_daily", **cache_key)
        if cached is not None and not cached.empty:
            self._record_cache_hit("stock_daily")
            # 过滤日期范围
            cached = cached.copy()
            if "datetime" in cached.columns:
                cached["datetime"] = pd.to_datetime(cached["datetime"])
                cached = cached[
                    (cached["datetime"] >= pd.to_datetime(start))
                    & (cached["datetime"] <= pd.to_datetime(end))
                ]
            if not cached.empty:
                logger.debug(f"[cache] {symbol}: 使用缓存数据")
                return cached

        # 离线模式
        if self._offline_mode:
            if cached is not None and not cached.empty:
                return cached
            raise SourceUnavailableError(
                "离线模式下无缓存数据",
                error_code=ErrorCode.SOURCE_UNAVAILABLE,
                source=self.name,
                symbol=symbol,
            )

        # 从数据源获取 - 直接使用 akshare（避免 market_data 循环依赖）
        # 注意：market_data.stock.get_stock_daily 会调用 data_source_backup，
        # 而 data_source_backup 又调用 get_adapter().get_daily_data()，形成循环
        # 所以直接使用 akshare API
        if self._akshare_available:
            try:
                import time

                # 转换代码格式
                ak_symbol = symbol.replace("sh", "").replace("sz", "")
                # 新浪前缀：股票 6xxxxx=sh, ETF 51xxxx/56xxxx/58xxxx=sh, 指数 000xxx=sh/399xxx=sz
                sh_prefixes = ("6", "51", "56", "58", "000")
                sz_prefixes = ("15", "16", "18", "399")
                sina_symbol = (
                    f"sh{ak_symbol}"
                    if ak_symbol.startswith(sh_prefixes)
                    else f"sz{ak_symbol}"
                )

                # 检测类型
                etf_prefixes = ("51", "56", "58", "15", "16", "18")
                index_prefixes = ("000", "399")
                is_etf = ak_symbol.startswith(etf_prefixes)
                is_index = ak_symbol.startswith(index_prefixes)

                # 优先使用新浪（更稳定），失败时使用东方财富
                raw_df = None
                if is_etf:
                    # ETF 使用专用函数
                    source_funcs = [
                        (
                            lambda: self._akshare.fund_etf_hist_sina(
                                symbol=sina_symbol
                            ),
                            "sina",
                            {},
                        ),
                        (
                            lambda: self._akshare.fund_etf_hist_em(
                                symbol=ak_symbol,
                                period="daily",
                                start_date=start.replace("-", ""),
                                end_date=end.replace("-", ""),
                                adjust=adjust if adjust else "",
                            ),
                            "eastmoney",
                            {},
                        ),
                    ]
                else:
                    # 股票使用通用函数
                    source_funcs = [
                        (
                            lambda: self._akshare.stock_zh_a_daily(
                                symbol=sina_symbol,
                                start_date=start.replace("-", ""),
                                end_date=end.replace("-", ""),
                                adjust=adjust if adjust else "",
                            ),
                            "sina",
                            {},
                        ),
                        (
                            lambda: self._akshare.stock_zh_a_hist(
                                symbol=ak_symbol,
                                period="daily",
                                start_date=start.replace("-", ""),
                                end_date=end.replace("-", ""),
                                adjust=adjust,
                            ),
                            "eastmoney",
                            {},
                        ),
                    ]

                for source_func, source_name, source_kwargs in source_funcs:
                    for attempt in range(self._max_retries):
                        try:
                            start_time = time.time()
                            raw_df = source_func()
                            duration_ms = (time.time() - start_time) * 1000
                            self._record_request(
                                source_name,
                                duration_ms,
                                True,
                                endpoint=f"{source_name}_daily",
                            )
                            if raw_df is not None and not raw_df.empty:
                                break
                        except Exception as e:
                            duration_ms = (
                                (time.time() - start_time) * 1000
                                if "start_time" in dir()
                                else 0
                            )
                            self._record_request(
                                source_name,
                                duration_ms,
                                False,
                                error_type=type(e).__name__,
                                endpoint=f"{source_name}_daily",
                            )
                            if attempt < self._max_retries - 1:
                                time.sleep(self._retry_delay)
                            else:
                                logger.warning(
                                    f"[{source_name}] 获取 {symbol} 失败: {e}"
                                )
                    if raw_df is not None and not raw_df.empty:
                        break

                if raw_df is None or raw_df.empty:
                    raise SourceUnavailableError(
                        "所有数据源都不可用",
                        error_code=ErrorCode.SOURCE_UNAVAILABLE,
                        source=self.name,
                        symbol=symbol,
                    )

                # 标准化字段
                df = self._standardize_ohlcv(raw_df)
                self._set_to_cache("market", "stock_daily", df, **cache_key)
                return df
            except Exception as e:
                logger.warning(f"获取 {symbol} 日线数据失败: {e}")

        raise SourceUnavailableError(
            "数据源不可用",
            error_code=ErrorCode.SOURCE_UNAVAILABLE,
            source=self.name,
            symbol=symbol,
        )

    def _standardize_ohlcv(self, df: pd.DataFrame) -> pd.DataFrame:
        """标准化 OHLCV 字段"""
        if df is None or df.empty:
            return pd.DataFrame()

        result = df.copy()
        columns_map = {
            "日期": "datetime",
            "date": "datetime",
            "开盘": "open",
            "open": "open",
            "最高": "high",
            "high": "high",
            "最低": "low",
            "low": "low",
            "收盘": "close",
            "close": "close",
            "成交量": "volume",
            "volume": "volume",
            "成交额": "amount",
            "amount": "amount",
        }

        for old_col, new_col in columns_map.items():
            if old_col in result.columns:
                result[new_col] = result[old_col]

        if "datetime" in result.columns:
            result["datetime"] = pd.to_datetime(result["datetime"])

        select_cols = ["datetime", "open", "high", "low", "close", "volume"]
        if "amount" in result.columns:
            select_cols.append("amount")

        return result[select_cols].copy()

    def get_index_stocks(self, index_code: str, **kwargs) -> List[str]:
        """获取指数成分股列表"""
        self._load_market_data()

        # 尝试从 parquet_cache 获取
        cached = self._parquet_get(
            "index_components",
            where={"index_code": index_code},
        )
        if cached is not None and not cached.empty:
            logger.debug(f"[parquet_cache] {index_code}: 使用缓存成分股列表")
            if "code" in cached.columns:
                return cached["code"].dropna().tolist()

        if hasattr(self, "_get_index_stocks"):
            try:
                stocks = self._get_index_stocks(
                    index_code,
                    force_update=kwargs.get("force_update", False),
                )
                return stocks
            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=index_code)

        # 直接使用 akshare
        if self._akshare_available:
            try:
                # 转换代码格式
                index_num = (
                    index_code.split(".")[0] if "." in index_code else index_code
                )
                index_num = index_num.replace("sh", "").replace("sz", "").zfill(6)

                df = self._akshare.index_stock_cons(symbol=index_num)
                if df is not None and not df.empty:
                    stocks = []
                    for code in df.get("成分股代码", df.get("品种代码", [])):
                        code_str = str(code).zfill(6)
                        if code_str.startswith("6"):
                            stocks.append(f"{code_str}.XSHG")
                        else:
                            stocks.append(f"{code_str}.XSHE")
                    # 写入 parquet_cache
                    result_df = pd.DataFrame(
                        {"index_code": [index_code] * len(stocks), "code": stocks}
                    )
                    self._parquet_put("index_components", result_df)
                    return stocks
            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=index_code)

        raise DataSourceError("数据源不可用", source=self.name, symbol=index_code)

    def get_index_components(
        self,
        index_code: str,
        include_weights: bool = True,
        **kwargs,
    ) -> pd.DataFrame:
        """获取指数成分股详情"""
        self._load_market_data()

        # 尝试从 parquet_cache 获取
        cached = self._parquet_get(
            "index_components",
            where={"index_code": index_code},
        )
        if cached is not None and not cached.empty:
            logger.debug(f"[parquet_cache] {index_code}: 使用缓存成分股")
            return cached

        if hasattr(self, "_get_index_components"):
            try:
                df = self._get_index_components(
                    index_code,
                    force_update=kwargs.get("force_update", False),
                )
                return df
            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=index_code)

        # 直接使用 akshare (含权重)
        if self._akshare_available and include_weights:
            try:
                index_num = (
                    index_code.split(".")[0] if "." in index_code else index_code
                )
                index_num = index_num.replace("sh", "").replace("sz", "").zfill(6)

                # 尝试从中证指数获取
                try:
                    df = self._akshare.index_stock_cons_weight_csindex(symbol=index_num)
                    if df is not None and not df.empty:
                        # 标准化
                        result = pd.DataFrame()
                        jq_code = (
                            index_code
                            if "." in index_code
                            else self._to_jq_format(index_code)
                        )
                        result["index_code"] = [jq_code] * len(df)

                        # 查找代码列
                        code_col = None
                        for col in ["成分券代码", "成分股代码", "品种代码"]:
                            if col in df.columns:
                                code_col = col
                                break
                        if code_col:
                            result["code"] = df[code_col].apply(self._to_jq_format)

                        # 查找名称列
                        name_col = None
                        for col in ["成分券名称", "成分股名称", "品种名称"]:
                            if col in df.columns:
                                name_col = col
                                break
                        if name_col:
                            result["stock_name"] = df[name_col]

                        # 查找权重列
                        weight_col = None
                        for col in ["权重", "weight", "占比"]:
                            if col in df.columns:
                                weight_col = col
                                break
                        if weight_col:
                            result["weight"] = df[weight_col]

                        # 写入 parquet_cache
                        if not result.empty:
                            self._parquet_put("index_components", result)
                        return result
                except Exception:
                    pass

                # 备用: 使用无权重版本
                df = self._akshare.index_stock_cons(symbol=index_num)
                if df is not None and not df.empty:
                    result = pd.DataFrame()
                    jq_code = (
                        index_code
                        if "." in index_code
                        else self._to_jq_format(index_code)
                    )
                    result["index_code"] = [jq_code] * len(df)
                    result["code"] = df.get("成分股代码", df.get("品种代码")).apply(
                        self._to_jq_format
                    )
                    result["stock_name"] = df.get("成分股名称", df.get("品种名称", ""))
                    if include_weights:
                        result["weight"] = 100.0 / len(df)  # 等权重
                    # 写入 parquet_cache
                    if not result.empty:
                        self._parquet_put("index_components", result)
                    return result

            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=index_code)

        raise DataSourceError("数据源不可用", source=self.name, symbol=index_code)

    def _to_jq_format(self, code: str) -> str:
        """转换为聚宽代码格式"""
        code = str(code).zfill(6)
        if code.startswith("6"):
            return f"{code}.XSHG"
        return f"{code}.XSHE"

    def get_trading_days(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> List[str]:
        """获取交易日列表"""
        # 检查缓存
        cached = self._get_from_cache("meta", "trade_days")
        if cached is not None and not cached.empty:
            days = (
                cached["date"].tolist()
                if "date" in cached.columns
                else cached.index.tolist()
            )
            if start_date:
                start = self._normalize_date(start_date)
                days = [d for d in days if d >= start]
            if end_date:
                end = self._normalize_date(end_date)
                days = [d for d in days if d <= end]
            return days

        # 从数据源获取
        if self._akshare_available:
            try:
                df = self._akshare.tool_trade_date_hist_sina()
                if df is not None and not df.empty:
                    days = df["trade_date"].tolist()
                    # 写入缓存
                    cache_df = pd.DataFrame({"date": days})
                    self._set_to_cache("meta", "trade_days", cache_df)

                    # 过滤日期
                    if start_date:
                        start = self._normalize_date(start_date)
                        days = [d for d in days if d >= start]
                    if end_date:
                        end = self._normalize_date(end_date)
                        days = [d for d in days if d <= end]
                    return days
            except Exception as e:
                raise DataSourceError(str(e), source=self.name)

        raise DataSourceError("数据源不可用", source=self.name)

    def get_securities_list(
        self,
        security_type: str = "stock",
        date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取证券列表"""
        if self._akshare_available:
            try:
                import time

                compat = self._get_compat_adapter()

                if security_type == "stock":
                    start_time = time.time()
                    df = compat.call("stock_info_a_code_name")
                    duration_ms = (time.time() - start_time) * 1000
                    self._record_request(
                        "akshare", duration_ms, True, endpoint="stock_info_a_code_name"
                    )
                elif security_type == "etf":
                    start_time = time.time()
                    df = compat.call("fund_etf_category_sina", symbol="ETF基金")
                    duration_ms = (time.time() - start_time) * 1000
                    self._record_request(
                        "akshare", duration_ms, True, endpoint="fund_etf_category_sina"
                    )
                elif security_type == "index":
                    start_time = time.time()
                    df = compat.call("index_stock_info")
                    duration_ms = (time.time() - start_time) * 1000
                    self._record_request(
                        "akshare", duration_ms, True, endpoint="index_stock_info"
                    )
                else:
                    raise DataSourceError(
                        f"不支持类型: {security_type}", source=self.name
                    )

                # 标准化字段
                result = pd.DataFrame()
                if "code" in df.columns:
                    result["code"] = df["code"].apply(self._to_jq_format)
                elif "symbol" in df.columns:
                    result["code"] = df["symbol"].apply(self._to_jq_format)

                if "name" in df.columns:
                    result["display_name"] = df["name"]
                elif "display_name" in df.columns:
                    result["display_name"] = df["display_name"]

                result["type"] = security_type

                return result

            except Exception as e:
                raise DataSourceError(str(e), source=self.name)

        raise SourceUnavailableError(
            "数据源不可用", error_code=ErrorCode.SOURCE_UNAVAILABLE, source=self.name
        )

    def get_security_info(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """获取单个证券基本信息"""
        if self._akshare_available:
            try:
                code = symbol.split(".")[0] if "." in symbol else symbol
                code = code.replace("sh", "").replace("sz", "").zfill(6)

                df = self._akshare.stock_individual_info_em(symbol=code)
                if df is not None and not df.empty:
                    info = {}
                    for _, row in df.iterrows():
                        key = row.get("item", row.get("指标", ""))
                        value = row.get("value", row.get("值", ""))
                        if key:
                            info[key] = value

                    return {
                        "code": symbol,
                        "display_name": info.get("股票简称", info.get("名称", "")),
                        "type": "stock",
                        "start_date": info.get("上市时间", ""),
                        "industry": info.get("行业", ""),
                    }
            except Exception as e:
                logger.warning(f"获取证券信息失败: {e}")
                return {"code": symbol, "display_name": "", "type": "unknown"}

        return {"code": symbol, "display_name": "", "type": "unknown"}

    def get_minute_data(
        self,
        symbol: str,
        freq: str = "1min",
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取分钟线数据"""
        self._load_market_data()
        symbol = self._normalize_symbol(symbol)
        start = self._normalize_date(start_date) if start_date else None
        end = self._normalize_date(end_date) if end_date else None
        adjust = kwargs.get("adjust", "")

        cache_key = {
            "symbol": symbol,
            "freq": freq,
            "adjust": adjust,
            "start_date": start,
            "end_date": end,
        }

        if hasattr(self, "_get_stock_minute"):
            try:
                symbol = self._normalize_symbol(symbol)
                start = self._normalize_date(start_date) if start_date else None
                end = self._normalize_date(end_date) if end_date else None

                df = self._get_stock_minute(symbol, freq=freq)
                return df
            except Exception as e:
                raise DataErrorCode(str(e), source=self.name, symbol=symbol)

        if self._akshare_available:
            try:
                code = (
                    symbol.replace("sh", "")
                    .replace("sz", "")
                    .replace(".XSHG", "")
                    .replace(".XSHE", "")
                )

                # akshare 分钟数据
                df = self._akshare.stock_zh_a_minute(
                    symbol=code,
                    period=freq.replace("min", ""),
                    adjust=kwargs.get("adjust", ""),
                )
                if df is not None and not df.empty:
                    return self._standardize_ohlcv(df)
            except Exception as e:
                logger.warning("[AkShare] 获取 %s 失败，尝试备用数据源: %s", symbol, e)

                if data_source_backup is not None:
                    try:
                        fallback_df = data_source_backup.get_stock_daily_with_fallback(
                            symbol,
                            start,
                            end,
                            adjust,
                            sources=["east_money", "tushare", "baostock"],
                        )
                        if fallback_df is not None and not fallback_df.empty:
                            df = self._standardize_ohlcv(fallback_df)
                            self._set_to_cache("market", "stock_daily", df, **cache_key)
                            return df
                    except Exception as fallback_error:
                        logger.warning(
                            "[Fallback] 备用数据源获取失败: %s", fallback_error
                        )

                raise DataErrorCode(str(e), source=self.name, symbol=symbol)

        raise SourceUnavailableError(
            "数据源不可用",
            error_code=ErrorCode.SOURCE_UNAVAILABLE,
            source=self.name,
            symbol=symbol,
        )

    def get_money_flow(
        self,
        symbol: str,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取资金流向数据"""
        symbol = self._normalize_symbol(symbol)

        # 尝试从 parquet_cache 获取
        where = {"symbol": symbol}
        if start_date:
            where["date"] = [
                self._normalize_date(start_date),
                self._normalize_date(end_date or datetime.now()),
            ]

        cached = self._parquet_get("money_flow", where=where)
        if cached is not None and not cached.empty:
            logger.debug(f"[parquet_cache] {symbol}: 使用缓存资金流")
            return cached

        self._load_market_data()

        if hasattr(self, "_get_money_flow"):
            try:
                df = self._get_money_flow(symbol)
                if not df.empty:
                    self._parquet_put("money_flow", df)
                return df
            except Exception as e:
                raise DataErrorCode(str(e), source=self.name, symbol=symbol)

        if self._akshare_available:
            try:
                code = (
                    symbol.replace("sh", "")
                    .replace("sz", "")
                    .replace(".XSHG", "")
                    .replace(".XSHE", "")
                )
                df = self._akshare.stock_individual_fund_flow(
                    stock=code, market="sh" if code.startswith("6") else "sz"
                )
                if df is not None and not df.empty:
                    self._parquet_put("money_flow", df)
                return df
            except Exception as e:
                raise DataErrorCode(str(e), source=self.name, symbol=symbol)

        raise DataSourceError("数据源不可用", source=self.name, symbol=symbol)

    def get_north_money_flow(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取北向资金流向"""
        # 尝试从 parquet_cache 获取
        where = {}
        if start_date:
            where["date"] = [
                self._normalize_date(start_date),
                self._normalize_date(end_date or datetime.now()),
            ]

        cached = self._parquet_get("north_flow", where=where)
        if cached is not None and not cached.empty:
            logger.debug(f"[parquet_cache] 使用缓存北向资金流")
            return cached

        self._load_market_data()

        if hasattr(self, "_get_north_money_flow"):
            try:
                df = self._get_north_money_flow()
                if not df.empty:
                    self._parquet_put("north_flow", df)
                return df
            except Exception as e:
                raise DataSourceError(str(e), source=self.name)

        if self._akshare_available:
            try:
                df = self._akshare.stock_hsgt_north_net_flow_in_em()
                if df is not None and not df.empty:
                    self._parquet_put("north_flow", df)
                return df
            except Exception as e:
                raise DataSourceError(str(e), source=self.name)

        raise DataSourceError("数据源不可用", source=self.name)

    def get_industry_stocks(
        self,
        industry_code: str,
        level: int = 1,
        **kwargs,
    ) -> List[str]:
        """获取行业成分股"""
        cached = self._parquet_get(
            "industry_components",
            where={"industry_code": industry_code},
        )
        if cached is not None and not cached.empty:
            if "symbol" in cached.columns:
                return cached["symbol"].dropna().tolist()

        self._load_market_data()

        if hasattr(self, "_get_industry_stocks_sw"):
            try:
                stocks = self._get_industry_stocks_sw(industry_code)
                if stocks:
                    df = pd.DataFrame(
                        {"industry_code": industry_code, "symbol": stocks}
                    )
                    self._parquet_put("industry_components", df)
                return stocks
            except Exception as e:
                logger.warning(f"market_data 获取失败: {e}")

        if self._akshare_available:
            try:
                code = industry_code.replace(".SI", "").zfill(6)
                df = self._akshare.index_component_sw(symbol=code)
                if df is not None and not df.empty:
                    stocks = []
                    code_col = None
                    for col in ["证券代码", "股票代码", "code", "symbol"]:
                        if col in df.columns:
                            code_col = col
                            break
                    if code_col:
                        for stock_code in df[code_col]:
                            code_str = str(stock_code).zfill(6)
                            if code_str.startswith("6"):
                                stocks.append(f"{code_str}.XSHG")
                            else:
                                stocks.append(f"{code_str}.XSHE")

                    if stocks:
                        cache_df = pd.DataFrame(
                            {"industry_code": industry_code, "symbol": stocks}
                        )
                        self._parquet_put("industry_components", cache_df)
                    return stocks
            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=industry_code)

        raise DataSourceError("数据源不可用", source=self.name, symbol=industry_code)

    def get_industry_mapping(
        self,
        symbol: str,
        level: int = 1,
        **kwargs,
    ) -> str:
        """获取股票所属行业"""
        symbol = (
            self._normalize_symbol(symbol)
            if "." in symbol or symbol.startswith(("sh", "sz"))
            else self._to_jq_format(symbol)
        )

        # 尝试从 parquet_cache 获取
        cached = self._parquet_get("industry_mapping", where={"symbol": symbol})
        if cached is not None and not cached.empty:
            if "industry_code" in cached.columns:
                return cached["industry_code"].iloc[0]

        self._load_market_data()

        if hasattr(self, "_get_all_industry_mapping"):
            try:
                mapping = self._get_all_industry_mapping()
                result = mapping.get(symbol, "")
                if result:
                    df = pd.DataFrame({"symbol": symbol, "industry_code": result})
                    self._parquet_put("industry_mapping", df)
                return result
            except Exception as e:
                logger.warning(f"获取行业映射失败: {e}")
                return ""

        return ""

    def get_finance_indicator(
        self,
        symbol: str,
        fields: Optional[List[str]] = None,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取财务指标数据"""
        symbol = (
            self._normalize_symbol(symbol)
            if "." in symbol or symbol.startswith(("sh", "sz"))
            else symbol
        )

        # 尝试从 parquet_cache 获取
        where = {"symbol": symbol}
        if start_date:
            where["report_date"] = [
                self._normalize_date(start_date),
                self._normalize_date(end_date or datetime.now()),
            ]

        cached = self._parquet_get("finance_indicator", where=where)
        if cached is not None and not cached.empty:
            logger.debug(f"[parquet_cache] {symbol}: 使用缓存财务指标")
            return cached

        # finance.finance 模块不存在 get_finance_indicator 函数
        # 直接使用 akshare 获取财务指标数据

        if self._akshare_available:
            try:
                code = (
                    symbol.replace("sh", "")
                    .replace("sz", "")
                    .replace(".XSHG", "")
                    .replace(".XSHE", "")
                )
                df = self._akshare.stock_financial_analysis_indicator(symbol=code)
                if not df.empty:
                    self._parquet_put("finance_indicator", df)
                return df
            except Exception as e:
                raise DataErrorCode(str(e), source=self.name, symbol=symbol)

        raise DataSourceError("数据源不可用", source=self.name, symbol=symbol)

    def get_call_auction(
        self,
        symbol: str,
        date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取集合竞价数据"""
        self._load_market_data()

        if hasattr(self, "_get_call_auction"):
            try:
                df = self._get_call_auction(symbol, date)
                return df
            except Exception as e:
                raise DataErrorCode(str(e), source=self.name, symbol=symbol)

        raise DataSourceError(
            f"{self.name} 不支持集合竞价数据", source=self.name, symbol=symbol
        )

    # ETF/指数日线复用 get_daily_data
    def get_etf_daily(
        self,
        symbol: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
        **kwargs,
    ) -> pd.DataFrame:
        """获取 ETF 日线数据"""
        symbol = self._normalize_symbol(symbol)
        start = self._normalize_date(start_date)
        end = self._normalize_date(end_date)

        # 尝试从 parquet_cache 获取
        cached = self._parquet_get(
            "etf_daily",
            where={"symbol": symbol, "date": [start, end]},
        )
        if cached is not None and not cached.empty:
            cached = cached.copy()
            if "date" in cached.columns or "datetime" in cached.columns:
                date_col = "date" if "date" in cached.columns else "datetime"
                cached[date_col] = pd.to_datetime(cached[date_col])
                cached = cached[
                    (cached[date_col] >= pd.to_datetime(start))
                    & (cached[date_col] <= pd.to_datetime(end))
                ]
            if not cached.empty:
                logger.debug(f"[parquet_cache] {symbol}: 使用缓存数据")
                return cached

        # 离线模式检查
        if self._offline_mode:
            raise SourceUnavailableError(
                "离线模式下无缓存数据",
                error_code=ErrorCode.SOURCE_UNAVAILABLE,
                source=self.name,
                symbol=symbol,
            )

        self._load_market_data()

        if hasattr(self, "_get_etf_daily"):
            try:
                df = self._get_etf_daily(symbol, start, end)
                if not df.empty:
                    self._parquet_put("etf_daily", df)
                return df
            except Exception as e:
                logger.warning(f"ETF 数据获取失败: {e}")

        return self.get_daily_data(symbol, start_date, end_date, adjust="", **kwargs)

    def get_index_daily(
        self,
        symbol: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
        **kwargs,
    ) -> pd.DataFrame:
        """获取指数日线数据"""
        symbol = self._normalize_symbol(symbol)
        start = self._normalize_date(start_date)
        end = self._normalize_date(end_date)

        # 尝试从 parquet_cache 获取
        cached = self._parquet_get(
            "index_daily",
            where={"symbol": symbol, "date": [start, end]},
        )
        if cached is not None and not cached.empty:
            cached = cached.copy()
            if "date" in cached.columns or "datetime" in cached.columns:
                date_col = "date" if "date" in cached.columns else "datetime"
                cached[date_col] = pd.to_datetime(cached[date_col])
                cached = cached[
                    (cached[date_col] >= pd.to_datetime(start))
                    & (cached[date_col] <= pd.to_datetime(end))
                ]
            if not cached.empty:
                logger.debug(f"[parquet_cache] {symbol}: 使用缓存数据")
                return cached

        # 离线模式检查
        if self._offline_mode:
            raise SourceUnavailableError(
                "离线模式下无缓存数据",
                error_code=ErrorCode.SOURCE_UNAVAILABLE,
                source=self.name,
                symbol=symbol,
            )

        self._load_market_data()

        if hasattr(self, "_get_index_daily"):
            try:
                df = self._get_index_daily(symbol, start, end)
                if not df.empty:
                    self._parquet_put("index_daily", df)
                return df
            except Exception as e:
                logger.warning(f"指数数据获取失败: {e}")

        return self.get_daily_data(symbol, start_date, end_date, adjust="", **kwargs)

    def get_source_info(self) -> Dict[str, Any]:
        """获取数据源信息"""
        return {
            "name": self.name,
            "type": self.source_type,
            "description": "AkShare 数据源适配器",
            "akshare_available": self._akshare_available,
            "cache_enabled": self._use_cache,
            "offline_mode": self._offline_mode,
            "data_sources": self._data_sources,
        }

    # ── ST/停牌 ───────────────────────────────────────────────────

    def get_st_stocks(self) -> pd.DataFrame:
        """获取 ST 股票列表"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_zh_a_st_em()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_suspended_stocks(self) -> pd.DataFrame:
        """获取停牌股票列表"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_zh_a_stop_em()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 估值 ──────────────────────────────────────────────────────

    def get_index_valuation(self, index_code: str) -> pd.DataFrame:
        """获取指数估值历史数据"""
        cached = self._parquet_get("valuation", where={"symbol": index_code})
        if cached is not None and not cached.empty:
            return cached

        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            csindex_code = (
                index_code.replace("000", "H30").zfill(6)
                if index_code.startswith("000")
                else index_code
            )
            result = self._akshare.stock_zh_index_value_csindex(symbol=csindex_code)
            if result is not None and not result.empty:
                result["symbol"] = index_code
                self._parquet_put("valuation", result)
            return result if result is not None else pd.DataFrame()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def _get_stock_valuation_em(self, symbol: str) -> pd.DataFrame:
        """获取个股估值数据（东方财富）"""
        symbol = self._normalize_symbol(symbol)

        cached = self._parquet_get("valuation", where={"symbol": symbol})
        if cached is not None and not cached.empty:
            return cached

        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            code = (
                symbol.replace("sh", "")
                .replace("sz", "")
                .replace(".XSHG", "")
                .replace(".XSHE", "")
                .zfill(6)
            )
            market = ".SH" if code.startswith("6") else ".SZ"
            ak_symbol = code + market
            result = self._akshare.stock_a_indicator_em(symbol=ak_symbol)
            if result is not None and not result.empty:
                result["symbol"] = symbol
                self._parquet_put("valuation", result)
            return result if result is not None else pd.DataFrame()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_stock_pe_pb(self, symbol: str) -> pd.DataFrame:
        """获取个股 PE/PB 数据"""
        symbol = self._normalize_symbol(symbol)

        cached = self._parquet_get("valuation", where={"symbol": symbol})
        if cached is not None and not cached.empty:
            return cached

        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            df_all = self._akshare.stock_a_all_pb()
            if df_all is None or df_all.empty:
                return pd.DataFrame()

            target_code = (
                symbol.replace("sh", "")
                .replace("sz", "")
                .replace(".XSHG", "")
                .replace(".XSHE", "")
                .zfill(6)
            )
            code_col = None
            for col in ["股票代码", "code", "symbol", "证券代码"]:
                if col in df_all.columns:
                    code_col = col
                    break

            if code_col:
                df_all["code_normalized"] = df_all[code_col].astype(str).str.zfill(6)
                result = df_all[df_all["code_normalized"] == target_code].copy()
                result = result.drop(columns=["code_normalized"])
                result["symbol"] = symbol
            else:
                result = df_all

            if not result.empty:
                self._parquet_put("valuation", result)
            return result
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 融资融券 ──────────────────────────────────────────────────

    def get_margin_detail(self, market: str, date: str) -> pd.DataFrame:
        """获取融资融券明细。market: 'sh' | 'sz'"""
        # 尝试从 parquet_cache 获取
        cached = self._parquet_get(
            "margin_detail", where={"market": market, "date": date}
        )
        if cached is not None and not cached.empty:
            return cached

        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            date_str = date.replace("-", "")
            if market == "sh":
                result = self._akshare.stock_margin_detail_sse(date=date_str)
            elif market == "sz":
                result = self._akshare.stock_margin_detail_szse(date=date_str)
            else:
                raise DataSourceError(f"不支持的市场: {market}", source=self.name)

            # 检查返回数据是否为空
            if result is None or result.empty:
                logger.warning(f"{market} {date}: 融资融券数据为空（可能是非交易日）")
                return pd.DataFrame()

            # 添加 market 和 date 列
            result["market"] = market
            result["date"] = date

            if not result.empty:
                self._parquet_put("margin_detail", result)
            return result
        except ValueError as e:
            # 处理 pandas 列赋值失败
            if "Length mismatch" in str(e):
                logger.warning(f"{market} {date}: akshare 返回数据格式异常")
                return pd.DataFrame()
            raise DataSourceError(str(e), source=self.name)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_margin_underlying(self, market: str) -> pd.DataFrame:
        """获取融资融券标的信息。market: 'sh' | 'sz'"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            if market == "sh":
                return self._akshare.stock_margin_underlying_info_sse()
            elif market == "sz":
                return self._akshare.stock_margin_underlying_info_szse()
            else:
                raise DataSourceError(f"不支持的市场: {market}", source=self.name)
        except DataSourceError:
            raise
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 宏观数据（原始，不含缓存）────────────────────────────────

    def get_macro_raw(self, indicator: str) -> pd.DataFrame:
        """获取宏观数据原始 DataFrame"""
        # 尝试从 parquet_cache 获取
        cached = self._parquet_get("macro_data", where={"indicator": indicator})
        if cached is not None and not cached.empty:
            return cached

        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        _indicator_map = {
            "pmi": self._akshare.macro_china_pmi,
            "cpi": self._akshare.macro_china_cpi,
            "ppi": self._akshare.macro_china_ppi,
            "gdp": self._akshare.macro_china_gdp,
            "m2": self._akshare.macro_china_m2_yearly,
            "interest_rate": self._akshare.macro_bank_china_interest_rate,
            "exchange_rate": self._akshare.macro_china_rmb,
            "rmb": self._akshare.macro_china_rmb,
        }
        fn = _indicator_map.get(indicator.lower())
        if fn is None:
            raise DataSourceError(f"不支持的宏观指标: {indicator}", source=self.name)
        try:
            result = fn()
            if not result.empty:
                result["indicator"] = indicator
                self._parquet_put("macro_data", result)
            return result
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 股东数据 ──────────────────────────────────────────────────

    def get_top10_holders(self, symbol: str) -> pd.DataFrame:
        """获取前十大股东数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_zh_a_gdhs(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_top10_holders_em(self, symbol: str) -> pd.DataFrame:
        """获取前十大股东数据（东方财富，stock_gdfx_holding_detail_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_gdfx_holding_detail_em(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_top10_float_holders(self, symbol: str) -> pd.DataFrame:
        """获取前十大流通股东数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_zh_a_gdhs_detail_em(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_top10_float_holders_em(self, symbol: str) -> pd.DataFrame:
        """获取前十大流通股东数据（东方财富，stock_gdfx_free_holding_detail_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_gdfx_free_holding_detail_em(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_holder_count(self, symbol: str) -> pd.DataFrame:
        """获取股东人数数据（stock_hold_num_cninfo）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_hold_num_cninfo(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_institutional_holders(self, symbol: str) -> pd.DataFrame:
        """获取机构持股数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_institute_hold(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 财务报表 ──────────────────────────────────────────────────

    def get_financial_report(self, symbol: str, report_type: str) -> pd.DataFrame:
        """获取财务报表。report_type: '现金流量表' | '资产负债表' | '利润表'"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_financial_report_sina(
                stock=symbol, symbol=report_type
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_financial_benefit(self, symbol: str, indicator: str) -> pd.DataFrame:
        """获取财务效益数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_financial_benefit_ths(
                symbol=symbol, indicator=indicator
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_cashflow(self, symbol: str) -> pd.DataFrame:
        """获取现金流数据"""
        symbol = (
            self._normalize_symbol(symbol)
            if "." in symbol or symbol.startswith(("sh", "sz"))
            else symbol
        )

        # 尝试从 parquet_cache 获取
        cached = self._parquet_get(
            "financial_report", where={"symbol": symbol, "report_type": "现金流量表"}
        )
        if cached is not None and not cached.empty:
            return cached

        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            result = self._akshare.stock_financial_report_sina(
                stock=symbol, symbol="现金流量表"
            )
            if not result.empty:
                self._parquet_put("financial_report", result)
            return result
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 分红/股本变动/解禁 ────────────────────────────────────────

    def get_dividend(self, symbol: str) -> pd.DataFrame:
        """获取分红数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_dividend_cninfo(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_dividend_fhps(self, symbol: str = None, date: str = None) -> pd.DataFrame:
        """获取分红送股数据"""
        # 尝试从 parquet_cache 获取
        where = {}
        if symbol:
            where["symbol"] = self._normalize_symbol(symbol)
        if date:
            where["announce_date"] = date

        cached = self._parquet_get("dividend", where=where)
        if cached is not None and not cached.empty:
            return cached

        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            # 获取指定日期的全市场分红数据
            if date is None:
                # 默认获取最近一个报告期（年报/半年报/季报）
                from datetime import datetime

                # 尝试最近的报告期日期
                today = datetime.now()
                for report_date in ["1231", "0630", "0930", "0331"]:
                    test_date = today.strftime("%Y") + report_date
                    try:
                        df_all = self._akshare.stock_fhps_em(date=test_date)
                        if df_all is not None and not df_all.empty:
                            break
                    except:
                        continue
            else:
                df_all = self._akshare.stock_fhps_em(date=date.replace("-", ""))

            if df_all is None or df_all.empty:
                return pd.DataFrame()

            # 如果指定了 symbol，过滤
            if symbol:
                symbol_norm = self._normalize_symbol(symbol)
                code_col = None
                for col in ["股票代码", "code", "symbol", "证券代码"]:
                    if col in df_all.columns:
                        code_col = col
                        break

                if code_col:
                    target_code = (
                        symbol_norm.replace("sh", "").replace("sz", "").zfill(6)
                    )
                    df_all["code_normalized"] = (
                        df_all[code_col].astype(str).str.zfill(6)
                    )
                    result = df_all[df_all["code_normalized"] == target_code].copy()
                    result = result.drop(columns=["code_normalized"])
                else:
                    result = df_all
            else:
                result = df_all

            if not result.empty:
                self._parquet_put("dividend", result)
            return result
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_dividend_all(self) -> pd.DataFrame:
        """获取全市场分红数据（不指定股票）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_dividend_cninfo()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_share_change(self, symbol: str) -> pd.DataFrame:
        """获取股本变动数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_share_change_cninfo(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_share_change_cninfo(
        self, symbol: str, start_date: str = None, end_date: str = None
    ) -> pd.DataFrame:
        """获取巨潮资讯股本变动数据（stock_share_change_cninfo）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            kwargs = {"symbol": symbol}
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            return self._akshare.stock_share_change_cninfo(**kwargs)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_shareholder_change_ths(self, symbol: str) -> pd.DataFrame:
        """获取同花顺股东变动数据（stock_shareholder_change_ths）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_shareholder_change_ths(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_holding_change_em(
        self, symbol: str = None, date: str = None
    ) -> pd.DataFrame:
        """获取东方财富股东增减持数据（stock_gdfx_holding_change_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            if symbol is not None:
                return self._akshare.stock_gdfx_holding_change_em(symbol=symbol)
            elif date is not None:
                return self._akshare.stock_gdfx_holding_change_em(date=date)
            else:
                return self._akshare.stock_gdfx_holding_change_em()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_pledge_ratio_em(self, symbol: str) -> pd.DataFrame:
        """获取股权质押比例数据"""
        symbol = self._normalize_symbol(symbol)

        # 尝试从 parquet_cache 获取
        cached = self._parquet_get("share_change", where={"symbol": symbol})
        if cached is not None and not cached.empty:
            return cached

        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            # 获取最新日期的全市场质押数据
            today = datetime.now().strftime("%Y%m%d")
            df_all = self._akshare.stock_gpzy_pledge_ratio_em(date=today)

            if df_all is None or df_all.empty:
                return pd.DataFrame()

            # 过滤指定 symbol（代码列可能是 '股票代码' 或类似字段）
            code_col = None
            for col in ["股票代码", "code", "symbol", "证券代码"]:
                if col in df_all.columns:
                    code_col = col
                    break

            if code_col:
                # 标准化代码格式进行比较
                target_code = symbol.replace("sh", "").replace("sz", "").zfill(6)
                df_all["code_normalized"] = df_all[code_col].astype(str).str.zfill(6)
                result = df_all[df_all["code_normalized"] == target_code].copy()
                result = result.drop(columns=["code_normalized"])
                result["symbol"] = symbol  # 确保有 symbol 列
            else:
                result = df_all  # 无法过滤，返回全量

            if not result.empty:
                self._parquet_put("share_change", result)
            return result
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_equity_mortgage_cninfo(self, symbol: str) -> pd.DataFrame:
        """获取巨潮资讯股权质押数据（stock_cg_equity_mortgage_cninfo）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_cg_equity_mortgage_cninfo(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_unlock_schedule(self, symbol: str) -> pd.DataFrame:
        """获取解禁计划数据"""
        symbol = self._normalize_symbol(symbol)

        # 尝试从 parquet_cache 获取
        cached = self._parquet_get("unlock", where={"symbol": symbol})
        if cached is not None and not cached.empty:
            return cached

        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            from datetime import timedelta

            start = datetime.now().strftime("%Y%m%d")
            end = (datetime.now() + timedelta(days=90)).strftime("%Y%m%d")

            df_all = self._akshare.stock_restricted_release_detail_em(
                start_date=start, end_date=end
            )

            if df_all is None or df_all.empty:
                return pd.DataFrame()

            code_col = None
            for col in ["股票代码", "code", "symbol", "证券代码"]:
                if col in df_all.columns:
                    code_col = col
                    break

            if code_col:
                target_code = symbol.replace("sh", "").replace("sz", "").zfill(6)
                df_all["code_normalized"] = df_all[code_col].astype(str).str.zfill(6)
                result = df_all[df_all["code_normalized"] == target_code].copy()
                result = result.drop(columns=["code_normalized"])
                result["symbol"] = symbol
            else:
                result = df_all

            if not result.empty:
                self._parquet_put("unlock", result)
            return result
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_unlock_queue_sina(self, symbol: str) -> pd.DataFrame:
        """获取新浪限售股解禁排队数据（stock_restricted_release_queue_sina）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_restricted_release_queue_sina(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_unlock_summary_em(self, symbol: str) -> pd.DataFrame:
        """获取东方财富限售股解禁汇总数据（stock_restricted_release_summary_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_restricted_release_summary_em(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_unlock_detail_em(self, start_date: str, end_date: str) -> pd.DataFrame:
        """获取东方财富限售股解禁明细数据（stock_restricted_release_detail_em by date range）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_restricted_release_detail_em(
                start_date=start_date, end_date=end_date
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 行情扩展 ──────────────────────────────────────────────────

    def get_spot_em(self) -> pd.DataFrame:
        """获取全市场实时行情"""
        if not self._akshare_available:
            raise SourceUnavailableError(
                "akshare 不可用",
                error_code=ErrorCode.SOURCE_UNAVAILABLE,
                source=self.name,
            )
        try:
            import time

            compat = self._get_compat_adapter()
            start_time = time.time()
            result = compat.call("stock_zh_a_spot_em")
            duration_ms = (time.time() - start_time) * 1000
            self._record_request(
                "akshare", duration_ms, True, endpoint="stock_zh_a_spot_em"
            )
            return result
        except Exception as e:
            self._record_request(
                "akshare",
                0,
                False,
                error_type=type(e).__name__,
                endpoint="stock_zh_a_spot_em",
            )
            raise SourceUnavailableError(
                str(e), error_code=ErrorCode.SOURCE_TIMEOUT, source=self.name
            )

    def get_stock_hist(
        self,
        symbol: str,
        period: str = "daily",
        start_date: str = "",
        end_date: str = "",
        adjust: str = "",
    ) -> pd.DataFrame:
        """获取股票历史行情"""
        if not self._akshare_available:
            raise SourceUnavailableError(
                "akshare 不可用",
                error_code=ErrorCode.SOURCE_UNAVAILABLE,
                source=self.name,
            )
        try:
            import time

            compat = self._get_compat_adapter()
            start_time = time.time()
            result = compat.call(
                "stock_zh_a_hist",
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust=adjust,
            )
            duration_ms = (time.time() - start_time) * 1000
            self._record_request(
                "akshare", duration_ms, True, endpoint="stock_zh_a_hist"
            )
            return result
        except Exception as e:
            self._record_request(
                "akshare",
                0,
                False,
                error_type=type(e).__name__,
                endpoint="stock_zh_a_hist",
            )
            raise SourceUnavailableError(
                str(e), error_code=ErrorCode.SOURCE_TIMEOUT, source=self.name
            )

    def get_trade_dates(self) -> pd.DataFrame:
        """获取交易日历 DataFrame"""
        if not self._akshare_available:
            raise SourceUnavailableError(
                "akshare 不可用",
                error_code=ErrorCode.SOURCE_UNAVAILABLE,
                source=self.name,
            )
        try:
            import time

            compat = self._get_compat_adapter()
            start_time = time.time()
            result = compat.call("tool_trade_date_hist_sina")
            duration_ms = (time.time() - start_time) * 1000
            self._record_request(
                "akshare", duration_ms, True, endpoint="tool_trade_date_hist_sina"
            )
            return result
        except Exception as e:
            self._record_request(
                "akshare",
                0,
                False,
                error_type=type(e).__name__,
                endpoint="tool_trade_date_hist_sina",
            )
            raise SourceUnavailableError(
                str(e), error_code=ErrorCode.SOURCE_TIMEOUT, source=self.name
            )

    def get_securities_code_name(self) -> pd.DataFrame:
        """获取 A 股代码名称映射"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            import time

            compat = self._get_compat_adapter()
            start_time = time.time()
            result = compat.call("stock_info_a_code_name")
            duration_ms = (time.time() - start_time) * 1000
            self._record_request(
                "akshare", duration_ms, True, endpoint="stock_info_a_code_name"
            )
            return result
        except Exception as e:
            self._record_request(
                "akshare",
                0,
                False,
                error_type=type(e).__name__,
                endpoint="stock_info_a_code_name",
            )
            raise DataSourceError(str(e), source=self.name)

    def get_bond_yield(self, start_date: str = "", end_date: str = "") -> pd.DataFrame:
        """获取债券收益率数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            kwargs = {}
            if start_date:
                kwargs["start_date"] = start_date
            if end_date:
                kwargs["end_date"] = end_date
            return self._akshare.bond_china_yield(**kwargs)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_stock_valuation_baidu(self, symbol: str, indicator: str) -> pd.DataFrame:
        """获取百度股票估值数据（stock_zh_valuation_baidu）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_zh_valuation_baidu(
                symbol=symbol, indicator=indicator
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_stock_individual_info(self, symbol: str) -> pd.DataFrame:
        """获取个股基本信息（stock_individual_info_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_individual_info_em(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_stock_valuation(self, symbol: str) -> pd.DataFrame:
        """
        获取个股估值数据，支持多数据源自动切换（BAIDU→EASTMONEY→THS）。

        Returns DataFrame with columns: date, market_cap, pe_ratio, pb_ratio,
        circulating_market_cap, pe_ratio_ttm
        """
        router = MultiSourceRouter(
            providers=[
                ("baidu", lambda: self._fetch_valuation_baidu(symbol)),
                ("eastmoney", lambda: self._fetch_valuation_eastmoney(symbol)),
                ("ths", lambda: self._fetch_valuation_ths(symbol)),
            ],
            required_columns=["date"],
            min_rows=1,
        )
        result = router.execute()
        if not result.success:
            raise DataSourceError(
                result.error or "all sources failed", source=result.source or "all"
            )
        return result.data

    get_stock_valuation_with_fallback = get_stock_valuation

    def _fetch_valuation_baidu(self, symbol: str) -> pd.DataFrame:
        """从百度估值接口获取数据"""
        symbol_norm = (
            symbol.replace("sh", "")
            .replace("sz", "")
            .replace(".XSHG", "")
            .replace(".XSHE", "")
            .zfill(6)
        )

        indicators = [
            ("总市值", "market_cap"),
            ("市净率", "pb_ratio"),
            ("市盈率", "pe_ratio"),
        ]

        dfs = []
        for indicator, col_name in indicators:
            try:
                df = self.get_stock_valuation_baidu(
                    symbol=symbol_norm, indicator=indicator
                )
                if df is not None and not df.empty:
                    df = df.rename(columns={"value": col_name})
                    dfs.append(df)
            except Exception as e:
                warnings.warn(f"百度接口获取 {indicator} 失败: {e}")

        if not dfs:
            return pd.DataFrame()

        result = reduce(lambda x, y: pd.merge(x, y, on="date", how="outer"), dfs)
        if "date" in result.columns:
            result["date"] = pd.to_datetime(result["date"]).dt.strftime("%Y-%m-%d")
        return result.sort_values("date").reset_index(drop=True)

    def _fetch_valuation_eastmoney(self, symbol: str) -> pd.DataFrame:
        """从东财估值接口获取数据"""
        symbol_norm = (
            symbol.replace("sh", "")
            .replace("sz", "")
            .replace(".XSHG", "")
            .replace(".XSHE", "")
            .zfill(6)
        )

        df = self.get_stock_valuation(symbol=symbol_norm)
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

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
            df = df.sort_values("date").reset_index(drop=True)

        return df

    def _fetch_valuation_ths(self, symbol: str) -> pd.DataFrame:
        """从同花顺接口获取估值数据"""
        symbol_norm = (
            symbol.replace("sh", "")
            .replace("sz", "")
            .replace(".XSHG", "")
            .replace(".XSHE", "")
            .zfill(6)
        )

        df = self.get_stock_individual_info(symbol=symbol_norm)
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

    def get_futures_main_sina(
        self,
        symbol: str,
        start_date: str = "19900101",
        end_date: str = "22220101",
    ) -> pd.DataFrame:
        """获取期货主力合约数据（futures_main_sina）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.futures_main_sina(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_index_daily_raw(self, symbol: str) -> pd.DataFrame:
        """直接获取指数日线数据（返回 akshare 原始 DataFrame）"""
        if not self._akshare_available:
            raise SourceUnavailableError(
                "akshare 不可用",
                error_code=ErrorCode.SOURCE_UNAVAILABLE,
                source=self.name,
            )
        try:
            import time

            compat = self._get_compat_adapter()
            start_time = time.time()
            result = compat.call("stock_zh_index_daily", symbol=symbol)
            duration_ms = (time.time() - start_time) * 1000
            self._record_request(
                "akshare", duration_ms, True, endpoint="stock_zh_index_daily"
            )
            return result
        except Exception as e:
            self._record_request(
                "akshare",
                0,
                False,
                error_type=type(e).__name__,
                endpoint="stock_zh_index_daily",
            )
            raise SourceUnavailableError(
                str(e), error_code=ErrorCode.SOURCE_TIMEOUT, source=self.name
            )

    def get_index_zh_a_hist(self, symbol: str, period: str = "daily") -> pd.DataFrame:
        """获取指数A股历史行情（index_zh_a_hist）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            import time

            compat = self._get_compat_adapter()
            start_time = time.time()
            result = compat.call("index_zh_a_hist", symbol=symbol, period=period)
            duration_ms = (time.time() - start_time) * 1000
            self._record_request(
                "akshare", duration_ms, True, endpoint="index_zh_a_hist"
            )
            return result
        except Exception as e:
            self._record_request(
                "akshare",
                0,
                False,
                error_type=type(e).__name__,
                endpoint="index_zh_a_hist",
            )
            raise DataSourceError(str(e), source=self.name)

    def get_financial_analysis_indicator(self, symbol: str) -> pd.DataFrame:
        """获取财务分析指标数据（stock_financial_analysis_indicator）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_financial_analysis_indicator(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 行业/概念 ─────────────────────────────────────────────────

    def get_industry_list(self, source: str = "em") -> pd.DataFrame:
        """获取行业列表"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            if source == "em":
                return self._akshare.stock_board_industry_name_em()
            else:
                raise DataSourceError(f"不支持的行业数据源: {source}", source=self.name)
        except DataSourceError:
            raise
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_industry_components(
        self, industry_name: str, source: str = "em"
    ) -> pd.DataFrame:
        """获取行业成分股"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            if source == "em":
                return self._akshare.stock_board_industry_cons_em(symbol=industry_name)
            else:
                raise DataSourceError(f"不支持的行业数据源: {source}", source=self.name)
        except DataSourceError:
            raise
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_concept_list(
        self, use_cache: bool = True, cache_ttl_hours: int = 24
    ) -> pd.DataFrame:
        """获取概念板块列表，支持磁盘缓存"""
        cache_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "..",
            "data",
            "cache",
            "concept_list.json",
        )
        cache_file = os.path.normpath(cache_file)

        if use_cache and os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                cached_time = cached.get("timestamp", 0)
                now = time.time()
                if (now - cached_time) < cache_ttl_hours * 3600:
                    df = pd.DataFrame(cached.get("data", []))
                    if not df.empty:
                        return df
            except Exception:
                pass

        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            df = self._akshare.stock_board_concept_name_em()
            if use_cache and df is not None and not df.empty:
                try:
                    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                    cache_data = {
                        "timestamp": time.time(),
                        "data": df.to_dict(orient="records"),
                    }
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(cache_data, f, ensure_ascii=False, default=str)
                except Exception as e:
                    logger.debug(f"概念列表缓存写入失败: {e}")
            return df
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_concept_components(self, concept_name: str) -> pd.DataFrame:
        """获取概念板块成分股"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_board_concept_cons_em(symbol=concept_name)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_sw_industry(
        self, level: str = "1", use_cache: bool = True, cache_ttl_hours: int = 168
    ) -> pd.DataFrame:
        """获取申万行业数据，支持磁盘缓存（默认缓存7天）"""
        cache_file = os.path.join("data_cache", f"sw_industry_l{level}.json")
        cache_file = os.path.normpath(cache_file)

        if use_cache and os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                cached_time = cached.get("timestamp", 0)
                now = time.time()
                if (now - cached_time) < cache_ttl_hours * 3600:
                    df = pd.DataFrame(cached.get("data", []))
                    if not df.empty:
                        return df
            except Exception:
                pass

        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            df = self._akshare.sw_index_first_info()
            if use_cache and df is not None and not df.empty:
                try:
                    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                    cache_data = {
                        "timestamp": time.time(),
                        "data": df.to_dict(orient="records"),
                    }
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(cache_data, f, ensure_ascii=False, default=str)
                except Exception as e:
                    logger.debug(f"行业列表缓存写入失败: {e}")
            return df
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── ETF/LOF/可转债/期货/期权 ──────────────────────────────────

    def get_etf_hist(self, symbol: str) -> pd.DataFrame:
        """获取 ETF 历史行情"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.fund_etf_hist_em(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_lof_hist(self, symbol: str) -> pd.DataFrame:
        """获取 LOF 历史行情"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.fund_lof_hist_em(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_conversion_bond_list(self, **kwargs) -> pd.DataFrame:
        """获取可转债列表"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.bond_zh_cov()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_conversion_bond_daily(self, symbol: str) -> pd.DataFrame:
        """获取可转债日线数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.bond_zh_cov_daily(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def _fetch_futures_daily_sina(self, contract_code: str) -> pd.DataFrame:
        """获取期货日线数据（sina源）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.futures_zh_daily_sina(symbol=contract_code)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_futures_daily(
        self,
        symbol: str,
        start_date: str = None,
        end_date: str = None,
    ) -> pd.DataFrame:
        """
        获取期货日线数据，支持多数据源自动切换。

        Parameters
        ----------
        symbol : str
            期货代码（如 IF2401, AU9999）
        start_date : str, optional
            开始日期（YYYYMMDD格式）
        end_date : str, optional
            结束日期（YYYYMMDD格式）

        Returns
        -------
        pd.DataFrame
            包含 datetime, open, high, low, close, volume, money, openinterest 字段
        """
        if not self._akshare_available:
            return pd.DataFrame()

        def _jq_futures_to_sina(sym):
            """将聚宽风格期货代码转换为新浪期货符号"""
            sym = sym.upper()
            for ex in [".CCFX", ".XSGE", ".XDCE", ".XZCE", ".XINE", ".GFEX"]:
                if sym.endswith(ex):
                    code = sym[: -len(ex)]
                    break
            else:
                code = sym
            if code.endswith("9999"):
                variety = code[:-4]
                return variety + "0"
            return code

        def _standardize_futures(df):
            """标准化期货数据格式"""
            if df is None or df.empty:
                return pd.DataFrame()
            col_map = {
                "date": "datetime",
                "open": "open",
                "high": "high",
                "low": "low",
                "close": "close",
                "volume": "volume",
            }
            df = df.rename(columns=col_map)
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
            df = df.dropna(subset=["datetime"])
            df["money"] = None
            if "hold" in df.columns:
                df["openinterest"] = df["hold"]
            elif "持仓量" in df.columns:
                df["openinterest"] = df["持仓量"]
            if start_date:
                start_dt = pd.to_datetime(start_date)
                df = df[df["datetime"] >= start_dt]
            if end_date:
                end_dt = pd.to_datetime(end_date)
                df = df[df["datetime"] <= end_dt]
            return df.sort_values("datetime").reset_index(drop=True)

        sina_symbol = _jq_futures_to_sina(symbol)
        is_continuous = sina_symbol.endswith("0")

        providers = [
            (
                "sina",
                lambda: _standardize_futures(
                    self._fetch_futures_daily_sina(sina_symbol)
                ),
            ),
        ]

        if is_continuous:

            def main_fetcher():
                return self.get_futures_main_sina(
                    symbol=sina_symbol,
                    start_date=start_date or "19900101",
                    end_date=end_date or "22220101",
                )

            providers.append(("main_sina", main_fetcher))

        router = MultiSourceRouter(
            providers=providers,
            min_rows=1,
        )
        result = router.execute()
        if not result.success:
            return pd.DataFrame()
        return result.data

    get_futures_daily_with_fallback = get_futures_daily

    def get_option_daily(self, option_code: str) -> pd.DataFrame:
        """获取期权日线数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.option_finance_board(symbol=option_code)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 龙虎榜/公司信息/预测 ─────────────────────────────────────

    def get_billboard_list(self, start_date: str, end_date: str = None) -> pd.DataFrame:
        """获取龙虎榜数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            if end_date is None:
                end_date = start_date
            return self._akshare.stock_lhb_detail_em(
                start_date=start_date, end_date=end_date
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_company_info(self, symbol: str) -> pd.DataFrame:
        """获取公司基本信息"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_individual_info_em(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_company_industry_em(self, symbol: str) -> pd.DataFrame:
        """获取公司行业信息（stock_board_industry_name_em by symbol）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_board_industry_name_em(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_suspension_em(self, date: str) -> pd.DataFrame:
        """获取停牌数据（stock_tfp_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_tfp_em(date=date)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_stock_info_sh_name_code(self, symbol: str = "sh") -> pd.DataFrame:
        """获取上交所股票代码名称（stock_info_sh_name_code）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_info_sh_name_code(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_stock_info_sz_name_code(self, symbol: str = "sz") -> pd.DataFrame:
        """获取深交所股票代码名称（stock_info_sz_name_code）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_info_sz_name_code(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_forecast(self, symbol: str) -> pd.DataFrame:
        """获取业绩预告数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_profit_forecast(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_forecast_ths(self, symbol: str, indicator: str) -> pd.DataFrame:
        """获取同花顺业绩预告数据（stock_profit_forecast_ths）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_profit_forecast_ths(
                symbol=symbol, indicator=indicator
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 资金流向（板块/排名）─────────────────────────────────────

    def get_sector_money_flow(
        self, sector_type: str = "industry", indicator: str = "今日"
    ) -> pd.DataFrame:
        """获取板块资金流向排名。sector_type: 'industry' | 'concept'"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            if sector_type == "industry":
                return self._akshare.stock_board_industry_fund_flow_rank(
                    indicator=indicator
                )
            elif sector_type == "concept":
                return self._akshare.stock_board_concept_fund_flow_rank(
                    indicator=indicator
                )
            else:
                raise DataSourceError(
                    f"不支持的板块类型: {sector_type}", source=self.name
                )
        except DataSourceError:
            raise
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_individual_fund_flow(self, symbol: str, market: str = "sh") -> pd.DataFrame:
        """获取个股资金流向历史数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_individual_fund_flow(stock=symbol, market=market)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_individual_fund_flow_rank(self, indicator: str = "今日") -> pd.DataFrame:
        """获取个股资金流向排名"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_individual_fund_flow_rank(indicator=indicator)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 解禁汇总/基金信息 ─────────────────────────────────────────

    def get_unlock_summary(self) -> pd.DataFrame:
        """获取全市场限售股解禁汇总数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_restricted_release_summary_em()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_fund_name_list(self) -> pd.DataFrame:
        """获取基金名称列表"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.fund_name_em()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_fund_hold_stock(self, symbol: str) -> pd.DataFrame:
        """获取基金持股数据"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_fund_hold_stock(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 场外基金 ──────────────────────────────────────────────────

    def get_fund_of_nav(self, symbol: str) -> pd.DataFrame:
        """获取场外基金历史净值（fund_etf_fund_info_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.fund_etf_fund_info_em(fund=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_fund_open_daily(self) -> pd.DataFrame:
        """获取场外基金当日净值列表（fund_open_fund_daily_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.fund_open_fund_daily_em()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_fund_open_info(self, symbol: str) -> pd.DataFrame:
        """获取场外基金基本信息（fund_open_fund_info_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.fund_open_fund_info_em(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_fund_net_value_hist(
        self, fund_code: str, indicator: str = "单位净值走势"
    ) -> pd.DataFrame:
        """获取基金历史净值（fund_open_fund_info_em with indicator）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.fund_open_fund_info_em(
                fund=fund_code, indicator=indicator
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_fund_portfolio(self, fund_code: str) -> pd.DataFrame:
        """获取基金持仓数据（fund_portfolio_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.fund_portfolio_em(fund=fund_code)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_fund_dividend(self, fund_code: str) -> pd.DataFrame:
        """获取基金分红拆分数据（fund_individual_basic_info_xq with 分红拆分）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.fund_individual_basic_info_xq(
                symbol=fund_code, indicator="分红拆分"
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── LOF 扩展 ──────────────────────────────────────────────────

    def get_lof_spot(self) -> pd.DataFrame:
        """获取 LOF 实时行情列表（fund_lof_spot_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.fund_lof_spot_em()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_lof_hist_min(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        period: str,
        adjust: str = "",
    ) -> pd.DataFrame:
        """获取 LOF 分钟行情（fund_lof_hist_min_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.fund_lof_hist_min_em(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                period=period,
                adjust=adjust,
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 期货扩展 ──────────────────────────────────────────────────

    def get_futures_spot(self) -> pd.DataFrame:
        """获取期货实时行情（futures_zh_spot）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.futures_zh_spot()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_futures_main_em(self, symbol: str) -> pd.DataFrame:
        """获取期货主力合约行情（futures_main_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.futures_main_em(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_futures_sina_main(self, symbol: str) -> pd.DataFrame:
        """获取新浪期货主力合约（futures_sina_main_sina）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.futures_sina_main_sina(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_futures_display_main(self, symbol: str) -> pd.DataFrame:
        """获取期货合约列表（futures_display_main_sina）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.futures_display_main_sina(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 北向资金 ──────────────────────────────────────────────────

    def get_hsgt_north_net_flow(self, symbol: str = "北上") -> pd.DataFrame:
        """获取北向资金净流入（stock_em_hsgt_north_net_flow_in）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_em_hsgt_north_net_flow_in(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_hsgt_hold_stock(
        self, symbol: str = "北向", indicator: str = "今日"
    ) -> pd.DataFrame:
        """获取北向资金持股统计（stock_em_hsgt_hold_stock）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_em_hsgt_hold_stock(
                symbol=symbol, indicator=indicator
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_hsgt_individual_stock_flow(
        self, stock: str, indicator: str = "北向资金"
    ) -> pd.DataFrame:
        """获取个股北向资金流入（stock_em_hsgt_individual_stock_flow）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_em_hsgt_individual_stock_flow(
                stock=stock, indicator=indicator
            )
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 分钟数据 ──────────────────────────────────────────────────

    def get_stock_minute_raw(
        self,
        symbol: str,
        period: str,
        start_date: str,
        end_date: str,
        adjust: str = "",
    ) -> pd.DataFrame:
        """获取股票分钟行情（stock_zh_a_hist_min_em）"""
        if not self._akshare_available:
            raise SourceUnavailableError(
                "akshare 不可用",
                error_code=ErrorCode.SOURCE_UNAVAILABLE,
                source=self.name,
            )
        try:
            import time

            compat = self._get_compat_adapter()
            start_time = time.time()
            result = compat.call(
                "stock_zh_a_hist_min_em",
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust=adjust,
            )
            duration_ms = (time.time() - start_time) * 1000
            self._record_request(
                "akshare", duration_ms, True, endpoint="stock_zh_a_hist_min_em"
            )
            return result
        except Exception as e:
            self._record_request(
                "akshare",
                0,
                False,
                error_type=type(e).__name__,
                endpoint="stock_zh_a_hist_min_em",
            )
            raise SourceUnavailableError(
                str(e), error_code=ErrorCode.SOURCE_TIMEOUT, source=self.name
            )

    def get_etf_minute_raw(
        self,
        symbol: str,
        period: str,
        start_date: str,
        end_date: str,
        adjust: str = "qfq",
    ) -> pd.DataFrame:
        """获取 ETF 分钟行情（fund_etf_hist_min_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            import time

            compat = self._get_compat_adapter()
            start_time = time.time()
            result = compat.call(
                "fund_etf_hist_min_em",
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust=adjust,
            )
            duration_ms = (time.time() - start_time) * 1000
            self._record_request(
                "akshare", duration_ms, True, endpoint="fund_etf_hist_min_em"
            )
            return result
        except Exception as e:
            self._record_request(
                "akshare",
                0,
                False,
                error_type=type(e).__name__,
                endpoint="fund_etf_hist_min_em",
            )
            raise DataSourceError(str(e), source=self.name)

    # ── 指数成分扩展 ──────────────────────────────────────────────

    def get_index_stock_info(self) -> pd.DataFrame:
        """获取指数基本信息列表（index_stock_info）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.index_stock_info()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_index_component_sw(self, symbol: str) -> pd.DataFrame:
        """获取申万行业指数成分股（index_component_sw）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.index_component_sw(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_index_stock_cons(self, symbol: str) -> pd.DataFrame:
        """获取指数成分股（index_stock_cons）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.index_stock_cons(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_index_stock_cons_weight_csindex(self, symbol: str) -> pd.DataFrame:
        """获取中证指数成分股及权重（index_stock_cons_weight_csindex）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.index_stock_cons_weight_csindex(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_index_components(self, symbol: str) -> pd.DataFrame:
        """获取指数成分股及权重（统一接口，带 fallback）

        优先级: csindex -> sina
        csindex 优先因为包含权重信息，sina 仅在 csindex 不可用时使用（等权重）
        """
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)

        try:
            return self._akshare.index_stock_cons_weight_csindex(symbol=symbol)
        except Exception:
            pass

        try:
            df = self._akshare.index_stock_cons(symbol=symbol)
            if df is not None and not df.empty:
                df = df.copy()
                df["权重"] = 100.0 / len(df)
                logger.info(
                    f"[fallback] sina 成功获取 {symbol} 成分股: {len(df)} 只 (等权重)"
                )
            return df
        except Exception:
            pass

        raise DataSourceError(f"无法获取指数 {symbol} 成分股", source=self.name)

    # ── 申万行业扩展 ──────────────────────────────────────────────

    def get_sw_index_info(self) -> pd.DataFrame:
        """获取申万行业指数信息（sw_index_info）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.sw_index_info()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_sw_index_cons(self, index_code: str) -> pd.DataFrame:
        """获取申万行业指数成分股（sw_index_cons）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.sw_index_cons(index_code=index_code)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_sw_index_daily(self, index_code: str) -> pd.DataFrame:
        """获取申万行业指数日线行情（sw_index_daily）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.sw_index_daily(index_code=index_code)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_sw_index_daily_spot(self) -> pd.DataFrame:
        """获取申万行业指数实时行情（sw_index_daily_spot）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.sw_index_daily_spot()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 期权扩展 ──────────────────────────────────────────────────

    def get_option_current_day_sse(self) -> pd.DataFrame:
        """获取上交所期权当日行情（option_current_day_sse）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.option_current_day_sse()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_option_current_day_szse(self) -> pd.DataFrame:
        """获取深交所期权当日行情（option_current_day_szse）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.option_current_day_szse()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_option_cffex_hs300_spot(self) -> pd.DataFrame:
        """获取中金所沪深300期权行情（option_cffex_hs300_spot_sina）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.option_cffex_hs300_spot_sina()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_option_sse_greeks(self, symbol: str) -> pd.DataFrame:
        """获取上交所期权希腊字母（option_sse_greeks_sina）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.option_sse_greeks_sina(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_option_sse_daily(self, symbol: str) -> pd.DataFrame:
        """获取上交所期权日线数据（option_sse_daily_sina）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.option_sse_daily_sina(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 可转债扩展 ────────────────────────────────────────────────

    def get_call_auction_raw(
        self,
        symbol: str,
        start_time: str = "09:15:00",
        end_time: str = "09:25:00",
    ) -> pd.DataFrame:
        """获取集合竞价原始数据（stock_zh_a_hist_pre_min_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            code = (
                symbol.replace("sh", "")
                .replace("sz", "")
                .replace(".XSHG", "")
                .replace(".XSHE", "")
            )
            return self._akshare.stock_zh_a_hist_pre_min_em(
                symbol=code,
                start_time=start_time,
                end_time=end_time,
            )
        except Exception as e:
            raise DataErrorCode(str(e), source=self.name, symbol=symbol)

    def get_bond_cb_jsl(self) -> pd.DataFrame:
        """获取可转债数据（bond_cb_jsl）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.bond_cb_jsl()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_bond_zh_hs_daily(self, symbol: str) -> pd.DataFrame:
        """获取可转债历史行情（bond_zh_hs_daily）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.bond_zh_hs_daily(symbol=symbol)
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_ah_stock_list(self) -> pd.DataFrame:
        """获取AH股对照列表（stock_hk_ah_name_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_hk_ah_name_em()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    def get_ah_stock_spot(self) -> pd.DataFrame:
        """获取AH股实时行情（stock_hk_ah_spot_em）"""
        if not self._akshare_available:
            raise DataSourceError("akshare 不可用", source=self.name)
        try:
            return self._akshare.stock_hk_ah_spot_em()
        except Exception as e:
            raise DataSourceError(str(e), source=self.name)

    # ── 多数据源 Fallback 封装 ──────────────────────────────────────

    def get_unlock_with_fallback(self, symbol: str) -> list:
        """获取限售股解禁数据（多数据源 fallback）

        Returns:
            list of (source_name, DataFrame) tuples.
            优先级: get_unlock_queue_sina -> get_unlock_summary_em
        """
        results = []

        try:
            df_queue = self.get_unlock_queue_sina(symbol=symbol)
            if df_queue is not None and not df_queue.empty:
                results.append(("sina_queue", df_queue))
        except Exception as e:
            logger.debug(f"get_unlock_queue_sina 失败: {e}")

        try:
            df_summary = self.get_unlock_summary_em(symbol=symbol)
            if df_summary is not None and not df_summary.empty:
                results.append(("em_summary", df_summary))
        except Exception as e:
            logger.debug(f"get_unlock_summary_em 失败: {e}")

        return results

    def get_top10_shareholders(self, symbol: str) -> pd.DataFrame:
        """获取前十大股东数据（多数据源 fallback）

        优先级: get_top10_holders_em -> get_top10_holders
        """
        router = MultiSourceRouter(
            providers=[
                ("em", lambda: self.get_top10_holders_em(symbol=symbol)),
                ("tushare", lambda: self.get_top10_holders(symbol=symbol)),
            ],
            min_rows=1,
        )
        result = router.execute()
        if not result.success:
            return pd.DataFrame()
        return result.data

    get_top10_shareholders_with_fallback = get_top10_shareholders

    def get_shareholders(self, symbol: str) -> pd.DataFrame:
        """获取股东数据（多数据源 fallback）

        优先级: get_top10_holders -> get_share_change
        """
        router = MultiSourceRouter(
            providers=[
                ("tushare", lambda: self.get_top10_holders(symbol=symbol)),
                ("cninfo", lambda: self.get_share_change(symbol=symbol)),
            ],
            min_rows=1,
        )
        result = router.execute()
        if not result.success:
            return pd.DataFrame()
        return result.data

    get_shareholders_with_fallback = get_shareholders

    def get_shareholder_changes(
        self, symbol: str, start_date: str = None, end_date: str = None
    ) -> pd.DataFrame:
        """获取股东增减持数据（多数据源 fallback）

        优先级: get_holding_change_em -> get_share_change_cninfo
        """

        def make_cninfo_fetcher():
            if start_date is None:
                from datetime import datetime, timedelta

                end_date_str = datetime.now().strftime("%Y%m%d")
                start_date_str = (datetime.now() - timedelta(days=365)).strftime(
                    "%Y%m%d"
                )
            else:
                start_date_str = start_date
                end_date_str = end_date or datetime.now().strftime("%Y%m%d")
            return self.get_share_change_cninfo(
                symbol=symbol, start_date=start_date_str, end_date=end_date_str
            )

        router = MultiSourceRouter(
            providers=[
                ("em", lambda: self.get_holding_change_em(symbol=symbol)),
                ("cninfo", make_cninfo_fetcher),
            ],
            min_rows=1,
        )
        result = router.execute()
        if not result.success:
            return pd.DataFrame()
        return result.data

    get_shareholder_changes_with_fallback = get_shareholder_changes


__all__ = ["AkShareAdapter"]
