"""
JoinQuant 数据源执行器

在 JoinQuant Notebook 环境中执行数据获取操作。
通过 run-strategy.js 调用执行，返回原始结果。

使用方式:
    node run-strategy.js --cell-source "$(cat joinquant_data_executor.py)"

    # 或通过 CLI
    node joinquant_data_cli.js --function get_stock_daily --params '{"symbol":"000001.XSHE","count":5}'
"""

from jqdata import *
import json
import pandas as pd
from datetime import datetime, timedelta

# ============================================================
# 数据源执行器
# ============================================================

class JoinQuantDataExecutor:
    """JoinQuant 数据执行器"""

    def __init__(self):
        self.name = "JoinQuant"
        self.version = "1.0"

    # ============================================================
    # 第一类：行情数据
    # ============================================================

    def get_stock_daily(self, symbol, start_date=None, end_date=None, count=None, adjust="qfq"):
        """获取单只股票的日线行情数据"""
        fq_map = {"qfq": "pre", "hfq": "post", "none": "none"}
        fq = fq_map.get(adjust, "pre")

        df = get_price(
            security=symbol,
            start_date=start_date,
            end_date=end_date,
            count=count,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money', 'high_limit', 'low_limit', 'avg', 'pre_close', 'paused'],
            skip_paused=False,
            fq=fq
        )
        return df

    def get_stock_daily_batch(self, symbols, start_date=None, end_date=None, count=None, adjust="qfq"):
        """批量获取多只股票的日线行情数据"""
        fq_map = {"qfq": "pre", "hfq": "post", "none": "none"}
        fq = fq_map.get(adjust, "pre")

        df = get_price(
            security=symbols,
            start_date=start_date,
            end_date=end_date,
            count=count,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            skip_paused=False,
            fq=fq
        )
        return df

    def get_stock_minute(self, symbol, date, freq="5min"):
        """获取单只股票的分时行情数据"""
        unit = freq.replace("min", "m")

        df = get_bars(
            security=symbol,
            count=100,
            end_dt=date + " 15:00:00",
            unit=unit,
            fields=['open', 'close', 'high', 'low', 'volume', 'money', 'date'],
            df=True
        )
        if df is not None and not df.empty:
            df['amount'] = df['money']
        return df

    def get_call_auction(self, symbol, date):
        """获取单只股票的集合竞价数据"""
        df = get_call_auction(
            security=symbol,
            start_date=date,
            end_date=date
        )
        return df

    # ============================================================
    # 第二类：估值数据
    # ============================================================

    def get_valuation(self, symbol, start_date=None, end_date=None):
        """获取单只股票的估值数据"""
        from jqdatasdk import finance

        q = query(
            finance.PUBLIC_YIELD_HISTORY
        ).filter(
            finance.PUBLIC_YIELD_HISTORY.code == symbol
        )

        if start_date:
            q = q.filter(finance.PUBLIC_YIELD_HISTORY.date >= start_date)
        if end_date:
            q = q.filter(finance.PUBLIC_YIELD_HISTORY.date <= end_date)

        df = finance.run_query(q)

        if df is not None and not df.empty:
            df = df.set_index('date')

        return df

    def get_index_valuation(self, index_symbol, start_date=None, end_date=None):
        """获取指数的估值数据"""
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

    # ============================================================
    # 第三类：财务数据
    # ============================================================

    def get_financial(self, symbol, table="income", period="quarterly"):
        """获取单只股票的财务报表数据"""
        df = get_fundamentals(
            security=symbol,
            date=None,
            indicator=None
        )
        return df

    def get_finance_indicators(self, symbol, start_date=None, end_date=None):
        """获取单只股票的财务指标数据"""
        from jqdatasdk import finance

        q = query(finance.FINANCIAL_INDICATOR).filter(
            finance.FINANCIAL_INDICATOR.code == symbol
        )

        if start_date:
            q = q.filter(finance.FINANCIAL_INDICATOR.pubDate >= start_date)
        if end_date:
            q = q.filter(finance.FINANCIAL_INDICATOR.pubDate <= end_date)

        df = finance.run_query(q)

        if df is not None and not df.empty:
            df = df.set_index('pubDate')

        return df

    def get_dividend(self, symbol):
        """获取单只股票的分红送转数据"""
        from jqdatasdk import finance

        q = query(finance.STK_DIVIDEND).filter(
            finance.STK_DIVIDEND.code == symbol
        )

        df = finance.run_query(q)

        if df is not None and not df.empty:
            df = df.set_index('pub_date')

        return df

    # ============================================================
    # 第四类：指数与行业
    # ============================================================

    def get_index_daily(self, symbol, start_date=None, end_date=None, count=None):
        """获取指数的日线行情数据"""
        df = get_price(
            security=symbol,
            start_date=start_date,
            end_date=end_date,
            count=count,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            skip_paused=False,
            fq='none'
        )
        if df is not None:
            df = df.rename(columns={'money': 'amount'})
        return df

    def get_index_components(self, index_symbol, date):
        """获取指数在指定日期的成分股列表"""
        stocks = get_index_stocks(index_symbol, date=date)
        return list(stocks) if stocks is not None else []

    def get_industry_daily(self, industry_name, start_date=None, end_date=None):
        """获取行业指数的日线行情数据"""
        return pd.DataFrame()

    def get_industry_list(self, level="sw_l1"):
        """获取行业分类列表"""
        industries = get_industry()
        return list(industries.keys()) if industries else []

    def get_industry_classification(self, symbols, level="sw_l1"):
        """获取股票的行业分类信息"""
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

    # ============================================================
    # 第五类：宏观与情绪
    # ============================================================

    def get_market_spot(self, date):
        """获取指定日期的全市场行情快照"""
        stocks = list(get_all_securities(['stock'], date).index)
        df = get_price(
            security=stocks,
            start_date=date,
            end_date=date,
            count=1,
            frequency='daily',
            fields=['close', 'volume', 'money', 'high_limit', 'low_limit'],
            skip_paused=False,
            fq='pre'
        )
        return df

    def get_money_flow(self, symbol, start_date=None, end_date=None):
        """获取单只股票的资金流向数据"""
        df = get_money_flow(
            securities=symbol,
            start_date=start_date,
            end_date=end_date
        )
        return df

    def get_analyst_forecast(self, symbol, start_date=None, end_date=None):
        """获取分析师盈利预测数据"""
        from jqdatasdk import finance

        q = query(finance.ANALYST_PREDICT).filter(
            finance.ANALYST_PREDICT.code == symbol
        )

        if start_date:
            q = q.filter(finance.ANALYST_PREDICT.pubDate >= start_date)
        if end_date:
            q = q.filter(finance.ANALYST_PREDICT.pubDate <= end_date)

        df = finance.run_query(q)

        if df is not None and not df.empty:
            df = df.set_index('pubDate')

        return df

    def get_shareholder_data(self, symbol, start_date=None, end_date=None):
        """获取股东人数及户均持股数据"""
        from jqdatasdk import finance

        q = query(finance.STK_SHAREHOLDER_NUM).filter(
            finance.STK_SHAREHOLDER_NUM.code == symbol
        )

        if start_date:
            q = q.filter(finance.STK_SHAREHOLDER_NUM.pubDate >= start_date)
        if end_date:
            q = q.filter(finance.STK_SHAREHOLDER_NUM.pubDate <= end_date)

        df = finance.run_query(q)

        if df is not None and not df.empty:
            df = df.set_index('pubDate')

        return df

    # ============================================================
    # 第六类：辅助数据
    # ============================================================

    def get_trading_calendar(self, start_date=None, end_date=None):
        """获取交易日日历"""
        dates = get_trade_days(start_date=start_date, end_date=end_date)
        return dates

    def get_stock_info(self, symbol):
        """获取单只股票的基本信息"""
        df = get_all_securities(['stock'])
        if symbol in df.index:
            info = df.loc[symbol]
            return {
                'name': info.get('display_name', ''),
                'industry': '',
                'list_date': info.get('start_date', None),
                'delist_date': info.get('end_date', None) if info.get('end_date') != '2200-01-01' else None,
                'special_name': ''
            }
        return {}

    def get_margin_trading(self, symbol, start_date=None, end_date=None):
        """获取单只股票的融资融券数据"""
        from jqdatasdk import finance

        q = query(finance.MARGIN_TRADING).filter(
            finance.MARGIN_TRADING.code == symbol
        )

        if start_date:
            q = q.filter(finance.MARGIN_TRADING.date >= start_date)
        if end_date:
            q = q.filter(finance.MARGIN_TRADING.date <= end_date)

        df = finance.run_query(q)

        if df is not None and not df.empty:
            df = df.set_index('date')

        return df

    # ============================================================
    # 第七类：交易事件
    # ============================================================

    def get_dragon_tiger_list(self, date):
        """获取指定日期的龙虎榜明细数据"""
        df = get_billboard_list(date=date)
        return df

    def get_limit_up_pool(self, date):
        """获取指定日期的涨停股池"""
        df = get_billboard_list(date=date)
        return df

    def get_restricted_release(self, start_date=None, end_date=None):
        """获取限售解禁数据"""
        df = get_locked_shares(start_date=start_date, end_date=end_date)
        return df

    # ============================================================
    # 第八类：公司事件
    # ============================================================

    def get_equity_pledge(self, symbol, start_date=None, end_date=None):
        """获取个股股权质押数据"""
        from jqdatasdk import finance

        q = query(finance.STK_EQUITY_PLEDGE).filter(
            finance.STK_EQUITY_PLEDGE.code == symbol
        )

        if start_date:
            q = q.filter(finance.STK_EQUITY_PLEDGE.pubDate >= start_date)
        if end_date:
            q = q.filter(finance.STK_EQUITY_PLEDGE.pubDate <= end_date)

        df = finance.run_query(q)

        if df is not None and not df.empty:
            df = df.set_index('pubDate')

        return df

    def get_shareholder_changes(self, symbol, start_date=None, end_date=None):
        """获取股东增减持数据"""
        from jqdatasdk import finance

        q = query(finance.STK_SHAREHOLDER_CHANGE).filter(
            finance.STK_SHAREHOLDER_CHANGE.code == symbol
        )

        if start_date:
            q = q.filter(finance.STK_SHAREHOLDER_CHANGE.pubDate >= start_date)
        if end_date:
            q = q.filter(finance.STK_SHAREHOLDER_CHANGE.pubDate <= end_date)

        df = finance.run_query(q)

        if df is not None and not df.empty:
            df = df.set_index('pubDate')

        return df

    # ============================================================
    # 第九类：板块与概念
    # ============================================================

    def get_concept_list(self):
        """获取概念板块列表"""
        concepts = get_security_lists(type='concept')
        if concepts is not None:
            return concepts
        return pd.DataFrame()

    def get_concept_constituents(self, concept_code):
        """获取概念板块成分股"""
        stocks = get_concept_stocks(concept_code)
        if stocks is not None:
            return pd.DataFrame({'symbol': list(stocks)})
        return pd.DataFrame()

    def get_stock_industry(self, symbol):
        """获取个股行业信息"""
        industry = get_industry(symbol)
        return industry if industry else {}

    def get_st_stocks(self):
        """获取ST股票列表"""
        df = get_all_securities(['stock'])
        st_stocks = df[df['display_name'].str.contains('ST|星', na=False)].index.tolist()
        return st_stocks

    # ============================================================
    # 第十类：基金与可转债
    # ============================================================

    def get_etf_list(self):
        """获取ETF列表"""
        df = get_all_securities(['etf'])
        return df

    def get_etf_hist(self, symbol, start_date=None, end_date=None):
        """获取ETF历史行情"""
        df = get_price(
            security=symbol,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            skip_paused=False,
            fq='none'
        )
        if df is not None:
            df = df.rename(columns={'money': 'amount'})
        return df

    def get_convert_bond_list(self):
        """获取可转债列表"""
        df = get_all_securities(['conbond'])
        return df

    def get_convert_bond_hist(self, symbol, start_date=None, end_date=None):
        """获取可转债历史行情"""
        df = get_price(
            security=symbol,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            skip_paused=False,
            fq='none'
        )
        if df is not None:
            df = df.rename(columns={'money': 'amount'})
        return df

    # ============================================================
    # 第十一类：因子数据
    # ============================================================

    def get_all_factors(self):
        """获取聚宽因子库所有因子"""
        df = get_all_factors()
        return df

    def get_factor_kanban_values(self, universe='hs300', bt_cycle='month_3', model='long_only',
                                 category=None, skip_paused=False, commision_slippage=0):
        """获取因子看板数据"""
        if category is None:
            category = ['quality', 'basics']

        df = get_factor_kanban_values(
            universe=universe,
            bt_cycle=bt_cycle,
            model=model,
            category=category,
            skip_paused=skip_paused,
            commision_slippage=commision_slippage
        )
        return df

    # ============================================================
    # 第十二类：其他常用API
    # ============================================================

    def get_all_securities(self, types=None, date=None):
        """获取股票列表"""
        if types is None:
            types = ['stock']
        df = get_all_securities(types, date)
        return df

    def get_trade_days(self, start_date=None, end_date=None, count=None):
        """获取交易日列表"""
        dates = get_trade_days(start_date=start_date, end_date=end_date, count=count)
        return dates


