print("=== 小市值状态分层快速测试 ===")

import numpy as np

try:
    start_date = "2024-01-01"
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

    # 只测试前6个样本点，更详细调试
    test_indices = [0, 10, 20, 30, 40, 50]
    test_indices = [i for i in test_indices if i < len(trade_days)]

    print(f"测试样本点数: {len(test_indices)}")

    for idx in test_indices:
        date = trade_days[idx]
        date_str = date.strftime("%Y-%m-%d")
        print(f"\n{'=' * 40}")
        print(f"测试 {date_str}")

        # 获取前一天
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
        print(f"市场广度: {market_breadth:.1%} (高于MA20: {above_ma20}/{total})")

        # 2. 广度分层
        if market_breadth < 0.15:
            breadth_state = "极弱"
        elif market_breadth < 0.25:
            breadth_state = "弱"
        elif market_breadth < 0.35:
            breadth_state = "中"
        else:
            breadth_state = "强"

        print(f"广度状态: {breadth_state}")

        # 3. 涨停数
        all_stocks = get_all_securities("stock", prev_date_str).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"][
            :300
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

        print(f"涨停数: {zt_count}")

        # 4. 情绪分层
        if zt_count < 30:
            sentiment_state = "冰点"
        elif zt_count < 50:
            sentiment_state = "启动"
        elif zt_count < 80:
            sentiment_state = "发酵"
        else:
            sentiment_state = "高潮"

        print(f"情绪状态: {sentiment_state}")

        # 5. 选小市值（5-30亿）
        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.circulating_market_cap >= 5,
            valuation.circulating_market_cap <= 30,
        )

        df_cap = get_fundamentals(q, date=date_str)
        print(f"小市值股票数(5-30亿): {len(df_cap) if not df_cap.empty else 0}")

        if df_cap.empty:
            print("无小市值股票，跳过")
            continue

        smallcap_stocks = list(df_cap["code"])[:5]
        print(f"选中的股票: {smallcap_stocks}")

        # 6. 次日收益
        next_idx = min(len(trade_days) - 1, idx + 1)
        next_date_str = trade_days[next_idx].strftime("%Y-%m-%d")
        print(f"次日日期: {next_date_str}")

        returns = []
        for stock in smallcap_stocks:
            try:
                # 尝试获取当日和次日价格
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
                        print(
                            f"  {stock}: 今日={today_close:.2f}, 次日={next_close:.2f}, 收益={ret:.2f}%"
                        )
            except Exception as e:
                print(f"  {stock}: 获取失败 - {e}")

        print(f"有效收益数: {len(returns)}")

        if returns:
            avg_ret = np.mean(returns)
            print(f"平均收益: {avg_ret:.2f}%")
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
        else:
            print("无有效收益数据")

    print(f"\n{'=' * 50}")
    print(f"完成! 共收集 {len(results)} 个样本")

    if results:
        print("\n【广度分层结果】")
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

        print("\n【情绪分层结果】")
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

        if len(results) > 0:
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

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n=== 测试完成 ===")
