"""
测试 RiceQuant Notebook API
"""

print("=== RiceQuant API 测试 ===")

# 测试 get_price
try:
    print("\n1. 测试 get_price...")
    df = get_price(
        "000001.XSHE",
        start_date="2024-01-02",
        end_date="2024-01-02",
        frequency="1d",
        fields=["close", "open", "high"],
    )
    print(f"   成功! 数据: {df}")
except Exception as e:
    print(f"   失败: {e}")

# 测试 history_bars
try:
    print("\n2. 测试 history_bars...")
    bars = history_bars("000001.XSHE", 5, "1d", "close")
    print(f"   成功! 数据: {bars}")
except Exception as e:
    print(f"   失败: {e}")

# 测试 all_instruments
try:
    print("\n3. 测试 all_instruments...")
    stocks = all_instruments(type="CS")
    print(f"   成功! 股票数: {len(stocks)}")
except Exception as e:
    print(f"   失败: {e}")

# 测试 index_components
try:
    print("\n4. 测试 index_components...")
    hs300 = index_components("000300.XSHG")
    print(f"   成功! 沪深300股票数: {len(hs300)}")
except Exception as e:
    print(f"   失败: {e}")

# 测试 get_trading_dates
try:
    print("\n5. 测试 get_trading_dates...")
    dates = get_trading_dates("2024-01-01", "2024-01-10")
    print(f"   成功! 交易日: {list(dates)}")
except Exception as e:
    print(f"   失败: {e}")

print("\n=== 测试完成 ===")
