"""
JoinQuant 数据源测试脚本

测试所有可用方法的功能和返回结果。

运行方式:
    node run-strategy.js --strategy data_source/test_joinquant_data.py --timeout-ms 180000
"""

from jqdata import *
import pandas as pd
from datetime import datetime

# ============================================================
# 执行器类（内联版本）
# ============================================================

class JoinQuantDataExecutor:
    """JoinQuant 数据执行器"""

    def __init__(self):
        self.name = "JoinQuant"
        self.version = "1.0"

    def get_stock_daily(self, symbol, start_date=None, end_date=None, count=None, adjust="qfq"):
        fq_map = {"qfq": "pre", "hfq": "post", "none": "none"}
        fq = fq_map.get(adjust, "pre")
        df = get_price(security=symbol, start_date=start_date, end_date=end_date, count=count,
                       frequency='daily', fields=['open', 'close', 'high', 'low', 'volume', 'money'],
                       skip_paused=False, fq=fq)
        return df

    def get_stock_daily_batch(self, symbols, start_date=None, end_date=None, count=None, adjust="qfq"):
        fq_map = {"qfq": "pre", "hfq": "post", "none": "none"}
        fq = fq_map.get(adjust, "pre")
        df = get_price(security=symbols, start_date=start_date, end_date=end_date, count=count,
                       frequency='daily', fields=['open', 'close', 'high', 'low', 'volume', 'money'],
                       skip_paused=False, fq=fq)
        return df

    def get_stock_minute(self, symbol, date, freq="5min"):
        unit = freq.replace("min", "m")
        df = get_bars(security=symbol, count=100, end_dt=date + " 15:00:00", unit=unit,
                      fields=['open', 'close', 'high', 'low', 'volume', 'money', 'date'], df=True)
        if df is not None and not df.empty:
            df['amount'] = df['money']
        return df

    def get_call_auction(self, symbol, date):
        return get_call_auction(security=symbol, start_date=date, end_date=date)

    def get_valuation(self, symbol, start_date=None, end_date=None):
        q = query(finance.PUBLIC_YIELD_HISTORY).filter(finance.PUBLIC_YIELD_HISTORY.code == symbol)
        if start_date:
            q = q.filter(finance.PUBLIC_YIELD_HISTORY.date >= start_date)
        if end_date:
            q = q.filter(finance.PUBLIC_YIELD_HISTORY.date <= end_date)
        df = finance.run_query(q)
        if df is not None and not df.empty:
            df = df.set_index('date')
        return df

    def get_index_valuation(self, index_symbol, start_date=None, end_date=None):
        stocks = get_index_stocks(index_symbol)
        valuations = []
        for sym in stocks[:100]:
            df = self.get_valuation(sym, start_date, end_date)
            if df is not None and not df.empty:
                valuations.append(df)
        if valuations:
            combined = pd.concat(valuations)
            return combined.groupby(combined.index).mean()
        return pd.DataFrame()

    def get_finance_indicators(self, symbol, start_date=None, end_date=None):
        q = query(finance.FINANCIAL_INDICATOR).filter(finance.FINANCIAL_INDICATOR.code == symbol)
        if start_date:
            q = q.filter(finance.FINANCIAL_INDICATOR.pubDate >= start_date)
        if end_date:
            q = q.filter(finance.FINANCIAL_INDICATOR.pubDate <= end_date)
        df = finance.run_query(q)
        if df is not None and not df.empty:
            df = df.set_index('pubDate')
        return df

    def get_dividend(self, symbol):
        q = query(finance.STK_DIVIDEND).filter(finance.STK_DIVIDEND.code == symbol)
        df = finance.run_query(q)
        if df is not None and not df.empty:
            df = df.set_index('pub_date')
        return df

    def get_index_daily(self, symbol, start_date=None, end_date=None, count=None):
        df = get_price(security=symbol, start_date=start_date, end_date=end_date, count=count,
                       frequency='daily', fields=['open', 'close', 'high', 'low', 'volume', 'money'],
                       skip_paused=False, fq='none')
        if df is not None:
            df = df.rename(columns={'money': 'amount'})
        return df

    def get_index_components(self, index_symbol, date):
        stocks = get_index_stocks(index_symbol, date=date)
        return list(stocks) if stocks is not None else []

    def get_industry_list(self, level="sw_l1"):
        industries = get_industry()
        return list(industries.keys()) if industries else []

    def get_industry_classification(self, symbols, level="sw_l1"):
        result = []
        for sym in symbols:
            industry = get_industry(sym)
            if industry:
                result.append({
                    'symbol': sym,
                    'industry': list(industry.values())[0] if industry else None,
                    'industry_code': list(industry.keys())[0] if industry else None
                })
        return pd.DataFrame(result)

    def get_market_spot(self, date):
        stocks = list(get_all_securities(['stock'], date).index)
        df = get_price(security=stocks, start_date=date, end_date=date, count=1,
                       frequency='daily', fields=['close', 'volume', 'money'],
                       skip_paused=False, fq='pre')
        return df

    def get_money_flow(self, symbol, start_date=None, end_date=None):
        return get_money_flow(securities=symbol, start_date=start_date, end_date=end_date)

    def get_analyst_forecast(self, symbol, start_date=None, end_date=None):
        q = query(finance.ANALYST_PREDICT).filter(finance.ANALYST_PREDICT.code == symbol)
        if start_date:
            q = q.filter(finance.ANALYST_PREDICT.pubDate >= start_date)
        if end_date:
            q = q.filter(finance.ANALYST_PREDICT.pubDate <= end_date)
        df = finance.run_query(q)
        if df is not None and not df.empty:
            df = df.set_index('pubDate')
        return df

    def get_shareholder_data(self, symbol, start_date=None, end_date=None):
        q = query(finance.STK_SHAREHOLDER_NUM).filter(finance.STK_SHAREHOLDER_NUM.code == symbol)
        if start_date:
            q = q.filter(finance.STK_SHAREHOLDER_NUM.pubDate >= start_date)
        if end_date:
            q = q.filter(finance.STK_SHAREHOLDER_NUM.pubDate <= end_date)
        df = finance.run_query(q)
        if df is not None and not df.empty:
            df = df.set_index('pubDate')
        return df

    def get_trading_calendar(self, start_date=None, end_date=None):
        return get_trade_days(start_date=start_date, end_date=end_date)

    def get_stock_info(self, symbol):
        df = get_all_securities(['stock'])
        if symbol in df.index:
            info = df.loc[symbol]
            return {
                'name': info.get('display_name', ''),
                'list_date': info.get('start_date', None),
            }
        return {}

    def get_dragon_tiger_list(self, date):
        return get_billboard_list(date=date)

    def get_restricted_release(self, start_date=None, end_date=None):
        return get_locked_shares(start_date=start_date, end_date=end_date)

    def get_concept_list(self):
        concepts = get_security_lists(type='concept')
        return concepts if concepts is not None else pd.DataFrame()

    def get_concept_constituents(self, concept_code):
        stocks = get_concept_stocks(concept_code)
        return pd.DataFrame({'symbol': list(stocks)}) if stocks is not None else pd.DataFrame()

    def get_stock_industry(self, symbol):
        industry = get_industry(symbol)
        return industry if industry else {}

    def get_st_stocks(self):
        df = get_all_securities(['stock'])
        return df[df['display_name'].str.contains('ST|星', na=False)].index.tolist()

    def get_etf_list(self):
        return get_all_securities(['etf'])

    def get_convert_bond_list(self):
        return get_all_securities(['conbond'])

    def get_all_factors(self):
        return get_all_factors()

    def get_factor_kanban_values(self, universe='hs300', bt_cycle='month_3', model='long_only',
                                 category=None, skip_paused=False, commision_slippage=0):
        if category is None:
            category = ['quality', 'basics']
        return get_factor_kanban_values(universe=universe, bt_cycle=bt_cycle, model=model,
                                        category=category, skip_paused=skip_paused,
                                        commision_slippage=commision_slippage)

    def get_all_securities(self, types=None, date=None):
        if types is None:
            types = ['stock']
        return get_all_securities(types, date)

    def get_trade_days(self, start_date=None, end_date=None, count=None):
        return get_trade_days(start_date=start_date, end_date=end_date, count=count)


