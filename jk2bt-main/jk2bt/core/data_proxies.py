"""
data_proxies.py
数据代理类，用于模拟聚宽数据访问接口。

包含:
- RobustResult: 稳健结果封装类 (从 securities_utils 重新导出)
- _CurrentDataEntry: 聚宽 get_current_data()[code] 返回的对象
- _CurrentDataProxy: 模拟聚宽 get_current_data() 返回的对象
- _TickDataProxy: 模拟聚宽 get_current_tick() 返回的对象
- SecurityInfo: 兼容聚宽 get_security_info 返回的对象风格访问
- PositionProxy: 聚宽 position 对象模拟
- PortfolioProxy: 聚宽 portfolio 对象模拟
- _QueryBuilder: 聚宽 query builder
- _Expression: 表达式对象
- _FieldProxy: 聚宽 query filter 字段代理
- _TableProxy: 聚宽估值/财务表代理
- FinanceDBProxy: 聚宽 finance 数据库模拟
- _FinanceModule: finance 模块模拟
"""

import warnings
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date, time

# 从 securities_utils 导入工具函数
from .securities_utils import (
    format_stock_symbol_for_akshare,
    jq_code_to_ak,
    ak_code_to_jq,
    _stock_code_to_jq,
    _find_date_column,
    RobustResult,
)


# =====================================================================
# SecurityInfo - 兼容聚宽 get_security_info 返回的对象风格访问
# =====================================================================


class SecurityInfo:
    """兼容聚宽 get_security_info 返回的对象风格访问。

    聚宽平台返回的是一个对象，可以通过 .code, .display_name, .start_date 等属性访问。
    这个类将字典转换为对象风格访问。
    """

    def __init__(self, info_dict):
        self._dict = info_dict
        self.code = info_dict.get("code", "")
        self.display_name = info_dict.get("display_name", info_dict.get("name", ""))
        self.name = info_dict.get("name", "")
        self.start_date = info_dict.get("start_date")
        self.end_date = info_dict.get("end_date")
        self.type = info_dict.get("type", "stock")

    def __getitem__(self, key):
        return self._dict.get(key)

    def __repr__(self):
        return f"SecurityInfo(code={self.code}, display_name={self.display_name}, start_date={self.start_date})"


# =====================================================================
# Query Builder 相关类
# =====================================================================


class _QueryBuilder:
    """
    聚宽query builder，支持:
    query(valuation).filter(valuation.code.in_(stocks)).limit(n)
    query(valuation).filter(valuation.pb_ratio > 0, valuation.pe_ratio > 0)
    """

    def __init__(self, tables):
        if not isinstance(tables, (list, tuple)):
            tables = [tables]
        self._tables = tables
        self._filters = []
        self._limit_n = None
        self._symbols = None
        self._filter_expressions = []
        self._order_field = None
        self._order_ascending = True

    def filter(self, *args):
        """添加过滤条件"""
        for arg in args:
            if hasattr(arg, "_symbols") and arg._symbols is not None:
                self._symbols = arg._symbols
            elif hasattr(arg, "_field"):
                self._filter_expressions.append(arg)
        return self

    def order_by(self, field, ascending=True):
        """排序"""
        self._order_field = field
        self._order_ascending = ascending
        return self

    def limit(self, n):
        """限制返回数量"""
        self._limit_n = n
        return self

    def __repr__(self):
        return f"<QueryBuilder tables={self._tables} symbols={self._symbols}>"


class _Expression:
    """表达式对象，支持 valuation.pb_ratio > 0.15 * valuation.pe_ratio"""

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class _FieldProxy:
    """
    聚宽query filter字段代理
    支持:
        valuation.code.in_(stocks)
        valuation.pb_ratio > 0
        valuation.pe_ratio > 0
    """

    def __init__(self, table, field):
        self._table = table
        self._field = field
        self._symbols = None
        self._operator = None
        self._value = None

    def in_(self, lst):
        """in操作"""
        self._symbols = list(lst)
        return self

    def __eq__(self, other):
        self._operator = "=="
        self._value = other
        return self

    def __lt__(self, other):
        self._operator = "<"
        self._value = other
        return self

    def __le__(self, other):
        self._operator = "<="
        self._value = other
        return self

    def __gt__(self, other):
        self._operator = ">"
        self._value = other
        return self

    def __ge__(self, other):
        self._operator = ">="
        self._value = other
        return self

    def __mul__(self, other):
        """支持 valuation.pb_ratio > 0.15 * valuation.pe_ratio"""
        return _Expression(self, "*", other)

    def __rmul__(self, other):
        return _Expression(other, "*", self)

    def __truediv__(self, other):
        return _Expression(self, "/", other)

    def __add__(self, other):
        return _Expression(self, "+", other)

    def __sub__(self, other):
        return _Expression(self, "-", other)

    def asc(self):
        return self

    def desc(self):
        return self


