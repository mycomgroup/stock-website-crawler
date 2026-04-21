"""
原子操作符注册表。每个 filter 操作符签名:
    fn(series: pd.Series, **params) -> pd.Series[bool]

每个 sort 操作符:
    fn(df: pd.DataFrame, column: str, **params) -> pd.Index   （已排序的行索引）

YAML 里通过 op 字段的字符串引用，loader 负责把字符串映射到这些函数。
新增操作符只需在本文件加函数并放进 FILTER_OPS / SORT_OPS。
"""

from typing import Callable, Dict
import numpy as np
import pandas as pd


# ---------- filter ops ----------

def op_gt(s: pd.Series, value: float) -> pd.Series:
    return s > value


def op_ge(s: pd.Series, value: float) -> pd.Series:
    return s >= value


def op_lt(s: pd.Series, value: float) -> pd.Series:
    return s < value


def op_le(s: pd.Series, value: float) -> pd.Series:
    return s <= value


def op_eq(s: pd.Series, value) -> pd.Series:
    return s == value


def op_ne(s: pd.Series, value) -> pd.Series:
    return s != value


def op_between(s: pd.Series, low: float, high: float,
               inclusive: str = "both") -> pd.Series:
    return s.between(low, high, inclusive=inclusive)


def op_not_null(s: pd.Series) -> pd.Series:
    return s.notna()


def op_is_null(s: pd.Series) -> pd.Series:
    return s.isna()


def op_top_pct(s: pd.Series, pct: float) -> pd.Series:
    """取 s 在横截面中的 top pct%（pct∈(0,1]）。NaN 不通过。"""
    valid = s.dropna()
    if len(valid) == 0:
        return pd.Series(False, index=s.index)
    k = max(1, int(np.ceil(len(valid) * pct)))
    threshold = valid.nlargest(k).min()
    return (s >= threshold) & s.notna()


def op_bottom_pct(s: pd.Series, pct: float) -> pd.Series:
    valid = s.dropna()
    if len(valid) == 0:
        return pd.Series(False, index=s.index)
    k = max(1, int(np.ceil(len(valid) * pct)))
    threshold = valid.nsmallest(k).max()
    return (s <= threshold) & s.notna()


def op_rank_gt(s: pd.Series, pct: float) -> pd.Series:
    """横截面 rank percentile > pct（pct∈[0,1]）。等价于 top (1-pct)。"""
    r = s.rank(pct=True, method="average")
    return r > pct


def op_rank_lt(s: pd.Series, pct: float) -> pd.Series:
    r = s.rank(pct=True, method="average")
    return r < pct


FILTER_OPS: Dict[str, Callable] = {
    "gt": op_gt,
    "ge": op_ge,
    "lt": op_lt,
    "le": op_le,
    "eq": op_eq,
    "ne": op_ne,
    "between": op_between,
    "not_null": op_not_null,
    "is_null": op_is_null,
    "top_pct": op_top_pct,
    "bottom_pct": op_bottom_pct,
    "rank_gt": op_rank_gt,
    "rank_lt": op_rank_lt,
}


# ---------- sort ops ----------

def sort_by_column(df: pd.DataFrame, column: str,
                   ascending: bool = False, n: int = None) -> pd.DataFrame:
    """
    按单列排序并可选截取前 n 行。NaN 始终放在末尾。
    """
    ordered = df.sort_values(
        column, ascending=ascending, na_position="last"
    )
    if n is not None:
        ordered = ordered.head(n)
    return ordered


SORT_OPS: Dict[str, Callable] = {
    "sort": sort_by_column,
}


def is_filter_op(op: str) -> bool:
    return op in FILTER_OPS


def is_sort_op(op: str) -> bool:
    return op in SORT_OPS


def apply_filter_op(op: str, series: pd.Series, params: dict) -> pd.Series:
    if op not in FILTER_OPS:
        raise ValueError(f"Unknown filter op: {op!r}. "
                         f"Available: {sorted(FILTER_OPS)}")
    mask = FILTER_OPS[op](series, **params)
    return mask.fillna(False)
