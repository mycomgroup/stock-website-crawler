#!/usr/bin/env python3
"""
analyze.py - Wizard 实验结果分析工具

读取实验目录的 history/*.json，输出五个维度的分析报告：
  1. 总览（keep/rollback/crash 统计，baseline vs champion 对比）
  2. Keep 序列（改进路径，每次 keep 的 mutation 和 score 提升）
  3. Top 改进（按单次 score 提升排名）
  4. 失败模式（rollback reason 分类，反复失败的方向）
  5. 指标趋势（ASCII 折线图）

报告同时写入 history/analysis_report.txt，供 agent 读取。

Usage:
    python analyze.py --base experiments/<name>
"""

import argparse
import json
import glob
import os
from pathlib import Path
from datetime import datetime


# ── 数据加载 ──────────────────────────────────────────────────────────────────

def load_history(base: Path) -> list[dict]:
    """加载 history/ 下所有迭代记录，按 iter 编号排序"""
    files = sorted(glob.glob(str(base / "history" / "*.json")))
    records = []
    for f in files:
        try:
            d = json.load(open(f, encoding="utf-8"))
            # 补充 calmar
            ar = d.get("annual_return") or 0
            dd = abs(d.get("max_drawdown") or 0)
            s = d.get("fetch_result", {}).get("summary", {})
            d["_calmar"] = ar / max(dd, 0.01)
            d["_sortino"] = s.get("sortina") or s.get("sortino") or 0
            d["_ir"] = s.get("information_ratio") or 0
            records.append(d)
        except Exception:
            pass
    return records


def load_state(base: Path) -> dict:
    state_file = base / "state.json"
    if state_file.exists():
        return json.load(open(state_file, encoding="utf-8"))
    return {}


# ── ASCII 折线图 ───────────────────────────────────────────────────────────────

def ascii_sparkline(values: list[float], width: int = 50, height: int = 6) -> str:
    """生成 ASCII 折线图，返回多行字符串"""
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


# ── 各 section 生成 ───────────────────────────────────────────────────────────

def section_overview(records: list[dict], state: dict) -> str:
    lines = ["=" * 60, "  总览", "=" * 60]

    total = len(records)
    keeps = [r for r in records if r.get("decision") == "keep"]
    rollbacks = [r for r in records if r.get("decision") == "rollback"]
    crashes = [r for r in records if r.get("decision") == "crash"]
    decided = len(keeps) + len(rollbacks)
    keep_rate = len(keeps) / decided if decided else 0

    lines.append(f"总迭代数:  {total}")
    lines.append(f"  keep:    {len(keeps)}")
    lines.append(f"  rollback:{len(rollbacks)}")
    lines.append(f"  crash:   {len(crashes)}")
    lines.append(f"keep rate: {keep_rate:.1%}  ({len(keeps)}/{decided})")
    lines.append("")

    baseline = next((r for r in records if "baseline" in r.get("iter", "")), None)
    champion_iter = state.get("champion_iter", "")
    champion = next((r for r in records if r.get("iter") == champion_iter), None)
    if not champion and keeps:
        champion = keeps[-1]

    def fmt(r):
        if not r:
            return "N/A"
        ar = r.get("annual_return", 0) or 0
        dd = abs(r.get("max_drawdown", 0) or 0)
        sh = r.get("sharpe", 0) or 0
        sc = r.get("score", 0) or 0
        calmar = r.get("_calmar", 0) or 0
        so = r.get("_sortino", 0) or 0
        ir = r.get("_ir", 0) or 0
        return (f"annual={ar:.2%}  dd={dd:.2%}  sharpe={sh:.3f}\n"
                f"         calmar={calmar:.2f}  sortino={so:.3f}  IR={ir:.3f}\n"
                f"         score={sc:.4f}")

    lines.append(f"Baseline  [{(baseline or {}).get('iter', '?')}]")
    lines.append(f"  {fmt(baseline)}")
    lines.append(f"Champion  [{champion_iter or '?'}]")
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
    if not keeps:
        lines.append("  (暂无 keep 记录)")
        return "\n".join(lines)

    prev_score = None
    for r in keeps:
        sc = r.get("score", 0) or 0
        delta = f"{sc - prev_score:+.4f}" if prev_score is not None else "baseline"
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

    reason_cats = {"score 不足": 0, "回撤超限": 0, "回测失败": 0, "其他": 0}
    for r in rollbacks:
        reason = r.get("reason", "").lower()
        if "score" in reason or "champion" in reason:
            reason_cats["score 不足"] += 1
        elif "drawdown" in reason or "max_drawdown" in reason:
            reason_cats["回撤超限"] += 1
        elif "backtest" in reason or "failed" in reason or "error" in reason:
            reason_cats["回测失败"] += 1
        else:
            reason_cats["其他"] += 1

    lines.append(f"Rollback 共 {len(rollbacks)} 次:")
    for cat, cnt in reason_cats.items():
        if cnt:
            lines.append(f"  {cat}: {cnt}")
    lines.append(f"Crash 共 {len(crashes)} 次")
    lines.append("")

    fail_mutations = [r.get("mutation", "") for r in rollbacks + crashes if r.get("mutation")]
    if fail_mutations:
        word_count: dict[str, int] = {}
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
            reason = r.get("reason", "")[:40]
            lines.append(f"  [{r.get('iter', '?')}] {r.get('decision')} | {mutation}")
            lines.append(f"       reason: {reason}")

    return "\n".join(lines)


