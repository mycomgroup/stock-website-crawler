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
    "code",  # 股票代码
    "pub_date",  # 公告日期
    "stat_date",  # 统计日期
    "total_assets",  # 资产总计
    "total_liability",  # 负债合计
    "total_equity",  # 所有者权益合计
    "total_current_assets",  # 流动资产合计
    "total_current_liability",  # 流动负债合计
    "total_non_current_assets",  # 非流动资产合计
    "total_non_current_liability",  # 非流动负债合计
    "capital_reserve",  # 资本公积
    "surplus_reserve",  # 盈余公积
    "retained_earnings",  # 未分配利润
    "paid_in_capital",  # 实收资本
    "inventory",  # 存货
    "account_receivable",  # 应收账款
    "cash_and_equivalents",  # 货币资金
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
    from jk2bt.data.sources import get_adapter

    # 标准化代码格式
    code = symbol.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

    try:
        # 尝试获取资产负债表数据
        df = get_adapter().get_financial_report(symbol=code, report_type="资产负债表")

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
    "operating_revenue",  # 营业收入
    "total_operating_cost",  # 营业总成本
    "operating_cost",  # 营业成本
    "operating_profit",  # 营业利润
    "total_profit",  # 利润总额
    "net_profit",  # 净利润
    "net_profit_to_shareholders",  # 归属于母公司股东的净利润
    "basic_eps",  # 基本每股收益
    "diluted_eps",  # 稀释每股收益
    "gross_profit",  # 毛利
]


