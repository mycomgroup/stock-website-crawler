"""
二板策略深度调试 - 检查数据结构
"""

print("=" * 80)
print("二板策略深度调试 - RiceQuant")
print("=" * 80)

import numpy as np

# 测试日期
test_date = "2021-01-15"
print(f"\n测试日期: {test_date}")

# 1. 检查是否是交易日
print("\n=== 1. 检查交易日 ===")
try:
    trading_days = get_trading_dates("2021-01-01", "2021-01-31")
    print(f"2021年1月交易日数: {len(trading_days)}")
    print(f"前10个交易日: {trading_days[:10]}")

    if test_date in [str(d) for d in trading_days]:
        print(f"{test_date} 是交易日 ✓")
    else:
        print(f"{test_date} 不是交易日 ✗")
        print("尝试使用第一个交易日")
        test_date = str(trading_days[0])
        print(f"新测试日期: {test_date}")
except Exception as e:
    print(f"获取交易日失败: {e}")

# 2. 检查单只股票数据结构
print("\n=== 2. 检查单只股票数据结构 ===")
test_stock = "000001.XSHE"
print(f"测试股票: {test_stock}")

try:
    bars = history_bars(
        test_stock,
        1,
        "1d",
        ["close", "open", "high", "low", "limit_up", "limit_down"],
        end_date=test_date,
    )
    if bars is not None and len(bars) > 0:
        print(f"bars类型: {type(bars)}")
        print(f"bars长度: {len(bars)}")
        print(f"bars字段: {bars.dtype.names if hasattr(bars, 'dtype') else 'N/A'}")
        print(f"bars[0]: {bars[0]}")
        print(f"bars[-1]: {bars[-1]}")

        # 检查涨停价字段
        if "limit_up" in bars.dtype.names:
            print(f"涨停价: {bars[-1]['limit_up']}")
            print(f"收盘价: {bars[-1]['close']}")
            print(f"涨停判断: {bars[-1]['close'] >= bars[-1]['limit_up'] * 0.995}")
        else:
            print("没有limit_up字段！")
    else:
        print("bars为空或None")
except Exception as e:
    print(f"获取数据失败: {e}")
    import traceback

    traceback.print_exc()

# 3. 检查股票池
print("\n=== 3. 检查股票池 ===")
try:
    all_inst = all_instruments("CS")
    print(f"all_instruments类型: {type(all_inst)}")
    print(
        f"all_instruments列名: {all_inst.columns.tolist() if hasattr(all_inst, 'columns') else 'N/A'}"
    )
    print(f"股票数量: {len(all_inst)}")
    print(f"前5只股票:")
    print(all_inst.head())

    stock_list = all_inst["order_book_id"].tolist()
    print(f"\n股票列表长度: {len(stock_list)}")
    print(f"前10只股票代码: {stock_list[:10]}")
except Exception as e:
    print(f"获取股票池失败: {e}")

# 4. 找涨停股票（详细版）
print("\n=== 4. 找涨停股票（详细版） ===")
stocks_to_check = ["000001.XSHE", "600000.XSHG", "000002.XSHE", "600519.XSHG"]
zt_found = []

for stock in stocks_to_check:
    try:
        bars = history_bars(stock, 1, "1d", ["close", "limit_up"], end_date=test_date)
        if bars is not None and len(bars) > 0:
            close = bars[-1]["close"]
            limit_up = bars[-1]["limit_up"]
            ratio = close / limit_up if limit_up > 0 else 0

            print(f"\n{stock}:")
            print(f"  收盘价: {close:.2f}")
            print(f"  涨停价: {limit_up:.2f}")
            print(f"  比值: {ratio:.4f}")
            print(f"  是否涨停(≥0.995): {ratio >= 0.995}")
            print(f"  是否涨停(≥0.99): {ratio >= 0.99}")

            if ratio >= 0.995:
                zt_found.append(stock)
    except Exception as e:
        print(f"{stock}: 获取失败 - {e}")

print(f"\n涨停股票数: {len(zt_found)}")
print(f"涨停股票: {zt_found}")

# 5. 扩大范围找涨停
print("\n=== 5. 扩大范围找涨停（检查500只） ===")
all_inst = all_instruments("CS")
stock_list = all_inst["order_book_id"].tolist()
stocks = [
    s
    for s in stock_list
    if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
]

zt_count = 0
zt_examples = []

for i, stock in enumerate(stocks[:500]):
    if i % 100 == 0:
        print(f"检查进度: {i}/500")

    try:
        bars = history_bars(stock, 1, "1d", ["close", "limit_up"], end_date=test_date)
        if bars is not None and len(bars) > 0:
            close = bars[-1]["close"]
            limit_up = bars[-1]["limit_up"]

            if limit_up > 0 and close >= limit_up * 0.995:
                zt_count += 1
                if len(zt_examples) < 5:
                    zt_examples.append(
                        {
                            "stock": stock,
                            "close": close,
                            "limit_up": limit_up,
                            "ratio": close / limit_up,
                        }
                    )
    except:
        pass

print(f"\n涨停股票总数: {zt_count}")
if zt_examples:
    print("涨停股票示例:")
    for ex in zt_examples:
        print(
            f"  {ex['stock']}: 收盘{ex['close']:.2f}, 涨停价{ex['limit_up']:.2f}, 比值{ex['ratio']:.4f}"
        )

print("\n" + "=" * 80)
print("调试完成")
print("=" * 80)