# ============================================================
# 执行入口
# ============================================================

def main():
    """主入口 - 从环境变量或参数获取指令并执行"""

    import os

    # 获取执行指令
    func_name = os.environ.get('JQ_FUNCTION')
    params_str = os.environ.get('JQ_PARAMS', '{}')

    if not func_name:
        print("错误: 未指定 JQ_FUNCTION")
        print("用法: JQ_FUNCTION=get_stock_daily JQ_PARAMS='{\"symbol\":\"000001.XSHE\"}' python ricequant_data_executor.py")
        return

    # 解析参数
    try:
        params = json.loads(params_str)
    except:
        params = {}

    # 创建执行器
    executor = JoinQuantDataExecutor()

    # 检查方法是否存在
    if not hasattr(executor, func_name):
        print(f"错误: 未知方法 {func_name}")
        print(f"可用方法: {', '.join([m for m in dir(executor) if not m.startswith('_')])}")
        return

    # 执行方法
    try:
        method = getattr(executor, func_name)
        result = method(**params)

        # 返回结果
        if isinstance(result, pd.DataFrame):
            print("__RESULT_TYPE__DataFrame")
            print("__RESULT_SHAPE__" + str(result.shape))
            print("__RESULT_DATA__")
            print(result.to_string())
        elif isinstance(result, (list, dict)):
            print("__RESULT_TYPE__" + type(result).__name__)
            print("__RESULT_DATA__")
            print(json.dumps(result, ensure_ascii=False, default=str))
        else:
            print("__RESULT_TYPE__" + type(result).__name__)
            print("__RESULT_DATA__")
            print(result)

    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()