class _TableProxy:
    """聚宽估值/财务表代理，支持 valuation.code / valuation.pe_ratio 等写法。"""

    def __init__(self, name):
        self._name = name

    def __getattr__(self, field):
        return _FieldProxy(self._name, field)


# 暴露聚宽风格的表名对象，供策略代码直接使用
valuation = _TableProxy("valuation")
income = _TableProxy("income")
cash_flow = _TableProxy("cash_flow")
balance = _TableProxy("balance")
indicator = _TableProxy("indicator")


# =====================================================================
# Finance Module 相关类
# =====================================================================


class _FinanceTableProxy:
    """聚宽finance表代理"""

    def __init__(self, name):
        self._name = name

    def __getattr__(self, field):
        if field.startswith("_"):
            raise AttributeError(field)
        return _FinanceFieldProxy(self._name, field)


class _FinanceFieldProxy:
    """finance字段代理，支持比较操作"""

    def __init__(self, table, field):
        self._table = table
        self._field = field
        self._symbols = None
        self._value = None
        self._gt = False
        self._ge = False
        self._lt = False
        self._le = False

    def in_(self, lst):
        self._symbols = list(lst)
        return self

    def __gt__(self, other):
        self._value = other
        self._gt = True
        return self

    def __ge__(self, other):
        self._value = other
        self._ge = True
        return self

    def __lt__(self, other):
        self._value = other
        self._lt = True
        return self

    def __le__(self, other):
        self._value = other
        self._le = True
        return self

    def __eq__(self, other):
        self._value = other
        return self


class _FinanceModule:
    """finance模块模拟"""

    STK_XR_XD = _FinanceTableProxy("STK_XR_XD")
    STK_MX_RZ_RQ = _FinanceTableProxy("STK_MX_RZ_RQ")
    STK_FIN_FORCAST = _FinanceTableProxy("STK_FIN_FORCAST")
    STK_COMPANY_BASIC_INFO = _FinanceTableProxy("STK_COMPANY_BASIC_INFO")
    STK_STATUS_CHANGE = _FinanceTableProxy("STK_STATUS_CHANGE")
    STK_LISTING_INFO = _FinanceTableProxy("STK_LISTING_INFO")
    STK_SHAREHOLDER_TOP10 = _FinanceTableProxy("STK_SHAREHOLDER_TOP10")
    STK_SHAREHOLDER_FLOAT_TOP10 = _FinanceTableProxy("STK_SHAREHOLDER_FLOAT_TOP10")
    STK_SHAREHOLDER_NUM = _FinanceTableProxy("STK_SHAREHOLDER_NUM")
    STK_DIVIDEND = _FinanceTableProxy("STK_DIVIDEND")
    STK_DIVIDEND_RIGHT = _FinanceTableProxy("STK_DIVIDEND_RIGHT")
    STK_UNLOCK = _FinanceTableProxy("STK_UNLOCK")
    STK_LOCK_UNLOCK = _FinanceTableProxy("STK_LOCK_UNLOCK")
    STK_LOCK_SHARE = _FinanceTableProxy("STK_LOCK_SHARE")
    STK_UNLOCK_DATE = _FinanceTableProxy("STK_UNLOCK_DATE")
    STK_SHARE_CHANGE = _FinanceTableProxy("STK_SHARE_CHANGE")
    STK_SHARE_PLEDGE = _FinanceTableProxy("STK_SHARE_PLEDGE")
    STK_SHARE_FREEZE = _FinanceTableProxy("STK_SHARE_FREEZE")
    STK_TOPHOLDER_CHANGE = _FinanceTableProxy("STK_TOPHOLDER_CHANGE")
    STK_CAPITAL_CHANGE = _FinanceTableProxy("STK_CAPITAL_CHANGE")
    STK_OPTION_DAILY = _FinanceTableProxy("STK_OPTION_DAILY")
    STK_OPTION_BASIC = _FinanceTableProxy("STK_OPTION_BASIC")
    STK_INDEX_WEIGHTS = _FinanceTableProxy("STK_INDEX_WEIGHTS")
    STK_INDEX_COMPONENTS = _FinanceTableProxy("STK_INDEX_COMPONENTS")
    STK_INDUSTRY_SW = _FinanceTableProxy("STK_INDUSTRY_SW")
    STK_SW_INDUSTRY = _FinanceTableProxy("STK_SW_INDUSTRY")
    STK_SW_INDUSTRY_STOCK = _FinanceTableProxy("STK_SW_INDUSTRY_STOCK")
    STK_CONVERSION_BOND_BASIC = _FinanceTableProxy("STK_CONVERSION_BOND_BASIC")
    STK_CONVERSION_BOND_PRICE = _FinanceTableProxy("STK_CONVERSION_BOND_PRICE")
    STK_CB_DAILY = _FinanceTableProxy("STK_CB_DAILY")
    CONVERSION_BOND = _FinanceTableProxy("CONVERSION_BOND")
    MACRO_ECONOMIC_DATA = _FinanceTableProxy("MACRO_ECONOMIC_DATA")
    MAC_ECONOMIC_DATA = _FinanceTableProxy("MAC_ECONOMIC_DATA")
    STK_ML_QUOTA = _FinanceTableProxy("STK_ML_QUOTA")
    STK_HK_HOLD_INFO = _FinanceTableProxy("STK_HK_HOLD_INFO")

    def run_query(self, query_obj, finance_db=None):
        """执行finance查询 - 聚宽风格 API

        JoinQuant用法: finance.run_query(query_obj)
        无需传入finance_db参数，自动获取全局实例
        """
        if finance_db is None:
            # 尝试多种方式获取finance_db实例
            import sys
            # 1. 从当前模块获取
            this_module = sys.modules.get(__name__)
            if hasattr(this_module, 'finance_db'):
                finance_db = this_module.finance_db
            # 2. 从strategy_base模块获取
            elif 'jk2bt.core.strategy_base' in sys.modules:
                sb_module = sys.modules['jk2bt.core.strategy_base']
                if hasattr(sb_module, 'finance_db'):
                    finance_db = sb_module.finance_db
            # 3. 动态导入
            else:
                try:
                    from .strategy_base import finance_db
                except ImportError:
                    from jk2bt.core.strategy_base import finance_db

        if finance_db is None:
            # 最后的fallback: 创建一个临时的finance_db实例
            finance_db = FinanceDBProxy()

        return finance_db.run_query(query_obj)


