#!/usr/bin/env python3
"""
果仁策略自动研究系统 - 单次迭代执行器

执行完整的迭代流程：变异 → 回测 → 评分 → 决策 → 更新状态

用法:
    python run_iteration.py --base experiments/<name> --mutation-summary "..." [--mutation-type <type>]

退出码:
    0: keep（新配置更好）
    1: rollback（新配置不如 champion）
    2: crash（回测失败或超时）
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# 导入本地模块
from scorer import (
    parse_backtest_result,
    calculate_score,
    decide_keep_rollback,
    DEFAULT_WEIGHTS,
    DEFAULT_HARD_CONSTRAINTS,
)
from guorn_mutator import mutate, validate_config
from guorn_executor import run_backtest, GuornExecutorError, BacktestTimeoutError


# ── 工具函数 ──────────────────────────────────────────────────────────────────


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="果仁策略自动研究系统 - 单次迭代执行器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--base",
        required=True,
        help="实验目录路径（如 experiments/my_experiment）",
    )
    parser.add_argument(
        "--mutation-summary",
        required=True,
        help="变异描述（如 '[筛选] 添加市盈率<20'）",
    )
    parser.add_argument(
        "--mutation-type",
        choices=[
            "add_filter",
            "remove_filter",
            "adjust_filter_threshold",
            "add_ranking",
            "adjust_ranking_weight",
            "adjust_holding_num",
            "adjust_rebalance_interval",
            "change_pool",
        ],
        help="变异类型（可选，不指定则随机选择）",
    )
    return parser.parse_args()


def _load_state(base_dir: Path) -> dict:
    """读取 state.json"""
    state_path = base_dir / "state.json"
    if not state_path.exists():
        print(f"错误：state.json 不存在：{state_path}", file=sys.stderr)
        sys.exit(2)
    with open(state_path, encoding="utf-8") as f:
        return json.load(f)


def _save_state(base_dir: Path, state: dict) -> None:
    """保存 state.json"""
    state_path = base_dir / "state.json"
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _load_config(base_dir: Path) -> dict:
    """读取 guorn_config.json"""
    config_path = base_dir / "guorn_config.json"
    if not config_path.exists():
        print(f"错误：guorn_config.json 不存在：{config_path}", file=sys.stderr)
        sys.exit(2)
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def _save_config(base_dir: Path, config: dict) -> None:
    """保存 guorn_config.json"""
    config_path = base_dir / "guorn_config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def _format_iter_id(iter_num: int) -> str:
    """格式化迭代编号（如 0001）"""
    return f"{iter_num:04d}"


def _git(args: list, cwd: Path) -> subprocess.CompletedProcess:
    """执行 git 命令"""
    return subprocess.run(["git"] + args, cwd=str(cwd), capture_output=True, text=True)


def _git_commit(base_dir: Path, iter_id: str, mutation: str) -> str:
    """git add guorn_config.json && git commit，返回短 commit hash"""
    _git(["add", "guorn_config.json"], cwd=base_dir)
    msg = f"iter_{iter_id}: {mutation}" if mutation else f"iter_{iter_id}"
    r = _git(["commit", "-m", msg], cwd=base_dir)
    if r.returncode != 0:
        return ""
    r2 = _git(["rev-parse", "--short", "HEAD"], cwd=base_dir)
    return r2.stdout.strip() if r2.returncode == 0 else ""


def _git_rollback_to_champion(base_dir: Path, champion_iter: str) -> None:
    """把 guorn_config.json 恢复到 champion 版本对应的 git commit"""
    champion_json = base_dir / "history" / f"{champion_iter}.json"
    if not champion_json.exists():
        return
    with open(champion_json, encoding="utf-8") as f:
        data = json.load(f)
    commit = data.get("commit", "")
    if commit:
        _git(["checkout", commit, "--", "guorn_config.json"], cwd=base_dir)
    else:
        print(
            f"[rollback] 警告：champion {champion_iter} 无 commit hash，guorn_config.json 未恢复",
            flush=True,
        )


# ── 主流程 ────────────────────────────────────────────────────────────────────


def main() -> None:
    args = _parse_args()
    base_dir = Path(args.base).resolve()

    if not base_dir.exists():
        print(f"错误：实验目录不存在：{base_dir}", file=sys.stderr)
        sys.exit(2)

    history_dir = base_dir / "history"
    history_dir.mkdir(exist_ok=True)

    # 1. 读取当前状态和配置
    print("=" * 70)
    print("果仁策略自动研究系统 - 单次迭代")
    print("=" * 70)

    state = _load_state(base_dir)
    champion_config = _load_config(base_dir)

    current_iter = state.get("current_iter", 0) + 1
    iter_id = _format_iter_id(current_iter)

    print(f"\n[迭代 {iter_id}] 开始")
    print(f"  Champion 得分: {state.get('champion_score', -1e308):.6f}")
    print(f"  连续失败次数: {state.get('consecutive_failures', 0)}")
    print(f"  变异描述: {args.mutation_summary}")

    # 2. 生成候选配置
    print(f"\n[步骤 1/6] 生成候选配置")
    try:
        candidate_config, mutation_desc = mutate(
            champion_config, mutation_type=args.mutation_type
        )
        print(f"  变异类型: {mutation_desc}")

        # 验证配置合法性
        if not validate_config(candidate_config):
            print("  错误：生成的配置不合法", file=sys.stderr)
            sys.exit(2)

    except Exception as e:
        print(f"  错误：变异失败：{e}", file=sys.stderr)
        sys.exit(2)

    # 3. 保存临时配置
    print(f"\n[步骤 2/6] 保存临时配置")
    config_snapshot_path = history_dir / f"{iter_id}_config.json"
    with open(config_snapshot_path, "w", encoding="utf-8") as f:
        json.dump(candidate_config, f, ensure_ascii=False, indent=2)
    print(f"  已保存: {config_snapshot_path}")

    # 4. 执行回测
    print(f"\n[步骤 3/6] 执行回测")
    start_time = datetime.now(timezone.utc)

    try:
        result = run_backtest(candidate_config)
        end_time = datetime.now(timezone.utc)
        elapsed = (end_time - start_time).total_seconds()

        print(f"  回测完成，耗时 {elapsed:.1f} 秒")
        print(f"  回测 ID: {result['backtest_id']}")

    except (GuornExecutorError, BacktestTimeoutError) as e:
        end_time = datetime.now(timezone.utc)
        elapsed = (end_time - start_time).total_seconds()

        print(f"  回测失败：{e}", file=sys.stderr)

        # 记录 crash
        crash_record = {
            "iter": iter_id,
            "commit": "",
            "backtest_id": "",
            "status": "crash",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "elapsed_seconds": elapsed,
            "error": str(e),
            "mutation": args.mutation_summary,
            "mutation_type": args.mutation_type,
        }

        crash_path = history_dir / f"{iter_id}.json"
        with open(crash_path, "w", encoding="utf-8") as f:
            json.dump(crash_record, f, ensure_ascii=False, indent=2)

        # 更新 state.json
        state["current_iter"] = current_iter
        state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1
        state["last_update"] = datetime.now(timezone.utc).isoformat()
        _save_state(base_dir, state)

        # 追加到 iterations.tsv
        tsv_path = history_dir / "iterations.tsv"
        with open(tsv_path, "a", encoding="utf-8") as f:
            f.write(
                f"{iter_id}\t\t\tcrash\t0.0000\t0.0000\t0.0000\t0.000000\tcrash\t{args.mutation_summary}\n"
            )

        sys.exit(2)

    # 5. 解析结果并计算得分
    print(f"\n[步骤 4/6] 计算得分")

    try:
        # 构造 result_json 格式（适配 scorer.py）
        result_json = {
            "status": result["status"],
            "data": {
                "calc_id": result["backtest_id"],
                "trade_summary": {
                    "winsorize_annual": result["summary"]["annualReturn"],
                    "maxdrop_day": result["summary"]["maxDrawdown"],
                    "win_ratio": result["summary"]["winRate"],
                    "year_information_ratio": result["summary"]["informationRatio"],
                    "sharpe_ratio": result["summary"]["sharpe"],
                    "sortino_ratio": result["summary"]["sortino"],
                    "avg_hold_days": result["summary"]["avgHoldingDays"],
                    "sell_count": result["summary"]["sellCount"],
                    "total_return": result["summary"]["totalReturn"],
                },
            },
        }

        new_metrics = parse_backtest_result(result_json)
        new_score = calculate_score(new_metrics, weights=DEFAULT_WEIGHTS)

        print(f"  年化收益: {new_metrics.annual_return:.4f}")
        print(f"  最大回撤: {new_metrics.max_drawdown:.4f}")
        print(f"  夏普比率: {new_metrics.sharpe:.4f}")
        print(f"  Sortino 比率: {new_metrics.sortino:.4f}")
        print(f"  信息比率: {new_metrics.information_ratio:.4f}")
        print(f"  复合得分: {new_score:.6f}")

    except Exception as e:
        print(f"  错误：解析结果失败：{e}", file=sys.stderr)
        sys.exit(2)

    # 6. 决策 keep/rollback
    print(f"\n[步骤 5/6] 决策")

    champion_score = state.get("champion_score", -1e308)
    champion_metrics = state.get("champion_metrics")

    # 如果 champion_metrics 存在，转换为 ParsedMetrics 对象
    if champion_metrics:
        from scorer import ParsedMetrics

        champion_metrics_obj = ParsedMetrics(**champion_metrics)
    else:
        champion_metrics_obj = None

    decision, reason = decide_keep_rollback(
        new_score=new_score,
        champion_score=champion_score,
        new_metrics=new_metrics,
        champion_metrics=champion_metrics_obj,
        hard_constraints=DEFAULT_HARD_CONSTRAINTS,
    )

    print(f"  决策: {decision}")
    print(f"  理由: {reason}")

    # 7. git commit / rollback
    print(f"\n[步骤 6/6] git commit / rollback")
    commit_hash = ""

    if decision == "keep":
        _save_config(base_dir, candidate_config)
        commit_hash = _git_commit(base_dir, iter_id, args.mutation_summary)
        if commit_hash:
            print(f"  git commit {commit_hash}")

        state["current_iter"] = current_iter
        state["champion_score"] = new_score
        state["champion_iter"] = iter_id
        state["champion_config"] = candidate_config
        state["champion_metrics"] = {
            "status": new_metrics.status,
            "backtest_id": new_metrics.backtest_id,
            "total_return": new_metrics.total_return,
            "annual_return": new_metrics.annual_return,
            "max_drawdown": new_metrics.max_drawdown,
            "sharpe": new_metrics.sharpe,
            "sortino": new_metrics.sortino,
            "information_ratio": new_metrics.information_ratio,
            "win_rate": new_metrics.win_rate,
            "avg_holding_days": new_metrics.avg_holding_days,
            "sell_count": new_metrics.sell_count,
        }
        state["consecutive_failures"] = 0
        state["last_update"] = datetime.now(timezone.utc).isoformat()
        _save_state(base_dir, state)

        exit_code = 0

    else:  # rollback
        champion_iter = state.get("champion_iter", "")
        if champion_iter:
            _git_rollback_to_champion(base_dir, champion_iter)
            print(f"  git rollback → champion {champion_iter}")

        state["current_iter"] = current_iter
        state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1
        state["last_update"] = datetime.now(timezone.utc).isoformat()
        _save_state(base_dir, state)

        exit_code = 1

    # 8. 写入 history/<iter>.json
    iteration_record = {
        "iter": iter_id,
        "commit": commit_hash,
        "backtest_id": new_metrics.backtest_id,
        "status": new_metrics.status,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "elapsed_seconds": elapsed,
        "annual_return": new_metrics.annual_return,
        "max_drawdown": new_metrics.max_drawdown,
        "win_rate": new_metrics.win_rate,
        "information_ratio": new_metrics.information_ratio,
        "sharpe": new_metrics.sharpe,
        "sortino": new_metrics.sortino,
        "avg_holding_days": new_metrics.avg_holding_days,
        "sell_count": new_metrics.sell_count,
        "score": new_score,
        "decision": decision,
        "reason": reason,
        "mutation": args.mutation_summary,
        "mutation_type": args.mutation_type,
        "full_result": result.get("full_result", {}),
    }

    iteration_path = history_dir / f"{iter_id}.json"
    with open(iteration_path, "w", encoding="utf-8") as f:
        json.dump(iteration_record, f, ensure_ascii=False, indent=2)
    print(f"  已保存 {iteration_path}")

    # 9. 追加到 iterations.tsv
    tsv_path = history_dir / "iterations.tsv"
    with open(tsv_path, "a", encoding="utf-8") as f:
        f.write(
            f"{iter_id}\t{commit_hash}\t{new_metrics.backtest_id}\t{new_metrics.status}\t"
            f"{new_metrics.annual_return:.4f}\t{new_metrics.max_drawdown:.4f}\t"
            f"{new_metrics.sharpe:.4f}\t{new_score:.6f}\t{decision}\t{args.mutation_summary}\n"
        )
    print(f"  已追加 {tsv_path}")

    # 11. 完成
    print("\n" + "=" * 70)
    print(f"迭代 {iter_id} 完成")
    print("=" * 70)
    print(f"  决策: {decision}")
    print(f"  得分: {new_score:.6f}")
    print(f"  Champion 得分: {state['champion_score']:.6f}")
    print(f"  退出码: {exit_code}")
    print()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
