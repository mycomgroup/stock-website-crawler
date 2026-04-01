"""
RFScore7 + PB 简化测试 - 米筐 Notebook 版本

先测试 API 是否正常工作
"""

import numpy as np
import pandas as pd
from datetime import datetime

print("=" * 70)
print("RFScore7 + PB API 测试 (米筐)")
print("运行时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 70)

# 测试 1: 获取指数成分股
print("\n【测试1】获取指数成分股")
try:
    hs300 = index_components("000300.XSHG")
    print(f"  沪深300成分股数量: {len(hs300)}")
    print(f"  示例: {hs300[:5]}")
except Exception as e:
    print(f"  错误: {e}")

# 测试 2: 获取历史数据
print("\n【测试2】获取历史数据")
try:
    stock = hs300[0] if hs300 else "000001.XSHE"
    bars = history_bars(stock, 20, "1d", ["close", "volume"], include_now=True)
    if bars is not None:
        print(f"  {stock} 最近5天数据:")
        for i, bar in enumerate(bars[-5:]):
            print(
                f"    Day {i + 1}: close={bar['close']:.2f}, volume={bar['volume']:.0f}"
            )
    else:
        print("  无数据")
except Exception as e:
    print(f"  错误: {e}")

# 测试 3: 获取财务因子
print("\n【测试3】获取财务因子 (get_fundamentals)")
try:
    test_stocks = hs300[:5] if hs300 else ["000001.XSHE"]

    for stock in test_stocks:
        try:
            # 获取 PE/PB
            pe_data = get_fundamentals(
                query(
                    fundamentals.eod_derivative_indicator.pe_ratio,
                    fundamentals.eod_derivative_indicator.pb_ratio,
                ).filter(fundamentals.stockcode == stock),
                "2025-03-28",
            )
            if pe_data is not None and not pe_data.empty:
                pe = (
                    pe_data["pe_ratio"].iloc[0]
                    if "pe_ratio" in pe_data.columns
                    else "N/A"
                )
                pb = (
                    pe_data["pb_ratio"].iloc[0]
                    if "pb_ratio" in pe_data.columns
                    else "N/A"
                )
                print(f"  {stock}: PE={pe}, PB={pb}")
            else:
                print(f"  {stock}: 无数据")
        except Exception as e:
            print(f"  {stock}: 错误 - {e}")
except Exception as e:
    print(f"  错误: {e}")

# 测试 4: 获取 ROE/ROA
print("\n【测试4】获取 ROE/ROA (get_fundamentals)")
try:
    for stock in test_stocks[:2]:
        try:
            roe_data = get_fundamentals(
                query(
                    fundamentals.financial_indicator.roe,
                    fundamentals.financial_indicator.roa,
                ).filter(fundamentals.stockcode == stock),
                "2025-03-28",
            )
            if roe_data is not None and not roe_data.empty:
                roe = roe_data["roe"].iloc[0] if "roe" in roe_data.columns else "N/A"
                roa = roe_data["roa"].iloc[0] if "roa" in roe_data.columns else "N/A"
                print(f"  {stock}: ROE={roe}, ROA={roa}")
            else:
                print(f"  {stock}: 无数据")
        except Exception as e:
            print(f"  {stock}: 错误 - {e}")
except Exception as e:
    print(f"  错误: {e}")

# 测试 5: 计算市场宽度
print("\n【测试5】计算市场宽度")
try:
    test_count = 30
    above_ma20 = 0
    valid = 0

    for stock in hs300[:test_count]:
        try:
            bars = history_bars(stock, 20, "1d", "close", include_now=True)
            if bars is not None and len(bars) >= 20:
                ma20 = np.mean(bars)
                if bars[-1] > ma20:
                    above_ma20 += 1
                valid += 1
        except:
            continue

    breadth = above_ma20 / valid if valid > 0 else 0.5
    print(f"  测试股票数: {valid}")
    print(f"  MA20上方: {above_ma20}")
    print(f"  市场宽度: {breadth:.2%}")
except Exception as e:
    print(f"  错误: {e}")

# 测试 6: 沪深300趋势
print("\n【测试6】沪深300趋势")
try:
    idx_bars = history_bars("000300.XSHG", 20, "1d", "close", include_now=True)
    if idx_bars is not None and len(idx_bars) >= 20:
        ma20 = np.mean(idx_bars)
        current = idx_bars[-1]
        trend = "向上" if current > ma20 else "向下"
        print(f"  当前价: {current:.2f}")
        print(f"  MA20: {ma20:.2f}")
        print(f"  趋势: {trend}")
    else:
        print("  数据不足")
except Exception as e:
    print(f"  错误: {e}")

print("\n" + "=" * 70)
print("测试完成!")
print("=" * 70)