# ============================================================
# 测试执行
# ============================================================

executor = JoinQuantDataExecutor()

print("=" * 60)
print("JoinQuant 数据源测试")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# 测试配置
TEST_STOCK = '000001.XSHE'
TEST_STOCKS = ['000001.XSHE', '000002.XSHE']
TEST_DATE = '2024-01-02'
TEST_END_DATE = '2024-01-10'
TEST_INDEX = '000300.XSHG'

def test_and_print(name, func, *args, **kwargs):
    print(f"\n[测试] {name}")
    print("-" * 40)
    try:
        result = func(*args, **kwargs)
        if result is None:
            print("  结果: None")
            return ('success', 'None')
        elif isinstance(result, pd.DataFrame):
            print(f"  类型: DataFrame, 形状: {result.shape}")
            print(f"  列名: {list(result.columns)[:8]}...")
            print(f"  前2行:\n{result.head(2).to_string()}")
            return ('success', f'DataFrame({result.shape[0]}x{result.shape[1]})')
        elif isinstance(result, (list, dict)):
            print(f"  类型: {type(result).__name__}, 长度: {len(result) if hasattr(result, '__len__') else 'N/A'}")
            if isinstance(result, list):
                print(f"  前5项: {result[:5]}")
            elif isinstance(result, dict):
                print(f"  键: {list(result.keys())[:8]}...")
            return ('success', f'{type(result).__name__}')
        else:
            print(f"  类型: {type(result).__name__}")
            print(f"  结果: {str(result)[:100]}...")
            return ('success', str(result)[:50])
    except Exception as e:
        print(f"  错误: {str(e)}")
        return ('error', str(e))

