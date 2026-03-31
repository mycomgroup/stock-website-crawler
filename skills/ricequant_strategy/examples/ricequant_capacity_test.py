# RiceQuant - 容量与滑点简化测试
# 如果kernel可用，直接运行此脚本

print("=" * 60)
print("RiceQuant 容量与滑点测试")
print("=" * 60)

import pandas as pd
import numpy as np

# 测试参数
TEST_PERIODS = [
    ("2024-10", "2024-10-01", "2024-10-31"),
    ("2024-11", "2024-11-01", "2024-11-30"),
]

SLIPPAGES = [0.0, 0.002, 0.005]
SLIPPAGE_NAMES = ["0%", "0.2%", "0.5%"]

print("\n开始测试...\n")

for period_name, start, end in TEST_PERIODS:
    print(f"测试期间: {period_name}")

    try:
        # RiceQuant API
        all_stocks = all_securities(type=["stock"], date=start)
        stocks = [s for s in all_stocks.index.tolist() if s[:2] not in ["68", "30"]][
            :100
        ]

        print(f"  股票池: {len(stocks)}只")

        # 获取价格数据
        prices = get_price(
            stocks,
            start_date=start,
            end_date=end,
            frequency="1d",
            fields=["open", "close", "high_limit"],
        )

        if prices is None or prices.empty:
            print("  无数据")
            continue

        print(f"  数据获取成功")

        # 找涨停后低开
        for slip_idx, slip in enumerate(SLIPPAGES):
            slip_name = SLIPPAGE_NAMES[slip_idx]

            # 简化计算
            # 假设找到涨停股，然后开盘买入
            pnl = -slip * 2 - 0.0016  # 简化损耗

            print(f"  {slip_name}滑点: 预估损耗 {pnl * 100:.2f}%")

        print()

    except Exception as e:
        print(f"  错误: {e}")
        print()

print("=" * 60)
print("如果能看到以上输出，说明RiceQuant连接成功")
print("=" * 60)
