"""
JoinQuant API 测试脚本

测试所有 API 接口的调用和返回结果。
运行方式:
    node run-api-call.js --function test_all --params '{"mode":"quick"}'

    # 或直接运行测试
    node run-strategy.js --strategy data/test_all_apis.py
"""

from jqdata import *
import pandas as pd
from datetime import datetime, timedelta

# ============================================================
# 测试配置
# ============================================================

# 测试用的股票代码
TEST_STOCKS = ['000001.XSHE', '000002.XSHE', '000004.XSHE']
TEST_DATE = '2024-01-02'
TEST_END_DATE = '2024-01-10'

# ============================================================
# 测试函数
# ============================================================

def test_resultPrinter(name, df_or_result):
    """格式化打印测试结果"""
    print(f"\n{'='*60}")
    print(f"测试: {name}")
    print(f"{'='*60}")

    if df_or_result is None:
        print("  结果: None")
        return False

    if isinstance(df_or_result, pd.DataFrame):
        print(f"  类型: DataFrame")
        print(f"  形状: {df_or_result.shape}")
        print(f"  列名: {list(df_or_result.columns)}")
        print(f"  前3行:")
        print(df_or_result.head(3).to_string())
        return True
    elif isinstance(df_or_result, (list, dict, pd.Series)):
        print(f"  类型: {type(df_or_result).__name__}")
        if isinstance(df_or_result, list):
            print(f"  长度: {len(df_or_result)}")
            print(f"  前5项: {df_or_result[:5]}")
        elif isinstance(df_or_result, dict):
            print(f"  键: {list(df_or_result.keys())[:10]}")
        elif isinstance(df_or_result, pd.Series):
            print(f"  长度: {len(df_or_result)}")
            print(f"  前5项: {df_or_result.head().to_string()}")
        return True
    else:
        print(f"  类型: {type(df_or_result).__name__}")
        print(f"  结果: {str(df_or_result)[:200]}")
        return True