results = []

# 测试各方法
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

print("\n" + "=" * 60)
print("第二类：估值数据")
print("=" * 60)

r = test_and_print("get_valuation", executor.get_valuation, TEST_STOCK)
results.append(("get_valuation", r))

r = test_and_print("get_index_valuation", executor.get_index_valuation, TEST_INDEX)
results.append(("get_index_valuation", r))

print("\n" + "=" * 60)
print("第三类：财务数据")
print("=" * 60)

r = test_and_print("get_finance_indicators", executor.get_finance_indicators, TEST_STOCK)
results.append(("get_finance_indicators", r))

r = test_and_print("get_dividend", executor.get_dividend, TEST_STOCK)
results.append(("get_dividend", r))

print("\n" + "=" * 60)
print("第四类：指数与行业")
print("=" * 60)

r = test_and_print("get_index_daily", executor.get_index_daily, TEST_INDEX, count=5)
results.append(("get_index_daily", r))

r = test_and_print("get_index_components", executor.get_index_components, TEST_INDEX, TEST_DATE)
results.append(("get_index_components", r))

r = test_and_print("get_industry_list", executor.get_industry_list)
results.append(("get_industry_list", r))

r = test_and_print("get_industry_classification", executor.get_industry_classification, TEST_STOCKS)
results.append(("get_industry_classification", r))

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

print("\n" + "=" * 60)
print("第六类：辅助数据")
print("=" * 60)

r = test_and_print("get_trading_calendar", executor.get_trading_calendar, '2024-01-01', '2024-01-10')
results.append(("get_trading_calendar", r))

r = test_and_print("get_stock_info", executor.get_stock_info, TEST_STOCK)
results.append(("get_stock_info", r))

print("\n" + "=" * 60)
print("第七类：交易事件")
print("=" * 60)

r = test_and_print("get_dragon_tiger_list", executor.get_dragon_tiger_list, TEST_DATE)
results.append(("get_dragon_tiger_list", r))

r = test_and_print("get_restricted_release", executor.get_restricted_release, '2024-01-01', '2024-03-01')
results.append(("get_restricted_release", r))

print("\n" + "=" * 60)
print("第九类：板块与概念")
print("=" * 60)

r = test_and_print("get_concept_list", executor.get_concept_list)
results.append(("get_concept_list", r))

r = test_and_print("get_stock_industry", executor.get_stock_industry, TEST_STOCK)
results.append(("get_stock_industry", r))

r = test_and_print("get_st_stocks", executor.get_st_stocks)
results.append(("get_st_stocks", r))

print("\n" + "=" * 60)
print("第十类：基金与可转债")
print("=" * 60)

r = test_and_print("get_etf_list", executor.get_etf_list)
results.append(("get_etf_list", r))

r = test_and_print("get_convert_bond_list", executor.get_convert_bond_list)
results.append(("get_convert_bond_list", r))

print("\n" + "=" * 60)
print("第十一类：因子数据")
print("=" * 60)

r = test_and_print("get_all_factors", executor.get_all_factors)
results.append(("get_all_factors", r))

r = test_and_print("get_factor_kanban_values", executor.get_factor_kanban_values, 'hs300', 'month_3', 'long_only', ['quality', 'basics'])
results.append(("get_factor_kanban_values", r))

print("\n" + "=" * 60)
print("其他常用API")
print("=" * 60)

r = test_and_print("get_all_securities", executor.get_all_securities, ['stock'], TEST_DATE)
results.append(("get_all_securities", r))

r = test_and_print("get_trade_days", executor.get_trade_days, '2024-01-01', '2024-01-10')
results.append(("get_trade_days", r))

# 结果汇总
print("\n" + "=" * 60)
print("测试结果汇总")
print("=" * 60)

success = sum(1 for _, (s, _) in results if s == 'success')
error = sum(1 for _, (s, _) in results if s == 'error')

print(f"\n总计: {len(results)} 个测试")
print(f"成功: {success}, 失败: {error}")

print("\n详细结果:")
for name, (status, msg) in results:
    icon = '✓' if status == 'success' else '✗'
    print(f"  {icon} {name}: {msg}")

print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")