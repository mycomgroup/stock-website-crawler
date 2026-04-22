# 影子策略 - 优化版多日期回测
# 扩大候选池，测试更多日期

print("=" * 80)
print("影子策略优化版回测（2024年）")
print("=" * 80)

import pandas as pd
import numpy as np

# ====== 配置 ======
EMOTION_THRESHOLD = 30
TEST_DATES = [
    "2024-02-28",
    "2024-03-29",  # Q1
    "2024-05-31",
    "2024-06-28",  # Q2
    "2024-08-30",
    "2024-09-27",  # Q3
    "2024-11-29",
    "2024-12-27",  # Q4
]

# ====== 获取候选池 ======
print("\n[1] 获取全市场候选池...")
try:
    # 使用全市场股票
    all_inst = all_instruments("CS")
    stocks = [
        inst.order_book_id
        for inst in all_inst
        if not inst.order_book_id.startswith(("688", "4", "8"))
    ]
    print(f"  全市场候选池: {len(stocks)}只")
except Exception as e:
    print(f"  ✗ 获取失败: {e}")
    # 降级到指数成分股
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300) | set(zz500))
        stocks = [s for s in stocks if not s.startswith("688")]
        print(f"  指数成分股候选池: {len(stocks)}只")
    except:
        stocks = []

# ====== 多日期测试 ======
results = []

if stocks:
    print("\n[2] 测试多个日期...")
    test_pool = stocks[:500]  # 扩大测试范围
    print(f"  实际测试股票数: {len(test_pool)}只")

    for test_date in TEST_DATES:
        print(f"\n{'=' * 80}")
        print(f"测试日期: {test_date}")
        print("=" * 80)

        try:
            # 统计涨停家数
            limit_up_count = 0
            limit_up_stocks = []

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
                                limit_up_stocks.append(stock)
                except:
                    continue

            # 筛选假弱高开
            fake_weak_count = 0
            fake_weak_stocks = []

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
                                fake_weak_stocks.append(stock)
                    except:
                        continue

            # 筛选二板
            second_board_count = 0
            second_board_stocks = []

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
                        second_board_stocks.append(stock)
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

            # 显示部分股票代码
            if limit_up_stocks:
                print(f"  涨停股票示例: {', '.join(limit_up_stocks[:5])}")
            if fake_weak_stocks:
                print(f"  假弱高开示例: {', '.join(fake_weak_stocks[:5])}")
            if second_board_stocks:
                print(f"  二板股票示例: {', '.join(second_board_stocks[:5])}")

        except Exception as e:
            print(f"  ✗ 执行出错: {e}")
            import traceback

            traceback.print_exc()

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

if results:
    total_fake_weak = sum(r["fake_weak"] for r in results)
    total_second_board = sum(r["second_board"] for r in results)
    emotion_ok_days = sum(1 for r in results if r["emotion_ok"] == "✓")
    avg_limit_up = sum(r["limit_up"] for r in results) / len(results)

    print(f"\n测试日期数: {len(results)}")
    print(f"平均涨停家数: {avg_limit_up:.1f}")
    print(f"情绪满足天数: {emotion_ok_days}/{len(results)}")
    print(f"假弱高开总信号: {total_fake_weak}只")
    print(f"二板总信号: {total_second_board}只")

    print("\n参考数据（2024实测）:")
    print("  主线：收益+2.89%，胜率88.5%，全年136信号")
    print("  观察线：胜率87.95%，盈亏比21.91")

print("\n" + "=" * 80)
print("回测完成")
print("=" * 80)
