"""
jk2bt/market_data/concept.py
概念板块数据模块

使用 AkShare 获取概念板块相关数据。

功能:
- 概念板块列表
- 概念板块成分股
- 股票所属概念
"""

import warnings
from typing import Optional, List, Dict
import pandas as pd
from datetime import datetime

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    warnings.warn("akshare未安装，概念板块数据将不可用")


# 概念板块数据缓存
_concept_cache: Dict[str, pd.DataFrame] = {}
_concept_stocks_cache: Dict[str, List[str]] = {}


def get_concept_list(
    date: Optional[str] = None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    获取概念板块列表。

    参数
    ----
    date : str, optional
        查询日期，默认当前日期
    use_cache : bool, default True
        是否使用缓存

    返回
    ----
    pd.DataFrame
        概念板块列表，包含:
        - code: 概念板块代码
        - name: 概念板块名称
        - change_pct: 涨跌幅（可选）
        - reason: 板块原因（可选）
    """
    if not AKSHARE_AVAILABLE:
        return pd.DataFrame(columns=["code", "name"])

    cache_key = f"concepts_{date or 'latest'}"
    if use_cache and cache_key in _concept_cache:
        return _concept_cache[cache_key].copy()

    try:
        # 使用东方财富概念板块接口
        df = ak.board_concept_name_em()

        if df is not None and not df.empty:
            # 标准化列名
            column_mapping = {
                "板块代码": "code",
                "板块名称": "name",
                "涨跌幅": "change_pct",
                "总市值": "total_market_cap",
                "换手率": "turnover_rate",
            }
            df = df.rename(columns=column_mapping)

            # 确保必要列存在
            if "code" not in df.columns and "板块代码" in df.columns:
                df["code"] = df["板块代码"]
            if "name" not in df.columns and "板块名称" in df.columns:
                df["name"] = df["板块名称"]

            result = df[["code", "name"]].copy()

            if use_cache:
                _concept_cache[cache_key] = result

            return result

    except Exception as e:
        warnings.warn(f"获取概念板块列表失败: {e}")

    return pd.DataFrame(columns=["code", "name"])


def get_concept_stocks(
    concept_code: str,
    date: Optional[str] = None,
    use_cache: bool = True,
) -> List[str]:
    """
    获取概念板块成分股。

    参数
    ----
    concept_code : str
        概念板块代码或名称
    date : str, optional
        查询日期
    use_cache : bool, default True
        是否使用缓存

    返回
    ----
    List[str]
        股票代码列表（聚宽格式: 000001.XSHE, 600519.XSHG）
    """
    if not AKSHARE_AVAILABLE:
        return []

    cache_key = f"{concept_code}_{date or 'latest'}"
    if use_cache and cache_key in _concept_stocks_cache:
        return _concept_stocks_cache[cache_key].copy()

    try:
        # 使用东方财富概念板块成分股接口
        df = ak.board_concept_cons_em(symbol=concept_code)

        if df is not None and not df.empty:
            stocks = []
            # 查找代码列
            code_col = None
            for col in ["成分股代码", "股票代码", "代码", "code"]:
                if col in df.columns:
                    code_col = col
                    break

            if code_col:
                for code in df[code_col]:
                    code_str = str(code).zfill(6)
                    # 转换为聚宽格式
                    if code_str.startswith("6"):
                        stocks.append(f"{code_str}.XSHG")
                    elif code_str.startswith(("0", "3")):
                        stocks.append(f"{code_str}.XSHE")
                    elif code_str.startswith(("4", "8")):
                        stocks.append(f"{code_str}.XBSE")  # 北交所

            if use_cache:
                _concept_stocks_cache[cache_key] = stocks

            return stocks

    except Exception as e:
        warnings.warn(f"获取概念板块成分股失败 {concept_code}: {e}")

    return []


def get_stock_concepts(
    security: str,
    date: Optional[str] = None,
) -> List[str]:
    """
    获取股票所属概念。

    参数
    ----
    security : str
        股票代码（支持多种格式）
    date : str, optional
        查询日期

    返回
    ----
    List[str]
        概念板块名称列表
    """
    if not AKSHARE_AVAILABLE:
        return []

    # 标准化股票代码
    code = (
        security.replace("sh", "")
        .replace("sz", "")
        .replace(".XSHG", "")
        .replace(".XSHE", "")
        .replace(".XBSE", "")
        .zfill(6)
    )

    try:
        # 使用个股信息接口
        df = ak.stock_individual_info_em(symbol=code)

        if df is not None and not df.empty:
            concepts = []
            # 查找概念字段
            for item in df["item"]:
                if "概念" in str(item) or "板块" in str(item):
                    concept_str = df[df["item"] == item]["value"].iloc[0]
                    if isinstance(concept_str, str):
                        # 分割概念字符串
                        for concept in concept_str.split(";"):
                            concept = concept.strip()
                            if concept and concept not in concepts:
                                concepts.append(concept)
            return concepts

    except Exception as e:
        warnings.warn(f"获取股票所属概念失败 {security}: {e}")

    return []


def get_all_concept_stocks(
    date: Optional[str] = None,
    top_n: int = 50,
) -> Dict[str, List[str]]:
    """
    获取所有概念板块的成分股。

    参数
    ----
    date : str, optional
        查询日期
    top_n : int, default 50
        获取前N个概念板块

    返回
    ----
    Dict[str, List[str]]
        {概念板块名称: 股票代码列表}
    """
    if not AKSHARE_AVAILABLE:
        return {}

    concepts = get_concept_list(date)
    if concepts.empty:
        return {}

    result = {}
    for _, row in concepts.head(top_n).iterrows():
        concept_code = row.get("code", "")
        concept_name = row.get("name", "")

        if concept_code:
            stocks = get_concept_stocks(concept_code, date)
            if stocks:
                result[concept_name or concept_code] = stocks

    return result


def search_concept(
    keyword: str,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """
    搜索概念板块。

    参数
    ----
    keyword : str
        搜索关键词
    date : str, optional
        查询日期

    返回
    ----
    pd.DataFrame
        匹配的概念板块列表
    """
    concepts = get_concept_list(date)

    if concepts.empty:
        return concepts

    # 按名称搜索
    mask = concepts["name"].str.contains(keyword, case=False, na=False)
    return concepts[mask]


def get_concept_performance(
    date: Optional[str] = None,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    获取概念板块涨跌幅排名。

    参数
    ----
    date : str, optional
        查询日期
    top_n : int, default 10
        返回前N个

    返回
    ----
    pd.DataFrame
        概念板块涨跌幅排名
    """
    if not AKSHARE_AVAILABLE:
        return pd.DataFrame()

    try:
        df = ak.board_concept_name_em()

        if df is not None and not df.empty:
            # 查找涨跌幅列
            pct_col = None
            for col in ["涨跌幅", "change_pct", "涨幅"]:
                if col in df.columns:
                    pct_col = col
                    break

            if pct_col:
                df = df.sort_values(pct_col, ascending=False)
                result = df.head(top_n).copy()
                result = result.rename(columns={
                    "板块代码": "code",
                    "板块名称": "name",
                    pct_col: "change_pct",
                })
                return result[["code", "name", "change_pct"]]

    except Exception as e:
        warnings.warn(f"获取概念板块涨跌幅失败: {e}")

    return pd.DataFrame()


__all__ = [
    "get_concept_list",
    "get_concept_stocks",
    "get_stock_concepts",
    "get_all_concept_stocks",
    "search_concept",
    "get_concept_performance",
]