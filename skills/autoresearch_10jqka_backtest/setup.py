#!/usr/bin/env python3
"""
问财公式回测自动研究系统初始化脚本。

功能：
1. 初始化实验目录结构
2. 复制种子配置
3. 运行多窗口 baseline 回测并记录初始状态
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from formula_executor import run_backtest_windows
from scorer import (
    calculate_complexity,
    calculate_robust_score_multi_window,
    calculate_score,
    classify_direction_status,
    parse_backtest_result,
)
from tree_profile import load_tree_profile, load_tree_profile_from_dir, validate_profile, merge_with_defaults


SKILL_ROOT = Path(__file__).parent
EXPERIMENTS_DIR = SKILL_ROOT / "experiments"
SEED_DIR = SKILL_ROOT
PROGRAM_MD_PATH = SKILL_ROOT / "program.md"
TREES_DIR = SKILL_ROOT / "trees"
DEFAULT_SEED = "seed_config.json"
WINDOWS = ["recent_6m", "recent_12m", "prior_12m", "full_24m"]
TSV_HEADER = "iter\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\trobust_score\trecent6\trecent12\tprior12\tfull24\tsensitivity\ttrade_count\tcomplexity\treason\n"


def compute_seed_hash(config: dict) -> str:
    config_for_hash = {
        "formula": config.get("formula", []),
        "maxPositions": config.get("maxPositions"),
        "takeProfit": config.get("takeProfit"),
        "stopLoss": config.get("stopLoss"),
    }
    config_str = json.dumps(config_for_hash, sort_keys=True)
    return hashlib.md5(config_str.encode()).hexdigest()[:8]


def _get_default_dates() -> tuple:
    today = datetime.now()
    end_date = today.strftime("%Y-%m-%d")
    start_date = (today - timedelta(days=365 * 5)).strftime("%Y-%m-%d")
    return start_date, end_date


def _parse_args() -> argparse.Namespace:
    default_start, default_end = _get_default_dates()

    parser = argparse.ArgumentParser(
        description="问财公式回测自动研究系统初始化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例：\n  python setup.py --name my_experiment\n  python setup.py --name mock_test --mock",
    )
    parser.add_argument("--name", required=True, help="实验名称（用作目录名）")
    parser.add_argument(
        "--tree",
        default=None,
        help="指定树的目录路径（相对或绝对路径），自动使用该目录下的 seed.json 和 program.md",
    )
    parser.add_argument(
        "--seed",
        default=None,
        help="种子配置文件路径（--tree 模式下默认使用 trees/<tree>/seed.json）",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="使用 Mock 模式，跳过真实 API 调用，返回模拟数据",
    )
    parser.add_argument("--start-date", default=None, help=f"回测开始日期（默认：{default_start}）")
    parser.add_argument("--end-date", default=None, help=f"回测结束日期（默认：{default_end}）")
    args = parser.parse_args()

    if args.start_date is None:
        args.start_date = default_start
    if args.end_date is None:
        args.end_date = default_end

    if args.tree:
        tree_dir = Path(args.tree)
        if not tree_dir.is_absolute():
            tree_dir = SKILL_ROOT / tree_dir
        if not tree_dir.exists():
            print(f"错误：树目录不存在：{tree_dir}", file=sys.stderr)
            sys.exit(1)
        
        profile_path = tree_dir / "profile.json"
        if profile_path.exists():
            args.profile_path = str(profile_path)
            print(f"  使用树配置：{profile_path}")
        else:
            args.profile_path = None
            if args.seed is None:
                args.seed = str(tree_dir / "seed.json")
        
        if args.seed is None and args.profile_path is None:
            args.seed = str(tree_dir / "seed.json")

    return args


def _load_seed_config(seed_path_str: str, start_date: str, end_date: str) -> dict:
    seed_path = Path(seed_path_str)
    if not seed_path.is_absolute():
        seed_path = SEED_DIR / seed_path

    if not seed_path.exists():
        print(f"错误：种子配置文件不存在：{seed_path}", file=sys.stderr)
        sys.exit(1)

    with open(seed_path, encoding="utf-8") as f:
        config = json.load(f)

    if config.get("startDate") == "AUTO":
        config["startDate"] = start_date
    if config.get("endDate") == "AUTO":
        config["endDate"] = end_date

    return config


def _load_profile_config(tree_dir: Path, start_date: str, end_date: str) -> dict:
    """Load config from tree profile.json, generating initial formula config."""
    profile = load_tree_profile_from_dir(tree_dir)
    if profile is None:
        return None
    
    errors = validate_profile(profile)
    if errors:
        print(f"警告：profile.json 校验问题: {errors}", file=sys.stderr)
    
    initial_formula = profile.get("initial_formula", ["非ST", "非退市"])
    
    config = {
        "name": profile.get("name", tree_dir.name),
        "description": profile.get("description", ""),
        "formula": initial_formula,
        "startDate": start_date,
        "endDate": end_date,
        "maxPositions": profile.get("soft_priors", {}).get("maxPositions", {}).get("preferred", [5, 8])[0],
        "dailyBuyCount": 2,
        "takeProfit": profile.get("soft_priors", {}).get("takeProfit", {}).get("preferred", [15, 25])[0],
        "stopLoss": profile.get("soft_priors", {}).get("stopLoss", {}).get("preferred", [7, 12])[0],
        "trailingStopLoss": profile.get("soft_priors", {}).get("trailingStopLoss", {}).get("preferred", [5, 8])[0],
        "daysForSaleStrategy": "3,5",
        "tree_profile": profile,
    }
    
    return config


def _metrics_snapshot(metrics) -> dict:
    return {
        "annual_return": metrics.annual_return,
        "max_drawdown": metrics.max_drawdown,
        "sortino": metrics.sortino,
        "information_ratio": metrics.information_ratio,
        "win_rate": metrics.win_rate,
        "trade_count": metrics.trade_count,
        "sharpe": metrics.sharpe,
        "avg_holding_days": metrics.avg_holding_days,
    }


def _infer_recommendation(direction_status: str, stable_param_ranges: dict) -> str:
    if direction_status == "INACTIVE":
        return "停止深挖，当前方向近期失效。"
    if stable_param_ranges:
        return "继续跟踪 champion，并优先在稳定参数带内微调。"
    if direction_status == "WATCH":
        return "先保持观察，只做有限粗搜索，不扩展复杂条件。"
    return "方向仍活着，进入粗搜索。"


def _build_window_bundle(config: dict, results_by_window: dict) -> tuple[dict, dict, dict, object, float, float]:
    metrics_by_window = {}
    score_map = {}
    window_snapshot = {}
    complexity = calculate_complexity(config)

    for window_name in WINDOWS:
        result = results_by_window.get(window_name, {})
        metrics = parse_backtest_result(result, window_name=window_name)
        score = calculate_score(metrics, complexity=complexity, config=config)
        metrics_by_window[window_name] = metrics
        score_map[window_name] = score
        window_snapshot[window_name] = {
            "score": score,
            **_metrics_snapshot(metrics),
        }

    primary_metrics = metrics_by_window.get("recent_12m") or metrics_by_window.get("recent_6m")
    primary_score = score_map.get("recent_12m", score_map.get("recent_6m", 0.0))
    robust_score = calculate_robust_score_multi_window(metrics_by_window, neighbor_scores=[], config=config)
    return metrics_by_window, score_map, window_snapshot, primary_metrics, primary_score, robust_score


def _init_experiment_dir(name: str, args: argparse.Namespace) -> Path:
    print("\n[1/4] 初始化实验目录")

    seed_config = None
    profile_config = None
    
    if hasattr(args, 'profile_path') and args.profile_path:
        tree_dir = Path(args.profile_path).parent
        profile_config = _load_profile_config(tree_dir, args.start_date, args.end_date)
    
    if profile_config:
        seed_config = profile_config
        print(f"✓ 加载树配置：{args.profile_path}（{seed_config.get('name', '未知策略')}）")
    else:
        seed_config = _load_seed_config(args.seed, args.start_date, args.end_date)
        print(f"✓ 加载种子：{args.seed}（{seed_config.get('name', '未知策略')}）")
    if "description" in seed_config:
        print(f"  描述：{seed_config['description']}")

    if args.tree:
        tree_dir = Path(args.tree)
        if not tree_dir.is_absolute():
            tree_dir = SKILL_ROOT / tree_dir
        exp_dir = tree_dir / "experiments" / name
        program_source = tree_dir / "program.md"
        print(f"  树模式：{args.tree}")
    else:
        exp_dir = EXPERIMENTS_DIR / name
        program_source = PROGRAM_MD_PATH

    if exp_dir.exists():
        print(f"警告：实验目录已存在：{exp_dir}")
        try:
            answer = input("是否覆盖？(y/N) ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)
        if answer not in ("y", "yes"):
            print("已取消。")
            sys.exit(0)

    exp_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ 创建目录：{exp_dir}")

    formula_config_path = exp_dir / "formula_config.json"
    with open(formula_config_path, "w", encoding="utf-8") as f:
        json.dump(seed_config, f, ensure_ascii=False, indent=2)
    print("✓ 写入配置：formula_config.json")

    state = {
        "current_iter": 1,
        "champion_score": -1e308,
        "champion_robust_score": -1e308,
        "consecutive_failures": 0,
        "last_update": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "objective_version": "v3_a_value_pipeline",
        "seed_name": seed_config.get("name", "unknown"),
        "seed_hash": compute_seed_hash(seed_config),
        "search_mode": "tree_profile" if (hasattr(args, 'profile_path') and args.profile_path) else "seed_config",
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
    }
    if hasattr(args, 'profile_path') and args.profile_path:
        state["tree_profile_path"] = args.profile_path
    with open(exp_dir / "state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("✓ 写入状态：state.json")

    program_dest = exp_dir / "program.md"
    if program_source.exists():
        with open(program_source, encoding="utf-8") as src:
            content = src.read()
        content = content.replace("{{STRATEGY_NAME}}", seed_config.get("name", "未命名策略"))
        content = content.replace("{{STRATEGY_DESCRIPTION}}", seed_config.get("description", "无描述"))
        with open(program_dest, "w", encoding="utf-8") as dst:
            dst.write(content)
        print("✓ 生成指南：program.md（已注入策略目标）")

    with open(exp_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(f"# {name}\n\n")
        f.write("问财公式回测自动研究实验\n\n")
        f.write(f"- 创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 开始迭代\n\n")
        f.write("```bash\n")
        f.write(f"cd {exp_dir}\n")
        f.write("# 阅读 program.md，然后让 agent 开始迭代\n")
        f.write("```\n")
    print("✓ 创建说明：README.md")

    with open(exp_dir / "iterations.tsv", "w", encoding="utf-8") as f:
        f.write(TSV_HEADER)
    print("✓ 创建记录：iterations.tsv")

    with open(exp_dir / "search_notes.md", "w", encoding="utf-8") as f:
        f.write("# 搜索笔记\n\n")
        f.write("记录方向状态、稳定参数带和最近 keep/rollback 原因。\n\n")
    print("✓ 创建笔记：search_notes.md")

    return exp_dir


def _run_baseline_backtest(exp_dir: Path, args: argparse.Namespace, use_mock: bool) -> dict:
    print("\n[2/4] 运行 baseline 回测")
    print(f"  回测区间：{args.start_date} ~ {args.end_date}")
    if use_mock:
        print("  模式：Mock（模拟数据）")

    try:
        if use_mock:
            os.environ["JQKA_MOCK_MODE"] = "1"

        config = json.load(open(exp_dir / "formula_config.json"))
        results = run_backtest_windows(config, windows=WINDOWS, experiment_dir=exp_dir)

        first_backtest_id = ""
        for window_name in WINDOWS:
            result = results.get(window_name, {})
            backtest_id = result.get("backtest_id", "") if isinstance(result, dict) else ""
            if backtest_id and not first_backtest_id:
                first_backtest_id = backtest_id

            metrics = parse_backtest_result(result, window_name=window_name)
            print(
                f"  {window_name}: annual={metrics.annual_return:.2%} dd={metrics.max_drawdown:.2%} trades={metrics.trade_count}",
            )

        if not first_backtest_id:
            raise ValueError("未能从多窗口 baseline 输出获取 backtest_id")

        return {
            "backtest_id": first_backtest_id,
            "results_by_window": results,
        }
    except Exception as e:
        print(f"错误：baseline 回测执行失败：{e}")
        raise


def _update_state_with_baseline(exp_dir: Path, baseline_result: dict) -> None:
    print("\n[3/4] 更新状态文件")

    state_path = exp_dir / "state.json"
    with open(state_path, encoding="utf-8") as f:
        state = json.load(f)

    seed_config = json.load(open(exp_dir / "formula_config.json"))
    results_by_window = baseline_result["results_by_window"]
    metrics_by_window, score_map, window_snapshot, primary_metrics, primary_score, robust_score = _build_window_bundle(seed_config, results_by_window)

    direction_status, direction_reason, _ = classify_direction_status(
        score_map.get("recent_6m", 0.0),
        score_map.get("recent_12m", 0.0),
        score_map,
    )

    state.update(
        {
            "champion_score": primary_score,
            "champion_robust_score": robust_score,
            "current_iter": 1,
            "consecutive_failures": 0,
            "last_update": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            "phase": "coarse_search",
            "direction_status": direction_status,
            "direction_reason": direction_reason,
            "champion_metrics": _metrics_snapshot(primary_metrics),
            "champion_windows": window_snapshot,
            "baseline_window_scores": score_map,
            "baseline_metrics_by_window": {k: _metrics_snapshot(v) for k, v in metrics_by_window.items()},
            "stable_param_ranges": {},
            "last_keep_reason": "baseline initialized",
            "last_mutation_type": "baseline",
            "final_recommendation": _infer_recommendation(direction_status, {}),
            "stop_reason": "",
        }
    )

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("✓ 更新 state.json")

    with open(exp_dir / "iterations.tsv", "a", encoding="utf-8") as f:
        f.write(f"0000\t{baseline_result['backtest_id']}\tsuccess\t")
        f.write(f"{primary_metrics.annual_return:.4f}\t")
        f.write(f"{primary_metrics.max_drawdown:.4f}\t")
        f.write(f"{primary_metrics.sharpe:.4f}\t")
        f.write(f"{primary_score:.4f}\tbaseline\tinitial_seed_config\t")
        f.write(f"{robust_score:.4f}\t")
        f.write(f"{score_map.get('recent_6m', 0):.4f}\t")
        f.write(f"{score_map.get('recent_12m', 0):.4f}\t")
        f.write(f"{score_map.get('prior_12m', 0):.4f}\t")
        f.write(f"{score_map.get('full_24m', 0):.4f}\t")
        f.write("0.0000\t")
        f.write(f"{primary_metrics.trade_count}\t")
        f.write(f"{calculate_complexity(seed_config)}\t")
        f.write("baseline\n")
    print("✓ 追加记录：iterations.tsv")


def _init_git_repo(exp_dir: Path) -> None:
    print("\n[4/4] 初始化 Git 仓库")
    try:
        subprocess.run(["git", "init"], cwd=exp_dir, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=exp_dir, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "baseline: initial seed config"],
            cwd=exp_dir,
            check=True,
            capture_output=True,
        )
        print("✓ Git 仓库初始化完成")
    except subprocess.CalledProcessError as e:
        print(f"警告：Git 初始化失败：{e}")


def main() -> None:
    args = _parse_args()

    print("=" * 70)
    print("问财公式回测自动研究系统初始化")
    print("=" * 70)

    exp_dir = _init_experiment_dir(args.name, args)
    baseline_result = _run_baseline_backtest(exp_dir, args, args.mock)
    _update_state_with_baseline(exp_dir, baseline_result)
    _init_git_repo(exp_dir)

    print("\n" + "=" * 70)
    print("初始化完成！")
    print("=" * 70)
    print(f"\n实验目录：{exp_dir}")
    print(f"回测模式：{'Mock（模拟数据）' if args.mock else '真实回测'}")
    print("\n下一步：")
    print(f"  cd {exp_dir}")
    print("  # 阅读 program.md，然后让 agent 开始迭代")
    print()


if __name__ == "__main__":
    main()
