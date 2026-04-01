print("=== 小市值状态分层快速测试 ===")

import numpy as np

try:
    start_date = "2024-01-01"
    end_date = "2024-06-30"

    print(f"\n测试期间: {start_date} ~ {end_date}")

    hs300_stocks = get_index_stocks("000300.XSHG")
    print(f"沪深300成分股数: {len(hs300_stocks)}")

    # 获取交易日列表 - 使用get_price间接获取
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

    test_days = trade_days[::10]  # 每10天测一次
    print(f"实际测试天数: {len(test_days)}")

    for i, date in enumerate(test_days):
        date_str = date.strftime("%Y-%m-%d")
        print(f"进度: {i + 1}/{len(test_days)} - {date_str}")

        # 获取前一天
        prev_idx = max(0, i * 10 - 1)
        prev_date_str = trade_days[prev_idx].strftime("%Y-%m-%d")

        # 1. 计算市场广度（只测前30只沪深300）
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

        # 3. 涨停数（只测前200只股票）
        all_stocks = get_all_securities("stock", prev_date_str).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"][
            :200
        ]

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

        smallcap_stocks = list(df_cap["code"])[:5]  # 只测5只

        # 6. 次日收益
        next_idx = min(len(trade_days) - 1, i * 10 + 1)
        next_date_str = trade_days[next_idx].strftime("%Y-%m-%d")

        returns = []
        for stock in smallcap_stocks:
            try:
                prices = get_price(
                    stock,
                    end_date=next_date_str,
                    count=2,
                    fields=["close"],
                    panel=False,
                    fill_paused=False,
                )
                if len(prices) >= 2:
                    ret = (
                        (
                            float(prices["close"].iloc[-1])
                            - float(prices["close"].iloc[-2])
                        )
                        / float(prices["close"].iloc[-2])
                        * 100
                    )
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

    if len(results) > 0:
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
                cnt = len(breadth_stats[state])
                print(f"{state}: 平均收益={avg:.2f}%, 样本={cnt}")

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
                cnt = len(sentiment_stats[state])
                print(f"{state}: 平均收益={avg:.2f}%, 样本={cnt}")

        all_avg = np.mean([r["return"] for r in results])
        print(f"\n无过滤基准: {all_avg:.2f}%")

        bf_rets = [r["return"] for r in results if r["breadth"] >= 0.25]
        if bf_rets:
            print(
                f"广度>=25%: {np.mean(bf_rets):.2f}% (提升{np.mean(bf_rets) - all_avg:.2f}%)"
            )

        sf_rets = [r["return"] for r in results if r["zt"] >= 50]
        if sf_rets:
            print(
                f"涨停>=50: {np.mean(sf_rets):.2f}% (提升{np.mean(sf_rets) - all_avg:.2f}%)"
            )

        both_rets = [
            r["return"] for r in results if r["breadth"] >= 0.25 and r["zt"] >= 50
        ]
        if both_rets:
            print(
                f"双过滤: {np.mean(both_rets):.2f}% (提升{np.mean(both_rets) - all_avg:.2f}%)"
            )

        print("\n" + "=" * 50)
        print("【关键发现】")
        print("=" * 50)
        if "极弱" in breadth_stats:
            ew_avg = np.mean(breadth_stats["极弱"])
            ew_cnt = len(breadth_stats["极弱"])
            if ew_avg < 0:
                print(f"极弱市场收益{ew_avg:.2f}% ({ew_cnt}个样本) - 系统性失效!")
            else:
                print(f"极弱市场收益{ew_avg:.2f}% ({ew_cnt}个样本) - 表现较弱")

        if "冰点" in sentiment_stats:
            fz_avg = np.mean(sentiment_stats["冰点"])
            fz_cnt = len(sentiment_stats["冰点"])
            if fz_avg < 0:
                print(f"情绪冰点收益{fz_avg:.2f}% ({fz_cnt}个样本) - 系统性失效!")
            else:
                print(f"情绪冰点收益{fz_avg:.2f}% ({fz_cnt}个样本) - 表现较弱")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n=== 测试完成 ===")
