"""
JoinQuant 数据源测试脚本

测试所有可用方法的功能和返回结果。

运行方式:
    node run-strategy.js --strategy data_source/test_joinquant_data.py --timeout-ms 120000

    # 或在 Notebook 中直接运行
"""

from jqdata import *
import pandas as pd
from datetime import datetime

# 导入执行器
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from joinquant_data_executor import JoinQuantDataExecutor

# 创建执行器实例
executor = JoinQuantDataExecutor()

print("=" * 60)
print("JoinQuant 数据源测试")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# ============================================================
# 测试配置
# ============================================================

TEST_STOCK = '000001.XSHE'
TEST_STOCKS = ['000001.XSHE', '000002.XSHE', '000004.XSHE']
TEST_DATE = '2024-01-02'
TEST_END_DATE = '2024-01-10'
TEST_INDEX = '000300.XSHG'  # 沪深300

# ============================================================
# 测试函数
# ============================================================

def test_and_print(name, func, *args, **kwargs):
    """测试并打印结果"""
    print(f"\n[测试] {name}")
    print("-" * 40)
    try:
        result = func(*args, **kwargs)
        if result is None:
            print("  结果: None")
            return ('success', 'None')
        elif isinstance(result, pd.DataFrame):
            print(f"  类型: DataFrame")
            print(f"  形状: {result.shape}")
            print(f"  列名: {list(result.columns)[:10]}...")  # 只显示前10列
            print(f"  前3行:")
            print(result.head(3).to_string())
            return ('success', f'DataFrame({result.shape[0]}x{result.shape[1]})')
        elif isinstance(result, (list, dict)):
            print(f"  类型: {type(result).__name__}")
            if isinstance(result, list):
                print(f"  长度: {len(result)}")
                print(f"  前5项: {result[:5]}")
            elif isinstance(result, dict):
                print(f"  键: {list(result.keys())[:10]}...")
            return ('success', f'{type(result).__name__}({len(result) if hasattr(result, "__len__") else "N/A"})')
        else:
            print(f"  类型: {type(result).__name__}")
            print(f"  结果: {str(result)[:100]}...")
            return ('success', str(result)[:50])
    except Exception as e:
        print(f"  错误: {str(e)}")
        return ('error', str(e))


# ============================================================
# 执行测试
# ============================================================

results = []

# 第一类：行情数据
print("\n" + "=" * 60)
print("第一类：行情数据")
print("=" * 60)

r = test_and_print("get_stock_daily", executor.get_stock_daily, TEST_STOCK, count=5)
results.append(("get_stock_daily", r))

r = test_and_print("get_stock_daily_batch", executor.get_stock_daily_batch, TEST_STOCKS, count=5)
results.append(("get_stock_daily_batch", r))

r = test_and_print("get_stock_minute", executor.get_stock_minute, TEST_STOCK, TEST_DATE, "5min")
results.append(("get_stock_minute", r))

r = test_and_print("get_call_auction", executor.get_call_auction, TEST_STOCK, TEST_DATE)
results.append(("get_call_auction", r))

# 第二类：估值数据
print("\n" + "=" * 60)
print("第二类：估值数据")
print("=" * 60)

r = test_and_print("get_valuation", executor.get_valuation, TEST_STOCK)
results.append(("get_valuation", r))

r = test_and_print("get_index_valuation", executor.get_index_valuation, TEST_INDEX)
results.append(("get_index_valuation", r))

# 第三类：财务数据
print("\n" + "=" * 60)
print("第三类：财务数据")
print("=" * 60)

r = test_and_print("get_finance_indicators", executor.get_finance_indicators, TEST_STOCK, TEST_DATE, TEST_END_DATE)
results.append(("get_finance_indicators", r))

r = test_and_print("get_dividend", executor.get_dividend, TEST_STOCK)
results.append(("get_dividend", r))

# 第四类：指数与行业
print("\n" + "=" * 60)
print("第四类：指数与行业")
print("=" * 60)

r = test_and_print("get_index_daily", executor.get_index_daily, TEST_INDEX, count=5)
results.append(("get_index_daily", r))

