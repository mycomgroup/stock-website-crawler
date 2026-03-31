"""
最小化测试 - JoinQuant Notebook
验证API连接
"""

print("=== JoinQuant Notebook 最小测试 ===")
print("测试时间:", context.now if "context" in dir() else "N/A")

try:
    # 测试1: 获取股票数量
    stocks = get_all_securities("stock", "2024-01-01")
    print(f"股票总数: {len(stocks)}")

    # 测试2: 获取指数成分股
    hs300 = get_index_stocks("000300.XSHG", date="2024-01-01")
    print(f"沪深300成分股: {len(hs300)}")

    # 测试3: 获取市值最小的10只股票
    q = (
        query(valuation.code, valuation.market_cap)
        .filter(valuation.code.in_(hs300))
        .order_by(valuation.market_cap.asc())
        .limit(10)
    )

    df = get_fundamentals(q, date="2024-01-01")
    print(f"\n市值最小的10只股票:")
    print(df.to_string(index=False))

    print("\n=== 测试成功 ===")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
