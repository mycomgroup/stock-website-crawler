"""
jk2bt/api/concept.py
概念板块 API 模块

提供 JQData 兼容的概念板块查询接口。
数据源: AkShare

主要功能:
- get_concepts: 获取概念板块列表
- get_concept_stocks: 获取概念板块成分股
- get_concept: 获取股票所属概念
- get_industry_classify: 获取行业分类（1/2/3级）
"""

import pandas as pd
from typing import Optional, List, Union


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
        - start_date: 板块起始日期（如有）

    示例
    ----
    >>> concepts = get_concepts()
    >>> print(concepts.head())
    >>> concepts_dict = get_concepts(df=False)
    """
    from jk2bt.data.market.concept import get_concept_list

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
    from jk2bt.data.market.concept import get_concept_stocks as _get_concept_stocks

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
    from jk2bt.data.market.concept import get_stock_concepts

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
    from jk2bt.data.market.concept import get_concept_list, get_concept_stocks

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
                results.append(
                    {
                        "concept_code": concept_code,
                        "concept_name": concept_name,
                        "stock_code": stock,
                    }
                )

    return pd.DataFrame(results)


def get_industry_classify(
    level: Optional[int] = 1,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取行业分类（申万行业分类）。

    聚宽兼容接口

    参数
    ----
    level : int, optional
        行业分类级别，1/2/3 分别对应一级/二级/三级行业，默认1
    date : str, optional
        查询日期，格式 'YYYY-MM-DD'

    返回
    ----
    pd.DataFrame
        行业分类列表:
        - code: 行业代码
        - name: 行业名称
        - level: 行业级别
        - parent_code: 父级行业代码（2/3级时有值）

    示例
    ----
    >>> industries = get_industry_classify(level=1)
    >>> print(industries.head())
    >>> industries_l2 = get_industry_classify(level=2)
    """
    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_sw_industry(level=str(level))
        if df is not None and not df.empty:
            result = pd.DataFrame()
            result["code"] = df.get("行业代码", df.get("代码", ""))
            result["name"] = df.get("行业名称", df.get("名称", ""))
            result["level"] = level

            # For level 2/3, try to get parent_code from the data
            if level == 2:
                # Try to get level 1 industries as parent
                try:
                    l1_df = get_adapter().get_sw_industry(level="1")
                    if l1_df is not None and not l1_df.empty:
                        l1_codes = set(
                            l1_df.get("行业代码", l1_df.get("代码", [])).tolist()
                            if hasattr(
                                l1_df.get("行业代码", l1_df.get("代码", [])), "tolist"
                            )
                            else []
                        )
                        # For level 2, parent_code is typically the first 2-3 digits of the code
                        result["parent_code"] = result["code"].apply(
                            lambda x: str(x)[:3] if len(str(x)) >= 3 else None
                        )
                    else:
                        result["parent_code"] = None
                except Exception:
                    result["parent_code"] = None
            elif level == 3:
                # For level 3, parent_code is typically the level 2 code (first 4-5 digits)
                result["parent_code"] = result["code"].apply(
                    lambda x: str(x)[:4] if len(str(x)) >= 4 else None
                )
            else:
                result["parent_code"] = None
            return result
    except Exception as e:
        import warnings

        warnings.warn(f"获取行业分类失败 (level={level}): {e}")

    return pd.DataFrame(columns=["code", "name", "level", "parent_code"])


def get_stock_industry(
    security: str,
    date: Optional[str] = None,
    industry_type: str = "sw_l1",
) -> pd.DataFrame:
    """
    获取股票所属行业（专有接口）。

    聚宽兼容接口

    参数
    ----
    security : str
        股票代码，支持多种格式
    date : str, optional
        查询日期
    industry_type : str, default 'sw_l1'
        行业分类标准: 'sw_l1', 'sw_l2', 'sw_l3', 'zjw' (证监会)

    返回
    ----
    pd.DataFrame
        股票所属行业信息:
        - code: 股票代码
        - industry_code: 行业代码
        - industry_name: 行业名称
        - industry_type: 行业分类标准
        - pub_date: 发布日期

    示例
    ----
    >>> df = get_stock_industry('600519.XSHG')
    >>> print(df)
    """
    from jk2bt.data.sources import get_adapter

    code = security.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

    try:
        df = get_adapter().get_stock_industry(industry_type=industry_type, code=code)
        if df is not None and not df.empty:
            result = pd.DataFrame()
            result["code"] = [security] * len(df)

            col_map = {
                "行业代码": "industry_code",
                "行业名称": "industry_name",
                "行业分类": "industry_type",
                "发布日期": "pub_date",
                "纳入日期": "pub_date",
            }
            for src, target in col_map.items():
                if src in df.columns:
                    result[target] = df[src]

            if "industry_code" not in result.columns:
                result["industry_code"] = df.iloc[:, 0] if len(df.columns) > 0 else None
            if "industry_name" not in result.columns:
                result["industry_name"] = df.iloc[:, 1] if len(df.columns) > 1 else None
            if "industry_type" not in result.columns:
                result["industry_type"] = industry_type
            if "pub_date" not in result.columns:
                result["pub_date"] = date

            return result
    except Exception as e:
        import warnings

        warnings.warn(f"获取股票行业信息失败 {security}: {e}")

    return pd.DataFrame(
        columns=["code", "industry_code", "industry_name", "industry_type", "pub_date"]
    )


# 聚宽风格别名
get_concepts_jq = get_concepts
get_concept_stocks_jq = get_concept_stocks
get_concept_jq = get_concept
get_industry_classify_jq = get_industry_classify


__all__ = [
    "get_concepts",
    "get_concept_stocks",
    "get_concept",
    "get_all_concepts",
    "get_industry_classify",
    "get_stock_industry",
    "get_concepts_jq",
    "get_concept_stocks_jq",
    "get_concept_jq",
    "get_industry_classify_jq",
]
