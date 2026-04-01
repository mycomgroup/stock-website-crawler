"""
二板策略调试 - 使用正确的 RiceQuant Notebook API
"""

print("=" * 80)
print("二板策略调试 - RiceQuant Notebook（正确API）")
print("=" * 80)

import pandas as pd
import numpy as np

# 测试日期
test_date = "2021-01-15"
print(f"\n测试日期: {test_date}")

# 1. 检查交易日
print("\n=== 1. 检查交易日 ===")
try:
    trading_days = get_trading_dates("2021-01-01", "2021-01-31")
    print(f"2021年1月交易日数: {len(trading_days)}")

    if test_date in [str(d)[:10] for d in trading_days]:
        print(f"{test_date} 是交易日 ✓")
    else:
        print(f"{test_date} 不是交易日 ✗")
        test_date = str(trading_days[10])[:10]
        print(f"改用: {test_date}")
except Exception as e:
    print(f"错误: {e}")

# 2. 检查股票池
print("\n=== 2. 检查股票池 ===")
try:
    all_stocks = all_securities(type=["stock"], date=test_date)
    print(f"股票总数: {len(all_stocks)}")
    print(f"前5只股票:")
    print(all_stocks.head())

    stock_list = all_stocks.index.tolist()
    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]
    print(f"过滤后股票数: {len(stocks)}")
except Exception as e:
    print(f"错误: {e}")

# 3. 检查单只股票价格数据
print("\n=== 3. 检查单只股票价格数据 ===")
test_stock = "000001.XSHE"
print(f"测试股票: {test_stock}")

try:
    prices = get_price(
        test_stock,
        start_date=test_date,
        end_date=test_date,
        frequency="1d",
        fields=["open", "close", "high", "low", "high_limit", "low_limit"],
    )

    if prices is not None and not prices.empty:
        print(f"价格数据:")
        print(prices)

        close = prices["close"].iloc[0]
        high_limit = prices["high_limit"].iloc[0]

        print(f"\n收盘价: {close:.2f}")
        print(f"涨停价: {high_limit:.2f}")
        print(f"比值: {close / high_limit:.4f}")
        print(f"是否涨停(≥0.995): {close >= high_limit * 0.995}")
    else:
        print("无数据")
except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

# 4. 批量获取涨停股票
print("\n=== 4. 批量获取涨停股票（检查500只） ===")
try:
    test_stocks = stocks[:500]

    prices = get_price(
        test_stocks,
        start_date=test_date,
        end_date=test_date,
        frequency="1d",
        fields=["close", "high_limit"],
    )

    if prices is not None and not prices.empty:
        print(f"获取价格数据成功: {len(prices)}只股票")

        # 找涨停
        zt_stocks = []
        for stock in test_stocks:
            try:
                if stock in prices.index:
                    close = prices.loc[stock, "close"]
                    high_limit = prices.loc[stock, "high_limit"]

                    if pd.notna(close) and pd.notna(high_limit) and high_limit > 0:
                        if close >= high_limit * 0.995:
                            zt_stocks.append(
                                {
                                    "stock": stock,
                                    "close": close,
                                    "limit": high_limit,
                                    "ratio": close / high_limit,
                                }
                            )
            except:
                pass

        print(f"\n涨停股票总数: {len(zt_stocks)}")

        if len(zt_stocks) > 0:
            print(f"涨停股票示例:")
            for i, s in enumerate(zt_stocks[:5]):
                print(
                    f"  {s['stock']}: 收盘{s['close']:.2f}, 涨停价{s['limit']:.2f}, 比值{s['ratio']:.4f}"
                )

        # 找二板（昨日涨停 + 前日涨停 + 大前天不涨停）
        if len(zt_stocks) > 0:
            print(f"\n=== 5. 找二板股票 ===")

            # 获取前一天和大前天的交易日
            trading_days_list = list(trading_days)
            dates_str = [str(d)[:10] for d in trading_days_list]

            if test_date in dates_str:
                idx = dates_str.index(test_date)
                if idx >= 2:
                    prev_date = dates_str[idx - 1]
                    prev2_date = dates_str[idx - 2]

                    print(f"检查日期:")
                    print(f"  今天: {test_date}")
                    print(f"  昨天: {prev_date}")
                    print(f"  前天: {prev2_date}")

                    # 获取最近3天数据
                    zt_codes = [s["stock"] for s in zt_stocks]

                    prices_3d = get_price(
                        zt_codes[:20],  # 只检查前20只涨停股
                        start_date=prev2_date,
                        end_date=test_date,
                        frequency="1d",
                        fields=["close", "high_limit"],
                    )

                    if prices_3d is not None and not prices_3d.empty:
                        print(f"3天数据获取成功")

                        second_board = []
                        for stock in zt_codes[:20]:
                            try:
                                # 今天涨停
                                today_close = (
                                    prices_3d.loc[stock, "close"][-1]
                                    if stock in prices_3d.index
                                    else None
                                )
                                today_limit = (
                                    prices_3d.loc[stock, "high_limit"][-1]
                                    if stock in prices_3d.index
                                    else None
                                )

                                # 昨天涨停
                                yesterday_close = (
                                    prices_3d.loc[stock, "close"][-2]
                                    if stock in prices_3d.index
                                    else None
                                )
                                yesterday_limit = (
                                    prices_3d.loc[stock, "high_limit"][-2]
                                    if stock in prices_3d.index
                                    else None
                                )

                                # 前天不涨停
                                prev2_close = (
                                    prices_3d.loc[stock, "close"][-3]
                                    if stock in prices_3d.index
                                    else None
                                )
                                prev2_limit = (
                                    prices_3d.loc[stock, "high_limit"][-3]
                                    if stock in prices_3d.index
                                    else None
                                )

                                if all(
                                    [
                                        pd.notna(today_close),
                                        pd.notna(today_limit),
                                        pd.notna(yesterday_close),
                                        pd.notna(yesterday_limit),
                                        pd.notna(prev2_close),
                                        pd.notna(prev2_limit),
                                    ]
                                ):
                                    # 今天涨停
                                    if today_close >= today_limit * 0.995:
                                        # 昨天涨停
                                        if yesterday_close >= yesterday_limit * 0.995:
                                            # 前天不涨停
                                            if prev2_close < prev2_limit * 0.995:
                                                second_board.append(stock)
                                                print(f"  找到二板: {stock}")

                            except Exception as e:
                                pass

                        print(f"\n二板股票总数: {len(second_board)}")

except Exception as e:
    print(f"批量获取失败: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 80)
print("调试完成")
print("=" * 80)
