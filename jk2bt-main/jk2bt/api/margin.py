"""
jk2bt/api/margin.py
融资融券 API 模块

提供 JQData 兼容的融资融券查询接口。
数据源: AkShare (上交所/深交所)

主要功能:
- get_mtss: 获取融资融券数据
- get_margincash_stocks: 获取可融资标的列表
- get_marginsec_stocks: 获取可融券标的列表
"""

import pandas as pd
from typing import Optional, List, Union
import warnings
from datetime import datetime, timedelta


def get_mtss(
    security: Optional[Union[str, List[str]]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    fields: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    获取融资融券数据。

    聚宽兼容接口

    参数
    ----
    security : str or list of str, optional
        股票代码或股票列表，支持多种格式:
        - '000001.XSHE' (聚宽格式)
        - '600519.XSHG' (聚宽格式)
        - 'sh600519' (akshare 格式)
        - '600519' (纯代码)
        None 表示获取全市场数据
    start_date : str, optional
        开始日期，格式 'YYYY-MM-DD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD'
    count : int, optional
        返回最近N天的数据（与 start_date 互斥）
    fields : list of str, optional
        返回字段列表，默认返回全部字段

    返回
    ----
    pd.DataFrame
        融资融券数据:
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

    示例
    ----
    >>> df = get_mtss('600519.XSHG', start_date='2024-01-01', end_date='2024-01-31')
    >>> df = get_mtss(['600519.XSHG', '000858.XSHE'], count=5)
    """
    from jk2bt.finance_data.margin import get_margin_data, get_margin_history

    # 参数校验
    if start_date and count:
        raise ValueError("start_date 和 count 不能同时使用")

    # 标准化股票代码
    if security is None:
        securities = None
    elif isinstance(security, str):
        securities = [security]
    else:
        securities = list(security)

    # 处理 count 参数
    if count and not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    if count:
        start_date_dt = datetime.now() - timedelta(days=count * 2)  # 预留非交易日
        start_date = start_date_dt.strftime("%Y-%m-%d")

    # 获取数据
    if securities:
        results = []
        for sec in securities:
            if start_date and end_date:
                df = get_margin_history(sec, start_date, end_date)
            else:
                df = get_margin_data(sec, date=end_date)

            if not df.empty:
                results.append(df)

        if not results:
            return _get_empty_mtss_frame()

        result = pd.concat(results, ignore_index=True)
    else:
        # 全市场数据
        result = _get_market_mtss(start_date, end_date)

    # 字段筛选
    if fields and not result.empty:
        available_fields = [f for f in fields if f in result.columns]
        if "code" not in available_fields:
            available_fields = ["code"] + available_fields
        if "date" not in available_fields:
            available_fields = ["date"] + available_fields
        result = result[available_fields]

    return result


def _get_empty_mtss_frame() -> pd.DataFrame:
    """返回空的融资融券 DataFrame"""
    return pd.DataFrame(columns=[
        "code", "date", "margin_balance", "margin_buy", "margin_repay",
        "short_balance_volume", "short_sell_volume", "short_repay_volume"
    ])


def _get_market_mtss(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """获取全市场融资融券数据"""
    try:
        import akshare as ak
    except ImportError:
        warnings.warn("akshare 未安装")
        return _get_empty_mtss_frame()

    results = []

    try:
        # 获取上海证券交易所数据
        if end_date:
            date_str = end_date.replace("-", "")
        else:
            date_str = datetime.now().strftime("%Y%m%d")

        # 上交所
        try:
            df_sh = ak.stock_margin_detail_sse(date=date_str)
            if df_sh is not None and not df_sh.empty:
                df_sh = _normalize_sse_margin(df_sh)
                results.append(df_sh)
        except Exception:
            pass

        # 深交所
        try:
            df_sz = ak.stock_margin_detail_szse(date=date_str)
            if df_sz is not None and not df_sz.empty:
                df_sz = _normalize_szse_margin(df_sz)
                results.append(df_sz)
        except Exception:
            pass

    except Exception as e:
        warnings.warn(f"获取全市场融资融券数据失败: {e}")

    if not results:
        return _get_empty_mtss_frame()

    return pd.concat(results, ignore_index=True)


def _normalize_sse_margin(df: pd.DataFrame) -> pd.DataFrame:
    """标准化上交所融资融券数据"""
    result = pd.DataFrame()

    # 查找代码列
    code_col = None
    for col in ["标的证券代码", "证券代码", "代码"]:
        if col in df.columns:
            code_col = col
            break

    if code_col:
        result["code"] = df[code_col].apply(lambda x: f"{str(x).zfill(6)}.XSHG")

    # 标准化其他字段
    column_mapping = {
        "信用交易日期": "date",
        "融资余额": "margin_balance",
        "融资买入额": "margin_buy",
        "融资偿还额": "margin_repay",
        "融券余量": "short_balance_volume",
        "融券卖出量": "short_sell_volume",
        "融券偿还量": "short_repay_volume",
    }

    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            result[new_col] = df[old_col]

    return result


def _normalize_szse_margin(df: pd.DataFrame) -> pd.DataFrame:
    """标准化深交所融资融券数据"""
    result = pd.DataFrame()

    # 查找代码列
    code_col = None
    for col in ["证券代码", "代码"]:
        if col in df.columns:
            code_col = col
            break

    if code_col:
        result["code"] = df[code_col].apply(lambda x: f"{str(x).zfill(6)}.XSHE")

    # 标准化其他字段
    column_mapping = {
        "融资余额": "margin_balance",
        "融资买入额": "margin_buy",
        "融券余量": "short_balance_volume",
        "融券卖出量": "short_sell_volume",
    }

    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            result[new_col] = df[old_col]

    # 设置日期
    result["date"] = pd.Timestamp.now().strftime("%Y-%m-%d")

    return result


def get_margincash_stocks(
    date: Optional[str] = None,
) -> List[str]:
    """
    获取可融资标的列表。

    聚宽兼容接口

    参数
    ----
    date : str, optional
        查询日期，格式 'YYYY-MM-DD'

    返回
    ----
    List[str]
        可融资标的股票代码列表（聚宽格式）

    示例
    ----
    >>> stocks = get_margincash_stocks()
    >>> print(len(stocks))
    1000
    """
    try:
        import akshare as ak
    except ImportError:
        warnings.warn("akshare 未安装")
        return []

    stocks = []

    try:
        # 上交所融资标的
        try:
            df_sh = ak.stock_margin_underlying_info_sse(date=date.replace("-", "") if date else None)
            if df_sh is not None and not df_sh.empty:
                code_col = None
                for col in ["证券代码", "代码", "标的代码"]:
                    if col in df_sh.columns:
                        code_col = col
                        break
                if code_col:
                    for code in df_sh[code_col]:
                        code_str = str(code).zfill(6)
                        if code_str.startswith("6"):
                            stocks.append(f"{code_str}.XSHG")
        except Exception:
            pass

        # 深交所融资标的
        try:
            df_sz = ak.stock_margin_underlying_info_szse(date=date.replace("-", "") if date else None)
            if df_sz is not None and not df_sz.empty:
                code_col = None
                for col in ["证券代码", "代码", "标的代码"]:
                    if col in df_sz.columns:
                        code_col = col
                        break
                if code_col:
                    for code in df_sz[code_col]:
                        code_str = str(code).zfill(6)
                        if code_str.startswith(("0", "3")):
                            stocks.append(f"{code_str}.XSHE")
        except Exception:
            pass

    except Exception as e:
        warnings.warn(f"获取可融资标的列表失败: {e}")

    return list(set(stocks))


def get_marginsec_stocks(
    date: Optional[str] = None,
) -> List[str]:
    """
    获取可融券标的列表。

    聚宽兼容接口

    参数
    ----
    date : str, optional
        查询日期，格式 'YYYY-MM-DD'

    返回
    ----
    List[str]
        可融券标的股票代码列表（聚宽格式）

    示例
    ----
    >>> stocks = get_marginsec_stocks()
    >>> print(len(stocks))
    800
    """
    # 可融券标的通常与可融资标的有较大重叠
    # 使用相同的接口
    return get_margincash_stocks(date)


# 聚宽风格别名
get_mtss_jq = get_mtss


__all__ = [
    "get_mtss",
    "get_margincash_stocks",
    "get_marginsec_stocks",
    "get_mtss_jq",
]