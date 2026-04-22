# 简单测试 - RiceQuant API 验证

print("=== RiceQuant API 数据测试 ===")
print("")

# 测试 1: 获取交易日历
print("1. 测试交易日历")
try:
    dates = get_trading_dates("2024-01-01", "2024-01-31")
    print(f"   2024年1月交易日: {len(dates)} 天")
    print(f"   前5个交易日: {dates[:5]}")
except Exception as e:
    print(f"   错误: {e}")

print("")

# 测试 2: 获取指数成分股
print("2. 测试指数成分股")
try:
    hs300 = index_components("000300.XSHG")
    print(f"   沪深300成分股: {len(hs300)} 只")
    print(f"   前5只: {hs300[:5]}")
except Exception as e:
    print(f"   错误: {e}")

print("")

# 测试 3: 获取历史数据
print("3. 测试历史数据")
test_stocks = ["000001.XSHE", "600000.XSHG"]
for stock in test_stocks:
    try:
        bars = history_bars(stock, 10, "1d", ["open", "high", "low", "close", "volume"])
        if bars is not None and len(bars) > 0:
            print(f"   {stock}:")
            print(f"     获取到 {len(bars)} 天数据")
            print(f"     最新收盘价: {bars['close'][-1]:.2f}")
            print(f"     成交量: {bars['volume'][-1]:.0f}")
        else:
            print(f"   {stock}: 无数据")
    except Exception as e:
        print(f"   {stock}: 错误 - {e}")

print("")

# 测试 4: 获取财务数据
print("4. 测试财务数据")
try:
    from rqalpha.apis import query, fundamentals

    q = query(
        fundamentals.eod_derivative_indicator.market_cap,
        fundamentals.eod_derivative_indicator.pe_ratio,
    ).filter(
        fundamentals.eod_derivative_indicator.order_book_id.in_(
            ["000001.XSHE", "600000.XSHG"]
        )
    )

    df = get_fundamentals(q, entry_date="2024-01-01")

    if df is not None and not df.empty:
        print(f"   获取到 {len(df)} 条财务数据")
        print(f"   数据列: {df.columns.tolist()}")
        print(df)
    else:
        print("   无财务数据")
except Exception as e:
    print(f"   错误: {e}")

print("")
print("=== 测试完成 ===")
