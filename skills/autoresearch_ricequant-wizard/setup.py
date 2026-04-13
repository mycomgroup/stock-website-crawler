#!/usr/bin/env python3
"""
向导式策略自动研究系统初始化脚本。

功能：
1. 在 RiceQuant 平台创建/复用向导式策略
2. 初始化实验目录结构
3. 运行 baseline 回测并记录初始状态

用法示例：
    python setup.py --name my_wizard_experiment
    python setup.py --name smallcap_exp --seed seed_smallcap_value.json --strategy-id 2421275
    python setup.py --name mock_test --mock  # 使用 Mock 模式

种子文件：
    当前目录可用：seed_config.json, seed_smallcap_value.json,
                  seed_largecap_growth.json, seed_dividend.json

注意：
    --strategy-id: RiceQuant 平台的真实策略 ID，用于真实回测
    --mock: 使用 Mock 模式，跳过真实 API 调用，返回模拟数据
    如不提供以上任一参数，将提示用户手动创建策略
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── 路径常量 ──────────────────────────────────────────────────────────────────
SKILL_ROOT = Path(__file__).parent
EXPERIMENTS_DIR = SKILL_ROOT / "experiments"
SEED_DIR = SKILL_ROOT
PROGRAM_MD_PATH = SKILL_ROOT / "program.md"

# ── 默认参数 ──────────────────────────────────────────────────────────────────
DEFAULT_SEED = "seed_config.json"
DEFAULT_CAPITAL = 100000
DEFAULT_BENCHMARK = "000300.XSHG"


# ── 工具函数 ──────────────────────────────────────────────────────────────────


def _get_default_dates() -> tuple[str, str]:
    """生成最近5年的默认回测日期"""
    today = datetime.now()
    end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    start_date = (today - timedelta(days=5 * 365)).strftime("%Y-%m-%d")
    return start_date, end_date


def _parse_args() -> argparse.Namespace:
    default_start, default_end = _get_default_dates()

    parser = argparse.ArgumentParser(
        description="向导式策略自动研究系统初始化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例：\n  python setup.py --name my_wizard_experiment\n  python setup.py --name smallcap_exp --seed seed_smallcap_value.json",
    )
    parser.add_argument("--name", required=True, help="实验名称（用作目录名）")
    parser.add_argument(
        "--seed",
        default=DEFAULT_SEED,
        help="种子配置文件路径（默认：seed_config.json）\n可以是当前目录文件名或绝对路径",
    )
    parser.add_argument(
        "--strategy-id",
        default=None,
        help="RiceQuant 平台的真实策略 ID（用于真实回测）",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="使用 Mock 模式，跳过真实 API 调用，返回模拟数据",
    )
    parser.add_argument(
        "--start-date",
        default=None,
        help=f"回测开始日期（默认：最近5年，即 {default_start}）",
    )
    parser.add_argument(
        "--end-date",
        default=None,
        help=f"回测结束日期（默认：今天，即 {default_end}）",
    )
    parser.add_argument(
        "--capital", type=int, default=DEFAULT_CAPITAL, help=f"初始资金（默认：{DEFAULT_CAPITAL}）"
    )
    parser.add_argument(
        "--benchmark", default=DEFAULT_BENCHMARK, help=f"基准指数（默认：{DEFAULT_BENCHMARK}）"
    )
    args = parser.parse_args()

    if args.start_date is None:
        args.start_date = default_start
    if args.end_date is None:
        args.end_date = default_end

    return args


def _load_seed_config(seed_path_str: str, start_date: str, end_date: str) -> dict:
    """读取种子配置文件并处理 AUTO 日期

    Args:
        seed_path_str: 种子文件路径（相对或绝对）
        start_date: 回测开始日期
        end_date: 回测结束日期

    Returns:
        配置字典
    """
    seed_path = Path(seed_path_str)

    if not seed_path.is_absolute():
        seed_path = SEED_DIR / seed_path

    if not seed_path.exists():
        print(f"错误：种子配置文件不存在：{seed_path}", file=sys.stderr)
        sys.exit(1)

    with open(seed_path, encoding="utf-8") as f:
        config = json.load(f)

    if "backtest" in config:
        if config["backtest"].get("start_date") == "AUTO":
            config["backtest"]["start_date"] = start_date
        if config["backtest"].get("end_date") == "AUTO":
            config["backtest"]["end_date"] = end_date

    return config


def _create_ricequant_strategy(
    name: str, args: argparse.Namespace, config_path: Path
) -> tuple[str, bool]:
    """
    获取策略 ID 并确定回测模式。

    Returns:
        tuple[str, bool]: (strategy_id, use_mock_mode)

    三种模式：
    1. 真实回测：--strategy-id 提供，use_mock_mode=False
    2. Mock 模式：--mock 提供，use_mock_mode=True
    3. 自动创建：两者都不提供，自动调用 RiceQuant API 创建策略
    """
    if args.strategy_id:
        strategy_id = args.strategy_id
        use_mock = False
        print(f"\n[2/5] 使用已有策略 ID：{strategy_id}")
        print(f"  将在 RiceQuant 平台运行真实回测")
    elif args.mock:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        strategy_id = f"mock_{name}_{timestamp}"
        use_mock = True
        print(f"\n[2/5] Mock 模式：生成模拟策略 ID")
        print(f"  Mock ID：{strategy_id}")
        print(f"  将使用模拟数据进行回测")
    else:
        print(f"\n[2/5] 自动创建 RiceQuant 向导式策略")
        strategy_id = _create_strategy_via_api(name, config_path)
        if strategy_id:
            use_mock = False
            print(f"  ✓ 策略创建成功，ID：{strategy_id}")
            print(f"  将在 RiceQuant 平台运行真实回测")
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            strategy_id = f"wizard_{name}_{timestamp}"
            use_mock = True
            print(f"  ⚠ 策略创建失败，使用本地实验 ID")
            print(f"  本地 ID：{strategy_id}")
            print(f"  将使用模拟数据进行回测")

    return strategy_id, use_mock


def _create_strategy_via_api(name: str, config_path: Path) -> str | None:
    """
    通过 RiceQuant API 创建向导式策略。

    Returns:
        strategy_id 或 None（失败时）
    """
    wizard_skill_dir = SKILL_ROOT.parent / "ricequant-wizard"
    run_skill_path = wizard_skill_dir / "run-skill.js"

    if not run_skill_path.exists():
        print(f"  ⚠ 未找到 run-skill.js：{run_skill_path}")
        return None

    try:
        result = subprocess.run(
            [
                "node",
                str(run_skill_path),
                "--create",
                "--config",
                str(config_path),
            ],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(wizard_skill_dir),
        )

        output = result.stdout + result.stderr

        if result.returncode != 0:
            print(f"  ⚠ 创建策略失败：{output[:300]}")
            return None

        for line in output.split("\n"):
            m = re.search(r"ID[：:]\s*(\d+)", line)
            if m:
                return m.group(1)

        print(f"  ⚠ 无法从输出中提取策略 ID")
        print(f"  输出：{output[:200]}")
        return None

    except subprocess.TimeoutExpired:
        print(f"  ⚠ 创建策略超时")
        return None
    except FileNotFoundError:
        print(f"  ⚠ Node.js 未安装或不可用")
        return None
    except Exception as e:
        print(f"  ⚠ 创建策略异常：{e}")
        return None


def _init_experiment_dir(name: str, strategy_id: str | None, args: argparse.Namespace) -> Path:
    """初始化实验目录结构"""
    print(f"\n[1/5] 初始化实验目录：experiments/{name}")

    seed_config = _load_seed_config(args.seed, args.start_date, args.end_date)
    print(f"✓ 加载种子：{args.seed}（{seed_config.get('name', '未知策略')}）")
    if "description" in seed_config:
        print(f"  描述：{seed_config['description']}")

    exp_dir = EXPERIMENTS_DIR / name
    history_dir = exp_dir / "history"

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

    history_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ 创建目录：{exp_dir}")

    wizard_config_path = exp_dir / "wizard_config.json"
    with open(wizard_config_path, "w", encoding="utf-8") as f:
        json.dump(seed_config, f, ensure_ascii=False, indent=2)
    print(f"✓ 写入配置：wizard_config.json")

    # 创建初始 state.json
    state = {
        "current_iter": 0,
        "strategy_id": strategy_id,
        "champion_score": -1e308,
        "champion_iter": "",
        "champion_config": None,
        "champion_metrics": None,
        "consecutive_failures": 0,
        "last_update": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
    }
    state_path = exp_dir / "state.json"
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"✓ 写入状态：state.json")

    # 复制 program.md，并注入种子描述
    program_dest = exp_dir / "program.md"
    if PROGRAM_MD_PATH.exists():
        with open(PROGRAM_MD_PATH, encoding="utf-8") as src:
            content = src.read()

        if "description" in seed_config:
            desc_section = f"""## 策略优化方向

