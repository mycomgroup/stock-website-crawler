# 主线信号放宽测试 - 单日完整筛选（使用确定交易日）
from jqdata import *
import pandas as pd

print("主线信号放宽测试 - 单日完整筛选")

trade_days = get_trade_days("2024-01-01", "2024-12-31")
print(f"全年交易日数: {len(trade_days)}")

test_idx = 60
test_date_obj = trade_days[test_idx]
test_date = test_date_obj.strftime("%Y-%m-%d")
prev_date_obj = trade_days[test_idx - 1]
prev_date = prev_date_obj.strftime("%Y-%m-%d")

print(f"测试日期: {test_date}, 前一日: {prev_date}")

versions = {
    "原版": (50, 150, 0.30),
    "放宽C": (40, 200, 0.50),
    "放宽D": (30, 300, 0.50),
}

results = {}

for vname, (cap_min, cap_max, pos_max) in versions.items():
    print(f"\n版本: {vname} (市值{cap_min}-{cap_max}亿, 位置≤{int(pos_max * 100)}%)")

    q = query(valuation.code, valuation.circulating_market_cap).filter(
        valuation.circulating_market_cap >= cap_min,
        valuation.circulating_market_cap <= cap_max,
    )
    df_val = get_fundamentals(q, date=test_date)

    candidates = df_val["code"].tolist()
    print(f"  市值筛选基数: {len(candidates)}只")

    signals = []

    for stock in candidates:
        try:
            df_prev = get_price(
                stock,
                end_date=prev_date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )
            if df_prev.empty:
                continue

            prev_close = float(df_prev["close"].iloc[0])
            prev_limit = float(df_prev["high_limit"].iloc[0])

            if abs(prev_close - prev_limit) / prev_limit > 0.01:
                continue

            df_curr = get_price(
                stock,
                end_date=test_date,
                count=1,
                fields=["open", "close", "high"],
                panel=False,
            )
            if df_curr.empty:
                continue

            curr_open = float(df_curr["open"].iloc[0])
            curr_close = float(df_curr["close"].iloc[0])
            curr_high = float(df_curr["high"].iloc[0])

            open_pct = (curr_open - prev_close) / prev_close * 100

            df_pos = get_price(
                stock, end_date=test_date, count=15, fields=["close"], panel=False
            )
            if len(df_pos) < 5:
                continue

            high_15d = float(df_pos["close"].max())
            low_15d = float(df_pos["close"].min())
            if high_15d == low_15d:
                continue

            position = (df_pos["close"].iloc[-1] - low_15d) / (high_15d - low_15d)
            if position > pos_max:
                continue

            df_lb = get_price(
                stock,
                end_date=prev_date,
                count=2,
                fields=["close", "high_limit"],
                panel=False,
            )
            if len(df_lb) >= 2:
                prev_prev_close = float(df_lb["close"].iloc[-2])
                prev_prev_limit = float(df_lb["high_limit"].iloc[-2])
                if abs(prev_prev_close - prev_prev_limit) / prev_prev_limit < 0.01:
                    continue

            intra_return = (curr_close - curr_open) / curr_open * 100
            max_return = (curr_high - curr_open) / curr_open * 100
            win = 1 if curr_close > curr_open else 0

            signals.append(
                {
                    "stock": stock,
                    "open_pct": open_pct,
                    "intra_return": intra_return,
                    "max_return": max_return,
                    "win": win,
                }
            )

        except:
            continue

    if len(signals) > 0:
        df_s = pd.DataFrame(signals)

        jwr_signals = df_s[(df_s["open_pct"] >= 0.5) & (df_s["open_pct"] <= 1.5)]

        results[vname] = {
            "total": len(signals),
            "jwr_count": len(jwr_signals),
            "avg_return": df_s["intra_return"].mean(),
            "avg_max": df_s["max_return"].mean(),
            "win_rate": df_s["win"].mean() * 100,
            "jwr_return": jwr_signals["intra_return"].mean()
            if len(jwr_signals) > 0
            else 0,
            "jwr_win": jwr_signals["win"].mean() * 100 if len(jwr_signals) > 0 else 0,
        }

        print(f"  总信号数: {len(signals)}")
        print(f"  假弱高开数: {len(jwr_signals)}")
        print(f"  日内收益均值: {df_s['intra_return'].mean():.2f}%")
        print(f"  胜率: {df_s['win'].mean() * 100:.2f}%")
        if len(jwr_signals) > 0:
            print(f"  假弱高开收益: {jwr_signals['intra_return'].mean():.2f}%")
            print(f"  假弱高开胜率: {jwr_signals['win'].mean() * 100:.2f}%")

print("\n" + "=" * 60)
print("单日对比")
print("=" * 60)

if len(results) > 0:
    print("\n| 版本 | 总信号 | 假弱高开 | 日内收益 | 胜率 | 假弱高开收益 |")
    print("|------|--------|----------|----------|------|-------------|")

    for vname in ["原版", "放宽C", "放宽D"]:
        if vname in results:
            r = results[vname]
            print(
                f"| {vname} | {r['total']} | {r['jwr_count']} | {r['avg_return']:.2f}% | {r['win_rate']:.2f}% | {r['jwr_return']:.2f}% |"
            )

    if "原版" in results and results["原版"]["total"] > 0:
        base = results["原版"]
        print("\n与原版对比:")
        for vname in ["放宽C", "放宽D"]:
            if vname in results:
                r = results[vname]
                print(
                    f"  {vname}: 信号{r['total'] / base['total']:.2f}x, 收益{r['avg_return'] / base['avg_return'] if base['avg_return'] != 0 else 0:.2f}x, 胜率{r['win_rate'] / base['win_rate'] if base['win_rate'] > 0 else 0:.2f}x"
                )

print("=" * 60)
