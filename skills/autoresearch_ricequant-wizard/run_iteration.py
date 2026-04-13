#!/usr/bin/env python3
"""
run_iteration.py — 向导式策略单次迭代执行器

对 wizard_config.json（向导式策略参数）执行一次变异→回测→评分→keep/rollback 迭代。

版本管理：
- 每次迭代完成后自动 git commit，方便追溯历史
- keep: commit message 包含新 champion 信息
- rollback: commit message 包含回滚原因

Usage:
    python run_iteration.py \\
        --base experiments/<experiment_name> \\
        --mutation-summary "调整 pe_ratio 阈值" \\
        [--mutation-type adjust_filter_threshold]

Exit codes:
    0 = keep（新配置优于 champion，已更新）
    1 = rollback（新配置不如 champion，已恢复）
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

TSV_HEADER = "iter\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\n"


# ── 工具函数 ──────────────────────────────────────────────────────────────────


def load_json(path: Path) -> dict:
    """读取 JSON 文件，返回 dict。"""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    """写入 JSON 文件，自动创建父目录。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def git_commit(base: Path, message: str) -> bool:
    """
    执行 git add + commit。

    Args:
        base: 实验目录路径
        message: commit message

    Returns:
        bool: True 表示成功，False 表示失败或无变更
    """
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
        elif (
            "nothing to commit" in result.stdout or "nothing to commit" in result.stderr
        ):
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


def append_tsv(base: Path, row: dict) -> None:
    """
    追加一行到 history/iterations.tsv。
    若文件不存在则先写入表头。

    Columns: iter, backtest_id, status, annual_return, max_drawdown, sharpe, score, decision, mutation
    """
    tsv = base / "history" / "iterations.tsv"
    tsv.parent.mkdir(parents=True, exist_ok=True)

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


# ── 重启恢复 ──────────────────────────────────────────────────────────────────


def _recover_state(base: Path, state: dict) -> dict:
    """
    检查 state.json 与 history/ 目录的一致性，修正中间状态。

    场景 1：current_iter > 0 但 history/<current_iter-1>.json 不存在
        → 上次迭代在写 history 前崩溃，回退 current_iter
        → 从 history/<champion_iter>_config.json 恢复 wizard_config.json

    场景 2：champion_iter 对应的 history 文件不存在
        → champion 记录丢失，清空 champion 信息
    """
    history_dir = base / "history"
    history_dir.mkdir(parents=True, exist_ok=True)

    current_iter = state.get("current_iter", 0)
    champion_iter_str = state.get("champion_iter", "")
    changed = False

    # 场景 1：检查 current_iter - 1 是否有对应 history 文件
    if current_iter > 0:
        last_iter_id = f"{current_iter - 1:04d}"
        last_json = history_dir / f"{last_iter_id}.json"
        if not last_json.exists():
            print(
                f"[recover] 检测到不一致：current_iter={current_iter} 但 "
                f"history/{last_iter_id}.json 不存在，回退 current_iter → {current_iter - 1}",
                flush=True,
            )
            state["current_iter"] = current_iter - 1
            changed = True

            # 从 champion 配置恢复 wizard_config.json
            if champion_iter_str:
                champion_config_path = history_dir / f"{champion_iter_str}_config.json"
                if champion_config_path.exists():
                    champion_cfg = load_json(champion_config_path)
                    save_json(base / "wizard_config.json", champion_cfg)
                    print(
                        f"[recover] wizard_config.json 已从 champion {champion_iter_str} 恢复",
                        flush=True,
                    )
                else:
                    print(
                        f"[recover] 警告：champion config {champion_config_path} 不存在，wizard_config.json 未恢复",
                        flush=True,
                    )

    # 场景 2：检查 champion_iter 对应的 history 文件是否存在
    if champion_iter_str:
        champion_json = history_dir / f"{champion_iter_str}.json"
        if not champion_json.exists():
            print(
                f"[recover] champion_iter={champion_iter_str} 的 history 文件不存在，清空 champion 信息",
                flush=True,
            )
            state["champion_score"] = float("-inf")
            state["champion_iter"] = ""
            state["champion_metrics"] = None
            changed = True

    if changed:
        save_json(base / "state.json", state)

    return state


