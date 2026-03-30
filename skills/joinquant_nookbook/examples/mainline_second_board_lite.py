from jqdata import *
import pandas as pd
import numpy as np

print("=" * 80)
print("任务07v2：主线二板组合测试（简化版）")
print("=" * 80)

test_dates = list(get_trade_days(end_date="2024-12-31", count=250))
test_dates = test_dates[
    test_dates.index("2024-01-02") : test_dates.index("2024-12-31") + 1
]
print(f"测试期间：2024全年，共 {len(test_dates)} 个交易日")

mainline_data = []
second_board_data = []

for i in range(1, min(len(test_dates), 60)):
    prev_date = test_dates[i - 1]
    curr_date = test_dates[i]

    print(f"进度: {i}/{min(len(test_dates), 60)}")

    try:
        all_stocks = get_all_securities("stock", prev_date).index.tolist()
        all_stocks = [
            s for s in all_stocks if not s.startswith("68") and s[:1] not in ["4", "8"]
        ]

        price_prev = get_price(
            all_stocks,
            end_date=prev_date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        if price_prev.empty:
            continue

        zt_stocks = price_prev[
            abs(price_prev["close"] - price_prev["high_limit"])
            / price_prev["high_limit"]
            < 0.01
        ]["code"].tolist()

        if len(zt_stocks) == 0:
            continue

        price_curr = get_price(
            zt_stocks,
            end_date=curr_date,
            count=1,
            fields=["open", "close", "high", "high_limit"],
            panel=False,
        )
        if price_curr.empty:
            continue

        for stock in zt_stocks[:20]:
            try:
                prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                curr_row = price_curr[price_curr["code"] == stock].iloc[0]

                prev_close = float(prev_row["close"])
                curr_open = float(curr_row["open"])
                curr_close = float(curr_row["close"])
                curr_high = float(curr_row["high"])

                open_pct = (curr_open - prev_close) / prev_close * 100

                if 0.5 <= open_pct <= 1.5:
                    intra_return = (curr_close - curr_open) / curr_open * 100
                    mainline_data.append(
                        {
                            "date": curr_date,
                            "stock": stock,
                            "open_pct": open_pct,
                            "return": intra_return,
                            "type": "mainline",
                        }
                    )
            except:
                continue

        try:
            prev2_date = test_dates[i - 2] if i >= 2 else None
            if prev2_date:
                hl1 = get_price(
                    all_stocks,
                    end_date=prev_date,
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                hl1 = hl1[hl1["close"] == hl1["high_limit"]]["code"].tolist()

                hl2 = get_price(
                    all_stocks,
                    end_date=prev2_date,
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                hl2 = hl2[hl2["close"] == hl2["high_limit"]]["code"].tolist()

                hl3 = get_price(
                    all_stocks,
                    end_date=test_dates[i - 3] if i >= 3 else prev2_date,
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                hl3 = hl3[hl3["close"] == hl3["high_limit"]]["code"].tolist()

                second_board = list(set(hl1) & set(hl2) - set(hl3))

                if len(second_board) > 0:
                    sb_price = get_price(
                        second_board[:10],
                        end_date=curr_date,
                        count=1,
                        fields=["open", "close", "high", "high_limit"],
                        panel=False,
                    )
                    if not sb_price.empty:
                        for s in second_board[:10]:
                            try:
                                sb_row = sb_price[sb_price["code"] == s].iloc[0]
                                sb_open = float(sb_row["open"])
                                sb_close = float(sb_row["close"])
                                sb_high = float(sb_row["high"])
                                sb_limit = float(sb_row["high_limit"])

                                if sb_open != sb_limit:
                                    buy_price = sb_open * 1.005
                                    sell_price = (
                                        sb_high if sb_high > buy_price else sb_close
                                    )
                                    profit = (sell_price / buy_price - 1) * 100
                                    second_board_data.append(
                                        {
                                            "date": curr_date,
                                            "stock": s,
                                            "return": profit,
                                            "type": "second_board",
                                        }
                                    )
                            except:
                                continue
        except:
            pass
    except:
        continue

print("\n" + "=" * 80)
print("信号统计")
print("=" * 80)

ml_count = len(mainline_data)
sb_count = len(second_board_data)
print(f"主线信号数: {ml_count}")
print(f"二板信号数: {sb_count}")

if ml_count > 0:
    ml_df = pd.DataFrame(mainline_data)
    print(f"主线平均收益: {ml_df['return'].mean():.2f}%")
    print(f"主线胜率: {(ml_df['return'] > 0).sum() / ml_count * 100:.2f}%")

if sb_count > 0:
    sb_df = pd.DataFrame(second_board_data)
    print(f"二板平均收益: {sb_df['return'].mean():.2f}%")
    print(f"二板胜率: {(sb_df['return'] > 0).sum() / sb_count * 100:.2f}%")

if ml_count > 0 and sb_count > 0:
    ml_df = pd.DataFrame(mainline_data)
    sb_df = pd.DataFrame(second_board_data)

    merged = pd.merge(ml_df, sb_df, on=["date", "stock"], how="outer", indicator=True)
    overlap_count = len(merged[merged["_merge"] == "both"])
    overlap_ratio = (
        overlap_count / (ml_count + sb_count) * 100 if (ml_count + sb_count) > 0 else 0
    )

    print(f"\n信号重叠数: {overlap_count}")
    print(f"重叠比例: {overlap_ratio:.2f}%")

    print("\n" + "=" * 80)
    print("组合方案测试")
    print("=" * 80)

    scheme_A_returns = []
    scheme_B_returns = []
    scheme_C_returns = []
    scheme_D_returns = []

    for date in ml_df["date"].unique():
        ml_today = ml_df[ml_df["date"] == date]
        sb_today = sb_df[sb_df["date"] == date]

        ml_return = ml_today["return"].mean() if len(ml_today) > 0 else None
        sb_return = sb_today["return"].mean() if len(sb_today) > 0 else None

        if ml_return is not None:
            scheme_A_returns.append(ml_return)
        elif sb_return is not None:
            scheme_A_returns.append(sb_return)

        if sb_return is not None:
            scheme_B_returns.append(sb_return)
        elif ml_return is not None:
            scheme_B_returns.append(ml_return)

        if ml_return is not None or sb_return is not None:
            returns = []
            if ml_return is not None:
                returns.append(ml_return)
            if sb_return is not None:
                returns.append(sb_return)
            scheme_C_returns.append(np.mean(returns))

            scheme_D_returns.append(
                max(ml_return if ml_return else -999, sb_return if sb_return else -999)
            )

    for scheme_name, returns in [
        ("A_主线优先", scheme_A_returns),
        ("B_二板优先", scheme_B_returns),
        ("C_并行平均", scheme_C_returns),
        ("D_收益优先", scheme_D_returns),
    ]:
        if len(returns) > 0:
            cum_return = sum(returns)
            win_rate = len([r for r in returns if r > 0]) / len(returns) * 100
            avg_return = np.mean(returns)
            print(f"\n方案{scheme_name}:")
            print(f"  交易次数: {len(returns)}")
            print(f"  累计收益: {cum_return:.2f}%")
            print(f"  平均收益: {avg_return:.2f}%")
            print(f"  胜率: {win_rate:.2f}%")

print("\n" + "=" * 80)
print("结论")
print("=" * 80)

if ml_count > 0 and sb_count > 0:
    if overlap_ratio < 10:
        print("信号重叠比例低，适合组合使用")
        print("推荐方案: C(并行平均)或D(收益优先)")
    else:
        print(f"信号重叠比例较高({overlap_ratio:.2f}%)，组合效果有限")
elif ml_count > 0:
    print("仅主线信号有效，单独使用主线策略")
elif sb_count > 0:
    print("仅二板信号有效，单独使用二板策略")
else:
    print("无有效信号")

print("\n测试完成！")
