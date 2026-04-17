"""
engine/data_proxies.py
引擎层数据代理类 - 策略运行时使用的代理对象。

包含:
- PositionProxy: 聚宽 position 对象模拟
- PortfolioProxy: 聚宽 portfolio 对象模拟
- _CurrentDataEntry: 聚宽 get_current_data()[code] 返回的对象
- _CurrentDataProxy: 模拟聚宽 get_current_data() 返回的对象
- _TickDataProxy: 模拟聚宽 get_current_tick() 返回的对象

注意: API 兼容类（SecurityInfo, QueryBuilder, TableProxy 等）已移动到 api/proxies.py
"""

import warnings
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date, time

from jk2bt.api.securities_utils import (
    format_stock_symbol_for_akshare,
    jq_code_to_ak,
    ak_code_to_jq,
)
from jk2bt.api.proxies import (
    SecurityInfo,
    _QueryBuilder,
    _TableProxy,
)


class PositionProxy:
    """聚宽 position 对象模拟"""

    def __init__(self, bt_position, data):
        self._pos = bt_position
        self._data = data

    @property
    def total_amount(self):
        """持股数量"""
        return int(self._pos.size)

    @property
    def value(self):
        """持仓市值"""
        return self._pos.size * self._data.close[0]

    @property
    def price(self):
        """成本价"""
        return self._pos.price

    @property
    def closeable_amount(self):
        """可卖数量（与total_amount相同）"""
        return self.total_amount


class PortfolioProxy:
    """聚宽 portfolio 对象模拟"""

    def __init__(self, strategy):
        self._strategy = strategy

    @property
    def positions(self):
        """返回持仓字典 {stock_code: PositionProxy}"""
        positions = {}
        for data in self._strategy.datas:
            pos = self._strategy.getposition(data)
            if pos.size > 0:
                positions[data._name] = PositionProxy(pos, data)
        return positions

    @property
    def total_value(self):
        """总资产"""
        return self._strategy.broker.getvalue()

    @property
    def available_cash(self):
        """可用现金"""
        return self._strategy.broker.getcash()

    @property
    def returns(self):
        """收益率"""
        if (
            hasattr(self._strategy, "_initial_capital")
            and self._strategy._initial_capital > 0
        ):
            return self.total_value / self._strategy._initial_capital - 1
        return 0.0

    @property
    def market_value(self):
        """持仓市值"""
        return self.total_value - self.available_cash

    @property
    def cash(self):
        """现金（兼容别名）"""
        return self.available_cash

    @property
    def positions_value(self):
        """持仓总市值"""
        return self.market_value

    @property
    def starting_cash(self):
        """初始资金"""
        if (
            hasattr(self._strategy, "_initial_capital")
            and self._strategy._initial_capital is not None
        ):
            return self._strategy._initial_capital
        if hasattr(self._strategy.broker, "_initial_cash"):
            return self._strategy.broker._initial_cash
        return self._strategy.broker.getvalue()


