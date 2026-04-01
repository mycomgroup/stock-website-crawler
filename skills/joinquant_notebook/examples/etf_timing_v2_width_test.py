#!/usr/bin/env python3
"""ETF 择时 V2 - 市场宽度信号测试（Notebook 版本）"""

print("=" * 70)
print("ETF 择时 V2 - 市场宽度信号测试")
print("=" * 70)

try:
    from jqdata import *
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta

    # 配置
    end_date = "2025-12-31"
    start_date = "2020-01-01"
    BENCHMARK_INDEX = "000300.XSHG"

    print(f"\n回测区间: {start_date} ~ {end_date}")
    print(f"基准指数: {BENCHMARK_INDEX}")

    # 获取沪深300成分股
    print("\n【1】获取沪深300成分股...")
    hs300_stocks = get_index_stocks(BENCHMARK_INDEX, date=end_date)
    print(f"  成分股数量: {len(hs300_stocks)}")

    # 获取交易日
    print("\n【2】获取交易日...")
    trade_days = get_trade_days(start_date=start_date, end_date=end_date)
    print(f"  交易日数量: {len(trade_days)}")

    # 获取价格数据（分批次避免超时）
    print("\n【3】获取价格数据...")
    print("  正在获取价格数据（可能需要1-2分钟）...")

    # 限制股票数量以加快测试
    test_stocks = hs300_stocks[:50]  # 先用前50只测试
    print(f"  测试使用股票数: {len(test_stocks)} (前50只)")

    all_prices = get_price(
        test_stocks,
        start_date=start_date,
        end_date=end_date,
        fields=["close"],
        panel=False,
    )

    # 转换为 pivot 表
    close_pivot = all_prices.pivot(index="time", columns="code", values="close")
    print(f"  价格数据维度: {close_pivot.shape}")

    # 计算 MA20
    print("\n【4】计算市场宽度...")
    ma20 = close_pivot.rolling(20).mean()

    # 计算市场宽度：C > MA20 的股票占比
    market_width = (close_pivot > ma20).sum(axis=1) / len(test_stocks)
    market_width = market_width.dropna()

    print(f"  市场宽度数据量: {len(market_width)}")
    print(f"\n  市场宽度统计:")
    print(f"    最新值: {market_width.iloc[-1]:.2%}")
    print(f"    均值: {market_width.mean():.2%}")
    print(f"    中位数: {market_width.median():.2%}")
    print(f"    最小值: {market_width.min():.2%}")
    print(f"    最大值: {market_width.max():.2%}")

    # 测试不同阈值
    print(f"\n【5】不同阈值下的信号统计:")
    thresholds = [0.20, 0.25, 0.30, 0.35, 0.40, 0.50]
    for thresh in thresholds:
        full_ratio = (market_width >= thresh).sum() / len(market_width)
        empty_ratio = (market_width < thresh).sum() / len(market_width)
        print(f"    阈值 {thresh:.0%}: 满仓 {full_ratio:.1%}, 空仓 {empty_ratio:.1%}")

    # 分级仓位统计
    print(f"\n【6】分级仓位统计:")
    full_pos = (market_width >= 0.5).sum() / len(market_width)
    half_pos = ((market_width >= 0.3) & (market_width < 0.5)).sum() / len(market_width)
    empty_pos = (market_width < 0.3).sum() / len(market_width)
    print(f"    满仓 (>=0.5): {full_pos:.1%}")
    print(f"    半仓 (0.3-0.5): {half_pos:.1%}")
    print(f"    空仓 (<0.3): {empty_pos:.1%}")

    # 当前信号
    print(f"\n【7】当前市场信号 ({market_width.index[-1].date()}):")
    latest_width = market_width.iloc[-1]
    print(f"    市场宽度: {latest_width:.2%}")
    if latest_width >= 0.5:
        print(f"    信号: 满仓")
    elif latest_width >= 0.3:
        print(f"    信号: 半仓")
    else:
        print(f"    信号: 空仓")

    # 最近5天
    print(f"\n【8】最近5天市场宽度:")
    for date, width in market_width.tail(5).items():
        signal = "满仓" if width >= 0.5 else ("半仓" if width >= 0.3 else "空仓")
        print(f"    {date.date()}: {width:.2%} ({signal})")

    print("\n" + "=" * 70)
    print("测试完成!")
    print("=" * 70)

except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()
