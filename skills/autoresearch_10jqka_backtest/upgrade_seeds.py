#!/usr/bin/env python3
"""
Upgrade seed files with new metadata fields.

Run: python upgrade_seeds.py
"""

import json
import os
from pathlib import Path

def upgrade_seed_file(filepath: Path) -> bool:
    with open(filepath, 'r', encoding='utf-8') as f:
        seed = json.load(f)

    if "seed_metadata" in seed:
        return False

    formula = seed.get("formula", [])
    if isinstance(formula, str):
        formula = [formula]
    non_sort = [c for c in formula if not any(kw in c for kw in ["从大到小", "从小到大", "由近到远", "由远到近"])]
    core_formula = non_sort[:3] if len(non_sort) >= 3 else non_sort

    locked = [c for c in formula if c in ["非ST", "非退市", "非科创板", "创业板", "沪深A股"]]

    max_pos = seed.get("maxPositions", 5)
    take_profit = seed.get("takeProfit", 20)
    stop_loss = seed.get("stopLoss", 9)
    trailing = seed.get("trailingStopLoss", 5)

    tree_tags = []
    name = filepath.stem
    if name.startswith("A"):
        tree_tags.append("value")
    elif name.startswith("B"):
        tree_tags.append("quality_growth")
    elif name.startswith("C"):
        tree_tags.append("small_cap")
    elif name.startswith("D"):
        tree_tags.append("mispricing_reversal")
    elif name.startswith("E"):
        tree_tags.append("technical_trend")
    elif name.startswith("F"):
        tree_tags.append("fund_flow")
    elif name.startswith("G"):
        tree_tags.append("event_driven")
    elif name.startswith("H"):
        tree_tags.append("composite")
    elif name.startswith("I"):
        tree_tags.append("portfolio_risk")

    seed["seed_metadata"] = {
        "core_formula": core_formula,
        "locked_formula": locked,
        "forbidden_formula": [],
        "parameter_priors": {
            "maxPositions": {"type": "discrete", "values": [3, 5, 8, 10], "preferred": max_pos},
            "takeProfit": {"type": "range", "min": 15, "max": 30, "step": 5, "preferred": take_profit},
            "stopLoss": {"type": "range", "min": 7, "max": 12, "step": 1, "preferred": stop_loss},
            "trailingStopLoss": {"type": "range", "min": 3, "max": 8, "step": 1, "preferred": trailing},
        },
        "expected_holding_profile": "medium_term",
        "expected_position_range": [max(3, max_pos - 2), max_pos + 3],
        "recency_weight_profile": {"recent6m": 0.40, "recent12m": 0.40, "prior12m": 0.15, "full24m": 0.05}
    }

    seed["tree_tags"] = tree_tags

    seed["search_hints"] = {
        "coarse_step_sizes": {"growth_rates": 5, "profitability": 2, "valuation": 10, "turnover": 1},
        "fine_step_sizes": {"growth_rates": 2, "profitability": 1, "valuation": 5, "turnover": 0.5},
        "avoid_extreme_values": {
            "maxPositions": {"min": 4, "max": 12},
            "takeProfit": {"min": 10, "max": 35},
            "stopLoss": {"min": 5, "max": 15}
        }
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)

    return True


def main():
    dirs = [Path("/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch_10jqka_backtest/seeds/")]
    tree_dir = Path("/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch_10jqka_backtest/trees")
    if tree_dir.exists():
        for subdir in tree_dir.iterdir():
            if subdir.is_dir() and (subdir / "seed.json").exists():
                dirs.append(subdir)

    total_modified = 0
    total_skipped = 0

    for seeds_dir in dirs:
        if not seeds_dir.exists():
            continue
        print(f"\n=== Processing {seeds_dir} ===")

        for filepath in sorted(seeds_dir.glob("*.json")):
            try:
                if upgrade_seed_file(filepath):
                    print(f"Upgraded: {filepath.name}")
                    total_modified += 1
                else:
                    print(f"Skipped: {filepath.name}")
                    total_skipped += 1
            except Exception as e:
                print(f"Error with {filepath.name}: {e}")

    print(f"\nTotal: {total_modified} upgraded, {total_skipped} skipped")


if __name__ == "__main__":
    main()