#!/usr/bin/env python3
"""
果仁策略自动研究系统初始化脚本

功能：
1. 创建实验目录结构
2. 复制种子配置
3. 初始化 state.json
4. 创建 history/ 目录和 iterations.tsv
5. 生成 program.md 和 README.md
6. 初始化 Git 仓库

用法示例：
    python init_experiment.py --name my_experiment --seed-config seed_config.json
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# 添加 skill 根目录到 sys.path，以便 import 本地模块
sys.path.insert(0, str(Path(__file__).parent))


# ── 路径常量 ──────────────────────────────────────────────────────────────────
SKILL_ROOT = Path(__file__).parent
EXPERIMENTS_DIR = SKILL_ROOT / "experiments"
DEFAULT_SEED_CONFIG = SKILL_ROOT / "seed_config.json"
PROGRAM_MD_PATH = SKILL_ROOT / "program.md"


# ── 工具函数 ──────────────────────────────────────────────────────────────────


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="果仁策略自动研究系统初始化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例：\n  python init_experiment.py --name my_experiment",
    )
    parser.add_argument("--name", required=True, help="实验名称（用作目录名）")
    parser.add_argument(
        "--seed-config",
        default=str(DEFAULT_SEED_CONFIG),
        help=f"种子配置文件路径（默认：{DEFAULT_SEED_CONFIG}）",
    )
    return parser.parse_args()


def _load_seed_config(seed_config_path: str) -> dict:
    """读取种子配置文件"""
    path = Path(seed_config_path)
    if not path.exists():
        print(f"错误：种子配置文件不存在：{path}", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _create_experiment_dir(name: str) -> Path:
    """创建实验目录结构"""
    print(f"\n[1/5] 创建实验目录：experiments/{name}")

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

    return exp_dir


def _init_config_and_state(exp_dir: Path, seed_config: dict) -> None:
    """初始化配置和状态文件"""
    print(f"\n[2/5] 初始化配置和状态文件")

    # 复制种子配置到 guorn_config.json
    config_path = exp_dir / "guorn_config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(seed_config, f, ensure_ascii=False, indent=2)
    print(f"✓ 写入配置：guorn_config.json")

    # 创建初始 state.json
    state = {
        "current_iter": 0,
        "champion_score": -1e308,
        "champion_iter": "",
        "champion_config": None,
        "champion_metrics": None,
        "consecutive_failures": 0,
        "last_update": datetime.now(timezone.utc).isoformat(),
    }
    state_path = exp_dir / "state.json"
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"✓ 写入状态：state.json")


def _create_documentation(exp_dir: Path, name: str, seed_config: dict) -> None:
    """创建文档文件"""
    print(f"\n[3/5] 创建文档文件")

    # 复制 program.md 并注入策略信息
    program_dest = exp_dir / "program.md"
    if PROGRAM_MD_PATH.exists():
        with open(PROGRAM_MD_PATH, encoding="utf-8") as src:
            content = src.read()
            # 替换占位符
            strategy_name = seed_config.get("name", "未命名策略")
            strategy_desc = seed_config.get("description", "无描述")
            content = content.replace("{{STRATEGY_NAME}}", strategy_name)
            content = content.replace("{{STRATEGY_DESCRIPTION}}", strategy_desc)
            with open(program_dest, "w", encoding="utf-8") as dst:
                dst.write(content)
        print(f"✓ 生成指南：program.md（已注入策略目标）")

    # 创建 README.md
    readme_path = exp_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {name}\n\n")
        f.write(f"果仁策略自动研究实验\n\n")
        f.write(f"- 创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 开始迭代\n\n")
        f.write("```bash\n")
        f.write(f"cd {exp_dir}\n")
        f.write("# 阅读 program.md，然后让 agent 开始迭代\n")
        f.write("```\n\n")
        f.write("## 查看状态\n\n")
        f.write("```bash\n")
        f.write("cat state.json\n")
        f.write("cat history/iterations.tsv\n")
        f.write("```\n")
    print(f"✓ 创建说明：README.md")


def _init_history(exp_dir: Path, seed_config: dict) -> None:
    """初始化 history/ 目录"""
    print(f"\n[4/5] 初始化 history/ 目录")

    history_dir = exp_dir / "history"

    # 创建 iterations.tsv
    tsv_path = history_dir / "iterations.tsv"
    with open(tsv_path, "w", encoding="utf-8") as f:
        f.write(
            "iter\tcommit\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\n"
        )
    print(f"✓ 创建记录：history/iterations.tsv")

    # 保存初始配置快照
    snapshot_path = history_dir / "0000_config.json"
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(seed_config, f, ensure_ascii=False, indent=2)
    print(f"✓ 保存快照：history/0000_config.json")

    # 创建 search_notes.md 模板
    notes_path = history_dir / "search_notes.md"
    with open(notes_path, "w", encoding="utf-8") as f:
        f.write("# 搜索笔记\n\n")
        f.write("## 搜索地图\n\n")
        f.write("### 已验证有效（keep）\n\n")
        f.write("（暂无）\n\n")
        f.write("### 已验证无效（rollback）\n\n")
        f.write("（暂无）\n\n")
        f.write("### 待探索方向\n\n")
        f.write("- [ ] 添加筛选条件（如市净率、换手率等）\n")
        f.write("- [ ] 调整排序权重\n")
        f.write("- [ ] 调整持仓数量\n")
        f.write("- [ ] 调整调仓间隔\n\n")
        f.write("### 规律总结\n\n")
        f.write("（暂无）\n")
    print(f"✓ 创建笔记：history/search_notes.md")


def _run_baseline_backtest(exp_dir: Path, seed_config: dict) -> None:
    """用种子配置跑一次回测，建立真实基准分数"""
    print(f"\n[6/6] 运行基准回测（种子配置）")

    try:
        from guorn_executor import run_backtest, GuornExecutorError, BacktestTimeoutError
        from scorer import (
            parse_backtest_result,
            calculate_score,
            DEFAULT_WEIGHTS,
            DEFAULT_HARD_CONSTRAINTS,
        )
    except ImportError as e:
        print(f"  警告：无法导入回测模块（{e}），跳过基准回测")
        print(f"  提示：第一次 run_iteration.py 将以 -inf 为基准")
        return

    start_time = datetime.now(timezone.utc)
    try:
        result = run_backtest(seed_config)
        end_time = datetime.now(timezone.utc)
        elapsed = (end_time - start_time).total_seconds()
        print(f"  回测完成，耗时 {elapsed:.1f} 秒，ID: {result['backtest_id']}")
    except (GuornExecutorError, BacktestTimeoutError) as e:
        print(f"  警告：基准回测失败（{e}），跳过")
        print(f"  提示：第一次 run_iteration.py 将以 -inf 为基准")
        return

    # 解析结果
    try:
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
        from scorer import parse_backtest_result, calculate_score, DEFAULT_WEIGHTS
        metrics = parse_backtest_result(result_json)
        score = calculate_score(metrics, weights=DEFAULT_WEIGHTS)
    except Exception as e:
        print(f"  警告：解析基准结果失败（{e}），跳过")
        return

    print(f"  年化收益: {metrics.annual_return:.4f}")
    print(f"  最大回撤: {metrics.max_drawdown:.4f}")
    print(f"  Sortino:  {metrics.sortino:.4f}")
    print(f"  信息比率: {metrics.information_ratio:.4f}")
    print(f"  基准得分: {score:.6f}")

    # 更新 state.json：写入真实基准
    state_path = exp_dir / "state.json"
    with open(state_path, encoding="utf-8") as f:
        state = json.load(f)

    state["champion_score"] = score
    state["champion_iter"] = "0000"
    state["champion_config"] = seed_config
    state["champion_metrics"] = {
        "status": metrics.status,
        "backtest_id": metrics.backtest_id,
        "total_return": metrics.total_return,
        "annual_return": metrics.annual_return,
        "max_drawdown": metrics.max_drawdown,
        "sharpe": metrics.sharpe,
        "sortino": metrics.sortino,
        "information_ratio": metrics.information_ratio,
        "win_rate": metrics.win_rate,
        "avg_holding_days": metrics.avg_holding_days,
        "sell_count": metrics.sell_count,
    }
    state["last_update"] = datetime.now(timezone.utc).isoformat()

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"  ✓ state.json 已更新，基准得分 = {score:.6f}")

    # 写入 history/0000.json
    history_dir = exp_dir / "history"
    baseline_record = {
        "iter": "0000",
        "commit": "baseline",
        "backtest_id": metrics.backtest_id,
        "status": metrics.status,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "elapsed_seconds": elapsed,
        "annual_return": metrics.annual_return,
        "max_drawdown": metrics.max_drawdown,
        "win_rate": metrics.win_rate,
        "information_ratio": metrics.information_ratio,
        "sharpe": metrics.sharpe,
        "sortino": metrics.sortino,
        "avg_holding_days": metrics.avg_holding_days,
        "sell_count": metrics.sell_count,
        "score": score,
        "decision": "baseline",
        "reason": "种子配置基准回测",
        "mutation": "baseline",
        "mutation_type": "baseline",
    }
    with open(history_dir / "0000.json", "w", encoding="utf-8") as f:
        json.dump(baseline_record, f, ensure_ascii=False, indent=2)

    # 追加到 iterations.tsv
    tsv_path = history_dir / "iterations.tsv"
    with open(tsv_path, "a", encoding="utf-8") as f:
        f.write(
            f"0000\tbaseline\t{metrics.backtest_id}\t{metrics.status}\t"
            f"{metrics.annual_return:.4f}\t{metrics.max_drawdown:.4f}\t"
            f"{metrics.sharpe:.4f}\t{score:.6f}\tbaseline\t种子配置基准回测\n"
        )
    print(f"  ✓ history/0000.json 和 iterations.tsv 已写入")


def _init_git_repo(exp_dir: Path) -> None:
    """初始化 Git 仓库"""
    print(f"\n[5/6] 初始化 Git 仓库")

    try:
        subprocess.run(["git", "init"], cwd=exp_dir, check=True, capture_output=True)
        subprocess.run(
            ["git", "add", "."], cwd=exp_dir, check=True, capture_output=True
        )
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
    print("果仁策略自动研究系统初始化")
    print("=" * 70)

    # 1. 读取种子配置
    seed_config = _load_seed_config(args.seed_config)

    # 2. 创建实验目录
    exp_dir = _create_experiment_dir(args.name)

    # 3. 初始化配置和状态
    _init_config_and_state(exp_dir, seed_config)

    # 4. 创建文档
    _create_documentation(exp_dir, args.name, seed_config)

    # 5. 初始化 history/
    _init_history(exp_dir, seed_config)

    # 6. 初始化 Git 仓库
    _init_git_repo(exp_dir)

    # 7. 运行基准回测
    _run_baseline_backtest(exp_dir, seed_config)

    print("\n" + "=" * 70)
    print("初始化完成！")
    print("=" * 70)
    print(f"\n实验目录：{exp_dir}")
    print(f"\n下一步：")
    print(f"  cd {exp_dir}")
    print(f"  # 阅读 program.md，然后让 agent 开始迭代")
    print()


if __name__ == "__main__":
    main()
