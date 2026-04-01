"""
首板低开策略极简验证 - 最新期关键指标

只统计最近3个月（2026-01至2026-03）的信号数量和特征
"""

from jqdata import *
import pandas as pd
from datetime import datetime

print("=" * 60)
print("首板低开策略极简验证")
print("=" * 60)

months_to_test = [
    ("2026-01", "2026-01-01", "2026-01-31"),
    ("2026-02", "2026-02-01", "2026-02-29"),
    ("2026-03", "2026-03-01", "2026-03-31"),
]

print("\n验证最近3个月数据")

monthly_stats = []

for month_name, start, end in months_to_test:
    print(f"\n{'=' * 40}")
    print(f"验证月份: {month_name}")
    print(f"{'=' * 40}")

    trading_dates = get_trade_days(start, end)
    print(f"交易日数: {len(trading_dates)}")

    zt_count_total = 0
    first_board_count_total = 0
    valid_signal_count = 0

    sample_signals = []

    for i, date in enumerate(trading_dates):
        prev_dates = get_trade_days(end_date=date, count=2)
        if len(prev_dates) < 2:
            continue

        prev_date = prev_dates[0]

        all_stocks = get_all_securities(types=["stock"], date=date)
        stocks_list = [
            s
            for s in all_stocks.index.tolist()
            if not (
                s.startswith("688")
                or s.startswith("300")
                or s.startswith("4")
                or s.startswith("8")
            )
        ]

        df_zt = get_price(
            stocks_list,
            end_date=prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )

        df_zt = df_zt.dropna()
        zt_df = df_zt[df_zt["close"] == df_zt["high_limit"]]
        zt_count = len(zt_df)
        zt_count_total += zt_count

        if zt_count == 0:
            continue

        zt_stocks = zt_df["code"].tolist()

        prev_prev_date = prev_dates[0]

        df_prev_zt = get_price(
            zt_stocks,
            end_date=prev_prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )

        df_prev_zt = df_prev_zt.dropna()
        prev_zt_df = df_prev_zt[df_prev_zt["close"] == df_prev_zt["high_limit"]]
        prev_zt_stocks = prev_zt_df["code"].tolist()

        first_board = [s for s in zt_stocks if s not in prev_zt_stocks]
        first_board_count_total += len(first_board)

        if len(first_board) == 0:
            continue

        for stock in first_board[:5]:
            df_curr = get_price(
                stock,
                end_date=date,
                frequency="daily",
                fields=["open", "close"],
                count=2,
                panel=False,
            )

            if len(df_curr) < 2:
                continue

            prev_close = df_curr.iloc[0]["close"]
            curr_open = df_curr.iloc[1]["open"]
            open_pct = (curr_open - prev_close) / prev_close * 100

            if not (-2.0 <= open_pct <= 1.5):
                continue

            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.code == stock
            )
            df_cap = get_fundamentals(q, date)

            if df_cap.empty:
                continue

            market_cap = float(df_cap["circulating_market_cap"].iloc[0])

            if not (5 <= market_cap <= 15):
                continue

            valid_signal_count += 1

            if len(sample_signals) < 10:
                sample_signals.append(
                    {
                        "date": date,
                        "stock": stock,
                        "open_pct": open_pct,
                        "market_cap": market_cap,
                    }
                )

    print(f"\n统计结果:")
    print(f"  涨停总数: {zt_count_total}")
    print(f"  首板总数: {first_board_count_total}")
    print(f"  有效信号数（低开+市值5-15亿）: {valid_signal_count}")
    print(f"  日均涨停: {zt_count_total / len(trading_dates):.1f}")
    print(f"  日均首板: {first_board_count_total / len(trading_dates):.1f}")
    print(f"  日均有效信号: {valid_signal_count / len(trading_dates):.2f}")

    if sample_signals:
        print(f"\n样本信号（最多10个）:")
        for sig in sample_signals:
            print(
                f"  {sig['date']} {sig['stock']}: 开盘{sig['open_pct']:.2f}%, 市值{sig['market_cap']:.1f}亿"
            )

    monthly_stats.append(
        {
            "month": month_name,
            "trading_days": len(trading_dates),
            "zt_count": zt_count_total,
            "first_board_count": first_board_count_total,
            "valid_signal_count": valid_signal_count,
            "avg_daily_zt": zt_count_total / len(trading_dates),
            "avg_daily_fb": first_board_count_total / len(trading_dates),
            "avg_daily_signal": valid_signal_count / len(trading_dates),
        }
    )

print(f"\n{'=' * 60}")
print("汇总统计")
print(f"{'=' * 60}")

if monthly_stats:
    df_stats = pd.DataFrame(monthly_stats)

    print(f"\n月度对比:")
    print(
        f"{'月份':<12} {'交易日':<10} {'涨停总数':<12} {'首板总数':<12} {'有效信号':<12} {'日均信号':<10}"
    )
    print("-" * 70)
    for row in monthly_stats:
        print(
            f"{row['month']:<12} {row['trading_days']:<10} {row['zt_count']:<12} {row['first_board_count']:<12} {row['valid_signal_count']:<12} {row['avg_daily_signal']:<10.2f}"
        )

    total_signals = sum([s["valid_signal_count"] for s in monthly_stats])
    total_days = sum([s["trading_days"] for s in monthly_stats])

    print(f"\n总计:")
    print(f"  总交易日: {total_days}")
    print(f"  总有效信号: {total_signals}")
    print(f"  平均日均信号: {total_signals / total_days:.2f}")

    print(f"\n趋势分析:")
    if len(monthly_stats) >= 2:
        first_month = monthly_stats[0]["avg_daily_signal"]
        last_month = monthly_stats[-1]["avg_daily_signal"]

        if first_month > 0:
            change = (last_month - first_month) / first_month * 100
            print(
                f"  日均信号变化: {change:.1f}% ({first_month:.2f} -> {last_month:.2f})"
            )

        if last_month < first_month * 0.5:
            print("  ⚠️ 信号数量显著减少，可能策略衰减")
        elif last_month < first_month * 0.7:
            print("  ⚠️ 信号数量有所减少，需关注")
        else:
            print("  ✓ 信号数量稳定")

print("\n" + "=" * 60)
print("极简验证完成")
print("=" * 60)

print("\n建议:")
print("1. 日均信号数如低于历史期（约0.5-1个/日），可能策略衰减")
print("2. 需进一步验证收益表现，本测试仅统计信号数量")
print("3. 如需完整验证，建议使用策略回测而非Notebook")
