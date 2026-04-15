#!/usr/bin/env python3
"""
analyze.py - 问财公式回测实验结果分析工具

读取实验目录的 iterations.tsv，输出五个维度的分析报告：
  1. 总览（keep/rollback/crash 统计，baseline vs champion 对比）
  2. Keep 序列（改进路径，每次 keep 的 mutation 和 score 提升）
  3. Top 改进（按单次 score 提升排名）
  4. 失败模式（rollback reason 分类，反复失败的方向）
  5. 指标趋势（ASCII 折线图）

报告同时写入 analysis_report.txt，供 agent 读取。

Usage:
    python analyze.py --base <实验目录>
    python analyze.py --base experiments/exp_A_value12
"""

import argparse
import csv
import json
import os
import urllib.parse
from pathlib import Path
from datetime import datetime


def load_iterations(base: Path) -> list[dict]:
    """加载 iterations.tsv 文件，返回迭代记录列表"""
    tsv_path = base / "iterations.tsv"
    if not tsv_path.exists():
        return []

    records = []
    with open(tsv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            try:
                d = {
                    "iter": row.get("iter", ""),
                    "backtest_id": row.get("backtest_id", ""),
                    "status": row.get("status", ""),
                    "annual_return": float(row.get("annual_return", 0) or 0),
                    "max_drawdown": float(row.get("max_drawdown", 0) or 0),
                    "sharpe": float(row.get("sharpe", 0) or 0),
                    "score": float(row.get("score", 0) or 0),
                    "decision": row.get("decision", ""),
                    "mutation": row.get("mutation", ""),
                }
                ar = d.get("annual_return") or 0
                dd = abs(d.get("max_drawdown") or 0)
                d["_calmar"] = ar / max(dd, 0.01)
                d["_sortino"] = 0
                d["_ir"] = 0
                records.append(d)
            except Exception:
                pass
    return records


def load_state(base: Path) -> dict:
    state_file = base / "state.json"
    if state_file.exists():
        return json.load(open(state_file, encoding="utf-8"))
    return {}


def load_formula_config(base: Path) -> dict:
    config_file = base / "formula_config.json"
    if config_file.exists():
        return json.load(open(config_file, encoding="utf-8"))
    return {}


def generate_backtest_url(config: dict) -> str:
    """根据 formula_config.json 生成问财回测分享 URL"""
    field_map = {
        "formula": "query",
        "conditions": "query",
        "startDate": "startDate",
        "start_date": "startDate",
        "endDate": "endDate",
        "end_date": "endDate",
        "daysForSaleStrategy": "daysForSaleStrategy",
        "period": "daysForSaleStrategy",
        "maxPositions": "stockHoldCount",
        "stockHoldCount": "stockHoldCount",
        "dailyBuyCount": "dayBuyStockNum",
        "dayBuyStockNum": "dayBuyStockNum",
        "takeProfit": "upperIncome",
        "upperIncome": "upperIncome",
        "stopLoss": "lowerIncome",
        "lowerIncome": "lowerIncome",
        "trailingStopLoss": "fallIncome",
        "fallIncome": "fallIncome",
        "capital": "capital",
        "initialCapital": "capital",
    }

    params = {}
    for key, value in config.items():
        if key in field_map:
            target_key = field_map[key]
            if target_key == "query" and isinstance(value, list):
                params[target_key] = "，".join(value)
            else:
                params[target_key] = str(value)

    if "query" not in params:
        return ""

    params.setdefault("daysForSaleStrategy", "2,3")
    params.setdefault("startDate", "2024-01-01")
    params.setdefault("endDate", "2026-12-31")
    params.setdefault("stockHoldCount", "1")
    params.setdefault("dayBuyStockNum", "1")
    params.setdefault("upperIncome", "20")
    params.setdefault("lowerIncome", "10")
    params.setdefault("fallIncome", "5")
    params.setdefault("engine", "online")
    params.setdefault("capital", "10000000")

    encoded = urllib.parse.urlencode(params, safe=",")
    return f"https://backtest.10jqka.com.cn/backtest/app.html#/strategybacktest?{encoded}"


def ascii_sparkline(values: list[float], width: int = 50, height: int = 6) -> str:
    """生成 ASCII 折线图，返回多行字符串"""
    if not values:
        return "  (无数据)"
    valid = [v for v in values if v is not None and v != float("-inf")]
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
    lines.append(f"  baseline:{len(baselines)}")
    lines.append(f"  keep:    {len(keeps)}")
    lines.append(f"  rollback:{len(rollbacks)}")
    lines.append(f"  crash:   {len(crashes)}")
    lines.append(f"keep rate: {keep_rate:.1%}  ({len(keeps)}/{decided})")
    lines.append("")

    baseline = baselines[0] if baselines else None
    champion_score = state.get("champion_score", float("-inf"))
    champion = None
    for r in records:
        if r.get("score") == champion_score and r.get("decision") == "keep":
            champion = r
            break
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
        return f"annual={ar:.2%}  dd={dd:.2%}  sharpe={sh:.3f}\n         calmar={calmar:.2f}\n         score={sc:.4f}"

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

    prev_score = baselines[0].get("score", 0) if baselines else None
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
    baselines = [r for r in records if r.get("decision") == "baseline"]

    if len(keeps) < 1:
        lines.append("  (keep 次数不足，无法排名)")
        return "\n".join(lines)

    deltas = []
    prev_score = baselines[0].get("score", 0) if baselines else 0
    for r in keeps:
        curr = r.get("score", 0) or 0
        delta = curr - prev_score
        deltas.append((delta, r))
        prev_score = curr

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
        sc = r.get("score", 0) or 0
        dd = abs(r.get("max_drawdown", 0) or 0)
        status = r.get("status", "").lower()
        if "error" in status or "fail" in status:
            reason_cats["回测失败"] += 1
        elif dd > 0.35:
            reason_cats["回撤超限"] += 1
        else:
            reason_cats["score 不足"] += 1

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
            lines.append(f"  [{r.get('iter', '?')}] {r.get('decision')} | {mutation}")

    return "\n".join(lines)


def section_metric_trends(records: list[dict]) -> str:
    lines = ["", "=" * 60, "  指标趋势（所有迭代，含 rollback）", "=" * 60]

    valid = [r for r in records if r.get("decision") in ("keep", "rollback", "baseline")]
    if not valid:
        lines.append("  (无数据)")
        return "\n".join(lines)

    scores = [r.get("score") or 0 for r in valid]
    calmars = [r.get("_calmar") or 0 for r in valid]
    annuals = [r.get("annual_return") or 0 for r in valid]

    lines.append(f"Score 趋势  (n={len(scores)})")
    lines.append(ascii_sparkline(scores, width=50, height=5))
    lines.append("")
    lines.append(f"Calmar 趋势")
    lines.append(ascii_sparkline(calmars, width=50, height=5))
    lines.append("")
    lines.append(f"Annual Return 趋势")
    lines.append(ascii_sparkline(annuals, width=50, height=5))

    return "\n".join(lines)


def section_backtest_url(config: dict) -> str:
    """生成回测分享 URL 段落"""
    lines = ["", "=" * 60, "  回测分享链接", "=" * 60]

    if not config:
        lines.append("  (未找到 formula_config.json)")
        return "\n".join(lines)

    url = generate_backtest_url(config)
    if url:
        lines.append(f"当前配置的回测链接:")
        lines.append(f"  {url}")
        lines.append("")
        query = config.get("formula", config.get("conditions", ""))
        if isinstance(query, list):
            query = "，".join(query)
        lines.append(f"选股条件: {query}")
        lines.append(
            f"回测区间: {config.get('startDate', config.get('start_date', ''))} ~ {config.get('endDate', config.get('end_date', ''))}"
        )
        lines.append(
            f"持仓: {config.get('maxPositions', config.get('stockHoldCount', ''))}  每日买入: {config.get('dailyBuyCount', config.get('dayBuyStockNum', ''))}"
        )
        lines.append(
            f"止盈: {config.get('takeProfit', config.get('upperIncome', ''))}%  止损: {config.get('stopLoss', config.get('lowerIncome', ''))}%  移动止损: {config.get('trailingStopLoss', config.get('fallIncome', ''))}%"
        )
    else:
        lines.append("  (无法生成 URL，配置中缺少选股条件)")

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
        sc = champion.get("score", 0) or 0

        lines.append(f"当前 champion 指标:")
        lines.append(f"  calmar={calmar:.2f}  score={sc:.4f}  dd={dd:.2%}")
        lines.append("")

        weak = []
        if dd > 0.15:
            weak.append(f"回撤偏高({dd:.2%})，可尝试加止损或降仓位")
        if calmar < 5.0:
            weak.append(f"calmar 偏低({calmar:.2f})，可尝试提升收益或压缩回撤")
        if sc < 10.0:
            weak.append(f"score 偏低({sc:.4f})，可尝试优化筛选条件")

        if weak:
            lines.append("薄弱点（优先改进方向）:")
            for w in weak:
                lines.append(f"  • {w}")
        else:
            lines.append("各指标表现良好，可尝试更激进的优化或探索新方向")

    tried = set()
    for r in rollbacks[-10:]:
        m = r.get("mutation", "")
        for word in m.replace("，", " ").replace(",", " ").replace("[", "").replace("]", "").split():
            if len(word) >= 3:
                tried.add(word)
    if tried:
        lines.append("")
        lines.append(f"近期已尝试方向（避免重复）: {', '.join(list(tried)[:10])}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="分析问财公式回测实验结果")
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
    config = load_formula_config(base)

    if not records:
        print(f"[analyze] iterations.tsv 无记录或不存在: {base}")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"# 问财公式回测分析报告\n生成时间: {now}\n实验目录: {base.name}\n"

    report = "\n".join(
        [
            header,
            section_overview(records, state),
            section_keep_sequence(records),
            section_top_improvements(records),
            section_failure_analysis(records),
            section_metric_trends(records),
            section_backtest_url(config),
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
