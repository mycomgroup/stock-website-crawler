"""
二板策略调试版 - 添加详细日志
"""

print("=" * 80)
print("二板策略调试 - RiceQuant Notebook")
print("=" * 80)

import numpy as np

# 测试单日，看看数据
print("\n=== 测试单日数据 ===")

test_date = "2021-01-15"
print(f"测试日期: {test_date}")

# 获取所有股票
all_inst = all_instruments("CS")
stock_list = all_inst["order_book_id"].tolist()
stocks = [
    s
    for s in stock_list
    if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
]
print(f"股票池数量: {len(stocks)}")

# 找涨停股票
zt_count = 0
zt_stocks = []
for stock in stocks[:500]:
    try:
        bars = history_bars(stock, 1, "1d", ["close", "limit_up"], end_date=test_date)
        if bars is not None and len(bars) > 0:
            if bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99:
                zt_stocks.append(stock)
                zt_count += 1
    except:
        pass

print(f"涨停股票数: {zt_count}")
print(f"涨停股票示例: {zt_stocks[:5]}")

# 找二板
second_board_count = 0
for stock in zt_stocks[:20]:
    try:
        bars = history_bars(stock, 3, "1d", ["close", "limit_up"], end_date=test_date)
        if bars is None or len(bars) < 3:
            continue

        # 昨天（-1）涨停
        if bars[-1]["close"] < bars[-1]["limit_up"] * 0.99:
            continue
        # 前天（-2）涨停
        if bars[-2]["close"] < bars[-2]["limit_up"] * 0.99:
            continue
        # 大前天（-3）不涨停
        if bars[-3]["close"] >= bars[-3]["limit_up"] * 0.99:
            continue

        print(f"  二板: {stock}")
        print(
            f"    大前天收盘: {bars[-3]['close']:.2f}, 涨停价: {bars[-3]['limit_up']:.2f}"
        )
        print(
            f"    前天收盘: {bars[-2]['close']:.2f}, 涨停价: {bars[-2]['limit_up']:.2f}"
        )
        print(
            f"    昨天收盘: {bars[-1]['close']:.2f}, 涨停价: {bars[-1]['limit_up']:.2f}"
        )
        second_board_count += 1

    except Exception as e:
        pass

print(f"\n二板股票数: {second_board_count}")

# 如果找到了二板，继续测试买入条件
if second_board_count > 0:
    print("\n=== 测试买入条件 ===")
    # 选第一只二板股票
    for stock in zt_stocks:
        try:
            bars = history_bars(
                stock, 3, "1d", ["close", "limit_up"], end_date=test_date
            )
            if bars is None or len(bars) < 3:
                continue
            if bars[-1]["close"] < bars[-1]["limit_up"] * 0.99:
                continue
            if bars[-2]["close"] < bars[-2]["limit_up"] * 0.99:
                continue
            if bars[-3]["close"] >= bars[-3]["limit_up"] * 0.99:
                continue

            limit_up = bars[-1]["limit_up"]

            # 次日数据
            next_date = "2021-01-18"  # 下一个交易日
            next_bars = history_bars(
                stock, 1, "1d", ["open", "close"], end_date=next_date
            )
            if next_bars is not None and len(next_bars) > 0:
                open_price = next_bars[-1]["open"]
                close_price = next_bars[-1]["close"]

                print(f"股票: {stock}")
                print(f"  涨停价: {limit_up:.2f}")
                print(f"  次日开盘: {open_price:.2f}")
                print(f"  次日收盘: {close_price:.2f}")
                print(f"  是否涨停开盘: {open_price >= limit_up * 0.99}")

                if open_price < limit_up * 0.99:
                    buy_price = open_price * 1.005
                    profit = (close_price / buy_price - 1) * 100
                    print(f"  可买入! 预期收益: {profit:.2f}%")
            break
        except:
            pass

print("\n" + "=" * 80)
print("调试完成")
print("=" * 80)
