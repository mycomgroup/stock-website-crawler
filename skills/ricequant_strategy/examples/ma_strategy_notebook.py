"""
移动平均策略 - Notebook 版本

用于在 RiceQuant Notebook 中逐步验证策略逻辑
"""

import numpy as np

print("=== 双均线策略 Notebook 测试 ===")

try:
    stock = "000001.XSHE"
    print(f"测试股票: {stock}")

    bars = history_bars(stock, 30, "1d", ["close", "volume"], include_now=True)

    if bars is not None and len(bars) >= 20:
        close = bars["close"]
        volume = bars["volume"]

        short_window = 5
        long_window = 20

        short_ma = np.mean(close[-short_window:])
        long_ma = np.mean(close[-long_window:])

        print(f"最近收盘价: {close[-1]:.2f}")
        print(f"短期均线({short_window}日): {short_ma:.2f}")
        print(f"长期均线({long_window}日): {long_ma:.2f}")

        if short_ma > long_ma:
            print("\n>>> 金叉信号: 短期均线 > 长期均线，建议买入")
        else:
            print("\n>>> 无金叉信号: 短期均线 <= 长期均线")

        print("\n策略逻辑验证成功!")

    else:
        print("无法获取足够的历史数据")

except Exception as e:
    print(f"策略测试错误: {e}")
    print("可能需要在 RiceQuant Notebook 平台上运行")

print("\n=== 测试完成 ===")
