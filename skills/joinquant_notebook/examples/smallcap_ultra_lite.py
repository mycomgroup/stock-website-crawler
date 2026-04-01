"""
小市值市值区间分层基线研究 - 超轻量版本
使用季度调仓，快速验证
"""

from jqdata import *
import pandas as pd
import numpy as np

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

print(f"\n回测时间: {START_DATE} 至 {END_DATE}")
print(f"市值分组: {len(GROUPS)} 组")

trade_days = get_trade_days(START_DATE, END_DATE)
print(f"交易日数: {len(trade_days)}")

quarterly_dates = []
for i, day in enumerate(trade_days):
    date_obj = pd.to_datetime(day)
    if i == 0:
        quarterly_dates.append(day)
    else:
        prev_date_obj = pd.to_datetime(trade_days[i - 1])
        if date_obj.month != prev_date_obj.month and date_obj.month in [1, 4, 7, 10]:
            quarterly_dates.append(day)

quarterly_dates.append(END_DATE)
print(f"季度调仓次数: {len(quarterly_dates)}")


def filter_stocks(date, cap_min, cap_max):
    all_stocks = get_all_securities(types=["stock"], date=date).index.tolist()

    current_data = get_current_data()
    valid_stocks = []
    for stock in all_stocks[:500]:
        name = current_data[stock].name
        if (
            "ST" not in name
            and "*" not in name
            and "退" not in name
            and not stock.startswith("688")
        ):
            valid_stocks.append(stock)

    q = (
        query(valuation.code, valuation.circulating_market_cap, valuation.pb_ratio)
        .filter(
            valuation.code.in_(valid_stocks),
            valuation.circulating_market_cap >= cap_min,
            valuation.circulating_market_cap < cap_max,
            valuation.pb_ratio > 0,
        )
        .order_by(valuation.circulating_market_cap.asc())
        .limit(10)
    )

    df = get_fundamentals(q, date=date)
    if df is None or len(df) == 0:
        return []

    return df["code"].tolist()


results = {}

for cap_min, cap_max, group_name in GROUPS:
    print(f"\n处理 {group_name}...")

    quarterly_returns = []
    yearly_returns_dict = {}

    for i in range(len(quarterly_dates) - 1):
        select_date = quarterly_dates[i]
        next_date = quarterly_dates[i + 1]

        stocks = filter_stocks(select_date, cap_min, cap_max)

        if len(stocks) == 0:
            quarterly_returns.append(0)
            continue

        try:
            prices = get_price(
                stocks,
                start_date=select_date,
                end_date=next_date,
                frequency="daily",
                fields=["close"],
                panel=False,
            )

            if prices is None or len(prices) == 0:
                quarterly_returns.append(0)
                continue

            stock_returns = []
            for stock in stocks:
                stock_prices = prices[prices["code"] == stock]["close"]
                if len(stock_prices) >= 2:
                    ret = stock_prices.iloc[-1] / stock_prices.iloc[0] - 1
                    stock_returns.append(ret)

            if len(stock_returns) == 0:
                quarterly_returns.append(0)
                continue

            avg_return = np.mean(stock_returns)
            quarterly_returns.append(avg_return)

            year = str(pd.to_datetime(select_date).year)
            if year not in yearly_returns_dict:
                yearly_returns_dict[year] = []
            yearly_returns_dict[year].append(avg_return)

        except Exception as e:
            quarterly_returns.append(0)
            continue

        if (i + 1) % 8 == 0:
            print(f"  已处理 {i + 1}/{len(quarterly_dates) - 1} 季度")

    if len(quarterly_returns) == 0:
        continue

    total_return = (1 + pd.Series(quarterly_returns)).prod() - 1
    years = len(quarterly_returns) / 4
    annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0

    cum_returns = (1 + pd.Series(quarterly_returns)).cumprod()
    cummax = cum_returns.cummax()
    drawdown = (cum_returns - cummax) / cummax
    max_drawdown = drawdown.min()

    sharpe = 0
    if len(quarterly_returns) > 1 and pd.Series(quarterly_returns).std() > 0:
        sharpe = (
            pd.Series(quarterly_returns).mean()
            / pd.Series(quarterly_returns).std()
            * np.sqrt(4)
        )

    yearly_annual_returns = {}
    for year, returns in yearly_returns_dict.items():
        if len(returns) > 0:
            yearly_return = (1 + pd.Series(returns)).prod() - 1
            yearly_annual_returns[year] = yearly_return

    results[group_name] = {
        "total_return": float(total_return),
        "annual_return": float(annual_return),
        "max_drawdown": float(max_drawdown),
        "sharpe_ratio": float(sharpe),
        "quarterly_count": len(quarterly_returns),
        "yearly_returns": yearly_annual_returns,
    }

    print(f"  总收益: {total_return:.2%}")
    print(f"  年化收益: {annual_return:.2%}")
    print(f"  最大回撤: {max_drawdown:.2%}")
    print(f"  夏普: {sharpe:.2f}")

print("\n" + "=" * 80)
print("五组对比汇总")
print("=" * 80)

print("\n| 市值区间 | 总收益率 | 年化收益率 | 最大回撤 | 夏普比率 |")
print("|---------|---------|-----------|---------|---------|")
for group_name in ["A_5-15亿", "B_15-30亿", "C_30-60亿", "D_60-100亿", "E_100-200亿"]:
    if group_name in results:
        r = results[group_name]
        print(
            f"| {group_name.split('_')[1]} | {r['total_return']:.2%} | {r['annual_return']:.2%} | {r['max_drawdown']:.2%} | {r['sharpe_ratio']:.2f} |"
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
    print("------|", end="")
print()

for group_name in ["A_5-15亿", "B_15-30亿", "C_30-60亿", "D_60-100亿", "E_100-200亿"]:
    if group_name in results:
        print(f"| {group_name.split('_')[1]} |", end="")
        for year in years_list:
            if year in results[group_name]["yearly_returns"]:
                print(f" {results[group_name]['yearly_returns'][year]:.2%} |", end="")
            else:
                print(" - |", end="")
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

    print("\n建议:")
    if (
        results[best_sharpe]["annual_return"] > 0.15
        and results[best_sharpe]["max_drawdown"] < -0.25
    ):
        print(f"✓ 推荐市值区间: {best_sharpe.split('_')[1]}")
        print(f"  - 年化收益 {results[best_sharpe]['annual_return']:.2%} > 15%")
        print(f"  - 最大回撤 {results[best_sharpe]['max_drawdown']:.2%} < 25%")
    else:
        print("⚠ 需进一步优化")
        if results[best_sharpe]["annual_return"] < 0.15:
            print(f"  - 年化收益不足 ({results[best_sharpe]['annual_return']:.2%})")
        if results[best_sharpe]["max_drawdown"] > -0.25:
            print(f"  - 回撤过大 ({results[best_sharpe]['max_drawdown']:.2%})")

import json

output_path = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook/output/smallcap_stratification_lite.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n结果已保存: {output_path}")
print("\n回测完成！")
