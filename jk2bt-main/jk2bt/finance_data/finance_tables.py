"""
finance_tables.py
聚宽 finance 模块的财务表定义

实现:
- STK_BALANCE_SHEET: 资产负债表
- STK_INCOME_STATEMENT: 利润表
- STK_CASHFLOW_STATEMENT: 现金流量表
- FUND_NET_VALUE: 基金净值
- FUND_PORTFOLIO: 基金持仓
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Union, Dict
import warnings
from datetime import datetime


# =====================================================================
# 资产负债表
# =====================================================================

STK_BALANCE_SHEET_SCHEMA = [
    "code",           # 股票代码
    "pub_date",       # 公告日期
    "stat_date",      # 统计日期
    "total_assets",   # 资产总计
    "total_liability", # 负债合计
    "total_equity",   # 所有者权益合计
    "total_current_assets",  # 流动资产合计
    "total_current_liability", # 流动负债合计
    "total_non_current_assets", # 非流动资产合计
    "total_non_current_liability", # 非流动负债合计
    "capital_reserve", # 资本公积
    "surplus_reserve", # 盈余公积
    "retained_earnings", # 未分配利润
    "paid_in_capital", # 实收资本
    "inventory",      # 存货
    "account_receivable", # 应收账款
    "cash_and_equivalents", # 货币资金
]


def get_balance_sheet(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    report_type: str = "合并报表",
) -> pd.DataFrame:
    """
    获取资产负债表数据

    参数:
        symbol: 股票代码（支持聚宽格式如 '600519.XSHG' 或普通格式 '600519'）
        start_date: 开始日期
        end_date: 结束日期
        report_type: 报表类型

    返回:
        DataFrame，包含资产负债表数据
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    # 标准化代码格式
    code = symbol.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

    try:
        # 尝试获取资产负债表数据
        df = ak.stock_financial_report_sina(stock=code, symbol="资产负债表")

        if df is None or df.empty:
            return pd.DataFrame(columns=STK_BALANCE_SHEET_SCHEMA)

        # 标准化字段名
        column_mapping = {
            "报告日": "stat_date",
            "资产总计": "total_assets",
            "负债合计": "total_liability",
            "所有者权益(或股东权益)合计": "total_equity",
            "流动资产合计": "total_current_assets",
            "流动负债合计": "total_current_liability",
            "非流动资产合计": "total_non_current_assets",
            "非流动负债合计": "total_non_current_liability",
            "资本公积": "capital_reserve",
            "盈余公积": "surplus_reserve",
            "未分配利润": "retained_earnings",
            "实收资本(或股本)": "paid_in_capital",
            "存货": "inventory",
            "应收账款": "account_receivable",
            "货币资金": "cash_and_equivalents",
        }

        df = df.rename(columns=column_mapping)
        df["code"] = code

        # 日期过滤
        if "stat_date" in df.columns:
            df["stat_date"] = pd.to_datetime(df["stat_date"], errors="coerce")
            if start_date:
                df = df[df["stat_date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["stat_date"] <= pd.to_datetime(end_date)]

        # 选择需要的列
        available_cols = [c for c in STK_BALANCE_SHEET_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取资产负债表失败 {symbol}: {e}")
        return pd.DataFrame(columns=STK_BALANCE_SHEET_SCHEMA)


# =====================================================================
# 利润表
# =====================================================================

STK_INCOME_STATEMENT_SCHEMA = [
    "code",
    "pub_date",
    "stat_date",
    "total_operating_revenue",  # 营业总收入
    "operating_revenue",        # 营业收入
    "total_operating_cost",     # 营业总成本
    "operating_cost",           # 营业成本
    "operating_profit",         # 营业利润
    "total_profit",             # 利润总额
    "net_profit",               # 净利润
    "net_profit_to_shareholders", # 归属于母公司股东的净利润
    "basic_eps",                # 基本每股收益
    "diluted_eps",              # 稀释每股收益
    "gross_profit",             # 毛利
]


def get_income_statement(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取利润表数据
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    code = symbol.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

    try:
        df = ak.stock_financial_report_sina(stock=code, symbol="利润表")

        if df is None or df.empty:
            return pd.DataFrame(columns=STK_INCOME_STATEMENT_SCHEMA)

        column_mapping = {
            "报告日": "stat_date",
            "营业总收入": "total_operating_revenue",
            "营业收入": "operating_revenue",
            "营业总成本": "total_operating_cost",
            "营业成本": "operating_cost",
            "营业利润": "operating_profit",
            "利润总额": "total_profit",
            "净利润": "net_profit",
            "归属于母公司所有者的净利润": "net_profit_to_shareholders",
            "基本每股收益": "basic_eps",
            "稀释每股收益": "diluted_eps",
        }

        df = df.rename(columns=column_mapping)
        df["code"] = code

        if "stat_date" in df.columns:
            df["stat_date"] = pd.to_datetime(df["stat_date"], errors="coerce")
            if start_date:
                df = df[df["stat_date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["stat_date"] <= pd.to_datetime(end_date)]

        available_cols = [c for c in STK_INCOME_STATEMENT_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取利润表失败 {symbol}: {e}")
        return pd.DataFrame(columns=STK_INCOME_STATEMENT_SCHEMA)


# =====================================================================
# 现金流量表
# =====================================================================

STK_CASHFLOW_STATEMENT_SCHEMA = [
    "code",
    "pub_date",
    "stat_date",
    "net_cashflow_operating",   # 经营活动产生的现金流量净额
    "net_cashflow_investing",   # 投资活动产生的现金流量净额
    "net_cashflow_financing",   # 筹资活动产生的现金流量净额
    "net_increase_cash",        # 现金及现金等价物净增加额
    "cash_equivalent_begin",    # 期初现金及现金等价物余额
    "cash_equivalent_end",      # 期末现金及现金等价物余额
]


def get_cashflow_statement(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取现金流量表数据
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    code = symbol.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

    try:
        df = ak.stock_financial_report_sina(stock=code, symbol="现金流量表")

        if df is None or df.empty:
            return pd.DataFrame(columns=STK_CASHFLOW_STATEMENT_SCHEMA)

        column_mapping = {
            "报告日": "stat_date",
            "经营活动产生的现金流量净额": "net_cashflow_operating",
            "投资活动产生的现金流量净额": "net_cashflow_investing",
            "筹资活动产生的现金流量净额": "net_cashflow_financing",
            "现金及现金等价物净增加额": "net_increase_cash",
            "期初现金及现金等价物余额": "cash_equivalent_begin",
            "期末现金及现金等价物余额": "cash_equivalent_end",
        }

        df = df.rename(columns=column_mapping)
        df["code"] = code

        if "stat_date" in df.columns:
            df["stat_date"] = pd.to_datetime(df["stat_date"], errors="coerce")
            if start_date:
                df = df[df["stat_date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["stat_date"] <= pd.to_datetime(end_date)]

        available_cols = [c for c in STK_CASHFLOW_STATEMENT_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取现金流量表失败 {symbol}: {e}")
        return pd.DataFrame(columns=STK_CASHFLOW_STATEMENT_SCHEMA)


# =====================================================================
# 基金净值
# =====================================================================

FUND_NET_VALUE_SCHEMA = [
    "code",           # 基金代码
    "date",           # 日期
    "net_value",      # 单位净值
    "accumulated_value", # 累计净值
    "daily_growth",   # 日增长率
]


def get_fund_net_value(
    fund_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取基金净值数据

    参数:
        fund_code: 基金代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含基金净值数据
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    try:
        # 获取基金历史净值
        df = ak.fund_open_fund_info_em(fund=fund_code, indicator="单位净值走势")

        if df is None or df.empty:
            return pd.DataFrame(columns=FUND_NET_VALUE_SCHEMA)

        # 标准化字段
        column_mapping = {
            "净值日期": "date",
            "单位净值": "net_value",
            "累计净值": "accumulated_value",
            "日增长率": "daily_growth",
        }

        df = df.rename(columns=column_mapping)
        df["code"] = fund_code

        # 日期过滤
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            if start_date:
                df = df[df["date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["date"] <= pd.to_datetime(end_date)]

        available_cols = [c for c in FUND_NET_VALUE_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取基金净值失败 {fund_code}: {e}")
        return pd.DataFrame(columns=FUND_NET_VALUE_SCHEMA)


# =====================================================================
# 基金持仓
# =====================================================================

FUND_PORTFOLIO_SCHEMA = [
    "fund_code",      # 基金代码
    "stock_code",     # 股票代码
    "stock_name",     # 股票名称
    "shares",         # 持股数量
    "market_value",   # 市值
    "weight",         # 占净值比例
    "report_date",    # 报告日期
]


def get_fund_portfolio(
    fund_code: str,
    report_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取基金持仓数据

    参数:
        fund_code: 基金代码
        report_date: 报告日期

    返回:
        DataFrame，包含基金持仓数据
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    try:
        # 获取基金股票持仓
        df = ak.fund_portfolio_em(fund=fund_code)

        if df is None or df.empty:
            return pd.DataFrame(columns=FUND_PORTFOLIO_SCHEMA)

        # 标准化字段
        column_mapping = {
            "序号": "seq",
            "股票代码": "stock_code",
            "股票名称": "stock_name",
            "占净值比例": "weight",
            "持股数": "shares",
            "持仓市值": "market_value",
            "季度": "report_date",
        }

        df = df.rename(columns=column_mapping)
        df["fund_code"] = fund_code

        available_cols = [c for c in FUND_PORTFOLIO_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取基金持仓失败 {fund_code}: {e}")
        return pd.DataFrame(columns=FUND_PORTFOLIO_SCHEMA)


# =====================================================================
# 统一的 FinanceQuery 类
# =====================================================================

class FinanceTables:
    """
    聚宽 finance 模块的财务表定义
    提供类似 ORM 的表对象
    """

    # 资产负债表
    class STK_BALANCE_SHEET:
        code = None
        pub_date = None
        stat_date = None
        total_assets = None
        total_liability = None
        total_equity = None
        total_current_assets = None
        total_current_liability = None
        total_non_current_assets = None
        total_non_current_liability = None
        capital_reserve = None
        surplus_reserve = None
        retained_earnings = None
        paid_in_capital = None
        inventory = None
        account_receivable = None
        cash_and_equivalents = None

    # 利润表
    class STK_INCOME_STATEMENT:
        code = None
        pub_date = None
        stat_date = None
        total_operating_revenue = None
        operating_revenue = None
        total_operating_cost = None
        operating_cost = None
        operating_profit = None
        total_profit = None
        net_profit = None
        net_profit_to_shareholders = None
        basic_eps = None
        diluted_eps = None
        gross_profit = None

    # 现金流量表
    class STK_CASHFLOW_STATEMENT:
        code = None
        pub_date = None
        stat_date = None
        net_cashflow_operating = None
        net_cashflow_investing = None
        net_cashflow_financing = None
        net_increase_cash = None
        cash_equivalent_begin = None
        cash_equivalent_end = None

    # 基金净值
    class FUND_NET_VALUE:
        code = None
        date = None
        net_value = None
        accumulated_value = None
        daily_growth = None

    # 基金持仓
    class FUND_PORTFOLIO:
        fund_code = None
        stock_code = None
        stock_name = None
        shares = None
        market_value = None
        weight = None
        report_date = None

    def run_query(self, query_obj, **kwargs) -> pd.DataFrame:
        """
        执行查询

        参数:
            query_obj: 查询对象（通常是表的实例或过滤条件）

        返回:
            DataFrame
        """
        table_name = None
        code = None

        # 解析查询对象
        if hasattr(query_obj, "__class__"):
            table_name = query_obj.__class__.__name__

        # 如果是过滤条件对象
        if hasattr(query_obj, "left"):
            if hasattr(query_obj.left, "__class__"):
                table_name = query_obj.left.__class__.__name__
            if hasattr(query_obj, "right"):
                code = str(query_obj.right)

        # 根据表名返回数据
        if table_name == "STK_BALANCE_SHEET":
            if code:
                return get_balance_sheet(code, **kwargs)
            return pd.DataFrame(columns=STK_BALANCE_SHEET_SCHEMA)

        elif table_name == "STK_INCOME_STATEMENT":
            if code:
                return get_income_statement(code, **kwargs)
            return pd.DataFrame(columns=STK_INCOME_STATEMENT_SCHEMA)

        elif table_name == "STK_CASHFLOW_STATEMENT":
            if code:
                return get_cashflow_statement(code, **kwargs)
            return pd.DataFrame(columns=STK_CASHFLOW_STATEMENT_SCHEMA)

        elif table_name == "FUND_NET_VALUE":
            if code:
                return get_fund_net_value(code, **kwargs)
            return pd.DataFrame(columns=FUND_NET_VALUE_SCHEMA)

        elif table_name == "FUND_PORTFOLIO":
            if code:
                return get_fund_portfolio(code, **kwargs)
            return pd.DataFrame(columns=FUND_PORTFOLIO_SCHEMA)

        else:
            raise ValueError(f"不支持的表: {table_name}")


# 创建全局实例
finance_tables = FinanceTables()


__all__ = [
    "STK_BALANCE_SHEET_SCHEMA",
    "STK_INCOME_STATEMENT_SCHEMA",
    "STK_CASHFLOW_STATEMENT_SCHEMA",
    "FUND_NET_VALUE_SCHEMA",
    "FUND_PORTFOLIO_SCHEMA",
    "get_balance_sheet",
    "get_income_statement",
    "get_cashflow_statement",
    "get_fund_net_value",
    "get_fund_portfolio",
    "FinanceTables",
    "finance_tables",
]