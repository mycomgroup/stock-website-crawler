#!/usr/bin/env python3
"""
setup.py - 一条命令完成全部初始化

用法：
    python setup.py --strategy-file /path/to/strategy.py [--name my_strategy]

流程：
    1. 在 RiceQuant 创建/复用专用策略，获取 strategy_id
    2. 在实验目录生成 seed_config.json
    3. 创建目录结构，复制策略为 strategy.py
    4. 提交 baseline 回测，等待结果，写入 state.json 和 history/

实验目录：skills/autoresearch/strategy_autoresearch_<name>/
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from ricequant_executor import run_backtest, fetch_results, wait_for_completion
from scorer import parse_backtest_result, calculate_score
from preflight_checker import run_all_checks

AUTORESEARCH_DIR = Path(__file__).parent
RQ_STRATEGY_DIR = AUTORESEARCH_DIR.parent / "ricequant_strategy"
CREATE_STRATEGY_JS = RQ_STRATEGY_DIR / "create_rq_strategy.js"

TSV_HEADER = "iter\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\n"

from datetime import datetime, timedelta

def _default_dates():
    today = datetime.today()
    end = (today - timedelta(days=7)).strftime("%Y-%m-%d")   # 上周，确保数据完整
    start = (today - timedelta(days=365 * 5)).strftime("%Y-%m-%d")  # 最近5年
    return start, end

_start, _end = _default_dates()

# 默认回测参数（动态：最近一年）
DEFAULT_BACKTEST = {
    "start_date": _start,
    "end_date": _end,
    "capital": "100000",
    "freq": "day",
    "benchmark": "000300.XSHG",
}
DEFAULT_OBJECTIVE = {
    "weights": {"calmar": 0.55, "sortino": 0.25, "information_ratio": 0.20},
    "hard_constraints": {"max_drawdown_limit": 0.35},
}
DEFAULT_LOOP = {"max_iterations": 100, "max_consecutive_failures": 5, "max_wait_seconds": 600}


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create_rq_strategy(strategy_file: str, strategy_name: str) -> str:
    """调用 create_rq_strategy.js，返回 strategy_id"""
    if not CREATE_STRATEGY_JS.exists():
        raise FileNotFoundError(f"create_rq_strategy.js 不存在: {CREATE_STRATEGY_JS}")

    result = subprocess.run(
        ["node", str(CREATE_STRATEGY_JS), "--name", strategy_name, "--file", strategy_file],
        capture_output=True, text=True, timeout=120, cwd=str(RQ_STRATEGY_DIR)
    )

    if result.returncode != 0:
        raise RuntimeError(f"create_rq_strategy.js 失败:\n{result.stderr}\n{result.stdout}")

    # 打印所有输出（stderr + stdout 里的非 JSON 行）作为进度日志
    for line in (result.stderr + result.stdout).split("\n"):
        line = line.strip()
        if line and not line.startswith("{"):
            print(f"  {line}")

    # 从 stdout 里找最后一个 JSON 对象（忽略 console.log 混入的非 JSON 行）
    json_output = None
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line.startswith("{"):
            try:
                json_output = json.loads(line)
            except json.JSONDecodeError:
                pass
    # 也尝试把整个 stdout 当多行 JSON 解析
    if json_output is None:
        stdout = result.stdout.strip()
        # 找最后一个 { 开头的完整 JSON 块
        last_brace = stdout.rfind("{")
        if last_brace >= 0:
            try:
                json_output = json.loads(stdout[last_brace:])
            except json.JSONDecodeError:
                pass

    if json_output is None:
        raise RuntimeError(f"无法从输出中解析 JSON\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")

    strategy_id = json_output["strategy_id"]
    action = json_output.get("action", "")
    print(f"[rq] strategy_id={strategy_id} ({action})")
    return strategy_id


def init_state(base: Path, strategy_id: str) -> None:
    save_json(base / "state.json", {
        "current_iter": 1,
        "consecutive_failures": 0,
        "champion_iter": "0000_baseline",
        "champion_score": float("-inf"),
        "champion_metrics": None,
        "is_baseline_done": False,
        "strategy_id": strategy_id,
        "last_update": datetime.now().isoformat(),
    })


def init_history(base: Path) -> None:
    (base / "history").mkdir(parents=True, exist_ok=True)
    tsv = base / "history" / "iterations.tsv"
    if not tsv.exists():
        tsv.write_text(TSV_HEADER, encoding="utf-8")


def append_tsv(base: Path, row: dict) -> None:
    tsv = base / "history" / "iterations.tsv"
    line = "\t".join([
        str(row.get("iter", "")),
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


def run_baseline(base: Path, cfg: dict, baseline_commit: str = "") -> None:
    strategy_id = cfg["seed"]["strategy_id"]
    bt_cfg = cfg["backtest"]
    obj_cfg = cfg.get("objective", {})
    strategy_file = str(base / "strategy.py")

    passed, reasons = run_all_checks(strategy_file)
    if not passed:
        print(f"[preflight FAILED] {reasons}")
        sys.exit(1)
    print("[preflight] OK")

    print(f"[baseline] 提交回测 strategy_id={strategy_id} ...")
    start_time = datetime.now()
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
    print(f"[baseline] backtest_id={backtest_id}")

    wait_result = wait_for_completion(
        strategy_id=strategy_id,
        backtest_id=backtest_id,
        max_wait_seconds=cfg.get("loop", {}).get("max_wait_seconds", 600),
        poll_interval=10,
    )
    end_time = datetime.now()

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

    iter_record = {
        "iter": "0000_baseline",
        "commit": baseline_commit,
        "backtest_id": backtest_id,
        "status": metrics.status,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "annual_return": metrics.annual_return,
        "max_drawdown": metrics.max_drawdown,
        "sharpe": metrics.sharpe,
        "sortino": metrics.sortino,
        "information_ratio": metrics.information_ratio,
        "score": score,
        "decision": "keep",
        "mutation": "baseline - no modification",
        "fetch_result": fetch,
    }

    save_json(base / "history" / "0000_baseline.json", iter_record)
    append_tsv(base, iter_record)

    # 更新 state.json
    state = json.loads((base / "state.json").read_text())
    state.update({
        "is_baseline_done": True,
        "champion_iter": "0000_baseline",
        "champion_score": score,
        "champion_metrics": {
            "annual_return": metrics.annual_return,
            "max_drawdown": metrics.max_drawdown,
            "sharpe": metrics.sharpe,
            "sortino": metrics.sortino,
            "information_ratio": metrics.information_ratio,
            "status": metrics.status,
            "backtest_id": backtest_id,
        },
        "last_update": datetime.now().isoformat(),
    })
    save_json(base / "state.json", state)

    print(f"[baseline] 完成 score={score:.4f} annual={metrics.annual_return:.2%} "
          f"dd={metrics.max_drawdown:.2%} sharpe={metrics.sharpe:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description="一条命令完成初始化 + Baseline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python setup.py --strategy-file /path/to/rfscore7_pb10_final_v2.py
  python setup.py --strategy-file /path/to/strategy.py --name my_strategy
        """
    )
    parser.add_argument("--strategy-file", required=True, help="seed 策略文件路径（.py）")
    parser.add_argument("--name", default=None,
                        help="策略名称，用于目录命名（默认取文件名去掉 .py）")
    parser.add_argument("--start-date", default=DEFAULT_BACKTEST["start_date"])
    parser.add_argument("--end-date", default=DEFAULT_BACKTEST["end_date"])
    parser.add_argument("--capital", default=DEFAULT_BACKTEST["capital"])
    parser.add_argument("--benchmark", default=DEFAULT_BACKTEST["benchmark"])
    args = parser.parse_args()

    strategy_file = Path(args.strategy_file).resolve()
    if not strategy_file.exists():
        print(f"错误：策略文件不存在: {strategy_file}")
        sys.exit(1)

    # 策略名称：用户指定 or 文件名，加日期后缀防止同名冲突
    ts = datetime.now().strftime("%Y%m%d")
    strategy_name = args.name or f"{strategy_file.stem}_{ts}"
    rq_strategy_name = f"autoresearch_{strategy_name}"
    base = AUTORESEARCH_DIR / f"strategy_autoresearch_{strategy_name}"

    print(f"[setup] 策略文件: {strategy_file}")
    print(f"[setup] 实验目录: {base}")
    print(f"[setup] RiceQuant 策略名: {rq_strategy_name}")

    # 已完成则跳过
    state_file = base / "state.json"
    if state_file.exists():
        state = json.loads(state_file.read_text())
        if state.get("is_baseline_done"):
            print("[setup] 已完成初始化，跳过。如需重新初始化请删除实验目录。")
            return

    # ── Step 1：在 RiceQuant 创建/复用策略 ────────────────────────────────
    print("\n[Step 1] 在 RiceQuant 创建/复用策略...")
    strategy_id = create_rq_strategy(str(strategy_file), rq_strategy_name)

    # ── Step 2：创建目录结构 ───────────────────────────────────────────────
    print("\n[Step 2] 创建实验目录...")
    base.mkdir(parents=True, exist_ok=True)
    (base / "history").mkdir(exist_ok=True)

    # 复制策略
    shutil.copy2(strategy_file, base / "strategy.py")
    print(f"  复制策略: {strategy_file.name} → strategy.py")

    # git init + baseline commit（让 rollback 有据可查）
    subprocess.run(["git", "init"], cwd=str(base), capture_output=True)
    subprocess.run(["git", "add", "strategy.py"], cwd=str(base), capture_output=True)
    r = subprocess.run(
        ["git", "commit", "-m", "iter_0000_baseline: initial strategy"],
        cwd=str(base), capture_output=True, text=True
    )
    if r.returncode == 0:
        r2 = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(base), capture_output=True, text=True)
        _baseline_commit = r2.stdout.strip()
        print(f"  git init + baseline commit {_baseline_commit}")
    else:
        _baseline_commit = ""
        print(f"  git init 失败（非致命）: {r.stderr.strip()}")

    # 生成 seed_config.json 到实验目录
    cfg = {
        "project": {"strategy_name": strategy_name},
        "seed": {
            "strategy_file": str(strategy_file),
            "strategy_id": strategy_id,
            "strategy_name": rq_strategy_name,
        },
        "backtest": {
            "start_date": args.start_date,
            "end_date": args.end_date,
            "capital": args.capital,
            "freq": DEFAULT_BACKTEST["freq"],
            "benchmark": args.benchmark,
        },
        "objective": DEFAULT_OBJECTIVE,
        "loop": DEFAULT_LOOP,
    }
    save_json(base / "seed_config.json", cfg)
    print(f"  生成 seed_config.json (strategy_id={strategy_id})")

    # 生成 program.md，替换所有占位符为真实值
    src_program = AUTORESEARCH_DIR / "program.md"
    if src_program.exists():
        content = src_program.read_text(encoding="utf-8")
        content = content.replace("STRATEGY_NAME", strategy_name)
        content = content.replace(
            'AUTORESEARCH_DIR="/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch"',
            f'AUTORESEARCH_DIR="{AUTORESEARCH_DIR}"'
        )
        (base / "program.md").write_text(content, encoding="utf-8")

    # 生成 program_enhance.md（增强版，含通用机制库引用）
    src_enhance = AUTORESEARCH_DIR / "program_enhance.md"
    if src_enhance.exists():
        content = src_enhance.read_text(encoding="utf-8")
        content = content.replace("STRATEGY_NAME", strategy_name)
        content = content.replace(
            'AUTORESEARCH_DIR="/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch"',
            f'AUTORESEARCH_DIR="{AUTORESEARCH_DIR}"'
        )
        (base / "program_enhance.md").write_text(content, encoding="utf-8")
        print(f"  生成 program_enhance.md（增强版，含通用机制库）")

    # 生成 README.md，替换所有占位符为真实值
    src_readme = AUTORESEARCH_DIR / "README.md"
    if src_readme.exists():
        content = src_readme.read_text(encoding="utf-8")
        # 替换策略名占位符
        content = content.replace("strategy_autoresearch_<策略名>", f"strategy_autoresearch_{strategy_name}")
        content = content.replace("strategy_autoresearch_<name>", f"strategy_autoresearch_{strategy_name}")
        content = content.replace("`autoresearch_<name>`", f"`autoresearch_{strategy_name}`")
        content = content.replace("autoresearch_<name>", f"autoresearch_{strategy_name}")
        # 替换 Step 2 里的启动提示
        content = content.replace(
            f"请阅读 {base}/program.md，然后开始迭代优化循环。",
            "请阅读 program.md，然后开始迭代优化循环。"
        )
        # 替换 Step 3 里的示例路径
        content = content.replace(
            "cat strategy_autoresearch_rfscore7_pb10_rq/history/iterations.tsv",
            f"cat strategy_autoresearch_{strategy_name}/history/iterations.tsv"
        )
        # 替换回测参数为实际值
        content = content.replace("--start-date 2021-01-01", f"--start-date {args.start_date}")
        content = content.replace("--end-date 2025-03-28", f"--end-date {args.end_date}")
        content = content.replace("--capital 100000", f"--capital {args.capital}")
        content = content.replace("--benchmark 000300.XSHG", f"--benchmark {args.benchmark}")
        # 替换 strategy_id 信息
        content = content.replace(
            "/path/to/your/strategy.py",
            str(strategy_file)
        )
        (base / "README.md").write_text(content, encoding="utf-8")

    # 初始化状态和台账
    init_state(base, strategy_id)
    init_history(base)
    print("  初始化完成")

    # ── Step 3：运行 Baseline ─────────────────────────────────────────────
    print("\n[Step 3] 运行 Baseline 回测...")
    run_baseline(base, cfg, baseline_commit=_baseline_commit)

    print(f"\n[setup] 全部完成！")
    print(f"  实验目录: {base}")
    print(f"  下一步：把 {base}/program.md 发给 agent 开始迭代")


if __name__ == "__main__":
    main()
