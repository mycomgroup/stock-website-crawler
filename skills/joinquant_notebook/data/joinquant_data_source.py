"""
JoinQuant 数据源实现

将 JoinQuant API 包装成 AbstractDataSource 接口格式，
实现从 JoinQuant 获取所有类型的数据。

使用方式:
    from jqdata import *

    ds = JoinQuantDataSource()
    df = ds.get_stock_daily('000001.XSHE', count=5)

更多示例见: examples/get_data_and_factors.py
"""

from typing import Optional, List, Dict, Literal
import pandas as pd
from datetime import datetime, timedelta

# 导入聚宽 API
from jqdata import (
    get_price, get_all_securities, get_fundamentals,
    get_security_lists, get_index_stocks, get_industry_stocks,
    get_trade_days, get_extras, get_billboard_list,
    get_locked_shares, get_money_flow, get_stock_details,
    get_concept_stocks, get_industry, get_sw_daily,
    get_bars, get_ticks, get_call_auction,
    finance, WIND_CLIENT
)

from joinquant_doc.doc.doc_JQDatadoc_10335_overview_get_price_移动窗口 import (
    get_price as jq_get_price
)

# 类型定义
FinancialTable = Literal["income", "balance", "cashflow"]
ReportPeriod = Literal["quarterly", "annual", "ttm"]
AdjustType = Literal["qfq", "hfq", "none"]
MinuteFreq = Literal["1min", "5min", "15min", "30min", "60min"]
IndustryLevel = Literal["sw_l1", "sw_l2", "sw_l3"]


