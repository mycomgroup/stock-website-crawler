"""
二板策略测试 - 使用2024年数据验证
因为文档显示2024年有139次交易
"""

print("=" * 80)
print("二板策略测试 - RiceQuant Notebook")
print("测试日期：2024年（已知有139次交易）")
print("=" * 80)

import pandas as pd
import numpy as np

# 测试2024年的多个日期
test_dates = ["2024-03-15", "2024-06-15", "2024-09-15", "2024-12-15"]
zt_threshold = 0.99  # 降低阈值

print(f"\n涨停判断阈值: ≥{zt_threshold}")

results = {}

for test_date in test_dates:
    print(f"\n{'=' * 60}")
    print(f"测试日期: {test_date}")
    print(f"{'=' * 60}")

    try:
        # 1. 检查是否是交易日
        trading_days = get_trading_dates(test_date[:7] + "-01", test_date[:7] + "-28")

        dates_str = [str(d)[:10] for d in trading_days]

        if test_date not in dates_str:
            print(f"{test_date} 不是交易日，跳过")
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

        print(f"股票池: {len(stocks)}只")

        # 3. 找涨停股票
        prices = get_price(
            stocks[:500],
            start_date=test_date,
            end_date=test_date,
            frequency="1d",
            fields=["close", "limit_up"],
        )

        if prices is None or prices.empty:
            print("无数据")
            continue

        zt_stocks = []

        # 处理数据
        if isinstance(prices.index, pd.MultiIndex):
            for stock in stocks[:500]:
                try:
                    if (stock, test_date) in prices.index:
                        close = prices.loc[(stock, test_date), "close"]
                        limit_up = prices.loc[(stock, test_date), "limit_up"]

                        if pd.notna(close) and pd.notna(limit_up) and limit_up > 0:
                            ratio = close / limit_up
                            if ratio >= zt_threshold:
                                zt_stocks.append(
                                    {
                                        "stock": stock,
                                        "close": close,
                                        "limit": limit_up,
                                        "ratio": ratio,
                                    }
                                )
                except:
                    pass
        else:
            for stock in stocks[:500]:
                try:
                    if stock in prices.index:
                        close = prices.loc[stock, "close"]
                        limit_up = prices.loc[stock, "limit_up"]

                        if pd.notna(close) and pd.notna(limit_up) and limit_up > 0:
                            ratio = close / limit_up
                            if ratio >= zt_threshold:
                                zt_stocks.append(
                                    {
                                        "stock": stock,
                                        "close": close,
                                        "limit": limit_up,
                                        "ratio": ratio,
                                    }
                                )
                except:
                    pass

        results[test_date] = {"zt_count": len(zt_stocks), "zt_examples": zt_stocks[:5]}

        print(f"涨停股票数: {len(zt_stocks)}")

        if len(zt_stocks) > 0:
            print(f"涨停示例:")
            for s in zt_stocks[:3]:
                print(
                    f"  {s['stock']}: 收盘{s['close']:.2f}, 涨停价{s['limit']:.2f}, 比值{s['ratio']:.4f}"
                )

            # 4. 找二板（如果涨停>0）
            if len(trading_days) > 2:
                idx = dates_str.index(test_date)

                if idx >= 2:
                    prev_date = dates_str[idx - 1]
                    prev2_date = dates_str[idx - 2]

                    print(f"\n找二板:")
                    print(f"  昨天: {prev_date}")
                    print(f"  前天: {prev2_date}")

                    zt_codes = [s["stock"] for s in zt_stocks]

                    prices_3d = get_price(
                        zt_codes[:20],
                        start_date=prev2_date,
                        end_date=test_date,
                        frequency="1d",
                        fields=["close", "limit_up"],
                    )

                    if prices_3d is not None and not prices_3d.empty:
                        second_board = []

                        for stock in zt_codes[:20]:
                            try:
                                if isinstance(prices_3d.index, pd.MultiIndex):
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
                                        if today_close >= today_limit * zt_threshold:
                                            # 昨天涨停
                                            if (
                                                yesterday_close
                                                >= yesterday_limit * zt_threshold
                                            ):
                                                # 前天不涨停
                                                if (
                                                    prev2_close
                                                    < prev2_limit * zt_threshold
                                                ):
                                                    second_board.append(stock)
                                                    print(f"  找到二板: {stock}")
                            except:
                                pass

                        results[test_date]["second_board"] = len(second_board)
                        print(f"二板数: {len(second_board)}")

    except Exception as e:
        print(f"错误: {e}")
        import traceback

        traceback.print_exc()

# 汇总
print(f"\n{'=' * 80}")
print("汇总结果")
print(f"{'=' * 80}")

for date, r in results.items():
    print(f"{date}: 涨停{r['zt_count']}只, 二板{r.get('second_board', 0)}只")

print(f"\n如果涨停数>0，说明API正确")
print(f"如果二板数>0，说明筛选逻辑正确")
print("=" * 80)
