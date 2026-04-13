#!/usr/bin/env python3
"""
run_iteration.py — 向导式策略单次迭代执行器

对 wizard_config.json 执行一次变异→回测→评分→keep/rollback 迭代。

设计理念（借鉴 karpathy/autoresearch）：
- wizard_config.json 永远是最优配置
- 成功 → 覆盖 wizard_config.json + git commit
- 失败 → wizard_config.json 保持不变，不 commit
- iterations.tsv 记录所有结果（不 commit）

Usage:
    python run_iteration.py \\
        --base experiments/<experiment_name> \\
        --mutation-summary "调整 pe_ratio 阈值" \\
        [--mutation-type adjust_filter_threshold]

Exit codes:
    0 = keep（新配置优于 champion，已更新并 commit）
    1 = rollback（新配置不如 champion，已恢复，不 commit）
    2 = crash（执行过程中发生异常）
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from wizard_executor import (
    update_strategy,
    run_backtest,
    wait_for_completion,
    fetch_results,
    BacktestTimeoutError,
    BacktestFailedError,
    WizardExecutorError,
)
from scorer import (
    parse_backtest_result,
    calculate_score,
    decide_keep_rollback,
    ParsedMetrics,
)
from wizard_mutator import (
    mutate,
    smart_mutate,
    MUTATION_TYPES,
    estimate_candidate_pool_size,
)

TSV_HEADER = (
    "iter\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\n"
)


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def git_commit(base: Path, message: str) -> bool:
    try:
        subprocess.run(["git", "add", "."], cwd=base, check=True, capture_output=True)
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=base,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return True
        elif "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            return False
        else:
            print(f"[git] commit 失败: {result.stderr}", flush=True)
            return False
    except subprocess.CalledProcessError as e:
        print(f"[git] add 失败: {e}", flush=True)
        return False
    except Exception as e:
        print(f"[git] 异常: {e}", flush=True)
        return False


def git_restore(base: Path, filename: str) -> bool:
    """恢复文件到上一个 commit 的状态"""
    try:
        result = subprocess.run(
            ["git", "checkout", "HEAD", filename],
            cwd=base,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[git] restore 失败: {e}", flush=True)
        return False


def append_tsv(base: Path, row: dict) -> None:
    tsv = base / "iterations.tsv"
    write_header = not tsv.exists()
    line = (
        "\t".join(
            [
                str(row.get("iter", "")),
                str(row.get("backtest_id", "")),
                str(row.get("status", "")),
                f"{row.get('annual_return', 0):.4f}",
                f"{row.get('max_drawdown', 0):.4f}",
                f"{row.get('sharpe', 0):.4f}",
                f"{row.get('score', 0):.6f}",
                str(row.get("decision", "")),
                str(row.get("mutation", "")),
            ]
        )
        + "\n"
    )
    with open(tsv, "a", encoding="utf-8") as f:
        if write_header:
            f.write(TSV_HEADER)
        f.write(line)


def update_state(state: dict, base: Path, iter_n: int, decision: str, score: float) -> None:
    state["current_iter"] = iter_n + 1
    state["last_update"] = datetime.now().isoformat()
    if decision == "keep":
        state["champion_score"] = score
        state["consecutive_failures"] = 0
    else:
        state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1
    save_json(base / "state.json", state)


def main():
    parser = argparse.ArgumentParser(
        description="向导式策略单次迭代执行器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--base",
        required=True,
        help="实验目录路径（含 state.json 和 wizard_config.json）",
    )
    parser.add_argument("--mutation-summary", required=True, help="本轮变异的描述（人类可读）")
    parser.add_argument(
        "--mutation-type",
        choices=MUTATION_TYPES,
        default=None,
        help=f"变异类型（可选），不指定时随机选择。可选值: {', '.join(MUTATION_TYPES)}",
    )
    args = parser.parse_args()

    base = Path(args.base)
    mutation_summary = args.mutation_summary
    mutation_type_arg = args.mutation_type

    state_path = base / "state.json"
    if not state_path.exists():
        print(f"[ERROR] state.json 不存在: {state_path}", flush=True)
        sys.exit(2)

    state = load_json(state_path)
    iter_n = state.get("current_iter", 0)
    iter_id = f"{iter_n:04d}"
    strategy_id = state.get("strategy_id", "")

    if not strategy_id:
        print(f"[iter_{iter_id}] [ERROR] state.json 中 strategy_id 为空", flush=True)
        sys.exit(2)

    consecutive_failures = state.get("consecutive_failures", 0)
    if consecutive_failures >= 5:
        print(
            f"[iter_{iter_id}] ⚠️  警告：已连续失败 {consecutive_failures} 次，建议检查策略配置或手动干预",
            flush=True,
        )

    print(f"[iter_{iter_id}] 开始迭代 strategy_id={strategy_id}", flush=True)

    wizard_config_path = base / "wizard_config.json"
    if not wizard_config_path.exists():
        print(
            f"[iter_{iter_id}] [ERROR] wizard_config.json 不存在: {wizard_config_path}", flush=True
        )
        sys.exit(2)

    champion_config = load_json(wizard_config_path)
    champion_score = float(state.get("champion_score", float("-inf")))

    bt_config = champion_config.get("backtest", {})
    obj_cfg = champion_config.get("objective", {})
    loop_cfg = champion_config.get("loop", {})

    candidate_num_min = obj_cfg.get("candidate_num_min", 5)
    candidate_num_max = obj_cfg.get("candidate_num_max", 50)

    start_time = datetime.now()
    backtest_id = ""
    metrics = None
    score = float("-inf")
    reason = ""
    decision = "crash"
    actual_mutation_type = mutation_type_arg or "random"
    new_pool_size = 0

    try:
        current_pool_size = estimate_candidate_pool_size(champion_config)
        print(f"[iter_{iter_id}] 当前候选池预估: {current_pool_size} 只股票", flush=True)

        if current_pool_size < candidate_num_min:
            print(
                f"[iter_{iter_id}] 候选池太少（<{candidate_num_min}），使用 relax_filter",
                flush=True,
            )
        elif current_pool_size > candidate_num_max:
            print(
                f"[iter_{iter_id}] 候选池太多（>{candidate_num_max}），使用 tighten_filter",
                flush=True,
            )

        if mutation_type_arg:
            new_config, mutation_desc = mutate(champion_config, mutation_type_arg)
        else:
            new_config, mutation_desc = smart_mutate(
                champion_config,
                candidate_num_min=candidate_num_min,
                candidate_num_max=candidate_num_max,
            )

        new_pool_size = estimate_candidate_pool_size(new_config)
        print(f"[iter_{iter_id}] 新配置候选池预估: {new_pool_size} 只股票", flush=True)

        actual_mutation_type = (
            mutation_desc.split(":")[0].strip()
            if ":" in mutation_desc
            else (mutation_type_arg or "smart")
        )
        print(f"[iter_{iter_id}] 变异描述: {mutation_desc}", flush=True)

        save_json(wizard_config_path, new_config)
        print(f"[iter_{iter_id}] wizard_config.json 已更新为新配置（待验证）", flush=True)

        print(f"[iter_{iter_id}] 更新策略配置...", flush=True)
        update_strategy(strategy_id, str(wizard_config_path))
        print(f"[iter_{iter_id}] 策略配置更新完成", flush=True)

        print(f"[iter_{iter_id}] 触发回测...", flush=True)
        run_result = run_backtest(strategy_id, bt_config)
        backtest_id = run_result.get("backtest_id", "")
        print(f"[iter_{iter_id}] backtest_id={backtest_id}", flush=True)

        max_wait = loop_cfg.get("max_wait_seconds", 600)
        poll_interval = loop_cfg.get("poll_interval", 15)
        print(f"[iter_{iter_id}] 等待回测完成 max_wait={max_wait}s...", flush=True)
        wait_result = wait_for_completion(
            backtest_id, max_wait=max_wait, poll_interval=poll_interval
        )
        print(f"[iter_{iter_id}] 回测完成 status={wait_result.get('status')}", flush=True)

        print(f"[iter_{iter_id}] 获取回测结果...", flush=True)
        fetch = fetch_results(strategy_id, backtest_id)

        parse_input = {
            "status": fetch.get("status") or wait_result.get("status", ""),
            "backtestId": backtest_id,
            "annualReturn": fetch.get("annualReturn", 0),
            "totalReturn": fetch.get("totalReturn", 0),
            "maxDrawdown": fetch.get("maxDrawdown", 0),
            "sharpe": fetch.get("sharpe", 0),
            "sortino": fetch.get("sortino", 0),
            "informationRatio": fetch.get("informationRatio", 0),
            "alpha": fetch.get("alpha", 0),
            "beta": fetch.get("beta", 0),
        }
        metrics = parse_backtest_result(parse_input)

        weights = obj_cfg.get("weights")
        score = calculate_score(metrics, weights)

        hard_constraints = obj_cfg.get("hard_constraints")
        decision, reason = decide_keep_rollback(
            new_score=score,
            champion_score=champion_score,
            new_metrics=metrics,
            champion_metrics=None,
            hard_constraints=hard_constraints,
        )

        end_time = datetime.now()
        print(
            f"[iter_{iter_id}] score={score:.4f} champion={champion_score:.4f} "
            f"annual={metrics.annual_return:.2%} dd={metrics.max_drawdown:.2%} "
            f"sharpe={metrics.sharpe:.2f} sortino={metrics.sortino:.2f}",
            flush=True,
        )
        print(f"[iter_{iter_id}] 决策: {decision} — {reason}", flush=True)

        append_tsv(
            base,
            {
                "iter": iter_id,
                "backtest_id": backtest_id,
                "status": metrics.status,
                "annual_return": metrics.annual_return,
                "max_drawdown": metrics.max_drawdown,
                "sharpe": metrics.sharpe,
                "score": score,
                "decision": decision,
                "mutation": mutation_desc,
            },
        )

        if decision == "keep":
            update_state(state, base, iter_n, "keep", score)

            git_msg = f"keep: iter_{iter_id} score={score:.4f} annual={metrics.annual_return:.2%} dd={metrics.max_drawdown:.2%} pool={new_pool_size}\n{mutation_desc}"
            git_commit(base, git_msg)

            print(f"[iter_{iter_id}] ✅ keep — 新 champion score={score:.4f}", flush=True)
            sys.exit(0)
        else:
            git_restore(base, "wizard_config.json")
            print(f"[iter_{iter_id}] wizard_config.json 已恢复到 champion", flush=True)

            update_state(state, base, iter_n, "rollback", champion_score)

            print(f"[iter_{iter_id}] ↩️  rollback — {reason}（不 commit）", flush=True)
            sys.exit(1)

    except Exception as e:
        end_time = datetime.now()
        crash_reason = f"{type(e).__name__}: {e}"
        print(f"[iter_{iter_id}] [CRASH] {crash_reason}", flush=True)

        try:
            append_tsv(
                base,
                {
                    "iter": iter_id,
                    "backtest_id": backtest_id,
                    "status": "crash",
                    "annual_return": 0.0,
                    "max_drawdown": 0.0,
                    "sharpe": 0.0,
                    "score": float("-inf"),
                    "decision": "crash",
                    "mutation": mutation_summary,
                },
            )
        except Exception as write_err:
            print(f"[iter_{iter_id}] [CRASH] 写 crash 记录失败: {write_err}", flush=True)

        try:
            git_restore(base, "wizard_config.json")
            print(f"[iter_{iter_id}] wizard_config.json 已恢复", flush=True)
        except Exception as restore_err:
            print(f"[iter_{iter_id}] [CRASH] restore 失败: {restore_err}", flush=True)

        try:
            update_state(state, base, iter_n, "crash", champion_score)
        except Exception as state_err:
            print(f"[iter_{iter_id}] [CRASH] 更新 state.json 失败: {state_err}", flush=True)

        sys.exit(2)


if __name__ == "__main__":
    main()
