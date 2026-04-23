#!/usr/bin/env python3
"""
run_tree.py - 树级长跑调度器

读取 trees/<tree>/profile.json 的 run_policy，自动创建多个 runs/run-NNN 子实验，
每个 run 从同一个 profile 的 initial_formula 起步，循环调用 run_iteration.py，
直到 rounds_per_run 或 stagnation 触发重启。

Usage:
    python run_tree.py --tree A_value
    python run_tree.py --tree A_value --restarts 8 --rounds 300
    python run_tree.py --tree B_quality_growth --mock
"""

import argparse
import json
import subprocess
import sys
import shutil
import random
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

SKILL_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(SKILL_ROOT))

from tree_profile import (
    load_tree_profile_from_dir,
    get_initial_formula,
    get_hard_guards,
    get_run_policy,
    validate_profile,
    merge_with_defaults,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="树级长跑调度器")
    parser.add_argument("--tree", required=True, help="树名称或路径（如 A_value 或 trees/A_value）")
    parser.add_argument("--restarts", type=int, default=None, help="重启次数（覆盖 profile 的 num_restarts）")
    parser.add_argument("--rounds", type=int, default=None, help="每轮运行次数（覆盖 profile 的 rounds_per_run）")
    parser.add_argument("--stagnation", type=int, default=None, help="停滞重启阈值（覆盖 profile 的 restart_on_stagnation）")
    parser.add_argument("--mock", action="store_true", help="Mock 模式")
    parser.add_argument("--start-date", default=None, help="回测开始日期")
    parser.add_argument("--end-date", default=None, help="回测结束日期")
    parser.add_argument("--continue-from", default=None, help="从已有 run 继续（如 run-003）")
    return parser.parse_args()


def resolve_tree_dir(tree_arg: str) -> Path:
    tree_path = Path(tree_arg)
    if tree_path.is_absolute():
        return tree_path
    if (SKILL_ROOT / "trees" / tree_path).exists():
        return SKILL_ROOT / "trees" / tree_path
    if tree_path.exists():
        return tree_path
    print(f"错误：找不到树：{tree_arg}", file=sys.stderr)
    sys.exit(1)


