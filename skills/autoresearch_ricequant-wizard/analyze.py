#!/usr/bin/env python3
"""
analyze.py - Wizard 实验结果分析工具

读取 iterations.tsv，输出分析报告：
  1. 总览（keep/rollback/crash 统计）
  2. Keep 序列（改进路径）
  3. Top 改进（按单次 score 提升排名）
  4. 失败模式分析
  5. 指标趋势（ASCII 折线图）

报告写入 analysis_report.txt，供用户查看。

Usage:
    python analyze.py --base experiments/<name>
"""

import argparse
from pathlib import Path
from datetime import datetime


def load_iterations(base: Path) -> list[dict]:
    tsv = base / "iterations.tsv"
    if not tsv.exists():
        return []

    records = []
    with open(tsv, encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        return []

    header = lines[0].strip().split("\t")
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.strip().split("\t")
        row = {}
        for i, col in enumerate(header):
            if i < len(parts):
                val = parts[i]
                if col in ("annual_return", "max_drawdown", "sharpe", "score"):
                    try:
                        row[col] = float(val)
                    except:
                        row[col] = 0.0
                else:
                    row[col] = val
            else:
                row[col] = ""
        records.append(row)

    for r in records:
        ar = r.get("annual_return", 0) or 0
        dd = abs(r.get("max_drawdown", 0) or 0)
        r["_calmar"] = ar / max(dd, 0.01)

    return records


def load_state(base: Path) -> dict:
    state_file = base / "state.json"
    if state_file.exists():
        import json

        return json.load(open(state_file, encoding="utf-8"))
    return {}


def ascii_sparkline(values: list[float], width: int = 50, height: int = 6) -> str:
    if not values:
        return "  (无数据)"
    valid = [v for v in values if v is not None]
    if not valid:
        return "  (无数据)"

    mn, mx = min(valid), max(valid)
    if mx == mn:
        mid = height // 2
        lines = []
        for row in range(height):
            marker = "─" * width if row == mid else " " * width
            lines.append(f"  {marker}")
        return "\n".join(lines)

    def scale(v):
        return int((v - mn) / (mx - mn) * (height - 1))

    step = max(1, len(valid) // width)
    sampled = valid[::step][:width]

    grid = [[" "] * len(sampled) for _ in range(height)]
    for x, v in enumerate(sampled):
        y = scale(v)
        grid[height - 1 - y][x] = "●"

    lines = []
    for row_idx, row in enumerate(grid):
        if row_idx == 0:
            label = f"{mx:6.3f} │"
        elif row_idx == height - 1:
            label = f"{mn:6.3f} │"
        else:
            label = "       │"
        lines.append(label + "".join(row))
    lines.append("       └" + "─" * len(sampled))
    lines.append(f"        0{' ' * (len(sampled) - 4)}{len(valid) - 1}")
    return "\n".join(lines)


def section_overview(records: list[dict], state: dict) -> str:
    lines = ["=" * 60, "  总览", "=" * 60]

    total = len(records)
    keeps = [r for r in records if r.get("decision") == "keep"]
    rollbacks = [r for r in records if r.get("decision") == "rollback"]
    crashes = [r for r in records if r.get("decision") == "crash"]
    baselines = [r for r in records if r.get("decision") == "baseline"]
    decided = len(keeps) + len(rollbacks)
    keep_rate = len(keeps) / decided if decided else 0

    lines.append(f"总迭代数:  {total}")
    lines.append(f"  keep:    {len(keeps)}")
    lines.append(f"  rollback:{len(rollbacks)}")
    lines.append(f"  crash:   {len(crashes)}")
    lines.append(f"keep rate: {keep_rate:.1%}  ({len(keeps)}/{decided})")
    lines.append("")

    baseline = baselines[0] if baselines else None
    champion = keeps[-1] if keeps else baseline

    def fmt(r):
        if not r:
            return "N/A"
        ar = r.get("annual_return", 0) or 0
        dd = abs(r.get("max_drawdown", 0) or 0)
        sh = r.get("sharpe", 0) or 0
        sc = r.get("score", 0) or 0
        calmar = r.get("_calmar", 0) or 0
        return (
            f"annual={ar:.2%}  dd={dd:.2%}  sharpe={sh:.3f}\n"
            f"         calmar={calmar:.2f}\n"
            f"         score={sc:.4f}"
        )

    lines.append(f"Baseline  [{(baseline or {}).get('iter', '?')}]")
    lines.append(f"  {fmt(baseline)}")
    lines.append(f"Champion  [{(champion or {}).get('iter', '?')}]")
    lines.append(f"  {fmt(champion)}")

    if baseline and champion:
        b_sc = baseline.get("score", 0) or 0
        c_sc = champion.get("score", 0) or 0
        b_ar = baseline.get("annual_return", 0) or 0
        c_ar = champion.get("annual_return", 0) or 0
        b_dd = abs(baseline.get("max_drawdown", 0) or 0)
        c_dd = abs(champion.get("max_drawdown", 0) or 0)
        lines.append("")
        lines.append("总提升:")
        lines.append(f"  score:   {b_sc:.4f} → {c_sc:.4f}  ({c_sc - b_sc:+.4f})")
        lines.append(f"  annual:  {b_ar:.2%} → {c_ar:.2%}  ({c_ar - b_ar:+.2%})")
        lines.append(f"  dd:      {b_dd:.2%} → {c_dd:.2%}  ({c_dd - b_dd:+.2%})")

    return "\n".join(lines)


def section_keep_sequence(records: list[dict]) -> str:
    lines = ["", "=" * 60, "  Keep 序列（改进路径）", "=" * 60]
    keeps = [r for r in records if r.get("decision") == "keep"]
    baselines = [r for r in records if r.get("decision") == "baseline"]

    if not keeps:
        lines.append("  (暂无 keep 记录)")
        return "\n".join(lines)

    all_keeps = baselines + keeps
    prev_score = None
    for r in all_keeps:
        sc = r.get("score", 0) or 0
        delta = f"{sc - prev_score:+.4f}" if prev_score is not None else "(baseline)"
        mutation = r.get("mutation", "")[:55]
        ar = r.get("annual_return", 0) or 0
        dd = abs(r.get("max_drawdown", 0) or 0)
        calmar = r.get("_calmar", 0) or 0
        lines.append(f"[{r.get('iter', '?'):>14}]  score={sc:.4f} ({delta})")
        lines.append(f"  annual={ar:.2%}  dd={dd:.2%}  calmar={calmar:.2f}")
        lines.append(f"  → {mutation}")
        prev_score = sc

    return "\n".join(lines)


def section_top_improvements(records: list[dict]) -> str:
    lines = ["", "=" * 60, "  Top 改进（按单次 score 提升排名）", "=" * 60]
    keeps = [r for r in records if r.get("decision") == "keep"]

    if len(keeps) < 2:
        lines.append("  (keep 次数不足，无法排名)")
        return "\n".join(lines)

    deltas = []
    for i in range(1, len(keeps)):
        prev = keeps[i - 1].get("score", 0) or 0
        curr = keeps[i].get("score", 0) or 0
        delta = curr - prev
        deltas.append((delta, keeps[i]))

    deltas.sort(key=lambda x: x[0], reverse=True)
    lines.append(f"{'Rank':>4}  {'Delta':>8}  {'Score':>8}  Mutation")
    lines.append("-" * 60)
    for rank, (delta, r) in enumerate(deltas, 1):
        sc = r.get("score", 0) or 0
        mutation = r.get("mutation", "")[:40]
        lines.append(f"{rank:4d}  {delta:+.4f}  {sc:.4f}  {mutation}")

    return "\n".join(lines)


def section_failure_analysis(records: list[dict]) -> str:
    lines = ["", "=" * 60, "  失败模式分析", "=" * 60]

    rollbacks = [r for r in records if r.get("decision") == "rollback"]
    crashes = [r for r in records if r.get("decision") == "crash"]

    lines.append(f"Rollback 共 {len(rollbacks)} 次")
    lines.append(f"Crash 共 {len(crashes)} 次")
    lines.append("")

    fail_mutations = [r.get("mutation", "") for r in rollbacks + crashes if r.get("mutation")]
    if fail_mutations:
        word_count = {}
        for m in fail_mutations:
            for word in m.replace("，", " ").replace(",", " ").split():
                if len(word) >= 2:
                    word_count[word] = word_count.get(word, 0) + 1
        top_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:8]
        lines.append("失败改动高频词（可能是反复尝试的方向）:")
        for word, cnt in top_words:
            if cnt >= 2:
                lines.append(f"  '{word}': {cnt} 次")

    recent_fails = [r for r in records if r.get("decision") in ("rollback", "crash")][-5:]
    if recent_fails:
        lines.append("")
        lines.append("最近 5 次失败:")
        for r in recent_fails:
            mutation = r.get("mutation", "")[:45]
            lines.append(f"  [{r.get('iter', '?')}] {r.get('decision')} | {mutation}")

    return "\n".join(lines)


def section_metric_trends(records: list[dict]) -> str:
    lines = ["", "=" * 60, "  指标趋势（所有迭代，含 rollback）", "=" * 60]

    valid = [r for r in records if r.get("decision") in ("keep", "rollback")]
    if not valid:
        lines.append("  (无数据)")
        return "\n".join(lines)

    scores = [r.get("score") or 0 for r in valid]
    calmars = [r.get("_calmar") or 0 for r in valid]

    lines.append(f"Score 趋势  (n={len(scores)})")
    lines.append(ascii_sparkline(scores, width=50, height=5))
    lines.append("")
    lines.append(f"Calmar 趋势")
    lines.append(ascii_sparkline(calmars, width=50, height=5))

    return "\n".join(lines)


def section_next_suggestions(records: list[dict], state: dict) -> str:
    lines = ["", "=" * 60, "  下一步建议（供 agent 参考）", "=" * 60]

    keeps = [r for r in records if r.get("decision") == "keep"]
    rollbacks = [r for r in records if r.get("decision") == "rollback"]
    consec_fail = state.get("consecutive_failures", 0)

    if consec_fail >= 3:
        lines.append(f"⚠ 连续失败 {consec_fail} 次，建议换方向，不要重复已失败的改动")

    if keeps:
        champion = keeps[-1]
        dd = abs(champion.get("max_drawdown", 0) or 0)
        calmar = champion.get("_calmar", 0) or 0

        lines.append(f"当前 champion 指标:")
        lines.append(f"  calmar={calmar:.2f}  dd={dd:.2%}")
        lines.append("")

        weak = []
        if dd > 0.20:
            weak.append(f"回撤偏高({dd:.2%})，可尝试加筛选条件或调整持仓数量")
        if calmar < 3.0:
            weak.append(f"calmar 偏低({calmar:.2f})，可尝试优化筛选或排序规则")

        if weak:
            lines.append("薄弱点（优先改进方向）:")
            for w in weak:
                lines.append(f"  • {w}")
        else:
            lines.append("各指标表现良好，可尝试更激进的优化或探索新方向")

    tried = set()
    for r in rollbacks[-10:]:
        m = r.get("mutation", "")
        for word in m.replace("，", " ").replace(",", " ").split():
            if len(word) >= 3:
                tried.add(word)
    if tried:
        lines.append("")
        lines.append(f"近期已尝试方向（避免重复）: {', '.join(list(tried)[:10])}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="分析 wizard 实验结果")
    parser.add_argument("--base", required=True, help="实验目录路径")
    args = parser.parse_args()

    base = Path(args.base)
    if not base.is_absolute():
        script_dir = Path(__file__).parent
        base = script_dir / base
        if not base.exists():
            base = Path(args.base).resolve()

    if not base.exists():
        print(f"[analyze] 目录不存在: {base}")
        return

    records = load_iterations(base)
    state = load_state(base)

    if not records:
        print(f"[analyze] iterations.tsv 无记录: {base}")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"# Wizard Autoresearch 分析报告\n生成时间: {now}\n实验目录: {base.name}\n"

    report = "\n".join(
        [
            header,
            section_overview(records, state),
            section_keep_sequence(records),
            section_top_improvements(records),
            section_failure_analysis(records),
            section_metric_trends(records),
            section_next_suggestions(records, state),
            "",
        ]
    )

    print(report)

    out_path = base / "analysis_report.txt"
    out_path.write_text(report, encoding="utf-8")
    print(f"\n[analyze] 报告已写入: {out_path}")


if __name__ == "__main__":
    main()
