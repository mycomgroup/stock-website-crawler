# RiceQuant API 测试
print("=== RiceQuant API 测试 ===")

try:
    # RiceQuant API: 获取所有股票
    all_stocks = all_instruments("CS")
    print(f"股票总数: {len(all_stocks)}")

    # 获取交易日
    dates = get_trading_dates("2024-03-01", "2024-03-10")
    print(f"2024-03-01至2024-03-10交易日: {len(dates)}")

    # 测试获取股票数据
    if len(all_stocks) > 0:
        test_stock = all_stocks[0].order_book_id
        print(f"测试股票: {test_stock}")

        bars = history_bars(test_stock, 5, "1d", "close")
        print(f"历史数据: {len(bars) if bars is not None else 0} 条")

    print("\nAPI 测试成功!")

except Exception as e:
    print(f"API 测试错误: {e}")
    import traceback

    traceback.print_exc()

print("=== 测试完成 ===")
