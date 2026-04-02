# 涨停检测逻辑验证 - RiceQuant Notebook

print("=" * 80)
print("涨停检测逻辑验证")
print("=" * 80)

import pandas as pd
import numpy as np

try:
    date = "2024-03-15"
    print(f"测试日期: {date}")

    # 获取所有股票
    all_stocks_df = all_instruments("CS", date)
    stocks = all_stocks_df["order_book_id"].tolist()
    stocks = [s for s in stocks if not (s.startswith("68") or s.startswith("300"))]
    print(f"股票池大小: {len(stocks)}")

    # 测试10只股票，看API返回什么
    print("\nAPI测试（前10只）:")
    for stock in stocks[:10]:
        try:
            bars = history_bars(stock, 1, "1d", "close,limit_up,limit_down", date)
            if bars is not None and len(bars) > 0:
                close = bars[0]["close"]
                limit_up = bars[0]["limit_up"]
                limit_down = bars[0]["limit_down"]
                pct_change = (close / limit_up - 1) * 100

                print(
                    f"{stock}: close={close:.2f}, limit_up={limit_up:.2f}, limit_down={limit_down:.2f}, pct={pct_change:.2f}%"
                )
            else:
                print(f"{stock}: 无数据")
        except Exception as e:
            print(f"{stock}: 错误 - {e}")

    # 检查涨停股（放宽条件：接近涨停即可）
    print("\n检查涨幅>=9%的股票（前100只）:")
    high_pct_stocks = []

    for stock in stocks[:100]:
        try:
            bars = history_bars(stock, 1, "1d", "close,limit_up", date)
            if bars is not None and len(bars) > 0:
                close = bars[0]["close"]
                limit_up = bars[0]["limit_up"]

                # 计算涨幅百分比
                pct = (close / limit_up - 1) * 100

                # 涨幅>=9%的股票
                if pct >= -1:  # 接近涨停（涨幅9%以上）
                    high_pct_stocks.append(
                        {
                            "stock": stock,
                            "close": close,
                            "limit_up": limit_up,
                            "pct": pct,
                        }
                    )
        except:
            pass

    print(f"\n涨幅>=9%的股票数: {len(high_pct_stocks)}")
    if len(high_pct_stocks) > 0:
        print("示例:")
        for s in high_pct_stocks[:10]:
            print(
                f"  {s['stock']}: close={s['close']:.2f}, limit_up={s['limit_up']:.2f}, pct={s['pct']:.2f}%"
            )

    # 真正的涨停股（涨幅>=9.9%）
    limit_up_stocks = [s for s in high_pct_stocks if s["pct"] >= -0.1]
    print(f"\n真正涨停股（涨幅>=9.9%）: {len(limit_up_stocks)}")
    if len(limit_up_stocks) > 0:
        print("涨停股:")
        for s in limit_up_stocks[:10]:
            print(
                f"  {s['stock']}: close={s['close']:.2f}, limit_up={s['limit_up']:.2f}"
            )

    # 如果还是没找到，扩大搜索范围
    if len(limit_up_stocks) == 0:
        print("\n前100只无涨停，扩大到全部股票池...")

        all_limit_up = []
        for stock in stocks:
            try:
                bars = history_bars(stock, 1, "1d", "close,limit_up", date)
                if bars is not None and len(bars) > 0:
                    close = bars[0]["close"]
                    limit_up = bars[0]["limit_up"]
                    if close >= limit_up * 0.99:
                        all_limit_up.append(stock)
            except:
                pass

        print(f"全部涨停股数: {len(all_limit_up)}")
        if len(all_limit_up) > 0:
            print(f"涨停股示例（前20只）:")
            for s in all_limit_up[:20]:
                print(f"  {s}")
        else:
            print("2024-03-15确实无涨停股！")
            print("这可能是因为该日市场情绪低迷")

            # 尝试其他日期
            print("\n尝试其他日期...")
            other_dates = ["2024-01-02", "2024-02-19", "2024-03-20", "2024-04-01"]

            for other_date in other_dates:
                print(f"\n日期: {other_date}")
                count = 0
                for stock in stocks[:200]:  # 只测200只
                    try:
                        bars = history_bars(
                            stock, 1, "1d", "close,limit_up", other_date
                        )
                        if bars is not None and len(bars) > 0:
                            close = bars[0]["close"]
                            limit_up = bars[0]["limit_up"]
                            if close >= limit_up * 0.99:
                                count += 1
                    except:
                        pass
                print(f"  涨停股数（采样200只）: {count}")
                if count > 0:
                    print(f"  ✓ 有涨停股！")
                    break

except Exception as e:
    print(f"执行错误: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 80)
print("验证完成")
print("=" * 80)
