"""
二板策略简化测试 - RiceQuant Notebook
测试单个日期验证 API
"""

print("=== RiceQuant 二板策略简化测试 ===")

try:
    # 获取交易日
    dates = get_trading_dates("2025-01-01", "2025-03-31")
    print(f"2025Q1交易日数: {len(dates)}")
    
    if len(dates) > 0:
        test_date = dates[-5]  # 测试最近第5天
        print(f"测试日期: {test_date}")
        
        # 获取股票列表
        all_stocks = get_all_securities(["stock"])
        print(f"股票总数: {len(all_stocks)}")
        
        # 测试单个股票
        test_stock = list(all_stocks.index)[0]
        print(f"测试股票: {test_stock}")
        
        # 获取价格数据
        prices = get_price(test_stock, start_date=test_date, end_date=test_date,
                           fields=['open', 'close', 'high', 'low', 'volume'])
        print(f"价格数据: {len(prices)} 行")
        
        if len(prices) > 0:
            print(f"开盘: {prices['open'].iloc[0]}, 收盘: {prices['close'].iloc[0]}")
        
        print("\nAPI 测试成功!")
        
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 测试完成 ===")
