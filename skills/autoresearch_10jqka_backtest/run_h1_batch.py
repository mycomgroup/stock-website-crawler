#!/usr/bin/env python3
"""H_composite/h1 实验的 100 轮批量迭代"""
import subprocess
import sys
import json
import time
from pathlib import Path
from datetime import datetime

BASE = Path("trees/H_composite/experiments/h1")

def load_state():
    with open(BASE / "state.json", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    with open(BASE / "state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def append_tsv(row):
    tsv = BASE / "iterations.tsv"
    header = "iter\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\n"
    write_header = not tsv.exists()
    line = (
        "\t".join([
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
    )
    with open(tsv, "a", encoding="utf-8") as f:
        if write_header:
            f.write(header)
        f.write(line)

def main():
    state = load_state()
    start_iter = state.get("current_iter", 124)
    target_iter = start_iter + 100  # Run 100 more iterations

    print(f"Starting batch run: iter {start_iter} to {target_iter-1}")
    print(f"Current champion score: {state.get('champion_score', 'N/A')}")

    crash_count = 0
    max_crash = 15

    i = start_iter
    while i < target_iter:
        state = load_state()
        current_iter = state.get("current_iter", 124)
        if current_iter != i:
            print(f"State mismatch: expected {i}, got {current_iter}. Syncing.")
            i = current_iter

        iter_id = f"{i:04d}"
        mutation_summary = f"[随机探索] 自动变异 iter {i}"

        cmd = [
            sys.executable, "run_iteration.py",
            "--base", str(BASE),
            "--mutation-summary", mutation_summary,
        ]

        print(f"\n=== Running iter {iter_id} ({i-start_iter+1}/100) ===", flush=True)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = result.stdout + result.stderr
        print(output[-2000:] if len(output) > 2000 else output, flush=True)

        # Parse decision
        decision = "crash"
        score = 0.0
        annual = 0.0
        dd = 0.0
        backtest_id = ""

        for line in output.splitlines():
            if "决策: keep" in line or "decision=keep" in line:
                decision = "keep"
            elif "决策: rollback" in line or "decision=rollback" in line:
                decision = "rollback"
            if "backtest_id=" in line:
                parts = line.split("backtest_id=")
                if len(parts) > 1:
                    backtest_id = parts[1].split()[0]
            if "score=" in line and "champion=" in line:
                try:
                    score = float(line.split("score=")[1].split()[0])
                    annual_str = line.split("annual=")[1].split()[0].replace("%", "")
                    annual = float(annual_str) / 100.0 if annual_str else 0.0
                    dd_str = line.split("dd=")[1].split()[0].replace("%", "")
                    dd = float(dd_str) / 100.0 if dd_str else 0.0
                except Exception:
                    pass

        if decision == "crash":
            crash_count += 1
            print(f"Crash #{crash_count}")
            append_tsv({
                "iter": iter_id,
                "backtest_id": "",
                "status": "crash",
                "annual_return": 0.0,
                "max_drawdown": 0.0,
                "sharpe": 0.0,
                "score": float("-inf"),
                "decision": "crash",
                "mutation": mutation_summary,
            })
            if crash_count >= max_crash:
                print(f"Too many crashes ({max_crash}). Stopping batch.")
                break
        else:
            crash_count = 0

        # Small delay to avoid rate limiting
        time.sleep(3)
        i += 1

    print(f"\nBatch complete. Final iter: {i-1}")
    state = load_state()
    print(f"Current champion score: {state.get('champion_score', 'N/A')}")

if __name__ == "__main__":
    main()