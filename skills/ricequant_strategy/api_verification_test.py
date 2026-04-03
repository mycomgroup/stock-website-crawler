"""
RiceQuant API 验证测试
"""

print("=" * 70)
print("RiceQuant API 验证测试")
print("=" * 70)

# 1. 获取交易日
print("\n1. 获取交易日")
dates = get_trading_dates("2024-01-01", "2024-01-31")
print(f"2024年1月交易日: {len(dates)}天")
print(f"首个交易日: {dates[0]}")
print(f"最后交易日: {dates[-1]}")

# 2. 获取股票列表
print("\n2. 获取股票列表")
all_stocks = all_instruments("CS")
print(f"股票总数: {len(all_stocks)}")
print(f"列名: {all_stocks.columns.tolist()}")

# 3. 过滤股票
stock_list = all_stocks["order_book_id"].tolist()
print(f"股票代码示例: {stock_list[:5]}")

# 排除科创板、北交所
filtered = [s for s in stock_list if not s.startswith(("688", "4", "8"))]
print(f"过滤后股票数: {len(filtered)}")

# 4. 测试获取价格数据
print("\n3. 测试获取价格数据")
test_stock = filtered[0]
print(f"测试股票: {test_stock}")

bars = history_bars(
    test_stock, 5, "1d", "close,open,high,low,limit_up", end_date=dates[-1]
)
if bars is not None:
    print(f"获取到 {len(bars)} 条数据")
    print(f"最新数据: close={bars[-1]['close']}, limit_up={bars[-1]['limit_up']}")
    print(f"是否涨停: {bars[-1]['close'] >= bars[-1]['limit_up'] * 0.99}")
else:
    print("获取数据失败")

# 5. 统计涨停（扩大样本）
print("\n4. 统计涨停股票（样本200只）")
zt_count = 0
zt_stocks = []
for stock in filtered[:200]:
    try:
        bars = history_bars(stock, 1, "1d", "close,limit_up", end_date=dates[-1])
        if bars is not None and len(bars) > 0:
            if bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99:
                zt_count += 1
                zt_stocks.append(stock)
    except:
        pass

print(f"涨停股票数: {zt_count}")
print(f"涨停股票示例: {zt_stocks[:5]}")

# 6. 测试二板判断
print("\n5. 测试二板判断")
if len(zt_stocks) > 0:
    test_stock = zt_stocks[0]
    print(f"测试股票: {test_stock}")

    # 获取3天数据
    bars = history_bars(test_stock, 3, "1d", "close,limit_up", end_date=dates[-1])
    if bars is not None and len(bars) >= 3:
        for i, bar in enumerate(bars):
            is_zt = bar["close"] >= bar["limit_up"] * 0.99
            print(
                f"  第{i + 1}天: close={bar['close']:.2f}, limit_up={bar['limit_up']:.2f}, 涨停={is_zt}"
            )

print("\n" + "=" * 70)
print("API验证完成")
print("=" * 70)
