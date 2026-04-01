"""
二板策略调试 - RiceQuant Notebook 最终版
正确的API和字段名
"""

print("=" * 80)
print("二板策略调试 - RiceQuant Notebook")
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

    dates_str = [str(d)[:10] for d in trading_days]
    if test_date in dates_str:
        print(f"{test_date} 是交易日 ✓")
    else:
        test_date = dates_str[10]
        print(f"改用: {test_date}")

    trading_days_list = list(trading_days)

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

# 2. 检查股票池 - 使用正确的API
print("\n=== 2. 检查股票池 ===")
try:
    # 尝试 all_instruments
    all_inst = all_instruments("CS")
    print(f"all_instruments成功")
    print(f"股票总数: {len(all_inst)}")

    stock_list = all_inst["order_book_id"].tolist()
    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]
    print(f"过滤后股票数: {len(stocks)}")
    print(f"前10只: {stocks[:10]}")

except Exception as e:
    print(f"all_instruments失败: {e}")
    print("尝试其他API...")

    try:
        all_stocks_df = get_all_securities(["stock"])
        print(f"get_all_securities成功")
        print(f"股票总数: {len(all_stocks_df)}")

        stock_list = all_stocks_df.index.tolist()
        stocks = [
            s
            for s in stock_list
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]
        print(f"过滤后股票数: {len(stocks)}")
    except Exception as e2:
        print(f"get_all_securities也失败: {e2}")
        stocks = []

# 3. 测试单只股票 - 使用正确的字段名 limit_up
print("\n=== 3. 测试单只股票 ===")
test_stock = "000001.XSHE"
print(f"测试股票: {test_stock}")

try:
    prices = get_price(
        test_stock,
        start_date=test_date,
        end_date=test_date,
        frequency="1d",
        fields=["open", "close", "high", "limit_up", "limit_down"],  # 正确字段名
    )

    if prices is not None and not prices.empty:
        print(f"价格数据:")
        print(prices)

        close = prices["close"].iloc[0]
        limit_up = prices["limit_up"].iloc[0]

        print(f"\n收盘价: {close:.2f}")
        print(f"涨停价: {limit_up:.2f}")
        print(f"比值: {close / limit_up:.4f}")
        print(f"是否涨停(≥0.995): {close >= limit_up * 0.995}")
    else:
        print("无数据")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

# 4. 批量找涨停股票
print("\n=== 4. 批量找涨停股票 ===")
if len(stocks) > 0:
    try:
        test_stocks = stocks[:500]

        prices = get_price(
            test_stocks,
            start_date=test_date,
            end_date=test_date,
            frequency="1d",
            fields=["close", "limit_up"],
        )

        if prices is not None and not prices.empty:
            print(f"获取价格数据成功")

            zt_stocks = []

            # prices可能是DataFrame或多层索引
            if isinstance(prices.index, pd.MultiIndex):
                # 多层索引格式
                for stock in test_stocks:
                    try:
                        if (stock, test_date) in prices.index:
                            close = prices.loc[(stock, test_date), "close"]
                            limit_up = prices.loc[(stock, test_date), "limit_up"]

                            if pd.notna(close) and pd.notna(limit_up) and limit_up > 0:
                                if close >= limit_up * 0.995:
                                    zt_stocks.append(
                                        {
                                            "stock": stock,
                                            "close": close,
                                            "limit": limit_up,
                                            "ratio": close / limit_up,
                                        }
                                    )
                    except:
                        pass
            else:
                # 单层索引格式
                for stock in test_stocks:
                    try:
                        if stock in prices.index:
                            close = prices.loc[stock, "close"]
                            limit_up = prices.loc[stock, "limit_up"]

                            if pd.notna(close) and pd.notna(limit_up) and limit_up > 0:
                                if close >= limit_up * 0.995:
                                    zt_stocks.append(
                                        {
                                            "stock": stock,
                                            "close": close,
                                            "limit": limit_up,
                                            "ratio": close / limit_up,
                                        }
                                    )
                    except:
                        pass

            print(f"\n涨停股票总数: {len(zt_stocks)}")

            if len(zt_stocks) > 0:
                print(f"涨停股票示例:")
                for s in zt_stocks[:5]:
                    print(
                        f"  {s['stock']}: 收盘{s['close']:.2f}, 涨停价{s['limit']:.2f}, 比值{s['ratio']:.4f}"
                    )

            # 找二板
            if len(zt_stocks) > 0 and len(trading_days_list) > 0:
                print(f"\n=== 5. 找二板股票 ===")

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

                        zt_codes = [s["stock"] for s in zt_stocks]

                        prices_3d = get_price(
                            zt_codes[:30],
                            start_date=prev2_date,
                            end_date=test_date,
                            frequency="1d",
                            fields=["close", "limit_up"],
                        )

                        if prices_3d is not None and not prices_3d.empty:
                            print(f"3天数据获取成功")

                            second_board = []

                            for stock in zt_codes[:30]:
                                try:
                                    # 根据索引类型处理
                                    if isinstance(prices_3d.index, pd.MultiIndex):
                                        # 今天涨停
                                        today_close = prices_3d.loc[
                                            (stock, test_date), "close"
                                        ]
                                        today_limit = prices_3d.loc[
                                            (stock, test_date), "limit_up"
                                        ]

                                        yesterday_close = prices_3d.loc[
                                            (stock, prev_date), "close"
                                        ]
                                        yesterday_limit = prices_3d.loc[
                                            (stock, prev_date), "limit_up"
                                        ]

                                        prev2_close = prices_3d.loc[
                                            (stock, prev2_date), "close"
                                        ]
                                        prev2_limit = prices_3d.loc[
                                            (stock, prev2_date), "limit_up"
                                        ]
                                    else:
                                        # 单层索引 - 需要其他方法
                                        print(f"  单层索引格式，跳过 {stock}")
                                        continue

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
                                            if (
                                                yesterday_close
                                                >= yesterday_limit * 0.995
                                            ):
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
