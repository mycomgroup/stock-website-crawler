"""
二板接力 2022年Q1测试 - RiceQuant Notebook格式
测试范围：2022-01-01 至 2022-03-31
"""

print("=" * 80)
print("二板接力 2022年Q1测试")
print("=" * 80)

try:
    import pandas as pd
    import numpy as np

    # RiceQuant API
    from rqalpha.apis import *

    print("✓ 导入依赖成功")

    # 测试配置
    year = 2022
    quarter = 1
    start_date = f"{year}-01-01"
    end_date = f"{year}-03-31"

    print(f"\n测试范围: {start_date} 至 {end_date}")

    # 获取交易日
    all_dates = get_trading_dates(start_date, end_date)
    print(f"交易日数: {len(all_dates)}")

    signals = []

    for i in range(2, min(len(all_dates), 50)):  # 限制前50天，防止超时
        prev_prev = all_dates[i - 2].strftime("%Y-%m-%d")
        prev = all_dates[i - 1].strftime("%Y-%m-%d")
        curr = all_dates[i].strftime("%Y-%m-%d")

        if i % 5 == 0:
            print(f"处理第{i}天: {prev} -> {curr}")

        try:
            # 获取所有股票
            all_stocks = all_instruments("CS", prev)
            all_stocks = [s.order_book_id for s in all_stocks]

            # 过滤科创板、北交所等
            all_stocks = [
                s
                for s in all_stocks
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ]

            if len(all_stocks) > 500:
                all_stocks = all_stocks[:500]

            # 获取涨停数据
            price_prev = history_bars(
                all_stocks, 1, "1d", "close,limit_up", prev, include_now=True
            )

            if not price_prev:
                continue

            # 找涨停股票
            zt_stocks = []
            for stock, bars in price_prev.items():
                if len(bars) > 0:
                    close = bars[0]["close"]
                    limit_up = bars[0]["limit_up"]
                    if abs(close - limit_up) / limit_up < 0.01:
                        zt_stocks.append(stock)

            zt_count = len(zt_stocks)
            if i % 5 == 0:
                print(f"  涨停数: {zt_count}")

            if zt_count < 10:
                continue

            # 获取前一日涨停数据
            price_pp = history_bars(
                zt_stocks, 1, "1d", "close,limit_up", prev_prev, include_now=True
            )

            if not price_pp:
                continue

            # 筛选二板候选
            for stock in zt_stocks[:30]:
                try:
                    # 前一日涨停价
                    prev_bars = price_prev.get(stock)
                    if not prev_bars or len(prev_bars) == 0:
                        continue

                    prev_limit = prev_bars[0]["limit_up"]

                    # 前前一日是否涨停
                    pp_bars = price_pp.get(stock)
                    if not pp_bars or len(pp_bars) == 0:
                        continue

                    pp_close = pp_bars[0]["close"]
                    pp_limit = pp_bars[0]["limit_up"]

                    if abs(pp_close - pp_limit) / pp_limit >= 0.01:
                        continue

                    # 当日数据
                    price_curr = history_bars(
                        stock, 1, "1d", "open,close,limit_up", curr, include_now=True
                    )

                    if not price_curr or len(price_curr) == 0:
                        continue

                    curr_bar = price_curr[0]
                    curr_open = curr_bar["open"]
                    curr_close = curr_bar["close"]
                    curr_limit = curr_bar["limit_up"]

                    # 涨停开盘则跳过
                    if abs(curr_open - curr_limit) / curr_limit < 0.01:
                        continue

                    # 计算收益
                    ret = (curr_close - curr_open) / curr_open * 100
                    signals.append(
                        {"date": curr, "stock": stock, "return": ret, "win": ret > 0}
                    )

                except Exception as e:
                    continue

        except Exception as e:
            continue

    # 统计结果
    print("\n" + "=" * 80)
    print("2022年Q1测试结果")
    print("=" * 80)

    if len(signals) > 0:
        df = pd.DataFrame(signals)
        print(f"信号数: {len(df)}")
        print(f"平均收益: {df['return'].mean():.2f}%")
        print(f"胜率: {df['win'].sum() / len(df) * 100:.1f}%")
        print(f"最大收益: {df['return'].max():.2f}%")
        print(f"最大亏损: {df['return'].min():.2f}%")
    else:
        print("无信号")

    print("\n✓ 2022年Q1测试完成")

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback

    traceback.print_exc()

print("=" * 80)
