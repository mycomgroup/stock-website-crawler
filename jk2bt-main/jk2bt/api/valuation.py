"""
jk2bt/api/valuation.py
估值数据 API 模块

提供指数估值数据查询接口。
数据源: AkShare

主要功能:
- get_index_valuation: 获取指数估值数据
"""

import pandas as pd
from typing import Optional, List, Union
import warnings


def get_index_valuation(
    index_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fields: Optional[List[str]] = None,
    count: Optional[int] = None,
) -> pd.DataFrame:
    """
    获取指数估值数据。

    聚宽兼容接口

    参数
    ----
    index_code : str
        指数代码，支持多种格式:
        - '000300.XSHG' (聚宽格式)
        - '000300' (纯代码)
        - 'sh000300' (akshare 格式)
    start_date : str, optional
        开始日期，格式 'YYYY-MM-DD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD'
    fields : list of str, optional
        返回字段列表，默认返回全部字段
        可选字段: ['pe', 'pb', 'roe', 'dividend_yield', 'market_cap']
    count : int, optional
        返回最近N天的数据

    返回
    ----
    pd.DataFrame
        指数估值数据:
        - code: 指数代码
        - date: 日期
        - pe: 市盈率
        - pb: 市净率
        - roe: 净资产收益率
        - dividend_yield: 股息率
        - market_cap: 总市值

    示例
    ----
    >>> df = get_index_valuation('000300.XSHG', start_date='2024-01-01', end_date='2024-01-31')
    >>> print(df.head())
    """
    try:
        import akshare as ak
    except ImportError:
        warnings.warn("akshare 未安装")
        return _get_empty_valuation_frame()

    # 标准化指数代码
    code = _normalize_index_code(index_code)

    try:
        # 使用指数估值接口
        df = ak.index_value_hist_fina(symbol=code)

        if df is not None and not df.empty:
            # 标准化列名
            column_mapping = {
                "日期": "date",
                "市盈率": "pe",
                "市净率": "pb",
                "股息率": "dividend_yield",
                "收益率": "dividend_yield",
            }
            df = df.rename(columns=column_mapping)

            # 添加代码列
            df["code"] = index_code

            # 处理日期
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])

                # 过滤日期范围
                if start_date:
                    df = df[df["date"] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df["date"] <= pd.to_datetime(end_date)]

                if count:
                    df = df.tail(count)

            # 字段筛选
            if fields:
                available_fields = ["code", "date"] + [f for f in fields if f in df.columns]
                df = df[available_fields]

            return df.reset_index(drop=True)

    except Exception as e:
        warnings.warn(f"获取指数估值数据失败 {index_code}: {e}")

    # 尝试备用接口
    return _get_valuation_from_backup(index_code, start_date, end_date)


def _normalize_index_code(index_code: str) -> str:
    """标准化指数代码"""
    code = (
        index_code.replace(".XSHG", "")
        .replace(".XSHE", "")
        .replace("sh", "")
        .replace("sz", "")
    )
    return code.zfill(6)


def _get_valuation_from_backup(
    index_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """备用方法获取估值数据"""
    try:
        import akshare as ak

        code = _normalize_index_code(index_code)

        # 尝试从指数行情计算
        df = ak.stock_zh_index_daily(symbol=f"sh{code}")

        if df is not None and not df.empty:
            # 使用收盘价作为估值的代理变量
            result = pd.DataFrame()
            result["date"] = pd.to_datetime(df["date"])
            result["code"] = index_code
            result["close"] = df["close"]

            # 过滤日期
            if start_date:
                result = result[result["date"] >= pd.to_datetime(start_date)]
            if end_date:
                result = result[result["date"] <= pd.to_datetime(end_date)]

            return result.reset_index(drop=True)

    except Exception:
        pass

    return _get_empty_valuation_frame()


def _get_empty_valuation_frame() -> pd.DataFrame:
    """返回空的估值 DataFrame"""
    return pd.DataFrame(columns=["code", "date", "pe", "pb", "dividend_yield"])


def get_valuation(
    security: Union[str, List[str]],
    date: Optional[str] = None,
    fields: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    获取股票/指数估值数据。

    聚宽兼容接口

    参数
    ----
    security : str or list of str
        股票/指数代码
    date : str, optional
        查询日期
    fields : list of str, optional
        返回字段

    返回
    ----
    pd.DataFrame
        估值数据
    """
    if isinstance(security, str):
        securities = [security]
    else:
        securities = list(security)

    results = []
    for sec in securities:
        # 判断是指数还是股票
        if _is_index(sec):
            df = get_index_valuation(sec, start_date=date, end_date=date)
        else:
            df = _get_stock_valuation(sec, date, fields)

        if not df.empty:
            results.append(df)

    if not results:
        return pd.DataFrame()

    return pd.concat(results, ignore_index=True)


def _is_index(code: str) -> bool:
    """判断是否为指数"""
    clean_code = code.replace(".XSHG", "").replace(".XSHE", "").replace("sh", "").replace("sz", "")
    # 指数代码通常以 000, 399, 930 开头
    return clean_code.startswith(("000", "399", "930"))


def _get_stock_valuation(
    security: str,
    date: Optional[str] = None,
    fields: Optional[List[str]] = None,
) -> pd.DataFrame:
    """获取股票估值数据"""
    try:
        import akshare as ak

        code = security.replace(".XSHG", "").replace(".XSHE", "").replace("sh", "").replace("sz", "")

        # 使用个股估值接口
        df = ak.stock_a_lg_indicator(symbol=code)

        if df is not None and not df.empty:
            result = pd.DataFrame()
            result["code"] = [security]
            result["date"] = [date or df.iloc[-1].get("日期", "")]

            # 提取估值字段
            if "市盈率" in df.columns:
                result["pe"] = [df.iloc[-1].get("市盈率", 0)]
            if "市净率" in df.columns:
                result["pb"] = [df.iloc[-1].get("市净率", 0)]

            return result

    except Exception:
        pass

    return pd.DataFrame()


# 聚宽风格别名
get_index_valuation_jq = get_index_valuation


__all__ = [
    "get_index_valuation",
    "get_valuation",
    "get_index_valuation_jq",
]