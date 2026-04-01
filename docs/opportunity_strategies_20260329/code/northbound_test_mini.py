from jqdata import *
import pandas as pd

print("北向资金数据测试（最小化）")

q = (
    query(finance.STK_ML_QUOTA)
    .filter(
        finance.STK_ML_QUOTA.day >= "2024-01-01",
        finance.STK_ML_QUOTA.day <= "2024-01-10",
        finance.STK_ML_QUOTA.link_id.in_([310001, 310002]),
    )
    .order_by(finance.STK_ML_QUOTA.day.asc())
)

nb_data = finance.run_query(q)

print(f"查询结果条数: {len(nb_data)}")
print("\n前5条数据:")
print(nb_data.head())

if len(nb_data) > 0:
    nb_daily = (
        nb_data.groupby("day")
        .agg({"buy_amount": "sum", "sell_amount": "sum"})
        .reset_index()
    )

    nb_daily["net_flow"] = nb_daily["buy_amount"] - nb_daily["sell_amount"]

    print("\n日度汇总:")
    print(nb_daily)

    print("\n北向净流入统计:")
    print(f"  平均净流入: {nb_daily['net_flow'].mean() / 1e8:.2f}亿")
    print(f"  净流入>0天数: {(nb_daily['net_flow'] > 0).sum()}")
else:
    print("未获取到数据")

print("\n测试完成")
