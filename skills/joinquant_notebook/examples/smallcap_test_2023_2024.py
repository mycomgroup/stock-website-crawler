"""
小市值市值区间分层 - 测试版（2023-2024）
快速验证分层效果
"""

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 80)
print("小市值市值区间分层测试（2023-2024）")
print("=" * 80)

START_DATE = "2023-01-01"
END_DATE = "2024-12-31"

GROUPS = [
    (5, 15, "A_5-15亿"),
    (15, 30, "B_15-30亿"),
    (30, 60, "C_30-60亿"),
    (60, 100, "D_60-100亿"),
    (100, 200, "E_100-200亿"),
]

print(f"\n测试时间: {START_DATE} 至 {END_DATE}")

trade_days = get_trade_days(START_DATE, END_DATE)
print(f"交易日数: {len(trade_days)}")

monthly_dates = []
for i, day in enumerate(trade_days):
    date_obj = pd.to_datetime(day)
    if i == 0 or date_obj.month != pd.to_datetime(trade_days[i - 1]).month:
        monthly_dates.append(day)

monthly_dates.append(END_DATE)
print(f"月度调仓次数: {len(monthly_dates)}")

results = {}

for cap_min, cap_max, group_name in GROUPS:
    print(f"\n{group_name}...")

    monthly_returns = []

    for i in range(len(monthly_dates) - 1):
        select_date = monthly_dates[i]
        next_date = monthly_dates[i + 1]

        try:
            all_stocks = get_all_securities("stock", select_date).index.tolist()[:1000]

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

            df_cap = get_fundamentals(q, date=select_date)

            if df_cap is None or len(df_cap) == 0:
                monthly_returns.append(0)
                continue

            stocks = df_cap["code"].tolist()

            prices = get_price(
                stocks,
                start_date=select_date,
                end_date=next_date,
                frequency="daily",
                fields=["close"],
                panel=False,
            )

            if prices is None or len(prices) == 0:
                monthly_returns.append(0)
                continue

            stock_returns = []
            for stock in stocks:
                try:
                    stock_prices = prices[prices["code"] == stock]["close"]
                    if len(stock_prices) >= 2:
                        ret = stock_prices.iloc[-1] / stock_prices.iloc[0] - 1
                        stock_returns.append(ret)
                except:
                    continue

            if len(stock_returns) == 0:
                monthly_returns.append(0)
                continue

            avg_return = np.mean(stock_returns)
            monthly_returns.append(avg_return)

        except:
            monthly_returns.append(0)
            continue

    if len(monthly_returns) == 0:
        continue

    total_return = (1 + pd.Series(monthly_returns)).prod() - 1
    annual_return = (1 + total_return) ** (1 / 2) - 1

    cum_returns = (1 + pd.Series(monthly_returns)).cumprod()
    cummax = cum_returns.cummax()
    drawdown = (cum_returns - cummax) / cummax
    max_drawdown = drawdown.min()

    sharpe = 0
    if len(monthly_returns) > 1 and pd.Series(monthly_returns).std() > 0:
        sharpe = (
            pd.Series(monthly_returns).mean()
            / pd.Series(monthly_returns).std()
            * np.sqrt(12)
        )

    results[group_name] = {
        "total_return": float(total_return),
        "annual_return": float(annual_return),
        "max_drawdown": float(max_drawdown),
        "sharpe_ratio": float(sharpe),
    }

    print(f"  总收益: {total_return:.2%}")
    print(f"  年化: {annual_return:.2%}")
    print(f"  回撤: {max_drawdown:.2%}")
    print(f"  夏普: {sharpe:.2f}")

print("\n" + "=" * 80)
print("对比汇总")
print("=" * 80)

print("\n| 市值区间 | 总收益率 | 年化收益率 | 最大回撤 | 夏普比率 |")
print("|---------|---------|-----------|---------|---------|")
for group_name in ["A_5-15亿", "B_15-30亿", "C_30-60亿", "D_60-100亿", "E_100-200亿"]:
    if group_name in results:
        r = results[group_name]
        print(
            f"| {group_name.split('_')[1]} | {r['total_return']:.2%} | {r['annual_return']:.2%} | {r['max_drawdown']:.2%} | {r['sharpe_ratio']:.2f} |"
        )

if len(results) > 0:
    best = max(results.keys(), key=lambda x: results[x]["sharpe_ratio"])
    print(f"\n最优: {best.split('_')[1]} (夏普 {results[best]['sharpe_ratio']:.2f})")

print("\n测试完成！")
