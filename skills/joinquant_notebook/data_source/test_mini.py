"""Minimal test"""
from jqdata import *
from datetime import datetime

print("=== JQ API Test ===")

# Test 1
print("1. get_price...")
df = get_price('000001.XSHE', count=3, frequency='daily')
print(f"  OK: {df.shape}")

# Test 2
print("2. get_all_securities...")
df = get_all_securities(['stock'], '2024-01-02')
print(f"  OK: {len(df)} stocks")

# Test 3
print("3. get_trade_days...")
dates = get_trade_days('2024-01-01', '2024-01-10')
print(f"  OK: {len(dates)} days")

# Test 4
print("4. get_index_stocks...")
stocks = get_index_stocks('000300.XSHG')
print(f"  OK: {len(stocks)} stocks")

# Test 5
print("5. get_industry...")
ind = get_industry('000001.XSHE')
print(f"  OK: {ind}")

# Test 6
print("6. get_money_flow...")
df = get_money_flow('000001.XSHE', '2024-01-02', '2024-01-05')
print(f"  OK: {df.shape}")

print("=== All OK ===")
print(datetime.now())