"""
jk2bt/market_data/concept.py
概念板块数据模块

使用 AkShare 获取概念板块相关数据。

功能:
- 概念板块列表
- 概念板块成分股
- 股票所属概念
"""

import json
import os
import warnings
from typing import Optional, List, Dict
import pandas as pd
from datetime import datetime

from jk2bt.data.sources import get_adapter


# 概念板块数据缓存
_concept_cache: Dict[str, pd.DataFrame] = {}
_concept_stocks_cache: Dict[str, List[str]] = {}

# 概念start_date持久化文件
_CONCEPT_START_DATE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    "data",
    "cache",
    "concept_start_dates.json",
)
_CONCEPT_START_DATE_FILE = os.path.normpath(_CONCEPT_START_DATE_FILE)


def _load_concept_start_dates() -> Dict[str, str]:
    """加载已记录的概念start_date"""
    if os.path.exists(_CONCEPT_START_DATE_FILE):
        try:
            with open(_CONCEPT_START_DATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_concept_start_dates(dates: Dict[str, str]):
    """保存概念start_date"""
    try:
        os.makedirs(os.path.dirname(_CONCEPT_START_DATE_FILE), exist_ok=True)
        with open(_CONCEPT_START_DATE_FILE, "w", encoding="utf-8") as f:
            json.dump(dates, f, ensure_ascii=False, default=str)
    except Exception as e:
        warnings.warn(f"保存概念start_date失败: {e}")


def _update_concept_start_dates(
    current_concepts: Dict[str, str], stored_dates: Dict[str, str]
) -> Dict[str, str]:
    """
    更新概念start_date：
    - 如果概念已存在，保持原有日期
    - 如果概念是新增的，记录今天为start_date
    """
    today = datetime.now().strftime("%Y-%m-%d")
    updated = dict(stored_dates)  # copy

    for code, name in current_concepts.items():
        if code not in updated:
            updated[code] = today

    # 清理已不存在的概念（可选，保留历史记录）
    return updated


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
        - start_date: 概念首次出现日期（通过每日追踪记录）
        - change_pct: 涨跌幅（可选）
    """
    cache_key = f"concepts_{date or 'latest'}"
    if use_cache and cache_key in _concept_cache:
        return _concept_cache[cache_key].copy()

    try:
        # 使用东方财富概念板块接口
        df = get_adapter().get_concept_list()

        if df is not None and not df.empty:
            # 标准化列名
            column_mapping = {
                "板块代码": "code",
                "板块名称": "name",
                "涨跌幅": "change_pct",
                "总市值": "total_market_cap",
                "换手率": "turnover_rate",
                "成立日期": "start_date",
                "起始日期": "start_date",
            }
            df = df.rename(columns=column_mapping)

            # 确保必要列存在
            if "code" not in df.columns and "板块代码" in df.columns:
                df["code"] = df["板块代码"]
            if "name" not in df.columns and "板块名称" in df.columns:
                df["name"] = df["板块名称"]

            # 处理start_date：如果akshare没提供，通过追踪首次出现日期来记录
            has_start_date = (
                "start_date" in df.columns and df["start_date"].notna().any()
            )

            if not has_start_date:
                # 加载已记录的start_date
                stored_dates = _load_concept_start_dates()

                # 构建当前概念映射 {code: name}
                current_concepts = {}
                for _, row in df.iterrows():
                    code = str(row.get("code", ""))
                    name = str(row.get("name", ""))
                    if code:
                        current_concepts[code] = name

                # 更新start_date记录
                updated_dates = _update_concept_start_dates(
                    current_concepts, stored_dates
                )
                _save_concept_start_dates(updated_dates)

                # 将start_date添加到DataFrame
                df["start_date"] = df["code"].apply(
                    lambda x: updated_dates.get(str(x), None)
                )

            result_cols = ["code", "name", "start_date"]
            for extra_col in ["change_pct", "total_market_cap", "turnover_rate"]:
                if extra_col in df.columns:
                    result_cols.append(extra_col)

            result = df[[c for c in result_cols if c in df.columns]].copy()

            if use_cache:
                _concept_cache[cache_key] = result

            return result

    except Exception as e:
        warnings.warn(f"获取概念板块列表失败: {e}")

    return pd.DataFrame(columns=["code", "name", "start_date"])


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
    cache_key = f"{concept_code}_{date or 'latest'}"
    if use_cache and cache_key in _concept_stocks_cache:
        return _concept_stocks_cache[cache_key].copy()

    try:
        # 使用东方财富概念板块成分股接口
        df = get_adapter().get_concept_components(concept_code)

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
        df = get_adapter().get_company_info(code)

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
    try:
        df = get_adapter().get_concept_list()

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
                result = result.rename(
                    columns={
                        "板块代码": "code",
                        "板块名称": "name",
                        pct_col: "change_pct",
                    }
                )
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
