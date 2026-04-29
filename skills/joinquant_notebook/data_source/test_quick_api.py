"""
JoinQuant API 快速测试
"""
from jqdata import *
import pandas as pd
from datetime import datetime

print("=" * 50)
print("JoinQuant API 快速测试")
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print("=" * 50)

results = []

def test(name, func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        if result is None:
            print(f"✓ {name}: None")
            return ('ok', 'None')
        elif isinstance(result, pd.DataFrame):
            print(f"✓ {name}: DataFrame {result.shape}")
            return ('ok', f'DataFrame{result.shape}')
        elif isinstance(result, (list, dict)):
            print(f"✓ {name}: {type(result).__name__} len={len(result)}")
            return ('ok', f'{type(result).__name__}')
        else:
            print(f"✓ {name}: {type(result).__name__} = {str(result)[:50]}")
            return ('ok', str(result)[:30])
    except Exception as e:
        print(f"✗ {name}: {str(e)[:60]}")
        return ('fail', str(e)[:60])

# 核心 API 测试
print("\n--- 行情数据 ---")
results.append(test("get_stock_daily", get_price, '000001.XSHE', count=5, frequency='daily'))
results.append(test("get_all_securities", get_all_securities, ['stock'], '2024-01-02'))
results.append(test("get_trade_days", get_trade_days, '2024-01-01', '2024-01-10'))

print("\n--- 指数与行业 ---")
results.append(test("get_index_stocks", get_index_stocks, '000300.XSHG'))
results.append(test("get_industry", get_industry, '000001.XSHE'))

print("\n--- 因子数据 (需要 jqdatasdk) ---")
print("  - get_all_factors: skip")
print("  - get_factor_kanban: skip")

print("\n--- 资金流 ---")
results.append(test("get_money_flow", get_money_flow, '000001.XSHE', '2024-01-02', '2024-01-05'))

print("\n--- 龙虎榜 ---")
results.append(test("get_billboard_list", get_billboard_list, start_date='2024-01-02'))

# skip: get_locked_shares 太慢，跳过

# 汇总
print("\n" + "=" * 50)
ok = sum(1 for s, _ in results if s == 'ok')
fail = sum(1 for s, _ in results if s == 'fail')
print(f"结果: {ok} 成功, {fail} 失败")
print("=" * 50)