from jqdata import *

print("测试Notebook连接")
stocks = get_all_securities("stock", "2024-01-01")
print(f"股票数量: {len(stocks)}")
