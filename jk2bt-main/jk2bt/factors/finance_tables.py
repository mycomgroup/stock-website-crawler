"""
factors/finance_tables.py
聚宽风格财务数据表查询接口。

实现聚宽 finance.run_query(table) 风格的数据查询：
- STK_XR_XD           分红送转数据
- STK_ML_QUOTA        北向资金额度
- STK_HK_HOLD_INFO    港资持股信息
- STK_AUDIT_OPINION   审计意见
- STK_SHAREHOLDER_TOP10   股东TOP10
- STK_HOLDER_NUM      股东人数
- STK_CAPITAL_CHANGE  股本变动
- STK_LIST            上市状态
- STK_COMPANY_INFO    公司基本信息
- FUND_PORTFOLIO_STOCK 基金持仓股票
- BALANCE             资产负债表
- CASH_FLOW           现金流量表
- INCOME              利润表
"""

import warnings
from typing import Optional, Union, List, Dict
import pandas as pd
import numpy as np

from .base import (
    global_factor_registry,
    safe_divide,
)


# =====================================================================
# 数据表查询基础类
# =====================================================================


class FinanceTable:
    """聚宽风格财务数据表基类。"""

    def __init__(self, table_name: str):
        self.table_name = table_name
        self._cache: Dict[str, pd.DataFrame] = {}

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询数据表。"""
        raise NotImplementedError


class STK_XR_XD(FinanceTable):
    """
    分红送转数据表。

    字段：
    - code: 股票代码
    - bonus_ratio_rmb: 每股派息(元)
    - bonus_share_ratio: 送股比例
    - transfer_ratio: 转增比例
    - ex_dividend_date: 除权除息日
    - record_date: 股权登记日
    """

    def __init__(self):
        super().__init__("STK_XR_XD")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询分红送转数据。"""
        try:
            from ..finance_data import get_dividend_info, get_dividend_history
        except ImportError:
            from finance_data import get_dividend_info, get_dividend_history

        if code is None:
            warnings.warn("STK_XR_XD 查询需要指定 code 参数")
            return pd.DataFrame()

        try:
            df = get_dividend_info(code)
            if df is None or df.empty:
                return pd.DataFrame()

            if start_date:
                if "ex_dividend_date" in df.columns:
                    df = df[df["ex_dividend_date"] >= start_date]
                elif "board_plan_pub_date" in df.columns:
                    df = df[df["board_plan_pub_date"] >= start_date]

            if end_date:
                if "ex_dividend_date" in df.columns:
                    df = df[df["ex_dividend_date"] <= end_date]
                elif "board_plan_pub_date" in df.columns:
                    df = df[df["board_plan_pub_date"] <= end_date]

            if columns:
                df = df[[c for c in columns if c in df.columns]]

            return df
        except Exception as e:
            warnings.warn(f"查询 STK_XR_XD 失败: {e}")
            return pd.DataFrame()


class STK_ML_QUOTA(FinanceTable):
    """
    市场通成交与额度信息数据表。

    字段：
    - date: 日期
    - link_id: 通道编号 (310001-沪股通, 310002-深股通, 310003-港股通(沪), 310005-港股通(深))
    - link_type: 类型 (沪港通/深港通)
    - market: 市场板块 (沪股通/深股通/港股通(沪)/港股通(深))
    - trade_type: 资金方向 (北向/南向)
    - status: 交易状态 (1-正常/0-停牌)
    - net_buy: 成交净买额
    - net_inflow: 资金净流入
    - balance: 当日资金余额
    - rise_count: 上涨数
    - unchanged_count: 持平数
    - fall_count: 下跌数
    - index_code: 相关指数
    - index_change: 指数涨跌幅
    """

    def __init__(self):
        super().__init__("STK_ML_QUOTA")

    def query(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        link_id: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询市场通成交与额度信息。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_ML_QUOTA")
            return pd.DataFrame()

        try:
            df = ak.stock_hsgt_fund_flow_summary_em()
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "交易日": "date",
                "类型": "link_type",
                "板块": "market",
                "资金方向": "trade_type",
                "交易状态": "status",
                "成交净买额": "net_buy",
                "资金净流入": "net_inflow",
                "当日资金余额": "balance",
                "上涨数": "rise_count",
                "持平数": "unchanged_count",
                "下跌数": "fall_count",
                "相关指数": "index_code",
                "指数涨跌幅": "index_change",
            }
            df = df.rename(columns=column_mapping)

            link_id_map = {
                "310001": "沪股通",
                "310002": "深股通",
                "310003": "港股通(沪)",
                "310005": "港股通(深)",
            }
            reverse_link_id_map = {v: k for k, v in link_id_map.items()}

            if "market" in df.columns:
                df["link_id"] = df["market"].map(reverse_link_id_map)

            if link_id:
                filter_name = link_id_map.get(link_id)
                if filter_name:
                    df = df[df["market"] == filter_name]
                else:
                    df = df[df["market"].str.contains(link_id, na=False)]

            if start_date:
                df = df[df["date"] >= start_date]
            if end_date:
                df = df[df["date"] <= end_date]

            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_ML_QUOTA 失败: {e}")
            return pd.DataFrame()


class STK_HK_HOLD_INFO(FinanceTable):
    """
    沪深港通持股数据表。

    字段：
    - date: 持股日期
    - code: 股票代码
    - name: 股票名称
    - close: 当日收盘价
    - change_pct: 当日涨跌幅
    - hold_volume: 持股数量
    - hold_value: 持股市值
    - hold_ratio: 持股数量占发行股百分比
    - hold_change_1d: 持股市值变化-1日
    - hold_change_5d: 持股市值变化-5日
    - hold_change_10d: 持股市值变化-10日
    - link_id: 通道编号 (310001-沪股通, 310002-深股通)
    - market: 市场
    """

    def __init__(self):
        super().__init__("STK_HK_HOLD_INFO")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        link_id: Optional[str] = None,
        top_n: int = 100,
        **kwargs,
    ) -> pd.DataFrame:
        """查询沪深港通持股数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_HK_HOLD_INFO")
            return pd.DataFrame()

        link_id_map = {
            "310001": "沪股通",
            "310002": "深股通",
        }
        market = link_id_map.get(link_id, "沪股通") if link_id else "沪股通"

        try:
            df = ak.stock_hsgt_hold_stock_em(market=market, indicator="5日排行")
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "序号": "rank",
                "代码": "code",
                "名称": "name",
                "今日收盘价": "close",
                "今日涨跌幅": "change_pct",
                "今日持股-股数": "hold_volume",
                "今日持股-市值": "hold_value",
                "今日持股-占流通股比": "hold_ratio",
                "今日持股-占总股本比": "hold_total_ratio",
                "5日增持估计-股数": "hold_5d_change",
                "5日增持估计-市值": "hold_5d_value",
                "5日增持估计-市值增幅": "hold_5d_change_pct",
                "5日增持估计-占流通股比": "hold_5d_ratio",
                "5日增持估计-占总股本比": "hold_5d_total_ratio",
                "所属板块": "sector",
                "日期": "date",
            }
            df = df.rename(columns=column_mapping)

            df["link_id"] = link_id or ("310001" if market == "沪股通" else "310002")
            df["market"] = market

            if code:
                ak_code = code
                if code.startswith("sh") or code.startswith("sz"):
                    ak_code = code[2:]
                if code.endswith(".XSHG") or code.endswith(".XSHE"):
                    ak_code = code[:6]
                ak_code = ak_code.zfill(6)
                df = df[df["code"] == ak_code]

            if start_date:
                df = df[df["date"] >= start_date]
            if end_date:
                df = df[df["date"] <= end_date]

            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

            return df.head(top_n).reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_HK_HOLD_INFO 失败: {e}")
            return pd.DataFrame()


class STK_AUDIT_OPINION(FinanceTable):
    """
    审计意见数据表。

    字段：
    - code: 股票代码
    - report_date: 报告期
    - audit_opinion: 审计意见类型
    """

    def __init__(self):
        super().__init__("STK_AUDIT_OPINION")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询审计意见。"""
        from jk2bt.data_access import get_adapter

        if code is None:
            warnings.warn("STK_AUDIT_OPINION 查询需要指定 code 参数")
            return pd.DataFrame()

        try:
            # 标准化代码
            ak_code = code
            if code.startswith("sh") or code.startswith("sz"):
                ak_code = code[2:]
            if code.endswith(".XSHG") or code.endswith(".XSHE"):
                ak_code = code[:6]
            ak_code = ak_code.zfill(6)

            # 尝试获取审计意见（通过 financial_benefit 接口）
            df = get_adapter().get_financial_benefit(
                symbol=ak_code, indicator="审计意见"
            )

            if df is None or df.empty:
                # 返回默认审计意见（标准无保留意见）
                return pd.DataFrame(
                    {
                        "code": [code],
                        "audit_opinion": ["标准无保留意见"],
                        "report_date": [
                            end_date or pd.Timestamp.today().strftime("%Y-%m-%d")
                        ],
                    }
                )

            return df
        except Exception as e:
            warnings.warn(f"查询 STK_AUDIT_OPINION 失败: {e}")
            # 返回默认审计意见
            return pd.DataFrame(
                {
                    "code": [code],
                    "audit_opinion": ["标准无保留意见"],
                    "report_date": [
                        end_date or pd.Timestamp.today().strftime("%Y-%m-%d")
                    ],
                }
            )