class JoinQuantDataSource:
    """JoinQuant 数据源实现

    将聚宽 API 包装成统一的数据源接口。
    """

    def __init__(self):
        """初始化数据源"""
        pass

    # =========================================================================
    # 第一类：行情数据 (4个)
    # =========================================================================

    def get_stock_daily(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        count: Optional[int] = None,
        adjust: AdjustType = "qfq",
    ) -> pd.DataFrame:
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

        if df is not None and not df.empty:
            df = df.rename(columns={
                'money': 'amount'
            })
            # 计算换手率 turnover_rate
            df['turnover_rate'] = None  # JQ 不直接提供，换手率需额外计算

        return df

    def get_stock_daily_batch(
        self,
        symbols: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        count: Optional[int] = None,
        adjust: AdjustType = "qfq",
    ) -> Dict[str, pd.DataFrame]:
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

        result = {}
        if df is not None and not df.empty:
            for sym in symbols:
                try:
                    if isinstance(df.columns, pd.MultiIndex):
                        result[sym] = df[sym].copy()
                    else:
                        result[sym] = df[df['code'] == sym].copy() if 'code' in df.columns else df.copy()
                except:
                    result[sym] = pd.DataFrame()

        return result

    def get_stock_minute(
        self,
        symbol: str,
        date: str,
        freq: MinuteFreq = "5min",
    ) -> pd.DataFrame:
        """获取单只股票的分时行情数据"""
        # freq 转换: "5min" -> "5m"
        unit = freq.replace("min", "m")

        df = get_bars(
            security=symbol,
            count=100,  # 默认获取最近100个bar
            end_dt=date + " 15:00:00",
            unit=unit,
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            df=True
        )

        if df is not None and not df.empty:
            df = df.rename(columns={'date': 'time'})
            df['amount'] = df['money']

        return df

    def get_call_auction(
        self,
        symbol: str,
        date: str,
    ) -> pd.DataFrame:
        """获取单只股票的集合竞价数据"""
        df = get_call_auction(
            security=symbol,
            start_date=date,
            end_date=date
        )

        if df is not None:
            df = df.rename(columns={
                'time': 'index'
            })

        return df

    # =========================================================================
    # 第二类：估值数据 (2个)
    # =========================================================================

    def get_valuation(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取单只股票的估值数据"""
        # 使用 jqdata 的估值接口
        from jqdatasdk import get_fundamentals_continuously

        # JQ 的估值数据需要通过财务数据获取
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
            df = df.rename(columns={
                'pe_ratio': 'pe_ratio',
                'pb_ratio': 'pb_ratio',
                'ps_ratio': 'ps_ratio',
                'pcf_ratio': 'pcf_ratio'
            })

        return df

    def get_valuation_batch(
        self,
        symbols: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, pd.DataFrame]:
        """批量获取多只股票的估值数据"""
        result = {}
        for sym in symbols:
            df = self.get_valuation(sym, start_date, end_date)
            if df is not None and not df.empty:
                result[sym] = df
        return result

    def get_index_valuation(
        self,
        index_symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取指数的估值数据"""
        # JQ 没有直接的指数估值 API，需要通过成分股计算
        stocks = get_index_stocks(index_symbol)

        valuations = []
        for sym in stocks[:100]:  # 限制数量避免超时
            df = self.get_valuation(sym, start_date, end_date)
            if df is not None and not df.empty:
                valuations.append(df)

        if valuations:
            # 可以计算指数的平均估值
            combined = pd.concat(valuations)
            return combined.groupby(combined.index).mean()
        return pd.DataFrame()

    # =========================================================================
    # 第三类：财务数据 (3个)
    # =========================================================================

    def get_financial(
        self,
        symbol: str,
        table: FinancialTable,
        period: ReportPeriod = "quarterly",
    ) -> pd.DataFrame:
        """获取单只股票的财务报表数据"""
        table_map = {
            "income": "income",
            "balance": "balance_sheet",
            "cashflow": "cash_flow"
        }
        jd_table = table_map.get(table, "income")

        period_map = {
            "quarterly": None,  # 默认就是季度
            "annual": "annual",
            "ttm": None  # JQ 不直接支持 TTM，需要计算
        }

        dt_map = {"1": "1", "4": "4"}  # 季度

        q = query(finance)
        if period == "annual":
            q = query(finance).filter(
                finance.STATEMENT_CODE == 32011
            )

        df = get_fundamentals(
            security=symbol,
            date=None,  # 使用默认的最新数据
            indicator=None
        )

        return df

    def get_finance_indicators(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取单只股票的财务指标数据"""
        # JQ 提供 financial_indicator
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

    def get_dividend(
        self,
        symbol: str,
    ) -> pd.DataFrame:
        """获取单只股票的分红送转数据"""
        from jqdatasdk import finance

        q = query(finance.STK_DIVIDEND).filter(
            finance.STK_DIVIDEND.code == symbol
        )

        df = finance.run_query(q)

        if df is not None and not df.empty:
            df = df.set_index('pub_date')
            df = df.rename(columns={
                'cash_dividend': 'cash_dividend',
                'stock_dividend': 'stock_dividend',
                'dividend_ratio': 'stock_split'
            })

        return df

    # =========================================================================
    # 第四类：指数与行业 (5个)
    # =========================================================================

    def get_index_daily(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        count: Optional[int] = None,
    ) -> pd.DataFrame:
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

    def get_index_components(
        self,
        index_symbol: str,
        date: str,
    ) -> List[str]:
        """获取指数在指定日期的成分股列表"""
        stocks = get_index_stocks(index_symbol, date=date)
        return list(stocks) if stocks is not None else []

    def get_industry_daily(
        self,
        industry_name: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取行业指数的日线行情数据"""
        # JQ 使用申万行业指数
        # 需要先获取行业指数代码
        industry_codes = get_industry(name=industry_name)
        if not industry_codes:
            return pd.DataFrame()

        # 获取行业成分股并计算平均行情
        stocks = get_industry_stocks(industry_codes[0])
        df = get_price(
            security=stocks,
            start_date=start_date,
            end_date=end_date,
            count=None,
            frequency='daily',
            fields=['close'],
            skip_paused=False,
            fq='pre'
        )

        return df

    def get_industry_list(
        self,
        level: IndustryLevel = "sw_l1",
    ) -> List[str]:
        """获取行业分类列表"""
        # JQ 提供申万行业分类
        industries = get_industry()
        return list(industries.keys()) if industries else []

    def get_industry_classification(
        self,
        symbols: List[str],
        level: IndustryLevel = "sw_l1",
    ) -> pd.DataFrame:
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

    # =========================================================================
    # 第五类：宏观与情绪 (5个)
    # =========================================================================

    def get_bond_yield(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取国债收益率曲线数据"""
        # JQ 不直接提供国债收益率，需要使用宏观数据
        return pd.DataFrame()

    def get_market_spot(
        self,
        date: str,
    ) -> pd.DataFrame:
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

        if df is not None:
            df['change_pct'] = (df['close'] - df['pre_close']) / df['pre_close'] * 100

        return df

    def get_money_flow(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取单只股票的资金流向数据"""
        df = get_money_flow(
            securities=symbol,
            start_date=start_date,
            end_date=end_date
        )

        return df

    def get_north_money(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取北向资金（沪深股通）的每日净流入数据"""
        # JQ 需要机构账号才能获取北向数据
        return pd.DataFrame()

    def get_north_money_holdings(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取北向资金对单只股票的持仓数据"""
        return pd.DataFrame()

    def get_analyst_forecast(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取分析师盈利预测数据（一致预期）"""
        # JQ 提供分析师预期数据
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

    def get_shareholder_data(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
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

    def get_macro_indicator(
        self,
        indicator_type: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取宏观经济指标数据"""
        # JQ 宏观数据需要机构账号
        return pd.DataFrame()

    # =========================================================================
    # 第六类：辅助数据 (3个)
    # =========================================================================

    def get_trading_calendar(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DatetimeIndex:
        """获取交易日日历"""
        dates = get_trade_days(start_date=start_date, end_date=end_date)
        return dates

    def get_stock_info(
        self,
        symbol: str,
    ) -> Dict:
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

    def get_ah_premium(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取AH股溢价数据"""
        return pd.DataFrame()

    def get_margin_trading(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
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

    # =========================================================================
    # 第七类：交易事件 (7个) - 暂不完整实现
    # =========================================================================

    def get_dragon_tiger_list(self, date: str) -> pd.DataFrame:
        """获取指定日期的龙虎榜明细数据"""
        df = get_billboard_list(date=date)
        return df

    def get_dragon_tiger_summary(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取个股龙虎榜统计数据"""
        return pd.DataFrame()

    def get_limit_up_pool(self, date: str) -> pd.DataFrame:
        """获取指定日期的涨停股池"""
        df = get_billboard_list(date=date)
        if df is not None:
            df = df[df['limit_type'] == '涨停']
        return df if df is not None else pd.DataFrame()

    def get_limit_down_pool(self, date: str) -> pd.DataFrame:
        """获取指定日期的跌停股池"""
        return pd.DataFrame()

    def get_limit_stats(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取涨跌停统计数据"""
        return pd.DataFrame()

    def get_limit_list(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取个股涨跌停历史列表"""
        return pd.DataFrame()

    def get_block_deal(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取个股大宗交易数据"""
        return pd.DataFrame()

    def get_block_deal_summary(self, date: str) -> pd.DataFrame:
        """获取指定日期的大宗交易汇总"""
        return pd.DataFrame()

    # =========================================================================
    # 第八类：公司事件 (7个) - 暂不完整实现
    # =========================================================================

    def get_equity_pledge(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取个股股权质押数据"""
        return pd.DataFrame()

    def get_restricted_release(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取限售解禁数据"""
        df = get_locked_shares(
            start_date=start_date,
            end_date=end_date
        )
        return df

    def get_goodwill_data(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取个股商誉数据"""
        return pd.DataFrame()

    def get_repurchase_data(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取个股回购数据"""
        return pd.DataFrame()

    def get_performance_forecast(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取个股业绩预告数据"""
        return pd.DataFrame()

    def get_performance_express(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取个股业绩快报数据"""
        return pd.DataFrame()

    def get_institutional_research(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取机构调研数据"""
        return pd.DataFrame()

    # =========================================================================
    # 第九类：板块与概念 (5个)
    # =========================================================================

    def get_concept_list(self) -> pd.DataFrame:
        """获取概念板块列表"""
        concepts = get_security_lists(type='concept')
        if concepts is not None:
            return concepts
        return pd.DataFrame()

    def get_concept_constituents(
        self,
        concept_code: str,
    ) -> pd.DataFrame:
        """获取概念板块成分股"""
        stocks = get_concept_stocks(concept_code)
        if stocks is not None:
            return pd.DataFrame({'symbol': list(stocks)})
        return pd.DataFrame()

    def get_stock_industry(self, symbol: str) -> Dict:
        """获取个股行业信息"""
        industry = get_industry(symbol)
        return industry if industry else {}

    def get_name_history(self, symbol: str) -> pd.DataFrame:
        """获取股票更名历史"""
        return pd.DataFrame()

    def get_st_stocks(self) -> List[str]:
        """获取ST股票列表"""
        df = get_all_securities(['stock'])
        # JQ 不直接提供 ST 列表，需要通过名称筛选
        st_stocks = df[df['display_name'].str.contains('ST|星', na=False)].index.tolist()
        return st_stocks

    # =========================================================================
    # 第十类：基金与可转债 (7个)
    # =========================================================================

    def get_etf_list(self) -> pd.DataFrame:
        """获取ETF列表"""
        df = get_all_securities(['etf'])
        return df

    def get_etf_hist(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取ETF历史行情"""
        df = get_price(
            security=symbol,
            start_date=start_date,
            end_date=end_date,
            count=None,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            skip_paused=False,
            fq='none'
        )
        if df is not None:
            df = df.rename(columns={'money': 'amount'})
        return df

    def get_fund_nav(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取基金净值历史"""
        return pd.DataFrame()

    def get_convert_bond_list(self) -> pd.DataFrame:
        """获取可转债列表"""
        df = get_all_securities(['conbond'])
        return df

    def get_convert_bond_hist(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取可转债历史行情"""
        df = get_price(
            security=symbol,
            start_date=start_date,
            end_date=end_date,
            count=None,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            skip_paused=False,
            fq='none'
        )
        if df is not None:
            df = df.rename(columns={'money': 'amount'})
        return df

    def get_fund_portfolio(self, fund_code: str) -> pd.DataFrame:
        """获取基金持仓数据"""
        return pd.DataFrame()

    def get_lof_list(self) -> pd.DataFrame:
        """获取LOF基金列表"""
        df = get_all_securities(['lof'])
        return df

    # =========================================================================
    # 第十一类：宏观扩展 - 暂不实现
    # =========================================================================

    def get_cpi_data(self, start_date=None, end_date=None) -> pd.DataFrame:
        return pd.DataFrame()

    def get_ppi_data(self, start_date=None, end_date=None) -> pd.DataFrame:
        return pd.DataFrame()

    def get_pmi_index(self, start_date=None, end_date=None) -> pd.DataFrame:
        return pd.DataFrame()

    def get_m2_supply(self, start_date=None, end_date=None) -> pd.DataFrame:
        return pd.DataFrame()

    def get_gdp(self, start_date=None, end_date=None) -> pd.DataFrame:
        return pd.DataFrame()

    def get_gold_price(self, start_date=None, end_date=None) -> pd.DataFrame:
        return pd.DataFrame()

    def get_crude_oil(self, start_date=None, end_date=None) -> pd.DataFrame:
        return pd.DataFrame()

    def get_shibor_rate(self, start_date=None, end_date=None) -> pd.DataFrame:
        return pd.DataFrame()

    def get_social_financing(self, start_date=None, end_date=None) -> pd.DataFrame:
        return pd.DataFrame()

    def get_foreign_trade(self, start_date=None, end_date=None) -> pd.DataFrame:
        return pd.DataFrame()

    def get_currency_exchange_rate(self, start_date=None, end_date=None) -> pd.DataFrame:
        return pd.DataFrame()

    def get_macro_series(
        self,
        indicators: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        return pd.DataFrame()

    # =========================================================================
    # 第十二类：股东深度 - 暂不完整实现
    # =========================================================================

    def get_top_shareholders(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取前十大股东数据"""
        return pd.DataFrame()

    def get_top10_float_shareholders(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取前十大流通股东数据"""
        return pd.DataFrame()

    def get_institution_holdings(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """获取机构持仓数据"""
        return pd.DataFrame()

    def get_shareholder_changes(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
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


# =========================================================================
# 便捷函数 - 与原 AbstractDataSource API 一致
# =========================================================================

def create_jq_data_source() -> JoinQuantDataSource:
    """创建 JoinQuant 数据源实例"""
    return JoinQuantDataSource()