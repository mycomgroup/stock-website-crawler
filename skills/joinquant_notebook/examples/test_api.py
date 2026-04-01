"""
极简测试：验证JoinQuant Notebook是否正常
"""

from jqdata import *

print("测试 JoinQuant API")

# 测试1：获取交易日
days = get_trade_days("2024-01-01", "2024-01-10")
print(f"交易日列表: {days}")

# 测试2：获取股票列表
stocks = get_all_securities("stock", "2024-01-02")
print(f"股票总数: {len(stocks)}")

# 测试3：查询市值
q = query(valuation.code, valuation.circulating_market_cap).filter(
    valuation.code.in_(["000001.XSHE", "600000.XSHG"])
)
df = get_fundamentals(q, date="2024-01-02")
print(f"\n市值查询结果:")
print(df)

print("\n测试完成!")
