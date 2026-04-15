#!/usr/bin/env python3
"""
run_iteration.py - 执行单次迭代

用法：
    python run_iteration.py --base . --mutation-summary "改动描述"

流程：
    1. 加载 search_notes.md
    2. 生成新因子组合
    3. 更新 strategy.py
    4. git commit
    5. 执行 Notebook
    6. 评分 + 决策
    7. keep/rollback
    8. 更新 search_notes.md
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

AUTORESEARCH_DIR = Path(__file__).parent
sys.path.insert(0, str(AUTORESEARCH_DIR))

from combination_generator import CombinationGenerator
from notebook_executor import execute_strategy
from factor_categories import FACTOR_CATEGORIES


def get_full_factor_pool() -> list:
    """获取完整因子池"""
    factors = []
    for category, fs in FACTOR_CATEGORIES.items():
        factors.extend(fs)
    return list(set(factors))


def parse_search_notes(content: str) -> dict:
    """解析 search_notes.md"""
    state = {}
    history = []
    keep_list = []
    rollback_list = []
    todo_list = []
    notebook_info = {}
    
    current_section = None
    in_table = False
    
    for line in content.split("\n"):
        line = line.strip()
        
        if line.startswith("## "):
            current_section = line[3:].strip()
            in_table = False
            continue
        
        if current_section == "当前状态":
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().strip("-").strip()  # 修复：移除 - 和多余空格
                val = val.strip()
                try:
                    state[key] = float(val) if "." in val else int(val)
                except:
                    state[key] = val

        elif current_section == "Notebook 信息":
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().strip("-").strip()  # 修复：移除 - 和多余空格
                notebook_info[key] = val.strip()

        elif current_section == "回测配置":
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().strip("-").strip()  # 修复：移除 - 和多余空格
                state[key] = val.strip()
        
        elif current_section == "已尝试组合" and "|" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 4 and parts[0] != "iter":
                try:
                    history.append({
                        "iter": parts[0],
                        "score": float(parts[1]),
                        "factors": parts[2],
                        "strategy": parts[3],
                    })
                except:
                    pass
        
        elif current_section == "已验证有效（keep）":
            if line.startswith("- "):
                keep_list.append(line[2:])
        
        elif current_section == "已验证无效（rollback）":
            if line.startswith("- "):
                rollback_list.append(line[2:])
        
        elif current_section == "待探索方向":
            if line.startswith("- [ ]"):
                todo_list.append(line[6:])
            elif line.startswith("- [x]") or line.startswith("- [X]"):
                pass
    
    return {
        "state": state,
        "history": history,
        "keep_list": keep_list,
        "rollback_list": rollback_list,
        "todo_list": todo_list,
        "notebook_info": notebook_info,
    }


def update_search_notes(
    base: Path, parsed: dict, result: dict, decision: str, reason: str
):
    """更新 search_notes.md"""
    state = parsed["state"]
    history = parsed["history"]

    current_iter = state.get("current_iter", 0) + 1
    state["current_iter"] = current_iter

    score = result.get("score", 0)
    factors = result.get("factors", [])
    strategy = result.get("strategy", "unknown")

    if decision == "keep":
        state["champion_score"] = score
        state["champion_factors"] = factors
        state["consecutive_failures"] = 0
    else:
        state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1

    if score > state.get("champion_score", -999):
        state["phase"] = "converge" if score > 1.5 else "explore"

    # 更新历史表格
    history.append(
        {
            "iter": f"{current_iter:04d}",
            "score": score,
            "factors": str(factors),
            "strategy": strategy,
        }
    )

    # 构建新内容
    lines = []
    lines.append("## 当前状态")
    for k, v in state.items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("## 回测配置")
    lines.append(f"- 日期范围: {state.get('日期范围', 'N/A')}")
    lines.append(f"- 选股池: {state.get('选股池', 'N/A')}")
    lines.append("")

    lines.append("## 已尝试组合")
    lines.append("| iter | score | factors | strategy |")
    lines.append("|------|-------|---------|----------|")
    for h in history[-20:]:
        lines.append(
            f"| {h['iter']} | {h['score']:.4f} | {h['factors']} | {h['strategy']} |"
        )
    lines.append("")

    lines.append("## 搜索地图")
    lines.append("")
    lines.append("### 已验证有效（keep）")
    if decision == "keep":
        lines.append(f"- {factors}: score={score:.4f}, {reason}")
    for item in parsed["keep_list"]:
        lines.append(f"- {item}")
    lines.append("")

    lines.append("### 已验证无效（rollback）")
    if decision == "rollback":
        lines.append(f"- {factors}: score={score:.4f}, {reason}")
    for item in parsed["rollback_list"]:
        lines.append(f"- {item}")
    lines.append("")

    lines.append("### 待探索方向")
    for item in parsed["todo_list"]:
        lines.append(f"- [ ] {item}")
    lines.append("")

    (base / "search_notes.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="执行单次因子搜索迭代")
    parser.add_argument("--base", default=".", help="实验目录路径")
    parser.add_argument("--mutation-summary", default="", help="改动描述")
    parser.add_argument("--notebook-dir", default=None, help="joinquant_notebook 目录")
    args = parser.parse_args()

    base = Path(args.base).resolve()
    search_notes_file = base / "search_notes.md"
    strategy_file = base / "strategy.py"

    if not search_notes_file.exists():
        print("[错误] search_notes.md 不存在，请先运行 setup.py")
        sys.exit(1)

    # 解析 search_notes.md
    content = search_notes_file.read_text(encoding="utf-8")
    parsed = parse_search_notes(content)

    state = parsed["state"]
    current_iter = state.get("current_iter", 0) + 1

    print(f"\n{'=' * 60}")
    print(f"Iteration: {current_iter}")
    print(f"Mutation: {args.mutation_summary}")
    print(f"Champion score: {state.get('champion_score', 0):.4f}")
    print(f"Phase: {state.get('phase', 'explore')}")
    print(f"{'=' * 60}\n")

    # 生成新因子组合
    factor_pool = get_full_factor_pool()

    tried = set()
    for h in parsed["history"]:
        try:
            factors = eval(h["factors"])
            tried.add(tuple(sorted(factors)))
        except:
            pass

    existing = []
    for h in parsed["history"]:
        try:
            factors = eval(h["factors"])
            existing.append(factors)
        except:
            pass

    generator = CombinationGenerator(
        factor_pool=factor_pool,
        existing_combinations=existing,
        tried_combinations=tried,
    )
    generator.phase = state.get("phase", "explore")

    combo, strategy = generator.generate()
    if combo is None:
        print("[错误] 无新组合可尝试")
        sys.exit(1)

    print(f"新因子组合: {combo}")
    print(f"生成策略: {strategy}")

    # 更新 strategy.py
    strategy_content = strategy_file.read_text(encoding="utf-8")
    new_strategy = f"FACTOR_COMBO = {combo}"
    strategy_content = re.sub(
        r"FACTOR_COMBO\s*=\s*\[.*?\]",
        new_strategy,
        strategy_content,
        flags=re.DOTALL,
    )
    strategy_file.write_text(strategy_content, encoding="utf-8")

    # git commit
    subprocess.run(["git", "add", "strategy.py"], cwd=str(base), capture_output=True)
    r = subprocess.run(
        ["git", "commit", "-m", f"iter_{current_iter:04d}: {combo} ({strategy})"],
        cwd=str(base),
        capture_output=True,
        text=True,
    )

    if r.returncode == 0:
        print("[git] commit 成功")
    else:
        print(f"[git] commit 失败: {r.stderr}")

    # 执行 Notebook
    print("[执行] 提交 Notebook 回测...")
    
    notebook_info = parsed.get("notebook_info", {})
    notebook_path = notebook_info.get("notebook_path")
    notebook_url = notebook_info.get("notebook_url")
    
    result = execute_strategy(
        str(strategy_file),
        notebook_url=notebook_url,
        timeout_ms=600000,
        notebook_dir=args.notebook_dir,
    )

    if not result["success"]:
        print(f"[错误] 执行失败: {result.get('error')}")
        result["score"] = 0
        result["metrics"] = {}
        result["factors"] = combo
        result["strategy"] = strategy

    score = result.get("score", 0)
    metrics = result.get("metrics", {})
    diversity = result.get("diversity", metrics.get("diversity", 0))

    print(f"\n[结果] score={score:.4f}")
    print(f"[结果] diversity={diversity:.2f}")
    if metrics:
        print(f"[结果] ic_mean={metrics.get('ic_mean', 0):.4f}")
        print(f"[结果] long_short={metrics.get('long_short_return', 0):.4f}")

    # 决策
    from scorer import decide

    metrics["diversity"] = diversity  # 确保 diversity 在 metrics 中
    champion_score = state.get("champion_score", -999)
    decision, reason = decide(champion_score, score, metrics)

    print(f"\n[决策] {decision}: {reason}")

    if decision == "rollback":
        print("[rollback] 恢复 strategy.py...")
        subprocess.run(
            ["git", "reset", "--hard", "HEAD~1"],
            cwd=str(base),
            capture_output=True,
        )

    # 更新 search_notes.md
    result["strategy"] = strategy
    update_search_notes(base, parsed, result, decision, reason)

    print(f"\n[完成] search_notes.md 已更新")

    # 设置 exit code
    if decision == "keep":
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