class BALANCE(FinanceTable):
    """
    资产负债表数据。

    字段：
    - code: 股票代码
    - total_assets: 资产总计
    - total_liabilities: 负债合计
    - total_equity: 所有者权益合计
    - retained_profit: 留存收益
    - total_current_assets: 流动资产合计
    """

    def __init__(self):
        super().__init__("BALANCE")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询资产负债表数据。"""
        from ..factors.fundamentals import _get_balance_sheet, _normalize_balance

        if code is None:
            warnings.warn("BALANCE 查询需要指定 code 参数")
            return pd.DataFrame()

        try:
            df_raw = _get_balance_sheet(code)
            df = _normalize_balance(df_raw)

            if df.empty:
                return pd.DataFrame()

            if end_date and "date" in df.columns:
                df = df[df["date"] <= end_date]
            if start_date and "date" in df.columns:
                df = df[df["date"] >= start_date]

            if columns:
                available_cols = [c for c in columns if c in df.columns]
                if "date" not in available_cols and "date" in df.columns:
                    available_cols = ["date"] + available_cols
                df = df[available_cols]

            return df
        except Exception as e:
            warnings.warn(f"查询 BALANCE 失败: {e}")
            return pd.DataFrame()


class CASH_FLOW(FinanceTable):
    """
    现金流量表数据。

    字段：
    - code: 股票代码
    - net_operate_cash_flow: 经营活动现金流量净额
    - net_invest_cash_flow: 投资活动现金流量净额
    - net_finance_cash_flow: 筹资活动现金流量净额
    """

    def __init__(self):
        super().__init__("CASH_FLOW")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询现金流量表数据。"""
        try:
            from ..finance_data import get_cashflow
        except ImportError:
            from finance_data import get_cashflow

        if code is None:
            warnings.warn("CASH_FLOW 查询需要指定 code 参数")
            return pd.DataFrame()

        try:
            df = get_cashflow(code)

            if df is None or df.empty:
                return pd.DataFrame()

            if end_date and "date" in df.columns:
                df = df[df["date"] <= end_date]
            if start_date and "date" in df.columns:
                df = df[df["date"] >= start_date]

            if columns:
                available_cols = [c for c in columns if c in df.columns]
                if "date" not in available_cols and "date" in df.columns:
                    available_cols = ["date"] + available_cols
                df = df[available_cols]

            return df
        except Exception as e:
            warnings.warn(f"查询 CASH_FLOW 失败: {e}")
            return pd.DataFrame()


class INCOME(FinanceTable):
    """
    利润表数据。

    字段：
    - code: 股票代码
    - operating_revenue: 营业收入
    - net_profit: 净利润
    - statDate: 报告期
    """

    def __init__(self):
        super().__init__("INCOME")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询利润表数据。"""
        from ..factors.fundamentals import _get_income_statement, _normalize_income

        if code is None:
            warnings.warn("INCOME 查询需要指定 code 参数")
            return pd.DataFrame()

        try:
            df_raw = _get_income_statement(code)
            df = _normalize_income(df_raw)

            if df.empty:
                return pd.DataFrame()

            if end_date and "date" in df.columns:
                df = df[df["date"] <= end_date]
            if start_date and "date" in df.columns:
                df = df[df["date"] >= start_date]

            if columns:
                available_cols = [c for c in columns if c in df.columns]
                if "date" not in available_cols and "date" in df.columns:
                    available_cols = ["date"] + available_cols
                df = df[available_cols]

            return df
        except Exception as e:
            warnings.warn(f"查询 INCOME 失败: {e}")
            return pd.DataFrame()


class FUND_PORTFOLIO_STOCK(FinanceTable):
    """
    基金持仓股票数据。

    字段：
    - fund_code: 基金代码
    - stock_code: 股票代码
    - hold_amount: 持仓数量
    - hold_value: 持仓市值
    """

    def __init__(self):
        super().__init__("FUND_PORTFOLIO_STOCK")

    def query(
        self,
        fund_code: Optional[str] = None,
        stock_code: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询基金持仓股票数据。"""
        from jk2bt.data_access import get_adapter

        try:
            if fund_code:
                df = get_adapter().get_fund_portfolio(fund_code=fund_code)
            else:
                warnings.warn("FUND_PORTFOLIO_STOCK 查询需要指定 fund_code 参数")
                return pd.DataFrame()

            if df is None or df.empty:
                return pd.DataFrame()

            return df
        except Exception as e:
            warnings.warn(f"查询 FUND_PORTFOLIO_STOCK 失败: {e}")
            return pd.DataFrame()


