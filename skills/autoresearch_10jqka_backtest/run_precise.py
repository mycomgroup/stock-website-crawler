#!/usr/bin/env python3
"""精确修改参数并运行一次迭代"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from scorer import (
    parse_backtest_result,
    calculate_score,
    calculate_complexity,
    decide_keep_rollback,
    DEFAULT_WEIGHTS,
    DEFAULT_HARD_CONSTRAINTS,
)
from formula_executor import run_backtest


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def git_commit(base: Path, message: str) -> bool:
    import subprocess
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
    except Exception as e:
        print(f"[git] 异常: {e}", flush=True)
        return False


def git_restore(base: Path, filename: str) -> bool:
    import subprocess
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


def append_tsv(base: Path, row: dict):
    tsv = base / "iterations.tsv"
    header = "iter\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\n"
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
            f.write(header)
        f.write(line)


def update_state(state: dict, base: Path, iter_n: int, decision: str, score: float):
    state["current_iter"] = iter_n + 1
    state["last_update"] = datetime.now().isoformat()
    if decision == "keep":
        state["champion_score"] = score
        state["consecutive_failures"] = 0
    else:
        state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1
    save_json(base / "state.json", state)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--mutation-summary", required=True)
    parser.add_argument("--set-formula", action="append", default=[], help='e.g. "市盈率小于50->市盈率小于40"')
    parser.add_argument("--set-param", action="append", default=[], help='e.g. "takeProfit=20"')
    args = parser.parse_args()

    base = Path(args.base)
    state = load_json(base / "state.json")
    iter_n = state.get("current_iter", 1)
    iter_id = f"{iter_n:04d}"

    champion_config = load_json(base / "formula_config.json")
    champion_score = float(state.get("champion_score", float("-inf")))

    new_config = json.loads(json.dumps(champion_config))
    mutation_parts = []

    # apply formula replacements
    for repl in args.set_formula:
        if "->" in repl:
            old, new = repl.split("->", 1)
            old = old.strip()
            new = new.strip()
            if old in new_config["formula"]:
                idx = new_config["formula"].index(old)
                new_config["formula"][idx] = new
                mutation_parts.append(f"[替换条件] {old} → {new}")
            else:
                print(f"[WARN] {old} not found in formula")
        else:
            new_config["formula"].append(repl.strip())
            mutation_parts.append(f"[添加条件] {repl.strip()}")

    # apply param changes
    for param in args.set_param:
        key, val = param.split("=", 1)
        key = key.strip()
        val = val.strip()
        old_val = new_config.get(key)
        # try int conversion
        try:
            val = int(val)
        except ValueError:
            pass
        new_config[key] = val
        mutation_parts.append(f"[{key}] {old_val} → {val}")

    mutation_desc = "; ".join(mutation_parts) if mutation_parts else args.mutation_summary

    save_json(base / "formula_config.json", new_config)
    print(f"[{iter_id}] 变异: {mutation_desc}", flush=True)

    try:
        result = run_backtest(new_config)
        backtest_id = result.get("backtest_id", "")
        metrics = parse_backtest_result(result)
        complexity = calculate_complexity(new_config)
        score = calculate_score(metrics, weights=DEFAULT_WEIGHTS, complexity=complexity, config=new_config)
        decision, reason = decide_keep_rollback(
            new_score=score,
            champion_score=champion_score,
            new_metrics=metrics,
            champion_metrics=None,
            hard_constraints=DEFAULT_HARD_CONSTRAINTS,
        )
        print(
            f"[{iter_id}] score={score:.4f} champion={champion_score:.4f} "
            f"annual={metrics.annual_return:.2%} dd={metrics.max_drawdown:.2%} "
            f"decision={decision}",
            flush=True,
        )

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
            git_msg = f"keep: iter_{iter_id} score={score:.4f} annual={metrics.annual_return:.2%} dd={metrics.max_drawdown:.2%}\n{mutation_desc}"
            git_commit(base, git_msg)
            print(f"[{iter_id}] keep", flush=True)
            sys.exit(0)
        else:
            git_restore(base, "formula_config.json")
            update_state(state, base, iter_n, "rollback", champion_score)
            print(f"[{iter_id}] rollback — {reason}", flush=True)
            sys.exit(1)

    except Exception as e:
        print(f"[{iter_id}] CRASH: {e}", flush=True)
        append_tsv(
            base,
            {
                "iter": iter_id,
                "backtest_id": "",
                "status": "crash",
                "annual_return": 0.0,
                "max_drawdown": 0.0,
                "sharpe": 0.0,
                "score": float("-inf"),
                "decision": "crash",
                "mutation": args.mutation_summary,
            },
        )
        git_restore(base, "formula_config.json")
        update_state(state, base, iter_n, "crash", champion_score)
        sys.exit(2)


if __name__ == "__main__":
    main()
