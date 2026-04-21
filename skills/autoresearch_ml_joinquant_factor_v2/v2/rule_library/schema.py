"""
规则库数据结构。所有字段都能从 YAML 映射过来。
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Rule:
    """
    单条规则。op 指向 operators 注册表里的函数名，column 是逻辑列名
    （允许中文别名，在 loader 中会解析到真实 CSV 列），
    params 是其他参数（value / low / high / pct / ascending…）。
    """
    op: str
    column: str = ""
    params: Dict[str, Any] = field(default_factory=dict)
    name: str = ""

    def describe(self) -> str:
        if self.name:
            return self.name
        if self.params:
            kv = ", ".join(f"{k}={v}" for k, v in self.params.items())
            return f"{self.op}({self.column}, {kv})"
        return f"{self.op}({self.column})"


@dataclass
class Strategy:
    """
    完整策略定义。
      hard_filters — 硬约束（排雷层），不通过即淘汰。
      soft_filters — 软筛选层（质量/估值/事件等）。
      sort_by      — 排序键（Rule，op 必须是 'sort'）。
      n_stocks     — 持仓数。
      rebalance_weeks — 调仓周期（周）。
      stage1_top_pct  — 两阶段选股时的第一阶段比例；None 表示单阶段。
      stage1_sort     — 第一阶段排序键（默认按 prediction，若无则按第一个 soft_filter）。
    """
    name: str
    hard_filters: List[Rule] = field(default_factory=list)
    soft_filters: List[Rule] = field(default_factory=list)
    sort_by: Optional[Rule] = None
    n_stocks: int = 30
    rebalance_weeks: int = 1
    stage1_top_pct: Optional[float] = None
    stage1_sort: Optional[Rule] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def n_filters(self) -> int:
        return len(self.hard_filters) + len(self.soft_filters)

    def signature(self) -> str:
        parts = [self.name or "unnamed"]
        for r in self.hard_filters:
            parts.append("H:" + r.describe())
        for r in self.soft_filters:
            parts.append("S:" + r.describe())
        if self.sort_by:
            parts.append("SORT:" + self.sort_by.describe())
        parts.append(f"N={self.n_stocks}")
        if self.stage1_top_pct:
            parts.append(f"STAGE1={self.stage1_top_pct}")
        return " | ".join(parts)


@dataclass
class FilterChoice:
    """搜索空间里一个"过滤槽"，可以从若干备选规则里选一个（或空)。"""
    name: str
    variants: List[Optional[Rule]]  # 允许含 None 表示"跳过"


@dataclass
class SearchSpace:
    """
    网格搜索空间定义。
      base_filters     — 硬排雷层，所有候选共享。
      filter_choices   — 软筛选槽，每个槽从若干 variants 里选一个。
      sort_keys        — 排序键候选。
      n_stocks_options — 持仓数候选。
      stage1_top_pcts  — 两阶段第一阶段比例候选（含 None 表示单阶段）。
      max_combinations — 最多展开多少条策略（超过则随机采样）。
      rebalance_weeks  — 调仓周期（固定，不参与搜索）。
    """
    base_filters: List[Rule] = field(default_factory=list)
    filter_choices: List[FilterChoice] = field(default_factory=list)
    sort_keys: List[Rule] = field(default_factory=list)
    n_stocks_options: List[int] = field(default_factory=lambda: [30])
    stage1_top_pcts: List[Optional[float]] = field(default_factory=lambda: [None])
    max_combinations: int = 500
    rebalance_weeks: int = 1
    random_seed: int = 42