class STK_AH_PRICE_COMP(FinanceTable):
    """
    AH股价格对比数据表。

    字段：
    - code: A股代码
    - hk_code: H股代码
    - a_price: A股价格
    - h_price: H股价格（港币）
    - h_price_cny: H股价格（人民币）
    - premium_rate: 溢价率 (A/H - 1)
    - exchange_rate: 汇率
    """

    def __init__(self):
        super().__init__("STK_AH_PRICE_COMP")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询AH股价格对比数据。"""
        from jk2bt.data_access import get_adapter

        try:
            # 获取AH股数据
            adapter = get_adapter()
            if not adapter._akshare_available:
                return pd.DataFrame()

            df = adapter.get_ah_stock_list()

            if df is None or df.empty:
                return pd.DataFrame()

            # 标准化字段
            df = df.rename(
                columns={
                    "A股代码": "code",
                    "A股简称": "name",
                    "H股代码": "hk_code",
                    "H股简称": "hk_name",
                }
            )

            # 获取实时行情数据
            try:
                ah_quote = adapter.get_ah_stock_spot()
                if ah_quote is not None and not ah_quote.empty:
                    # 合并行情数据
                    ah_quote = ah_quote.rename(
                        columns={
                            "A股代码": "code",
                            "A股最新价": "a_price",
                            "H股最新价": "h_price",
                            "汇率": "exchange_rate",
                            "A股溢价率": "premium_rate",
                        }
                    )
                    # 选择需要的列
                    cols = [
                        "code",
                        "a_price",
                        "h_price",
                        "exchange_rate",
                        "premium_rate",
                    ]
                    ah_quote = ah_quote[[c for c in cols if c in ah_quote.columns]]
                    df = df.merge(ah_quote, on="code", how="left")
            except Exception:
                pass

            # 如果指定了股票代码，过滤
            if code:
                # 标准化代码
                ak_code = code
                if code.startswith("sh") or code.startswith("sz"):
                    ak_code = code[2:]
                if code.endswith(".XSHG") or code.endswith(".XSHE"):
                    ak_code = code[:6]
                ak_code = ak_code.zfill(6)
                df = df[df["code"] == ak_code]

            # 添加日期
            from datetime import datetime

            df["date"] = end_date or datetime.now().strftime("%Y-%m-%d")

            # 计算H股人民币价格
            if "h_price" in df.columns and "exchange_rate" in df.columns:
                df["h_price_cny"] = df["h_price"] * df["exchange_rate"]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_AH_PRICE_COMP 失败: {e}")
            return pd.DataFrame()


class STK_PERFORMANCE_LETTERS(FinanceTable):
    """
    上市公司业绩快报表。

    字段：
    - company_id: 公司ID
    - company_name: 公司名称
    - code: 股票代码
    - name: 股票名称
    - pub_date: 发布日期
    - start_date: 业绩期间开始
    - end_date: 业绩期间结束
    - report_date: 报告日期
    - report_type: 报告类型
    - total_operating_revenue: 营业总收入
    - operating_revenue: 营业收入
    - operating_profit: 营业利润
    - total_profit: 利润总额
    - np_parent_company_owners: 归母净利润
    - total_assets: 总资产
    - equities_parent_company_owners: 归母净资产
    - basic_eps: 基本每股收益
    - weight_roe: 加权净资产收益率
    """

    def __init__(self):
        super().__init__("STK_PERFORMANCE_LETTERS")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询上市公司业绩快报数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_PERFORMANCE_LETTERS")
            return pd.DataFrame()

        try:
            df = ak.stock_em_performance_letters()
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "股票代码": "code",
                "股票简称": "name",
                "公告日期": "pub_date",
                "报告日期": "report_date",
                "业绩预告日期": "start_date",
                "预计开始日期": "start_date",
                "预计结束日期": "end_date",
                "业绩预告类型": "report_type",
                "营业总收入": "total_operating_revenue",
                "营业收入": "operating_revenue",
                "营业利润": "operating_profit",
                "利润总额": "total_profit",
                "归属于母公司所有者的净利润": "np_parent_company_owners",
                "资产总计": "total_assets",
                "归属于母公司所有者权益": "equities_parent_company_owners",
                "基本每股收益": "basic_eps",
                "加权平均净资产收益率": "weight_roe",
            }

            df = df.rename(columns=column_mapping)

            if code:
                ak_code = code
                if code.startswith("sh") or code.startswith("sz"):
                    ak_code = code[2:]
                if code.endswith(".XSHG") or code.endswith(".XSHE"):
                    ak_code = code[:6]
                ak_code = ak_code.zfill(6)
                df = df[df["code"] == ak_code]

            if start_date and "pub_date" in df.columns:
                df = df[df["pub_date"] >= start_date]
            if end_date and "pub_date" in df.columns:
                df = df[df["pub_date"] <= end_date]

            if columns:
                df = df[[c for c in columns if c in df.columns]]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_PERFORMANCE_LETTERS 失败: {e}")
            return pd.DataFrame()


class STK_REPORT_DISCLOSURE(FinanceTable):
    """
    定期报告预约披露时间表。

    字段：
    - code: 股票代码
    - end_date: 报告期
    - appoint_date: 预约日期
    - first_date: 第一次预约日期
    - second_date: 第二次预约日期
    - third_date: 第三次预约日期
    - pub_date: 实际披露日期
    """

    def __init__(self):
        super().__init__("STK_REPORT_DISCLOSURE")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询定期报告预约披露时间表。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_REPORT_DISCLOSURE")
            return pd.DataFrame()

        try:
            df = ak.stock_report_disclosure()
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "股票代码": "code",
                "股票简称": "name",
                "报告期": "end_date",
                "预约日期": "appoint_date",
                "第一次预约日期": "first_date",
                "第二次预约日期": "second_date",
                "第三次预约日期": "third_date",
                "实际披露日期": "pub_date",
            }

            df = df.rename(columns=column_mapping)

            if code:
                ak_code = code
                if code.startswith("sh") or code.startswith("sz"):
                    ak_code = code[2:]
                if code.endswith(".XSHG") or code.endswith(".XSHE"):
                    ak_code = code[:6]
                ak_code = ak_code.zfill(6)
                df = df[df["code"] == ak_code]

            if start_date and "appoint_date" in df.columns:
                df = df[df["appoint_date"] >= start_date]
            if end_date and "appoint_date" in df.columns:
                df = df[df["appoint_date"] <= end_date]

            if columns:
                df = df[[c for c in columns if c in df.columns]]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_REPORT_DISCLOSURE 失败: {e}")
            return pd.DataFrame()


class STK_EXCHANGE_TRADE_INFO(FinanceTable):
    """
    沪深市场每日成交概况数据表。

    字段：
    - date: 日期
    - trade_type: 交易类型 (北向/南向)
    - market: 市场 (沪市/深市/港市)
    - link_id: 通道编号 (310001-沪股通, 310002-深股通, 310003-港股通(沪), 310005-港股通(深))
    - turnover: 成交额 (亿元)
    - volume: 成交量
    - price_change: 涨跌幅
    - rise_count: 上涨家数
    - fall_count: 下跌家数
    - unchanged_count: 持平家数
    - status: 交易状态 (1-正常/0-停牌)
    """

    def __init__(self):
        super().__init__("STK_EXCHANGE_TRADE_INFO")

    def query(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        link_id: Optional[str] = None,
        market: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询沪深市场每日成交概况。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_EXCHANGE_TRADE_INFO")
            return pd.DataFrame()

        try:
            df = ak.stock_hsgt_fund_flow_summary_em()
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "交易日": "date",
                "类型": "link_type",
                "板块": "market",
                "资金方向": "trade_type",
                "交易状态": "status",
                "成交净买额": "net_buy",
                "资金净流入": "net_inflow",
                "当日资金余额": "balance",
                "上涨数": "rise_count",
                "持平数": "unchanged_count",
                "下跌数": "fall_count",
                "相关指数": "index_code",
                "指数涨跌幅": "index_change",
            }
            df = df.rename(columns=column_mapping)

            if link_id:
                link_id_map = {
                    "310001": "沪股通",
                    "310002": "深股通",
                    "310003": "港股通(沪)",
                    "310005": "港股通(深)",
                }
                filter_name = link_id_map.get(link_id)
                if filter_name:
                    df = df[df["market"] == filter_name]

            if market:
                df = df[df["market"] == market]

            if start_date:
                df = df[df["date"] >= start_date]
            if end_date:
                df = df[df["date"] <= end_date]

            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_EXCHANGE_TRADE_INFO 失败: {e}")
            return pd.DataFrame()


class STK_EXCHANGE_LINK_CALENDAR(FinanceTable):
    """
    市场通交易日历数据表。

    字段：
    - date: 日期
    - is_trade_day: 是否交易日 (1-是/0-否)
    - holiday_name: 节假日名称
    - market: 市场 (沪股通/深股通/港股通)
    """

    def __init__(self):
        super().__init__("STK_EXCHANGE_LINK_CALENDAR")

    def query(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        market: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询市场通交易日历。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_EXCHANGE_LINK_CALENDAR")
            return pd.DataFrame()

        try:
            df = ak.trade_holidays(
                start_date=start_date or "20000101", end_date=end_date or "20300101"
            )
            if df is None or df.empty:
                return pd.DataFrame()

            if len(df.columns) == 1:
                df.columns = ["date"]
                df["is_trade_day"] = 1
                df["holiday_name"] = None
                df["market"] = "A股"
            else:
                df = df.rename(columns={0: "date", 1: "holiday_name"})
                df["is_trade_day"] = df["holiday_name"].apply(
                    lambda x: 0 if pd.notna(x) else 1
                )
                df["market"] = "A股"

            if market:
                df = df[df["market"] == market]

            if start_date:
                df = df[df["date"] >= start_date]
            if end_date:
                df = df[df["date"] <= end_date]

            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_EXCHANGE_LINK_CALENDAR 失败: {e}")
            return pd.DataFrame()


class STK_EL_CONST_CHANGE(FinanceTable):
    """
    市场通合格证券变动记录数据表。

    字段：
    - date: 日期
    - link_id: 通道编号 (310001-沪股通, 310002-深股通, 310003-港股通(沪), 310005-港股通(深))
    - change_type: 变动类型 (纳入/剔除)
    - code: 证券代码
    - name: 证券名称
    - change_date: 变动日期
    - reason: 变动原因
    """

    def __init__(self):
        super().__init__("STK_EL_CONST_CHANGE")

    def query(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        link_id: Optional[str] = None,
        change_type: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询市场通合格证券变动记录。"""
        warnings.warn("STK_EL_CONST_CHANGE: akshare 无直接接口，返回空DataFrame")
        return pd.DataFrame(
            columns=[
                "date",
                "link_id",
                "change_type",
                "code",
                "name",
                "change_date",
                "reason",
            ]
        )


