"""
rule_search.py — YAML 驱动的规则库回测/搜索入口。

三种模式:
  1. candidates   — 跑 candidates.yaml 里列出的策略
  2. grid         — 跑 search_space.yaml 展开的网格
  3. single       — 跑一个单独的 strategy YAML 文件

使用示例:

  python v2/rule_search.py candidates \\
      --data skills/autoresearch_ml_joinquant_factor_v2/data/weekly_factors \\
      --aliases v2/rule_library/configs/column_aliases.yaml \\
      --base v2/rule_library/configs/small_cap_base.yaml \\
      --strategies v2/rule_library/configs/candidates.yaml \\
      --out output/rule_search/candidates.csv

  python v2/rule_search.py grid \\
      --data skills/autoresearch_ml_joinquant_factor_v2/data/weekly_factors \\
      --aliases v2/rule_library/configs/column_aliases.yaml \\
      --base v2/rule_library/configs/small_cap_base.yaml \\
      --search v2/rule_library/configs/search_space.yaml \\
      --out output/rule_search/grid.csv \\
      --topk 50

数据格式:
  --data 指向一个目录，里面是 factors_YYYYMMDD_all.csv；
  或者一个单独的 parquet 文件 (面板 DataFrame)；
  或者一个 csv/txt 清单（每行一个路径）。
"""

from __future__ import annotations

import argparse
import glob
import logging
import sys
import time
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd

# 允许直接 `python v2/rule_search.py` 从项目根执行
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from v2.rule_library import (  # noqa: E402
    Strategy,
    load_aliases,
    load_base_filters,
    load_search_space,
    expand_search_space,
    run_backtest,
)
from v2.rule_library.backtest import BacktestResult, ScoreWeights, score  # noqa: E402
from v2.rule_library.loader import load_candidates  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("rule_search")


# ---------- 数据加载 ----------

def _load_weekly_dir(data_dir: Path,
                     date_start: Optional[str] = None,
                     date_end: Optional[str] = None) -> pd.DataFrame:
    files = sorted(glob.glob(str(data_dir / "factors_*_all.csv")))
    if not files:
        raise FileNotFoundError(f"No factors_*.csv in {data_dir}")
    dfs = []
    for fp in files:
        stem = Path(fp).stem  # factors_YYYYMMDD_all
        parts = stem.split("_")
        if len(parts) < 2:
            continue
        date_str = parts[1]
        try:
            date = pd.to_datetime(date_str, format="%Y%m%d")
        except Exception:
            continue
        if date_start and date < pd.to_datetime(date_start):
            continue
        if date_end and date > pd.to_datetime(date_end):
            continue
        df = pd.read_csv(fp)
        if "Unnamed: 0" in df.columns:
            df = df.rename(columns={"Unnamed: 0": "stock_id"})
        df["date"] = date
        dfs.append(df)
    if not dfs:
        raise ValueError("No files matched the date window")
    panel = pd.concat(dfs, ignore_index=True)
    # 过滤掉已知的全 -1 异常周
    bad = []
    for d, g in panel.groupby("date"):
        valid = g["pchg"].dropna()
        if len(valid) == 0 or (valid == -1.0).sum() > len(valid) * 0.5:
            bad.append(d)
        elif np.isinf(valid).any():
            bad.append(d)
    if bad:
        logger.warning("Dropping %d anomaly weeks: %s",
                       len(bad), [str(d.date()) for d in bad[:6]])
        panel = panel[~panel["date"].isin(bad)]
    logger.info("Loaded panel: %d rows, %d weeks, %d stocks",
                len(panel), panel["date"].nunique(), panel["stock_id"].nunique())
    return panel


def load_panel(data_arg: str,
               date_start: Optional[str] = None,
               date_end: Optional[str] = None) -> pd.DataFrame:
    p = Path(data_arg)
    if p.is_dir():
        return _load_weekly_dir(p, date_start, date_end)
    if p.suffix == ".parquet":
        df = pd.read_parquet(p)
        if date_start:
            df = df[df["date"] >= pd.to_datetime(date_start)]
        if date_end:
            df = df[df["date"] <= pd.to_datetime(date_end)]
        return df
    raise ValueError(f"Unsupported data path: {data_arg}")


# ---------- 结果扁平化 ----------

def _flatten_result(r: BacktestResult, rank: int = 0) -> dict:
    s = r.strategy
    row = {
        "rank": rank,
        "name": s.name,
        "label": s.meta.get("label", ""),
        "n_stocks": s.n_stocks,
        "stage1_top_pct": s.stage1_top_pct or 0.0,
        "n_hard": len(s.hard_filters),
        "n_soft": len(s.soft_filters),
        "sort_col": s.sort_by.column if s.sort_by else "",
        "sort_asc": bool(s.sort_by.params.get("ascending", False)) if s.sort_by else False,
        "avg_holdings": round(r.avg_holdings, 2),
        "fill_rate": round(r.fill_rate, 3),
        "weeks_in_market": round(r.weeks_in_market_ratio, 3),
        "hard_rollback": r.hard_rollback,
        "failure_reason": r.failure_reason,
        "composite_score": round(r.composite_score, 4),
    }
    row.update({k: (round(v, 4) if isinstance(v, float) else v)
                for k, v in r.metrics.items()})
    # 策略签名，方便复现
    row["signature"] = s.signature()
    return row


def _sort_and_save(results: List[BacktestResult], out_path: Path,
                   topk: Optional[int] = None) -> pd.DataFrame:
    # 按 composite_score 降序
    results_sorted = sorted(results, key=lambda r: r.composite_score, reverse=True)
    rows = [_flatten_result(r, rank=i + 1)
            for i, r in enumerate(results_sorted)]
    df = pd.DataFrame(rows)
    if topk and topk < len(df):
        df = df.head(topk)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    logger.info("Saved %d rows → %s", len(df), out_path)
    return df


