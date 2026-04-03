# -*- coding: utf-8 -*-
"""
Debug get_price format in RiceQuant Notebook
"""

print("=" * 60)
print("Debug get_price format")
print("=" * 60)

import pandas as pd
import numpy as np

stocks = index_components("000905.XSHG", "2024-01-01")[:5]
print(f"Test stocks: {stocks}")

df = get_price(
    stocks,
    start_date="2024-01-01",
    end_date="2024-01-10",
    frequency="1d",
    fields=["close", "high", "low", "open"],
)

print(f"\nType: {type(df)}")
print(f"Shape: {df.shape}")
print(f"Index type: {type(df.index)}")
print(f"Index name(s): {df.index.names}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst 3 rows:")
print(df.head(3))
print(f"\nLast 3 rows:")
print(df.tail(3))

# Check if index is MultiIndex
if isinstance(df.index, pd.MultiIndex):
    print("\nMultiIndex detected")
    print(f"Level 0 (dates): {df.index.get_level_values(0).unique()[:5]}")
    print(f"Level 1 (stocks): {df.index.get_level_values(1).unique()}")
else:
    print("\nNOT MultiIndex - checking columns for stock info...")
    print(f"Index dtype: {df.index.dtype}")
    print(f"Index sample: {df.index[:5]}")

# Try single stock
print("\n\n--- Single stock test ---")
df1 = get_price(
    stocks[0],
    start_date="2024-01-01",
    end_date="2024-01-10",
    frequency="1d",
    fields=["close"],
)
print(f"Type: {type(df1)}")
print(f"Shape: {df1.shape}")
print(f"Index: {df1.index[:3]}")
print(f"Columns: {df1.columns.tolist() if hasattr(df1, 'columns') else 'N/A'}")
print(df1.head(3))
