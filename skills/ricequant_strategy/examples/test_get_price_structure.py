"""
简化测试 - 检查 get_price 数据结构
"""

print("=" * 80)
print("简化测试 - 检查数据结构")
print("=" * 80)

import pandas as pd

# 测试一只股票
test_stock = "000001.XSHE"
test_date = "2024-03-15"

print(f"\n测试股票: {test_stock}")
print(f"测试日期: {test_date}")

# 方式1: 使用 get_price 单只股票
print("\n=== 方式1: get_price 单只股票 ===")
try:
    prices1 = get_price(
        test_stock,
        start_date=test_date,
        end_date=test_date,
        frequency="1d",
        fields=["close", "limit_up"],
    )

    print(f"类型: {type(prices1)}")
    print(f"形状: {prices1.shape}")
    print(f"索引: {prices1.index}")
    print(f"列: {prices1.columns.tolist()}")
    print(f"数据:")
    print(prices1)

    if not prices1.empty:
        close = prices1["close"].iloc[0]
        limit_up = prices1["limit_up"].iloc[0]
        ratio = close / limit_up

        print(f"\n收盘: {close:.2f}")
        print(f"涨停价: {limit_up:.2f}")
        print(f"比值: {ratio:.4f}")
        print(f"涨停(≥0.995): {ratio >= 0.995}")
        print(f"涨停(≥0.99): {ratio >= 0.99}")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

# 方式2: 使用 get_price 多只股票
print("\n=== 方式2: get_price 多只股票 ===")
try:
    stocks = ["000001.XSHE", "000002.XSHE", "600000.XSHG"]

    prices2 = get_price(
        stocks,
        start_date=test_date,
        end_date=test_date,
        frequency="1d",
        fields=["close", "limit_up"],
    )

    print(f"类型: {type(prices2)}")
    print(f"形状: {prices2.shape}")
    print(f"索引类型: {type(prices2.index)}")
    print(f"是否MultiIndex: {isinstance(prices2.index, pd.MultiIndex)}")

    if isinstance(prices2.index, pd.MultiIndex):
        print(f"索引层级: {prices2.index.names}")
        print(f"索引值: {list(prices2.index)[:5]}")
    else:
        print(f"索引: {prices2.index.tolist()}")

    print(f"列: {prices2.columns.tolist()}")
    print(f"\n数据:")
    print(prices2)

    # 尝试提取数据
    print("\n=== 尝试提取数据 ===")

    if isinstance(prices2.index, pd.MultiIndex):
        # MultiIndex格式
        for stock in stocks:
            try:
                key = (stock, test_date)
                if key in prices2.index:
                    close = prices2.loc[key, "close"]
                    limit_up = prices2.loc[key, "limit_up"]

                    print(f"{stock}:")
                    print(f"  收盘: {close:.2f}")
                    print(f"  涨停价: {limit_up:.2f}")
                    print(f"  比值: {close / limit_up:.4f}")
            except Exception as e:
                print(f"{stock}: 提取失败 - {e}")
    else:
        # 单层索引格式
        for stock in stocks:
            try:
                if stock in prices2.index:
                    close = prices2.loc[stock, "close"]
                    limit_up = prices2.loc[stock, "limit_up"]

                    print(f"{stock}:")
                    print(f"  收盘: {close:.2f}")
                    print(f"  涨停价: {limit_up:.2f}")
                    print(f"  比值: {close / limit_up:.4f}")
            except Exception as e:
                print(f"{stock}: 提取失败 - {e}")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
