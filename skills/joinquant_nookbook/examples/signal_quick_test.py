from jqdata import *
import pandas as pd

print("=" * 80)
print("信号放宽版vs原版对比 - 快速版")
print("=" * 80)

all_dates_2024 = list(get_trade_days(end_date="2024-12-31", count=250))
all_dates_2024 = [str(d) if hasattr(d, "strftime") else d for d in all_dates_2024]
start_idx = all_dates_2024.index("2024-01-02") if "2024-01-02" in all_dates_2024 else 0
test_dates = all_dates_2024[start_idx:]

print(f"测试期间：2024全年，{len(test_dates)} 个交易日")

VERSIONS = {
    "原版": (50, 150, 0.30),
    "放宽A": (40, 200, 0.30),
    "放宽B": (50, 150, 0.50),
    "放宽C": (40, 200, 0.50),
    "放宽D": (30, 300, 0.50),
}

results = {}

for version_name, (min_cap, max_cap, max_position) in VERSIONS.items():
    print(
        f"\n{version_name}: 市值{min_cap}-{max_cap}亿, 位置<= {max_position * 100:.0f}%"
    )

    count = 0
    returns = []
    wins = 0

    sample_dates = test_dates[:50]

    for i in range(1, len(sample_dates)):
        prev_date = sample_dates[i - 1]
        curr_date = sample_dates[i]

        try:
            all_stocks = get_all_securities("stock", prev_date).index.tolist()
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

            price_curr = get_price(
                limit_stocks,
                end_date=curr_date,
                count=1,
                fields=["open", "close"],
                panel=False,
            )
            if price_curr.empty:
                continue

            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.code.in_(limit_stocks)
            )
            val_data = get_fundamentals(q, date=curr_date)
            if val_data.empty:
                continue

            for stock in limit_stocks:
                try:
                    prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                    curr_row = price_curr[price_curr["code"] == stock].iloc[0]

                    prev_close = float(prev_row["close"])
                    curr_open = float(curr_row["open"])
                    curr_close = float(curr_row["close"])

                    open_pct = (curr_open - prev_close) / prev_close * 100

                    if -10 <= open_pct <= 10:
                        val_row = val_data[val_data["code"] == stock]
                        if len(val_row) == 0:
                            continue

                        market_cap = float(val_row["circulating_market_cap"].iloc[0])
                        if not (min_cap <= market_cap <= max_cap):
                            continue

                        prices_15d = get_price(
                            stock,
                            end_date=prev_date,
                            count=15,
                            fields=["close"],
                            panel=False,
                        )
                        if len(prices_15d) < 10:
                            continue

                        high_15d = float(prices_15d["close"].max())
                        low_15d = float(prices_15d["close"].min())
                        if high_15d == low_15d:
                            continue

                        position = (prev_close - low_15d) / (high_15d - low_15d)
                        if position > max_position:
                            continue

                        lb_data_2d = get_price(
                            stock,
                            end_date=prev_date,
                            count=2,
                            fields=["close", "high_limit"],
                            panel=False,
                        )
                        if len(lb_data_2d) >= 2:
                            prev_prev_close = float(lb_data_2d["close"].iloc[0])
                            prev_prev_limit = float(lb_data_2d["high_limit"].iloc[0])
                            if (
                                abs(prev_prev_close - prev_prev_limit) / prev_prev_limit
                                < 0.01
                            ):
                                continue

                        intra_return = (curr_close - curr_open) / curr_open * 100
                        count += 1
                        returns.append(intra_return)
                        if intra_return > 0:
                            wins += 1
                except:
                    continue
        except:
            continue

    avg_return = sum(returns) / len(returns) if len(returns) > 0 else 0
    win_rate = wins / count * 100 if count > 0 else 0

    results[version_name] = {
        "count": count,
        "avg_return": avg_return,
        "win_rate": win_rate,
    }

    print(f"  样本期间信号数: {count}")
    print(f"  平均收益: {avg_return:.2f}%")
    print(f"  胜率: {win_rate:.1f}%")

print("\n" + "=" * 80)
print("预估全年数据")
print("=" * 80)

if "原版" in results and results["原版"]["count"] > 0:
    orig_count = results["原版"]["count"]
    orig_return = results["原版"]["avg_return"]
    orig_winrate = results["原版"]["win_rate"]

    print("\n基于样本估算全年:")
    for v, r in results.items():
        est_full_year = int(r["count"] * len(test_dates) / len(sample_dates))
        print(
            f"{v}: 预估全年信号 {est_full_year}, 收益 {r['avg_return']:.2f}%, 胜率 {r['win_rate']:.1f}%"
        )

    print("\n放宽效果对比:")
    for v, r in results.items():
        if v == "原版":
            continue
        est_full = int(r["count"] * len(test_dates) / len(sample_dates))
        est_orig = int(orig_count * len(test_dates) / len(sample_dates))

        signal_ratio = est_full / est_orig if est_orig > 0 else 0
        return_ratio = r["avg_return"] / orig_return if orig_return != 0 else 0
        winrate_ratio = r["win_rate"] / orig_winrate if orig_winrate != 0 else 0

        print(
            f"{v}: 信号提升 {signal_ratio:.2f}x, 收益比 {return_ratio:.2f}, 胜率比 {winrate_ratio:.2f}"
        )

print("\n快速测试完成!")