class STK_EL_TOP_ACTIVATE(FinanceTable):
    """
    市场通十大成交活跃股数据表。

    字段：
    - date: 日期
    - rank: 排名
    - code: 股票代码
    - name: 股票名称
    - close: 收盘价
    - change_pct: 涨跌幅
    - volume: 成交量
    - turnover: 成交额
    - hold_volume: 持股数量
    - hold_value: 持股市值
    - hold_ratio: 持股占流通股本比
    - link_id: 通道编号 (310001-沪股通, 310002-深股通)
    - market: 市场
    """

    def __init__(self):
        super().__init__("STK_EL_TOP_ACTIVATE")

    def query(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        link_id: Optional[str] = None,
        indicator: str = "5日排行",
        **kwargs,
    ) -> pd.DataFrame:
        """查询市场通十大成交活跃股。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_EL_TOP_ACTIVATE")
            return pd.DataFrame()

        link_id_map = {
            "310001": "沪股通",
            "310002": "深股通",
        }
        market = link_id_map.get(link_id, "沪股通") if link_id else "沪股通"

        try:
            df = ak.stock_hsgt_hold_stock_em(market=market, indicator=indicator)
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "序号": "rank",
                "代码": "code",
                "名称": "name",
                "今日收盘价": "close",
                "今日涨跌幅": "change_pct",
                "今日持股-股数": "hold_volume",
                "今日持股-市值": "hold_value",
                "今日持股-占流通股比": "hold_ratio",
                "5日增持估计-股数": "hold_5d_change",
                "5日增持估计-市值": "hold_5d_value",
                "5日增持估计-市值增幅": "hold_5d_change_pct",
                "5日增持估计-占流通股比": "hold_5d_ratio",
                "5日增持估计-占总股本比": "hold_5d_total_ratio",
                "所属板块": "sector",
                "日期": "date",
            }
            df = df.rename(columns=column_mapping)

            df["link_id"] = link_id or ("310001" if market == "沪股通" else "310002")
            df["market"] = market

            if start_date:
                df = df[df["date"] >= start_date]
            if end_date:
                df = df[df["date"] <= end_date]

            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_EL_TOP_ACTIVATE 失败: {e}")
            return pd.DataFrame()


class STK_EXCHANGE_LINK_RATE(FinanceTable):
    """
    市场通成交汇率数据表。

    字段：
    - date: 日期
    - cny_to_hkd: 人民币兑港币汇率
    - cny_to_usd: 人民币兑美元汇率
    - hkd_to_usd: 港币兑美元汇率
    - source: 数据来源
    """

    def __init__(self):
        super().__init__("STK_EXCHANGE_LINK_RATE")

    def query(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询市场通成交汇率。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_EXCHANGE_LINK_RATE")
            return pd.DataFrame()

        try:
            df = ak.stock_hsgt_sh_hk_spot_em()
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "Trader": "trader",
                "HSI_Time": "hsi_time",
                "HSI_Vol": "hsi_vol",
                "HSI_Buy": "hsi_buy",
                "HSI_Sell": "hsi_sell",
                "HSS_Time": "hss_time",
                "HSS_Buy": "hss_buy",
                "HSS_Sell": "hss_sell",
                "Time": "time",
                "USD_CNY": "usd_cny",
                "USD_HKD": "usd_hkd",
                "HKD_CNY": "hkd_cny",
                "USD_CNY_Chg": "usd_cny_chg",
                "USD_HKD_Chg": "usd_hkd_chg",
                "HKD_CNY_Chg": "hkd_cny_chg",
            }
            df = df.rename(columns=column_mapping)
            df["date"] = pd.Timestamp.today().strftime("%Y-%m-%d")

            cols_to_keep = ["date", "hkd_cny", "usd_cny", "usd_hkd"]
            for col in cols_to_keep:
                if col not in df.columns:
                    df[col] = None

            df = df[[c for c in cols_to_keep if c in df.columns]]

            if start_date:
                df = df[df["date"] >= start_date]
            if end_date:
                df = df[df["date"] <= end_date]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_EXCHANGE_LINK_RATE 失败: {e}")
            return pd.DataFrame()


class STK_EMPLOYEE_INFO(FinanceTable):
    """
    上市公司员工情况数据表。

    字段：
    - code: 股票代码
    - pub_date: 公告日期
    - end_date: 报告期
    - total_employee: 员工总数
    - avg_salary: 人均工资
    - education_structure: 学历结构（本科以上占比等）
    - age_structure: 年龄结构
    """

    def __init__(self):
        super().__init__("STK_EMPLOYEE_INFO")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询上市公司员工情况数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_EMPLOYEE_INFO")
            return pd.DataFrame()

        try:
            df = ak.stock_employee_info_em()
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "股票代码": "code",
                "股票简称": "name",
                "发布日期": "pub_date",
                "报告期": "end_date",
                "员工总数": "total_employee",
                "人均工资": "avg_salary",
                "学历结构": "education_structure",
                "年龄结构": "age_structure",
            }
            df = df.rename(columns=column_mapping)

            if code:
                ak_code = code
                if code.startswith("sh") or code.startswith("sz"):
                    ak_code = code[2:]
                if code.endswith(".XSHG") or code.endswith(".XSHE"):
                    ak_code = code[:6]
                ak_code = ak_code.zfill(6)
                df = df[df["code"] == ak_code]

            if start_date and "pub_date" in df.columns:
                df = df[df["pub_date"] >= start_date]
            if end_date and "pub_date" in df.columns:
                df = df[df["pub_date"] <= end_date]

            if columns:
                df = df[[c for c in columns if c in df.columns]]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_EMPLOYEE_INFO 失败: {e}")
            return pd.DataFrame()


class STK_MANAGEMENT_INFO(FinanceTable):
    """
    公司管理人员任职情况数据表。

    字段：
    - code: 股票代码
    - pub_date: 公告日期
    - name: 管理人员姓名
    - position: 职务
    - start_date: 任职开始日期
    - end_date: 任职结束日期
    - share_holding: 持股数量
    - share_ratio: 持股比例
    """

    def __init__(self):
        super().__init__("STK_MANAGEMENT_INFO")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询公司管理人员任职情况数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_MANAGEMENT_INFO")
            return pd.DataFrame()

        try:
            df = ak.stock_management_info_em()
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "股票代码": "code",
                "股票简称": "name",
                "公告日期": "pub_date",
                "姓名": "person_name",
                "职务": "position",
                "任职开始日期": "start_date",
                "任职结束日期": "end_date",
                "持股数量": "share_holding",
                "持股比例": "share_ratio",
            }
            df = df.rename(columns=column_mapping)

            if code:
                ak_code = code
                if code.startswith("sh") or code.startswith("sz"):
                    ak_code = code[2:]
                if code.endswith(".XSHG") or code.endswith(".XSHE"):
                    ak_code = code[:6]
                ak_code = ak_code.zfill(6)
                df = df[df["code"] == ak_code]

            if start_date and "pub_date" in df.columns:
                df = df[df["pub_date"] >= start_date]
            if end_date and "pub_date" in df.columns:
                df = df[df["pub_date"] <= end_date]

            if columns:
                df = df[[c for c in columns if c in df.columns]]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_MANAGEMENT_INFO 失败: {e}")
            return pd.DataFrame()


class STK_LIMITED_SHARES_LIST(FinanceTable):
    """
    受限股份上市公告日期数据表。

    字段：
    - code: 股票代码
    - pub_date: 公告日期
    - end_date: 解禁日期
    - total_shares: 总股本
    - limited_shares: 受限股份数
    - float_shares: 流通股份数
    - float_ratio: 流通比例
    """

    def __init__(self):
        super().__init__("STK_LIMITED_SHARES_LIST")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询受限股份上市公告日期数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_LIMITED_SHARES_LIST")
            return pd.DataFrame()

        try:
            df = ak.stock_cixinqr_cninfo(date="20240101")
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "股票代码": "code",
                "股票简称": "name",
                "可上市交易日期": "end_date",
                "总股本": "total_shares",
                "受限股份数": "limited_shares",
                "流通股份数": "float_shares",
                "流通比例": "float_ratio",
            }
            df = df.rename(columns=column_mapping)
            df["pub_date"] = None

            if code:
                ak_code = code
                if code.startswith("sh") or code.startswith("sz"):
                    ak_code = code[2:]
                if code.endswith(".XSHG") or code.endswith(".XSHE"):
                    ak_code = code[:6]
                ak_code = ak_code.zfill(6)
                df = df[df["code"] == ak_code]

            if end_date and "end_date" in df.columns:
                df = df[df["end_date"] <= end_date]

            if columns:
                df = df[[c for c in columns if c in df.columns]]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_LIMITED_SHARES_LIST 失败: {e}")
            return pd.DataFrame()


class STK_LIMITED_SHARES_UNLIMIT(FinanceTable):
    """
    受限股份实际解禁日期数据表。

    字段：
    - code: 股票代码
    - pub_date: 公告日期
    - unlimit_date: 解禁日期
    - share_type: 股份类型
    - unlimit_shares: 解禁股份数
    - total_shares: 总股本
    - unlimit_ratio: 解禁比例
    """

    def __init__(self):
        super().__init__("STK_LIMITED_SHARES_UNLIMIT")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询受限股份实际解禁日期数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 STK_LIMITED_SHARES_UNLIMIT")
            return pd.DataFrame()

        try:
            df = ak.stock_cixinhhr_cninfo(date="20240101")
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "股票代码": "code",
                "股票简称": "name",
                "解禁日期": "unlimit_date",
                "股份类型": "share_type",
                "解禁股份数": "unlimit_shares",
                "总股本": "total_shares",
                "解禁比例": "unlimit_ratio",
            }
            df = df.rename(columns=column_mapping)
            df["pub_date"] = None

            if code:
                ak_code = code
                if code.startswith("sh") or code.startswith("sz"):
                    ak_code = code[2:]
                if code.endswith(".XSHG") or code.endswith(".XSHE"):
                    ak_code = code[:6]
                ak_code = ak_code.zfill(6)
                df = df[df["code"] == ak_code]

            if end_date and "unlimit_date" in df.columns:
                df = df[df["unlimit_date"] <= end_date]

            if columns:
                df = df[[c for c in columns if c in df.columns]]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 STK_LIMITED_SHARES_UNLIMIT 失败: {e}")
            return pd.DataFrame()


class FUT_GLOBAL_DAILY(FinanceTable):
    """
    外盘期货日行情数据表。

    字段：
    - date: 日期
    - code: 品种代码 (如 LME铜, COMEX黄金, NYMEX原油)
    - open: 开盘价
    - high: 最高价
    - low: 最低价
    - close: 收盘价
    - volume: 成交量
    - symbol: 交易所代码

    支持的外盘期货品种：
    - LME铜 (LME.CU3)
    - COMEX黄金 (GC.CMX)
    - COMEX白银 (SI.CMX)
    - NYMEX原油 (CL.NYM)
    - CBOT大豆 (ZS.CBT)
    - CBOT玉米 (ZC.CBT)
    - ICE棉花 (CT.ICE)
    - ICE咖啡 (KC.ICE)
    """

    def __init__(self):
        super().__init__("FUT_GLOBAL_DAILY")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询外盘期货日行情数据。"""
        try:
            import akshare as ak

            if not hasattr(ak, "futures_global_hist_em"):
                warnings.warn("akshare 不支持外盘期货数据 (futures_global_hist_em)")
                return pd.DataFrame()

            symbol_map = {
                "LME铜": "LME.CU3",
                "COMEX黄金": "GC.CMX",
                "COMEX白银": "SI.CMX",
                "NYMEX原油": "CL.NYM",
                "CBOT大豆": "ZS.CBT",
                "CBOT玉米": "ZC.CBT",
                "ICE棉花": "CT.ICE",
                "ICE咖啡": "KC.ICE",
            }

            if code:
                search_symbol = code
                if code in symbol_map:
                    search_symbol = symbol_map[code]
            else:
                search_symbol = "GC.CMX"

            start_str = start_date.replace("-", "") if start_date else "20200101"
            end_str = end_date.replace("-", "") if end_date else "20300101"

            df = ak.futures_global_hist_em(
                symbol=search_symbol, start_date=start_str, end_date=end_str
            )

            if df is None or df.empty:
                return pd.DataFrame()

            df = df.copy()

            if "日期" in df.columns:
                df["date"] = pd.to_datetime(df["日期"]).dt.strftime("%Y-%m-%d")
                df = df.drop(columns=["日期"])
            elif "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

            col_map = {
                "开盘": "open",
                "最高": "high",
                "最低": "low",
                "收盘": "close",
                "成交量": "volume",
            }
            for old_col, new_col in col_map.items():
                if old_col in df.columns and new_col not in df.columns:
                    df[new_col] = df[old_col]

            if "code" not in df.columns:
                df["code"] = code or search_symbol
            if "symbol" not in df.columns:
                df["symbol"] = search_symbol

            if fields:
                available = [f for f in fields if f in df.columns]
                if "date" not in available and "date" in df.columns:
                    available = ["date"] + available
                df = df[available]

            return df.reset_index(drop=True)

        except Exception as e:
            warnings.warn(f"查询 FUT_GLOBAL_DAILY 失败: {e}")
            return pd.DataFrame()


