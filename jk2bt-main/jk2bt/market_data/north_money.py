"""
market_data/north_money.py
北向资金数据模块，使用 AkShare 获取北向资金流入流出数据。

功能:
- 北向资金净流入（日度）
- 北向资金持股统计
- 北向资金个股流入
"""

import warnings
from typing import Optional, List, Dict
import pandas as pd
import numpy as np
from datetime import datetime

try:
    import akshare as ak

    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    warnings.warn("akshare未安装，北向资金数据将不可用")


def get_north_money_flow(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取北向资金净流入数据（日度）。

    参数
    ----
    start_date : str, optional
        开始日期 'YYYY-MM-DD'
    end_date : str, optional
        结束日期 'YYYY-MM-DD'

    返回
    ----
    pd.DataFrame
        北向资金净流入数据，包含日期、净流入金额等
    """
    if not AKSHARE_AVAILABLE:
        raise ImportError("请安装 akshare: pip install akshare")

    try:
        df = ak.stock_em_hsgt_north_net_flow_in(symbol="北上")
        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "日期": "date",
                    "当日净流入": "net_inflow",
                    "当日资金流入": "inflow",
                    "当日资金流出": "outflow",
                }
            )

            df["date"] = pd.to_datetime(df["date"])

            if start_date:
                df = df[df["date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["date"] <= pd.to_datetime(end_date)]

            return df.sort_values("date").reset_index(drop=True)
    except Exception as e:
        warnings.warn(f"获取北向资金净流入失败: {e}")

    return pd.DataFrame()


def get_north_money_daily(
    date: Optional[str] = None,
) -> Dict[str, float]:
    """
    获取某日的北向资金数据。

    参数
    ----
    date : str, optional
        查询日期，默认最近交易日

    返回
    ----
    Dict[str, float]
        {'net_inflow': 净流入金额, 'inflow': 流入, 'outflow': 流出}
    """
    df = get_north_money_flow(end_date=date)

    if df.empty:
        return {"net_inflow": 0.0, "inflow": 0.0, "outflow": 0.0}

    latest = df.iloc[-1]
    return {
        "net_inflow": float(latest.get("net_inflow", 0)),
        "inflow": float(latest.get("inflow", 0)),
        "outflow": float(latest.get("outflow", 0)),
    }


def get_north_money_holdings(
    date: Optional[str] = None,
    top_n: int = 50,
) -> pd.DataFrame:
    """
    获取北向资金持股统计。

    参数
    ----
    date : str, optional
        查询日期
    top_n : int
        返回持股量前N只股票

    返回
    ----
    pd.DataFrame
        北向资金持股数据
    """
    if not AKSHARE_AVAILABLE:
        raise ImportError("请安装 akshare: pip install akshare")

    try:
        df = ak.stock_em_hsgt_hold_stock(symbol="北向", indicator="今日")
        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "股票代码": "code",
                    "股票名称": "name",
                    "持股数量": "holdings",
                    "持股市值": "holding_value",
                    "持股数量占A股百分比": "holding_pct",
                    "持股市值占A股百分比": "holding_value_pct",
                    "持股数量变化": "holdings_change",
                    "持股市值变化": "holding_value_change",
                }
            )

            if "holding_value" in df.columns:
                df = df.sort_values("holding_value", ascending=False)

            return df.head(top_n)
    except Exception as e:
        warnings.warn(f"获取北向资金持股统计失败: {e}")

    return pd.DataFrame()


def get_north_money_stock_flow(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取某股票的北向资金流入数据。

    参数
    ----
    symbol : str
        股票代码
    start_date : str
        开始日期
    end_date : str
        结束日期

    返回
    ----
    pd.DataFrame
        该股票的北向资金流入数据
    """
    if not AKSHARE_AVAILABLE:
        raise ImportError("请安装 akshare: pip install akshare")

    code = (
        symbol.replace("sh", "")
        .replace("sz", "")
        .replace(".XSHG", "")
        .replace(".XSHE", "")
        .zfill(6)
    )

    try:
        df = ak.stock_em_hsgt_individual_stock_flow(stock=code, indicator="北向资金")
        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "日期": "date",
                    "当日净流入": "net_inflow",
                    "当日资金流入": "inflow",
                    "当日资金流出": "outflow",
                }
            )

            df["date"] = pd.to_datetime(df["date"])

            if start_date:
                df = df[df["date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["date"] <= pd.to_datetime(end_date)]

            return df.sort_values("date").reset_index(drop=True)
    except Exception as e:
        warnings.warn(f"获取个股北向资金流入失败 {symbol}: {e}")

    return pd.DataFrame()


def get_north_money_stock_detail(
    symbol: str,
    date: Optional[str] = None,
) -> Dict[str, float]:
    """
    获取某股票某日的北向资金详情。

    返回
    ----
    Dict[str, float]
        {'net_inflow': 净流入, 'holdings': 持股数, 'holding_change': 持股变化}
    """
    df = get_north_money_stock_flow(symbol, end_date=date)

    if df.empty:
        return {"net_inflow": 0.0, "holdings": 0.0, "holding_change": 0.0}

    latest = df.iloc[-1]
    return {
        "net_inflow": float(latest.get("net_inflow", 0)),
        "holdings": 0.0,
        "holding_change": 0.0,
    }


def compute_north_money_signal(
    window: int = 20,
    threshold: float = 30.0,
    date: Optional[str] = None,
) -> Dict[str, any]:
    """
    计算北向资金择时信号。

    参数
    ----
    window : int
        计算均值的窗口期
    threshold : float
        判断阈值（亿元）
    date : str, optional
        计算截止日期

    返回
    ----
    Dict[str, any]
        {
            'signal': 1 (流入信号), -1 (流出信号), 0 (中性),
            'net_inflow': 当日净流入,
            'avg_inflow': 近N日平均净流入,
            'description': 信号描述
        }
    """
    df = get_north_money_flow(end_date=date)

    if df.empty or len(df) < window:
        return {
            "signal": 0,
            "net_inflow": 0.0,
            "avg_inflow": 0.0,
            "description": "数据不足",
        }

    df = df.tail(window)

    net_inflow = float(df["net_inflow"].iloc[-1])
    avg_inflow = float(df["net_inflow"].mean())

    if avg_inflow > threshold:
        signal = 1
        desc = f"北向资金持续流入，近{window}日平均净流入{avg_inflow:.2f}亿元"
    elif avg_inflow < -threshold:
        signal = -1
        desc = f"北向资金持续流出，近{window}日平均净流出{-avg_inflow:.2f}亿元"
    else:
        signal = 0
        desc = f"北向资金中性，近{window}日平均净流入{avg_inflow:.2f}亿元"

    return {
        "signal": signal,
        "net_inflow": net_inflow,
        "avg_inflow": avg_inflow,
        "description": desc,
    }


__all__ = [
    "get_north_money_flow",
    "get_north_money_daily",
    "get_north_money_holdings",
    "get_north_money_stock_flow",
    "get_north_money_stock_detail",
    "compute_north_money_signal",
]
