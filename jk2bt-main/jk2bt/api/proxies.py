"""
api/proxies.py
聚宽 API 兼容代理类。

包含:
- SecurityInfo: 兼容聚宽 get_security_info 返回的对象风格访问
- _QueryBuilder: 聚宽 query builder
- _Expression: 表达式对象
- _FieldProxy: 聚宽 query filter 字段代理
- _TableProxy: 聚宽估值/财务表代理
- _FinanceModule: finance 模块模拟
- valuation, income, cash_flow, balance, indicator: 表代理对象
"""

import warnings
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date, time

from .securities_utils import (
    format_stock_symbol_for_akshare,
    jq_code_to_ak,
    ak_code_to_jq,
    _stock_code_to_jq,
    _find_date_column,
)


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


valuation = _TableProxy("valuation")
income = _TableProxy("income")
cash_flow = _TableProxy("cash_flow")
balance = _TableProxy("balance")
indicator = _TableProxy("indicator")


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
    STK_NAME_HISTORY = _FinanceTableProxy("STK_NAME_HISTORY")
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

    FUND_SHARE_DAILY = _FinanceTableProxy("FUND_SHARE_DAILY")
    FUND_INVEST_TARGET = _FinanceTableProxy("FUND_INVEST_TARGET")
    FUND_FIN_INDICATOR = _FinanceTableProxy("FUND_FIN_INDICATOR")
    FUND_MAIN_INFO = _FinanceTableProxy("FUND_MAIN_INFO")
    FUND_PORTFOLIO_BOND = _FinanceTableProxy("FUND_PORTFOLIO_BOND")
    FUND_DIVIDEND = _FinanceTableProxy("FUND_DIVIDEND")

    STK_PERFORMANCE_LETTERS = _FinanceTableProxy("STK_PERFORMANCE_LETTERS")
    STK_REPORT_DISCLOSURE = _FinanceTableProxy("STK_REPORT_DISCLOSURE")

    STK_EXCHANGE_TRADE_INFO = _FinanceTableProxy("STK_EXCHANGE_TRADE_INFO")
    STK_EXCHANGE_LINK_CALENDAR = _FinanceTableProxy("STK_EXCHANGE_LINK_CALENDAR")
    STK_EL_CONST_CHANGE = _FinanceTableProxy("STK_EL_CONST_CHANGE")
    STK_EL_TOP_ACTIVATE = _FinanceTableProxy("STK_EL_TOP_ACTIVATE")
    STK_EXCHANGE_LINK_RATE = _FinanceTableProxy("STK_EXCHANGE_LINK_RATE")

    STK_EMPLOYEE_INFO = _FinanceTableProxy("STK_EMPLOYEE_INFO")
    STK_MANAGEMENT_INFO = _FinanceTableProxy("STK_MANAGEMENT_INFO")

    STK_LIMITED_SHARES_LIST = _FinanceTableProxy("STK_LIMITED_SHARES_LIST")
    STK_LIMITED_SHARES_UNLIMIT = _FinanceTableProxy("STK_LIMITED_SHARES_UNLIMIT")

    FINANCE_INCOME_STATEMENT = _FinanceTableProxy("FINANCE_INCOME_STATEMENT")
    FINANCE_CASHFLOW_STATEMENT = _FinanceTableProxy("FINANCE_CASHFLOW_STATEMENT")
    FINANCE_BALANCE_SHEET_PARENT = _FinanceTableProxy("FINANCE_BALANCE_SHEET_PARENT")

    FUT_MARGIN = _FinanceTableProxy("FUT_MARGIN")
    FUT_CHARGE = _FinanceTableProxy("FUT_CHARGE")
    FUT_WAREHOUSE_RECEIPT = _FinanceTableProxy("FUT_WAREHOUSE_RECEIPT")
    FUT_MEMBER_POSITION_RANK = _FinanceTableProxy("FUT_MEMBER_POSITION_RANK")

    # 新增表
    STK_AUDIT_OPINION = _FinanceTableProxy("STK_AUDIT_OPINION")
    STK_SHAREHOLDERS_SHARE_CHANGE = _FinanceTableProxy("STK_SHAREHOLDERS_SHARE_CHANGE")
    FUND_MF_DAILY_PROFIT = _FinanceTableProxy("FUND_MF_DAILY_PROFIT")
    FINANCE_INCOME_STATEMENT_PARENT = _FinanceTableProxy(
        "FINANCE_INCOME_STATEMENT_PARENT"
    )
    FINANCE_CASHFLOW_STATEMENT_PARENT = _FinanceTableProxy(
        "FINANCE_CASHFLOW_STATEMENT_PARENT"
    )
    FINANCE_BALANCE_SHEET = _FinanceTableProxy("FINANCE_BALANCE_SHEET")
    OPT_DAILY_PREOPEN = _FinanceTableProxy("OPT_DAILY_PREOPEN")

    OPT_RISK_INDICATOR = _FinanceTableProxy("OPT_RISK_INDICATOR")

    # JQData兼容别名
    STK_SHAREHOLDER_FLOATING_TOP10 = _FinanceTableProxy("STK_SHAREHOLDER_FLOAT_TOP10")
    STK_HOLDER_NUM = _FinanceTableProxy("STK_SHAREHOLDER_NUM")
    STK_SHARES_PLEDGE = _FinanceTableProxy("STK_SHARE_PLEDGE")
    STK_SHARES_FROZEN = _FinanceTableProxy("STK_SHARE_FREEZE")


finance = _FinanceModule()


__all__ = [
    "SecurityInfo",
    "_QueryBuilder",
    "_Expression",
    "_FieldProxy",
    "_TableProxy",
    "_FinanceTableProxy",
    "_FinanceFieldProxy",
    "_FinanceModule",
    "finance",
    "valuation",
    "income",
    "cash_flow",
    "balance",
    "indicator",
]
