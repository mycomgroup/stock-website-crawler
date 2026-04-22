"""
YAML → 数据结构。

约定:
  aliases.yaml         顶级键 aliases: {别名: 真实列名}
  base.yaml            顶级键 hard_filters: [Rule, ...]
  candidates.yaml      顶级键 strategies: [StrategyDict, ...]
  search_space.yaml    顶级键 search: {...}

StrategyDict 与 SearchSpace 的字段名与 schema 保持一致。
"""

from pathlib import Path
from typing import Dict, List, Optional

import yaml

from .schema import FilterChoice, Rule, SearchSpace, Strategy


def _load_yaml(path: str | Path) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {p}")
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_aliases(path: str | Path) -> Dict[str, str]:
    """别名 → 真实列名。别名缺失时直接返回空 dict，apply 时原样透传。"""
    data = _load_yaml(path)
    return dict(data.get("aliases", {}))


def _resolve_col(name: str, aliases: Dict[str, str]) -> str:
    return aliases.get(name, name)


def _parse_rule(node: dict, aliases: Dict[str, str]) -> Rule:
    if node is None:
        raise ValueError("Rule node is None")
    op = node.get("op")
    if not op:
        raise ValueError(f"Rule missing 'op' field: {node}")
    col = node.get("column", "")
    col = _resolve_col(col, aliases) if col else ""
    # 除 op/column/name 之外的字段一律进 params
    reserved = {"op", "column", "name"}
    params = {k: v for k, v in node.items() if k not in reserved}
    return Rule(op=op, column=col, params=params, name=node.get("name", ""))


def _parse_rules(nodes, aliases: Dict[str, str]) -> List[Rule]:
    if not nodes:
        return []
    return [_parse_rule(n, aliases) for n in nodes]


def load_base_filters(path: str | Path,
                      aliases: Optional[Dict[str, str]] = None) -> List[Rule]:
    """加载基础排雷层 YAML（只有 hard_filters 字段）。"""
    aliases = aliases or {}
    data = _load_yaml(path)
    return _parse_rules(data.get("hard_filters", []), aliases)


def load_strategy(node: dict | str | Path,
                  aliases: Optional[Dict[str, str]] = None,
                  base_filters: Optional[List[Rule]] = None) -> Strategy:
    """
    可传入:
      - dict (已解析的 YAML 节点)
      - YAML 文件路径（整个文件作为一个 strategy）
    """
    aliases = aliases or {}
    base_filters = base_filters or []

    if isinstance(node, (str, Path)):
        node = _load_yaml(node)

    hard = list(base_filters) + _parse_rules(node.get("hard_filters", []), aliases)
    soft = _parse_rules(node.get("soft_filters", node.get("filters", [])), aliases)

    sort_node = node.get("sort_by")
    sort_rule = None
    if sort_node:
        sort_rule = Rule(
            op="sort",
            column=_resolve_col(sort_node.get("column", ""), aliases),
            params={"ascending": sort_node.get("ascending", False)},
            name=sort_node.get("name", ""),
        )

    stage1_sort_node = node.get("stage1_sort")
    stage1_sort = None
    if stage1_sort_node:
        stage1_sort = Rule(
            op="sort",
            column=_resolve_col(stage1_sort_node.get("column", ""), aliases),
            params={"ascending": stage1_sort_node.get("ascending", False)},
        )

    return Strategy(
        name=node.get("name", "unnamed"),
        hard_filters=hard,
        soft_filters=soft,
        sort_by=sort_rule,
        n_stocks=int(node.get("n_stocks", 30)),
        rebalance_weeks=int(node.get("rebalance_weeks", 1)),
        stage1_top_pct=node.get("stage1_top_pct"),
        stage1_sort=stage1_sort,
        meta=node.get("meta", {}),
    )


def load_candidates(path: str | Path,
                    aliases: Optional[Dict[str, str]] = None,
                    base_filters: Optional[List[Rule]] = None) -> List[Strategy]:
    data = _load_yaml(path)
    strategies = []
    for node in data.get("strategies", []):
        strategies.append(load_strategy(node, aliases, base_filters))
    return strategies


def load_search_space(path: str | Path,
                      aliases: Optional[Dict[str, str]] = None,
                      base_filters: Optional[List[Rule]] = None) -> SearchSpace:
    aliases = aliases or {}
    base_filters = base_filters or []
    data = _load_yaml(path)
    node = data.get("search", data)

    # filter_choices: 每个 choice 有 name + variants；variant 可为 null 表示跳过
    choices: List[FilterChoice] = []
    for ch in node.get("filter_choices", []):
        variants: List[Optional[Rule]] = []
        for v in ch.get("variants", []):
            if v is None or v == "none" or v == "skip":
                variants.append(None)
            else:
                variants.append(_parse_rule(v, aliases))
        choices.append(FilterChoice(name=ch.get("name", ""), variants=variants))

    sort_keys: List[Rule] = []
    for sk in node.get("sort_keys", []):
        sort_keys.append(Rule(
            op="sort",
            column=_resolve_col(sk.get("column", ""), aliases),
            params={"ascending": sk.get("ascending", False)},
            name=sk.get("name", ""),
        ))

    stage1 = node.get("stage1_top_pcts", [None])
    # 允许在 YAML 里写 "none"
    stage1_norm: List[Optional[float]] = [
        None if (x is None or x == "none") else float(x) for x in stage1
    ]

    # base_filters 可以在 search_space.yaml 里单独再加
    extra_base = _parse_rules(node.get("base_filters", []), aliases)

    return SearchSpace(
        base_filters=list(base_filters) + extra_base,
        filter_choices=choices,
        sort_keys=sort_keys,
        n_stocks_options=[int(x) for x in node.get("n_stocks_options", [30])],
        stage1_top_pcts=stage1_norm,
        max_combinations=int(node.get("max_combinations", 500)),
        rebalance_weeks=int(node.get("rebalance_weeks", 1)),
        random_seed=int(node.get("random_seed", 42)),
    )
