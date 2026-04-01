"""
小市值市值区间分层基线研究 - 简化版本
直接计算各组收益率
"""

from jqdata import *
import pandas as pd
import numpy as np

print("开始小市值市值区间分层基线研究...")

start_date = "2018-01-01"
end_date = "2025-03-30"

market_cap_groups = [
    (5, 15, "A组_5-15亿"),
    (15, 30, "B组_15-30亿"),
    (30, 60, "C组_30-60亿"),
    (60, 100, "D组_60-100亿"),
    (100, 200, "E组_100-200亿"),
]


def get_base_stocks(date):
    stocks = get_all_securities(types=["stock"], date=date).index.tolist()

    current_data = get_current_data()
    st_stocks = []
    for stock in stocks:
        if (
            "ST" in current_data[stock].name
            or "*" in current_data[stock].name
            or "退" in current_data[stock].name
        ):
            st_stocks.append(stock)
    stocks = [s for s in stocks if s not in st_stocks]

    kcb_stocks = []
    for stock in stocks:
        if stock.startswith("688"):
            kcb_stocks.append(stock)
    stocks = [s for s in stocks if s not in kcb_stocks]

    q = query(valuation.code, valuation.pb_ratio).filter(
        valuation.code.in_(stocks), valuation.pb_ratio > 0
    )
    df = get_fundamentals(q, date=date)
    if df is not None and len(df) > 0:
        stocks = df["code"].tolist()

    return stocks


def get_stocks_by_cap(stocks, date, cap_min, cap_max):
    q = (
        query(valuation.code, valuation.circulating_market_cap)
        .filter(
            valuation.code.in_(stocks),
            valuation.circulating_market_cap >= cap_min,
            valuation.circulating_market_cap < cap_max,
        )
        .order_by(valuation.circulating_market_cap.asc())
        .limit(10)
    )

    df = get_fundamentals(q, date=date)
    if df is None or len(df) == 0:
        return [], []

    return df["code"].tolist(), df["circulating_market_cap"].tolist()


def get_monthly_returns(stocks, start_date, end_date):
    if len(stocks) == 0:
        return 0

    try:
        prices = get_price(
            stocks,
            start_date=start_date,
            end_date=end_date,
            frequency="m",
            fields=["close"],
            panel=False,
        )
        if prices is None or len(prices) == 0:
            return 0

        month_returns = []
        for stock in stocks:
            stock_prices = prices[prices["code"] == stock]["close"]
            if len(stock_prices) >= 2:
                month_return = stock_prices.iloc[-1] / stock_prices.iloc[0] - 1
                month_returns.append(month_return)

        if len(month_returns) == 0:
            return 0

        return np.mean(month_returns)
    except:
        return 0


trade_days = get_trade_days(start_date, end_date)
print(f"总交易日数: {len(trade_days)}")

monthly_dates = []
for i in range(len(trade_days)):
    date_obj = pd.to_datetime(trade_days[i])
    if i == 0 or date_obj.month != pd.to_datetime(trade_days[i - 1]).month:
        monthly_dates.append(trade_days[i])

print(f"月度调仓次数: {len(monthly_dates)}")

results = {}

