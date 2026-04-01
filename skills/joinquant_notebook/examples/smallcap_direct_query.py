"""
小市值市值区间分层 - 直接查询版
不运行回测引擎，直接计算各组的历史收益
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 80)
print("小市值市值区间分层基线研究")
print("=" * 80)

START_DATE = "2018-01-01"
END_DATE = "2025-03-30"

GROUPS = [
    (5, 15, "A_5-15亿"),
    (15, 30, "B_15-30亿"),
    (30, 60, "C_30-60亿"),
    (60, 100, "D_60-100亿"),
    (100, 200, "E_100-200亿"),
]

print(f"\n时间范围: {START_DATE} 至 {END_DATE}")

trade_days = get_trade_days(START_DATE, END_DATE)
print(f"交易日数: {len(trade_days)}")

sample_dates = []
for i in range(0, len(trade_days), 90):
    sample_dates.append(trade_days[i])

print(f"采样日期数: {len(sample_dates)}")

results = {}

for cap_min, cap_max, group_name in GROUPS:
    print(f"\n{group_name}...")

    all_returns = []
    yearly_data = {}

    for i, date in enumerate(sample_dates[:-1]):
        next_date = sample_dates[i + 1]

        try:
            all_stocks = get_all_securities("stock", date).index.tolist()

            q = (
                query(valuation.code, valuation.circulating_market_cap)
                .filter(
                    valuation.code.in_(all_stocks),
                    valuation.circulating_market_cap >= cap_min,
                    valuation.circulating_market_cap < cap_max,
                )
                .order_by(valuation.circulating_market_cap.asc())
                .limit(10)
            )

            df_cap = get_fundamentals(q, date=date)

            if df_cap is None or len(df_cap) == 0:
                continue

            stocks = df_cap["code"].tolist()

            prices = get_price(
                stocks,
                start_date=date,
                end_date=next_date,
                frequency="daily",
                fields=["close"],
                panel=False,
            )

            if prices is None or len(prices) == 0:
                continue

            returns = []
            for stock in stocks:
                stock_data = prices[prices["code"] == stock]
                if len(stock_data) >= 2:
                    ret = stock_data["close"].iloc[-1] / stock_data["close"].iloc[0] - 1
                    returns.append(ret)

            if len(returns) > 0:
                avg_ret = np.mean(returns)
                all_returns.append(avg_ret)

                year = str(pd.to_datetime(date).year)
                if year not in yearly_data:
                    yearly_data[year] = []
                yearly_data[year].append(avg_ret)

        except Exception as e:
            continue

        if (i + 1) % 5 == 0:
            print(f"  已处理 {i + 1}/{len(sample_dates) - 1}")

    if len(all_returns) == 0:
        print(f"  无数据")
        continue

    total_return = (1 + pd.Series(all_returns)).prod() - 1
    years = len(all_returns) / 4
    annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0

    cum_returns = (1 + pd.Series(all_returns)).cumprod()
    cummax = cum_returns.cummax()
    drawdown = (cum_returns - cummax) / cummax
    max_drawdown = drawdown.min()

    sharpe = 0
    if len(all_returns) > 1 and pd.Series(all_returns).std() > 0:
        sharpe = (
            pd.Series(all_returns).mean() / pd.Series(all_returns).std() * np.sqrt(4)
        )

    yearly_returns = {}
    for year, rets in yearly_data.items():
        yearly_returns[year] = (1 + pd.Series(rets)).prod() - 1

    results[group_name] = {
        "total_return": float(total_return),
        "annual_return": float(annual_return),
        "max_drawdown": float(max_drawdown),
        "sharpe_ratio": float(sharpe),
        "yearly_returns": yearly_returns,
        "sample_count": len(all_returns),
    }

    print(f"  总收益: {total_return:.2%}")
    print(f"  年化: {annual_return:.2%}")
    print(f"  回撤: {max_drawdown:.2%}")
    print(f"  夏普: {sharpe:.2f}")

print("\n" + "=" * 80)
print("五组对比汇总")
print("=" * 80)

print("\n| 市值区间 | 总收益率 | 年化收益率 | 最大回撤 | 夏普比率 | 样本数 |")
print("|---------|---------|-----------|---------|---------|-------|")
for group_name in ["A_5-15亿", "B_15-30亿", "C_30-60亿", "D_60-100亿", "E_100-200亿"]:
    if group_name in results:
        r = results[group_name]
        print(
            f"| {group_name.split('_')[1]} | {r['total_return']:.2%} | {r['annual_return']:.2%} | {r['max_drawdown']:.2%} | {r['sharpe_ratio']:.2f} | {r['sample_count']} |"
        )

print("\n" + "=" * 80)
print("年度收益率对比")
print("=" * 80)

years_list = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
print("\n| 市值区间 |", end="")
for year in years_list:
    print(f" {year} |", end="")
print()
print("|---------|", end="")
for year in years_list:
    print("-------|", end="")
print()

for group_name in ["A_5-15亿", "B_15-30亿", "C_30-60亿", "D_60-100亿", "E_100-200亿"]:
    if group_name in results:
        print(f"| {group_name.split('_')[1]} |", end="")
        for year in years_list:
            if year in results[group_name]["yearly_returns"]:
                print(f" {results[group_name]['yearly_returns'][year]:.2%} |", end="")
            else:
                print(" ----- |", end="")
        print()

print("\n" + "=" * 80)
print("核心发现")
print("=" * 80)

if len(results) > 0:
    best_sharpe = max(results.keys(), key=lambda x: results[x]["sharpe_ratio"])
    best_return = max(results.keys(), key=lambda x: results[x]["annual_return"])
    min_dd = min(results.keys(), key=lambda x: results[x]["max_drawdown"])

    print(
        f"\n最优夏普: {best_sharpe.split('_')[1]} ({results[best_sharpe]['sharpe_ratio']:.2f})"
    )
    print(
        f"最优收益: {best_return.split('_')[1]} ({results[best_return]['annual_return']:.2%})"
    )
    print(f"最小回撤: {min_dd.split('_')[1]} ({results[min_dd]['max_drawdown']:.2%})")

    print("\n推荐:")
    r = results[best_sharpe]
    if r["sharpe_ratio"] > 0.5:
        print(f"✓ 推荐市值区间: {best_sharpe.split('_')[1]}")
        print(f"  理由: 夏普比率 {r['sharpe_ratio']:.2f} > 0.5")
        print(f"  年化收益: {r['annual_return']:.2%}")
        print(f"  最大回撤: {r['max_drawdown']:.2%}")
    else:
        print("⚠ 所有组夏普偏低")

import json

output_path = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook/output/smallcap_stratification_direct.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n结果已保存: {output_path}")
print("\n回测完成！")
