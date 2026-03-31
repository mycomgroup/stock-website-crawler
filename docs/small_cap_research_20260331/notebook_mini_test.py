"""
小市值策略 - 最小化测试
"""

print("=== 小市值策略最小化测试 ===")

try:
    # 测试1: 获取股票数
    stocks = get_all_securities("stock", "2024-03-20")
    print(f"股票总数: {len(stocks)}")

    # 测试2: 获取指数成分股
    hs300 = get_index_stocks("000300.XSHG", date="2024-03-20")
    print(f"沪深300成分股: {len(hs300)}")

    # 测试3: 获取涨停家数（情绪指标）
    current = get_current_data()
    zt_count = 0
    for s in list(stocks.index)[:200]:
        if s in current and current[s].high_limit:
            if current[s].last_price >= current[s].high_limit * 0.99:
                zt_count += 1
    print(f"涨停家数(采样200只): {zt_count}")

    # 测试4: 情绪判断
    threshold = 30
    if zt_count >= threshold:
        print(f"✓ 情绪达标 ({zt_count} >= {threshold})")
    else:
        print(f"✗ 情绪不足 ({zt_count} < {threshold})")

    # 测试5: 市值筛选
    q = (
        query(valuation.code, valuation.market_cap)
        .filter(valuation.code.in_(hs300), valuation.market_cap.between(5, 200))
        .order_by(valuation.market_cap.asc())
        .limit(10)
    )

    df = get_fundamentals(q, date="2024-03-20")
    print(f"\n市值最小的10只股票:")
    print(df.to_string(index=False))

    print("\n=== 测试成功 ===")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