def setup_run(tree_dir: Path, run_id: str, profile: dict, args: argparse.Namespace) -> Path:
    """Create a new run directory and initialize it via setup.py."""
    runs_dir = tree_dir / "runs"
    runs_dir.mkdir(exist_ok=True)
    run_dir = runs_dir / run_id

    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)

    initial_formula = get_initial_formula(profile)
    hard_guards = get_hard_guards(profile)

    soft_priors = profile.get("soft_priors", {})
    max_pos_prefs = soft_priors.get("maxPositions", {}).get("preferred", [5, 8])
    tp_prefs = soft_priors.get("takeProfit", {}).get("preferred", [15, 25])
    sl_prefs = soft_priors.get("stopLoss", {}).get("preferred", [7, 12])
    tsl_prefs = soft_priors.get("trailingStopLoss", {}).get("preferred", [5, 8])

    start_date = args.start_date
    end_date = args.end_date

    if start_date is None or start_date == "AUTO":
        from datetime import timedelta
        end_date = end_date or datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365 * 5)).strftime("%Y-%m-%d")

    config = {
        "name": f"{profile.get('name', tree_dir.name)}-{run_id}",
        "description": f"{profile.get('description', '')} | Run {run_id}",
        "formula": list(initial_formula),
        "startDate": start_date,
        "endDate": end_date,
        "maxPositions": max_pos_prefs[0] if isinstance(max_pos_prefs, list) and len(max_pos_prefs) >= 2 else 5,
        "dailyBuyCount": 2,
        "takeProfit": tp_prefs[0] if isinstance(tp_prefs, list) and len(tp_prefs) >= 2 else 20,
        "stopLoss": sl_prefs[0] if isinstance(sl_prefs, list) and len(sl_prefs) >= 2 else 10,
        "trailingStopLoss": tsl_prefs[0] if isinstance(tsl_prefs, list) and len(tsl_prefs) >= 2 else 5,
        "daysForSaleStrategy": "3,5",
    }

    with open(run_dir / "formula_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    state = {
        "current_iter": 1,
        "champion_score": -1e308,
        "champion_robust_score": -1e308,
        "consecutive_failures": 0,
        "last_update": datetime.now().isoformat(),
        "objective_version": "v4_tree_profile",
        "seed_name": profile.get("name", tree_dir.name),
        "search_mode": "tree_profile",
        "phase": "coarse_search",
        "direction_status": "UNKNOWN",
        "direction_reason": "",
        "champion_metrics": {},
        "champion_windows": {},
        "baseline_window_scores": {},
        "baseline_metrics_by_window": {},
        "stable_param_ranges": {},
        "last_keep_reason": "",
        "last_mutation_type": "baseline",
        "final_recommendation": "",
        "stop_reason": "",
        "tree_profile": {
            "tree_id": profile.get("tree_id", tree_dir.name),
            "run_id": run_id,
        },
    }
    with open(run_dir / "state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    tsv_header = "iter\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\trobust_score\trecent6\trecent12\tprior12\tfull24\tsensitivity\ttrade_count\tcomplexity\treason\n"
    with open(run_dir / "iterations.tsv", "w", encoding="utf-8") as f:
        f.write(tsv_header)

    with open(run_dir / "program.md", "w", encoding="utf-8") as f:
        f.write(f"# {profile.get('name', tree_dir.name)} - {run_id}\n\n")
        f.write(f"{profile.get('description', '')}\n\n")
        f.write(f"## 初始公式\n\n")
        for clause in initial_formula:
            f.write(f"- {clause}\n")

    print(f"  ✓ 创建 {run_id}: formula={initial_formula}")
    return run_dir


def run_single_iteration(run_dir: Path, mutation_summary: str, mutation_type: Optional[str] = None) -> int:
    """Run a single iteration by calling run_iteration.py. Returns exit code."""
    cmd = [
        sys.executable, str(SKILL_ROOT / "run_iteration.py"),
        "--base", str(run_dir),
        "--mutation-summary", mutation_summary,
    ]
    if mutation_type:
        cmd.extend(["--mutation-type", mutation_type])

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

    if result.stdout:
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                print(f"    {line}")

    return result.returncode


def check_stagnation(run_dir: Path, stagnation_threshold: int) -> bool:
    """Check if the run has stagnated (no keep for stagnation_threshold rounds)."""
    state_path = run_dir / "state.json"
    if not state_path.exists():
        return False

    with open(state_path, encoding="utf-8") as f:
        state = json.load(f)

    consecutive_failures = state.get("consecutive_failures", 0)
    return consecutive_failures >= stagnation_threshold


def get_run_champion(run_dir: Path) -> Optional[dict]:
    """Get the champion config and score from a completed run."""
    state_path = run_dir / "state.json"
    config_path = run_dir / "formula_config.json"

    if not state_path.exists() or not config_path.exists():
        return None

    with open(state_path, encoding="utf-8") as f:
        state = json.load(f)
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    champion_score = state.get("champion_score", -1e308)
    champion_robust_score = state.get("champion_robust_score", -1e308)

    if champion_score == -1e308:
        return None

    return {
        "run_id": run_dir.name,
        "champion_score": champion_score,
        "champion_robust_score": champion_robust_score,
        "config": config,
        "formula": config.get("formula", []),
        "maxPositions": config.get("maxPositions"),
        "takeProfit": config.get("takeProfit"),
        "stopLoss": config.get("stopLoss"),
        "trailingStopLoss": config.get("trailingStopLoss"),
        "total_iterations": state.get("current_iter", 0),
        "direction_status": state.get("direction_status", "UNKNOWN"),
        "champion_metrics": state.get("champion_metrics", {}),
        "champion_windows": state.get("champion_windows", {}),
    }


def build_tree_leaderboard(tree_dir: Path) -> list[dict]:
    """Build leaderboard from all runs in a tree."""
    runs_dir = tree_dir / "runs"
    if not runs_dir.exists():
        return []

    champions = []
    for run_dir in sorted(runs_dir.iterdir()):
        if run_dir.is_dir() and run_dir.name.startswith("run-"):
            champion = get_run_champion(run_dir)
            if champion:
                champions.append(champion)

    champions.sort(key=lambda c: c["champion_robust_score"], reverse=True)

    leaderboard_path = tree_dir / "leaderboard.json"
    leaderboard = {
        "tree_id": tree_dir.name,
        "generated_at": datetime.now().isoformat(),
        "total_runs": len(champions),
        "champions": champions,
    }
    with open(leaderboard_path, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=2)

    return champions


def print_leaderboard(champions: list[dict]) -> None:
    """Print leaderboard to console."""
    if not champions:
        print("\n  (无有效 champion)")
        return

    print(f"\n{'='*70}")
    print(f"  树级 Leaderboard - Top {len(champions)}")
    print(f"{'='*70}")
    print(f"{'Rank':>4}  {'Run':>10}  {'Robust':>8}  {'Score':>8}  {'Iter':>6}  {'Status':>8}  Formula")
    print(f"{'-'*70}")

    for rank, c in enumerate(champions, 1):
        formula_summary = " + ".join(c["formula"][:3])
        if len(c["formula"]) > 3:
            formula_summary += f" ...(+{len(c['formula'])-3})"

        print(
            f"{rank:>4}  {c['run_id']:>10}  "
            f"{c['champion_robust_score']:>8.4f}  "
            f"{c['champion_score']:>8.4f}  "
            f"{c['total_iterations']:>6}  "
            f"{c['direction_status']:>8}  "
            f"{formula_summary}"
        )

    print(f"{'-'*70}")
    if champions:
        best = champions[0]
        print(f"\n  最佳: {best['run_id']} robust={best['champion_robust_score']:.4f}")
        print(f"  公式: {best['formula']}")


def main() -> None:
    args = parse_args()

    tree_dir = resolve_tree_dir(args.tree)
    print(f"\n{'='*70}")
    print(f"  树级长跑调度器")
    print(f"  树: {tree_dir.name}")
    print(f"{'='*70}")

    profile = load_tree_profile_from_dir(tree_dir)
    if profile is None:
        print(f"错误：无法加载树配置：{tree_dir}", file=sys.stderr)
        sys.exit(1)

    errors = validate_profile(profile)
    if errors:
        print(f"警告：profile 校验问题: {errors}")

    run_policy = get_run_policy(profile)

    num_restarts = args.restarts or run_policy.get("num_restarts", 5)
    rounds_per_run = args.rounds or run_policy.get("rounds_per_run", 500)
    restart_on_stagnation = args.stagnation or run_policy.get("restart_on_stagnation", 50)

    print(f"\n  运行策略:")
    print(f"    重启次数: {num_restarts}")
    print(f"    每轮运行: {rounds_per_run} 轮")
    print(f"    停滞阈值: {restart_on_stagnation} 轮无 keep 触发重启")
    print(f"    Mock 模式: {args.mock}")
    print()

    if args.mock:
        os.environ["JQKA_MOCK_MODE"] = "1"

    start_run = 1
    if args.continue_from:
        existing_runs = sorted([d.name for d in (tree_dir / "runs").iterdir() if d.is_dir() and d.name.startswith("run-")])
        if args.continue_from in existing_runs:
            start_run = int(args.continue_from.split("-")[1])
            print(f"  从 {args.continue_from} 继续...")
        else:
            print(f"  警告：找不到 {args.continue_from}，从头开始")

    completed_runs = []

    for run_n in range(start_run, num_restarts + 1):
        run_id = f"run-{run_n:03d}"
        print(f"\n{'='*70}")
        print(f"  [{run_n}/{num_restarts}] 启动 {run_id}")
        print(f"{'='*70}")

        run_dir = setup_run(tree_dir, run_id, profile, args)

        keep_count = 0
        stagnation_counter = 0
        early_stop = False

        for round_n in range(1, rounds_per_run + 1):
            mutation_summary = f"tree_run:{run_id} round:{round_n}"

            exit_code = run_single_iteration(run_dir, mutation_summary)

            sleep_time = random.uniform(5, 15)
            time.sleep(sleep_time)

            if exit_code == 0:
                keep_count += 1
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            if round_n % 50 == 0 or round_n == 1:
                state_path = run_dir / "state.json"
                if state_path.exists():
                    with open(state_path, encoding="utf-8") as f:
                        state = json.load(f)
                    score = state.get("champion_score", -1e308)
                    robust = state.get("champion_robust_score", -1e308)
                    print(f"    [{round_n}/{rounds_per_run}] keep={keep_count} stagnation={stagnation_counter} score={score:.4f} robust={robust:.4f}")

            if stagnation_counter >= restart_on_stagnation:
                print(f"    ⚠ 停滞 {stagnation_counter} 轮无 keep，提前结束 {run_id}")
                early_stop = True
                break

        champion = get_run_champion(run_dir)
        if champion:
            completed_runs.append(champion)
            print(f"  ✓ {run_id} 完成: {champion['total_iterations']} 轮, keep={keep_count}, robust={champion['champion_robust_score']:.4f}")
        else:
            print(f"  ✗ {run_id} 无有效 champion")

        if early_stop and run_n < num_restarts:
            print(f"  → 准备下一个 restart...")

    print(f"\n{'='*70}")
    print(f"  所有 {num_restarts} 个 run 完成")
    print(f"{'='*70}")

    champions = build_tree_leaderboard(tree_dir)
    print_leaderboard(champions)

    leaderboard_path = tree_dir / "leaderboard.json"
    print(f"\n  Leaderboard: {leaderboard_path}")
    print()


if __name__ == "__main__":
    main()