**种子策略**：{seed_config["description"]}

**风格约束（防止漂移）**：
- 保持策略风格一致性，避免从大盘漂移到小盘
- 优先在同类型股票池内优化参数，谨慎切换 universe
- 每次变异后检查持仓风格是否偏离种子策略目标

"""
            if "## 目录结构" in content:
                content = content.replace("## 目录结构", desc_section + "## 目录结构")
            else:
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    if line.startswith("## "):
                        lines.insert(i, desc_section.rstrip())
                        break
                content = "\n".join(lines)

        with open(program_dest, "w", encoding="utf-8") as dst:
            dst.write(content)
        print(f"✓ 复制指南：program.md")

    # 创建 README.md
    readme_path = exp_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {name}\n\n")
        f.write(f"向导式策略自动研究实验\n\n")
        f.write(f"- 策略 ID：{strategy_id}\n")
        f.write(f"- 创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 开始迭代\n\n")
        f.write("```bash\n")
        f.write(f"cd {exp_dir}\n")
        f.write("# 阅读 program.md，然后让 agent 开始迭代\n")
        f.write("```\n")
    print(f"✓ 创建说明：README.md")

    # 创建 history/iterations.tsv
    tsv_path = history_dir / "iterations.tsv"
    with open(tsv_path, "w", encoding="utf-8") as f:
        f.write(
            "iter\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\n"
        )
    print(f"✓ 创建记录：history/iterations.tsv")

    # 保存初始配置快照
    snapshot_path = history_dir / "0000_config.json"
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(seed_config, f, ensure_ascii=False, indent=2)
    print(f"✓ 保存快照：history/0000_config.json")

    return exp_dir


def _update_state_strategy_id(exp_dir: Path, strategy_id: str) -> None:
    state_path = exp_dir / "state.json"
    with open(state_path, encoding="utf-8") as f:
        state = json.load(f)
    state["strategy_id"] = strategy_id
    state["last_update"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _run_baseline_backtest(
    exp_dir: Path, args: argparse.Namespace, strategy_id: str, use_mock: bool
) -> dict:
    """运行 baseline 回测并返回结果

    Args:
        exp_dir: 实验目录
        args: 命令行参数
        strategy_id: 策略 ID
        use_mock: 是否使用 Mock 模式

    Returns:
        {"backtest_id": str, "metrics": dict}
    """
    print(f"\n[3/5] 运行 baseline 回测")

    config_path = exp_dir / "wizard_config.json"

    print(f"  策略 ID：{strategy_id}")
    print(f"  回测区间：{args.start_date} ~ {args.end_date}")
    print(f"  初始资金：{args.capital}")
    print(f"  基准指数：{args.benchmark}")
    if use_mock:
        print(f"  模式：Mock（模拟数据）")

    executor_path = SKILL_ROOT / "wizard_executor.py"

    try:
        env = os.environ.copy()
        if use_mock:
            env["WIZARD_MOCK_MODE"] = "1"

        result = subprocess.run(
            [
                sys.executable,
                str(executor_path),
                "--strategy-id",
                strategy_id,
                "--config",
                str(config_path),
                "--start-date",
                args.start_date,
                "--end-date",
                args.end_date,
                "--capital",
                str(args.capital),
                "--benchmark",
                args.benchmark,
            ],
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )

        json_lines = [line for line in result.stdout.strip().split("\n") if line.startswith("{")]
        if not json_lines:
            raise ValueError(f"未找到 JSON 输出\nstdout: {result.stdout[:500]}")

        output = json.loads(json_lines[-1])
        backtest_id = output.get("backtest_id")

        if not backtest_id:
            raise ValueError("未能从 executor 输出中获取 backtest_id")

        print(f"✓ 回测提交成功，ID：{backtest_id}")

        metrics = output.get("metrics", {})

        print(f"✓ 回测完成")
        print(f"  年化收益：{metrics.get('annual_return') or 0:.2%}")
        print(f"  最大回撤：{metrics.get('max_drawdown') or 0:.2%}")
        print(f"  夏普比率：{metrics.get('sharpe') or 0:.2f}")

        return {
            "backtest_id": backtest_id,
            "metrics": metrics,
        }

    except subprocess.CalledProcessError as e:
        print(f"错误：回测执行失败")
        print(f"  stderr: {e.stderr if e.stderr else '无'}")
        raise
    except json.JSONDecodeError as e:
        print(f"错误：无法解析回测结果 JSON")
        print(f"  stdout: {result.stdout[:500] if result.stdout else '无'}")
        raise


def _update_state_with_baseline(exp_dir: Path, baseline_result: dict) -> None:
    """更新 state.json 和 history/ 记录"""
    print(f"\n[4/5] 更新状态文件")

    state_path = exp_dir / "state.json"
    with open(state_path, encoding="utf-8") as f:
        state = json.load(f)

    metrics = baseline_result["metrics"]

    # 计算 baseline score
    # 注意：scorer.calculate_score 需要 ParsedMetrics 对象
    # 这里简化处理，直接计算 score
    annual_return = metrics.get("annual_return") or 0
    max_drawdown = metrics.get("max_drawdown") or 0
    sortino = metrics.get("sortino") or 0
    information_ratio = metrics.get("information_ratio") or 0

    calmar = annual_return / max(abs(max_drawdown), 0.01)
    score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20

    # 更新 state
    state["champion_score"] = score
    state["champion_iter"] = "0000"
    state["champion_config"] = None  # baseline 使用 seed config
    state["champion_metrics"] = metrics
    state["last_update"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"✓ 更新 state.json")

    # 写入 history/0000_baseline.json
    baseline_record = {
        "iter": "0000",
        "backtest_id": baseline_result["backtest_id"],
        "metrics": metrics,
        "score": score,
        "decision": "baseline",
        "mutation": "initial_seed_config",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    baseline_path = exp_dir / "history" / "0000_baseline.json"
    with open(baseline_path, "w", encoding="utf-8") as f:
        json.dump(baseline_record, f, ensure_ascii=False, indent=2)
    print(f"✓ 保存记录：history/0000_baseline.json")

    # 追加到 iterations.tsv
    tsv_path = exp_dir / "history" / "iterations.tsv"
    with open(tsv_path, "a", encoding="utf-8") as f:
        f.write(f"0000\t{baseline_result['backtest_id']}\tsuccess\t")
        f.write(f"{(metrics.get('annual_return') or 0):.4f}\t")
        f.write(f"{(metrics.get('max_drawdown') or 0):.4f}\t")
        f.write(f"{(metrics.get('sharpe') or 0):.4f}\t")
        f.write(f"{score:.4f}\tbaseline\tinitial_seed_config\n")
    print(f"✓ 追加记录：history/iterations.tsv")


def _init_git_repo(exp_dir: Path) -> None:
    """初始化 Git 仓库并提交 baseline"""
    print(f"\n[5/5] 初始化 Git 仓库")

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


# ── 主流程 ────────────────────────────────────────────────────────────────────


def main() -> None:
    args = _parse_args()

    print("=" * 70)
    print("向导式策略自动研究系统初始化")
    print("=" * 70)

    exp_dir = _init_experiment_dir(args.name, None, args)
    config_path = exp_dir / "wizard_config.json"

    strategy_id, use_mock = _create_ricequant_strategy(args.name, args, config_path)

    _update_state_strategy_id(exp_dir, strategy_id)

    baseline_result = _run_baseline_backtest(exp_dir, args, strategy_id, use_mock)

    _update_state_with_baseline(exp_dir, baseline_result)

    _init_git_repo(exp_dir)

    print("\n" + "=" * 70)
    print("初始化完成！")
    print("=" * 70)
    print(f"\n实验目录：{exp_dir}")
    print(f"策略 ID：{strategy_id}")
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
