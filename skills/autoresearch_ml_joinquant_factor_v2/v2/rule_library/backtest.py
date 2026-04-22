"""
回测与评分。

输入数据格式: DataFrame 含至少:
    date (datetime), stock_id, pchg (当期已实现收益), 以及策略引用的因子列。

约定:
  - 一行 = (date, stock_id) 的组合；pchg 就是该周收益。
  - 等权持仓、无交易成本（要加成本在 cost_bps 参数里）。
  - 年化频率默认 52（周频）；按需改 periods_per_year。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from .engine import apply_strategy
from .schema import Strategy


# ---------- 指标 ----------

def _safe_div(a, b):
    return a / b if b not in (0, 0.0) else 0.0


def _sortino(returns: pd.Series, mar: float = 0.0, ppy: int = 52) -> float:
    ex = returns - mar
    downside = ex[ex < 0]
    if len(downside) == 0:
        return 0.0
    dd = downside.std(ddof=1)
    if dd == 0 or np.isnan(dd):
        return 0.0
    return float(ex.mean() / dd * np.sqrt(ppy))


def _max_drawdown(cum: pd.Series) -> float:
    rolling_max = cum.cummax()
    dd = (cum - rolling_max) / rolling_max
    return float(dd.min()) if len(dd) else 0.0


def _calmar(ann_return: float, mdd: float) -> float:
    return float(ann_return / max(abs(mdd), 0.01))


def _information_ratio(port: pd.Series, bench: pd.Series, ppy: int = 52) -> float:
    active = port - bench
    if len(active) < 2 or active.std(ddof=1) == 0:
        return 0.0
    return float(active.mean() / active.std(ddof=1) * np.sqrt(ppy))


# ---------- 评分（复用汇总表里的公式，系数可调） ----------

@dataclass
class ScoreWeights:
    sortino: float = 0.40
    calmar: float = 0.25
    ir: float = 0.15
    win_rate: float = 0.10
    complexity: float = 0.10
    position: float = 1.0
    overfit: float = 1.0


def _complexity_penalty(strategy: Strategy) -> float:
    n_cond = strategy.n_filters() + (1 if strategy.sort_by else 0)
    n_params = sum(len(r.params) for r in strategy.hard_filters + strategy.soft_filters)
    return min((n_cond + n_params) / 10.0, 1.0)


def _position_penalty(n: int) -> float:
    if n < 5:
        return (5 - n) ** 2 * 0.1
    if n > 15:
        # 小票池放宽：40 以内不惩罚，超出 40 才轻度惩罚
        if n <= 40:
            return 0.0
        return (n - 40) ** 2 * 0.01
    return 0.0


def _overfit_penalty(n: int, win_rate: float) -> float:
    """持股少时，胜率不足惩罚。沿用表里的阈值但对小票收紧 5pp。"""
    thresholds = {1: 0.65, 2: 0.60, 3: 0.55, 4: 0.50}
    if n >= 5:
        return 0.0
    req = thresholds.get(n, 0.65)
    return max(0.0, (req - win_rate) * 2.0)


def score(metrics: Dict[str, float],
          strategy: Strategy,
          weights: ScoreWeights = ScoreWeights()) -> float:
    return float(
        metrics["sortino"] * weights.sortino
        + metrics["calmar"] * weights.calmar
        + metrics["ir"] * weights.ir
        + metrics["win_rate"] * weights.win_rate
        - _complexity_penalty(strategy) * weights.complexity
        - _position_penalty(strategy.n_stocks) * weights.position
        - _overfit_penalty(strategy.n_stocks, metrics["win_rate"]) * weights.overfit
    )


# ---------- 回测主循环 ----------

@dataclass
class BacktestResult:
    strategy: Strategy
    metrics: Dict[str, float] = field(default_factory=dict)
    weekly_returns: Optional[pd.Series] = None
    bench_returns: Optional[pd.Series] = None
    n_weeks: int = 0
    avg_holdings: float = 0.0
    fill_rate: float = 0.0           # avg_holdings / n_stocks
    weeks_in_market_ratio: float = 0.0   # 非空仓周 / 总周数
    hard_rollback: bool = False
    failure_reason: str = ""

    @property
    def composite_score(self) -> float:
        if self.hard_rollback:
            return -999.0
        base = score(self.metrics, self.strategy)
        # 仓位稀疏惩罚：过滤太严导致大部分时间空仓，
        # 空仓周按 0 返回计入后会虚高 sortino/calmar/mdd，
        # 必须在评分里扣回去。
        if self.fill_rate < 0.5:
            base -= (0.5 - self.fill_rate) * 4.0
        if self.weeks_in_market_ratio < 0.6:
            base -= (0.6 - self.weeks_in_market_ratio) * 4.0
        return base


def _empty_metrics() -> Dict[str, float]:
    return {
        "n_weeks": 0, "ann_return": 0.0, "ann_vol": 0.0, "sharpe": 0.0,
        "sortino": 0.0, "max_drawdown": 0.0, "calmar": 0.0, "ir": 0.0,
        "win_rate": 0.0, "bench_ann_return": 0.0, "excess_ann": 0.0,
    }


def run_backtest(panel: pd.DataFrame,
                 strategy: Strategy,
                 periods_per_year: int = 52,
                 cost_bps_per_turn: float = 0.0,
                 min_weeks: int = 20,
                 hard_dd_limit: float = 0.35) -> BacktestResult:
    """
    panel : 面板数据（date, stock_id, pchg, ...）
    """
    res = BacktestResult(strategy=strategy)

    if "date" not in panel.columns or "pchg" not in panel.columns:
        res.failure_reason = "panel missing 'date' or 'pchg'"
        res.metrics = _empty_metrics()
        return res

    all_dates = sorted(panel["date"].unique())
    if len(all_dates) < min_weeks:
        res.failure_reason = f"only {len(all_dates)} weeks < min_weeks={min_weeks}"
        res.metrics = _empty_metrics()
        return res

    rebalance_weeks = max(1, strategy.rebalance_weeks)
    port_returns: List[float] = []
    bench_returns: List[float] = []
    holdings: List[int] = []
    prev_stocks: Optional[set] = None

    for i, d in enumerate(all_dates):
        # 控制调仓周期：非调仓周沿用上周选股
        cross = panel[panel["date"] == d]
        if i % rebalance_weeks == 0 or prev_stocks is None:
            selected = apply_strategy(cross, strategy)
            if len(selected) == 0:
                port_returns.append(0.0)
                bench_returns.append(float(cross["pchg"].mean(skipna=True) or 0.0))
                holdings.append(0)
                continue
            stocks = set(selected["stock_id"].tolist())
            turnover = 1.0 if prev_stocks is None else \
                len(stocks.symmetric_difference(prev_stocks)) / max(len(stocks), 1) / 2
            prev_stocks = stocks
        else:
            stocks = prev_stocks
            turnover = 0.0

        rows = cross[cross["stock_id"].isin(stocks)]
        if len(rows) == 0:
            port_returns.append(0.0)
        else:
            r = float(rows["pchg"].mean(skipna=True) or 0.0)
            r -= turnover * cost_bps_per_turn / 1e4
            port_returns.append(r)

        bench_returns.append(float(cross["pchg"].mean(skipna=True) or 0.0))
        holdings.append(len(rows))

    port = pd.Series(port_returns, index=pd.to_datetime(all_dates))
    bench = pd.Series(bench_returns, index=pd.to_datetime(all_dates))
    port = port.fillna(0.0)
    bench = bench.fillna(0.0)

    cum = (1 + port).cumprod()
    bench_cum = (1 + bench).cumprod()

    n = len(port)
    ann_return = float(cum.iloc[-1] ** (periods_per_year / n) - 1) if n > 0 else 0.0
    bench_ann = float(bench_cum.iloc[-1] ** (periods_per_year / n) - 1) if n > 0 else 0.0
    ann_vol = float(port.std(ddof=1) * np.sqrt(periods_per_year)) if n > 1 else 0.0
    sharpe = _safe_div(ann_return, ann_vol)
    sortino = _sortino(port, ppy=periods_per_year)
    mdd = _max_drawdown(cum)
    calmar = _calmar(ann_return, mdd)
    ir = _information_ratio(port, bench, ppy=periods_per_year)
    win_rate = float((port > 0).mean()) if n > 0 else 0.0

    res.weekly_returns = port
    res.bench_returns = bench
    res.n_weeks = n
    res.avg_holdings = float(np.mean(holdings)) if holdings else 0.0
    res.fill_rate = (res.avg_holdings / strategy.n_stocks) if strategy.n_stocks else 0.0
    res.weeks_in_market_ratio = (
        float(np.mean([h > 0 for h in holdings])) if holdings else 0.0
    )
    res.metrics = {
        "n_weeks": n,
        "ann_return": ann_return,
        "ann_vol": ann_vol,
        "sharpe": sharpe,
        "sortino": sortino,
        "max_drawdown": mdd,
        "calmar": calmar,
        "ir": ir,
        "win_rate": win_rate,
        "bench_ann_return": bench_ann,
        "excess_ann": ann_return - bench_ann,
    }

    # 汇总表里的硬约束：最大回撤超限直接 rollback
    if abs(mdd) > hard_dd_limit:
        res.hard_rollback = True
        res.failure_reason = f"max_dd {mdd:.2%} > {hard_dd_limit:.2%}"

    return res
