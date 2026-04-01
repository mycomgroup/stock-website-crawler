"""
首板低开策略完整OOS验证 - JoinQuant版本

验证范围：
- 历史期：2024-07-01 至 2025-03-31
- 最新期：2025-04-01 至 2026-03-31
"""

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 80)
print("首板低开策略完整OOS验证")
print("=" * 80)

PERIODS = [
    ("历史期", "2024-07-01", "2025-03-31"),
    ("最新期", "2025-04-01", "2026-03-31"),
]

results_all_periods = []

for period_name, start_date, end_date in PERIODS:
    print(f"\n{'=' * 60}")
    print(f"验证时期: {period_name} ({start_date} 至 {end_date})")
    print(f"{'=' * 60}")

    trading_dates = get_trade_days(start_date, end_date)
    print(f"交易日数量: {len(trading_dates)}")

    print("\n第一步：批量获取涨停股票")

    all_zt_data = []
    for i, date in enumerate(trading_dates):
        if i % 10 == 0:
            print(f"  处理进度: {i}/{len(trading_dates)}")

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

        df = get_price(
            stocks_list,
            end_date=prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )

        df = df.dropna()
        zt_df = df[df["close"] == df["high_limit"]]

        for stock in zt_df["code"].values:
            all_zt_data.append(
                {"stock": stock, "zt_date": prev_date, "signal_date": date}
            )

    print(f"涨停总数: {len(all_zt_data)}")

    print("\n第二步：筛选首板（非连板）")

    first_board_data = []
    for i, item in enumerate(all_zt_data):
        if i % 100 == 0:
            print(f"  处理进度: {i}/{len(all_zt_data)}")

        stock = item["stock"]
        zt_date = item["zt_date"]

        prev_prev_dates = get_trade_days(end_date=zt_date, count=2)
        if len(prev_prev_dates) < 2:
            first_board_data.append(item)
            continue

        prev_prev_date = prev_prev_dates[0]

        df_prev = get_price(
            stock,
            end_date=prev_prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )

        if df_prev.empty:
            first_board_data.append(item)
            continue

        prev_close = float(df_prev["close"].iloc[0])
        prev_high_limit = float(df_prev["high_limit"].iloc[0])

        if abs(prev_close - prev_high_limit) / prev_high_limit >= 0.01:
            first_board_data.append(item)

    print(f"首板总数: {len(first_board_data)}")

    print("\n第三步：筛选低开+市值+位置")

    valid_signals = []
    for i, item in enumerate(first_board_data):
        if i % 50 == 0:
            print(f"  处理进度: {i}/{len(first_board_data)}")

        stock = item["stock"]
        signal_date = item["signal_date"]
        zt_date = item["zt_date"]

        df_open = get_price(
            stock,
            end_date=zt_date,
            frequency="daily",
            fields=["close"],
            count=1,
            panel=False,
        )

        if df_open.empty:
            continue

        zt_close = float(df_open["close"].iloc[0])

        df_curr = get_price(
            stock,
            end_date=signal_date,
            frequency="daily",
            fields=["open"],
            count=1,
            panel=False,
        )

        if df_curr.empty:
            continue

        curr_open = float(df_curr["open"].iloc[0])

        open_pct = (curr_open - zt_close) / zt_close * 100

        if not (-2.0 <= open_pct <= 1.5):
            continue

        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code == stock
        )
        df_cap = get_fundamentals(q, signal_date)

        if df_cap.empty:
            continue

        market_cap = float(df_cap["circulating_market_cap"].iloc[0])

        if not (5 <= market_cap <= 15):
            continue

        df_pos = get_price(
            stock,
            end_date=signal_date,
            frequency="daily",
            fields=["close"],
            count=15,
            panel=False,
        )

        if len(df_pos) < 5:
            continue

        high_15d = df_pos["close"].max()
        low_15d = df_pos["close"].min()
        curr_close = df_pos["close"].iloc[-1]

        if high_15d == low_15d:
            continue

        position = (curr_close - low_15d) / (high_15d - low_15d)

        if position > 0.30:
            continue

        valid_signals.append(
            {
                "stock": stock,
                "signal_date": signal_date,
                "open_pct": open_pct,
                "buy_price": curr_open,
                "market_cap": market_cap,
                "position": position,
            }
        )

    print(f"有效信号数: {len(valid_signals)}")

    print("\n第四步：计算收益")

    for i, signal in enumerate(valid_signals):
        if i % 10 == 0:
            print(f"  处理进度: {i}/{len(valid_signals)}")

        signal_date = signal["signal_date"]
        stock = signal["stock"]

        next_dates = get_trade_days(end_date=signal_date, count=2)
        if len(next_dates) < 2:
            signal["return_high"] = None
            signal["return_close"] = None
            continue

        next_date = next_dates[1]

        df_next = get_price(
            stock,
            end_date=next_date,
            frequency="daily",
            fields=["high", "close"],
            count=1,
            panel=False,
        )

        if df_next.empty:
            signal["return_high"] = None
            signal["return_close"] = None
            continue

        buy_price = signal["buy_price"]
        next_high = float(df_next["high"].iloc[0])
        next_close = float(df_next["close"].iloc[0])

        signal["return_high"] = (next_high - buy_price) / buy_price * 100
        signal["return_close"] = (next_close - buy_price) / buy_price * 100

    print(f"\n{'=' * 60}")
    print(f"{period_name} 统计结果")
    print(f"{'=' * 60}")

    if valid_signals:
        df_results = pd.DataFrame(valid_signals)
        df_valid = df_results.dropna(subset=["return_high"])

        if len(df_valid) > 0:
            trading_days = len(trading_dates)

            stats = {
                "period_name": period_name,
                "trading_days": trading_days,
                "total_signals": len(df_valid),
                "avg_daily_signals": len(df_valid) / trading_days,
                "avg_open_pct": df_valid["open_pct"].mean(),
                "avg_market_cap": df_valid["market_cap"].mean(),
                "avg_position": df_valid["position"].mean(),
                "return_high_avg": df_valid["return_high"].mean(),
                "return_high_win_rate": (df_valid["return_high"] > 0).sum()
                / len(df_valid)
                * 100,
                "return_high_profit_factor": abs(
                    df_valid[df_valid["return_high"] > 0]["return_high"].sum()
                    / abs(df_valid[df_valid["return_high"] < 0]["return_high"].sum())
                )
                if df_valid[df_valid["return_high"] < 0]["return_high"].sum() != 0
                else 0,
                "return_close_avg": df_valid["return_close"].mean(),
                "return_close_win_rate": (df_valid["return_close"] > 0).sum()
                / len(df_valid)
                * 100,
            }

            print(f"\n信号特征:")
            print(f"  总信号数: {stats['total_signals']}")
            print(f"  日均信号: {stats['avg_daily_signals']:.2f}")
            print(f"  平均开盘涨跌幅: {stats['avg_open_pct']:.2f}%")
            print(f"  平均市值: {stats['avg_market_cap']:.1f}亿")
            print(f"  平均位置: {stats['avg_position']:.2f}")

            print(f"\n收益统计（次日最高卖出）:")
            print(f"  平均收益: {stats['return_high_avg']:.2f}%")
            print(f"  胜率: {stats['return_high_win_rate']:.1f}%")
            print(f"  盈亏比: {stats['return_high_profit_factor']:.2f}")

            print(f"\n收益统计（次日收盘卖出）:")
            print(f"  平均收益: {stats['return_close_avg']:.2f}%")
            print(f"  胜率: {stats['return_close_win_rate']:.1f}%")

            results_all_periods.append(stats)
        else:
            print("无有效收益数据")
    else:
        print("无有效信号")

