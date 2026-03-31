# -*- coding: utf-8 -*-
"""
任务07：组合策略简化版回测（仅测试2024年Q1）
"""

import numpy as np
import pandas as pd
from jqdata import *

print("=" * 50)
print("任务07：组合策略简化回测")
print("测试期间: 2024-01-01 ~ 2024-03-31")
print("=" * 50)

# 简化测试期间
start_date = "2024-01-01"
end_date = "2024-03-31"

# 获取交易日
trade_days = list(get_trade_days(start_date, end_date))
print(f"交易日数: {len(trade_days)}")

# 存储结果
results = {
    "first_board": {"trades": 0, "returns": []},
    "weak_to_strong": {"trades": 0, "returns": []},
}

# 遍历交易日
for i, date in enumerate(trade_days[:20]):  # 只测试前20天
    print(f"处理: {date}")

    try:
        # 获取前一日
        prev_dates = list(get_trade_days("2023-01-01", date))
        if len(prev_dates) < 3:
            continue
        prev_date = prev_dates[-2]

        # 获取股票池
        stocks = get_all_securities("stock", date).index.tolist()
        stocks = [s for s in stocks if s[:2] != "68" and s[0] not in ["4", "8"]][
            :500
        ]  # 限制数量

        # 昨日涨停股
        df = get_price(
            stocks,
            end_date=prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        if df.empty:
            continue
        df = df.dropna()
        hl_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()

        if not hl_stocks:
            continue

        # 今日开盘价
        today_df = get_price(
            hl_stocks[:50],
            end_date=date,
            frequency="daily",
            fields=["open", "close", "high_limit"],
            count=1,
            panel=False,
        )
        if today_df.empty:
            continue
        today_df = today_df.dropna()
        today_df["open_ratio"] = today_df["open"] / (today_df["high_limit"] / 1.1)

        # 首板低开: 假弱高开 0.5%-1.5%
        fb = today_df[
            (today_df["open_ratio"] > 1.005) & (today_df["open_ratio"] < 1.015)
        ]
        for _, row in fb.iterrows():
            ret = (row["close"] - row["open"]) / row["open"]
            results["first_board"]["returns"].append(ret)
            results["first_board"]["trades"] += 1

        # 弱转强: 高开0-6%
        wts = today_df[(today_df["open_ratio"] > 1.0) & (today_df["open_ratio"] < 1.06)]
        for _, row in wts.iterrows():
            ret = (row["close"] - row["open"]) / row["open"]
            results["weak_to_strong"]["returns"].append(ret)
            results["weak_to_strong"]["trades"] += 1

    except Exception as e:
        print(f"错误: {e}")

# 计算统计
print("\n" + "=" * 50)
print("结果统计")
print("=" * 50)

for name, data in results.items():
    if data["returns"]:
        avg_ret = np.mean(data["returns"]) * 100
        win_rate = sum(1 for r in data["returns"] if r > 0) / len(data["returns"]) * 100
        print(f"\n{name}:")
        print(f"  交易次数: {data['trades']}")
        print(f"  平均收益: {avg_ret:.2f}%")
        print(f"  胜率: {win_rate:.1f}%")
    else:
        print(f"\n{name}: 无交易")

# 最终结论
print("\n" + "=" * 50)
print("结论")
print("=" * 50)
print("这是一个简化测试，仅测试了20个交易日")
print("完整回测需要更长时间")
