"""
二板策略 - RiceQuant Notebook格式
测试2024年数据（扩大样本）
"""

print("=" * 70)
print("二板策略 RiceQuant Notebook 测试 - 2024年")
print("=" * 70)

try:
    import numpy as np

    print("\n步骤1: 获取交易日")
    dates = get_trading_dates("2024-01-01", "2024-12-31")
    print(f"2024年交易日: {len(dates)}天")

    print("\n步骤2: 统计涨停家数（每10天测试1次）")
    results = []
    zt_counts = []

    # 每10个交易日测试1次
    test_dates = dates[::10]

    for i, date in enumerate(test_dates):
        print(f"\n处理 {date.strftime('%Y-%m-%d')} ({i + 1}/{len(test_dates)})")

        # 扩大样本到500只股票
        all_stocks = all_instruments("CS")
        stock_list = all_stocks["order_book_id"].tolist()
        stock_list = [
            s
            for s in stock_list
            if isinstance(s, str) and not s.startswith(("688", "4", "8"))
        ][:500]

        # 统计涨停
        zt_count = 0
        zt_stocks = []

        for stock in stock_list:
            try:
                bars = history_bars(stock, 1, "1d", "close,limit_up", end_date=date)
                if bars is not None and len(bars) > 0:
                    if bars[0]["close"] >= bars[0]["limit_up"] * 0.99:
                        zt_count += 1
                        zt_stocks.append(stock)
            except:
                pass

        zt_counts.append(zt_count)
        print(f"  涨停: {zt_count}只 (样本500只)")

        # 如果涨停>=10只（全市场约100只）
        if zt_count >= 5:  # 样本500只，阈值降低
            print(f"  触发情绪开关")

            # 尝试找二板
            try:
                prev_date = (
                    dates[dates.index(date) - 1] if dates.index(date) > 0 else None
                )
                prev2_date = (
                    dates[dates.index(date) - 2] if dates.index(date) > 1 else None
                )

                if prev_date and prev2_date:
                    # 获取前两天的涨停
                    zt_prev = []
                    zt_prev2 = []

                    for stock in stock_list[:200]:  # 限制数量避免超时
                        try:
                            # 前一天
                            bars1 = history_bars(
                                stock, 1, "1d", "close,limit_up", end_date=prev_date
                            )
                            if bars1 is not None and len(bars1) > 0:
                                if bars1[0]["close"] >= bars1[0]["limit_up"] * 0.99:
                                    zt_prev.append(stock)

                            # 前两天
                            bars2 = history_bars(
                                stock, 1, "1d", "close,limit_up", end_date=prev2_date
                            )
                            if bars2 is not None and len(bars2) > 0:
                                if bars2[0]["close"] >= bars2[0]["limit_up"] * 0.99:
                                    zt_prev2.append(stock)
                        except:
                            pass

                    # 二板 = 今天涨停 & 昨天涨停 & 前天不涨停
                    sb = list(set(zt_stocks) & set(zt_prev) - set(zt_prev2))
                    print(f"  二板候选: {len(sb)}只")

                    if len(sb) > 0:
                        # 测试第一个二板
                        test_stock = sb[0]
                        next_date_idx = dates.index(date) + 1
                        next_date = (
                            dates[next_date_idx] if next_date_idx < len(dates) else None
                        )

                        if next_date:
                            next_bars = history_bars(
                                test_stock,
                                1,
                                "1d",
                                "open,close,limit_up",
                                end_date=next_date,
                            )
                            if next_bars is not None and len(next_bars) > 0:
                                open_p = next_bars[0]["open"]
                                close_p = next_bars[0]["close"]
                                limit_p = next_bars[0]["limit_up"]

                                # 非涨停开盘
                                if open_p < limit_p * 0.99:
                                    buy_p = open_p * 1.005
                                    profit = (close_p / buy_p - 1) * 100
                                    results.append(
                                        {
                                            "date": date.strftime("%Y-%m-%d"),
                                            "stock": test_stock,
                                            "profit": profit,
                                        }
                                    )
                                    print(f"  ✓ 买入{test_stock}, 收益{profit:.2f}%")
            except:
                pass

    print("\n" + "=" * 70)
    print("测试结果")
    print("=" * 70)

    print(f"平均涨停家数: {np.mean(zt_counts):.1f}只 (样本500只)")
    print(f"估算全市场涨停: {np.mean(zt_counts) * 8:.0f}只")

    if results:
        profits = [r["profit"] for r in results]
        wins = len([p for p in profits if p > 0])

        print(f"\n交易次数: {len(results)}")
        print(f"胜率: {wins / len(results) * 100:.1f}%")
        print(f"平均收益: {np.mean(profits):.2f}%")
        print(f"总收益: {sum(profits):.2f}%")

        print("\n交易详情:")
        for r in results:
            print(f"  {r['date']} {r['stock']}: {r['profit']:.2f}%")
    else:
        print("\n未找到交易机会")

    print("\n测试完成")

except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()