class _CurrentDataEntry:
    """
    聚宽get_current_data()[code]返回的对象

    支持属性:
        last_price: 最新价
        day_open: 开盘价
        high: 最高价
        low: 最低价
        volume: 成交量
        high_limit: 涨停价
        low_limit: 跌停价
        paused: 是否停牌
        is_st: 是否ST
        name: 股票名称
    """

    def __init__(self, codes, bt_strategy=None):
        if isinstance(codes, str):
            self.codes = [codes]
            self._single = True
        else:
            self.codes = list(codes)
            self._single = False
        self._bt = bt_strategy
        self._cache = {}
        self._is_st_cache = None
        self._paused_cache = None

    def _get_data_feed(self, code):
        """从Backtrader获取data feed"""
        if self._bt is None:
            return None

        formats = [code]
        if ".XSHG" in code or ".XSHE" in code:
            formats.append(jq_code_to_ak(code))
        if code.startswith("sh") or code.startswith("sz"):
            formats.append(code[2:])

        for data in self._bt.datas:
            if data._name in formats:
                return data
        return None

    def _fetch_from_data_source(self, field):
        """从数据源获取最新数据"""
        code = self.codes[0]
        ak_code = format_stock_symbol_for_akshare(code)

        try:
            from jk2bt.data.sources import get_adapter

            source = get_adapter()
            df = source.get_daily_data(
                symbol=ak_code,
                start_date=(datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                end_date=datetime.now().strftime("%Y-%m-%d"),
                adjust="qfq",
            )

            if df is not None and not df.empty:
                latest = df.iloc[-1]
                col_mapping = {
                    "open": "open",
                    "high": "high",
                    "low": "low",
                    "close": "close",
                    "volume": "volume",
                }

                if field in col_mapping and col_mapping[field] in latest:
                    return latest[col_mapping[field]]

        except Exception:
            pass

        return None

    @property
    def last_price(self):
        """最新价格"""
        if self._bt:
            data = self._get_data_feed(self.codes[0])
            if data:
                return data.close[0]
        return self._fetch_from_data_source("close")

    @property
    def day_open(self):
        """今日开盘价"""
        if self._bt:
            data = self._get_data_feed(self.codes[0])
            if data:
                return data.open[0]
        return self._fetch_from_data_source("open")

    @property
    def high(self):
        """今日最高价"""
        if self._bt:
            data = self._get_data_feed(self.codes[0])
            if data:
                return data.high[0]
        return self._fetch_from_data_source("high")

    @property
    def low(self):
        """今日最低价"""
        if self._bt:
            data = self._get_data_feed(self.codes[0])
            if data:
                return data.low[0]
        return self._fetch_from_data_source("low")

    @property
    def volume(self):
        """今日成交量"""
        if self._bt:
            data = self._get_data_feed(self.codes[0])
            if data:
                return data.volume[0]
        return self._fetch_from_data_source("volume")

    @property
    def high_limit(self):
        """涨停价"""
        code = self.codes[0]
        code_num = format_stock_symbol_for_akshare(code)

        prev_close = None
        if self._bt:
            data = self._get_data_feed(code)
            if data and len(data.close) > 1:
                prev_close = data.close[-1]

        if prev_close is None:
            try:
                from jk2bt.data.sources import get_adapter

                source = get_adapter()
                ak_code = format_stock_symbol_for_akshare(code)
                df = source.get_daily_data(
                    symbol=ak_code,
                    start_date=(datetime.now() - timedelta(days=5)).strftime(
                        "%Y-%m-%d"
                    ),
                    end_date=datetime.now().strftime("%Y-%m-%d"),
                    adjust="none",
                )
                if df is not None and len(df) >= 2:
                    prev_close = df.iloc[-2]["close"]
            except Exception:
                pass

        if prev_close is None:
            return None

        limit_ratio = 0.10
        if code_num.startswith("300") or code_num.startswith("688"):
            limit_ratio = 0.20
        elif self.is_st:
            limit_ratio = 0.05

        return round(prev_close * (1 + limit_ratio), 2)

    @property
    def low_limit(self):
        """跌停价"""
        code = self.codes[0]
        code_num = format_stock_symbol_for_akshare(code)

        prev_close = None
        if self._bt:
            data = self._get_data_feed(code)
            if data and len(data.close) > 1:
                prev_close = data.close[-1]

        if prev_close is None:
            try:
                from jk2bt.data.sources import get_adapter

                source = get_adapter()
                ak_code = format_stock_symbol_for_akshare(code)
                df = source.get_daily_data(
                    symbol=ak_code,
                    start_date=(datetime.now() - timedelta(days=5)).strftime(
                        "%Y-%m-%d"
                    ),
                    end_date=datetime.now().strftime("%Y-%m-%d"),
                    adjust="none",
                )
                if df is not None and len(df) >= 2:
                    prev_close = df.iloc[-2]["close"]
            except Exception:
                pass

        if prev_close is None:
            return None

        limit_ratio = 0.10
        if code_num.startswith("300") or code_num.startswith("688"):
            limit_ratio = 0.20
        elif self.is_st:
            limit_ratio = 0.05

        return round(prev_close * (1 - limit_ratio), 2)

    @property
    def paused(self):
        """是否停牌"""
        if self._paused_cache is not None:
            return self._paused_cache

        code = self.codes[0]
        ak_code = format_stock_symbol_for_akshare(code)

        try:
            from jk2bt.data.sources import get_adapter

            stop_df = get_adapter().get_suspended_stocks()
            if stop_df is not None and not stop_df.empty:
                self._paused_cache = ak_code in stop_df["代码"].values
                return self._paused_cache
        except Exception:
            pass

        if self._bt:
            data = self._get_data_feed(code)
            if data and data.volume[0] == 0:
                self._paused_cache = True
                return True

        self._paused_cache = False
        return False

    @property
    def is_st(self):
        """是否ST股票"""
        if self._is_st_cache is not None:
            return self._is_st_cache

        code = self.codes[0]
        ak_code = format_stock_symbol_for_akshare(code)

        try:
            from jk2bt.data.sources import get_adapter

            st_df = get_adapter().get_st_stocks()
            if st_df is not None and not st_df.empty:
                self._is_st_cache = ak_code in st_df["代码"].values
                return self._is_st_cache
        except Exception:
            pass

        self._is_st_cache = False
        return False

    @property
    def name(self):
        """股票名称"""
        code = self.codes[0]

        try:
            from jk2bt.api.jq_compat import get_security_info_jq

            info = get_security_info_jq(code)
            if info and "display_name" in info:
                return info["display_name"]
            elif info and "name" in info:
                return info["name"]
        except Exception:
            pass

        return None


class _CurrentDataProxy:
    """模拟聚宽 get_current_data() 返回的对象"""

    def __init__(self, bt_strategy=None):
        self._bt = bt_strategy
        self._store = {}

    def __getitem__(self, codes):
        key = tuple(codes) if isinstance(codes, (list, tuple)) else codes
        if key not in self._store:
            self._store[key] = _CurrentDataEntry(codes, self._bt)
        return self._store[key]


class _TickDataProxy:
    """模拟聚宽 get_current_tick() 返回的对象"""

    def __init__(self, code, bt_strategy=None):
        self._code = code
        self._bt = bt_strategy
        self._data_entry = None
        self._cached_price = None

    def _get_data(self):
        """获取数据条目"""
        if self._data_entry is None:
            proxy = _CurrentDataProxy(self._bt)
            self._data_entry = proxy[self._code]
        return self._data_entry

    def _fetch_price_from_db(self):
        """从数据库获取当前价格"""
        if self._cached_price is not None:
            return self._cached_price

        current_date = None
        if self._bt and hasattr(self._bt, "current_dt") and self._bt.current_dt:
            current_date = self._bt.current_dt.strftime("%Y-%m-%d")

        if current_date is None:
            return None

        try:
            from jk2bt.api.market import get_price

            df = get_price(
                security=self._code,
                end_date=current_date,
                count=1,
                frequency="daily",
                fields=["close"],
            )
            if df is not None and not df.empty:
                if isinstance(df, pd.DataFrame):
                    if "close" in df.columns and len(df) > 0:
                        self._cached_price = df["close"].iloc[-1]
                    elif self._code in df.columns and len(df) > 0:
                        self._cached_price = df[self._code].iloc[-1]
                return self._cached_price
        except Exception:
            pass

        return None

    @property
    def current(self):
        """当前价格"""
        data = self._get_data()
        if self._bt:
            feed_data = data._get_data_feed(self._code)
            if feed_data:
                return feed_data.close[0]
        return self._fetch_price_from_db()

    @property
    def last_price(self):
        """最新价格"""
        return self.current

    @property
    def day_open(self):
        """今日开盘价"""
        return self._get_data().day_open

    @property
    def high(self):
        """今日最高价"""
        return self._get_data().high

    @property
    def low(self):
        """今日最低价"""
        return self._get_data().low

    @property
    def volume(self):
        """今日成交量"""
        return self._get_data().volume


__all__ = [
    "PositionProxy",
    "PortfolioProxy",
    "_CurrentDataEntry",
    "_CurrentDataProxy",
    "_TickDataProxy",
    "SecurityInfo",
    "_QueryBuilder",
    "_TableProxy",
]
