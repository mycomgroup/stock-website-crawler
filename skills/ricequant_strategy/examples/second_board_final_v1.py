"""
二板策略最终修正版 - 使用正确的Timestamp索引
"""

print("=" * 80)
print("二板策略 - RiceQuant Notebook（最终修正版）")
print("=" * 80)

import pandas as pd
import numpy as np

# 测试日期
test_dates = ["2024-03-15", "2024-03-20", "2024-06-20", "2024-09-20"]
zt_threshold = 0.99

print(f"\n涨停判断阈值: ≥{zt_threshold}")
print(f"测试日期: {test_dates}")

results = {}

for test_date_str in test_dates:
    print(f"\n{'=' * 60}")
    print(f"测试日期: {test_date_str}")
    print(f"{'=' * 60}")

    test_date = pd.Timestamp(test_date_str)

    try:
        # 1. 检查交易日
        month_start = test_date_str[:7] + "-01"
        month_end = test_date_str[:7] + "-28"

        trading_days = get_trading_dates(month_start, month_end)
        dates_ts = [pd.Timestamp(str(d)[:10]) for d in trading_days]

        if test_date not in dates_ts:
            print(f"{test_date_str} 不是交易日，跳过")
            continue

        print(f"是交易日 ✓")

        # 2. 获取股票池
        all_inst = all_instruments("CS")
        stock_list = all_inst["order_book_id"].tolist()
        stocks = [
            s
            for s in stock_list
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        print(f"股票池: {len(stocks)}只，测试前300只")

        # 3. 找涨停股票（使用Timestamp）
        prices = get_price(
            stocks[:300],
            start_date=test_date_str,
            end_date=test_date_str,
            frequency="1d",
            fields=["close", "limit_up"],
        )

        if prices is None or prices.empty:
            print("无数据")
            continue

        print(f"获取价格数据成功")

        zt_stocks = []

        # 使用Timestamp作为索引键
        for stock in stocks[:300]:
            try:
                key = (stock, test_date)

                if key in prices.index:
                    close = prices.loc[key, "close"]
                    limit_up = prices.loc[key, "limit_up"]

                    if pd.notna(close) and pd.notna(limit_up) and limit_up > 0:
                        ratio = close / limit_up

                        if ratio >= zt_threshold:
                            zt_stocks.append(
                                {
                                    "stock": stock,
                                    "close": float(close),
                                    "limit": float(limit_up),
                                    "ratio": float(ratio),
                                }
                            )
            except Exception as e:
                pass

        print(f"涨停股票数: {len(zt_stocks)}")

        if len(zt_stocks) > 0:
            print(f"涨停示例:")
            for s in zt_stocks[:3]:
                print(
                    f"  {s['stock']}: 收盘{s['close']:.2f}, 涨停价{s['limit']:.2f}, 比值{s['ratio']:.4f}"
                )

            # 找二板
            if len(dates_ts) > 2:
                idx = dates_ts.index(test_date)

                if idx >= 2:
                    prev_date = dates_ts[idx - 1]
                    prev2_date = dates_ts[idx - 2]

                    print(f"\n找二板:")
                    print(f"  昨天: {prev_date}")
                    print(f"  前天: {prev2_date}")

                    zt_codes = [s["stock"] for s in zt_stocks]

                    prices_3d = get_price(
                        zt_codes,
                        start_date=str(prev2_date)[:10],
                        end_date=test_date_str,
                        frequency="1d",
                        fields=["close", "limit_up"],
                    )

                    if prices_3d is not None and not prices_3d.empty:
                        second_board = []

                        for stock in zt_codes:
                            try:
                                # 今天涨停
                                key_today = (stock, test_date)
                                if key_today not in prices_3d.index:
                                    continue

                                today_close = float(prices_3d.loc[key_today, "close"])
                                today_limit = float(
                                    prices_3d.loc[key_today, "limit_up"]
                                )

                                # 昨天涨停
                                key_prev = (stock, prev_date)
                                if key_prev not in prices_3d.index:
                                    continue

                                yesterday_close = float(
                                    prices_3d.loc[key_prev, "close"]
                                )
                                yesterday_limit = float(
                                    prices_3d.loc[key_prev, "limit_up"]
                                )

                                # 前天不涨停
                                key_prev2 = (stock, prev2_date)
                                if key_prev2 not in prices_3d.index:
                                    continue

                                prev2_close = float(prices_3d.loc[key_prev2, "close"])
                                prev2_limit = float(
                                    prices_3d.loc[key_prev2, "limit_up"]
                                )

                                # 判断
                                if today_close >= today_limit * zt_threshold:
                                    if (
                                        yesterday_close
                                        >= yesterday_limit * zt_threshold
                                    ):
                                        if prev2_close < prev2_limit * zt_threshold:
                                            second_board.append(
                                                {
                                                    "stock": stock,
                                                    "today_close": today_close,
                                                    "today_limit": today_limit,
                                                    "buy_price": today_limit,  # 用涨停价买入
                                                }
                                            )
                                            print(f"  找到二板: {stock}")

                            except Exception as e:
                                pass

                        results[test_date_str] = {
                            "zt_count": len(zt_stocks),
                            "sb_count": len(second_board),
                            "sb_examples": second_board[:3],
                        }

                        print(f"二板数: {len(second_board)}")

                        if len(second_board) > 0:
                            print(f"二板示例:")
                            for sb in second_board[:3]:
                                print(f"  {sb['stock']}: 涨停价{sb['buy_price']:.2f}")
        else:
            results[test_date_str] = {"zt_count": 0, "sb_count": 0}

    except Exception as e:
        print(f"错误: {e}")
        import traceback

        traceback.print_exc()

# 汇总
print(f"\n{'=' * 80}")
print("汇总结果")
print(f"{'=' * 80}")

total_zt = sum(r.get("zt_count", 0) for r in results.values())
total_sb = sum(r.get("sb_count", 0) for r in results.values())

print(f"涨停总数: {total_zt}")
print(f"二板总数: {total_sb}")

for date, r in results.items():
    print(f"{date}: 涨停{r['zt_count']}只, 二板{r['sb_count']}只")

print(f"\n结论:")
if total_zt > 0:
    print("  ✓ API正确，能找到涨停股票")
else:
    print("  ✗ 未找到涨停股票，可能需要更多日期测试")

if total_sb > 0:
    print("  ✓ 筛选逻辑正确，能找到二板股票")
else:
    print("  ✗ 未找到二板股票，可能筛选条件过严")

print("=" * 80)