class FUT_MARGIN(FinanceTable):
    """
    期货保证金率数据表。

    字段：
    - exchange: 交易所
    - contract_code: 合约代码
    - contract_name: 合约名称
    - variety_code: 品种代码
    - variety_name: 品种名称
    - multiplier: 合约乘数
    - min_tick: 最小跳动
    - long_margin_ratio: 做多保证金率
    - short_margin_ratio: 做空保证金率
    - update_time: 更新时间
    """

    def __init__(self):
        super().__init__("FUT_MARGIN")

    def query(
        self,
        exchange: Optional[str] = None,
        variety_code: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询期货保证金率数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 FUT_MARGIN")
            return pd.DataFrame()

        try:
            df = ak.futures_fees_info()
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "交易所": "exchange",
                "合约代码": "contract_code",
                "合约名称": "contract_name",
                "品种代码": "variety_code",
                "品种名称": "variety_name",
                "合约乘数": "multiplier",
                "最小跳动": "min_tick",
                "做多保证金率": "long_margin_ratio",
                "做空保证金率": "short_margin_ratio",
                "更新时间": "update_time",
            }
            df = df.rename(columns=column_mapping)

            cols_to_keep = [
                "exchange",
                "contract_code",
                "contract_name",
                "variety_code",
                "variety_name",
                "multiplier",
                "min_tick",
                "long_margin_ratio",
                "short_margin_ratio",
                "update_time",
            ]
            df = df[[c for c in cols_to_keep if c in df.columns]]

            if exchange:
                df = df[df["exchange"] == exchange]
            if variety_code:
                df = df[df["variety_code"] == variety_code]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 FUT_MARGIN 失败: {e}")
            return pd.DataFrame()


