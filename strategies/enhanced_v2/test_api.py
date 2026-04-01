from jqdata import *

print("测试 JoinQuant Notebook 基本功能")

try:
    stocks = get_index_stocks("000300.XSHG", date="2024-06-01")
    print(f"沪深300成分股: {len(stocks)}只")

    price = get_price("000001.XSHE", end_date="2024-06-01", count=5, fields=["close"])
    print(f"\n平安银行最近5天收盘价:")
    print(price)

    print("\n基本API正常！")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
