#!/usr/bin/env python3
"""ETF 择时 V2 - 快速验证版"""

print("=" * 70)
print("ETF 择时 V2 - 快速验证")
print("=" * 70)

try:
    from jqdata import *
    import pandas as pd
    import numpy as np

    # 配置
    end_date = "2025-12-31"
    start_date = "2022-01-01"  # 缩短回测期

    ETF_POOL_A = {
        "沪深300ETF": "510300.XSHG",
        "中证500ETF": "510500.XSHG",
        "创业板ETF": "159915.XSHE",
    }

    print(f"\n【配置】")
    print(f"  ETF池: {len(ETF_POOL_A)} 只")
    print(f"  回测期: {start_date} ~ {end_date}")

    # 获取市场宽度
    print(f"\n【1】计算市场宽度...")
    hs300_stocks = get_index_stocks("000300.XSHG", date=end_date)[:50]

    prices = get_price(
        hs300_stocks,
        start_date=start_date,
        end_date=end_date,
        fields=["close"],
        panel=False,
    )
    close_pivot = prices.pivot(index="time", columns="code", values="close")
    ma20 = close_pivot.rolling(20).mean()
    market_width = (close_pivot > ma20).sum(axis=1) / len(hs300_stocks)
    market_width = market_width.dropna()

    print(f"  数据量: {len(market_width)}")
    print(f"  均值: {market_width.mean():.2%}")

    # 生成不同信号
    signals = pd.DataFrame(index=market_width.index)
    signals["width"] = market_width
    signals["binary_0.4"] = (market_width >= 0.4).astype(float)
    signals["binary_0.3"] = (market_width >= 0.3).astype(float)
    signals["tiered"] = market_width.apply(
        lambda x: 1.0 if x >= 0.5 else (0.5 if x >= 0.3 else 0.0)
    )

    print(f"\n【2】信号统计:")
    print(
        f"  二元0.4: 平均仓位 {signals['binary_0.4'].mean():.1%} (空仓率 {(signals['binary_0.4'] == 0).sum() / len(signals):.1%})"
    )
    print(
        f"  二元0.3: 平均仓位 {signals['binary_0.3'].mean():.1%} (空仓率 {(signals['binary_0.3'] == 0).sum() / len(signals):.1%})"
    )
    print(f"  分级仓位: 平均仓位 {signals['tiered'].mean():.1%}")
    print(f"    - 满仓: {(signals['tiered'] == 1.0).sum() / len(signals):.1%}")
    print(f"    - 半仓: {(signals['tiered'] == 0.5).sum() / len(signals):.1%}")
    print(f"    - 空仓: {(signals['tiered'] == 0.0).sum() / len(signals):.1%}")

    # 当前信号
    latest = signals.iloc[-1]
    print(f"\n【3】当前信号 ({signals.index[-1].date()}):")
    print(f"  市场宽度: {latest['width']:.1%}")
    print(f"  二元0.4: {latest['binary_0.4']:.0%}")
    print(f"  二元0.3: {latest['binary_0.3']:.0%}")
    print(f"  分级: {latest['tiered']:.0%}")

    if latest["width"] >= 0.5:
        print(f"\n  建议: 满仓")
    elif latest["width"] >= 0.3:
        print(f"\n  建议: 半仓")
    else:
        print(f"\n  建议: 空仓")

    print(f"\n" + "=" * 70)
    print("验证完成!")
    print("=" * 70)

except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()
