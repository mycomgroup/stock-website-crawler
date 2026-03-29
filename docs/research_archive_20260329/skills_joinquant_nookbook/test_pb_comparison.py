#!/usr/bin/env python3
"""
RFScore7 PB10/PB15/PB25 统一口径对比验证
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 80)
print("RFScore7 PB10/PB15/PB25 统一口径对比验证")
print("运行时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 80)

HOLD_N = 20


def get_monthly_rebal_dates(start, end):
    days = get_trade_days(start, end)
    result, last_m = [], None
    for d in days:
        if d.month != last_m:
            result.append(d)
            last_m = d.month
    return result


def calc_rfscore7(stocks, date):
    q = query(
        valuation.code,
        indicator.roe,
        indicator.roa,
        indicator.gross_profit_margin,
        indicator.net_profit_margin,
        indicator.inc_net_profit_year_on_year,
        indicator.inc_revenue_year_on_year,
        valuation.pb_ratio,
        valuation.pe_ratio,
        valuation.market_cap,
    ).filter(valuation.code.in_(stocks))
    df = (
        get_fundamentals(q, date=date)
        .set_index("code")
        .dropna(subset=["roe", "roa", "pb_ratio"])
    )
    score = pd.Series(0, index=df.index)
    score += (df["roe"] > 0).astype(int)
    score += (df["roa"] > 0).astype(int)
    score += (df["gross_profit_margin"] > df["gross_profit_margin"].median()).astype(
        int
    )
    score += (df["net_profit_margin"] > 0).astype(int)
    score += (df["inc_net_profit_year_on_year"] > 0).astype(int)
    score += (df["inc_revenue_year_on_year"] > 0).astype(int)
    score += (df["pe_ratio"] > 0).astype(int)
    df["rfscore7"] = score
    return df


def filter_stocks_basic(stocks, date):
    try:
        is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()
    except:
        pass
    return stocks


def run_backtest(pb_pct, label, dates, universe):
    monthly_rets = []
    monthly_details = []

    for i, date in enumerate(dates[:-1]):
        date_str = date.strftime("%Y-%m-%d")
        next_date = dates[i + 1]
        next_date_str = next_date.strftime("%Y-%m-%d")

        stocks = list(universe)
        stocks = filter_stocks_basic(stocks, date_str)

        if len(stocks) < 10:
            continue

        df = calc_rfscore7(stocks, date_str)
        if df.empty:
            continue

        df["pb_group"] = (
            pd.qcut(
                df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
            )
            + 1
        )

        pb_group_threshold = int(pb_pct / 10)
        primary = df[(df["rfscore7"] == 7) & (df["pb_group"] <= pb_group_threshold)]
        primary = primary.sort_values(["rfscore7", "pb_ratio"], ascending=[False, True])
        picks = primary.index.tolist()[:HOLD_N]

        if len(picks) < HOLD_N:
            secondary = df[
                (df["rfscore7"] >= 6) & (df["pb_group"] <= pb_group_threshold + 1)
            ]
            secondary = secondary.sort_values(
                ["rfscore7", "pb_ratio"], ascending=[False, True]
            )
            for c in secondary.index.tolist():
                if c not in picks:
                    picks.append(c)
                if len(picks) >= HOLD_N:
                    break

        picks = picks[:HOLD_N]
        if len(picks) < 5:
            continue

        try:
            start_price = get_price(
                picks, end_date=date_str, count=1, fields=["close"], panel=False
            )
            start_price = start_price.pivot(
                index="time", columns="code", values="close"
            ).iloc[-1]

            end_price = get_price(
                picks, end_date=next_date_str, count=1, fields=["close"], panel=False
            )
            end_price = end_price.pivot(
                index="time", columns="code", values="close"
            ).iloc[-1]

            ret = (end_price / start_price - 1).dropna()
            monthly_rets.append(ret.mean())
            monthly_details.append(
                {
                    "date": date_str,
                    "return": ret.mean(),
                    "count": len(picks),
                    "avg_pb": df.loc[picks, "pb_ratio"].mean()
                    if len(picks) > 0
                    else np.nan,
                    "avg_rfscore": df.loc[picks, "rfscore7"].mean()
                    if len(picks) > 0
                    else np.nan,
                }
            )
        except Exception as e:
            continue

    if not monthly_rets:
        return None

    rets = np.array(monthly_rets)
    cum_ret = (1 + rets).prod() - 1
    n_years = len(rets) / 12
    annual_ret = (1 + cum_ret) ** (1 / n_years) - 1 if n_years > 0 else 0

    running_max = np.maximum.accumulate(1 + rets)
    drawdown = (1 + rets) / running_max - 1
    max_dd = drawdown.min()

    sharpe = annual_ret / rets.std() * np.sqrt(12) if rets.std() > 0 else 0
    win_rate = (rets > 0).mean()

    return {
        "label": label,
        "pb_pct": pb_pct,
        "annual_ret": annual_ret,
        "cum_ret": cum_ret,
        "max_dd": max_dd,
        "sharpe": sharpe,
        "win_rate": win_rate,
        "months": len(rets),
        "monthly_details": monthly_details,
    }


print("\n【获取股票池】")
hs300 = set(get_index_stocks("000300.XSHG"))
zz500 = set(get_index_stocks("000905.XSHG"))
universe = hs300 | zz500
print(f"股票池: 中证800 ({len(universe)}只)")


print("\n【全区间测试 2023-2025】")
dates = get_monthly_rebal_dates("2023-01-01", "2025-12-31")
print(f"调仓次数: {len(dates)}")

results = []
for pb_pct, label in [(10, "PB10%"), (15, "PB15%"), (25, "PB25%")]:
    result = run_backtest(pb_pct, label, dates, universe)
    if result:
        results.append(result)
        print(
            f"  {label}: 年化={result['annual_ret'] * 100:.2f}% 回撤={result['max_dd'] * 100:.2f}% 夏普={result['sharpe']:.3f} 胜率={result['win_rate'] * 100:.0f}%"
        )


print("\n【近期区间测试 2024-2025Q1】")
dates2 = get_monthly_rebal_dates("2024-01-01", "2025-03-26")
print(f"调仓次数: {len(dates2)}")

results2 = []
for pb_pct, label in [(10, "PB10%"), (15, "PB15%"), (25, "PB25%")]:
    result = run_backtest(pb_pct, label, dates2, universe)
    if result:
        results2.append(result)
        print(
            f"  {label}: 年化={result['annual_ret'] * 100:.2f}% 回撤={result['max_dd'] * 100:.2f}% 夏普={result['sharpe']:.3f} 胜率={result['win_rate'] * 100:.0f}%"
        )


print("\n【熊市区间测试 2022】")
dates3 = get_monthly_rebal_dates("2022-01-01", "2022-12-31")
print(f"调仓次数: {len(dates3)}")

results3 = []
for pb_pct, label in [(10, "PB10%"), (15, "PB15%"), (25, "PB25%")]:
    result = run_backtest(pb_pct, label, dates3, universe)
    if result:
        results3.append(result)
        print(
            f"  {label}: 年化={result['annual_ret'] * 100:.2f}% 回撤={result['max_dd'] * 100:.2f}% 夏普={result['sharpe']:.3f} 胜率={result['win_rate'] * 100:.0f}%"
        )


print("\n【统一口径对比表】")
print("=" * 80)
print(
    f"{'版本':<12} {'年化收益':>10} {'累计收益':>10} {'最大回撤':>10} {'夏普比率':>8} {'月胜率':>8}"
)
print("-" * 80)
for r in results:
    print(
        f"{r['label']:<12} {r['annual_ret'] * 100:>9.2f}% {r['cum_ret'] * 100:>9.2f}% {r['max_dd'] * 100:>9.2f}% {r['sharpe']:>8.3f} {r['win_rate'] * 100:>7.0f}%"
    )
print("=" * 80)


print("\n【当前市场候选股快照】")
watch_date = "2026-03-27"

stocks = list(universe)
stocks = filter_stocks_basic(stocks, watch_date)

df = calc_rfscore7(stocks, watch_date)
df["pb_group"] = (
    pd.qcut(df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop")
    + 1
)

primary_pb10 = df[(df["rfscore7"] == 7) & (df["pb_group"] <= 1)]
primary_pb10 = primary_pb10.sort_values(
    ["rfscore7", "pb_ratio"], ascending=[False, True]
)

primary_pb15 = df[(df["rfscore7"] == 7) & (df["pb_group"] <= 2)]
primary_pb15 = primary_pb15.sort_values(
    ["rfscore7", "pb_ratio"], ascending=[False, True]
)

primary_pb25 = df[(df["rfscore7"] == 7) & (df["pb_group"] <= 3)]
primary_pb25 = primary_pb25.sort_values(
    ["rfscore7", "pb_ratio"], ascending=[False, True]
)

print(f"\nPB10% 候选股({len(primary_pb10)}只):")
print(
    primary_pb10[["rfscore7", "pb_ratio", "roe", "gross_profit_margin"]]
    .head(10)
    .to_string()
)

print(f"\nPB15% 候选股({len(primary_pb15)}只):")
print(
    primary_pb15[["rfscore7", "pb_ratio", "roe", "gross_profit_margin"]]
    .head(10)
    .to_string()
)

print(f"\nPB25% 候选股({len(primary_pb25)}只):")
print(
    primary_pb25[["rfscore7", "pb_ratio", "roe", "gross_profit_margin"]]
    .head(10)
    .to_string()
)


print("\n验证完成!")
