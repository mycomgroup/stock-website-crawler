# 影子策略 - 多日期回测
# 测试2024年不同时期的市场状态

print("=" * 80)
print("影子策略多日期回测（2024年）")
print("=" * 80)

import pandas as pd
import numpy as np

# ====== 配置 ======
MARKET_CAP_MIN = 50
MARKET_CAP_MAX = 150
EMOTION_THRESHOLD = 30
TEST_DATES = ["2024-03-31", "2024-06-30", "2024-09-30", "2024-12-31"]

# ====== 获取候选池 ======
print("\n[1] 获取候选池...")
try:
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")
    all_stocks = list(set(hs300) | set(zz500))
    stocks = [s for s in all_stocks if not s.startswith("688")]
    print(f"  候选池数量: {len(stocks)}")
except Exception as e:
    print(f"  ✗ 获取失败: {e}")
    stocks = []

# ====== 多日期测试 ======
results = []

if stocks:
    print("\n[2] 测试多个日期...")

    for test_date in TEST_DATES:
        print(f"\n{'=' * 80}")
        print(f"测试日期: {test_date}")
        print("=" * 80)

        try:
            # 统计涨停家数
            limit_up_count = 0
            test_pool = stocks[:200]

            for stock in test_pool:
                try:
                    bars = history_bars(stock, 2, "1d", "close", end_date=test_date)
                    if bars is not None and len(bars) >= 2:
                        prev_close = bars[-2]
                        curr_close = bars[-1]
                        if prev_close > 0:
                            pct = (curr_close - prev_close) / prev_close
                            if pct >= 0.095:
                                limit_up_count += 1
                except:
                    continue

            # 筛选假弱高开
            fake_weak_count = 0
            if limit_up_count >= EMOTION_THRESHOLD:
                for stock in test_pool:
                    try:
                        bars = history_bars(
                            stock,
                            2,
                            "1d",
                            ["close", "open", "high"],
                            end_date=test_date,
                        )
                        if bars is None or len(bars) < 2:
                            continue

                        prev_close = bars[-2]["close"]
                        open_price = bars[-1]["open"]
                        high_price = bars[-1]["high"]

                        if prev_close > 0:
                            open_change = (open_price - prev_close) / prev_close
                            if 0.001 < open_change < 0.03 and high_price > open_price:
                                fake_weak_count += 1
                    except:
                        continue

            # 筛选二板
            second_board_count = 0
            for stock in test_pool:
                try:
                    bars = history_bars(stock, 6, "1d", "close", end_date=test_date)
                    if bars is None or len(bars) < 6:
                        continue

                    boards = 0
                    for i in range(len(bars) - 1):
                        close = bars[i]
                        next_close = bars[i + 1]
                        if close > 0:
                            pct = (next_close - close) / close
                            if pct >= 0.095:
                                boards += 1
                            else:
                                break

                    if boards == 2:
                        second_board_count += 1
                except:
                    continue

            # 记录结果
            result = {
                "date": test_date,
                "limit_up": limit_up_count,
                "emotion_ok": "✓" if limit_up_count >= EMOTION_THRESHOLD else "✗",
                "fake_weak": fake_weak_count,
                "second_board": second_board_count,
            }
            results.append(result)

            print(f"  涨停家数: {limit_up_count}")
            print(f"  情绪状态: {result['emotion_ok']}")
            print(f"  假弱高开: {fake_weak_count}只")
            print(f"  二板信号: {second_board_count}只")

        except Exception as e:
            print(f"  ✗ 执行出错: {e}")
            results.append(
                {
                    "date": test_date,
                    "limit_up": 0,
                    "emotion_ok": "✗",
                    "fake_weak": 0,
                    "second_board": 0,
                    "error": str(e),
                }
            )

# ====== 汇总结果 ======
print("\n" + "=" * 80)
print("多日期回测汇总")
print("=" * 80)

print("\n日期         | 涨停数 | 情绪 | 假弱高开 | 二板")
print("-" * 60)
for r in results:
    print(
        f"{r['date']} | {r['limit_up']:6d} | {r['emotion_ok']:4s} | {r['fake_weak']:8d} | {r['second_board']:4d}"
    )

print("\n" + "=" * 80)
print("总结")
print("=" * 80)

total_fake_weak = sum(r["fake_weak"] for r in results)
total_second_board = sum(r["second_board"] for r in results)
emotion_ok_days = sum(1 for r in results if r["emotion_ok"] == "✓")

print(f"\n测试日期数: {len(results)}")
print(f"情绪满足天数: {emotion_ok_days}/{len(results)}")
print(f"假弱高开总信号: {total_fake_weak}只")
print(f"二板总信号: {total_second_board}只")

print("\n参考数据（2024实测）:")
print("  主线：收益+2.89%，胜率88.5%")
print("  观察线：胜率87.95%，盈亏比21.91")

print("\n" + "=" * 80)
print("回测完成")
print("=" * 80)
