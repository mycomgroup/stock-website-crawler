from jqdata import *

print("测试聚宽API连接...")

date = "2024-01-02"
stocks = get_all_securities("stock", date).index.tolist()[:10]
print(f"获取到{len(stocks)}只股票")

print(f"示例股票: {stocks[:3]}")

print("API连接成功")
print("测试完成")
