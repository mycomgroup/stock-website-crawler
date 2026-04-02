"""
RiceQuant Notebook API 测试
测试哪些API可用
"""

print("=" * 80)
print("RiceQuant Notebook API 测试")
print("=" * 80)

try:
    print("\n测试1: 基础Python")
    from datetime import datetime

    print(f"✓ 当前时间: {datetime.now()}")

    print("\n测试2: 尝试 all_instruments")
    try:
        stocks = all_instruments("CS")
        print(f"✓ 股票数: {len(stocks)}")
        print(f"  示例: {stocks['order_book_id'].head(3).tolist()}")
    except Exception as e:
        print(f"✗ all_instruments 失败: {e}")

    print("\n测试3: 尝试 get_trading_dates")
    try:
        dates = get_trading_dates("2022-01-01", "2022-01-31")
        print(f"✓ 交易日数: {len(dates)}")
    except Exception as e:
        print(f"✗ get_trading_dates 失败: {e}")

    print("\n测试4: 尝试 get_price")
    try:
        price = get_price(
            "000001.XSHE",
            start_date="2022-01-01",
            end_date="2022-01-05",
            frequency="1d",
            fields=["close", "limit_up"],
        )
        print(f"✓ 获取价格数据成功")
        print(f"  数据形状: {price.shape}")
    except Exception as e:
        print(f"✗ get_price 失败: {e}")

    print("\n测试5: 尝试 history_bars")
    try:
        bars = history_bars("000001.XSHE", 5, "1d", "close,limit_up")
        print(f"✓ 获取历史数据成功")
        print(f"  数据长度: {len(bars) if bars is not None else 0}")
    except Exception as e:
        print(f"✗ history_bars 失败: {e}")

    print("\n" + "=" * 80)
    print("API 测试完成")
    print("=" * 80)

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback

    traceback.print_exc()
