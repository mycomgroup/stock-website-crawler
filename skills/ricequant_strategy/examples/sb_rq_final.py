"""
二板策略 - RiceQuant Notebook格式
测试2022年4月数据
"""

print("=" * 70)
print("二板策略 RiceQuant Notebook 测试")
print("=" * 70)

try:
    import numpy as np

    print("\n步骤1: 获取交易日")
    dates = get_trading_dates("2022-04-01", "2022-04-30")
    print(f"2022年4月交易日: {len(dates)}天")

    print("\n步骤2: 统计涨停家数")
    results = []

    for i, date in enumerate(dates[:10]):
        print(f"\n处理 {date.strftime('%Y-%m-%d')} ({i + 1}/10)")

        # 获取所有股票（正确方式）
        all_stocks = all_instruments("CS")
        stock_list = all_stocks["order_book_id"].tolist()
        stock_list = [
            s
            for s in stock_list
            if isinstance(s, str) and not s.startswith(("688", "4", "8"))
        ][:100]

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

        print(f"  涨停: {zt_count}只 (样本100只)")

        if zt_count >= 3:
            test_stock = zt_stocks[0]

            try:
                next_date = dates[i + 1] if i + 1 < len(dates) else None
                if next_date:
                    next_bars = history_bars(
                        test_stock, 1, "1d", "open,close,limit_up", end_date=next_date
                    )
                    if next_bars is not None and len(next_bars) > 0:
                        open_p = next_bars[0]["open"]
                        close_p = next_bars[0]["close"]
                        limit_p = next_bars[0]["limit_up"]

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
                            print(f"  买入{test_stock}, 收益{profit:.2f}%")
            except:
                pass

    print("\n" + "=" * 70)
    print("测试结果")
    print("=" * 70)

    if results:
        profits = [r["profit"] for r in results]
        wins = len([p for p in profits if p > 0])

        print(f"交易次数: {len(results)}")
        print(f"胜率: {wins / len(results) * 100:.1f}%")
        print(f"平均收益: {np.mean(profits):.2f}%")
        print(f"总收益: {sum(profits):.2f}%")

        print("\n交易详情:")
        for r in results:
            print(f"  {r['date']} {r['stock']}: {r['profit']:.2f}%")
    else:
        print("未找到交易机会")

    print("\n测试完成")

except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()
