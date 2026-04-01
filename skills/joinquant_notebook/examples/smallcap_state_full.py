print("=== 小市值状态分层完整测试 ===")

import numpy as np

try:
    start_date = "2023-06-01"
    end_date = "2024-06-30"

    print(f"测试期间: {start_date} ~ {end_date}")

    hs300_stocks = get_index_stocks("000300.XSHG")
    print(f"沪深300成分股数: {len(hs300_stocks)}")

    # 获取交易日列表
    benchmark_price = get_price(
        "000300.XSHG",
        start_date=start_date,
        end_date=end_date,
        frequency="daily",
        fields=["close"],
        panel=False,
    )
    trade_days = list(benchmark_price.index)
    print(f"交易日数: {len(trade_days)}")

    results = []

    # 每5天测一次
    test_indices = range(0, len(trade_days), 5)
    print(f"测试样本点数: {len(test_indices)}")

    for i, idx in enumerate(test_indices):
        if i % 10 == 0:
            print(f"进度: {i}/{len(test_indices)}")

        date = trade_days[idx]
        date_str = date.strftime("%Y-%m-%d")

        prev_idx = max(0, idx - 1)
        prev_date_str = trade_days[prev_idx].strftime("%Y-%m-%d")

        # 1. 市场广度
        above_ma20 = 0
        total = 0

        for stock in hs300_stocks[:30]:
            try:
                prices = get_price(
                    stock,
                    end_date=prev_date_str,
                    count=20,
                    fields=["close"],
                    panel=False,
                    fill_paused=False,
                )
                if len(prices) >= 20:
                    ma20 = float(prices["close"].mean())
                    last_close = float(prices["close"].iloc[-1])
                    if last_close >= ma20:
                        above_ma20 += 1
                    total += 1
            except:
                pass

        market_breadth = above_ma20 / max(total, 1)

        # 2. 广度分层
        if market_breadth < 0.15:
            breadth_state = "极弱"
        elif market_breadth < 0.25:
            breadth_state = "弱"
        elif market_breadth < 0.35:
            breadth_state = "中"
        else:
            breadth_state = "强"

        # 3. 涨停数（扩大范围）
        all_stocks = get_all_securities("stock", prev_date_str).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if s[0] not in "48" and s[0] not in "83" and s[:2] != "68"
        ][:500]

        zt_count = 0
        try:
            df = get_price(
                all_stocks,
                end_date=prev_date_str,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
                fill_paused=False,
            )
            if not df.empty:
                df = df.dropna()
                zt_count = len(df[df["close"] == df["high_limit"]])
        except:
            pass

        # 4. 情绪分层
        if zt_count < 30:
            sentiment_state = "冰点"
        elif zt_count < 50:
            sentiment_state = "启动"
        elif zt_count < 80:
            sentiment_state = "发酵"
        else:
            sentiment_state = "高潮"

        # 5. 选小市值（5-30亿）
        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.circulating_market_cap >= 5,
            valuation.circulating_market_cap <= 30,
        )

        df_cap = get_fundamentals(q, date=date_str)

        if df_cap.empty:
            continue

        # 随机选5只，避免集中少数股票
        smallcap_stocks = list(df_cap["code"])
        if len(smallcap_stocks) > 5:
            import random

            random.seed(idx)
            smallcap_stocks = random.sample(smallcap_stocks, 5)

        # 6. 次日收益
        next_idx = min(len(trade_days) - 1, idx + 1)
        next_date_str = trade_days[next_idx].strftime("%Y-%m-%d")

        returns = []
        for stock in smallcap_stocks:
            try:
                prices_today = get_price(
                    stock,
                    end_date=date_str,
                    count=1,
                    fields=["close"],
                    panel=False,
                    fill_paused=False,
                )
                prices_next = get_price(
                    stock,
                    end_date=next_date_str,
                    count=1,
                    fields=["close"],
                    panel=False,
                    fill_paused=False,
                )

                if not prices_today.empty and not prices_next.empty:
                    today_close = float(prices_today["close"].iloc[0])
                    next_close = float(prices_next["close"].iloc[0])

                    if today_close > 0:
                        ret = (next_close - today_close) / today_close * 100
                        returns.append(ret)
            except:
                pass

        if returns:
            avg_ret = np.mean(returns)
            results.append(
                {
                    "date": date_str,
                    "breadth": market_breadth,
                    "breadth_state": breadth_state,
                    "zt": zt_count,
                    "sentiment_state": sentiment_state,
                    "return": avg_ret,
                }
            )

    print(f"\n完成! 共收集 {len(results)} 个样本")

    if results:
        print("\n" + "=" * 50)
        print("【广度分层结果】")
        print("=" * 50)
        breadth_stats = {}
        for r in results:
            state = r["breadth_state"]
            if state not in breadth_stats:
                breadth_stats[state] = []
            breadth_stats[state].append(r["return"])

        for state in ["极弱", "弱", "中", "强"]:
            if state in breadth_stats:
                avg = np.mean(breadth_stats[state])
                std = np.std(breadth_stats[state])
                cnt = len(breadth_stats[state])
                win_rate = sum(1 for x in breadth_stats[state] if x > 0) / cnt * 100
                print(
                    f"{state}: 平均收益={avg:.2f}% ± {std:.2f}%, 胜率={win_rate:.0f}%, 样本={cnt}"
                )

        print("\n" + "=" * 50)
        print("【情绪分层结果】")
        print("=" * 50)
        sentiment_stats = {}
        for r in results:
            state = r["sentiment_state"]
            if state not in sentiment_stats:
                sentiment_stats[state] = []
            sentiment_stats[state].append(r["return"])

        for state in ["冰点", "启动", "发酵", "高潮"]:
            if state in sentiment_stats:
                avg = np.mean(sentiment_stats[state])
                std = np.std(sentiment_stats[state])
                cnt = len(sentiment_stats[state])
                win_rate = sum(1 for x in sentiment_stats[state] if x > 0) / cnt * 100
                print(
                    f"{state}: 平均收益={avg:.2f}% ± {std:.2f}%, 胜率={win_rate:.0f}%, 样本={cnt}"
                )

        all_avg = np.mean([r["return"] for r in results])
        all_win = sum(1 for r in results if r["return"] > 0) / len(results) * 100
        print(f"\n无过滤基准: {all_avg:.2f}%, 胜率={all_win:.0f}%")

        print("\n" + "=" * 50)
        print("【状态过滤效果】")
        print("=" * 50)

        bf_rets = [r["return"] for r in results if r["breadth"] >= 0.25]
        if bf_rets:
            bf_avg = np.mean(bf_rets)
            bf_win = sum(1 for x in bf_rets if x > 0) / len(bf_rets) * 100
            print(
                f"广度>=25%: {bf_avg:.2f}%, 胜率={bf_win:.0f}% (提升{bf_avg - all_avg:.2f}%)"
            )

        sf_rets = [r["return"] for r in results if r["zt"] >= 50]
        if sf_rets:
            sf_avg = np.mean(sf_rets)
            sf_win = sum(1 for x in sf_rets if x > 0) / len(sf_rets) * 100
            print(
                f"涨停>=50: {sf_avg:.2f}%, 胜率={sf_win:.0f}% (提升{sf_avg - all_avg:.2f}%)"
            )

        both_rets = [
            r["return"] for r in results if r["breadth"] >= 0.25 and r["zt"] >= 50
        ]
        if both_rets:
            both_avg = np.mean(both_rets)
            both_win = sum(1 for x in both_rets if x > 0) / len(both_rets) * 100
            print(
                f"双过滤: {both_avg:.2f}%, 胜率={both_win:.0f}% (提升{both_avg - all_avg:.2f}%)"
            )

        print("\n" + "=" * 50)
        print("【关键发现】")
        print("=" * 50)

        if "极弱" in breadth_stats:
            ew_avg = np.mean(breadth_stats["极弱"])
            ew_cnt = len(breadth_stats["极弱"])
            ew_win = sum(1 for x in breadth_stats["极弱"] if x > 0) / ew_cnt * 100
            if ew_avg < 0 or ew_win < 40:
                print(
                    f"极弱市场: 收益{ew_avg:.2f}%, 胜率{ew_win:.0f}% ({ew_cnt}样本) - 系统性失效!"
                )
            else:
                print(
                    f"极弱市场: 收益{ew_avg:.2f}%, 胜率{ew_win:.0f}% ({ew_cnt}样本) - 表现较弱"
                )

        if "冰点" in sentiment_stats:
            fz_avg = np.mean(sentiment_stats["冰点"])
            fz_cnt = len(sentiment_stats["冰点"])
            fz_win = sum(1 for x in sentiment_stats["冰点"] if x > 0) / fz_cnt * 100
            if fz_avg < 0 or fz_win < 40:
                print(
                    f"情绪冰点: 收益{fz_avg:.2f}%, 胜率{fz_win:.0f}% ({fz_cnt}样本) - 系统性失效!"
                )
            else:
                print(
                    f"情绪冰点: 收益{fz_avg:.2f}%, 胜率{fz_win:.0f}% ({fz_cnt}样本) - 表现较弱"
                )

        print("\n" + "=" * 50)
        print("【状态组合矩阵】")
        print("=" * 50)

        combo_stats = {}
        for r in results:
            key = f"{r['breadth_state']}+{r['sentiment_state']}"
            if key not in combo_stats:
                combo_stats[key] = []
            combo_stats[key].append(r["return"])

        for key in sorted(combo_stats.keys()):
            avg = np.mean(combo_stats[key])
            cnt = len(combo_stats[key])
            print(f"{key}: {avg:.2f}% ({cnt}样本)")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n=== 测试完成 ===")