for cap_min, cap_max, group_name in market_cap_groups:
    print(f"\n处理 {group_name}...")

    monthly_returns_list = []
    yearly_returns = {}
    stock_counts = []
    avg_caps = []

    for i in range(len(monthly_dates) - 1):
        select_date = monthly_dates[i]
        next_date = monthly_dates[i + 1]

        base_stocks = get_base_stocks(select_date)

        target_stocks, caps = get_stocks_by_cap(
            base_stocks, select_date, cap_min, cap_max
        )

        stock_counts.append(len(target_stocks))
        if len(caps) > 0:
            avg_caps.append(np.mean(caps))

        month_return = get_monthly_returns(target_stocks, select_date, next_date)
        monthly_returns_list.append(month_return)

        year = str(pd.to_datetime(select_date).year)
        if year not in yearly_returns:
            yearly_returns[year] = []
        yearly_returns[year].append(month_return)

        if (i + 1) % 20 == 0:
            print(f"  已处理 {i + 1}/{len(monthly_dates) - 1} 月")

    total_return = (1 + pd.Series(monthly_returns_list)).prod() - 1
    years = len(monthly_returns_list) / 12
    annual_return = (1 + total_return) ** (1 / years) - 1

    cum_returns = (1 + pd.Series(monthly_returns_list)).cumprod()
    cummax = cum_returns.cummax()
    drawdown = (cum_returns - cummax) / cummax
    max_drawdown = drawdown.min()

    sharpe = (
        pd.Series(monthly_returns_list).mean()
        / pd.Series(monthly_returns_list).std()
        * np.sqrt(12)
    )

    yearly_annual_returns = {}
    for year, returns in yearly_returns.items():
        yearly_return = (1 + pd.Series(returns)).prod() - 1
        yearly_annual_returns[year] = yearly_return

    turnover = pd.Series(monthly_returns_list).count() / len(monthly_dates)

    avg_volume = np.mean(stock_counts) if len(stock_counts) > 0 else 0
    avg_cap = np.mean(avg_caps) if len(avg_caps) > 0 else 0

    results[group_name] = {
        "total_return": total_return,
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe,
        "turnover_rate": turnover,
        "avg_stock_count": avg_volume,
        "avg_market_cap": avg_cap,
        "yearly_returns": yearly_annual_returns,
        "monthly_returns": monthly_returns_list,
    }

    print(f"  总收益率: {total_return:.2%}")
    print(f"  年化收益率: {annual_return:.2%}")
    print(f"  最大回撤: {max_drawdown:.2%}")
    print(f"  夏普比率: {sharpe:.2f}")

print("\n" + "=" * 80)
print("五组市值分层回测结果汇总")
print("=" * 80)

summary_table = []
for group_name in [
    "A组_5-15亿",
    "B组_15-30亿",
    "C组_30-60亿",
    "D组_60-100亿",
    "E组_100-200亿",
]:
    if group_name in results:
        r = results[group_name]
        summary_table.append(
            {
                "市值区间": group_name.split("_")[1],
                "总收益率": f"{r['total_return']:.2%}",
                "年化收益率": f"{r['annual_return']:.2%}",
                "最大回撤": f"{r['max_drawdown']:.2%}",
                "夏普比率": f"{r['sharpe_ratio']:.2f}",
                "平均持股数": f"{r['avg_stock_count']:.0f}",
                "平均市值": f"{r['avg_market_cap']:.1f}亿",
            }
        )

summary_df = pd.DataFrame(summary_table)
print(summary_df.to_string(index=False))

print("\n" + "=" * 80)
print("年度收益率对比")
print("=" * 80)

years_list = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
yearly_table = []

for group_name in [
    "A组_5-15亿",
    "B组_15-30亿",
    "C组_30-60亿",
    "D组_60-100亿",
    "E组_100-200亿",
]:
    if group_name in results:
        row = {"市值区间": group_name.split("_")[1]}
        for year in years_list:
            if year in results[group_name]["yearly_returns"]:
                row[year] = f"{results[group_name]['yearly_returns'][year]:.2%}"
            else:
                row[year] = "-"
        yearly_table.append(row)

yearly_df = pd.DataFrame(yearly_table)
print(yearly_df.to_string(index=False))

import json

output_path = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook/output/smallcap_stratification_results.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=2, default=str)

print(f"\n结果已保存到: {output_path}")

print("\n" + "=" * 80)
print("核心结论")
print("=" * 80)

best_sharpe_group = max(results.keys(), key=lambda x: results[x]["sharpe_ratio"])
best_return_group = max(results.keys(), key=lambda x: results[x]["annual_return"])
min_drawdown_group = min(results.keys(), key=lambda x: results[x]["max_drawdown"])

print(
    f"最优夏普比率: {best_sharpe_group} ({results[best_sharpe_group]['sharpe_ratio']:.2f})"
)
print(
    f"最优年化收益: {best_return_group} ({results[best_return_group]['annual_return']:.2%})"
)
print(
    f"最小最大回撤: {min_drawdown_group} ({results[min_drawdown_group]['max_drawdown']:.2%})"
)

print("\n建议:")
if results[best_sharpe_group]["avg_stock_count"] >= 8:
    print(f"推荐市值区间: {best_sharpe_group}")
else:
    print("流动性受限，建议扩大市值区间")

print("\n回测完成！")
