"""
规则应用引擎：在单日横截面 DataFrame 上应用 Strategy，
返回被选中的行（DataFrame）。

容错策略:
  - 若 filter 引用的列在数据中缺失，跳过该条过滤并在返回的 diag 里记录。
  - 若过滤后候选为空，返回空 DataFrame。
  - 若排序列缺失，按第一个 soft_filter 的列降序兜底；再无则按自然顺序。
"""

from dataclasses import dataclass, field
from typing import List
import logging

import pandas as pd

from .operators import apply_filter_op
from .schema import Rule, Strategy

logger = logging.getLogger(__name__)


@dataclass
class ApplyDiag:
    """一次应用的诊断信息，用于调试与记录搜索时的失败原因。"""
    dropped_by: List[str] = field(default_factory=list)
    skipped_rules: List[str] = field(default_factory=list)
    n_input: int = 0
    n_after_hard: int = 0
    n_after_soft: int = 0
    n_output: int = 0


def _apply_rules_sequential(df: pd.DataFrame,
                            rules: List[Rule],
                            diag: ApplyDiag,
                            label: str) -> pd.DataFrame:
    cur = df
    for r in rules:
        if r.column and r.column not in cur.columns:
            diag.skipped_rules.append(f"{label}:{r.describe()}(missing column)")
            continue
        series = cur[r.column] if r.column else None
        try:
            mask = apply_filter_op(r.op, series, r.params)
        except Exception as e:
            diag.skipped_rules.append(f"{label}:{r.describe()}(error:{e})")
            continue
        before = len(cur)
        cur = cur[mask]
        after = len(cur)
        if after < before:
            diag.dropped_by.append(f"{label}:{r.describe()} -{before - after}")
        if len(cur) == 0:
            break
    return cur


def _select_topN(df: pd.DataFrame, sort_rule: Rule, n: int,
                 diag: ApplyDiag) -> pd.DataFrame:
    if len(df) <= n:
        return df
    if sort_rule is None or not sort_rule.column:
        diag.skipped_rules.append("sort:no_rule")
        return df.head(n)
    if sort_rule.column not in df.columns:
        diag.skipped_rules.append(f"sort:{sort_rule.column}(missing)")
        return df.head(n)
    ascending = bool(sort_rule.params.get("ascending", False))
    return df.sort_values(sort_rule.column,
                          ascending=ascending,
                          na_position="last").head(n)


def apply_strategy(df: pd.DataFrame, strategy: Strategy,
                   return_diag: bool = False):
    """
    在一个单日横截面 DataFrame 上应用策略。
    df 至少需要含有 stock_id 列（或索引），以及策略中引用到的列。

    Returns
    -------
    pd.DataFrame   （选中的行；若 return_diag=True 则返回 (df, ApplyDiag)）
    """
    diag = ApplyDiag(n_input=len(df))

    # 1) 硬排雷
    cur = _apply_rules_sequential(df, strategy.hard_filters, diag, "HARD")
    diag.n_after_hard = len(cur)
    if len(cur) == 0:
        diag.n_output = 0
        return (cur, diag) if return_diag else cur

    # 2) 两阶段：先按 stage1_sort 取 top_pct
    if strategy.stage1_top_pct and 0 < strategy.stage1_top_pct <= 1.0:
        stage1_sort = strategy.stage1_sort or strategy.sort_by
        if stage1_sort and stage1_sort.column in cur.columns:
            k = max(strategy.n_stocks,
                    int(len(cur) * strategy.stage1_top_pct))
            k = min(k, len(cur))
            ascending = bool(stage1_sort.params.get("ascending", False))
            cur = cur.sort_values(stage1_sort.column,
                                  ascending=ascending,
                                  na_position="last").head(k)
        else:
            diag.skipped_rules.append("stage1:no_sort_column")

    # 3) 软筛选
    cur = _apply_rules_sequential(cur, strategy.soft_filters, diag, "SOFT")
    diag.n_after_soft = len(cur)
    if len(cur) == 0:
        diag.n_output = 0
        return (cur, diag) if return_diag else cur

    # 4) 排序取 Top N
    out = _select_topN(cur, strategy.sort_by, strategy.n_stocks, diag)
    diag.n_output = len(out)
    return (out, diag) if return_diag else out