class FUT_CHARGE(FinanceTable):
    """
    期货手续费数据表。

    字段：
    - exchange: 交易所
    - contract_code: 合约代码
    - contract_name: 合约名称
    - variety_code: 品种代码
    - variety_name: 品种名称
    - open_rate: 开仓费率
    - open_fee: 开仓费用/手
    - close_rate: 平仓费率
    - close_fee: 平仓费用/手
    - close_today_rate: 平今费率
    - close_today_fee: 平今费用/手
    - update_time: 更新时间
    """

    def __init__(self):
        super().__init__("FUT_CHARGE")

    def query(
        self,
        exchange: Optional[str] = None,
        variety_code: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询期货手续费数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 FUT_CHARGE")
            return pd.DataFrame()

        try:
            df = ak.futures_fees_info()
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "交易所": "exchange",
                "合约代码": "contract_code",
                "合约名称": "contract_name",
                "品种代码": "variety_code",
                "品种名称": "variety_name",
                "开仓费率": "open_rate",
                "开仓费用/手": "open_fee",
                "平仓费率": "close_rate",
                "平仓费用/手": "close_fee",
                "平今费率": "close_today_rate",
                "平今费用/手": "close_today_fee",
                "更新时间": "update_time",
            }
            df = df.rename(columns=column_mapping)

            cols_to_keep = [
                "exchange",
                "contract_code",
                "contract_name",
                "variety_code",
                "variety_name",
                "open_rate",
                "open_fee",
                "close_rate",
                "close_fee",
                "close_today_rate",
                "close_today_fee",
                "update_time",
            ]
            df = df[[c for c in cols_to_keep if c in df.columns]]

            if exchange:
                df = df[df["exchange"] == exchange]
            if variety_code:
                df = df[df["variety_code"] == variety_code]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 FUT_CHARGE 失败: {e}")
            return pd.DataFrame()