# ── 写入历史记录 ──────────────────────────────────────────────────────────────


def _write_result(
    base: Path,
    iter_id: str,
    backtest_id: str,
    status: str,
    annual_return: float,
    max_drawdown: float,
    sharpe: float,
    sortino: float,
    information_ratio: float,
    score: float,
    decision: str,
    reason: str,
    mutation: str,
    mutation_type: str,
    start_time: datetime,
    end_time: datetime = None,
    fetch: dict = None,
) -> None:
    """
    写入 history/<iter_id>.json 并追加到 iterations.tsv。
    """
    record = {
        "iter": iter_id,
        "backtest_id": backtest_id,
        "status": status,
        "start_time": start_time.isoformat(),
        "end_time": (end_time or datetime.now()).isoformat(),
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
        "sortino": sortino,
        "information_ratio": information_ratio,
        "score": score,
        "decision": decision,
        "reason": reason,
        "mutation": mutation,
        "mutation_type": mutation_type,
    }
    if fetch:
        record["fetch_result"] = fetch

    save_json(base / "history" / f"{iter_id}.json", record)
    append_tsv(base, record)


# ── 更新状态 ──────────────────────────────────────────────────────────────────


def _update_state(
    state: dict,
    base: Path,
    iter_n: int,
    decision: str,
    new_champion_score: float,
    new_champion_iter: str,
    new_champion_metrics: dict,
) -> None:
    """
    更新 state.json：
    - current_iter = iter_n + 1
    - last_update = now
    - keep: 更新 champion 信息，重置 consecutive_failures
    - rollback/crash: consecutive_failures += 1
    """
    state["current_iter"] = iter_n + 1
    state["last_update"] = datetime.now().isoformat()

    if decision == "keep":
        state["champion_score"] = new_champion_score
        state["champion_iter"] = new_champion_iter
        state["champion_metrics"] = new_champion_metrics
        state["consecutive_failures"] = 0
    else:
        # rollback 或 crash
        state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1

    save_json(base / "state.json", state)


# ── 主流程 ────────────────────────────────────────────────────────────────────


