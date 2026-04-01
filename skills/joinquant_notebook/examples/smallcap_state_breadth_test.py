print("=== 小市值状态分层基线研究 - 广度分层测试 ===")

import numpy as np
import pandas as pd

try:
    start_date = "2023-01-01"
    end_date = "2024-12-31"

    print(f"\n测试期间: {start_date} ~ {end_date}")

    hs300_stocks = get_index_stocks("000300.XSHG")
    print(f"沪深300成分股数: {len(hs300_stocks)}")

    trade_days = get_trade_days(start_date=start_date, end_date=end_date)
    print(f"交易日数: {len(trade_days)}")

    results = []

    test_days = trade_days[::5]  # 每5天测一次，加快速度
    print(f"实际测试天数: {len(test_days)}")

    for i, date in enumerate(test_days[:100]):  # 只测试前100个样本点
        if i % 10 == 0:
            print(f"进度: {i}/{len(test_days[:100])}")

        prev_date = get_trade_days(end_date=date, count=2)[0]

        # 1. 计算市场广度（沪深300站上MA20比例）
        above_ma20_count = 0
        total_count = 0

        for stock in hs300_stocks[:50]:  # 只测前50只，加快速度
            try:
                prices = get_price(
                    stock,
                    end_date=prev_date,
                    count=20,
                    fields=["close"],
                    panel=False,
                    fill_paused=False,
                )
                if len(prices) >= 20:
                    ma20 = prices["close"].mean()
                    last_close = prices["close"].iloc[-1]
                    if last_close >= ma20:
                        above_ma20_count += 1
                    total_count += 1
            except:
                continue

        market_breadth = above_ma20_count / max(total_count, 1)

        # 2. 分层判断
        if market_breadth < 0.15:
            breadth_state = "极弱"
        elif market_breadth < 0.25:
            breadth_state = "弱"
        elif market_breadth < 0.35:
            breadth_state = "中"
        else:
            breadth_state = "强"

        # 3. 计算涨停数（情绪指标）
        all_stocks = get_all_securities("stock", prev_date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

        try:
            zt_df = get_price(
                all_stocks[:500],
                end_date=prev_date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
                fill_paused=False,
            )
            if not zt_df.empty:
                zt_df = zt_df.dropna()
                zt_count = len(zt_df[zt_df["close"] == zt_df["high_limit"]])
            else:
                zt_count = 0
        except:
            zt_count = 0

        # 4. 情绪分层
        if zt_count < 30:
            sentiment_state = "冰点"
        elif zt_count < 50:
            sentiment_state = "启动"
        elif zt_count < 80:
            sentiment_state = "发酵"
        else:
            sentiment_state = "高潮"

        # 5. 选小市值股票（5-30亿）
        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.circulating_market_cap >= 5,
            valuation.circulating_market_cap <= 30,
        )

        df_cap = get_fundamentals(q, date=date)

        if df_cap.empty:
            continue

        smallcap_stocks = list(df_cap["code"])[:10]

        # 6. 计算次日收益
        next_date = get_trade_days(end_date=date, count=3)[-1]

        returns_list = []
        for stock in smallcap_stocks:
            try:
                prices = get_price(
                    stock,
                    end_date=next_date,
                    count=2,
                    fields=["close"],
                    panel=False,
                    fill_paused=False,
                )
                if len(prices) >= 2:
                    today_close = prices["close"].iloc[0]
                    next_close = prices["close"].iloc[1]
                    ret = (next_close - today_close) / today_close * 100
                    returns_list.append(ret)
            except:
                continue

        if returns_list:
            avg_return = np.mean(returns_list)
            results.append(
                {
                    "date": date,
                    "market_breadth": market_breadth,
                    "breadth_state": breadth_state,
                    "zt_count": zt_count,
                    "sentiment_state": sentiment_state,
                    "avg_return": avg_return,
                    "stock_count": len(smallcap_stocks),
                    "valid_count": len(returns_list),
                }
            )

    print(f"\n完成! 共收集 {len(results)} 个样本")

    if results:
        df_results = pd.DataFrame(results)

        print("\n" + "=" * 60)
        print("【市场广度分层统计】")
        print("=" * 60)

        breadth_groups = df_results.groupby("breadth_state").agg(
            {"avg_return": ["mean", "std", "count"]}
        )

        for state in ["极弱", "弱", "中", "强"]:
            if state in breadth_groups.index:
                avg_ret = breadth_groups.loc[state, ("avg_return", "mean")]
                std_ret = breadth_groups.loc[state, ("avg_return", "std")]
                count = breadth_groups.loc[state, ("avg_return", "count")]
                print(
                    f"{state}: 平均收益={avg_ret:.2f}%, 标准差={std_ret:.2f}%, 样本数={count}"
                )

        print("\n" + "=" * 60)
        print("【情绪分层统计】")
        print("=" * 60)

        sentiment_groups = df_results.groupby("sentiment_state").agg(
            {"avg_return": ["mean", "std", "count"]}
        )

        for state in ["冰点", "启动", "发酵", "高潮"]:
            if state in sentiment_groups.index:
                avg_ret = sentiment_groups.loc[state, ("avg_return", "mean")]
                std_ret = sentiment_groups.loc[state, ("avg_return", "std")]
                count = sentiment_groups.loc[state, ("avg_return", "count")]
                print(
                    f"{state}: 平均收益={avg_ret:.2f}%, 标准差={std_ret:.2f}%, 样本数={count}"
                )

        print("\n" + "=" * 60)
        print("【状态过滤效果对比】")
        print("=" * 60)

        all_avg = df_results["avg_return"].mean()
        print(f"无过滤: 平均收益={all_avg:.2f}%, 样本数={len(df_results)}")

        breadth_filtered = df_results[df_results["market_breadth"] >= 0.25]
        if not breadth_filtered.empty:
            bf_avg = breadth_filtered["avg_return"].mean()
            print(
                f"广度过滤(>=25%): 平均收益={bf_avg:.2f}%, 样本数={len(breadth_filtered)}, 提升={bf_avg - all_avg:.2f}%"
            )

        sentiment_filtered = df_results[df_results["zt_count"] >= 50]
        if not sentiment_filtered.empty:
            sf_avg = sentiment_filtered["avg_return"].mean()
            print(
                f"情绪过滤(涨停>=50): 平均收益={sf_avg:.2f}%, 样本数={len(sentiment_filtered)}, 提升={sf_avg - all_avg:.2f}%"
            )

        both_filtered = df_results[
            (df_results["market_breadth"] >= 0.25) & (df_results["zt_count"] >= 50)
        ]
        if not both_filtered.empty:
            both_avg = both_filtered["avg_return"].mean()
            print(
                f"双过滤: 平均收益={both_avg:.2f}%, 样本数={len(both_filtered)}, 提升={both_avg - all_avg:.2f}%"
            )

        print("\n" + "=" * 60)
        print("【极弱市场分析】")
        print("=" * 60)

        extreme_weak = df_results[df_results["breadth_state"] == "极弱"]
        if not extreme_weak.empty:
            ew_avg = extreme_weak["avg_return"].mean()
            ew_win = (extreme_weak["avg_return"] > 0).sum() / len(extreme_weak) * 100
            print(f"极弱市场平均收益: {ew_avg:.2f}%")
            print(f"极弱市场胜率: {ew_win:.1f}%")
            print(f"极弱市场样本数: {len(extreme_weak)}")

            if ew_avg < 0:
                print("结论: 极弱市场小市值策略系统性失效!")
            else:
                print("结论: 极弱市场仍需谨慎，表现较弱")

        print("\n" + "=" * 60)
        print("【情绪冰点分析】")
        print("=" * 60)

        freeze = df_results[df_results["sentiment_state"] == "冰点"]
        if not freeze.empty:
            fz_avg = freeze["avg_return"].mean()
            fz_win = (freeze["avg_return"] > 0).sum() / len(freeze) * 100
            print(f"情绪冰点平均收益: {fz_avg:.2f}%")
            print(f"情绪冰点胜率: {fz_win:.1f}%")
            print(f"情绪冰点样本数: {len(freeze)}")

            if fz_avg < 0:
                print("结论: 情绪冰点时小市值策略系统性失效!")
            else:
                print("结论: 情绪冰点表现较弱，建议停手")

        print("\n" + "=" * 60)
        print("【状态组合矩阵】")
        print("=" * 60)

        combo_groups = df_results.groupby(["breadth_state", "sentiment_state"]).agg(
            {"avg_return": ["mean", "count"]}
        )

        for idx in combo_groups.index:
            breadth, sentiment = idx
            avg_ret = combo_groups.loc[idx, ("avg_return", "mean")]
            count = combo_groups.loc[idx, ("avg_return", "count")]
            print(f"{breadth}+{sentiment}: 平均收益={avg_ret:.2f}%, 样本数={count}")

        print("\n" + "=" * 60)
        print("【建议】")
        print("=" * 60)

        if not extreme_weak.empty and extreme_weak["avg_return"].mean() < 0:
            print("1. 建议在极弱市场(广度<15%)停手")
        elif not extreme_weak.empty:
            print("1. 极弱市场表现较弱，建议谨慎")

        if not freeze.empty and freeze["avg_return"].mean() < 0:
            print("2. 建议在情绪冰点(涨停<30)停手")
        elif not freeze.empty:
            print("2. 情绪冰点表现较弱，建议降低仓位")

        if (
            not both_filtered.empty
            and not breadth_filtered.empty
            and not sentiment_filtered.empty
        ):
            both_avg = both_filtered["avg_return"].mean()
            bf_avg = breadth_filtered["avg_return"].mean()
            sf_avg = sentiment_filtered["avg_return"].mean()

            if both_avg > bf_avg and both_avg > sf_avg:
                print("3. 建议同时使用广度和情绪过滤（双过滤效果最佳）")
            elif bf_avg > sf_avg:
                print("3. 建议优先使用广度过滤")
            else:
                print("3. 建议优先使用情绪过滤")

        print("\n" + "=" * 60)
        print("测试完成")
        print("=" * 60)

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("=== 测试结束 ===")