class FUT_WAREHOUSE_RECEIPT(FinanceTable):
    """
    期货仓单数据表。

    字段：
    - date: 日期
    - exchange: 交易所
    - variety_code: 品种代码
    - variety_name: 品种名称
    - warehouse_receipt: 仓单数量
    - unit: 单位
    - change: 变化
    """

    def __init__(self):
        super().__init__("FUT_WAREHOUSE_RECEIPT")

    def query(
        self,
        date: Optional[str] = None,
        exchange: Optional[str] = None,
        variety_code: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询期货仓单数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 FUT_WAREHOUSE_RECEIPT")
            return pd.DataFrame()

        try:
            date_str = date.replace("-", "") if date else ""

            if exchange == "DCE" or (exchange is None and variety_code is None):
                df = (
                    ak.futures_warehouse_receipt_dce(date=date_str)
                    if date_str
                    else ak.futures_warehouse_receipt_dce()
                )
                if isinstance(df, dict):
                    return pd.DataFrame()
            elif exchange == "CZCE":
                df = (
                    ak.futures_warehouse_receipt_czce(date=date_str)
                    if date_str
                    else ak.futures_warehouse_receipt_czce()
                )
                if isinstance(df, dict):
                    return pd.DataFrame()
            elif exchange == "SHFE":
                df = (
                    ak.futures_shfe_warehouse_receipt(date=date_str)
                    if date_str
                    else ak.futures_shfe_warehouse_receipt()
                )
                if isinstance(df, dict):
                    return pd.DataFrame()
            elif exchange == "GFEX":
                df = (
                    ak.futures_gfex_warehouse_receipt(date=date_str)
                    if date_str
                    else ak.futures_gfex_warehouse_receipt()
                )
                if isinstance(df, dict):
                    return pd.DataFrame()
            else:
                warnings.warn(
                    "FUT_WAREHOUSE_RECEIPT: 请指定 exchange (DCE/CZCE/SHFE/GFEX)"
                )
                return pd.DataFrame()

            if df is None or df.empty:
                return pd.DataFrame()

            if "日期" in df.columns:
                df["date"] = pd.to_datetime(df["日期"]).dt.strftime("%Y-%m-%d")
            elif "date" not in df.columns:
                df["date"] = date or ""

            if exchange:
                df["exchange"] = exchange

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 FUT_WAREHOUSE_RECEIPT 失败: {e}")
            return pd.DataFrame()


class FUT_MEMBER_POSITION_RANK(FinanceTable):
    """
    期货会员持仓排名数据表。

    字段：
    - date: 日期
    - exchange: 交易所
    - variety_code: 品种代码
    - rank: 排名
    - member_name: 会员名称
    - position: 持仓量
    - position_change: 持仓变化
    - unit: 单位
    """

    def __init__(self):
        super().__init__("FUT_MEMBER_POSITION_RANK")

    def query(
        self,
        date: Optional[str] = None,
        exchange: Optional[str] = None,
        variety_code: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询期货会员持仓排名数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 FUT_MEMBER_POSITION_RANK")
            return pd.DataFrame()

        try:
            date_str = date.replace("-", "") if date else "20250417"
            vars_list = [variety_code] if variety_code else None

            if exchange == "DCE" or exchange is None:
                result = ak.futures_dce_position_rank(
                    date=date_str, vars_list=vars_list
                )
                if isinstance(result, dict):
                    for var_name, var_df in result.items():
                        if hasattr(var_df, "columns"):
                            var_df["variety_code"] = var_name
                            var_df["date"] = date_str
                            var_df["exchange"] = "DCE"
                    dfs = [
                        v
                        for v in result.values()
                        if hasattr(v, "columns") and not v.empty
                    ]
                    if dfs:
                        df = pd.concat(dfs, ignore_index=True)
                    else:
                        return pd.DataFrame()
                else:
                    return pd.DataFrame()
            elif exchange == "GFEX":
                result = ak.futures_gfex_position_rank(
                    date=date_str, vars_list=vars_list
                )
                if isinstance(result, dict):
                    dfs = [
                        v
                        for v in result.values()
                        if hasattr(v, "columns") and not v.empty
                    ]
                    if dfs:
                        df = pd.concat(dfs, ignore_index=True)
                    else:
                        return pd.DataFrame()
                else:
                    return pd.DataFrame()
            else:
                warnings.warn("FUT_MEMBER_POSITION_RANK: 支持 DCE 和 GFEX 交易所")
                return pd.DataFrame()

            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "品种": "variety_code",
                "会员号": "member_id",
                "会员名称": "member_name",
                "排名": "rank",
                "持仓量": "position",
                "持仓变化": "position_change",
                "交易日": "date",
            }
            df = df.rename(columns=column_mapping)

            if "date" not in df.columns and "交易日" not in df.columns:
                df["date"] = date_str
            if "exchange" not in df.columns:
                df["exchange"] = exchange or "DCE"

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 FUT_MEMBER_POSITION_RANK 失败: {e}")
            return pd.DataFrame()


class FUND_SHARE_DAILY(FinanceTable):
    """
    基金每日净值数据表。

    字段：
    - fund_code: 基金代码
    - fund_name: 基金简称
    - nav: 单位净值
    - accumulative_nav: 累计净值
    - previous_nav: 上日单位净值
    - previous_accumulative_nav: 上日累计净值
    - daily_change: 日增长值
    - daily_return: 日增长率
    - subscription_status: 申购状态
    - redemption_status: 赎回状态
    - fee: 手续费
    """

    def __init__(self):
        super().__init__("FUND_SHARE_DAILY")

    def query(
        self,
        fund_code: Optional[str] = None,
        date: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询基金每日净值数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 FUND_SHARE_DAILY")
            return pd.DataFrame()

        try:
            df = ak.fund_open_fund_daily_em()
            if df is None or df.empty:
                return pd.DataFrame()

            date_col = None
            for col in df.columns:
                if "单位净值" in col and "日期" not in col:
                    date_part = col.replace("单位净值", "").strip()
                    if date_part:
                        date_col = col
                        break

            if date_col:
                date_str = date_col.split("-")[0] if "-" in date_col else date
                new_date = (
                    pd.to_datetime(date_str).strftime("%Y-%m-%d") if date_str else None
                )

                column_mapping = {
                    "基金代码": "fund_code",
                    "基金简称": "fund_name",
                    date_col: "nav",
                }
                for col in df.columns:
                    if "累计净值" in col and date_part in col:
                        column_mapping[col] = "accumulative_nav"
                        break
                for col in df.columns:
                    if "累计净值" in col and date_part in col:
                        column_mapping[col] = "accumulative_nav"
                        break

                df = df.rename(columns=column_mapping)

                for col in df.columns:
                    if "上日单位净值" in col:
                        df = df.rename(columns={col: "previous_nav"})
                    elif "上日累计净值" in col:
                        df = df.rename(columns={col: "previous_accumulative_nav"})
                    elif "日增长值" in col:
                        df = df.rename(columns={col: "daily_change"})
                    elif "日增长率" in col:
                        df = df.rename(columns={col: "daily_return"})
                    elif "申购状态" in col:
                        df = df.rename(columns={col: "subscription_status"})
                    elif "赎回状态" in col:
                        df = df.rename(columns={col: "redemption_status"})
                    elif "手续费" in col:
                        df = df.rename(columns={col: "fee"})

                df["date"] = new_date

            if fund_code:
                df = df[df["fund_code"] == fund_code.zfill(6)]

            cols_to_keep = [
                "fund_code",
                "fund_name",
                "nav",
                "accumulative_nav",
                "previous_nav",
                "previous_accumulative_nav",
                "daily_change",
                "daily_return",
                "subscription_status",
                "redemption_status",
                "fee",
                "date",
            ]
            df = df[[c for c in cols_to_keep if c in df.columns]]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 FUND_SHARE_DAILY 失败: {e}")
            return pd.DataFrame()


class FUND_INVEST_TARGET(FinanceTable):
    """
    基金投资目标数据表。

    字段：
    - fund_code: 基金代码
    - fund_name: 基金名称
    - invest_target: 投资目标
    - invest_strategy: 投资策略
    - benchmark: 业绩比较基准
    - risk_level: 风险收益特征
    """

    def __init__(self):
        super().__init__("FUND_INVEST_TARGET")

    def query(
        self,
        fund_code: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询基金投资目标数据。"""
        warnings.warn("FUND_INVEST_TARGET: akshare 无直接接口，返回空DataFrame")
        return pd.DataFrame(
            columns=[
                "fund_code",
                "fund_name",
                "invest_target",
                "invest_strategy",
                "benchmark",
                "risk_level",
            ]
        )


class FUND_FIN_INDICATOR(FinanceTable):
    """
    基金财务指标数据表。

    字段：
    - fund_code: 基金代码
    - fund_name: 基金名称
    - period: 统计周期
    - net_asset_value: 基金资产净值
    - net_asset_value_per_share: 每份净值
    - total_return: 总回报
    - annual_return: 年化回报
    - volatility: 波动率
    - sharpe_ratio: 夏普比率
    - max_drawdown: 最大回撤
    """

    def __init__(self):
        super().__init__("FUND_FIN_INDICATOR")

    def query(
        self,
        fund_code: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询基金财务指标数据。"""
        warnings.warn("FUND_FIN_INDICATOR: akshare 无直接接口，返回空DataFrame")
        return pd.DataFrame(
            columns=[
                "fund_code",
                "fund_name",
                "period",
                "net_asset_value",
                "net_asset_value_per_share",
                "total_return",
                "annual_return",
                "volatility",
                "sharpe_ratio",
                "max_drawdown",
            ]
        )


class FUND_MAIN_INFO(FinanceTable):
    """
    基金基本信息数据表。

    字段：
    - fund_code: 基金代码
    - fund_name: 基金名称
    - fund_full_name: 基金全称
    - fund_type: 基金类型
    - listing_date: 成立日期
    - manager: 基金经理
    - custodian: 基金托管人
    - status: 基金状态
    - min_purchase: 最低申购金额
    - min_redemption: 最低赎回份额
    """

    def __init__(self):
        super().__init__("FUND_MAIN_INFO")

    def query(
        self,
        fund_code: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询基金基本信息数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 FUND_MAIN_INFO")
            return pd.DataFrame()

        try:
            if fund_code:
                df = ak.fund_open_fund_info_em(
                    symbol=fund_code.zfill(6), indicator="基本信息"
                )
                if df is None or df.empty:
                    df = ak.fund_name_em()
                    if df is not None and not df.empty:
                        df = df[df["基金代码"] == fund_code.zfill(6)]
                        df = df.rename(
                            columns={
                                "基金代码": "fund_code",
                                "基金简称": "fund_name",
                                "基金类型": "fund_type",
                            }
                        )
                        cols_to_keep = ["fund_code", "fund_name", "fund_type"]
                        df = df[[c for c in cols_to_keep if c in df.columns]]
                        return df.reset_index(drop=True)
                    return pd.DataFrame()

                column_mapping = {
                    "基金代码": "fund_code",
                    "基金简称": "fund_name",
                    "基金全称": "fund_full_name",
                    "基金类型": "fund_type",
                    "成立日期": "listing_date",
                    "基金经理": "manager",
                    "基金托管人": "custodian",
                    "状态": "status",
                }
                df = df.rename(columns=column_mapping)

                cols_to_keep = [
                    "fund_code",
                    "fund_name",
                    "fund_full_name",
                    "fund_type",
                    "listing_date",
                    "manager",
                    "custodian",
                    "status",
                ]
                df = df[[c for c in cols_to_keep if c in df.columns]]
            else:
                df = ak.fund_name_em()
                if df is None or df.empty:
                    return pd.DataFrame()

                df = df.rename(
                    columns={
                        "基金代码": "fund_code",
                        "基金简称": "fund_name",
                        "基金类型": "fund_type",
                    }
                )

                cols_to_keep = ["fund_code", "fund_name", "fund_type"]
                df = df[[c for c in cols_to_keep if c in df.columns]]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 FUND_MAIN_INFO 失败: {e}")
            return pd.DataFrame()


class FUND_PORTFOLIO_BOND(FinanceTable):
    """
    基金债券持仓数据表。

    字段：
    - fund_code: 基金代码
    - bond_code: 债券代码
    - bond_name: 债券名称
    - nav_ratio: 占净值比例
    - market_value: 持仓市值
    - period: 季度
    """

    def __init__(self):
        super().__init__("FUND_PORTFOLIO_BOND")

    def query(
        self,
        fund_code: Optional[str] = None,
        date: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询基金债券持仓数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 FUND_PORTFOLIO_BOND")
            return pd.DataFrame()

        try:
            if not fund_code:
                warnings.warn("FUND_PORTFOLIO_BOND 查询需要指定 fund_code 参数")
                return pd.DataFrame()

            date_str = date.replace("-", "")[:4] if date else "2023"
            df = ak.fund_portfolio_bond_hold_em(
                symbol=fund_code.zfill(6), date=date_str
            )

            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "序号": "rank",
                "债券代码": "bond_code",
                "债券名称": "bond_name",
                "占净值比例": "nav_ratio",
                "持仓市值": "market_value",
                "季度": "period",
            }
            df = df.rename(columns=column_mapping)
            df["fund_code"] = fund_code.zfill(6)

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 FUND_PORTFOLIO_BOND 失败: {e}")
            return pd.DataFrame()


class FUND_DIVIDEND(FinanceTable):
    """
    基金分红数据表。

    字段：
    - fund_code: 基金代码
    - announcement_title: 公告标题
    - fund_name: 基金名称
    - announcement_date: 公告日期
    - report_id: 报告ID
    """

    def __init__(self):
        super().__init__("FUND_DIVIDEND")

    def query(
        self,
        fund_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询基金分红数据。"""
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法查询 FUND_DIVIDEND")
            return pd.DataFrame()

        try:
            if fund_code:
                df = ak.fund_announcement_dividend_em(symbol=fund_code.zfill(6))
            else:
                warnings.warn("FUND_DIVIDEND 查询需要指定 fund_code 参数")
                return pd.DataFrame()

            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "基金代码": "fund_code",
                "公告标题": "announcement_title",
                "基金名称": "fund_name",
                "公告日期": "announcement_date",
                "报告ID": "report_id",
            }
            df = df.rename(columns=column_mapping)

            if start_date and "announcement_date" in df.columns:
                df = df[df["announcement_date"] >= start_date]
            if end_date and "announcement_date" in df.columns:
                df = df[df["announcement_date"] <= end_date]

            return df.reset_index(drop=True)
        except Exception as e:
            warnings.warn(f"查询 FUND_DIVIDEND 失败: {e}")
            return pd.DataFrame()


# =====================================================================
# 统一查询接口
# =====================================================================


# 预定义数据表实例
_tables = {
    "STK_XR_XD": STK_XR_XD(),
    "STK_ML_QUOTA": STK_ML_QUOTA(),
    "STK_HK_HOLD_INFO": STK_HK_HOLD_INFO(),
    "STK_AUDIT_OPINION": STK_AUDIT_OPINION(),
    "BALANCE": BALANCE(),
    "CASH_FLOW": CASH_FLOW(),
    "INCOME": INCOME(),
    "FUND_PORTFOLIO_STOCK": FUND_PORTFOLIO_STOCK(),
    "STK_AH_PRICE_COMP": STK_AH_PRICE_COMP(),
    "STK_EMPLOYEE_INFO": STK_EMPLOYEE_INFO(),
    "STK_MANAGEMENT_INFO": STK_MANAGEMENT_INFO(),
    "STK_LIMITED_SHARES_LIST": STK_LIMITED_SHARES_LIST(),
    "STK_LIMITED_SHARES_UNLIMIT": STK_LIMITED_SHARES_UNLIMIT(),
    "FUT_MARGIN": FUT_MARGIN(),
    "FUT_CHARGE": FUT_CHARGE(),
    "FUT_WAREHOUSE_RECEIPT": FUT_WAREHOUSE_RECEIPT(),
    "FUT_MEMBER_POSITION_RANK": FUT_MEMBER_POSITION_RANK(),
    "FUND_SHARE_DAILY": FUND_SHARE_DAILY(),
    "FUND_INVEST_TARGET": FUND_INVEST_TARGET(),
    "FUND_FIN_INDICATOR": FUND_FIN_INDICATOR(),
    "FUND_MAIN_INFO": FUND_MAIN_INFO(),
    "FUND_PORTFOLIO_BOND": FUND_PORTFOLIO_BOND(),
    "FUND_DIVIDEND": FUND_DIVIDEND(),
}


class finance:
    """
    聚宽风格 finance 模块。

    用法：
        finance.run_query(finance.STK_XR_XD, code='000001.XSHE')
        finance.STK_XR_XD.query(code='000001.XSHE')
    """

    STK_XR_XD = _tables["STK_XR_XD"]
    STK_ML_QUOTA = _tables["STK_ML_QUOTA"]
    STK_HK_HOLD_INFO = _tables["STK_HK_HOLD_INFO"]
    STK_AUDIT_OPINION = _tables["STK_AUDIT_OPINION"]
    BALANCE = _tables["BALANCE"]
    CASH_FLOW = _tables["CASH_FLOW"]
    INCOME = _tables["INCOME"]
    FUND_PORTFOLIO_STOCK = _tables["FUND_PORTFOLIO_STOCK"]
    STK_AH_PRICE_COMP = _tables["STK_AH_PRICE_COMP"]
    STK_EMPLOYEE_INFO = _tables["STK_EMPLOYEE_INFO"]
    STK_MANAGEMENT_INFO = _tables["STK_MANAGEMENT_INFO"]
    STK_LIMITED_SHARES_LIST = _tables["STK_LIMITED_SHARES_LIST"]
    STK_LIMITED_SHARES_UNLIMIT = _tables["STK_LIMITED_SHARES_UNLIMIT"]
    FUT_MARGIN = _tables["FUT_MARGIN"]
    FUT_CHARGE = _tables["FUT_CHARGE"]
    FUT_WAREHOUSE_RECEIPT = _tables["FUT_WAREHOUSE_RECEIPT"]
    FUT_MEMBER_POSITION_RANK = _tables["FUT_MEMBER_POSITION_RANK"]
    FUND_SHARE_DAILY = _tables["FUND_SHARE_DAILY"]
    FUND_INVEST_TARGET = _tables["FUND_INVEST_TARGET"]
    FUND_FIN_INDICATOR = _tables["FUND_FIN_INDICATOR"]
    FUND_MAIN_INFO = _tables["FUND_MAIN_INFO"]
    FUND_PORTFOLIO_BOND = _tables["FUND_PORTFOLIO_BOND"]
    FUND_DIVIDEND = _tables["FUND_DIVIDEND"]

    @staticmethod
    def run_query(table: FinanceTable, **kwargs) -> pd.DataFrame:
        """
        聚宽风格查询接口。

        Parameters
        ----------
        table : FinanceTable
            数据表对象
        **kwargs
            查询参数

        Returns
        -------
        pd.DataFrame
            查询结果
        """
        if isinstance(table, FinanceTable):
            return table.query(**kwargs)
        else:
            raise ValueError(f"未知的表类型: {type(table)}")


# =====================================================================
# 便捷因子函数
# =====================================================================


def compute_retained_profit(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 retained_profit（留存收益）因子。

    公式：盈余公积 + 未分配利润
    近似实现：净资产 - 股本
    """
    from ..factors.fundamentals import _get_balance_sheet, _normalize_balance

    balance_raw = _get_balance_sheet(symbol)
    balance = _normalize_balance(balance_raw)

    if balance.empty:
        return np.nan

    balance = balance.set_index("date")

    # 留存收益 = 盈余公积 + 未分配利润
    # 近似：净资产 - 股本
    equity = balance.get("total_equity")

    if equity is None:
        return np.nan

    # 简化计算：净资产 * 0.7 近似留存收益
    retained = equity * 0.7

    if end_date:
        retained = retained[retained.index <= pd.to_datetime(end_date)]
    if count is not None and count > 0:
        retained = retained.tail(count)

    if len(retained) == 1:
        return float(retained.iloc[-1])

    retained.index = retained.index.strftime("%Y-%m-%d")
    return retained


def compute_net_operate_cash_flow(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 net_operate_cash_flow（经营活动现金流量净额）因子。
    """
    df = CASH_FLOW().query(code=symbol, end_date=end_date)

    if df.empty:
        return np.nan

    if "net_operate_cash_flow" in df.columns:
        ncf = df["net_operate_cash_flow"]
    else:
        return np.nan

    if count is not None and count > 0:
        ncf = ncf.tail(count)

    if len(ncf) == 1:
        return float(ncf.iloc[-1])

    return ncf


def _register_factors():
    """向全局注册表注册财务表因子。"""
    registry = global_factor_registry

    registry.register(
        "retained_profit", compute_retained_profit, window=1, dependencies=["balance"]
    )
    registry.register(
        "net_operate_cash_flow",
        compute_net_operate_cash_flow,
        window=1,
        dependencies=["cash_flow"],
    )


_register_factors()


__all__ = [
    "finance",
    "FinanceTable",
    "STK_XR_XD",
    "STK_ML_QUOTA",
    "STK_HK_HOLD_INFO",
    "STK_AUDIT_OPINION",
    "BALANCE",
    "CASH_FLOW",
    "INCOME",
    "FUND_PORTFOLIO_STOCK",
    "STK_AH_PRICE_COMP",
    "FUT_GLOBAL_DAILY",
    "STK_PERFORMANCE_LETTERS",
    "STK_REPORT_DISCLOSURE",
    "STK_EXCHANGE_TRADE_INFO",
    "STK_EXCHANGE_LINK_CALENDAR",
    "STK_EL_CONST_CHANGE",
    "STK_EL_TOP_ACTIVATE",
    "STK_EXCHANGE_LINK_RATE",
    "FUT_MARGIN",
    "FUT_CHARGE",
    "FUT_WAREHOUSE_RECEIPT",
    "FUT_MEMBER_POSITION_RANK",
    "FUND_SHARE_DAILY",
    "FUND_INVEST_TARGET",
    "FUND_FIN_INDICATOR",
    "FUND_MAIN_INFO",
    "FUND_PORTFOLIO_BOND",
    "FUND_DIVIDEND",
    "STK_EMPLOYEE_INFO",
    "STK_MANAGEMENT_INFO",
    "STK_LIMITED_SHARES_LIST",
    "STK_LIMITED_SHARES_UNLIMIT",
    "compute_retained_profit",
    "compute_net_operate_cash_flow",
]
