"""
二板策略简化验证 - 基于2024年数据
只验证2024年Q1，快速出结果
"""

print("=" * 80)
print("二板策略简化验证 - 2024年Q1")
print("=" * 80)

import numpy as np


# 简化版二板检测
def find_2b_stocks_simple(date):
    """找二板股票 - 简化版"""
    all_inst = all_instruments("CS")
    stock_list = list(all_inst["order_book_id"])

    # 过滤
    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    results = []
    for stock in stocks[:500]:  # 只检查前500只
        try:
            bars = history_bars(stock, 2, "1d", ["close", "limit_up"], end_date=date)
            if bars is None or len(bars) < 2:
                continue

            # 昨天涨停？
            if bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99:
                # 前天涨停？
                if bars[-2]["close"] >= bars[-2]["limit_up"] * 0.99:
                    # 连续2天涨停 = 二板！
                    results.append((stock, bars[-1]["limit_up"]))
        except:
            pass

    return results


# 测试参数
start_date = "2024-01-01"
end_date = "2024-03-31"

print(f"\n测试区间: {start_date} ~ {end_date}")

# 获取交易日
try:
    trading_days = get_trading_dates(start_date, end_date)
    print(f"交易日数: {len(trading_days)}")
except:
    print("无法获取交易日")
    trading_days = []

# 统计
total_2b = 0
trades = []
profits = []

for i, date in enumerate(trading_days[:-1]):
    if i % 10 == 0:
        print(f"处理: {date}")

    # 找二板
    candidates = find_2b_stocks_simple(date)
    total_2b += len(candidates)

    if not candidates:
        continue

    # 取第一只
    stock, limit_up = candidates[0]

    # 次日数据
    next_date = trading_days[i + 1]
    next_bars = history_bars(stock, 1, "1d", ["open", "close"], end_date=next_date)

    if next_bars is None or len(next_bars) == 0:
        continue

    open_price = next_bars[-1]["open"]
    close_price = next_bars[-1]["close"]

    # 非涨停开盘
    if open_price >= limit_up * 0.99:
        continue

    # 计算收益
    buy_price = open_price * 1.005
    profit = (close_price / buy_price - 1) * 100

    trades.append(
        {
            "date": str(date),
            "stock": stock,
            "open": open_price,
            "close": close_price,
            "profit": profit,
        }
    )
    profits.append(profit)

print(f"\n{'=' * 60}")
print("统计结果")
print(f"{'=' * 60}")
print(f"二板信号总数: {total_2b}")
print(f"实际交易数: {len(trades)}")

if trades:
    wins = [t for t in trades if t["profit"] > 0]
    print(f"胜率: {len(wins) / len(trades) * 100:.2f}%")
    print(f"平均收益: {np.mean(profits):.2f}%")
    print(f"累计收益: {sum(profits):.2f}%")

    print(f"\n前5笔交易:")
    for t in trades[:5]:
        print(f"  {t['date']} {t['stock']}: {t['profit']:.2f}%")
else:
    print("无交易")

print(f"\n{'=' * 60}")
print("验证完成")
print(f"{'=' * 60}")
