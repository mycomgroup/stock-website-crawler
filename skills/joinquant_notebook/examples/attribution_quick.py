"""
小市值因子 vs 事件策略归因分析 - 超简化版本
只验证选股逻辑，不做完整统计
"""

from jqdata import *

print("=== 策略归因分析 - 快速验证 ===")

test_date = "2024-01-02"
prev_date = "2024-01-02"
curr_date = "2024-01-03"

# ============ 策略A: 纯小市值因子 ============
print("\n策略A: 纯小市值因子")

all_stocks = get_all_securities("stock", test_date).index.tolist()
all_stocks = [s for s in all_stocks if s[0] not in ["4", "8", "3"] and s[:2] != "68"]

st_df = get_extras(
    "is_st", all_stocks, start_date=test_date, end_date=test_date, df=True
).T
st_df.columns = ["is_st"]
all_stocks = list(st_df[st_df["is_st"] == False].index)

q = (
    query(valuation.code, valuation.circulating_market_cap)
    .filter(valuation.code.in_(all_stocks), valuation.circulating_market_cap > 0)
    .order_by(valuation.circulating_market_cap.asc())
    .limit(50)
)

df = get_fundamentals(q, date=test_date)
print(f"市值最小的50只股票:")
print(df.head(10))

# ============ 策略B: 小市值 + 事件 ============
print("\n策略B: 小市值+事件（市值5-15亿+首板）")

q_b = query(valuation.code, valuation.circulating_market_cap).filter(
    valuation.code.in_(all_stocks),
    valuation.circulating_market_cap >= 5,
    valuation.circulating_market_cap <= 15,
)

df_b = get_fundamentals(q_b, date=prev_date)
print(f"市值5-15亿的股票数: {len(df_b)}")
print(df_b.head(10))

if len(df_b) > 0:
    small_cap_codes = list(df_b["code"])[:100]  # 只取前100只

    price_df = get_price(
        small_cap_codes,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )

    if not price_df.empty:
        price_df = price_df.dropna()
        limit_up = price_df[price_df["close"] == price_df["high_limit"]]
        print(f"\n首板股票数: {len(limit_up)}")
        if len(limit_up) > 0:
            print("首板股票:")
            print(limit_up)

# ============ 策略C: 纯事件（全市场首板） ============
print("\n策略C: 纯事件（全市场首板）")

# 为了快速，只取前500只股票测试
test_stocks = all_stocks[:500]

price_df_c = get_price(
    test_stocks,
    end_date=prev_date,
    frequency="daily",
    fields=["close", "high_limit"],
    count=1,
    panel=False,
)

if not price_df_c.empty:
    price_df_c = price_df_c.dropna()
    limit_up_c = price_df_c[price_df_c["close"] == price_df_c["high_limit"]]
    print(f"全市场首板股票数（前500只样本）: {len(limit_up_c)}")

print("\n=== 快速验证完成 ===")
