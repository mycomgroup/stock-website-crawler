#!/usr/bin/env python3
"""
RFScore 选股测试 - Notebook 版本
测试单日选股功能
"""

from jqdata import *
import pandas as pd

print("=" * 70)
print("RFScore 选股测试 - Notebook")
print("=" * 70)

# 测试日期
test_date = "2021-01-04"

print(f"\n测试日期: {test_date}")

# 1. 获取股票池
print("\n获取股票池...")
hs300 = set(get_index_stocks("000300.XSHG", date=test_date))
zz500 = set(get_index_stocks("000905.XSHG", date=test_date))
stocks = list(hs300 | zz500)
stocks = [s for s in stocks if not s.startswith("688")]
print(f"初始股票数: {len(stocks)}")

# 2. 过滤新股
print("\n过滤新股...")
sec = get_all_securities(types=["stock"], date=test_date)
sec = sec.loc[sec.index.intersection(stocks)]

# 使用字符串日期比较
threshold_str = "2020-07-04"  # 180天前
sec = sec[sec["start_date"].apply(lambda x: str(x) <= threshold_str)]
stocks = sec.index.tolist()
print(f"过滤后股票数: {len(stocks)}")

# 3. 过滤 ST
print("\n过滤 ST...")
is_st = get_extras("is_st", stocks, end_date=test_date, count=1).iloc[-1]
stocks = is_st[is_st == False].index.tolist()
print(f"过滤后股票数: {len(stocks)}")

# 4. 过滤停牌
print("\n过滤停牌...")
paused = get_price(stocks, end_date=test_date, count=1, fields="paused", panel=False)
paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
stocks = paused[paused == 0].index.tolist()
print(f"可用股票数: {len(stocks)}")

# 5. 获取基本面数据（简化：不使用 jqfactor）
print("\n获取基本面数据...")
# 使用 get_fundamentals 获取 ROA
q = query(valuation.code, valuation.pb_ratio, indicator.roa).filter(
    valuation.code.in_(stocks)
)

df = get_fundamentals(q, date=test_date)
df = df.dropna()

# PB 分组
df = df.sort_values("pb_ratio")
df["pb_group"] = (
    pd.qcut(df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop")
    + 1
)

# 简化选股：ROA 最高 + PB 最低 10%
primary = df[(df["pb_group"] == 1) & (df["roa"] > 0)]
primary = primary.sort_values("roa", ascending=False)

picks = primary["code"].head(20).tolist()

print(f"\n选中股票数: {len(picks)}")
print(f"选中股票: {picks[:10]}")

# 6. 计算收益（测试下月）
print("\n计算下月收益...")
next_trade_days = get_trade_days(test_date, "2021-01-31")
next_date = str(next_trade_days[-1])

returns = []
for stock in picks[:10]:  # 只测试前10个
    try:
        p1 = get_price(
            stock, end_date=test_date, count=1, fields=["close"], panel=False
        )
        p2 = get_price(
            stock, end_date=next_date, count=1, fields=["close"], panel=False
        )

        if not p1.empty and not p2.empty:
            ret = (float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1])) / float(
                p1["close"].iloc[-1]
            )
            returns.append(ret)
            print(f"  {stock}: {ret * 100:.2f}%")
    except Exception as e:
        print(f"  {stock}: 错误 - {e}")

if returns:
    avg_return = sum(returns) / len(returns)
    print(f"\n平均收益: {avg_return * 100:.2f}%")

print("\n" + "=" * 70)
print("完成!")
print("=" * 70)
