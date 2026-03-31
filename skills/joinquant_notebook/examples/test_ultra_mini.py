# 最小测试
from jqdata import *

print("=" * 40)
print("最小化测试")
print("=" * 40)

# 获取交易日
trade_days = list(get_trade_days("2024-01-01", "2024-01-10"))
print(f"交易日: {len(trade_days)}")

# 获取股票
stocks = get_all_securities("stock", "2024-01-02").index.tolist()[:10]
print(f"股票数: {len(stocks)}")

# 获取价格
df = get_price(
    stocks,
    end_date="2024-01-02",
    frequency="daily",
    fields=["open", "close", "high_limit"],
    count=1,
    panel=False,
)
print(df)

# 计算涨停股
if not df.empty:
    df = df.dropna()
    hl = df[df["close"] == df["high_limit"]]
    print(f"\n涨停股: {len(hl)}")

print("\n测试完成")