def section_metric_trends(records: list[dict]) -> str:
    lines = ["", "=" * 60, "  指标趋势（所有迭代，含 rollback）", "=" * 60]

    valid = [r for r in records if r.get("decision") in ("keep", "rollback")]
    if not valid:
        lines.append("  (无数据)")
        return "\n".join(lines)

    scores = [r.get("score") or 0 for r in valid]
    calmars = [r.get("_calmar") or 0 for r in valid]
    sortinos = [r.get("_sortino") or 0 for r in valid]
    irs = [r.get("_ir") or 0 for r in valid]

    lines.append(f"Score 趋势  (n={len(scores)})")
    lines.append(ascii_sparkline(scores, width=50, height=5))
    lines.append("")
    lines.append(f"Calmar 趋势")
    lines.append(ascii_sparkline(calmars, width=50, height=5))
    lines.append("")
    lines.append(f"Sortino 趋势")
    lines.append(ascii_sparkline(sortinos, width=50, height=5))
    lines.append("")
    lines.append(f"Information Ratio 趋势")
    lines.append(ascii_sparkline(irs, width=50, height=5))

    return "\n".join(lines)


def section_next_suggestions(records: list[dict], state: dict) -> str:
    """基于历史数据给出下一步改进建议（供 agent 参考）"""
    lines = ["", "=" * 60, "  下一步建议（供 agent 参考）", "=" * 60]

    keeps = [r for r in records if r.get("decision") == "keep"]
    rollbacks = [r for r in records if r.get("decision") == "rollback"]
    crashes = [r for r in records if r.get("decision") == "crash"]
    consec_fail = state.get("consecutive_failures", 0)

    if consec_fail >= 3:
        lines.append(f"⚠ 连续失败 {consec_fail} 次，建议换方向，不要重复已失败的改动")

    if keeps:
        champion = keeps[-1]
        dd = abs(champion.get("max_drawdown", 0) or 0)
        calmar = champion.get("_calmar", 0) or 0
        ir = champion.get("_ir", 0) or 0
        so = champion.get("_sortino", 0) or 0

        lines.append(f"当前 champion 指标:")
        lines.append(f"  calmar={calmar:.2f}  sortino={so:.3f}  IR={ir:.3f}  dd={dd:.2%}")
        lines.append("")

        weak = []
        if dd > 0.20:
            weak.append(f"回撤偏高({dd:.2%})，可尝试加筛选条件或调整持仓数量")
        if calmar < 3.0:
            weak.append(f"calmar 偏低({calmar:.2f})，可尝试优化筛选或排序规则")
        if ir < 1.5:
            weak.append(f"IR 偏低({ir:.3f})，可尝试优化因子组合")
        if so < 2.0:
            weak.append(f"sortino 偏低({so:.3f})，可尝试减少下行波动")

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


# ── 主函数 ────────────────────────────────────────────────────────────────────

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

    records = load_history(base)
    state = load_state(base)

    if not records:
        print(f"[analyze] history/ 下无记录: {base}")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"# Wizard Autoresearch 分析报告\n生成时间: {now}\n实验目录: {base.name}\n"

    report = "\n".join([
        header,
        section_overview(records, state),
        section_keep_sequence(records),
        section_top_improvements(records),
        section_failure_analysis(records),
        section_metric_trends(records),
        section_next_suggestions(records, state),
        "",
    ])

    print(report)

    out_path = base / "history" / "analysis_report.txt"
    out_path.write_text(report, encoding="utf-8")
    print(f"\n[analyze] 报告已写入: {out_path}")


if __name__ == "__main__":
    main()