print(f"\n{'=' * 80}")
print("对比分析")
print(f"{'=' * 80}")

if len(results_all_periods) >= 2:
    hist = results_all_periods[0]
    curr = results_all_periods[1]

    print("\n历史期 vs 最新期 对比表")
    print("-" * 80)

    print("\n次日最高卖出:")
    print(f"{'指标':<20} {'历史期':<15} {'最新期':<15} {'变化':<15}")
    print("-" * 60)

    metrics_high = [
        ("日均信号", "avg_daily_signals", "{:.2f}"),
        ("平均收益%", "return_high_avg", "{:.2f}"),
        ("胜率%", "return_high_win_rate", "{:.1f}"),
        ("盈亏比", "return_high_profit_factor", "{:.2f}"),
    ]

    for name, key, fmt in metrics_high:
        hist_val = hist[key]
        curr_val = curr[key]
        change = curr_val - hist_val

        print(
            f"{name:<20} {fmt.format(hist_val):<15} {fmt.format(curr_val):<15} {fmt.format(change):<15}"
        )

    print("\n次日收盘卖出:")
    print(f"{'指标':<20} {'历史期':<15} {'最新期':<15} {'变化':<15}")
    print("-" * 60)

    metrics_close = [
        ("日均信号", "avg_daily_signals", "{:.2f}"),
        ("平均收益%", "return_close_avg", "{:.2f}"),
        ("胜率%", "return_close_win_rate", "{:.1f}"),
    ]

    for name, key, fmt in metrics_close:
        hist_val = hist[key]
        curr_val = curr[key]
        change = curr_val - hist_val

        print(
            f"{name:<20} {fmt.format(hist_val):<15} {fmt.format(curr_val):<15} {fmt.format(change):<15}"
        )

    print("\n衰减判定:")

    avg_return_high_hist = hist["return_high_avg"]
    avg_return_high_curr = curr["return_high_avg"]

    if avg_return_high_hist > 0:
        decline_pct = (
            (avg_return_high_hist - avg_return_high_curr) / avg_return_high_hist * 100
        )
    else:
        decline_pct = 0

    if avg_return_high_curr <= 0:
        decay_level = "严重衰减"
        reason = "收益转为负值"
    elif decline_pct > 50:
        decay_level = "严重衰减"
        reason = f"收益下降超过50% ({decline_pct:.1f}%)"
    elif decline_pct > 30:
        decay_level = "中度衰减"
        reason = f"收益下降超过30% ({decline_pct:.1f}%)"
    elif decline_pct > 10:
        decay_level = "轻度衰减"
        reason = f"收益下降超过10% ({decline_pct:.1f}%)"
    else:
        decay_level = "无明显衰减"
        reason = f"收益下降小于10% ({decline_pct:.1f}%)"

    print(f"判定结果: {decay_level}")
    print(f"判定依据: {reason}")

    if decay_level in ["轻度衰减", "中度衰减", "严重衰减"]:
        print("\n可能原因分析:")

        signal_decline = (
            (hist["avg_daily_signals"] - curr["avg_daily_signals"])
            / hist["avg_daily_signals"]
            * 100
        )

        if signal_decline > 30:
            print(
                f"1. 信号数量显著减少 ({signal_decline:.1f}%)，可能策略拥挤或市场环境变化"
            )
        elif signal_decline < -30:
            print(
                f"1. 信号数量显著增加 ({abs(signal_decline):.1f}%)，可能市场环境更符合策略条件"
            )

        if curr["return_high_win_rate"] < hist["return_high_win_rate"] * 0.8:
            print("2. 胜率明显下降，可能市场波动加剧或策略逻辑失效")

        if curr["return_high_profit_factor"] < hist["return_high_profit_factor"] * 0.7:
            print("3. 盈亏比下降，可能止损效果变差或上涨幅度减小")

print("\n" + "=" * 80)
print("验证完成")
print("=" * 80)
