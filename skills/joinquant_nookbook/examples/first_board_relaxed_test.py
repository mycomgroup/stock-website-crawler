from jqdata import *
import pandas as pd
import numpy as np

"""
首板低开信号放宽版测试
目标：增加信号数量，同时保持收益质量

放宽条件：
版本1（原始）：市值50-150亿，位置≤30%
版本2（放宽）：市值30-200亿，位置≤50%
版本3（中度）：市值40-180亿，位置≤40%

测试期间：2024年Q4（10-12月）
"""


def classify_open_type(open_pct):
    if 0.5 <= open_pct <= 1.5:
        return "假弱高开"
    elif -3.0 <= open_pct < -1.0:
        return "真低开A"
    elif -1.0 <= open_pct < 0.0:
        return "真低开B"
    else:
        return "其他"


def get_relative_position(prices):
    if len(prices) < 2:
        return 1.0
    high_n = prices.max()
    low_n = prices.min()
    current = prices.iloc[-1]
    if high_n == low_n:
        return 0.5
    return (current - low_n) / (high_n - low_n)


def run_test(version_name, market_cap_range, position_threshold):
    """运行单个版本的测试"""
    print(f"\n{'=' * 80}")
    print(
        f"{version_name}: 市值{market_cap_range[0]}-{market_cap_range[1]}亿, 位置≤{position_threshold * 100:.0f}%"
    )
    print("=" * 80)

    test_dates = ["2024-10-08", "2024-11-04", "2024-12-02"]

    signals = []

    for curr_date_str in test_dates:
        trade_days = get_trade_days(end_date=curr_date_str, count=2)
        prev_date = str(trade_days[0])

        all_stocks = get_all_securities("stock", curr_date_str).index.tolist()

        price_prev = get_price(
            all_stocks,
            end_date=prev_date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )

        if price_prev.empty:
            continue

        limit_stocks = price_prev[
            abs(price_prev["close"] - price_prev["high_limit"])
            / price_prev["high_limit"]
            < 0.01
        ]["code"].tolist()

        if len(limit_stocks) == 0:
            continue

        print(f"\n{curr_date_str}: 涨停板{len(limit_stocks)}只")

        price_curr = get_price(
            limit_stocks,
            end_date=curr_date_str,
            count=1,
            fields=["open", "close", "high"],
            panel=False,
        )

        for stock in limit_stocks:
            try:
                prev_row = price_prev[price_prev["code"] == stock]
                curr_row = price_curr[price_curr["code"] == stock]

                if prev_row.empty or curr_row.empty:
                    continue

                prev_close = float(prev_row["close"].iloc[0])
                curr_open = float(curr_row["open"].iloc[0])
                curr_close = float(curr_row["close"].iloc[0])
                curr_high = float(curr_row["high"].iloc[0])

                open_pct = (curr_open - prev_close) / prev_close * 100

                if not (-10 <= open_pct <= 10):
                    continue

                q = query(valuation.code, valuation.circulating_market_cap).filter(
                    valuation.code == stock
                )
                df_val = get_fundamentals(q, date=curr_date_str)

                if df_val.empty:
                    continue

                market_cap = float(df_val["circulating_market_cap"].iloc[0])

                if not (market_cap_range[0] <= market_cap <= market_cap_range[1]):
                    continue

                prices_15d = get_price(
                    stock, end_date=prev_date, count=15, fields=["close"], panel=False
                )

                if prices_15d.empty or len(prices_15d) < 10:
                    continue

                rel_position = get_relative_position(prices_15d["close"])

                if rel_position > position_threshold:
                    continue

                lb_data = get_price(
                    stock,
                    end_date=prev_date,
                    count=2,
                    fields=["close", "high_limit"],
                    panel=False,
                )

                if len(lb_data) >= 2:
                    prev_prev_close = float(lb_data["close"].iloc[0])
                    prev_prev_limit = float(lb_data["high_limit"].iloc[0])

                    if abs(prev_prev_close - prev_prev_limit) / prev_prev_limit < 0.01:
                        continue

                intra_return = (curr_close - curr_open) / curr_open * 100
                max_return = (curr_high - curr_open) / curr_open * 100

                signals.append(
                    {
                        "date": curr_date_str,
                        "stock": stock,
                        "open_pct": open_pct,
                        "intra_return": intra_return,
                        "max_return": max_return,
                        "open_type": classify_open_type(open_pct),
                        "is_win": intra_return > 0,
                        "market_cap": market_cap,
                        "rel_position": rel_position,
                    }
                )

            except Exception as e:
                continue

    if len(signals) == 0:
        print("未找到信号")
        return None

    df = pd.DataFrame(signals)
    print(f"\n总信号数: {len(df)}")

    type_stats = []

    for open_type in ["假弱高开", "真低开A", "真低开B"]:
        subset = df[df["open_type"] == open_type]

        if len(subset) > 0:
            stats = {
                "open_type": open_type,
                "count": len(subset),
                "avg_intra_return": subset["intra_return"].mean(),
                "avg_max_return": subset["max_return"].mean(),
                "win_rate": subset["is_win"].sum() / len(subset) * 100,
            }
            type_stats.append(stats)

            print(f"\n{open_type}: {stats['count']}个")
            print(f"  日内收益: {stats['avg_intra_return']:.2f}%")
            print(f"  最高收益: {stats['avg_max_return']:.2f}%")
            print(f"  胜率: {stats['win_rate']:.1f}%")

    return {
        "version": version_name,
        "total_signals": len(df),
        "market_cap_range": market_cap_range,
        "position_threshold": position_threshold,
        "type_stats": type_stats,
    }


print("=" * 80)
print("首板低开信号放宽版对比测试")
print("=" * 80)

results = []

# 版本1：原始版（严格）
result1 = run_test("版本1（原始严格）", (50, 150), 0.30)
if result1:
    results.append(result1)

# 版本2：放宽版
result2 = run_test("版本2（放宽）", (30, 200), 0.50)
if result2:
    results.append(result2)

# 版本3：中度版
result3 = run_test("版本3（中度）", (40, 180), 0.40)
if result3:
    results.append(result3)

print("\n" + "=" * 80)
print("对比总结")
print("=" * 80)

for r in results:
    print(f"\n{r['version']}:")
    print(f"  总信号数: {r['total_signals']}")
    print(f"  市值范围: {r['market_cap_range'][0]}-{r['market_cap_range'][1]}亿")
    print(f"  位置阈值: ≤{r['position_threshold'] * 100:.0f}%")

    for ts in r["type_stats"]:
        print(
            f"  {ts['open_type']}: {ts['count']}个, 收益{ts['avg_intra_return']:.2f}%, 胜率{ts['win_rate']:.1f}%"
        )

print("\n测试完成！")