# =====================================================================
# Position 和 Portfolio 代理类
# =====================================================================


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
        # 尝试从多种来源获取初始资金
        if hasattr(self._strategy, "_initial_capital") and self._strategy._initial_capital is not None:
            return self._strategy._initial_capital
        # 尝试从 broker 的初始资金获取
        if hasattr(self._strategy.broker, "_initial_cash"):
            return self._strategy.broker._initial_cash
        # 默认返回当前总资产
        return self._strategy.broker.getvalue()


# =====================================================================
# Current Data 相关代理类
# =====================================================================


class _CurrentDataEntry:
    """
    聚宽get_current_data()[code]返回的对象

    支持属性:
        last_price: 最新价，从 data.close[0] 获取
        day_open: 开盘价，从 data.open[0] 获取
        high: 最高价
        low: 最低价
        volume: 成交量
        high_limit: 涨停价（主板10%，创业板/科创板20%，ST股5%）
        low_limit: 跌停价（主板10%，创业板/科创板20%，ST股5%）
        paused: 是否停牌，使用 ak.stock_zh_a_stop_em() 查询
        is_st: 是否ST，使用 ak.stock_zh_a_st_em() 查询
        name: 股票名称，使用 get_security_info_jq 获取
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
            from jk2bt.data_access import get_data_source
            source = get_data_source()
            df = source.get_daily_data(
                symbol=ak_code,
                start_date=(datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                end_date=datetime.now().strftime("%Y-%m-%d"),
                adjust="qfq",
            )

            if df is not None and not df.empty:
                latest = df.iloc[-1]
                # data_access 返回标准化字段名
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
        """
        涨停价
        计算方式: 前收盘价 * (1 + 涨幅)
        - 主板10%
        - 创业板/科创板20%
        - ST股5%
        """
        code = self.codes[0]
        code_num = format_stock_symbol_for_akshare(code)

        prev_close = None
        if self._bt:
            data = self._get_data_feed(code)
            if data and len(data.close) > 1:
                prev_close = data.close[-1]

        if prev_close is None:
            try:
                from jk2bt.data_access import get_data_source
                source = get_data_source()
                ak_code = format_stock_symbol_for_akshare(code)
                df = source.get_daily_data(
                    symbol=ak_code,
                    start_date=(datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
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
        """
        跌停价
        计算方式: 前收盘价 * (1 - 跌幅)
        - 主板10%
        - 创业板/科创板20%
        - ST股5%
        """
        code = self.codes[0]
        code_num = format_stock_symbol_for_akshare(code)

        prev_close = None
        if self._bt:
            data = self._get_data_feed(code)
            if data and len(data.close) > 1:
                prev_close = data.close[-1]

        if prev_close is None:
            try:
                from jk2bt.data_access import get_data_source
                source = get_data_source()
                ak_code = format_stock_symbol_for_akshare(code)
                df = source.get_daily_data(
                    symbol=ak_code,
                    start_date=(datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
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
        """
        是否停牌
        从AkShare停牌列表查询: ak.stock_zh_a_stop_em()
        """
        if self._paused_cache is not None:
            return self._paused_cache

        code = self.codes[0]
        ak_code = format_stock_symbol_for_akshare(code)

        try:
            # 延迟导入 akshare（data_access 暂未提供停牌查询方法）
            import akshare as ak
            stop_df = ak.stock_zh_a_stop_em()
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
        """
        是否ST股票
        从AkShare ST列表查询: ak.stock_zh_a_st_em()
        """
        if self._is_st_cache is not None:
            return self._is_st_cache

        code = self.codes[0]
        ak_code = format_stock_symbol_for_akshare(code)

        try:
            # 延迟导入 akshare（data_access 暂未提供 ST 查询方法）
            import akshare as ak
            st_df = ak.stock_zh_a_st_em()
            if st_df is not None and not st_df.empty:
                self._is_st_cache = ak_code in st_df["代码"].values
                return self._is_st_cache
        except Exception:
            pass

        self._is_st_cache = False
        return False

    @property
    def name(self):
        """股票名称，使用 get_security_info_jq 获取"""
        code = self.codes[0]

        try:
            # 延迟导入避免循环依赖
            from .api_wrappers import get_security_info_jq
            info = get_security_info_jq(code)
            if info and "display_name" in info:
                return info["display_name"]
            elif info and "name" in info:
                return info["name"]
        except Exception:
            pass

        return None


class _CurrentDataProxy:
    """
    模拟聚宽 get_current_data() 返回的对象，支持 [code] 和 [[code1, code2]] 两种访问方式。
    """

    def __init__(self, bt_strategy=None):
        self._bt = bt_strategy
        self._store = {}

    def __getitem__(self, codes):
        key = tuple(codes) if isinstance(codes, (list, tuple)) else codes
        if key not in self._store:
            self._store[key] = _CurrentDataEntry(codes, self._bt)
        return self._store[key]


class _TickDataProxy:
    """
    模拟聚宽 get_current_tick() 返回的对象。
    get_current_tick 返回的对象有 .current 属性表示当前价格。
    """

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
        """
        当股票不在策略数据源中时，从数据库获取当前价格
        使用 backtest 的当前日期
        """
        if self._cached_price is not None:
            return self._cached_price

        # 尝试从策略获取当前日期
        current_date = None
        if self._bt and hasattr(self._bt, 'current_dt') and self._bt.current_dt:
            current_date = self._bt.current_dt.strftime('%Y-%m-%d')

        if current_date is None:
            return None

        # 使用 get_price 获取数据
        try:
            from jk2bt.api.market import get_price
            df = get_price(
                security=self._code,
                end_date=current_date,
                count=1,
                frequency='daily',
                fields=['close']
            )
            if df is not None and not df.empty:
                # 根据返回格式获取价格
                if isinstance(df, pd.DataFrame):
                    if 'close' in df.columns and len(df) > 0:
                        self._cached_price = df['close'].iloc[-1]
                    elif self._code in df.columns and len(df) > 0:
                        self._cached_price = df[self._code].iloc[-1]
                return self._cached_price
        except Exception:
            pass

        return None

    @property
    def current(self):
        """当前价格 (兼容聚宽 get_current_tick().current)"""
        # 首先尝试从策略数据源获取
        data = self._get_data()
        if self._bt:
            feed_data = data._get_data_feed(self._code)
            if feed_data:
                return feed_data.close[0]

        # 如果不在数据源中，从数据库获取
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


# 导出的表对象
__all__ = [
    'RobustResult',
    'SecurityInfo',
    '_QueryBuilder',
    '_Expression',
    '_FieldProxy',
    '_TableProxy',
    '_FinanceTableProxy',
    '_FinanceFieldProxy',
    '_FinanceModule',
    'valuation',
    'income',
    'cash_flow',
    'balance',
    'indicator',
    'PositionProxy',
    'PortfolioProxy',
    '_CurrentDataEntry',
    '_CurrentDataProxy',
    '_TickDataProxy',
]