r = test_and_print("get_index_components", executor.get_index_components, TEST_INDEX, TEST_DATE)
results.append(("get_index_components", r))

r = test_and_print("get_industry_list", executor.get_industry_list)
results.append(("get_industry_list", r))

r = test_and_print("get_industry_classification", executor.get_industry_classification, TEST_STOCKS[:2])
results.append(("get_industry_classification", r))

# 第五类：宏观与情绪
print("\n" + "=" * 60)
print("第五类：宏观与情绪")
print("=" * 60)

r = test_and_print("get_market_spot", executor.get_market_spot, TEST_DATE)
results.append(("get_market_spot", r))

r = test_and_print("get_money_flow", executor.get_money_flow, TEST_STOCK, TEST_DATE, TEST_END_DATE)
results.append(("get_money_flow", r))

r = test_and_print("get_analyst_forecast", executor.get_analyst_forecast, TEST_STOCK)
results.append(("get_analyst_forecast", r))

r = test_and_print("get_shareholder_data", executor.get_shareholder_data, TEST_STOCK)
results.append(("get_shareholder_data", r))

# 第六类：辅助数据
print("\n" + "=" * 60)
print("第六类：辅助数据")
print("=" * 60)

r = test_and_print("get_trading_calendar", executor.get_trading_calendar, '2024-01-01', '2024-01-10')
results.append(("get_trading_calendar", r))

r = test_and_print("get_stock_info", executor.get_stock_info, TEST_STOCK)
results.append(("get_stock_info", r))

# 第七类：交易事件
print("\n" + "=" * 60)
print("第七类：交易事件")
print("=" * 60)

r = test_and_print("get_dragon_tiger_list", executor.get_dragon_tiger_list, TEST_DATE)
results.append(("get_dragon_tiger_list", r))

r = test_and_print("get_restricted_release", executor.get_restricted_release, '2024-01-01', '2024-03-01')
results.append(("get_restricted_release", r))

# 第九类：板块与概念
print("\n" + "=" * 60)
print("第九类：板块与概念")
print("=" * 60)

r = test_and_print("get_concept_list", executor.get_concept_list)
results.append(("get_concept_list", r))

r = test_and_print("get_stock_industry", executor.get_stock_industry, TEST_STOCK)
results.append(("get_stock_industry", r))

r = test_and_print("get_st_stocks", executor.get_st_stocks)
results.append(("get_st_stocks", r))

# 第十类：基金与可转债
print("\n" + "=" * 60)
print("第十类：基金与可转债")
print("=" * 60)

r = test_and_print("get_etf_list", executor.get_etf_list)
results.append(("get_etf_list", r))

r = test_and_print("get_convert_bond_list", executor.get_convert_bond_list)
results.append(("get_convert_bond_list", r))

# 第十一类：因子数据
print("\n" + "=" * 60)
print("第十一类：因子数据")
print("=" * 60)

r = test_and_print("get_all_factors", executor.get_all_factors)
results.append(("get_all_factors", r))

r = test_and_print("get_factor_kanban_values", executor.get_factor_kanban_values, 'hs300', 'month_3', 'long_only', ['quality', 'basics'])
results.append(("get_factor_kanban_values", r))

# 其他常用API
print("\n" + "=" * 60)
print("其他常用API")
print("=" * 60)

r = test_and_print("get_all_securities", executor.get_all_securities, ['stock'], TEST_DATE)
results.append(("get_all_securities", r))

r = test_and_print("get_trade_days", executor.get_trade_days, '2024-01-01', '2024-01-10')
results.append(("get_trade_days", r))

# ============================================================
# 测试结果汇总
# ============================================================

print("\n" + "=" * 60)
print("测试结果汇总")
print("=" * 60)

success_count = sum(1 for _, (status, _) in results if status == 'success')
error_count = sum(1 for _, (status, _) in results if status == 'error')

print(f"\n总计: {len(results)} 个测试")
print(f"成功: {success_count}")
print(f"失败: {error_count}")

print("\n详细结果:")
for name, (status, msg) in results:
    icon = '✓' if status == 'success' else '✗'
    print(f"  {icon} {name}: {msg}")

print(f"\n测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")