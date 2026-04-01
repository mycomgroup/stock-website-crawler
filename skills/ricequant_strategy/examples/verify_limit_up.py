"""
验证RiceQuant涨停价API
"""

print("=" * 70)
print("验证 RiceQuant 涨停价 API")
print("=" * 70)

try:
    # 获取一只股票
    all_stocks = all_instruments("CS")
    stock_list = all_stocks["order_book_id"].tolist()
    test_stock = stock_list[0]

    print(f"\n测试股票: {test_stock}")

    # 获取历史数据
    bars = history_bars(
        test_stock, 5, "1d", "close,limit_up,limit_down", end_date="2024-01-31"
    )

    if bars is not None:
        print(f"\n最近5天数据:")
        for i, bar in enumerate(bars):
            print(
                f"  第{i + 1}天: 收盘{bar['close']:.2f}, 涨停价{bar['limit_up'] if bar['limit_up'] else 'None'}, 跌停价{bar['limit_down'] if bar['limit_down'] else 'None'}"
            )
    else:
        print("无法获取数据")

    # 测试多只股票
    print(f"\n测试前10只股票的涨停价:")
    for stock in stock_list[:10]:
        try:
            bars = history_bars(stock, 1, "1d", "close,limit_up", end_date="2024-01-31")
            if bars is not None and len(bars) > 0:
                bar = bars[0]
                print(
                    f"  {stock}: 收盘{bar['close']:.2f}, 涨停价{bar['limit_up'] if bar['limit_up'] else 'None'}"
                )
        except:
            print(f"  {stock}: 获取失败")

except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()
