"""
test_task32_direct.py
直接测试分钟数据 API（绕过包导入问题）
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src")
)

import pandas as pd
from datetime import datetime

print("=" * 80)
print("任务32: 分钟数据 API 直接验证")
print("=" * 80)

print("\n1. 测试 DuckDB 缓存...")
from jk2bt.db.duckdb_manager import DuckDBManager

db = DuckDBManager(read_only=True)
with db._get_connection(read_only=True) as conn:
    tables = conn.execute("SHOW TABLES").fetchall()
    print(f"  可用表: {[t[0] for t in tables]}")

    count = conn.execute("SELECT COUNT(*) FROM stock_minute").fetchone()[0]
    print(f"  stock_minute 行数: {count}")

    if count > 0:
        sample = conn.execute("""
            SELECT symbol, period, adjust, MIN(datetime) as start_time, MAX(datetime) as end_time, COUNT(*) as cnt
            FROM stock_minute
            GROUP BY symbol, period, adjust
            ORDER BY cnt DESC
            LIMIT 5
        """).fetchall()
        print("\n  数据分布:")
        for row in sample:
            print(
                f"    {row[0]} (period={row[1]}, adjust={row[2]}): {row[3]} ~ {row[4]} ({row[5]} 条)"
            )

print("\n2. 测试 minute.py 直接调用...")
try:
    from market_data.minute import get_stock_minute

    df_1m = get_stock_minute(
        "sh600000", "2025-03-28 09:30:00", "2025-03-28 15:00:00", period="1m"
    )
    print(f"  1m 数据: {len(df_1m)} 条")
    if len(df_1m) > 0:
        print(f"    列: {list(df_1m.columns)}")
        print(f"    首条: {df_1m.iloc[0].to_dict()}")

    df_5m = get_stock_minute(
        "sh600000", "2025-03-28 09:30:00", "2025-03-28 15:00:00", period="5m"
    )
    print(f"  5m 数据: {len(df_5m)} 条")
    if len(df_5m) > 0:
        print(f"    列: {list(df_5m.columns)}")
        print(f"    首条: {df_5m.iloc[0].to_dict()}")

except Exception as e:
    print(f"  ✗ 失败: {e}")

print("\n3. 测试 market_api.py 分钟数据...")
try:
    from jk2bt.api.market import get_price

    df = get_price(
        security="600000.XSHG",
        start_date="2026-03-25 09:30:00",
        end_date="2026-03-30 15:00:00",
        frequency="5m",
        fields=["open", "high", "low", "close", "volume", "money"],
        fq="pre",
    )

    if df is not None and not df.empty:
        print(f"  ✓ get_price(5m) 成功: {len(df)} 条")
        print(f"    列: {list(df.columns)}")
        print(f"    时间范围: {df['datetime'].min()} ~ {df['datetime'].max()}")
        print(f"    部分数据:")
        print(df.head(3))
    else:
        print(f"  ✗ get_price(5m) 返回空数据")

except Exception as e:
    print(f"  ✗ 异常: {e}")

print("\n4. 测试 history/attribute_history/get_bars...")
try:
    from jk2bt.api.market import history, attribute_history, get_bars

    df_history = history(
        50, "5m", "close", ["600000.XSHG"], end_date="2025-03-28 15:00:00"
    )
    if not df_history.empty:
        print(f"  ✓ history(5m) 成功: {df_history.shape}")
        print(df_history.head(3))
    else:
        print(f"  ✗ history(5m) 返回空")

    df_attr = attribute_history(
        "600000.XSHG", 50, "5m", ["open", "close"], end_date="2025-03-28 15:00:00"
    )
    if not df_attr.empty:
        print(f"  ✓ attribute_history(5m) 成功: {df_attr.shape}")
        print(df_attr.head(3))
    else:
        print(f"  ✗ attribute_history(5m) 返回空")

    df_bars = get_bars(
        "600000.XSHG", 50, "5m", ["open", "close"], end_dt="2025-03-28 15:00:00"
    )
    if not df_bars.empty:
        print(f"  ✓ get_bars(5m) 成功: {df_bars.shape}")
        print(df_bars.head(3))
    else:
        print(f"  ✗ get_bars(5m) 返回空")

except Exception as e:
    print(f"  ✗ 异常: {e}")

print("\n" + "=" * 80)
print("任务32 完成")
print("=" * 80)
