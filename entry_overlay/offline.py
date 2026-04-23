from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, List, Optional

import numpy as np
import pandas as pd

from .data_sources import MarketDataAdapter
from .engine import EntryMode, EntryOverlayConfig, EntryOverlayEngine
from .profiles import build_profile_weights


@dataclass
class BacktestConfig:
    freq: str = "1m"
    lookback_bars: int = 240
    holding_bars: int = 240
    # timing_only 场景：一周内挑时点
    weekly_window_days: int = 5


@dataclass
class BacktestReport:
    trade_count: int
    win_rate: float
    avg_return: float
    sharpe_like: float
    max_drawdown_like: float
    summary: pd.DataFrame


def _calc_stats(returns: List[float]) -> Dict[str, float]:
    if not returns:
        return {"trade_count": 0, "win_rate": 0.0, "avg_return": 0.0, "sharpe_like": 0.0, "max_drawdown_like": 0.0}
    arr = np.array(returns)
    eq = np.cumprod(1 + arr)
    peak = np.maximum.accumulate(eq)
    dd = (eq - peak) / peak
    std = float(arr.std())
    sharpe_like = float(arr.mean() / std) if std > 1e-6 else 0.0
    return {
        "trade_count": int(len(arr)),
        "win_rate": float((arr > 0).mean()),
        "avg_return": float(arr.mean()),
        "sharpe_like": sharpe_like,
        "max_drawdown_like": float(dd.min()),
    }


def run_event_backtest(
    adapter: MarketDataAdapter,
    events: pd.DataFrame,
    config: Optional[BacktestConfig] = None,
    overlay_conf: Optional[EntryOverlayConfig] = None,
    weights: Optional[Dict[str, float]] = None,
) -> BacktestReport:
    """离线回测：

    events字段:
    - code: 标的
    - signal_time: 信号时间
    - must_buy: 可选，True表示必须买（适合timing_only）
    """
    config = config or BacktestConfig()
    overlay_conf = overlay_conf or EntryOverlayConfig()
    engine = EntryOverlayEngine(overlay_conf, weights)

    rows, rets = [], []
    for _, ev in events.iterrows():
        code = ev["code"]
        t0 = pd.Timestamp(ev["signal_time"])
        must_buy = bool(ev.get("must_buy", overlay_conf.mode == EntryMode.TIMING_ONLY))

        end = t0 + pd.Timedelta(days=config.weekly_window_days if must_buy else 1)
        bars = adapter.get_bars(code=code, start=t0, end=end, freq=config.freq)
        if bars.empty or len(bars) < max(overlay_conf.bar_count, 30):
            continue

        # 候选时点：过滤开盘前几分钟噪声
        idx = list(bars.index)
        candidate = idx[min(overlay_conf.wait_minutes_open, len(idx) - 1):]
        decision = engine.decide(bars, candidate)

        if (not decision.should_buy) and (not must_buy):
            rows.append({"code": code, "signal_time": t0, "action": "skip", "score": decision.score, "ret": 0.0})
            continue

        entry_t = decision.best_times[0][0] if decision.best_times else bars.index[-1]
        if entry_t not in bars.index:
            entry_t = bars.index[-1]
        entry_idx = bars.index.get_loc(entry_t)
        exit_idx = min(entry_idx + config.holding_bars, len(bars) - 1)

        entry_p = float(bars.iloc[entry_idx]["close"])
        exit_p = float(bars.iloc[exit_idx]["close"])
        r = exit_p / entry_p - 1
        rets.append(r)

        rows.append(
            {
                "code": code,
                "signal_time": t0,
                "action": "buy",
                "score": decision.score,
                "entry_time": entry_t,
                "exit_time": bars.index[exit_idx],
                "ret": r,
            }
        )

    df = pd.DataFrame(rows)
    stats = _calc_stats(rets)
    return BacktestReport(summary=df, **stats)


def grid_search_params(
    adapter: MarketDataAdapter,
    events: pd.DataFrame,
    profile_list: Iterable[str] = ("general", "trend", "reversal"),
    threshold_list: Iterable[float] = (0.55, 0.58, 0.60, 0.62),
    mode: EntryMode = EntryMode.RANK_FILTER,
) -> pd.DataFrame:
    """离线参数搜索：输出每组参数的收益统计。"""
    rows = []
    for profile, th in product(profile_list, threshold_list):
        conf = EntryOverlayConfig(mode=mode, profile=profile, min_score_to_buy=th)
        rep = run_event_backtest(
            adapter=adapter,
            events=events,
            overlay_conf=conf,
            weights=build_profile_weights(profile, normalize=True),
        )
        rows.append(
            {
                "profile": profile,
                "threshold": th,
                "trade_count": rep.trade_count,
                "win_rate": rep.win_rate,
                "avg_return": rep.avg_return,
                "sharpe_like": rep.sharpe_like,
                "max_drawdown_like": rep.max_drawdown_like,
            }
        )
    return pd.DataFrame(rows).sort_values(["sharpe_like", "avg_return"], ascending=False)