# ---------- 三种模式 ----------

def cmd_candidates(args):
    aliases = load_aliases(args.aliases) if args.aliases else {}
    base = load_base_filters(args.base, aliases) if args.base else []
    strategies = load_candidates(args.strategies, aliases, base)
    panel = load_panel(args.data, args.date_start, args.date_end)

    logger.info("Running %d candidate strategies", len(strategies))
    results: List[BacktestResult] = []
    for i, s in enumerate(strategies, 1):
        t0 = time.time()
        r = run_backtest(
            panel, s,
            periods_per_year=args.ppy,
            cost_bps_per_turn=args.cost_bps,
            min_weeks=args.min_weeks,
            hard_dd_limit=args.hard_dd_limit,
        )
        logger.info("[%d/%d] %-40s  score=%.3f  sortino=%.2f  ir=%.2f  "
                    "ann=%.2f%%  mdd=%.2f%%  nw=%d  (%.1fs)",
                    i, len(strategies), s.name,
                    r.composite_score,
                    r.metrics.get("sortino", 0),
                    r.metrics.get("ir", 0),
                    r.metrics.get("ann_return", 0) * 100,
                    r.metrics.get("max_drawdown", 0) * 100,
                    r.n_weeks, time.time() - t0)
        results.append(r)

    _sort_and_save(results, Path(args.out), args.topk)


def cmd_grid(args):
    aliases = load_aliases(args.aliases) if args.aliases else {}
    base = load_base_filters(args.base, aliases) if args.base else []
    sp = load_search_space(args.search, aliases, base)
    strategies = expand_search_space(sp)
    panel = load_panel(args.data, args.date_start, args.date_end)

    logger.info("Expanded %d strategies (seed=%d, cap=%d)",
                len(strategies), sp.random_seed, sp.max_combinations)
    results: List[BacktestResult] = []
    t_start = time.time()
    for i, s in enumerate(strategies, 1):
        r = run_backtest(
            panel, s,
            periods_per_year=args.ppy,
            cost_bps_per_turn=args.cost_bps,
            min_weeks=args.min_weeks,
            hard_dd_limit=args.hard_dd_limit,
        )
        results.append(r)
        if i % args.log_every == 0 or i == len(strategies):
            eta = (time.time() - t_start) / i * (len(strategies) - i)
            logger.info("Grid %d/%d   best_score_so_far=%.3f   ETA %.1fs",
                        i, len(strategies),
                        max((x.composite_score for x in results), default=0),
                        eta)

    _sort_and_save(results, Path(args.out), args.topk)


def cmd_single(args):
    aliases = load_aliases(args.aliases) if args.aliases else {}
    base = load_base_filters(args.base, aliases) if args.base else []
    from v2.rule_library.loader import load_strategy
    s = load_strategy(args.strategy, aliases, base)
    panel = load_panel(args.data, args.date_start, args.date_end)
    r = run_backtest(
        panel, s,
        periods_per_year=args.ppy,
        cost_bps_per_turn=args.cost_bps,
        min_weeks=args.min_weeks,
        hard_dd_limit=args.hard_dd_limit,
    )
    logger.info("=== %s ===", s.name)
    logger.info("signature: %s", s.signature())
    for k, v in r.metrics.items():
        if isinstance(v, float):
            logger.info("  %-18s %.4f", k, v)
        else:
            logger.info("  %-18s %s", k, v)
    logger.info("  composite_score    %.4f", r.composite_score)
    if r.failure_reason:
        logger.warning("  failure_reason: %s", r.failure_reason)
    if args.out:
        _sort_and_save([r], Path(args.out))


# ---------- arg parsing ----------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def _common(sp):
        sp.add_argument("--data", required=True,
                        help="周频因子数据目录或 parquet 文件")
        sp.add_argument("--aliases",
                        default=str(_HERE / "rule_library/configs/column_aliases.yaml"))
        sp.add_argument("--base",
                        default=str(_HERE / "rule_library/configs/small_cap_base.yaml"))
        sp.add_argument("--date-start", default=None)
        sp.add_argument("--date-end", default=None)
        sp.add_argument("--ppy", type=int, default=52,
                        help="每年周期数（周频=52，月频=12）")
        sp.add_argument("--cost-bps", type=float, default=0.0,
                        help="每次全换仓成本（bps）")
        sp.add_argument("--min-weeks", type=int, default=20)
        sp.add_argument("--hard-dd-limit", type=float, default=0.35)
        sp.add_argument("--topk", type=int, default=None)

    sp_c = sub.add_parser("candidates", help="跑 candidates.yaml")
    _common(sp_c)
    sp_c.add_argument("--strategies",
                      default=str(_HERE / "rule_library/configs/candidates.yaml"))
    sp_c.add_argument("--out", default="output/rule_search/candidates.csv")
    sp_c.set_defaults(func=cmd_candidates)

    sp_g = sub.add_parser("grid", help="跑 search_space.yaml 展开的网格")
    _common(sp_g)
    sp_g.add_argument("--search",
                      default=str(_HERE / "rule_library/configs/search_space.yaml"))
    sp_g.add_argument("--out", default="output/rule_search/grid.csv")
    sp_g.add_argument("--log-every", type=int, default=25)
    sp_g.set_defaults(func=cmd_grid)

    sp_s = sub.add_parser("single", help="跑单个策略 YAML")
    _common(sp_s)
    sp_s.add_argument("--strategy", required=True,
                      help="单独的 strategy YAML 文件")
    sp_s.add_argument("--out", default=None)
    sp_s.set_defaults(func=cmd_single)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
