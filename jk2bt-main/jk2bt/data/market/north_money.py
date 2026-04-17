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

from jk2bt.data.sources import get_adapter


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
    if not start_date and not end_date:
        pass  # no filter needed

    try:
        df = get_adapter().get_hsgt_individual_stock_flow(
            stock=code, indicator="北向资金"
        )
        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "日期": "date",
                    "当日净流入": "net_inflow",
                    "当日资金流入": "inflow",
                    "当日资金流出": "outflow",
                    "持股数量": "holdings",
                    "持股数量变化": "holding_change",
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


def get_north_money_daily(
    date: Optional[str] = None,
) -> Dict[str, float]:
    """
    获取北向资金日度数据。

    参数
    ----
    date : str, optional
        查询日期，默认最近交易日

    返回
    ----
    Dict[str, float]
        {'net_inflow': 净流入金额, 'inflow': 流入, 'outflow': 流出}
    """
    try:
        df = get_adapter().get_hsgt_hsgt_stock_em(indicator="北向资金")
        if df is not None and not df.empty:
            df["日期"] = pd.to_datetime(df["日期"])
            if date:
                target_date = pd.to_datetime(date)
                df = df[df["日期"] == target_date]
            if not df.empty:
                latest = df.iloc[-1]
                return {
                    "net_inflow": float(latest.get("当日净流入", 0)),
                    "inflow": float(latest.get("当日资金流入", 0)),
                    "outflow": float(latest.get("当日资金流出", 0)),
                }
    except Exception as e:
        warnings.warn(f"获取北向资金日度数据失败: {e}")
    return {"net_inflow": 0.0, "inflow": 0.0, "outflow": 0.0}


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
        返回持股市值前N名

    返回
    ----
    pd.DataFrame
        北向资金持股数据
    """
    try:
        df = get_adapter().get_hsgt_hold_stock_em(indicator="北向资金持股")
        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "股票代码": "code",
                    "股票名称": "name",
                    "持股数": "holdings",
                    "持股市值": "market_value",
                    "持股占流通股比": "float_ratio",
                }
            )
            df = df.head(top_n)
            return df.reset_index(drop=True)
    except Exception as e:
        warnings.warn(f"获取北向资金持股数据失败: {e}")
    return pd.DataFrame()


def get_north_money_stock_flow(
    symbol: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取北向资金个股流入数据。

    参数
    ----
    symbol : str, optional
        股票代码
    start_date : str, optional
        开始日期
    end_date : str, optional
        结束日期

    返回
    ----
    pd.DataFrame
        北向资金个股流入数据
    """
    code = None
    if symbol:
        code = (
            symbol.replace("sh", "")
            .replace("sz", "")
            .replace(".XSHG", "")
            .replace(".XSHE", "")
            .zfill(6)
        )

    try:
        if code:
            df = get_adapter().get_hsgt_individual_stock_flow(
                stock=code, indicator="北向资金"
            )
        else:
            df = get_adapter().get_hsgt_hsgt_stock_em(indicator="北向资金")
        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "日期": "date",
                    "当日净流入": "net_inflow",
                    "当日资金流入": "inflow",
                    "当日资金流出": "outflow",
                    "持股数量": "holdings",
                    "持股数量变化": "holding_change",
                }
            )
            df["date"] = pd.to_datetime(df["date"])
            if start_date:
                df = df[df["date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["date"] <= pd.to_datetime(end_date)]
            return df.sort_values("date").reset_index(drop=True)
    except Exception as e:
        warnings.warn(f"获取北向资金个股流入失败 {symbol}: {e}")
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
        {'net_inflow': 净流入, 'holdings': 持股数, 'holding_change': 持股变化,
         'link_id': 沪深港通标识, 'link_name': 沪深港通名称}
    """
    code = (
        symbol.replace("sh", "")
        .replace("sz", "")
        .replace(".XSHG", "")
        .replace(".XSHE", "")
        .zfill(6)
    )

    if code.startswith("6"):
        link_id = "sh"
        link_name = "沪股通"
    else:
        link_id = "sz"
        link_name = "深股通"

    df = get_north_money_stock_flow(symbol, end_date=date)

    if df.empty:
        return {
            "net_inflow": 0.0,
            "holdings": 0.0,
            "holding_change": 0.0,
            "link_id": link_id,
            "link_name": link_name,
        }

    latest = df.iloc[-1]
    return {
        "net_inflow": float(latest.get("net_inflow", 0)),
        "holdings": float(latest.get("holdings", 0)),
        "holding_change": float(latest.get("holding_change", 0)),
        "link_id": link_id,
        "link_name": link_name,
    }


def get_north_top_active_stocks(
    date: Optional[str] = None,
    link_id: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取十大成交活跃股数据。

    参数
    ----
    date : str, optional
        查询日期，默认最近交易日
    link_id : str, optional
        'sh' 为沪股通, 'sz' 为深股通, None 为全部

    返回
    ----
    pd.DataFrame
        十大成交活跃股数据，包含:
        code, name, close, change_pct, turnover, north_net_inflow,
        north_holdings, north_holdings_pct, link_id, link_name
    """
    try:
        compat = get_adapter()._get_compat_adapter()
        df = compat.call("stock_hsgt_active_stock_em")
        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "代码": "code",
                    "名称": "name",
                    "收盘价": "close",
                    "涨跌幅": "change_pct",
                    "成交额": "turnover",
                    "北向资金净流入": "north_net_inflow",
                    "北向资金持仓": "north_holdings",
                    "持仓占比": "north_holdings_pct",
                    "类型": "link_id",
                }
            )

            def _map_link(row):
                lid = str(row.get("link_id", "")).lower()
                if "沪" in lid or lid == "sh":
                    return "sh", "沪股通"
                elif "深" in lid or lid == "sz":
                    return "sz", "深股通"
                else:
                    code = str(row.get("code", "")).zfill(6)
                    if code.startswith("6"):
                        return "sh", "沪股通"
                    else:
                        return "sz", "深股通"

            links = df.apply(_map_link, axis=1, result_type="expand")
            df["link_id"] = links[0]
            df["link_name"] = links[1]

            if link_id:
                df = df[df["link_id"] == link_id]

            return df.reset_index(drop=True)
    except Exception as e:
        warnings.warn(f"获取十大成交活跃股失败: {e}")

    return pd.DataFrame()


