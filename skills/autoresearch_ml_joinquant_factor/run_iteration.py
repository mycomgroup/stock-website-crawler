#!/usr/bin/env python3
"""run_iteration.py - ML 多策略因子池单轮迭代。

目标：
1) 一轮生成多组候选因子组合
2) 批量评估并与历史池合并
3) 保留 Top-K 策略因子组
4) 将最佳组同步到 strategy.py（供后续验证/实盘）
"""

from __future__ import annotations

import argparse
import ast
import json
import random
import re
from datetime import datetime
from pathlib import Path
from typing import Iterable

from notebook_executor import execute_strategy

try:
    from skills.autoresearch_joinquant_factor.factor_categories import (
        calculate_diversity_score,
        get_factor_category,
    )
except Exception:
    import importlib.util
    import sys

    root = Path(__file__).resolve().parents[2]
    module_path = (
        root / "skills" / "autoresearch_joinquant_factor" / "factor_categories.py"
    )
    spec = importlib.util.spec_from_file_location("factor_categories", module_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["factor_categories"] = mod
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    calculate_diversity_score = mod.calculate_diversity_score
    get_factor_category = mod.get_factor_category


AUTORESEARCH_DIR = Path(__file__).parent
POOL_FILE = "strategy_pool.json"
HISTORY_FILE = "iteration_history.jsonl"


def _load_factor_pool() -> list[str]:
    """复用主项目因子分类，作为候选因子全集。"""
    try:
        from skills.autoresearch_joinquant_factor.factor_categories import (
            FACTOR_CATEGORIES,
        )
    except Exception:
        import importlib.util
        import sys

        root = Path(__file__).resolve().parents[2]
        module_path = (
            root / "skills" / "autoresearch_joinquant_factor" / "factor_categories.py"
        )
        spec = importlib.util.spec_from_file_location("factor_categories", module_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["factor_categories"] = mod
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        FACTOR_CATEGORIES = mod.FACTOR_CATEGORIES

    factors: list[str] = []
    for group in FACTOR_CATEGORIES.values():
        factors.extend(group)

    seen: set[str] = set()
    dedup: list[str] = []
    for f in factors:
        if f not in seen:
            dedup.append(f)
            seen.add(f)
    return dedup


def _normalize_combo(combo: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for f in combo:
        if not isinstance(f, str):
            continue
        name = f.strip()
        if not name or name in seen:
            continue
        out.append(name)
        seen.add(name)
    return out


def _combo_key(combo: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted(_normalize_combo(combo)))


def _read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _extract_factor_combo(strategy_text: str) -> list[str]:
    m = re.search(r"^FACTOR_COMBO\s*=\s*(.+)$", strategy_text, flags=re.MULTILINE)
    if not m:
        return []
    try:
        parsed = ast.literal_eval(m.group(1).strip())
        if isinstance(parsed, list):
            return _normalize_combo(parsed)
    except Exception:
        pass
    return []


def _replace_factor_combo(strategy_text: str, combo: list[str]) -> str:
    line = f"FACTOR_COMBO = {combo!r}"
    if re.search(r"^FACTOR_COMBO\s*=\s*.+$", strategy_text, flags=re.MULTILINE):
        return re.sub(
            r"^FACTOR_COMBO\s*=\s*.+$", line, strategy_text, flags=re.MULTILINE
        )
    return strategy_text + "\n" + line + "\n"


def _mutate_combo(
    base_combo: list[str], factor_pool: list[str], rng: random.Random
) -> list[str]:
    combo = _normalize_combo(base_combo)
    if not combo:
        combo = rng.sample(factor_pool, k=min(4, len(factor_pool)))

    action = rng.choice(["replace", "add", "drop", "shuffle"])

    if action == "replace" and combo:
        idx = rng.randrange(len(combo))
        combo[idx] = rng.choice(factor_pool)
    elif action == "add" and len(combo) < 8:
        combo.append(rng.choice(factor_pool))
    elif action == "drop" and len(combo) > 3:
        del combo[rng.randrange(len(combo))]
    else:
        rng.shuffle(combo)

    combo = _normalize_combo(combo)

    # 长度约束：3~8
    if len(combo) < 3:
        remain = [f for f in factor_pool if f not in combo]
        need = min(len(remain), 3 - len(combo))
        combo.extend(rng.sample(remain, k=need))
    if len(combo) > 8:
        combo = combo[:8]

    return _normalize_combo(combo)


def generate_combo_with_diversity(
    base_candidates: list[list[str]],
    factor_pool: list[str],
    seen: set[tuple[str, ...]],
    rng: random.Random,
    min_diversity: float = 0.5,
    max_trials: int = 100,
) -> list[str] | None:
    best_combo: list[str] | None = None
    best_diversity = 0.0

    for _ in range(max_trials):
        base_combo = rng.choice(base_candidates) if base_candidates else []
        combo = _mutate_combo(base_combo, factor_pool, rng)
        key = _combo_key(combo)
        if not key or key in seen:
            continue

        diversity = calculate_diversity_score(combo)
        if diversity >= min_diversity:
            return combo
        if diversity > best_diversity:
            best_diversity = diversity
            best_combo = combo

    return best_combo


def check_hard_constraints(result: dict) -> tuple[bool, str]:
    payload = result.get("payload", {})
    ic_mean = float(payload.get("ic_mean", 0.0))
    diversity = float(
        payload.get("diversity", calculate_diversity_score(result.get("factors", [])))
    )

    if diversity < 0.5:
        return False, f"diversity={diversity:.2f} < 0.5"
    if ic_mean < 0:
        return False, f"ic_mean={ic_mean:.4f} < 0"
    return True, ""


def _load_seed_config(base: Path) -> dict:
    return _read_json(base / "seed_config.json", default={})


def _load_strategy_pool(
    base: Path, seed_factors: list[list[str]], baseline_score: float
) -> list[dict]:
    pool_path = base / POOL_FILE
    existing = _read_json(pool_path, default=[])
    if existing:
        return existing

    bootstrap: list[dict] = []
    for i, combo in enumerate(seed_factors):
        c = _normalize_combo(combo)
        if not c:
            continue
        bootstrap.append(
            {
                "rank": i + 1,
                "score": baseline_score if i == 0 else 0.0,
                "factors": c,
                "source": "seed",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "iter": 0,
            }
        )
    return bootstrap


def _evaluate_combo(
    base: Path, strategy_template: str, combo: list[str], notebook_dir: str | None
) -> dict:
    temp_strategy = base / ".strategy_candidate.py"
    temp_strategy.write_text(
        _replace_factor_combo(strategy_template, combo), encoding="utf-8"
    )

    result = execute_strategy(
        str(temp_strategy), timeout_ms=600_000, notebook_dir=notebook_dir
    )
    score = float(result.get("score", 0.0)) if result.get("success") else -1e9

    return {
        "factors": combo,
        "score": score,
        "success": bool(result.get("success")),
        "payload": result.get("payload", {}),
        "error": result.get("error"),
    }


def _save_search_notes(
    base: Path,
    state: dict,
    strategy_pool: list[dict],
    latest_results: list[dict],
    decisions: list[dict] | None = None,
) -> None:
    lines: list[str] = []

    lines.append("## 当前状态")
    lines.append(f"- best_score: {state['best_score']:.6f}")
    lines.append(f"- best_factors: {state['best_factors']}")
    lines.append(f"- current_iter: {state['current_iter']}")
    lines.append(f"- top_k: {state['top_k']}")
    lines.append("")

    lines.append("## 回测配置")
    lines.append(f"- 日期范围: {state.get('date_range', 'N/A')}")
    lines.append(f"- 选股池: {state.get('pool', 'N/A')}")
    lines.append("")

    lines.append("## 多策略池（Top-K）")
    lines.append("| rank | score | factors | source | iter |")
    lines.append("|------|-------|---------|--------|------|")
    for i, item in enumerate(strategy_pool, start=1):
        lines.append(
            f"| {i} | {float(item.get('score', 0.0)):.6f} | {item.get('factors', [])} | {item.get('source', '')} | {item.get('iter', 0)} |"
        )
    lines.append("")

    lines.append("## 最近一轮候选结果")
    lines.append("| idx | score | factors | success | decision |")
    lines.append("|-----|-------|---------|---------|----------|")
    decisions = decisions or []
    for i, item in enumerate(latest_results, start=1):
        dec = decisions[i - 1].get("decision", "") if i - 1 < len(decisions) else ""
        lines.append(
            f"| {i} | {float(item.get('score', 0.0)):.6f} | {item.get('factors', [])} | {item.get('success', False)} | {dec} |"
        )
    lines.append("")

    keep_list = [d for d in decisions if d.get("decision") == "keep"]
    rollback_list = [d for d in decisions if d.get("decision") == "rollback"]

    lines.append("## 搜索地图")
    lines.append("")
    lines.append("### 已验证有效（keep）")
    for d in keep_list:
        factors = d.get("factors", [])
        score = d.get("score", 0.0)
        reason = d.get("reason", "")
        lines.append(f"- {factors}: score={score:.4f}, {reason}")
    lines.append("")

    lines.append("### 已验证无效（rollback）")
    for d in rollback_list:
        factors = d.get("factors", [])
        score = d.get("score", 0.0)
        reason = d.get("reason", "")
        lines.append(f"- {factors}: score={score:.4f}, {reason}")
    lines.append("")

    lines.append("### 待探索方向")
    lines.append("- [ ] 尝试新的因子类别组合")
    lines.append("- [ ] 优化因子权重配置")
    lines.append("")

    (base / "search_notes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="ML 多策略因子池单轮迭代")
    parser.add_argument("--base", default=".", help="实验目录")
    parser.add_argument("--batch-size", type=int, default=6, help="每轮生成候选组合数")
    parser.add_argument("--top-k", type=int, default=None, help="保留前K组策略")
    parser.add_argument("--notebook-dir", default=None, help="joinquant notebook目录")
    parser.add_argument("--seed", type=int, default=None, help="随机种子")
    args = parser.parse_args()

    base = Path(args.base).resolve()
    strategy_file = base / "strategy.py"
    if not strategy_file.exists():
        raise SystemExit(f"[错误] strategy.py 不存在: {strategy_file}")

    seed_cfg = _load_seed_config(base)
    seed_factors = seed_cfg.get("seed_factors") or []
    baseline_result = seed_cfg.get("baseline_result") or {}
    baseline_score = (
        float(baseline_result.get("score", 0.0))
        if isinstance(baseline_result, dict)
        else 0.0
    )
    top_k = int(args.top_k if args.top_k is not None else seed_cfg.get("top_k", 5))

    strategy_text = strategy_file.read_text(encoding="utf-8")
    current_combo = _extract_factor_combo(strategy_text)

    strategy_pool = _load_strategy_pool(
        base, seed_factors=seed_factors, baseline_score=baseline_score
    )
    if current_combo and _combo_key(current_combo) not in {
        _combo_key(x.get("factors", [])) for x in strategy_pool
    }:
        strategy_pool.append(
            {
                "rank": len(strategy_pool) + 1,
                "score": baseline_score,
                "factors": current_combo,
                "source": "current",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "iter": 0,
            }
        )

    rng = random.Random(
        args.seed if args.seed is not None else int(datetime.utcnow().timestamp())
    )
    factor_pool = _load_factor_pool()

    base_candidates = [
        p.get("factors", []) for p in strategy_pool[: min(len(strategy_pool), top_k)]
    ]
    if not base_candidates:
        base_candidates = (
            [current_combo]
            if current_combo
            else [seed_factors[0] if seed_factors else []]
        )

    seen = {_combo_key(x.get("factors", [])) for x in strategy_pool}
    candidates: list[list[str]] = []

    max_trials = max(20, args.batch_size * 10)
    trials = 0
    while len(candidates) < args.batch_size and trials < max_trials:
        trials += 1
        new_combo = generate_combo_with_diversity(
            base_candidates, factor_pool, seen, rng, min_diversity=0.5, max_trials=100
        )
        if new_combo is None:
            continue
        key = _combo_key(new_combo)
        if key and key not in seen:
            seen.add(key)
            candidates.append(new_combo)

    if not candidates:
        print("[warn] 未生成新候选组合，跳过本轮")
        return

    iter_no = 1
    history_path = base / HISTORY_FILE
    if history_path.exists():
        iter_no += sum(
            1
            for _ in history_path.read_text(encoding="utf-8").splitlines()
            if _.strip()
        )

    latest_results: list[dict] = []
    decisions: list[dict] = []
    for combo in candidates:
        result = _evaluate_combo(
            base, strategy_text, combo, notebook_dir=args.notebook_dir
        )
        passed, reason = check_hard_constraints(result)
        if not passed:
            result["score"] = -1e9
            decisions.append(
                {
                    "factors": combo,
                    "decision": "rollback",
                    "reason": f"hard constraint: {reason}",
                }
            )
        else:
            decisions.append(
                {"factors": combo, "decision": "keep", "reason": "passed constraints"}
            )
        latest_results.append(result)

    # 去重合并并按分数排序
    merged: dict[tuple[str, ...], dict] = {}
    for item in strategy_pool:
        key = _combo_key(item.get("factors", []))
        if key:
            merged[key] = item

    for item in latest_results:
        key = _combo_key(item.get("factors", []))
        if not key:
            continue
        old = merged.get(key)
        new_score = float(item.get("score", -1e9))
        old_score = float(old.get("score", -1e9)) if old else -1e9
        if old is None or new_score > old_score:
            merged[key] = {
                "score": new_score,
                "factors": item.get("factors", []),
                "source": "iteration",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "iter": iter_no,
            }

    sorted_pool = sorted(
        merged.values(), key=lambda x: float(x.get("score", -1e9)), reverse=True
    )
    sorted_pool = sorted_pool[: max(1, top_k)]
    for i, item in enumerate(sorted_pool, start=1):
        item["rank"] = i

    # 更新主 strategy.py 为当前第一名
    best = sorted_pool[0]
    best_combo = _normalize_combo(best.get("factors", []))
    strategy_file.write_text(
        _replace_factor_combo(strategy_text, best_combo), encoding="utf-8"
    )

    # 落盘
    (base / POOL_FILE).write_text(
        json.dumps(sorted_pool, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    state = {
        "best_score": float(best.get("score", 0.0)),
        "best_factors": best_combo,
        "current_iter": iter_no,
        "top_k": top_k,
        "date_range": f"{seed_cfg.get('start_date', 'N/A')} ~ {seed_cfg.get('end_date', 'N/A')}",
        "pool": seed_cfg.get("pool", "N/A"),
    }
    _save_search_notes(base, state, sorted_pool, latest_results, decisions)

    with history_path.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "iter": iter_no,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "candidates": latest_results,
                    "top_k": sorted_pool,
                    "best": best,
                },
                ensure_ascii=False,
            )
            + "\n"
        )

    # 清理临时文件
    temp_strategy = base / ".strategy_candidate.py"
    if temp_strategy.exists():
        temp_strategy.unlink()

    print(
        f"[iter] iter={iter_no} candidates={len(candidates)} top_k={top_k} best_score={state['best_score']:.6f}"
    )


if __name__ == "__main__":
    main()
