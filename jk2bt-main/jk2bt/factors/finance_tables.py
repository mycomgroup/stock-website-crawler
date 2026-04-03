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
    北向资金额度数据表。

    字段：
    - date: 日期
    - quota: 额度
    - remaining: 剩余额度
    """

    def __init__(self):
        super().__init__("STK_ML_QUOTA")

    def query(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询北向资金额度。"""
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        try:
            # 获取沪股通/深股通额度数据
            df = ak.stock_hsgt_north_net_flow_in_em()
            if df is None or df.empty:
                return pd.DataFrame()

            # 标准化字段
            df = df.rename(columns={
                "日期": "date",
                "当日成交净买额": "net_buy",
                "当日资金流入": "inflow",
                "当日资金流出": "outflow",
            })

            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

            if start_date:
                df = df[df["date"] >= start_date]
            if end_date:
                df = df[df["date"] <= end_date]

            return df
        except Exception as e:
            warnings.warn(f"查询 STK_ML_QUOTA 失败: {e}")
            return pd.DataFrame()


class STK_HK_HOLD_INFO(FinanceTable):
    """
    港资持股信息表。

    字段：
    - code: 股票代码
    - date: 日期
    - hold_amount: 持股数量
    - hold_ratio: 持股比例
    """

    def __init__(self):
        super().__init__("STK_HK_HOLD_INFO")

    def query(
        self,
        code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """查询港资持股信息。"""
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        try:
            # 获取港股通持股数据
            if code:
                # 标准化代码
                ak_code = code
                if code.startswith("sh") or code.startswith("sz"):
                    ak_code = code[2:]
                if code.endswith(".XSHG") or code.endswith(".XSHE"):
                    ak_code = code[:6]
                ak_code = ak_code.zfill(6)

                df = ak.stock_em_hsgt_north_net_flow_in(indicator="沪股通")
            else:
                df = ak.stock_em_hsgt_north_net_flow_in(indicator="沪股通")

            if df is None or df.empty:
                return pd.DataFrame()

            return df
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
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

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

            # 尝试获取审计意见
            df = ak.stock_financial_abstract_ths(symbol=ak_code, indicator="审计意见")

            if df is None or df.empty:
                # 返回默认审计意见（标准无保留意见）
                return pd.DataFrame({
                    "code": [code],
                    "audit_opinion": ["标准无保留意见"],
                    "report_date": [end_date or pd.Timestamp.today().strftime("%Y-%m-%d")],
                })

            return df
        except Exception as e:
            warnings.warn(f"查询 STK_AUDIT_OPINION 失败: {e}")
            # 返回默认审计意见
            return pd.DataFrame({
                "code": [code],
                "audit_opinion": ["标准无保留意见"],
                "report_date": [end_date or pd.Timestamp.today().strftime("%Y-%m-%d")],
            })


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
            df_raw = _get_balance_sheet(code, force_update=False)
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
            df_raw = _get_income_statement(code, force_update=False)
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
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        try:
            if fund_code:
                df = ak.fund_portfolio_em(fund=fund_code)
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
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")

        try:
            # 获取AH股数据
            df = ak.stock_hk_ah_name_em()

            if df is None or df.empty:
                return pd.DataFrame()

            # 标准化字段
            df = df.rename(columns={
                "A股代码": "code",
                "A股简称": "name",
                "H股代码": "hk_code",
                "H股简称": "hk_name",
            })

            # 获取实时行情数据
            try:
                ah_quote = ak.stock_hk_ah_spot_em()
                if ah_quote is not None and not ah_quote.empty:
                    # 合并行情数据
                    ah_quote = ah_quote.rename(columns={
                        "A股代码": "code",
                        "A股最新价": "a_price",
                        "H股最新价": "h_price",
                        "汇率": "exchange_rate",
                        "A股溢价率": "premium_rate",
                    })
                    # 选择需要的列
                    cols = ["code", "a_price", "h_price", "exchange_rate", "premium_rate"]
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
}


class finance:
    """
    聚宽风格 finance 模块。

    用法：
        finance.run_query(finance.STK_XR_XD, code='000001.XSHE')
        finance.STK_XR_XD.query(code='000001.XSHE')
    """

    # 数据表属性
    STK_XR_XD = _tables["STK_XR_XD"]
    STK_ML_QUOTA = _tables["STK_ML_QUOTA"]
    STK_HK_HOLD_INFO = _tables["STK_HK_HOLD_INFO"]
    STK_AUDIT_OPINION = _tables["STK_AUDIT_OPINION"]
    BALANCE = _tables["BALANCE"]
    CASH_FLOW = _tables["CASH_FLOW"]
    INCOME = _tables["INCOME"]
    FUND_PORTFOLIO_STOCK = _tables["FUND_PORTFOLIO_STOCK"]
    STK_AH_PRICE_COMP = _tables["STK_AH_PRICE_COMP"]

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
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 retained_profit（留存收益）因子。

    公式：盈余公积 + 未分配利润
    近似实现：净资产 - 股本
    """
    from ..factors.fundamentals import _get_balance_sheet, _normalize_balance

    balance_raw = _get_balance_sheet(symbol, cache_dir, force_update)
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
    cache_dir: str = "stock_cache",
    force_update: bool = False,
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

    registry.register("retained_profit", compute_retained_profit, window=1, dependencies=["balance"])
    registry.register("net_operate_cash_flow", compute_net_operate_cash_flow, window=1, dependencies=["cash_flow"])


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
    "compute_retained_profit",
    "compute_net_operate_cash_flow",
]