def main():
    # 4.1 CLI 参数解析
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
    parser.add_argument(
        "--mutation-summary", required=True, help="本轮变异的描述（人类可读）"
    )
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

    # 4.2 读取 state.json
    state_path = base / "state.json"
    if not state_path.exists():
        print(f"[ERROR] state.json 不存在: {state_path}", flush=True)
        sys.exit(2)

    state = load_json(state_path)

    # 4.3 重启恢复
    state = _recover_state(base, state)

    iter_n = state.get("current_iter", 0)
    iter_id = f"{iter_n:04d}"
    strategy_id = state.get("strategy_id", "")

    if not strategy_id:
        print(f"[iter_{iter_id}] [ERROR] state.json 中 strategy_id 为空", flush=True)
        sys.exit(2)

    # 连续失败警告
    consecutive_failures = state.get("consecutive_failures", 0)
    if consecutive_failures >= 5:
        print(
            f"[iter_{iter_id}] ⚠️  警告：已连续失败 {consecutive_failures} 次，"
            "建议检查策略配置或手动干预",
            flush=True,
        )

    print(f"[iter_{iter_id}] 开始迭代 strategy_id={strategy_id}", flush=True)

    # 4.4 读取 champion 配置
    wizard_config_path = base / "wizard_config.json"
    if not wizard_config_path.exists():
        print(
            f"[iter_{iter_id}] [ERROR] wizard_config.json 不存在: {wizard_config_path}",
            flush=True,
        )
        sys.exit(2)

    champion_config = load_json(wizard_config_path)

    # 从 wizard_config.json 中提取 backtest/objective/loop 配置
    bt_config = champion_config.get("backtest", {})
    obj_cfg = champion_config.get("objective", {})
    loop_cfg = champion_config.get("loop", {})

    candidate_num_min = obj_cfg.get("candidate_num_min", 5)
    candidate_num_max = obj_cfg.get("candidate_num_max", 50)

    # 重建 champion_metrics（从 state.json 中的 dict 恢复为 ParsedMetrics）
    champion_score = float(state.get("champion_score", float("-inf")))
    champion_metrics_raw = state.get("champion_metrics")
    champion_metrics = None
    if champion_metrics_raw:
        champion_metrics = ParsedMetrics(
            status=champion_metrics_raw.get("status", ""),
            backtest_id=champion_metrics_raw.get("backtest_id", ""),
            total_return=float(champion_metrics_raw.get("total_return", 0.0)),
            annual_return=float(champion_metrics_raw.get("annual_return", 0.0)),
            max_drawdown=float(champion_metrics_raw.get("max_drawdown", 0.0)),
            sharpe=float(champion_metrics_raw.get("sharpe", 0.0)),
            sortino=float(champion_metrics_raw.get("sortino", 0.0)),
            information_ratio=float(champion_metrics_raw.get("information_ratio", 0.0)),
            alpha=float(champion_metrics_raw.get("alpha", 0.0)),
            beta=float(champion_metrics_raw.get("beta", 0.0)),
        )

    start_time = datetime.now()
    backtest_id = ""
    metrics = None
    score = float("-inf")
    reason = ""
    decision = "crash"
    actual_mutation_type = mutation_type_arg or "random"

    try:
        # 步骤 6：变异配置（使用 smart_mutate 确保候选池数量合理）
        current_pool_size = estimate_candidate_pool_size(champion_config)
        print(
            f"[iter_{iter_id}] 当前候选池预估: {current_pool_size} 只股票", flush=True
        )

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

        # 步骤 7：保存临时配置快照到 history/<iter_id>_config.json
        iter_config_path = base / "history" / f"{iter_id}_config.json"
        save_json(iter_config_path, new_config)
        print(f"[iter_{iter_id}] 配置快照已保存: {iter_config_path}", flush=True)

        # 步骤 8：更新策略配置
        print(f"[iter_{iter_id}] 更新策略配置...", flush=True)
        update_strategy(strategy_id, str(iter_config_path))
        print(f"[iter_{iter_id}] 策略配置更新完成", flush=True)

        # 步骤 9：触发回测
        print(f"[iter_{iter_id}] 触发回测...", flush=True)
        run_result = run_backtest(strategy_id, bt_config)
        backtest_id = run_result.get("backtest_id", "")
        print(f"[iter_{iter_id}] backtest_id={backtest_id}", flush=True)

        # 步骤 10：等待回测完成
        max_wait = loop_cfg.get("max_wait_seconds", 600)
        poll_interval = loop_cfg.get("poll_interval", 15)
        print(f"[iter_{iter_id}] 等待回测完成 max_wait={max_wait}s...", flush=True)
        wait_result = wait_for_completion(
            backtest_id, max_wait=max_wait, poll_interval=poll_interval
        )
        print(
            f"[iter_{iter_id}] 回测完成 status={wait_result.get('status')}", flush=True
        )

        # 步骤 11：获取结果
        print(f"[iter_{iter_id}] 获取回测结果...", flush=True)
        fetch = fetch_results(strategy_id, backtest_id)

        # 步骤 12：解析指标
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

        # 步骤 13：计算得分
        weights = obj_cfg.get("weights")
        score = calculate_score(metrics, weights)

        # 步骤 14：决策 keep/rollback
        hard_constraints = obj_cfg.get("hard_constraints")
        decision, reason = decide_keep_rollback(
            new_score=score,
            champion_score=champion_score,
            new_metrics=metrics,
            champion_metrics=champion_metrics,
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

        # 步骤 15：处理 keep/rollback 分支
        if decision == "keep":
            # 4.5 keep 分支：覆盖 wizard_config.json，更新 champion 信息
            save_json(wizard_config_path, new_config)
            print(f"[iter_{iter_id}] wizard_config.json 已更新为新配置", flush=True)

            new_champion_metrics_dict = {
                "status": metrics.status,
                "backtest_id": backtest_id,
                "total_return": metrics.total_return,
                "annual_return": metrics.annual_return,
                "max_drawdown": metrics.max_drawdown,
                "sharpe": metrics.sharpe,
                "sortino": metrics.sortino,
                "information_ratio": metrics.information_ratio,
                "alpha": metrics.alpha,
                "beta": metrics.beta,
            }

            # 4.7 写历史记录
            _write_result(
                base,
                iter_id,
                backtest_id,
                metrics.status,
                metrics.annual_return,
                metrics.max_drawdown,
                metrics.sharpe,
                metrics.sortino,
                metrics.information_ratio,
                score,
                decision,
                reason,
                mutation_desc,
                actual_mutation_type,
                start_time,
                end_time,
                fetch,
            )

            # 4.8 更新 state.json
            _update_state(
                state, base, iter_n, "keep", score, iter_id, new_champion_metrics_dict
            )

            # 4.9 git commit
            git_msg = f"keep: iter_{iter_id} score={score:.4f} annual={metrics.annual_return:.2%} dd={metrics.max_drawdown:.2%} pool={new_pool_size}\n{mutation_desc}"
            git_commit(base, git_msg)

            print(
                f"[iter_{iter_id}] ✅ keep — 新 champion iter={iter_id} score={score:.4f}",
                flush=True,
            )
            sys.exit(0)

        else:
            # 4.6 rollback 分支：恢复 wizard_config.json
            champion_iter_str = state.get("champion_iter", "")
            if champion_iter_str:
                champion_config_path = (
                    base / "history" / f"{champion_iter_str}_config.json"
                )
                if champion_config_path.exists():
                    restored_cfg = load_json(champion_config_path)
                    save_json(wizard_config_path, restored_cfg)
                    print(
                        f"[iter_{iter_id}] wizard_config.json 已恢复到 champion {champion_iter_str}",
                        flush=True,
                    )
                else:
                    print(
                        f"[iter_{iter_id}] 警告：champion config {champion_config_path} 不存在，"
                        "wizard_config.json 保持不变",
                        flush=True,
                    )
            else:
                # 尚无 champion，保持 wizard_config.json 不变
                print(
                    f"[iter_{iter_id}] 尚无 champion，wizard_config.json 保持不变",
                    flush=True,
                )

            # 4.7 写历史记录
            _write_result(
                base,
                iter_id,
                backtest_id,
                metrics.status,
                metrics.annual_return,
                metrics.max_drawdown,
                metrics.sharpe,
                metrics.sortino,
                metrics.information_ratio,
                score,
                decision,
                reason,
                mutation_desc,
                actual_mutation_type,
                start_time,
                end_time,
                fetch,
            )

            # 4.8 更新 state.json
            _update_state(state, base, iter_n, "rollback", champion_score, None, None)

            # 4.9 git commit
            git_msg = f"rollback: iter_{iter_id} score={score:.4f} < champion={champion_score:.4f} pool={new_pool_size}\n{reason}\n{mutation_desc}"
            git_commit(base, git_msg)

            print(f"[iter_{iter_id}] ↩️  rollback — {reason}", flush=True)
            sys.exit(1)

    except Exception as e:
        # 4.10 crash 处理：写 crash 记录，consecutive_failures +1，退出码 2
        end_time = datetime.now()
        crash_reason = f"{type(e).__name__}: {e}"
        print(f"[iter_{iter_id}] [CRASH] {crash_reason}", flush=True)

        try:
            _write_result(
                base,
                iter_id,
                backtest_id,
                "crash",
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                float("-inf"),
                "crash",
                crash_reason,
                mutation_summary,
                mutation_type_arg or "",
                start_time,
                end_time,
                None,
            )
        except Exception as write_err:
            print(
                f"[iter_{iter_id}] [CRASH] 写 crash 记录失败: {write_err}", flush=True
            )

        try:
            _update_state(state, base, iter_n, "crash", champion_score, None, None)
        except Exception as state_err:
            print(
                f"[iter_{iter_id}] [CRASH] 更新 state.json 失败: {state_err}",
                flush=True,
            )

        # git commit crash
        try:
            git_msg = f"crash: iter_{iter_id}\n{crash_reason}\n{mutation_summary}"
            git_commit(base, git_msg)
        except Exception as git_err:
            print(f"[iter_{iter_id}] [CRASH] git commit 失败: {git_err}", flush=True)

        sys.exit(2)


if __name__ == "__main__":
    main()