def run_tests(mode='full'):
    """运行所有测试

    Args:
        mode: 'full' - 完整测试, 'quick' - 快速测试(只测核心接口)
    """
    results = {}

    if mode == 'quick':
        # 快速测试 - 只测核心接口
        print("\n" + "="*60)
        print("快速测试模式 - 核心接口")
        print("="*60)

        tests = [
            ("get_all_securities", lambda: get_all_securities(['stock'], TEST_DATE)),
            ("get_price_single", lambda: get_price('000001.XSHE', count=5, end_date=TEST_END_DATE, frequency='daily')),
            ("get_trade_days", lambda: get_trade_days(start_date='2024-01-01', end_date='2024-01-10')),
        ]
    else:
        # 完整测试
        print("\n" + "="*60)
        print("完整测试模式 - 所有接口")
        print("="*60)

        tests = [
            # ============================================================
            # 第一类：行情数据
            # ============================================================
            ("get_all_securities_stock", lambda: get_all_securities(['stock'], TEST_DATE)),
            ("get_all_securities_etf", lambda: get_all_securities(['etf'])),
            ("get_all_securities_index", lambda: get_all_securities(['index'])),

            ("get_price_single", lambda: get_price('000001.XSHE', count=5, end_date=TEST_END_DATE, frequency='daily')),
            ("get_price_multi", lambda: get_price(TEST_STOCKS, count=5, end_date=TEST_END_DATE, frequency='daily')),
            ("get_price_fields", lambda: get_price('000001.XSHE', count=3, end_date=TEST_END_DATE, frequency='daily',
                                                    fields=['open', 'close', 'high', 'low', 'volume', 'money'])),
            ("get_price_fq_none", lambda: get_price('000001.XSHE', count=3, end_date=TEST_END_DATE, frequency='daily', fq='none')),

            ("get_bars", lambda: get_bars('000001.XSHE', count=10, end_dt=TEST_DATE+' 15:00:00', unit='5m', df=True)),
            ("get_call_auction", lambda: get_call_auction('000001.XSHE', start_date=TEST_DATE, end_date=TEST_DATE)),

            # ============================================================
            # 第二类：估值数据
            # ============================================================
            ("get_valuation_history", lambda: get_price('000001.XSHE', count=5, end_date=TEST_END_DATE, frequency='daily',
                                                         fields=['close', 'volume', 'money'])),

            # ============================================================
            # 第三类：财务数据
            # ============================================================
            ("get_fundamentals", lambda: get_fundamentals('000001.XSHE', date=TEST_DATE)),
            ("get_financial_indicator", lambda: finance.run_query(
                query(finance.FINANCIAL_INDICATOR).filter(
                    finance.FINANCIAL_INDICATOR.code == '000001.XSHE'
                ).limit(5)
            )),

            # ============================================================
            # 第四类：指数与行业
            # ============================================================
            ("get_index_stocks_hs300", lambda: get_index_stocks('000300.XSHG')),
            ("get_index_stocks_zz500", lambda: get_index_stocks('000905.XSHG')),
            ("get_industry", lambda: get_industry('000001.XSHE')),
            ("get_industry_stocks", lambda: get_industry_stocks('801010')[:5] if hasattr(get_industry_stocks, '__call__') else []),

            # ============================================================
            # 第五类：宏观与情绪
            # ============================================================
            ("get_money_flow", lambda: get_money_flow('000001.XSHE', start_date='2024-01-01', end_date='2024-01-10')),
            ("get_billboard_list", lambda: get_billboard_list(date=TEST_DATE)),

            # ============================================================
            # 第六类：辅助数据
            # ============================================================
            ("get_trade_days", lambda: get_trade_days(start_date='2024-01-01', end_date='2024-01-10')),
            ("get_trade_days_count", lambda: get_trade_days(count=10)),

            # ============================================================
            # 第七类：交易事件
            # ============================================================
            ("get_locked_shares", lambda: get_locked_shares(start_date='2024-01-01', end_date='2024-03-01')),

            # ============================================================
            # 第八类：公司事件 (使用 finance 表)
            # ============================================================
            ("finance_equity_pledge", lambda: finance.run_query(
                query(finance.STK_EQUITY_PLEDGE).filter(
                    finance.STK_EQUITY_PLEDGE.code == '000001.XSHE'
                ).limit(5)
            ) if hasattr(finance, 'STK_EQUITY_PLEDGE') else pd.DataFrame()),

            # ============================================================
            # 第九类：板块与概念
            # ============================================================
            ("get_concept_stocks", lambda: get_concept_stocks('ARJ')[:5] if callable(get_concept_stocks) else []),

            # ============================================================
            # 第十类：基金与可转债
            # ============================================================
            ("get_etf_daily", lambda: get_price('510300.XSHG', count=5, end_date=TEST_END_DATE, frequency='daily')),
            ("get_convert_bond_daily", lambda: get_price('113009.XSHG', count=5, end_date=TEST_END_DATE, frequency='daily')),

            # ============================================================
            # 第十一类：因子数据
            # ============================================================
            ("get_all_factors", lambda: get_all_factors()),
            ("get_factor_kanban_values", lambda: get_factor_kanban_values(
                universe='hs300', bt_cycle='month_3', model='long_only',
                category=['quality', 'basics'], skip_paused=False, commision_slippage=0
            )),

            # ============================================================
            # 第十二类：股东深度
            # ============================================================
            ("finance_shareholder_change", lambda: finance.run_query(
                query(finance.STK_SHAREHOLDER_CHANGE).filter(
                    finance.STK_SHAREHOLDER_CHANGE.code == '000001.XSHE'
                ).limit(5)
            ) if hasattr(finance, 'STK_SHAREHOLDER_CHANGE') else pd.DataFrame()),
        ]

    print(f"\n共 {len(tests)} 个测试\n")

    for i, (name, test_func) in enumerate(tests, 1):
        print(f"[{i}/{len(tests)}] {name}...", end=" ")
        try:
            result = test_func()
            success = test_resultPrinter(name, result)
            results[name] = {'status': 'success' if success else 'empty', 'result': result}
            print(f"  -> {'OK' if success else 'EMPTY'}")
        except Exception as e:
            print(f"  -> FAIL: {str(e)[:100]}")
            results[name] = {'status': 'error', 'error': str(e)}

    # ============================================================
    # 测试结果汇总
    # ============================================================
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)

    success_count = sum(1 for r in results.values() if r['status'] == 'success')
    empty_count = sum(1 for r in results.values() if r['status'] == 'empty')
    error_count = sum(1 for r in results.values() if r['status'] == 'error')

    print(f"\n成功: {success_count}")
    print(f"空结果: {empty_count}")
    print(f"错误: {error_count}")

    print("\n详细结果:")
    for name, result in sorted(results.items()):
        status_icon = {'success': '✓', 'empty': '-', 'error': '✗'}[result['status']]
        if result['status'] == 'error':
            print(f"  {status_icon} {name}: {result['error'][:80]}")
        else:
            print(f"  {status_icon} {name}")

    return results


# ============================================================
# 主程序入口
# ============================================================

if __name__ == '__main__':
    import sys

    mode = 'full'
    if len(sys.argv) > 1:
        if 'quick' in sys.argv[1].lower():
            mode = 'quick'

    print(f"""
    ============================================================
    JoinQuant API 完整测试
    模式: {mode}
    ============================================================
    """)

    results = run_tests(mode=mode)

    print(f"\n测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")