def get_income_statement(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取利润表数据
    """
    from jk2bt.data.sources import get_adapter

    code = symbol.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

    try:
        df = get_adapter().get_financial_report(symbol=code, report_type="利润表")

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
    "net_cashflow_operating",  # 经营活动产生的现金流量净额
    "net_cashflow_investing",  # 投资活动产生的现金流量净额
    "net_cashflow_financing",  # 筹资活动产生的现金流量净额
    "net_increase_cash",  # 现金及现金等价物净增加额
    "cash_equivalent_begin",  # 期初现金及现金等价物余额
    "cash_equivalent_end",  # 期末现金及现金等价物余额
]


def get_cashflow_statement(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取现金流量表数据
    """
    from jk2bt.data.sources import get_adapter

    code = symbol.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

    try:
        df = get_adapter().get_financial_report(symbol=code, report_type="现金流量表")

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
    "code",  # 基金代码
    "date",  # 日期
    "net_value",  # 单位净值
    "accumulated_value",  # 累计净值
    "daily_growth",  # 日增长率
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
    from jk2bt.data.sources import get_adapter

    try:
        # 获取基金历史净值
        df = get_adapter().get_fund_net_value_hist(
            fund_code=fund_code, indicator="单位净值走势"
        )

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
    "fund_code",  # 基金代码
    "stock_code",  # 股票代码
    "stock_name",  # 股票名称
    "shares",  # 持股数量
    "market_value",  # 市值
    "weight",  # 占净值比例
    "report_date",  # 报告日期
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
    from jk2bt.data.sources import get_adapter

    try:
        # 获取基金股票持仓
        df = get_adapter().get_fund_portfolio(fund_code=fund_code)

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
# 基金分红拆分
# =====================================================================

FUND_DIVIDEND_SCHEMA = [
    "code",  # 基金代码
    "date",  # 公告日期
    "type",  # 类型（分红/拆分）
    "dividend",  # 每份分红金额
    "split_ratio",  # 拆分比例
]


def get_fund_dividend(
    fund_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取基金分红拆分数据

    参数:
        fund_code: 基金代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含基金分红拆分数据
    """
    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_fund_dividend(fund_code=fund_code)

        if df is None or df.empty:
            return pd.DataFrame(columns=FUND_DIVIDEND_SCHEMA)

        column_mapping = {
            "公告日": "date",
            "分红": "dividend",
            "拆分": "split_ratio",
            "类型": "type",
            "每份分红": "dividend",
            "拆分比例": "split_ratio",
        }

        df = df.rename(columns=column_mapping)
        df["code"] = fund_code

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            if start_date:
                df = df[df["date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["date"] <= pd.to_datetime(end_date)]

        if "type" not in df.columns:
            df["type"] = df.apply(
                lambda row: "分红" if pd.notna(row.get("dividend")) else "拆分",
                axis=1,
            )

        available_cols = [c for c in FUND_DIVIDEND_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取基金分红拆分失败 {fund_code}: {e}")
        return pd.DataFrame(columns=FUND_DIVIDEND_SCHEMA)


# =====================================================================
# 基金净值及业绩表现
# =====================================================================

FUND_PERFORMANCE_SCHEMA = [
    "code",  # 基金代码
    "date",  # 日期
    "unit_nav",  # 单位净值
    "acc_nav",  # 累计净值
    "accumulated_nav",  # 复权净值
    "growth_rate",  # 日增长率
    "return_1m",  # 近1月收益
    "return_3m",  # 近3月收益
    "return_6m",  # 近6月收益
    "return_1y",  # 近1年收益
    "return_3y",  # 近3年收益
    "return_5y",  # 近5年收益
]


def get_fund_performance(
    fund_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取基金净值及业绩表现数据

    参数:
        fund_code: 基金代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含基金净值及业绩表现数据
    """
    from jk2bt.data.sources import get_adapter

    try:
        df_unit = get_adapter().get_fund_net_value_hist(
            fund_code=fund_code, indicator="单位净值走势"
        )
        df_acc = get_adapter().get_fund_net_value_hist(
            fund_code=fund_code, indicator="累计净值走势"
        )

        if df_unit is None or df_unit.empty:
            return pd.DataFrame(columns=FUND_PERFORMANCE_SCHEMA)

        column_mapping = {
            "净值日期": "date",
            "单位净值": "unit_nav",
            "累计净值": "acc_nav",
            "日增长率": "growth_rate",
        }

        df = df_unit.rename(columns=column_mapping)
        df["code"] = fund_code

        if df_acc is not None and not df_acc.empty:
            acc_mapping = {"净值日期": "date", "累计净值": "accumulated_nav"}
            df_acc = df_acc.rename(columns=acc_mapping)
            if "accumulated_nav" in df_acc.columns and "date" in df_acc.columns:
                acc_dict = dict(
                    zip(df_acc["date"].astype(str), df_acc["accumulated_nav"])
                )
                df["accumulated_nav"] = df["date"].astype(str).map(acc_dict)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            if start_date:
                df = df[df["date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["date"] <= pd.to_datetime(end_date)]

            if len(df) > 1:
                df_sorted = df.sort_values("date").reset_index(drop=True)
                nav_col = "unit_nav" if "unit_nav" in df_sorted.columns else "acc_nav"
                if nav_col in df_sorted.columns:
                    nav_values = pd.to_numeric(df_sorted[nav_col], errors="coerce")
                    if len(nav_values) >= 2:
                        current_nav = nav_values.iloc[-1]
                        if current_nav > 0:
                            for period_days, col_name in [
                                (20, "return_1m"),
                                (60, "return_3m"),
                                (120, "return_6m"),
                                (252, "return_1y"),
                                (756, "return_3y"),
                                (1260, "return_5y"),
                            ]:
                                if len(nav_values) > period_days:
                                    past_nav = nav_values.iloc[-(period_days + 1)]
                                    if past_nav > 0:
                                        df_sorted.loc[df_sorted.index[-1], col_name] = (
                                            round((current_nav / past_nav - 1) * 100, 2)
                                        )
                                    else:
                                        df_sorted.loc[df_sorted.index[-1], col_name] = (
                                            None
                                        )
                                else:
                                    df_sorted.loc[df_sorted.index[-1], col_name] = None

                df = df_sorted

        for col in FUND_PERFORMANCE_SCHEMA:
            if col not in df.columns:
                df[col] = None

        available_cols = [c for c in FUND_PERFORMANCE_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取基金业绩表现失败 {fund_code}: {e}")
        return pd.DataFrame(columns=FUND_PERFORMANCE_SCHEMA)


# =====================================================================
# 期货保证金
# =====================================================================

FUT_MARGIN_SCHEMA = [
    "day",  # 日期
    "code",  # 合约代码
    "exchange",  # 交易所
    "exchange_name",  # 交易所名称
    "specul_buy_margin_rate",  # 投机买保证金比例
    "specul_sell_margin_rate",  # 投机卖保证金比例
    "hedg_buy_margin_rate",  # 套保买保证金比例
    "hedg_sell_margin_rate",  # 套保卖保证金比例
]


def get_futures_margin(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货保证金数据

    参数:
        code: 合约代码或品种代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含期货保证金数据
    """
    import akshare as ak

    try:
        df = ak.futures_contract_info_shfe_dce_czce()
        if df is None or df.empty:
            return pd.DataFrame(columns=FUT_MARGIN_SCHEMA)

        column_mapping = {
            "交易日": "day",
            "合约": "code",
            "交易所": "exchange",
            "交易所名称": "exchange_name",
            "投机买保证金比例": "specul_buy_margin_rate",
            "投机卖保证金比例": "specul_sell_margin_rate",
            "套保买保证金比例": "hedg_buy_margin_rate",
            "套保卖保证金比例": "hedg_sell_margin_rate",
        }

        df = df.rename(columns=column_mapping)

        if "day" in df.columns:
            df["day"] = pd.to_datetime(df["day"], errors="coerce")
            if start_date:
                df = df[df["day"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["day"] <= pd.to_datetime(end_date)]

        if code:
            df = df[df["code"].str.contains(code.upper(), case=False, na=False)]

        available_cols = [c for c in FUT_MARGIN_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取期货保证金数据失败: {e}")
        return _get_default_margin_data(code, start_date, end_date)


def _get_default_margin_data(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取默认保证金数据（基于交易所标准）

    参数:
        code: 合约代码或品种代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含默认保证金数据
    """
    from jk2bt.data.market.futures import CHINA_FUTURE_EXCHANGE_INFO

    results = []
    today = pd.Timestamp.now().strftime("%Y-%m-%d")

    for exchange, info in CHINA_FUTURE_EXCHANGE_INFO.items():
        exchange_name = info["name"]
        for product, margin_rate in info["margin_rates"].items():
            if code and code.upper() not in product:
                continue
            results.append(
                {
                    "day": today,
                    "code": product,
                    "exchange": exchange,
                    "exchange_name": exchange_name,
                    "specul_buy_margin_rate": margin_rate,
                    "specul_sell_margin_rate": margin_rate,
                    "hedg_buy_margin_rate": margin_rate * 0.8,
                    "hedg_sell_margin_rate": margin_rate * 0.8,
                }
            )

    df = pd.DataFrame(results)

    if start_date:
        df = df[df["day"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["day"] <= pd.to_datetime(end_date)]

    return df


# =====================================================================
# 期货手续费
# =====================================================================

FUT_CHARGE_SCHEMA = [
    "day",  # 日期
    "code",  # 合约代码
    "exchange",  # 交易所
    "exchange_name",  # 交易所名称
    "unit",  # 计费方式 (按手/按金额)
    "clearance_charge",  # 平仓手续费
    "opening_charge",  # 开仓手续费
    "short_clearance_charge",  # 平今仓手续费
    "short_opening_charge",  # 开今仓手续费
]


def get_futures_charge(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货手续费数据

    参数:
        code: 合约代码或品种代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含期货手续费数据
    """
    import akshare as ak

    try:
        df = ak.futures_comm_info()
        if df is None or df.empty:
            return pd.DataFrame(columns=FUT_CHARGE_SCHEMA)

        column_mapping = {
            "交易日": "day",
            "合约": "code",
            "交易所": "exchange",
            "交易所名称": "exchange_name",
            "计费方式": "unit",
            "平仓手续费": "clearance_charge",
            "开仓手续费": "opening_charge",
            "平今仓手续费": "short_clearance_charge",
            "开今仓手续费": "short_opening_charge",
        }

        df = df.rename(columns=column_mapping)

        if "day" in df.columns:
            df["day"] = pd.to_datetime(df["day"], errors="coerce")
            if start_date:
                df = df[df["day"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["day"] <= pd.to_datetime(end_date)]

        if code:
            df = df[df["code"].str.contains(code.upper(), case=False, na=False)]

        available_cols = [c for c in FUT_CHARGE_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取期货手续费数据失败: {e}")
        return _get_default_charge_data(code, start_date, end_date)


def _get_default_charge_data(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取默认手续费数据

    参数:
        code: 合约代码或品种代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含默认手续费数据
    """
    from jk2bt.data.market.futures import CHINA_FUTURE_EXCHANGE_INFO

    results = []
    today = pd.Timestamp.now().strftime("%Y-%m-%d")

    default_charges = {
        "CFFEX": {
            "opening": 0.000023,
            "clearance": 0.000023,
            "short_clearance": 0.000345,
            "unit": "按金额",
        },
        "SHFE": {
            "opening": 0.0001,
            "clearance": 0.0001,
            "short_clearance": 0.0001,
            "unit": "按手",
        },
        "DCE": {
            "opening": 0.0001,
            "clearance": 0.0001,
            "short_clearance": 0.0001,
            "unit": "按手",
        },
        "CZCE": {
            "opening": 3.0,
            "clearance": 3.0,
            "short_clearance": 0.0,
            "unit": "按手",
        },
        "INE": {
            "opening": 0.0001,
            "clearance": 0.0001,
            "short_clearance": 0.0,
            "unit": "按手",
        },
    }

    for exchange, info in CHINA_FUTURE_EXCHANGE_INFO.items():
        exchange_name = info["name"]
        charge_info = default_charges.get(
            exchange,
            {
                "opening": 0.0001,
                "clearance": 0.0001,
                "short_clearance": 0.0,
                "unit": "按手",
            },
        )
        for product in info["products"]:
            if code and code.upper() not in product:
                continue
            results.append(
                {
                    "day": today,
                    "code": product,
                    "exchange": exchange,
                    "exchange_name": exchange_name,
                    "unit": charge_info["unit"],
                    "clearance_charge": charge_info["clearance"],
                    "opening_charge": charge_info["opening"],
                    "short_clearance_charge": charge_info["short_clearance"],
                    "short_opening_charge": charge_info["opening"],
                }
            )

    df = pd.DataFrame(results)

    if start_date:
        df = df[df["day"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["day"] <= pd.to_datetime(end_date)]

    return df


# =====================================================================
# 期货仓单
# =====================================================================

FUT_WAREHOUSE_SCHEMA = [
    "day",  # 日期
    "symbol",  # 品种
    "warehouse_receipt",  # 仓单数量
    "warehouse_name",  # 仓库名称
    "region",  # 地区
]


def get_futures_warehouse(
    symbol: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货仓单数据

    参数:
        symbol: 品种代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含期货仓单数据
    """
    import akshare as ak

    try:
        df = ak.futures_warehouse_receipt()
        if df is None or df.empty:
            return pd.DataFrame(columns=FUT_WAREHOUSE_SCHEMA)

        column_mapping = {
            "日期": "day",
            "品种": "symbol",
            "仓单": "warehouse_receipt",
            "仓库名称": "warehouse_name",
            "地区": "region",
        }

        df = df.rename(columns=column_mapping)

        if "day" in df.columns:
            df["day"] = pd.to_datetime(df["day"], errors="coerce")
            if start_date:
                df = df[df["day"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["day"] <= pd.to_datetime(end_date)]

        if symbol:
            df = df[df["symbol"].str.contains(symbol.upper(), case=False, na=False)]

        available_cols = [c for c in FUT_WAREHOUSE_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取期货仓单数据失败: {e}")
        return pd.DataFrame(columns=FUT_WAREHOUSE_SCHEMA)


# =====================================================================
# 期货会员持仓（龙虎榜）
# =====================================================================

FUT_MEMBER_POSITION_SCHEMA = [
    "day",  # 日期
    "symbol",  # 合约代码
    "broker",  # 会员名称
    "long_holding",  # 多头持仓
    "long_change",  # 多头变化
    "short_holding",  # 空头持仓
    "short_change",  # 空头变化
    "volume",  # 成交量
    "volume_change",  # 成交量变化
]


def get_futures_member_position(
    symbol: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    exchange: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货会员持仓数据（龙虎榜）

    参数:
        symbol: 合约代码
        start_date: 开始日期
        end_date: 结束日期
        exchange: 交易所代码 (CFFEX/SHFE/DCE/CZCE)

    返回:
        DataFrame，包含期货会员持仓数据
    """
    import akshare as ak

    all_data = []

    exchange_funcs = {
        "SHFE": ("futures_shfe_position_rank", {}),
        "DCE": ("futures_dce_position_rank", {}),
        "CZCE": ("futures_czce_position_rank", {}),
        "CFFEX": ("futures_cffex_position_rank", {}),
    }

    exchanges_to_query = [exchange.upper()] if exchange else list(exchange_funcs.keys())

    for exch in exchanges_to_query:
        if exch not in exchange_funcs:
            continue
        func_name, kwargs = exchange_funcs[exch]
        try:
            func = getattr(ak, func_name)
            df = func(**kwargs)
            if df is not None and not df.empty:
                df["exchange"] = exch
                all_data.append(df)
        except Exception as e:
            warnings.warn(f"获取 {exch} 会员持仓数据失败: {e}")

    if not all_data:
        return pd.DataFrame(columns=FUT_MEMBER_POSITION_SCHEMA)

    df = pd.concat(all_data, ignore_index=True)

    column_mapping = {
        "日期": "day",
        "合约": "symbol",
        "会员": "broker",
        "多头": "long_holding",
        "多头变化": "long_change",
        "空头": "short_holding",
        "空头变化": "short_change",
        "成交量": "volume",
        "成交量变化": "volume_change",
    }

    df = df.rename(columns=column_mapping)

    if "day" in df.columns:
        df["day"] = pd.to_datetime(df["day"], errors="coerce")
        if start_date:
            df = df[df["day"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["day"] <= pd.to_datetime(end_date)]

    if symbol:
        df = df[df["symbol"].str.contains(symbol.upper(), case=False, na=False)]

    available_cols = [c for c in FUT_MEMBER_POSITION_SCHEMA if c in df.columns]
    return df[available_cols]


# =====================================================================
# 期权盘前静态数据
# =====================================================================

OPT_DAILY_PREOPEN_SCHEMA = [
    "date",  # 日期
    "option_code",  # 期权代码
    "option_name",  # 期权名称
    "underlying_code",  # 标的代码
    "pre_settle",  # 前结算价
    "pre_close",  # 前收盘价
    "pre_position",  # 前持仓量
    "limit_up",  # 涨停价
    "limit_down",  # 跌停价
]


def get_option_preopen(
    date: Optional[str] = None,
    exchange: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期权每日盘前静态数据

    参数:
        date: 日期 'YYYY-MM-DD'
        exchange: 交易所 'sse', 'szse', 'cffex', 'all'

    返回:
        DataFrame，包含期权盘前静态数据
    """
    try:
        from jk2bt.api.option import get_option_preopen as _get_option_preopen

        result = _get_option_preopen(date=date, exchange=exchange)
        if result.success and result.data is not None:
            return result.data
        return pd.DataFrame(columns=OPT_DAILY_PREOPEN_SCHEMA)
    except Exception as e:
        warnings.warn(f"获取期权盘前数据失败: {e}")
        return pd.DataFrame(columns=OPT_DAILY_PREOPEN_SCHEMA)


# =====================================================================
# 沪深市场每日成交概况
# =====================================================================

STK_EXCHANGE_TRADE_INFO_SCHEMA = [
    "date",  # 日期
    "sh_turnover",  # 上海成交额(亿元)
    "sh_trade_count",  # 上海成交笔数
    "sz_turnover",  # 深圳成交额(亿元)
    "sz_trade_count",  # 深圳成交笔数
    "total_turnover",  # 总成交额(亿元)
]


def get_exchange_trade_info(
    date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取沪深市场每日成交概况

    参数:
        date: 指定日期
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含沪深市场每日成交概况
    """
    raise NotImplementedError(
        "STK_EXCHANGE_TRADE_INFO 需要专业数据源。请替换为其他数据源（如Tushare/Wind）。"
    )


# =====================================================================
# 基金财务指标
# =====================================================================

FUND_FIN_INDICATOR_SCHEMA = [
    "code",  # 基金代码
    "date",  # 日期
    "profit",  # 利润
    "adjust_profit",  # 调整后利润
    "avg_roe",  # 平均净资产收益率
    "nav_growth",  # 净值增长率
    "total_asset",  # 总资产
    "net_asset",  # 净资产
    "operating_revenue",  # 营业收入
    "net_profit",  # 净利润
    "eps",  # 每股收益
    "bvps",  # 每份净资产
    "operating_cash_flow_per_share",  # 每股经营现金流
]


def get_fund_fin_indicator(
    fund_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取基金财务指标数据

    参数:
        fund_code: 基金代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含基金财务指标数据
    """
    import akshare as ak

    try:
        # 尝试获取基金开放信息
        df = ak.fund_open_fund_info_em(symbol=fund_code, indicator="单位净值走势")
        if df is None or df.empty:
            return pd.DataFrame(columns=FUND_FIN_INDICATOR_SCHEMA)

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

        # 从净值数据计算财务指标
        if "net_value" in df.columns and len(df) > 1:
            df["nav_growth"] = df["net_value"].pct_change()
            df["total_asset"] = None
            df["net_asset"] = (
                df["accumulated_value"] if "accumulated_value" in df.columns else None
            )
            df["profit"] = None
            df["adjust_profit"] = None
            df["avg_roe"] = None
            df["operating_revenue"] = None
            df["net_profit"] = None
            df["eps"] = None
            df["bvps"] = df["net_value"]
            df["operating_cash_flow_per_share"] = None

        available_cols = [c for c in FUND_FIN_INDICATOR_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取基金财务指标失败 {fund_code}: {e}")
        return pd.DataFrame(columns=FUND_FIN_INDICATOR_SCHEMA)


# =====================================================================
# 基金投资标的(ETF跟踪指数)
# =====================================================================

FUND_INVEST_TARGET_SCHEMA = [
    "code",  # 基金代码
    "fund_name",  # 基金名称
    "index_code",  # 指数代码
    "index_name",  # 指数名称
    "tracking_error",  # 跟踪误差
    "tracking_deviation",  # 跟踪偏离度
]


def get_fund_invest_target(
    fund_code: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取ETF跟踪指数信息

    参数:
        fund_code: 基金代码（可选，不传则返回全部ETF）

    返回:
        DataFrame，包含ETF跟踪指数信息
    """
    import akshare as ak

    try:
        # 获取ETF现货数据
        df = ak.fund_etf_spot_em()
        if df is None or df.empty:
            return pd.DataFrame(columns=FUND_INVEST_TARGET_SCHEMA)

        column_mapping = {}
        for col in df.columns:
            if "代码" in col or col == "代码":
                column_mapping[col] = "code"
            elif "名称" in col:
                column_mapping[col] = "fund_name"

        df = df.rename(columns=column_mapping)

        # 尝试获取指数基金信息来补充指数数据
        try:
            index_df = ak.fund_index_fund_em()
            if index_df is not None and not index_df.empty:
                index_map = {}
                for _, row in index_df.iterrows():
                    code_col = None
                    name_col = None
                    idx_code_col = None
                    idx_name_col = None
                    for c in index_df.columns:
                        if "基金代码" in c or "代码" == c.strip():
                            code_col = c
                        elif "基金名称" in c or "名称" == c.strip():
                            name_col = c
                        elif "指数代码" in c:
                            idx_code_col = c
                        elif "指数名称" in c:
                            idx_name_col = c
                    if code_col and idx_code_col:
                        fund_c = str(index_df.loc[_, code_col]).strip()
                        index_map[fund_c] = {
                            "index_code": str(index_df.loc[_, idx_code_col]).strip()
                            if idx_code_col
                            else None,
                            "index_name": str(index_df.loc[_, idx_name_col]).strip()
                            if idx_name_col and pd.notna(index_df.loc[_, idx_name_col])
                            else None,
                        }

                df["index_code"] = df["code"].map(
                    lambda x: index_map.get(str(x), {}).get("index_code")
                )
                df["index_name"] = df["code"].map(
                    lambda x: index_map.get(str(x), {}).get("index_name")
                )
        except Exception:
            pass

        df["tracking_error"] = None
        df["tracking_deviation"] = None

        if fund_code:
            df = df[
                df["code"]
                .astype(str)
                .str.contains(
                    fund_code.replace(".XSHG", "").replace(".XSHE", ""), na=False
                )
            ]

        available_cols = [c for c in FUND_INVEST_TARGET_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取ETF跟踪指数信息失败: {e}")
        return pd.DataFrame(columns=FUND_INVEST_TARGET_SCHEMA)


# =====================================================================
# 货币基金收益日报
# =====================================================================

FUND_MF_DAILY_PROFIT_SCHEMA = [
    "code",  # 基金代码
    "date",  # 日期
    "profit_per_million",  # 每万份收益
    "seven_day_yield",  # 7日年化收益率
    "five_day_avg_yield",  # 5日均价收益率
]


def get_fund_mf_daily_profit(
    fund_code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取货币基金收益日报

    参数:
        fund_code: 基金代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含货币基金收益数据
    """
    import akshare as ak

    try:
        df = ak.fund_money_fund_info_em()
        if df is None or df.empty:
            return pd.DataFrame(columns=FUND_MF_DAILY_PROFIT_SCHEMA)

        column_mapping = {
            "净值日期": "date",
            "每万份收益": "profit_per_million",
            "7日年化收益率": "seven_day_yield",
        }

        df = df.rename(columns=column_mapping)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            if start_date:
                df = df[df["date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["date"] <= pd.to_datetime(end_date)]

        if fund_code:
            df["code"] = fund_code

        available_cols = [c for c in FUND_MF_DAILY_PROFIT_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取货币基金收益失败: {e}")
        return pd.DataFrame(columns=FUND_MF_DAILY_PROFIT_SCHEMA)


# =====================================================================
# 审计报告
# =====================================================================

STK_AUDIT_OPINION_SCHEMA = [
    "code",  # 股票代码
    "pub_date",  # 公告日期
    "report_date",  # 报告日期
    "auditor",  # 审计机构
    "opinion_type",  # 审计意见类型
    "opinion_content",  # 审计意见内容
]


def get_audit_opinion(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取审计报告数据

    参数:
        code: 股票代码
        start_date: 开始日期
        end_date: 结束日期

    返回:
        DataFrame，包含审计报告数据
    """
    raise NotImplementedError(
        "STK_AUDIT_OPINION 需要专业数据源。请替换为其他数据源（如Tushare/Wind）。"
    )


# =====================================================================
# 定期报告预约披露时间表
# =====================================================================

STK_REPORT_DISCLOSURE_SCHEMA = [
    "code",  # 股票代码
    "report_type",  # 报告类型
    "scheduled_date",  # 预约披露日期
    "actual_date",  # 实际披露日期
    "report_date",  # 报告日期
]


def get_report_disclosure(
    code: Optional[str] = None,
    year: str = "2024",
) -> pd.DataFrame:
    """
    获取定期报告预约披露时间表

    参数:
        code: 股票代码
        year: 年份

    返回:
        DataFrame，包含预约披露时间数据
    """
    import akshare as ak

    try:
        df = ak.stock_report_disclosure(year=year)
        if df is None or df.empty:
            return pd.DataFrame(columns=STK_REPORT_DISCLOSURE_SCHEMA)

        column_mapping = {
            "股票代码": "code",
            "股票简称": "stock_name",
            "首次预约": "scheduled_date",
            "初次变更": "first_change",
            "二次变更": "second_change",
            "三次变更": "third_change",
            "实际披露": "actual_date",
        }

        df = df.rename(columns=column_mapping)

        df["report_type"] = f"{year}年年报"

        if "scheduled_date" in df.columns:
            df["scheduled_date"] = pd.to_datetime(df["scheduled_date"], errors="coerce")
            df["report_date"] = f"{year}-12-31"

        if code:
            code = code.replace(".XSHG", "").replace(".XSHE", "").zfill(6)
            df = df[df["code"] == code]

        available_cols = [c for c in STK_REPORT_DISCLOSURE_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取预约披露时间失败: {e}")
        return pd.DataFrame(columns=STK_REPORT_DISCLOSURE_SCHEMA)


# =====================================================================
# 业绩快报
# =====================================================================

STK_PERFORMANCE_LETTERS_SCHEMA = [
    "code",  # 股票代码
    "pub_date",  # 公告日期
    "report_date",  # 报告日期
    "eps",  # 每股收益
    "revenue",  # 营业收入
    "net_profit",  # 净利润
    "yoy_revenue",  # 营收同比
    "yoy_profit",  # 利润同比
]


def get_performance_letters(
    code: Optional[str] = None,
    date: str = "2024-03-31",
) -> pd.DataFrame:
    """
    获取业绩快报数据

    参数:
        code: 股票代码
        date: 报告期

    返回:
        DataFrame，包含业绩快报数据
    """
    import akshare as ak

    try:
        df = ak.stock_yjkb_em(date=date)
        if df is None or df.empty:
            return pd.DataFrame(columns=STK_PERFORMANCE_LETTERS_SCHEMA)

        column_mapping = {
            "股票代码": "code",
            "公告日期": "pub_date",
            "每股收益": "eps",
            "营业收入": "revenue",
            "净利润": "net_profit",
            "营业收入同比增长": "yoy_revenue",
            "净利润同比增长": "yoy_profit",
        }

        df = df.rename(columns=column_mapping)

        if "pub_date" in df.columns:
            df["pub_date"] = pd.to_datetime(df["pub_date"], errors="coerce")
            df["report_date"] = date

        if code:
            code = code.replace(".XSHG", "").replace(".XSHE", "").zfill(6)
            df = df[df["code"] == code]

        available_cols = [c for c in STK_PERFORMANCE_LETTERS_SCHEMA if c in df.columns]
        return df[available_cols]

    except Exception as e:
        warnings.warn(f"获取业绩快报失败: {e}")
        return pd.DataFrame(columns=STK_PERFORMANCE_LETTERS_SCHEMA)


# =====================================================================
# 金融类财务报表 -  stubs
# =====================================================================

FINANCE_INCOME_STATEMENT_SCHEMA = [
    "id",
    "company_id",
    "company_name",
    "code",
    "a_code",
    "b_code",
    "h_code",
    "pub_date",
    "start_date",
    "end_date",
    "report_date",
    "report_type",
    "source_id",
    "source",
    "operating_revenue",
    "interest_net_revenue",
    "interest_income",
    "interest_expense",
    "commission_net_income",
    "commission_income",
    "commission_expense",
    "investment_income",
    "fair_value_variable_income",
    "operating_profit",
    "total_profit",
    "income_tax_expense",
    "net_profit",
    "np_parent_company_owners",
    "minority_profit",
    "basic_eps",
    "diluted_eps",
]


def get_finance_income_statement(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """获取金融类上市公司利润表"""
    raise NotImplementedError(
        "FINANCE_INCOME_STATEMENT 需要专业数据源。请替换为其他数据源（如Tushare/Wind）。"
    )


FINANCE_CASHFLOW_STATEMENT_SCHEMA = [
    "id",
    "company_id",
    "company_name",
    "code",
    "a_code",
    "b_code",
    "h_code",
    "pub_date",
    "start_date",
    "end_date",
    "report_date",
    "report_type",
    "source_id",
    "source",
    "operate_cash_flow",
    "net_operate_cash_flow",
    "net_invest_cash_flow",
    "net_finance_cash_flow",
    "net_cash_increase",
]


def get_finance_cashflow_statement(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """获取金融类上市公司现金流量表"""
    raise NotImplementedError(
        "FINANCE_CASHFLOW_STATEMENT 需要专业数据源。请替换为其他数据源（如Tushare/Wind）。"
    )


FINANCE_BALANCE_SHEET_PARENT_SCHEMA = [
    "id",
    "company_id",
    "company_name",
    "code",
    "a_code",
    "b_code",
    "h_code",
    "pub_date",
    "start_date",
    "end_date",
    "report_date",
    "report_type",
    "source_id",
    "source",
    "cash_equivalents",
    "total_assets",
    "total_liability",
    "total_equity",
    "accounts_receivable",
    "accounts_payable",
    "inventory",
    "fixed_assets",
    "intangible_assets",
    "longterm_equity_invest",
    "shortterm_loan",
    "longterm_loan",
    "total_debt",
]


def get_finance_balance_sheet_parent(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """获取金融类上市公司资产负债表（母公司）"""
    raise NotImplementedError(
        "FINANCE_BALANCE_SHEET_PARENT 需要专业数据源。请替换为其他数据源（如Tushare/Wind）。"
    )


FINANCE_INCOME_STATEMENT_PARENT_NEW_SCHEMA = [
    "id",
    "company_id",
    "company_name",
    "code",
    "a_code",
    "b_code",
    "h_code",
    "pub_date",
    "start_date",
    "end_date",
    "report_date",
    "report_type",
    "source_id",
    "source",
    "operating_revenue",
    "interest_net_revenue",
    "interest_income",
    "interest_expense",
    "commission_net_income",
    "commission_income",
    "commission_expense",
    "investment_income",
    "fair_value_variable_income",
    "operating_profit",
    "total_profit",
    "income_tax_expense",
    "net_profit",
    "np_parent_company_owners",
    "minority_profit",
    "basic_eps",
    "diluted_eps",
]


def get_finance_income_statement_parent(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """获取金融类上市公司利润表（母公司）"""
    raise NotImplementedError(
        "FINANCE_INCOME_STATEMENT_PARENT 需要专业数据源。请替换为其他数据源（如Tushare/Wind）。"
    )


FINANCE_CASHFLOW_STATEMENT_PARENT_NEW_SCHEMA = [
    "id",
    "company_id",
    "company_name",
    "code",
    "a_code",
    "b_code",
    "h_code",
    "pub_date",
    "start_date",
    "end_date",
    "report_date",
    "report_type",
    "source_id",
    "source",
    "operate_cash_flow",
    "net_operate_cash_flow",
    "net_invest_cash_flow",
    "net_finance_cash_flow",
    "net_cash_increase",
]


def get_finance_cashflow_statement_parent(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """获取金融类上市公司现金流量表（母公司）"""
    raise NotImplementedError(
        "FINANCE_CASHFLOW_STATEMENT_PARENT 需要专业数据源。请替换为其他数据源（如Tushare/Wind）。"
    )


FINANCE_BALANCE_SHEET_NEW_SCHEMA = [
    "id",
    "company_id",
    "company_name",
    "code",
    "a_code",
    "b_code",
    "h_code",
    "pub_date",
    "start_date",
    "end_date",
    "report_date",
    "report_type",
    "source_id",
    "source",
    "cash_equivalents",
    "total_assets",
    "total_liability",
    "total_equity",
    "accounts_receivable",
    "accounts_payable",
    "inventory",
    "fixed_assets",
    "intangible_assets",
    "longterm_equity_invest",
    "shortterm_loan",
    "longterm_loan",
    "total_debt",
]


def get_finance_balance_sheet(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """获取金融类上市公司资产负债表"""
    raise NotImplementedError(
        "FINANCE_BALANCE_SHEET 需要专业数据源。请替换为其他数据源（如Tushare/Wind）。"
    )


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

    # 基金分红拆分
    class FUND_DIVIDEND:
        code = None
        date = None
        type = None
        dividend = None
        split_ratio = None

    # 基金净值及业绩表现
    class FUND_PERFORMANCE:
        code = None
        date = None
        unit_nav = None
        acc_nav = None
        accumulated_nav = None
        growth_rate = None
        return_1m = None
        return_3m = None
        return_6m = None
        return_1y = None
        return_3y = None
        return_5y = None

    # 基金财务指标
    class FUND_FIN_INDICATOR:
        code = None
        date = None
        profit = None
        adjust_profit = None
        avg_roe = None
        nav_growth = None
        total_asset = None
        net_asset = None
        operating_revenue = None
        net_profit = None
        eps = None
        bvps = None
        operating_cash_flow_per_share = None

    # 基金投资标的(ETF跟踪指数)
    class FUND_INVEST_TARGET:
        code = None
        fund_name = None
        index_code = None
        index_name = None
        tracking_error = None
        tracking_deviation = None

    # 期货保证金
    class FUT_MARGIN:
        day = None
        code = None
        exchange = None
        exchange_name = None
        specul_buy_margin_rate = None
        specul_sell_margin_rate = None
        hedg_buy_margin_rate = None
        hedg_sell_margin_rate = None

    # 期货手续费
    class FUT_CHARGE:
        day = None
        code = None
        exchange = None
        exchange_name = None
        unit = None
        clearance_charge = None
        opening_charge = None
        short_clearance_charge = None
        short_opening_charge = None

    # 期货仓单
    class FUT_WAREHOUSE:
        day = None
        symbol = None
        warehouse_receipt = None
        warehouse_name = None
        region = None

    # 期货会员持仓
    class FUT_MEMBER_POSITION:
        day = None
        symbol = None
        broker = None
        long_holding = None
        long_change = None
        short_holding = None
        short_change = None
        volume = None
        volume_change = None

    # 期权盘前静态数据
    class OPT_DAILY_PREOPEN:
        date = None
        option_code = None
        option_name = None
        underlying_code = None
        pre_settle = None
        pre_close = None
        pre_position = None
        limit_up = None
        limit_down = None

    # 沪深市场每日成交概况
    class STK_EXCHANGE_TRADE_INFO:
        date = None
        sh_turnover = None
        sh_trade_count = None
        sz_turnover = None
        sz_trade_count = None
        total_turnover = None

    # 货币基金收益日报
    class FUND_MF_DAILY_PROFIT:
        code = None
        date = None
        profit_per_million = None
        seven_day_yield = None
        five_day_avg_yield = None

    # 审计报告
    class STK_AUDIT_OPINION:
        code = None
        pub_date = None
        report_date = None
        auditor = None
        opinion_type = None
        opinion_content = None

    # 定期报告预约披露时间表
    class STK_REPORT_DISCLOSURE:
        code = None
        report_type = None
        scheduled_date = None
        actual_date = None
        report_date = None

    # 业绩快报
    class STK_PERFORMANCE_LETTERS:
        code = None
        pub_date = None
        report_date = None
        eps = None
        revenue = None
        net_profit = None
        yoy_revenue = None
        yoy_profit = None

    # 金融类利润表
    class FINANCE_INCOME_STATEMENT:
        id = None
        company_id = None
        company_name = None
        code = None
        a_code = None
        b_code = None
        h_code = None
        pub_date = None
        start_date = None
        end_date = None
        report_date = None
        report_type = None
        source_id = None
        source = None
        operating_revenue = None
        interest_net_revenue = None
        interest_income = None
        interest_expense = None
        commission_net_income = None
        commission_income = None
        commission_expense = None
        investment_income = None
        fair_value_variable_income = None
        operating_profit = None
        total_profit = None
        income_tax_expense = None
        net_profit = None
        np_parent_company_owners = None
        minority_profit = None
        basic_eps = None
        diluted_eps = None

    # 金融类现金流量表
    class FINANCE_CASHFLOW_STATEMENT:
        id = None
        company_id = None
        company_name = None
        code = None
        a_code = None
        b_code = None
        h_code = None
        pub_date = None
        start_date = None
        end_date = None
        report_date = None
        report_type = None
        source_id = None
        source = None
        operate_cash_flow = None
        net_operate_cash_flow = None
        net_invest_cash_flow = None
        net_finance_cash_flow = None
        net_cash_increase = None

    # 金融类资产负债表（母公司）
    class FINANCE_BALANCE_SHEET_PARENT:
        id = None
        company_id = None
        company_name = None
        code = None
        a_code = None
        b_code = None
        h_code = None
        pub_date = None
        start_date = None
        end_date = None
        report_date = None
        report_type = None
        source_id = None
        source = None
        cash_equivalents = None
        total_assets = None
        total_liability = None
        total_equity = None
        accounts_receivable = None
        accounts_payable = None
        inventory = None
        fixed_assets = None
        intangible_assets = None
        longterm_equity_invest = None
        shortterm_loan = None
        longterm_loan = None
        total_debt = None

    # 母公司利润表
    class FINANCE_INCOME_STATEMENT_PARENT:
        id = None
        company_id = None
        company_name = None
        code = None
        a_code = None
        b_code = None
        h_code = None
        pub_date = None
        start_date = None
        end_date = None
        report_date = None
        report_type = None
        source_id = None
        source = None
        operating_revenue = None
        interest_net_revenue = None
        interest_income = None
        interest_expense = None
        commission_net_income = None
        commission_income = None
        commission_expense = None
        investment_income = None
        fair_value_variable_income = None
        operating_profit = None
        total_profit = None
        income_tax_expense = None
        net_profit = None
        np_parent_company_owners = None
        minority_profit = None
        basic_eps = None
        diluted_eps = None

    # 母公司现金流量表
    class FINANCE_CASHFLOW_STATEMENT_PARENT:
        id = None
        company_id = None
        company_name = None
        code = None
        a_code = None
        b_code = None
        h_code = None
        pub_date = None
        start_date = None
        end_date = None
        report_date = None
        report_type = None
        source_id = None
        source = None
        operate_cash_flow = None
        net_operate_cash_flow = None
        net_invest_cash_flow = None
        net_finance_cash_flow = None
        net_cash_increase = None

    # 合并资产负债表
    class FINANCE_BALANCE_SHEET:
        id = None
        company_id = None
        company_name = None
        code = None
        a_code = None
        b_code = None
        h_code = None
        pub_date = None
        start_date = None
        end_date = None
        report_date = None
        report_type = None
        source_id = None
        source = None
        cash_equivalents = None
        total_assets = None
        total_liability = None
        total_equity = None
        accounts_receivable = None
        accounts_payable = None
        inventory = None
        fixed_assets = None
        intangible_assets = None
        longterm_equity_invest = None
        shortterm_loan = None
        longterm_loan = None
        total_debt = None

    FINANCE_INCOME_STATEMENT_PARENT_SCHEMA = [
        "id",
        "company_id",
        "company_name",
        "code",
        "a_code",
        "b_code",
        "h_code",
        "pub_date",
        "start_date",
        "end_date",
        "report_date",
        "report_type",
        "source_id",
        "source",
        "operating_revenue",
        "interest_net_revenue",
        "interest_income",
        "interest_expense",
        "commission_net_income",
        "commission_income",
        "commission_expense",
        "investment_income",
        "fair_value_variable_income",
        "operating_profit",
        "total_profit",
        "income_tax_expense",
        "net_profit",
        "np_parent_company_owners",
        "minority_profit",
        "basic_eps",
        "diluted_eps",
    ]

    FINANCE_CASHFLOW_STATEMENT_PARENT_SCHEMA = [
        "id",
        "company_id",
        "company_name",
        "code",
        "a_code",
        "b_code",
        "h_code",
        "pub_date",
        "start_date",
        "end_date",
        "report_date",
        "report_type",
        "source_id",
        "source",
        "operate_cash_flow",
        "net_operate_cash_flow",
        "net_invest_cash_flow",
        "net_finance_cash_flow",
        "net_cash_increase",
    ]

    FINANCE_BALANCE_SHEET_SCHEMA = [
        "id",
        "company_id",
        "company_name",
        "code",
        "a_code",
        "b_code",
        "h_code",
        "pub_date",
        "start_date",
        "end_date",
        "report_date",
        "report_type",
        "source_id",
        "source",
        "cash_equivalents",
        "total_assets",
        "total_liability",
        "total_equity",
        "accounts_receivable",
        "accounts_payable",
        "inventory",
        "fixed_assets",
        "intangible_assets",
        "longterm_equity_invest",
        "shortterm_loan",
        "longterm_loan",
        "total_debt",
    ]

    FUT_MARGIN_SCHEMA = FUT_MARGIN_SCHEMA
    FUT_CHARGE_SCHEMA = FUT_CHARGE_SCHEMA
    FUT_WAREHOUSE_SCHEMA = FUT_WAREHOUSE_SCHEMA
    FUT_MEMBER_POSITION_SCHEMA = FUT_MEMBER_POSITION_SCHEMA

    STK_EXCHANGE_TRADE_INFO_SCHEMA = STK_EXCHANGE_TRADE_INFO_SCHEMA
    FUND_MF_DAILY_PROFIT_SCHEMA = FUND_MF_DAILY_PROFIT_SCHEMA
    STK_AUDIT_OPINION_SCHEMA = STK_AUDIT_OPINION_SCHEMA
    STK_REPORT_DISCLOSURE_SCHEMA = STK_REPORT_DISCLOSURE_SCHEMA
    STK_PERFORMANCE_LETTERS_SCHEMA = STK_PERFORMANCE_LETTERS_SCHEMA
    FINANCE_INCOME_STATEMENT_SCHEMA = FINANCE_INCOME_STATEMENT_SCHEMA
    FINANCE_CASHFLOW_STATEMENT_SCHEMA = FINANCE_CASHFLOW_STATEMENT_SCHEMA
    FINANCE_BALANCE_SHEET_PARENT_SCHEMA = FINANCE_BALANCE_SHEET_PARENT_SCHEMA

    def _get_income_statement_parent(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取母公司利润表数据"""
        from jk2bt.data.sources import get_adapter

        if not code:
            return pd.DataFrame(columns=self.FINANCE_INCOME_STATEMENT_PARENT_SCHEMA)

        code = code.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

        try:
            df = get_adapter().get_financial_report(symbol=code, report_type="利润表")

            if df is None or df.empty:
                return pd.DataFrame(columns=self.FINANCE_INCOME_STATEMENT_PARENT_SCHEMA)

            column_mapping = {
                "报告日": "end_date",
                "公告日期": "pub_date",
                "营业收入": "operating_revenue",
                "利息收入": "interest_income",
                "利息支出": "interest_expense",
                "投资收益": "investment_income",
                "公允价值变动收益": "fair_value_variable_income",
                "营业利润": "operating_profit",
                "利润总额": "total_profit",
                "所得税费用": "income_tax_expense",
                "净利润": "net_profit",
                "归属于母公司所有者的净利润": "np_parent_company_owners",
                "少数股东损益": "minority_profit",
                "基本每股收益": "basic_eps",
                "稀释每股收益": "diluted_eps",
            }

            df = df.rename(columns=column_mapping)
            df["code"] = code
            df["a_code"] = code

            if "end_date" in df.columns:
                df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")
                if start_date:
                    df = df[df["end_date"] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df["end_date"] <= pd.to_datetime(end_date)]

            available_cols = [
                c
                for c in self.FINANCE_INCOME_STATEMENT_PARENT_SCHEMA
                if c in df.columns
            ]
            return df[available_cols]

        except Exception as e:
            warnings.warn(f"获取母公司利润表失败 {code}: {e}")
            return pd.DataFrame(columns=self.FINANCE_INCOME_STATEMENT_PARENT_SCHEMA)

    def _get_cashflow_statement_parent(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取母公司现金流量表数据"""
        from jk2bt.data.sources import get_adapter

        if not code:
            return pd.DataFrame(columns=self.FINANCE_CASHFLOW_STATEMENT_PARENT_SCHEMA)

        code = code.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

        try:
            df = get_adapter().get_financial_report(
                symbol=code, report_type="现金流量表"
            )

            if df is None or df.empty:
                return pd.DataFrame(
                    columns=self.FINANCE_CASHFLOW_STATEMENT_PARENT_SCHEMA
                )

            column_mapping = {
                "报告日": "end_date",
                "公告日期": "pub_date",
                "经营活动产生的现金流量净额": "net_operate_cash_flow",
                "投资活动产生的现金流量净额": "net_invest_cash_flow",
                "筹资活动产生的现金流量净额": "net_finance_cash_flow",
                "现金及现金等价物净增加额": "net_cash_increase",
            }

            df = df.rename(columns=column_mapping)
            df["code"] = code
            df["a_code"] = code

            if "end_date" in df.columns:
                df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")
                if start_date:
                    df = df[df["end_date"] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df["end_date"] <= pd.to_datetime(end_date)]

            available_cols = [
                c
                for c in self.FINANCE_CASHFLOW_STATEMENT_PARENT_SCHEMA
                if c in df.columns
            ]
            return df[available_cols]

        except Exception as e:
            warnings.warn(f"获取母公司现金流量表失败 {code}: {e}")
            return pd.DataFrame(columns=self.FINANCE_CASHFLOW_STATEMENT_PARENT_SCHEMA)

    def _get_balance_sheet_parent(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取母公司资产负债表数据"""
        from jk2bt.data.sources import get_adapter

        if not code:
            return pd.DataFrame(columns=self.FINANCE_BALANCE_SHEET_SCHEMA)

        code = code.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

        try:
            df = get_adapter().get_financial_report(
                symbol=code, report_type="资产负债表"
            )

            if df is None or df.empty:
                return pd.DataFrame(columns=self.FINANCE_BALANCE_SHEET_SCHEMA)

            column_mapping = {
                "报告日": "end_date",
                "公告日期": "pub_date",
                "资产总计": "total_assets",
                "负债合计": "total_liability",
                "所有者权益(或股东权益)合计": "total_equity",
                "应收账款": "accounts_receivable",
                "应付账款": "accounts_payable",
                "存货": "inventory",
                "货币资金": "cash_equivalents",
            }

            df = df.rename(columns=column_mapping)
            df["code"] = code
            df["a_code"] = code

            if "end_date" in df.columns:
                df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")
                if start_date:
                    df = df[df["end_date"] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df["end_date"] <= pd.to_datetime(end_date)]

            available_cols = [
                c for c in self.FINANCE_BALANCE_SHEET_SCHEMA if c in df.columns
            ]
            return df[available_cols]

        except Exception as e:
            warnings.warn(f"获取母公司资产负债表失败 {code}: {e}")
            return pd.DataFrame(columns=self.FINANCE_BALANCE_SHEET_SCHEMA)

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
        if hasattr(query_obj, "__name__"):
            # 类对象
            table_name = query_obj.__name__
        elif hasattr(query_obj, "__class__"):
            # 实例对象
            table_name = query_obj.__class__.__name__

        # 如果是过滤条件对象
        if hasattr(query_obj, "left"):
            if hasattr(query_obj.left, "__name__"):
                table_name = query_obj.left.__name__
            elif hasattr(query_obj.left, "__class__"):
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

        elif table_name == "FUND_DIVIDEND":
            if code:
                return get_fund_dividend(code, **kwargs)
            return pd.DataFrame(columns=FUND_DIVIDEND_SCHEMA)

        elif table_name == "FUND_PERFORMANCE":
            if code:
                return get_fund_performance(code, **kwargs)
            return pd.DataFrame(columns=FUND_PERFORMANCE_SCHEMA)

        elif table_name == "FUND_FIN_INDICATOR":
            if code:
                return get_fund_fin_indicator(code, **kwargs)
            return pd.DataFrame(columns=FUND_FIN_INDICATOR_SCHEMA)

        elif table_name == "FUND_INVEST_TARGET":
            return get_fund_invest_target(fund_code=code, **kwargs)

        elif table_name == "FINANCE_INCOME_STATEMENT_PARENT":
            return self._get_income_statement_parent(code, **kwargs)

        elif table_name == "FINANCE_CASHFLOW_STATEMENT_PARENT":
            return self._get_cashflow_statement_parent(code, **kwargs)

        elif table_name == "FINANCE_BALANCE_SHEET":
            return self._get_balance_sheet_parent(code, **kwargs)

        elif table_name == "FUT_MARGIN":
            return get_futures_margin(code, **kwargs)

        elif table_name == "FUT_CHARGE":
            return get_futures_charge(code, **kwargs)

        elif table_name == "FUT_WAREHOUSE":
            return get_futures_warehouse(code, **kwargs)

        elif table_name == "FUT_MEMBER_POSITION":
            return get_futures_member_position(symbol=code, **kwargs)

        elif table_name == "OPT_DAILY_PREOPEN":
            return get_option_preopen(**kwargs)

        elif table_name == "STK_EXCHANGE_TRADE_INFO":
            return get_exchange_trade_info(**kwargs)

        elif table_name == "FUND_MF_DAILY_PROFIT":
            if code:
                return get_fund_mf_daily_profit(fund_code=code, **kwargs)
            return get_fund_mf_daily_profit(**kwargs)

        elif table_name == "STK_AUDIT_OPINION":
            return get_audit_opinion(code=code, **kwargs)

        elif table_name == "STK_REPORT_DISCLOSURE":
            return get_report_disclosure(code=code, **kwargs)

        elif table_name == "STK_PERFORMANCE_LETTERS":
            return get_performance_letters(code=code, **kwargs)

        elif table_name == "FINANCE_INCOME_STATEMENT":
            return get_finance_income_statement(code=code, **kwargs)

        elif table_name == "FINANCE_CASHFLOW_STATEMENT":
            return get_finance_cashflow_statement(code=code, **kwargs)

        elif table_name == "FINANCE_BALANCE_SHEET_PARENT":
            return get_finance_balance_sheet_parent(code=code, **kwargs)

        elif table_name == "FINANCE_INCOME_STATEMENT_PARENT":
            return self._get_income_statement_parent(code, **kwargs)

        elif table_name == "FINANCE_CASHFLOW_STATEMENT_PARENT":
            return self._get_cashflow_statement_parent(code, **kwargs)

        elif table_name == "FINANCE_BALANCE_SHEET":
            return self._get_balance_sheet_parent(code, **kwargs)

        else:
            raise ValueError(f"不支持的表: {table_name}")


# 创建全局实例
finance_tables = FinanceTables()

# 模块级别别名（方便直接导入使用）
STK_EXCHANGE_TRADE_INFO = FinanceTables.STK_EXCHANGE_TRADE_INFO
FUND_MF_DAILY_PROFIT = FinanceTables.FUND_MF_DAILY_PROFIT
STK_AUDIT_OPINION = FinanceTables.STK_AUDIT_OPINION
STK_REPORT_DISCLOSURE = FinanceTables.STK_REPORT_DISCLOSURE
STK_PERFORMANCE_LETTERS = FinanceTables.STK_PERFORMANCE_LETTERS
FINANCE_INCOME_STATEMENT = FinanceTables.FINANCE_INCOME_STATEMENT
FINANCE_CASHFLOW_STATEMENT = FinanceTables.FINANCE_CASHFLOW_STATEMENT
FINANCE_BALANCE_SHEET_PARENT = FinanceTables.FINANCE_BALANCE_SHEET_PARENT
FINANCE_INCOME_STATEMENT_PARENT = FinanceTables.FINANCE_INCOME_STATEMENT_PARENT
FINANCE_CASHFLOW_STATEMENT_PARENT = FinanceTables.FINANCE_CASHFLOW_STATEMENT_PARENT
FINANCE_BALANCE_SHEET = FinanceTables.FINANCE_BALANCE_SHEET
OPT_DAILY_PREOPEN = FinanceTables.OPT_DAILY_PREOPEN
FUND_FIN_INDICATOR = FinanceTables.FUND_FIN_INDICATOR
FUND_INVEST_TARGET = FinanceTables.FUND_INVEST_TARGET

__all__ = [
    "STK_BALANCE_SHEET_SCHEMA",
    "STK_INCOME_STATEMENT_SCHEMA",
    "STK_CASHFLOW_STATEMENT_SCHEMA",
    "FUND_NET_VALUE_SCHEMA",
    "FUND_PORTFOLIO_SCHEMA",
    "FUND_DIVIDEND_SCHEMA",
    "FUND_PERFORMANCE_SCHEMA",
    "FUND_FIN_INDICATOR_SCHEMA",
    "FUND_INVEST_TARGET_SCHEMA",
    "FUT_MARGIN_SCHEMA",
    "FUT_CHARGE_SCHEMA",
    "FUT_WAREHOUSE_SCHEMA",
    "FUT_MEMBER_POSITION_SCHEMA",
    "OPT_DAILY_PREOPEN_SCHEMA",
    "STK_EXCHANGE_TRADE_INFO_SCHEMA",
    "FUND_MF_DAILY_PROFIT_SCHEMA",
    "STK_AUDIT_OPINION_SCHEMA",
    "STK_REPORT_DISCLOSURE_SCHEMA",
    "STK_PERFORMANCE_LETTERS_SCHEMA",
    "FINANCE_INCOME_STATEMENT_SCHEMA",
    "FINANCE_CASHFLOW_STATEMENT_SCHEMA",
    "FINANCE_BALANCE_SHEET_PARENT_SCHEMA",
    "get_balance_sheet",
    "get_income_statement",
    "get_cashflow_statement",
    "get_fund_net_value",
    "get_fund_portfolio",
    "get_fund_dividend",
    "get_fund_performance",
    "get_fund_fin_indicator",
    "get_fund_invest_target",
    "get_futures_margin",
    "get_futures_charge",
    "get_futures_warehouse",
    "get_futures_member_position",
    "get_option_preopen",
    "get_exchange_trade_info",
    "get_fund_mf_daily_profit",
    "get_audit_opinion",
    "get_report_disclosure",
    "get_performance_letters",
    "get_finance_income_statement",
    "get_finance_cashflow_statement",
    "get_finance_balance_sheet_parent",
    "get_finance_income_statement_parent",
    "get_finance_cashflow_statement_parent",
    "get_finance_balance_sheet",
    "FinanceTables",
    "finance_tables",
]
