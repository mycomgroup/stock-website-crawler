#!/usr/bin/env python3
"""
问财公式回测自动研究系统初始化脚本。

功能：
1. 初始化实验目录结构
2. 复制种子配置
3. 运行 baseline 回测并记录初始状态

用法示例：
    python setup.py --name my_experiment
    python setup.py --name mock_test --mock  # 使用 Mock 模式

注意：
    --mock: 使用 Mock 模式，跳过真实 API 调用，返回模拟数据
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


SKILL_ROOT = Path(__file__).parent
EXPERIMENTS_DIR = SKILL_ROOT / "experiments"
SEED_DIR = SKILL_ROOT
PROGRAM_MD_PATH = SKILL_ROOT / "program.md"
TREES_DIR = SKILL_ROOT / "trees"

DEFAULT_SEED = "seed_config.json"


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
    parser.add_argument(
        "--start-date",
        default=None,
        help=f"回测开始日期（默认：{default_start}）",
    )
    parser.add_argument(
        "--end-date",
        default=None,
        help=f"回测结束日期（默认：{default_end}）",
    )
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
        if args.seed is None:
            args.seed = str(tree_dir / "seed.json")

    if args.seed is None:
        args.seed = DEFAULT_SEED

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

    if "startDate" in config and config["startDate"] == "AUTO":
        config["startDate"] = start_date
    if "endDate" in config and config["endDate"] == "AUTO":
        config["endDate"] = end_date

    return config


def _init_experiment_dir(name: str, args: argparse.Namespace) -> Path:
    print(f"\n[1/4] 初始化实验目录")

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
    print(f"✓ 写入配置：formula_config.json")

    state = {
        "current_iter": 1,
        "champion_score": -1e308,
        "consecutive_failures": 0,
        "last_update": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
    }
    state_path = exp_dir / "state.json"
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"✓ 写入状态：state.json")

    program_dest = exp_dir / "program.md"
    if program_source.exists():
        with open(program_source, encoding="utf-8") as src:
            content = src.read()
        strategy_name = seed_config.get("name", "未命名策略")
        strategy_desc = seed_config.get("description", "无描述")
        content = content.replace("{{STRATEGY_NAME}}", strategy_name)
        content = content.replace("{{STRATEGY_DESCRIPTION}}", strategy_desc)
        with open(program_dest, "w", encoding="utf-8") as dst:
            dst.write(content)
        print(f"✓ 生成指南：program.md（已注入策略目标）")

    readme_path = exp_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {name}\n\n")
        f.write(f"问财公式回测自动研究实验\n\n")
        f.write(f"- 创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 开始迭代\n\n")
        f.write("```bash\n")
        f.write(f"cd {exp_dir}\n")
        f.write("# 阅读 program.md，然后让 agent 开始迭代\n")
        f.write("```\n")
    print(f"✓ 创建说明：README.md")

    tsv_path = exp_dir / "iterations.tsv"
    with open(tsv_path, "w", encoding="utf-8") as f:
        f.write("iter\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\n")
    print(f"✓ 创建记录：iterations.tsv")

    search_notes_path = exp_dir / "search_notes.md"
    with open(search_notes_path, "w", encoding="utf-8") as f:
        f.write("# 搜索笔记\n\n")
        f.write("记录迭代过程中的观察和想法。\n\n")
    print(f"✓ 创建笔记：search_notes.md")

    return exp_dir


def _run_baseline_backtest(exp_dir: Path, args: argparse.Namespace, use_mock: bool) -> dict:
    print(f"\n[2/4] 运行 baseline 回测")

    config_path = exp_dir / "formula_config.json"

    print(f"  回测区间：{args.start_date} ~ {args.end_date}")
    if use_mock:
        print(f"  模式：Mock（模拟数据）")

    executor_path = SKILL_ROOT / "formula_executor.py"

    try:
        env = os.environ.copy()
        if use_mock:
            env["JQKA_MOCK_MODE"] = "1"

        from formula_executor import run_backtest

        config = json.load(open(config_path))
        result = run_backtest(config)

        backtest_id = result.get("backtest_id", "")

        if not backtest_id:
            raise ValueError("未能从 executor 输出获取 backtest_id")

        print(f"✓ 回测提交成功，ID：{backtest_id}")

        summary = result.get("summary", {})

        print(f"✓ 回测完成")
        print(f"  年化收益：{summary.get('annualReturn', 0):.2%}")
        print(f"  最大回撤：{summary.get('maxDrawdown', 0):.2%}")
        print(f"  夏普比率：{summary.get('sharpe', 0):.2f}")

        return {
            "backtest_id": backtest_id,
            "summary": summary,
        }

    except Exception as e:
        print(f"错误：回测执行失败：{e}")
        raise


def _update_state_with_baseline(exp_dir: Path, baseline_result: dict) -> None:
    print(f"\n[3/4] 更新状态文件")

    state_path = exp_dir / "state.json"
    with open(state_path, encoding="utf-8") as f:
        state = json.load(f)

    summary = baseline_result["summary"]

    annual_return = summary.get("annualReturn", 0)
    max_drawdown = summary.get("maxDrawdown", 0)
    sortino = summary.get("sortino", 0)
    information_ratio = summary.get("informationRatio", 0)

    calmar = annual_return / max(abs(max_drawdown), 0.01)
    score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20

    state["champion_score"] = score
    state["current_iter"] = 1
    state["consecutive_failures"] = 0
    state["last_update"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"✓ 更新 state.json")

    tsv_path = exp_dir / "iterations.tsv"
    with open(tsv_path, "a", encoding="utf-8") as f:
        f.write(f"0000\t{baseline_result['backtest_id']}\tsuccess\t")
        f.write(f"{(summary.get('annualReturn', 0)):.4f}\t")
        f.write(f"{(summary.get('maxDrawdown', 0)):.4f}\t")
        f.write(f"{(summary.get('sharpe', 0)):.4f}\t")
        f.write(f"{score:.4f}\tbaseline\tinitial_seed_config\n")
    print(f"✓ 追加记录：iterations.tsv")


def _init_git_repo(exp_dir: Path) -> None:
    print(f"\n[4/4] 初始化 Git 仓库")

    try:
        subprocess.run(["git", "init"], cwd=exp_dir, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=exp_dir, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "baseline: initial seed config"],
            cwd=exp_dir,
            check=True,
            capture_output=True,
        )
        print(f"✓ Git 仓库初始化完成")
    except subprocess.CalledProcessError as e:
        print(f"警告：Git 初始化失败：{e}")


def main() -> None:
    args = _parse_args()

    print("=" * 70)
    print("问财公式回测自动研究系统初始化")
    print("=" * 70)

    exp_dir = _init_experiment_dir(args.name, args)

    use_mock = args.mock

    baseline_result = _run_baseline_backtest(exp_dir, args, use_mock)

    _update_state_with_baseline(exp_dir, baseline_result)

    _init_git_repo(exp_dir)

    print("\n" + "=" * 70)
    print("初始化完成！")
    print("=" * 70)
    print(f"\n实验目录：{exp_dir}")
    if use_mock:
        print(f"回测模式：Mock（模拟数据）")
    else:
        print(f"回测模式：真实回测")
    print(f"\n下一步：")
    print(f"  cd {exp_dir}")
    print(f"  # 阅读 program.md，然后让 agent 开始迭代")
    print()


if __name__ == "__main__":
    main()
