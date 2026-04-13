#!/usr/bin/env python3
"""
run_iteration.py - 单次迭代执行器

agent 改完 strategy.py 后调用本脚本：
  预检查 → 提交回测 → 等待结果 → 评分 → keep/rollback → 写 history/

Usage:
    python run_iteration.py --base <实验目录> --mutation-summary "改了什么"

Exit code:
    0 = keep
    1 = rollback
    2 = crash
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from ricequant_executor import run_backtest, fetch_results, wait_for_completion, BacktestTimeoutError, BacktestFailedError
from scorer import parse_backtest_result, calculate_score, decide_keep_rollback, ParsedMetrics
from preflight_checker import run_all_checks

AUTORESEARCH_DIR = Path(__file__).parent
TSV_HEADER = "iter\tcommit\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\n"


# ── Git 工具 ──────────────────────────────────────────────────────────────────

def _git(args: list, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=str(cwd), capture_output=True, text=True)


def _git_commit(base: Path, iter_id: str, mutation: str) -> str:
    """git add strategy.py && git commit，返回短 commit hash（失败返回空字符串）"""
    _git(["add", "strategy.py"], cwd=base)
    msg = f"iter_{iter_id}: {mutation}" if mutation else f"iter_{iter_id}"
    r = _git(["commit", "-m", msg], cwd=base)
    if r.returncode != 0:
        # 可能没有变更（内容未改），不报错
        return ""
    r2 = _git(["rev-parse", "--short", "HEAD"], cwd=base)
    return r2.stdout.strip() if r2.returncode == 0 else ""


def _git_rollback_to_champion(base: Path, champion_iter: str) -> None:
    """把 strategy.py 恢复到 champion 版本对应的 git commit"""
    champion_json = base / "history" / f"{champion_iter}.json"
    if not champion_json.exists():
        return
    with open(champion_json, encoding="utf-8") as f:
        data = json.load(f)
    commit = data.get("commit", "")
    if commit:
        _git(["checkout", commit, "--", "strategy.py"], cwd=base)
    else:
        print(f"[rollback] 警告：champion {champion_iter} 无 commit hash，strategy.py 未恢复", flush=True)


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def append_tsv(base: Path, row: dict) -> None:
    tsv = base / "history" / "iterations.tsv"
    line = "\t".join([
        str(row.get("iter", "")),
        str(row.get("commit", "")),
        str(row.get("backtest_id", "")),
        str(row.get("status", "")),
        f"{row.get('annual_return', 0):.4f}",
        f"{row.get('max_drawdown', 0):.4f}",
        f"{row.get('sharpe', 0):.4f}",
        f"{row.get('score', 0):.6f}",
        str(row.get("decision", "")),
        str(row.get("mutation", "")),
    ]) + "\n"
    with open(tsv, "a", encoding="utf-8") as f:
        f.write(line)


def _recover_state(base: Path, state: dict) -> dict:
    """
    重启恢复：检查 state.json 与 history/ 的一致性，修正中间状态。

    崩溃场景：
    - state["current_iter"] 已 +1，但对应的 history/NNNN.json 未写入
      → 说明上次在写 history 之前崩溃，回退 current_iter
    - champion_iter 指向的 history 文件不存在
      → champion 记录丢失，清空 champion 信息（下一轮会重新建立）
    """
    history_dir = base / "history"
    history_dir.mkdir(parents=True, exist_ok=True)

    # 找出 history/ 里实际存在的最大 iter 编号（排除 0000_baseline.json）
    completed_iters = set()
    for f in history_dir.glob("*.json"):
        stem = f.stem  # e.g. "0003" or "0000_baseline"
        if stem.isdigit():
            completed_iters.add(int(stem))

    current_iter = state.get("current_iter", 0)
    champion_iter_str = state.get("champion_iter", "")

    # 检查：current_iter - 1 是否已有对应 history 文件
    # 如果没有，说明上次迭代在写 history 前崩溃了，需要回退
    if current_iter > 0:
        last_iter = current_iter - 1
        if last_iter not in completed_iters:
            print(
                f"[recover] 检测到不一致：current_iter={current_iter} 但 "
                f"history/{last_iter:04d}.json 不存在，回退 current_iter → {last_iter}",
                flush=True,
            )
            state["current_iter"] = last_iter
            # 同时回退 strategy.py 到 champion 版本（上次改动未完成）
            if champion_iter_str:
                _git_rollback_to_champion(base, champion_iter_str)
                print(f"[recover] strategy.py 已恢复到 champion {champion_iter_str}", flush=True)
            save_json(base / "state.json", state)

    # 检查：champion_iter 对应的 history 文件是否存在
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
            save_json(base / "state.json", state)

    return state


def main():
    parser = argparse.ArgumentParser(description="执行单次迭代")
    parser.add_argument("--base", required=True, help="实验目录路径")
    parser.add_argument("--mutation-summary", default="", help="本轮改动摘要")
    args = parser.parse_args()

    base = Path(args.base)
    state = load_json(base / "state.json")
    state = _recover_state(base, state)
    cfg = load_json(base / "seed_config.json")

    iter_n = state["current_iter"]
    iter_id = f"{iter_n:04d}"
    strategy_id = state["strategy_id"]
    strategy_file = str(base / "strategy.py")
    bt_cfg = cfg["backtest"]
    obj_cfg = cfg.get("objective", {})

    champion_score = float(state.get("champion_score", float("-inf")))
    champion_metrics_raw = state.get("champion_metrics")
    champion_metrics = None
    if champion_metrics_raw:
        champion_metrics = ParsedMetrics(
            status=champion_metrics_raw.get("status", ""),
            backtest_id=champion_metrics_raw.get("backtest_id", ""),
            total_return=0.0,
            annual_return=champion_metrics_raw.get("annual_return", 0.0),
            max_drawdown=champion_metrics_raw.get("max_drawdown", 0.0),
            sharpe=champion_metrics_raw.get("sharpe", 0.0),
            sortino=champion_metrics_raw.get("sortino", 0.0),
            information_ratio=champion_metrics_raw.get("information_ratio", 0.0),
            alpha=0.0, beta=0.0,
        )

    start_time = datetime.now()
    decision = "crash"
    backtest_id = ""
    metrics = None
    score = float("-inf")
    reason = ""

    # ── 1. 预检查 ──────────────────────────────────────────────────────────
    passed, reasons = run_all_checks(strategy_file)
    if not passed:
        reason = f"preflight failed: {reasons}"
        print(f"[iter_{iter_id}] {reason}")
        _write_result(base, iter_id, backtest_id, "preflight_failed", 0, 0, 0, float("-inf"),
                      "crash", reason, args.mutation_summary, start_time)
        _update_state(state, base, iter_n, "crash", champion_score, None, None)
        sys.exit(2)
    print(f"[iter_{iter_id}] preflight OK")

    # ── 2. 提交回测 ────────────────────────────────────────────────────────
    try:
        submit = run_backtest(
            strategy_id=strategy_id,
            strategy_file=strategy_file,
            start_date=bt_cfg.get("start_date"),
            end_date=bt_cfg.get("end_date"),
            capital=str(bt_cfg.get("capital", "100000")),
            freq=bt_cfg.get("freq", "day"),
            benchmark=bt_cfg.get("benchmark", "000300.XSHG"),
            no_wait=True,
        )
        backtest_id = submit.get("backtest_id", "")
        print(f"[iter_{iter_id}] backtest_id={backtest_id}")
    except Exception as e:
        reason = f"submit failed: {e}"
        print(f"[iter_{iter_id}] {reason}")
        _write_result(base, iter_id, backtest_id, "error", 0, 0, 0, float("-inf"),
                      "crash", reason, args.mutation_summary, start_time)
        _update_state(state, base, iter_n, "crash", champion_score, None, None)
        sys.exit(2)

    # ── 3. 等待结果 ────────────────────────────────────────────────────────
    try:
        wait_result = wait_for_completion(
            strategy_id=strategy_id,
            backtest_id=backtest_id,
            max_wait_seconds=cfg.get("loop", {}).get("max_wait_seconds", 600),
            poll_interval=10,
        )
    except (BacktestTimeoutError, BacktestFailedError) as e:
        reason = str(e)
        print(f"[iter_{iter_id}] {reason}")
        _write_result(base, iter_id, backtest_id, "error", 0, 0, 0, float("-inf"),
                      "crash", reason, args.mutation_summary, start_time)
        _update_state(state, base, iter_n, "crash", champion_score, None, None)
        sys.exit(2)

    # ── 4. 解析指标 + 评分 ─────────────────────────────────────────────────
    fetch = fetch_results(strategy_id=strategy_id, backtest_id=backtest_id)
    parse_input = {
        "status": fetch.get("status") or wait_result.get("status", "normal_exit"),
        "backtestId": backtest_id,
        "annualReturn": fetch.get("annualReturn", 0),
        "totalReturn": fetch.get("totalReturn", 0),
        "maxDrawdown": fetch.get("maxDrawdown", 0),
        "sharpe": fetch.get("sharpe", 0),
        "winRate": fetch.get("winRate", 0),
        "alpha": fetch.get("alpha", 0),
        "beta": fetch.get("beta", 0),
    }
    metrics = parse_backtest_result(parse_input)
    score = calculate_score(metrics, obj_cfg.get("weights"))
    decision, reason = decide_keep_rollback(
        new_score=score,
        champion_score=champion_score,
        new_metrics=metrics,
        champion_metrics=champion_metrics,
        hard_constraints=obj_cfg.get("hard_constraints"),
    )

    end_time = datetime.now()
    print(f"[iter_{iter_id}] score={score:.4f} champion={champion_score:.4f} "
          f"annual={metrics.annual_return:.2%} dd={metrics.max_drawdown:.2%} sharpe={metrics.sharpe:.2f}")
    print(f"[iter_{iter_id}] 决策: {decision} — {reason}")

    # ── 5. git commit / rollback ───────────────────────────────────────────
    commit_hash = ""
    if decision == "keep":
        commit_hash = _git_commit(base, iter_id, args.mutation_summary)
        if commit_hash:
            print(f"[iter_{iter_id}] git commit {commit_hash}")
    elif decision == "rollback":
        champion_iter = state.get("champion_iter", "")
        if champion_iter:
            _git_rollback_to_champion(base, champion_iter)
            print(f"[iter_{iter_id}] git rollback → champion {champion_iter}")

    # ── 6. 写 history/ ─────────────────────────────────────────────────────
    _write_result(base, iter_id, backtest_id, metrics.status,
                  metrics.annual_return, metrics.max_drawdown, metrics.sharpe,
                  score, decision, reason, args.mutation_summary, start_time, end_time, fetch,
                  commit=commit_hash)

    # ── 7. 更新 state.json ─────────────────────────────────────────────────
    new_champion_metrics = None
    if decision == "keep":
        new_champion_metrics = {
            "annual_return": metrics.annual_return,
            "max_drawdown": metrics.max_drawdown,
            "sharpe": metrics.sharpe,
            "sortino": metrics.sortino,
            "information_ratio": metrics.information_ratio,
            "status": metrics.status,
            "backtest_id": backtest_id,
        }
    _update_state(state, base, iter_n, decision, score if decision == "keep" else champion_score,
                  iter_id if decision == "keep" else None, new_champion_metrics)

    sys.exit(0 if decision == "keep" else 1)


def _write_result(base, iter_id, backtest_id, status, annual_return, max_drawdown, sharpe,
                  score, decision, reason, mutation, start_time, end_time=None, fetch=None, commit=""):
    record = {
        "iter": iter_id,
        "commit": commit,
        "backtest_id": backtest_id,
        "status": status,
        "start_time": start_time.isoformat(),
        "end_time": (end_time or datetime.now()).isoformat(),
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
        "score": score,
        "decision": decision,
        "reason": reason,
        "mutation": mutation,
    }
    if fetch:
        record["fetch_result"] = fetch
    save_json(base / "history" / f"{iter_id}.json", record)
    append_tsv(base, record)


def _update_state(state, base, iter_n, decision, new_champion_score, new_champion_iter, new_champion_metrics):
    state["current_iter"] = iter_n + 1
    state["last_update"] = datetime.now().isoformat()
    if decision == "keep":
        state["champion_score"] = new_champion_score
        state["champion_iter"] = new_champion_iter
        state["champion_metrics"] = new_champion_metrics
        state["consecutive_failures"] = 0
    elif decision in ("rollback", "crash"):
        state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1
    save_json(base / "state.json", state)


if __name__ == "__main__":
    main()
