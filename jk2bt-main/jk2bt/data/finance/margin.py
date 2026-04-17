"""
finance_data/margin.py
融资融券数据获取模块。
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List
import warnings

from jk2bt.utils.symbol import extract_code_num, ak_code_to_jq

from jk2bt.utils.cache import fetch_and_cache_data


def get_margin_data(symbol, date=None, force_update=False):
    """
    获取单个股票的融资融券数据。

    参数
    ----
    symbol     : 股票代码，支持 '600519.XSHG', '000001.XSHE', 'sh600519', 'sz000001', '600519' 等格式
    date       : 查询日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'，默认最近交易日
    force_update: True 时强制重新下载

    返回
    ----
    pandas DataFrame，标准化字段：
    - code: 股票代码（聚宽格式）
    - date: 交易日期
    - margin_balance: 融资余额
    - margin_buy: 融资买入额
    - margin_repay: 融资偿还额
    - short_balance_volume: 融券余量
    - short_sell_volume: 融券卖出量
    - short_repay_volume: 融券偿还量
    - short_balance_amount: 融券余额（可选）
    - total_balance: 融资融券余额合计（可选）
    """
    code_num = extract_code_num(symbol)
    market = _get_market(symbol)

    if date is None:
        return _get_margin_auto_date(symbol, code_num, market, force_update)
    else:
        date = _normalize_date(date)
        return _get_margin_by_date(symbol, code_num, market, date, force_update)


def _get_margin_auto_date(symbol, code_num, market, force_update):
    """自动查找最近可用日期的融资融券数据"""
    max_days_back = 60
    today = datetime.now()

    for i in range(max_days_back):
        check_date = today - timedelta(days=i)
        if check_date.weekday() >= 5:
            continue

        date_str = check_date.strftime("%Y%m%d")

        try:
            df = _get_margin_by_date(symbol, code_num, market, date_str, force_update)
            if not df.empty:
                return df
        except Exception:
            pass

    return pd.DataFrame()


def _get_margin_by_date(symbol, code_num, market, date, force_update):
    """获取指定日期的融资融券数据"""
    from jk2bt.data.sources import get_adapter

    try:
        if market == "sh":
            df_all = get_adapter().get_margin_detail(market="sh", date=date)
        else:
            df_all = get_adapter().get_margin_detail(market="sz", date=date)

        if df_all is not None and not df_all.empty:
            df = _filter_and_normalize(df_all, code_num, market, symbol)
            return df
    except Exception as e:
        print(f"[margin] 下载失败 {date}: {e}")

    return pd.DataFrame()


def _get_market(symbol):
    """判断市场：sh 或 sz"""
    if "XSHG" in symbol or symbol.startswith("6") or symbol.startswith("sh"):
        return "sh"
    return "sz"


def _normalize_date(date_str):
    """标准化日期为 YYYYMMDD"""
    if "-" in date_str:
        return date_str.replace("-", "")
    return date_str


def _find_latest_trading_day(market, max_days_back=30):
    """查找最近的融资融券数据可用日期"""
    today = datetime.now()
    for i in range(max_days_back):
        check_date = today - timedelta(days=i)
        date_str = check_date.strftime("%Y%m%d")
        if check_date.weekday() < 5:
            return date_str
    return today.strftime("%Y%m%d")


def _filter_and_normalize(df_all, code_num, market, original_symbol):
    """筛选并标准化数据"""
    if market == "sh":
        code_col = "标的证券代码"
        date_col = "信用交易日期"
    else:
        code_col = "证券代码"
        date_col = None

    df_filtered = df_all[df_all[code_col] == code_num]

    if df_filtered.empty:
        return pd.DataFrame()

    result = pd.DataFrame()
    result["code"] = [ak_code_to_jq(original_symbol)]

    if market == "sh":
        row = df_filtered.iloc[0]
        result["date"] = [row["信用交易日期"]]
        result["margin_balance"] = [row["融资余额"]]
        result["margin_buy"] = [row["融资买入额"]]
        result["margin_repay"] = [row["融资偿还额"]]
        result["short_balance_volume"] = [row["融券余量"]]
        result["short_sell_volume"] = [row["融券卖出量"]]
        result["short_repay_volume"] = [row["融券偿还量"]]
    else:
        row = df_filtered.iloc[0]
        result["date"] = [pd.Timestamp.now().strftime("%Y%m%d")]
        result["margin_balance"] = [row["融资余额"]]
        result["margin_buy"] = [row["融资买入额"]]
        result["short_balance_volume"] = [row["融券余量"]]
        result["short_sell_volume"] = [row["融券卖出量"]]
        result["short_balance_amount"] = [row.get("融券余额", None)]
        result["total_balance"] = [row.get("融资融券余额", None)]

    return result


def get_margin_history(symbol, start_date, end_date, force_update=False):
    """
    获取融资融券历史数据（多个交易日）。

    参数
    ----
    symbol     : 股票代码
    start_date : 起始日期 'YYYY-MM-DD'
    end_date   : 结束日期 'YYYY-MM-DD'
    force_update: 强制更新

    返回
    ----
    DataFrame，每个交易日一条记录
    """
    market = _get_market(symbol)
    code_num = extract_code_num(symbol)

    start_dt = datetime.strptime(start_date.replace("-", ""), "%Y%m%d")
    end_dt = datetime.strptime(end_date.replace("-", ""), "%Y%m%d")

    dfs = []
    current_dt = start_dt

    while current_dt <= end_dt:
        if current_dt.weekday() < 5:
            date_str = current_dt.strftime("%Y%m%d")
            try:
                df = get_margin_data(symbol, date=date_str, force_update=force_update)
                if not df.empty:
                    dfs.append(df)
            except Exception:
                pass
        current_dt += timedelta(days=1)

    if not dfs:
        return pd.DataFrame()

    result = pd.concat(dfs, ignore_index=True)
    return result


def get_short_selling_underlying(date: Optional[str] = None) -> List[str]:
    """
    获取可融券标的列表。

    参数
    ----
    date : str, optional
        查询日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'，默认最近交易日

    返回
    ----
    List[str]
        可融券标的股票代码列表（聚宽格式）

    说明
    ----
    优先从交易所获取专门的融券标的列表，如果不可用则从融资融券数据中
    筛选有融券活动（融券余量 > 0）的股票作为可融券标的。
    """
    from jk2bt.data.sources import get_adapter

    stocks = []

    try:
        if date is not None:
            date_str = _normalize_date(date)
        else:
            date_str = _find_latest_trading_day("sh")

        # 尝试从上交所获取融券标的
        try:
            df_sh = get_adapter().get_margin_detail("sh", date_str)
            if df_sh is not None and not df_sh.empty:
                code_col = "标的证券代码"
                short_col = "融券余量"
                if code_col in df_sh.columns and short_col in df_sh.columns:
                    df_active = df_sh[df_sh[short_col] > 0]
                    for code in df_active[code_col]:
                        code_str = str(code).zfill(6)
                        if code_str.startswith("6"):
                            stocks.append(f"{code_str}.XSHG")
        except Exception:
            pass

        # 尝试从深交所获取融券标的
        try:
            df_sz = get_adapter().get_margin_detail("sz", date_str)
            if df_sz is not None and not df_sz.empty:
                code_col = "证券代码"
                short_col = "融券余量"
                if code_col in df_sz.columns and short_col in df_sz.columns:
                    df_active = df_sz[df_sz[short_col] > 0]
                    for code in df_active[code_col]:
                        code_str = str(code).zfill(6)
                        if code_str.startswith(("0", "3")):
                            stocks.append(f"{code_str}.XSHE")
        except Exception:
            pass

    except Exception as e:
        warnings.warn(f"获取可融券标的列表失败: {e}")

    return list(set(stocks))


# 向后兼容导出
from jk2bt.utils.symbol import extract_code_num as _extract_code_num
from jk2bt.utils.symbol import ak_code_to_jq as _normalize_to_jq
