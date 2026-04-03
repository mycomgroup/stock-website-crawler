"""
finance_data/margin.py
融资融券数据获取模块。
"""

import os
import pandas as pd
from datetime import datetime, timedelta

try:
    from ..utils.cache import fetch_and_cache_data
except ImportError:
    from utils.cache import fetch_and_cache_data


def get_margin_data(symbol, date=None, cache_dir="finance_cache", force_update=False):
    """
    获取单个股票的融资融券数据。

    参数
    ----
    symbol     : 股票代码，支持 '600519.XSHG', '000001.XSHE', 'sh600519', 'sz000001', '600519' 等格式
    date       : 查询日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'，默认最近交易日
    cache_dir  : 缓存目录
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
    code_num = _extract_code_num(symbol)
    market = _get_market(symbol)

    if date is None:
        return _get_margin_auto_date(symbol, code_num, market, cache_dir, force_update)
    else:
        date = _normalize_date(date)
        return _get_margin_by_date(
            symbol, code_num, market, date, cache_dir, force_update
        )


def _get_margin_auto_date(symbol, code_num, market, cache_dir, force_update):
    """自动查找最近可用日期的融资融券数据"""
    max_days_back = 60
    today = datetime.now()

    for i in range(max_days_back):
        check_date = today - timedelta(days=i)
        if check_date.weekday() >= 5:
            continue

        date_str = check_date.strftime("%Y%m%d")

        try:
            df = _get_margin_by_date(
                symbol, code_num, market, date_str, cache_dir, force_update
            )
            if not df.empty:
                return df
        except Exception:
            pass

    return pd.DataFrame()


def _get_margin_by_date(symbol, code_num, market, date, cache_dir, force_update):
    """获取指定日期的融资融券数据"""
    cache_file = os.path.join(cache_dir, f"margin_{market}_{date}.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            df_all = pd.read_pickle(cache_file)
        except Exception:
            need_download = True

    if need_download:
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        try:
            if market == "sh":
                df_all = ak.stock_margin_detail_sse(date=date)
            else:
                df_all = ak.stock_margin_detail_szse(date=date)

            if df_all is not None and not df_all.empty:
                df_all.to_pickle(cache_file)
        except Exception as e:
            print(f"[margin] 下载失败 {date}: {e}")
            return pd.DataFrame()

    if df_all is None or df_all.empty:
        return pd.DataFrame()

    df = _filter_and_normalize(df_all, code_num, market, symbol)
    return df


def _extract_code_num(symbol):
    """提取6位代码数字"""
    if symbol.startswith("sh") or symbol.startswith("sz"):
        return symbol[2:].zfill(6)
    if ".XSHG" in symbol or ".XSHE" in symbol:
        return symbol.split(".")[0].zfill(6)
    return symbol.zfill(6)


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
    result["code"] = [_normalize_to_jq(original_symbol)]

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


def _normalize_to_jq(symbol):
    """转换为聚宽格式"""
    if ".XSHG" in symbol or ".XSHE" in symbol:
        return symbol
    if symbol.startswith("sh"):
        return symbol[2:] + ".XSHG"
    if symbol.startswith("sz"):
        return symbol[2:] + ".XSHE"
    code = symbol.zfill(6)
    if code.startswith("6"):
        return code + ".XSHG"
    return code + ".XSHE"


def get_margin_history(
    symbol, start_date, end_date, cache_dir="finance_cache", force_update=False
):
    """
    获取融资融券历史数据（多个交易日）。

    参数
    ----
    symbol     : 股票代码
    start_date : 起始日期 'YYYY-MM-DD'
    end_date   : 结束日期 'YYYY-MM-DD'
    cache_dir  : 缓存目录
    force_update: 强制更新

    返回
    ----
    DataFrame，每个交易日一条记录
    """
    market = _get_market(symbol)
    code_num = _extract_code_num(symbol)

    start_dt = datetime.strptime(start_date.replace("-", ""), "%Y%m%d")
    end_dt = datetime.strptime(end_date.replace("-", ""), "%Y%m%d")

    dfs = []
    current_dt = start_dt

    while current_dt <= end_dt:
        if current_dt.weekday() < 5:
            date_str = current_dt.strftime("%Y%m%d")
            try:
                df = get_margin_data(
                    symbol,
                    date=date_str,
                    cache_dir=cache_dir,
                    force_update=force_update,
                )
                if not df.empty:
                    dfs.append(df)
            except Exception:
                pass
        current_dt += timedelta(days=1)

    if not dfs:
        return pd.DataFrame()

    result = pd.concat(dfs, ignore_index=True)
    return result
