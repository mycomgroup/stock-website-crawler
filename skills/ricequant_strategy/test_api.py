# -*- coding: utf-8 -*-
"""
风控测试 - RiceQuant Notebook格式
快速验证策略逻辑 v2
"""

print("=" * 60)
print("风控A/B测试 - RiceQuant Notebook验证")
print("=" * 60)

import datetime as dt
import pandas as pd
import numpy as np

test_date = "2023-06-01"
print(f"\n测试日期: {test_date}")

print("\n1. 获取股票池...")
all_stocks_df = all_instruments("CS")
print(f"类型: {type(all_stocks_df)}")
print(
    f"列名: {all_stocks_df.columns.tolist() if hasattr(all_stocks_df, 'columns') else 'N/A'}"
)
print(
    f"前5行:\n{all_stocks_df.head() if hasattr(all_stocks_df, 'head') else all_stocks_df[:5]}"
)

if hasattr(all_stocks_df, "order_book_id"):
    stocks = all_stocks_df["order_book_id"].tolist()
elif isinstance(all_stocks_df, pd.DataFrame):
    stocks = all_stocks_df.index.tolist()
else:
    stocks = list(all_stocks_df)

print(f"\n股票数量: {len(stocks)}")
print(f"前5只: {stocks[:5]}")

print("\n测试完成")