def get_north_quota_info(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取沪深港通成交与额度信息。

    参数
    ----
    start_date : str, optional
        开始日期 'YYYY-MM-DD'
    end_date : str, optional
        结束日期 'YYYY-MM-DD'

    返回
    ----
    pd.DataFrame
        额度信息数据，包含:
        date, link_id, link_name, daily_quota, used_quota, balance, net_inflow
    """
    results = []
    for lid, lname in [("沪股通", "sh"), ("深股通", "sz")]:
        try:
            compat = get_adapter()._get_compat_adapter()
            df = compat.call("stock_hsgt_hist_em", symbol=lid)
            if df is not None and not df.empty:
                df = df.rename(
                    columns={
                        "日期": "date",
                        "当日额度余额": "balance",
                        "当日已用额度": "used_quota",
                        "当日额度": "daily_quota",
                        "净流入": "net_inflow",
                    }
                )
                df["date"] = pd.to_datetime(df["date"])
                df["link_id"] = lname
                df["link_name"] = lid

                if start_date:
                    df = df[df["date"] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df["date"] <= pd.to_datetime(end_date)]

                results.append(df)
        except Exception as e:
            warnings.warn(f"获取{lname}额度信息失败: {e}")

    if results:
        return (
            pd.concat(results, ignore_index=True)
            .sort_values("date")
            .reset_index(drop=True)
        )
    return pd.DataFrame()


def get_north_exchange_rate(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取北向资金成交汇率数据（港币/人民币）。

    参数
    ----
    start_date : str, optional
        开始日期 'YYYY-MM-DD'
    end_date : str, optional
        结束日期 'YYYY-MM-DD'

    返回
    ----
    pd.DataFrame
        汇率数据，包含:
        date, link_id, exchange_rate, currency
    """
    results = []
    try:
        compat = get_adapter()._get_compat_adapter()
        df = compat.call("currency_boc_sina")
        if df is not None and not df.empty:
            hkd_col = None
            for col in df.columns:
                if "港币" in str(col) or "HKD" in str(col).upper():
                    hkd_col = col
                    break

            if hkd_col is None:
                for col in df.columns:
                    if "日期" in str(col) or "date" in str(col).lower():
                        date_col = col
                        break
                for col in df.columns:
                    if col != date_col:
                        hkd_col = col
                        break

            if hkd_col:
                for col in df.columns:
                    if "日期" in str(col) or "date" in str(col).lower():
                        date_col = col
                        break
                else:
                    date_col = df.columns[0]

                df = df[[date_col, hkd_col]].copy()
                df = df.rename(
                    columns={
                        date_col: "date",
                        hkd_col: "exchange_rate",
                    }
                )
                df["date"] = pd.to_datetime(df["date"])
                df["exchange_rate"] = pd.to_numeric(
                    df["exchange_rate"], errors="coerce"
                )

                if start_date:
                    df = df[df["date"] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df["date"] <= pd.to_datetime(end_date)]

                df = df.dropna(subset=["exchange_rate"])

                for lid in ["sh", "sz"]:
                    tmp = df.copy()
                    tmp["link_id"] = lid
                    tmp["link_name"] = "沪股通" if lid == "sh" else "深股通"
                    tmp["currency"] = "HKD/CNY"
                    results.append(tmp)
    except Exception as e:
        warnings.warn(f"获取汇率数据失败: {e}")

    if results:
        return (
            pd.concat(results, ignore_index=True)
            .sort_values("date")
            .reset_index(drop=True)
        )
    return pd.DataFrame()


def get_north_calendar(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取沪深港通交易日历。

    参数
    ----
    start_date : str, optional
        开始日期 'YYYY-MM-DD'
    end_date : str, optional
        结束日期 'YYYY-MM-DD'

    返回
    ----
    pd.DataFrame
        交易日历数据，包含:
        date, is_trading, link_id, holiday
    """
    from jk2bt.data.market.trade_calendar import get_trade_days

    try:
        if not start_date:
            start_date = (
                datetime.now().replace(year=datetime.now().year - 1)
            ).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        trade_days = get_trade_days(start_date=start_date, end_date=end_date)
        if isinstance(trade_days, pd.DataFrame) and not trade_days.empty:
            date_col = None
            for col in trade_days.columns:
                if "date" in col.lower() or "日期" in col:
                    date_col = col
                    break
            if date_col is None:
                date_col = trade_days.columns[0]
            trade_days = (
                pd.to_datetime(trade_days[date_col]).dt.strftime("%Y-%m-%d").tolist()
            )
        elif isinstance(trade_days, list):
            trade_days = [pd.to_datetime(d).strftime("%Y-%m-%d") for d in trade_days]
        else:
            trade_days = []

        date_range = pd.date_range(start=start_date, end=end_date, freq="D")
        rows = []
        holidays = {
            "01-01": "元旦",
            "01-02": "元旦",
            "02-10": "春节",
            "02-11": "春节",
            "02-12": "春节",
            "02-13": "春节",
            "02-14": "春节",
            "02-15": "春节",
            "02-16": "春节",
            "02-17": "春节",
            "04-04": "清明节",
            "04-05": "清明节",
            "04-06": "清明节",
            "05-01": "劳动节",
            "05-02": "劳动节",
            "05-03": "劳动节",
            "05-04": "劳动节",
            "05-05": "劳动节",
            "06-02": "端午节",
            "06-03": "端午节",
            "06-04": "端午节",
            "09-15": "中秋节",
            "09-16": "中秋节",
            "09-17": "中秋节",
            "10-01": "国庆节",
            "10-02": "国庆节",
            "10-03": "国庆节",
            "10-04": "国庆节",
            "10-05": "国庆节",
            "10-06": "国庆节",
            "10-07": "国庆节",
        }

        for dt in date_range:
            date_str = dt.strftime("%Y-%m-%d")
            md = dt.strftime("%m-%d")
            holiday = holidays.get(md, "")
            is_trading = date_str in trade_days and not holiday

            for lid in ["sh", "sz"]:
                rows.append(
                    {
                        "date": date_str,
                        "is_trading": is_trading,
                        "link_id": lid,
                        "link_name": "沪股通" if lid == "sh" else "深股通",
                        "holiday": holiday,
                    }
                )

        df = pd.DataFrame(rows)
        return df
    except Exception as e:
        warnings.warn(f"获取交易日历失败: {e}")

    return pd.DataFrame()


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
    "get_north_top_active_stocks",
    "get_north_quota_info",
    "get_north_exchange_rate",
    "get_north_calendar",
]
