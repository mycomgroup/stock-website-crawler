"""
jk2bt/api/concept.py
概念板块 API 模块

提供 JQData 兼容的概念板块查询接口。
数据源: AkShare

主要功能:
- get_concepts: 获取概念板块列表
- get_concept_stocks: 获取概念板块成分股
- get_concept: 获取股票所属概念
"""

import pandas as pd
from typing import Optional, List, Union
import warnings


def get_concepts(
    date: Optional[str] = None,
    df: bool = True,
) -> Union[pd.DataFrame, dict]:
    """
    获取概念板块列表。

    聚宽兼容接口

    参数
    ----
    date : str, optional
        查询日期，格式 'YYYY-MM-DD'，默认当前日期
    df : bool, default True
        True 返回 DataFrame，False 返回 dict

    返回
    ----
    pd.DataFrame or dict
        概念板块列表:
        - code: 概念板块代码
        - name: 概念板块名称

    示例
    ----
    >>> concepts = get_concepts()
    >>> print(concepts.head())
    >>> concepts_dict = get_concepts(df=False)
    """
    from jk2bt.market_data.concept import get_concept_list

    result = get_concept_list(date=date)

    if not df and not result.empty:
        return result.set_index("code")["name"].to_dict()

    return result


def get_concept_stocks(
    concept: str,
    date: Optional[str] = None,
) -> List[str]:
    """
    获取概念板块成分股。

    聚宽兼容接口

    参数
    ----
    concept : str
        概念板块代码或名称
    date : str, optional
        查询日期，格式 'YYYY-MM-DD'

    返回
    ----
    List[str]
        股票代码列表（聚宽格式）

    示例
    ----
    >>> stocks = get_concept_stocks('人工智能')
    >>> print(stocks[:5])
    ['300750.XSHE', '002230.XSHE', '000977.XSHE', ...]
    """
    from jk2bt.market_data.concept import get_concept_stocks as _get_concept_stocks

    return _get_concept_stocks(concept_code=concept, date=date)


def get_concept(
    security: str,
    date: Optional[str] = None,
) -> List[str]:
    """
    获取股票所属概念。

    聚宽兼容接口

    参数
    ----
    security : str
        股票代码，支持多种格式:
        - '000001.XSHE' (聚宽格式)
        - '600519.XSHG' (聚宽格式)
        - 'sh600519' (akshare 格式)
        - '600519' (纯代码)
    date : str, optional
        查询日期

    返回
    ----
    List[str]
        概念板块名称列表

    示例
    ----
    >>> concepts = get_concept('300750.XSHE')
    >>> print(concepts)
    ['锂电池', '新能源汽车', '储能', ...]
    """
    from jk2bt.market_data.concept import get_stock_concepts

    return get_stock_concepts(security=security, date=date)


def get_all_concepts(
    date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取所有概念板块及成分股。

    参数
    ----
    date : str, optional
        查询日期

    返回
    ----
    pd.DataFrame
        概念板块和成分股的映射表:
        - concept_code: 概念代码
        - concept_name: 概念名称
        - stock_code: 股票代码
    """
    from jk2bt.market_data.concept import get_concept_list, get_concept_stocks

    concepts = get_concept_list(date=date)

    if concepts.empty:
        return pd.DataFrame(columns=["concept_code", "concept_name", "stock_code"])

    results = []
    for _, row in concepts.iterrows():
        concept_code = row.get("code", "")
        concept_name = row.get("name", "")

        if concept_code:
            stocks = get_concept_stocks(concept_code, date)
            for stock in stocks:
                results.append({
                    "concept_code": concept_code,
                    "concept_name": concept_name,
                    "stock_code": stock,
                })

    return pd.DataFrame(results)


# 聚宽风格别名
get_concepts_jq = get_concepts
get_concept_stocks_jq = get_concept_stocks
get_concept_jq = get_concept


__all__ = [
    "get_concepts",
    "get_concept_stocks",
    "get_concept",
    "get_all_concepts",
    "get_concepts_jq",
    "get_concept_stocks_jq",
    "get_concept_jq",
]