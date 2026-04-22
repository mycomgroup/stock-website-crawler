"""
把 SearchSpace 展开成 Strategy 列表。
超过 max_combinations 时做随机采样。
"""

import itertools
import random
from typing import List, Optional

from .schema import Rule, SearchSpace, Strategy


def expand_search_space(sp: SearchSpace,
                        name_prefix: str = "S") -> List[Strategy]:
    # 每个 filter slot 的候选集（含 None 表示跳过）
    slot_iters = [ch.variants for ch in sp.filter_choices] or [[None]]
    sort_iters = sp.sort_keys or [None]
    n_iters = sp.n_stocks_options or [30]
    s1_iters = sp.stage1_top_pcts or [None]

    combos = list(itertools.product(slot_iters, *([None] if False else []), sort_iters))
    # 上一行的写法保守，这里正式枚举：
    full_combos = []
    for variants_choice in itertools.product(*slot_iters):
        for sort_rule in sort_iters:
            for n in n_iters:
                for s1 in s1_iters:
                    full_combos.append((variants_choice, sort_rule, n, s1))

    rng = random.Random(sp.random_seed)
    if len(full_combos) > sp.max_combinations:
        full_combos = rng.sample(full_combos, sp.max_combinations)

    strategies: List[Strategy] = []
    for idx, (variants_choice, sort_rule, n, s1) in enumerate(full_combos):
        soft_filters: List[Rule] = [v for v in variants_choice if v is not None]
        label_bits = []
        for ch, v in zip(sp.filter_choices, variants_choice):
            if v is None:
                label_bits.append(f"{ch.name}=-")
            else:
                label_bits.append(f"{ch.name}={v.describe()}")
        if sort_rule is not None:
            label_bits.append(f"sort={sort_rule.column}:{'asc' if sort_rule.params.get('ascending') else 'desc'}")
        label_bits.append(f"N={n}")
        if s1 is not None:
            label_bits.append(f"stage1={s1}")

        strategies.append(Strategy(
            name=f"{name_prefix}{idx:04d}",
            hard_filters=list(sp.base_filters),
            soft_filters=soft_filters,
            sort_by=sort_rule,
            n_stocks=int(n),
            rebalance_weeks=sp.rebalance_weeks,
            stage1_top_pct=s1,
            meta={"label": " | ".join(label_bits)},
        ))

    return strategies
