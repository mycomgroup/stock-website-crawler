# 影子策略 Notebook 回测 - 主线假弱高开
# 测试时间段：2024年全年

print("=" * 80)
print("影子策略回测 - 主线假弱高开（2024年）")
print("=" * 80)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ====== 1. 参数配置 ======
print("\n[1] 参数配置...")
MARKET_CAP_MIN = 50  # 亿元
MARKET_CAP_MAX = 150  # 亿元
EMOTION_THRESHOLD = 30  # 涨停家数阈值
OPEN_CHANGE_MIN = 0.001  # 0.1%
OPEN_CHANGE_MAX = 0.03  # 3%
TEST_START = "2024-01-01"
TEST_END = "2024-12-31"

print(f"  市值范围: {MARKET_CAP_MIN}-{MARKET_CAP_MAX}亿")
print(f"  情绪阈值: 涨停家数>={EMOTION_THRESHOLD}")
print(f"  开盘涨幅: {OPEN_CHANGE_MIN * 100:.1f}%-{OPEN_CHANGE_MAX * 100:.0f}%")
print(f"  测试时间: {TEST_START} 至 {TEST_END}")

# ====== 2. 获取候选池 ======
print("\n[2] 获取候选池（沪深300+中证500）...")
try:
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")
    all_stocks = list(set(hs300) | set(zz500))

    # 排除科创板
    stocks = [s for s in all_stocks if not s.startswith("688")]

    print(f"  ✓ 候选池数量: {len(stocks)}")
except Exception as e:
    print(f"  ✗ 获取失败: {e}")
    stocks = []

# ====== 3. 测试单个交易日 ======
print("\n[3] 测试最近一个交易日...")

if stocks:
    try:
        # 获取最近交易日
        dates = get_trading_dates(TEST_START, TEST_END)
        test_date = dates[-1] if dates else None

        if test_date:
            print(f"  测试日期: {test_date}")

            # 3.1 统计涨停家数
            print("\n  [3.1] 统计涨停家数...")
            limit_up_count = 0
            test_pool = stocks[:200]  # 限制数量

            for stock in test_pool:
                try:
                    bars = history_bars(stock, 2, "1d", "close")
                    if bars is not None and len(bars) >= 2:
                        prev_close = bars[-2]
                        curr_close = bars[-1]
                        if prev_close > 0:
                            pct = (curr_close - prev_close) / prev_close
                            if pct >= 0.095:
                                limit_up_count += 1
                except:
                    continue

            print(f"       涨停家数: {limit_up_count}")
            print(
                f"       情绪状态: {'✓ 满足' if limit_up_count >= EMOTION_THRESHOLD else '✗ 不满足'}"
            )

            # 3.2 筛选假弱高开
            print("\n  [3.2] 筛选假弱高开股票...")
            fake_weak_stocks = []

            if limit_up_count >= EMOTION_THRESHOLD:
                for stock in test_pool:
                    try:
                        bars = history_bars(stock, 2, "1d", ["close", "open", "high"])
                        if bars is None or len(bars) < 2:
                            continue

                        prev_close = bars[-2]["close"]
                        open_price = bars[-1]["open"]
                        high_price = bars[-1]["high"]

                        if prev_close > 0:
                            open_change = (open_price - prev_close) / prev_close

                            # 假弱高开条件
                            if OPEN_CHANGE_MIN < open_change < OPEN_CHANGE_MAX:
                                if high_price > open_price:
                                    fake_weak_stocks.append(
                                        {
                                            "stock": stock,
                                            "open_change": open_change,
                                            "open_price": open_price,
                                            "high_price": high_price,
                                        }
                                    )
                    except:
                        continue

                print(f"       假弱高开股票: {len(fake_weak_stocks)}只")

                if fake_weak_stocks:
                    print("\n       前10只股票:")
                    for i, item in enumerate(fake_weak_stocks[:10], 1):
                        print(
                            f"         {i}. {item['stock']}: 开盘涨幅 {item['open_change'] * 100:.2f}%"
                        )
            else:
                print("       情绪不足，不筛选")

            # ====== 4. 汇总结果 ======
            print("\n" + "=" * 80)
            print("回测结果汇总")
            print("=" * 80)
            print(f"\n测试日期: {test_date}")
            print(f"候选池数量: {len(test_pool)}")
            print(f"涨停家数: {limit_up_count}")
            print(
                f"情绪状态: {'✓ 满足' if limit_up_count >= EMOTION_THRESHOLD else '✗ 不满足'}"
            )
            print(f"假弱高开信号: {len(fake_weak_stocks)}只")

            if fake_weak_stocks:
                print("\n操作建议:")
                print("  ✓ 可以考虑买入")
                print("  ⚠️  单票上限10万，总仓上限30万")
                print("  ⚠️  次日冲高+3%止盈，否则尾盘卖出")
            else:
                print("\n操作建议:")
                print("  ✗ 无交易信号，观望")

        else:
            print("  ✗ 无法获取交易日")

    except Exception as e:
        print(f"  ✗ 执行出错: {e}")
        import traceback

        traceback.print_exc()

else:
    print("  ✗ 无候选池数据")

print("\n" + "=" * 80)
print("回测完成")
print("=" * 80)
