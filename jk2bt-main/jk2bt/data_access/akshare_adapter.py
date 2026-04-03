"""
src/data_access/akshare_adapter.py
AkShare 数据源适配器 - 实现 DataSource 接口。

整合现有的 market_data 模块，提供统一的数据访问接口。
支持缓存、多数据源备份、错误重试等特性。
"""

import logging
import time
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union
import pandas as pd

from .data_source import DataSource, DataSourceError
from .cache_manager import get_cache

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

    # 数据源优先级配置
    DEFAULT_DATA_SOURCES = ["sina", "east_money", "tushare", "baostock"]

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
            import akshare
            self._akshare = akshare
            self._akshare_available = True
        except ImportError:
            logger.warning("akshare 未安装，将仅使用缓存数据")

        # 按需导入 market_data 模块
        self._market_data_loaded = False

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
        # 去除前缀
        symbol = str(symbol)
        if symbol.startswith("sh"):
            return symbol
        if symbol.startswith("sz"):
            return symbol
        # 聚宽格式转换
        if ".XSHG" in symbol:
            return "sh" + symbol.replace(".XSHG", "")
        if ".XSHE" in symbol:
            return "sz" + symbol.replace(".XSHE", "")
        # 纯代码添加前缀
        if symbol.startswith("6"):
            return "sh" + symbol.zfill(6)
        if symbol.startswith("0") or symbol.startswith("3"):
            return "sz" + symbol.zfill(6)
        return symbol

    def _get_from_cache(
        self,
        domain: str,
        table: str,
        **conditions,
    ) -> Optional[pd.DataFrame]:
        """从缓存获取数据"""
        if not self._use_cache:
            return None
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
        cache = get_cache()
        cache.set(domain, table, df, **conditions)

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
        cache_key = {"symbol": symbol, "adjust": adjust}
        cached = self._get_from_cache("market", "stock_daily", **cache_key)
        if cached is not None and not cached.empty:
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
            raise DataSourceError(
                "离线模式下无缓存数据", source=self.name, symbol=symbol
            )

        # 从数据源获取
        self._load_market_data()

        if hasattr(self, "_get_stock_daily"):
            try:
                df = self._get_stock_daily(
                    symbol=symbol,
                    start=start,
                    end=end,
                    adjust=adjust,
                    force_update=kwargs.get("force_update", False),
                    offline_mode=self._offline_mode,
                )
                if not df.empty:
                    self._set_to_cache("market", "stock_daily", df, **cache_key)
                return df
            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=symbol)

        # 直接使用 akshare
        if self._akshare_available:
            try:
                import time

                # 转换代码格式
                ak_symbol = symbol.replace("sh", "").replace("sz", "")

                for attempt in range(self._max_retries):
                    try:
                        raw_df = self._akshare.stock_zh_a_hist(
                            symbol=ak_symbol,
                            period="daily",
                            start_date=start.replace("-", ""),
                            end_date=end.replace("-", ""),
                            adjust=adjust,
                        )
                        if raw_df is not None and not raw_df.empty:
                            break
                    except Exception as e:
                        if attempt < self._max_retries - 1:
                            time.sleep(self._retry_delay)
                        else:
                            raise DataSourceError(
                                f"下载失败: {e}", source=self.name, symbol=symbol
                            )

                # 标准化字段
                df = self._standardize_ohlcv(raw_df)
                self._set_to_cache("market", "stock_daily", df, **cache_key)
                return df

            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=symbol)

        raise DataSourceError("数据源不可用", source=self.name, symbol=symbol)

    def _standardize_ohlcv(self, df: pd.DataFrame) -> pd.DataFrame:
        """标准化 OHLCV 字段"""
        if df is None or df.empty:
            return pd.DataFrame()

        result = df.copy()
        columns_map = {
            "日期": "datetime",
            "开盘": "open",
            "最高": "high",
            "最低": "low",
            "收盘": "close",
            "成交量": "volume",
            "成交额": "amount",
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

        # 检查缓存
        cached = self._get_from_cache("meta", "index_components", index_code=index_code)
        if cached is not None and not cached.empty:
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
                index_num = index_code.split(".")[0] if "." in index_code else index_code
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
                index_num = index_code.split(".")[0] if "." in index_code else index_code
                index_num = index_num.replace("sh", "").replace("sz", "").zfill(6)

                # 尝试从中证指数获取
                try:
                    df = self._akshare.index_stock_cons_weight_csindex(symbol=index_num)
                    if df is not None and not df.empty:
                        # 标准化
                        result = pd.DataFrame()
                        jq_code = index_code if "." in index_code else self._to_jq_format(index_code)
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

                        return result
                except Exception:
                    pass

                # 备用: 使用无权重版本
                df = self._akshare.index_stock_cons(symbol=index_num)
                if df is not None and not df.empty:
                    result = pd.DataFrame()
                    jq_code = index_code if "." in index_code else self._to_jq_format(index_code)
                    result["index_code"] = [jq_code] * len(df)
                    result["code"] = df.get("成分股代码", df.get("品种代码")).apply(self._to_jq_format)
                    result["stock_name"] = df.get("成分股名称", df.get("品种名称", ""))
                    if include_weights:
                        result["weight"] = 100.0 / len(df)  # 等权重
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
            days = cached["date"].tolist() if "date" in cached.columns else cached.index.tolist()
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
                if security_type == "stock":
                    df = self._akshare.stock_info_a_code_name()
                elif security_type == "etf":
                    df = self._akshare.fund_etf_category_sina(symbol="ETF基金")
                elif security_type == "index":
                    df = self._akshare.index_stock_info()
                else:
                    raise DataSourceError(f"不支持类型: {security_type}", source=self.name)

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

        raise DataSourceError("数据源不可用", source=self.name)

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

        if hasattr(self, "_get_stock_minute"):
            try:
                symbol = self._normalize_symbol(symbol)
                start = self._normalize_date(start_date) if start_date else None
                end = self._normalize_date(end_date) if end_date else None

                df = self._get_stock_minute(symbol, freq=freq)
                return df
            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=symbol)

        if self._akshare_available:
            try:
                code = symbol.replace("sh", "").replace("sz", "").replace(".XSHG", "").replace(".XSHE", "")

                # akshare 分钟数据
                df = self._akshare.stock_zh_a_minute(
                    symbol=code,
                    period=freq.replace("min", ""),
                    adjust=kwargs.get("adjust", ""),
                )
                if df is not None and not df.empty:
                    return self._standardize_ohlcv(df)
            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=symbol)

        raise DataSourceError("数据源不可用", source=self.name, symbol=symbol)

    def get_money_flow(
        self,
        symbol: str,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取资金流向数据"""
        self._load_market_data()

        if hasattr(self, "_get_money_flow"):
            try:
                df = self._get_money_flow(symbol)
                return df
            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=symbol)

        if self._akshare_available:
            try:
                code = symbol.replace("sh", "").replace("sz", "").replace(".XSHG", "").replace(".XSHE", "")
                df = self._akshare.stock_individual_fund_flow(stock=code, market="sh" if code.startswith("6") else "sz")
                return df
            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=symbol)

        raise DataSourceError("数据源不可用", source=self.name, symbol=symbol)

    def get_north_money_flow(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取北向资金流向"""
        self._load_market_data()

        if hasattr(self, "_get_north_money_flow"):
            try:
                df = self._get_north_money_flow()
                return df
            except Exception as e:
                raise DataSourceError(str(e), source=self.name)

        if self._akshare_available:
            try:
                df = self._akshare.stock_hsgt_north_net_flow_in_em()
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
        self._load_market_data()

        if hasattr(self, "_get_industry_stocks_sw"):
            try:
                stocks = self._get_industry_stocks_sw(industry_code)
                return stocks
            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=industry_code)

        if self._akshare_available:
            try:
                code = industry_code.replace(".SI", "").zfill(6)
                df = self._akshare.index_component_sw(symbol=code)
                if df is not None and not df.empty:
                    stocks = []
                    for stock_code in df.get("证券代码", []):
                        code_str = str(stock_code).zfill(6)
                        if code_str.startswith("6"):
                            stocks.append(f"{code_str}.XSHG")
                        else:
                            stocks.append(f"{code_str}.XSHE")
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
        self._load_market_data()

        if hasattr(self, "_get_all_industry_mapping"):
            try:
                mapping = self._get_all_industry_mapping()
                jq_code = symbol if "." in symbol else self._to_jq_format(symbol)
                return mapping.get(jq_code, "")
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
        # 尝试从 finance_data 模块获取
        try:
            from finance_data.finance import get_finance_indicator
            return get_finance_indicator(symbol, fields, start_date, end_date)
        except ImportError:
            pass

        if self._akshare_available:
            try:
                code = symbol.replace("sh", "").replace("sz", "").replace(".XSHG", "").replace(".XSHE", "")
                df = self._akshare.stock_financial_analysis_indicator(symbol=code)
                return df
            except Exception as e:
                raise DataSourceError(str(e), source=self.name, symbol=symbol)

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
                raise DataSourceError(str(e), source=self.name, symbol=symbol)

        raise DataSourceError(f"{self.name} 不支持集合竞价数据", source=self.name, symbol=symbol)

    # ETF/指数日线复用 get_daily_data
    def get_etf_daily(
        self,
        symbol: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
        **kwargs,
    ) -> pd.DataFrame:
        """获取 ETF 日线数据"""
        self._load_market_data()

        if hasattr(self, "_get_etf_daily"):
            try:
                start = self._normalize_date(start_date)
                end = self._normalize_date(end_date)
                return self._get_etf_daily(symbol, start, end)
            except Exception as e:
                logger.warning(f"ETF 数据获取失败: {e}")

        return self.get_daily_data(symbol, start_date, end_date, adjust="none", **kwargs)

    def get_index_daily(
        self,
        symbol: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
        **kwargs,
    ) -> pd.DataFrame:
        """获取指数日线数据"""
        self._load_market_data()

        if hasattr(self, "_get_index_daily"):
            try:
                start = self._normalize_date(start_date)
                end = self._normalize_date(end_date)
                return self._get_index_daily(symbol, start, end)
            except Exception as e:
                logger.warning(f"指数数据获取失败: {e}")

        return self.get_daily_data(symbol, start_date, end_date, adjust="none", **kwargs)

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


__all__ = ["AkShareAdapter"]