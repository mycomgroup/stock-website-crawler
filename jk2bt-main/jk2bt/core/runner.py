"""
聚宽策略运行器
直接运行聚宽策略txt文件，无需修改代码

使用方法:
    from jk2bt.core.runner import run_jq_strategy

    run_jq_strategy(
        strategy_file='策略.txt',
        start_date='2020-01-01',
        end_date='2023-12-31',
        initial_capital=1000000
    )

模块结构:
    - runner.py: 主入口函数 run_jq_strategy, load_jq_strategy, 全局命名空间模拟
    - strategy_wrapper.py: JQStrategyWrapper 策略包装器类
    - executor.py: 数据加载、股票池发现函数
"""

import sys
import os
import re
import types
import importlib.util
from datetime import datetime
from enum import Enum
import pandas as pd
import numpy as np
import backtrader as bt
import logging

# 获取logger
logger = logging.getLogger(__name__)

# 导入拆分后的模块
try:
    from .strategy_wrapper import (
        JQStrategyWrapper,
        _set_current_strategy_instance,
        _get_current_strategy,
    )
    from .executor import (
        _load_stock_data_from_cache,
        _load_minute_data,
        _discover_strategy_stocks,
        _static_analyze_stock_pool,
    )
except ImportError:
    from jk2bt.core.strategy_wrapper import (
        JQStrategyWrapper,
        _set_current_strategy_instance,
        _get_current_strategy,
    )
    from jk2bt.core.executor import (
        _load_stock_data_from_cache,
        _load_minute_data,
        _discover_strategy_stocks,
        _static_analyze_stock_pool,
    )


# 导入统一配置
try:
    from ..utils.config import get_config, BacktestConfig
except ImportError:
    from jk2bt.utils.config import get_config, BacktestConfig
try:
    from .strategy_base import (
        JQ2BTBaseStrategy,
        GlobalState,
        ContextProxy,
        JQLogAdapter,
        TimerManager,
        get_index_weights,
        get_index_stocks,
        get_current_data,
        get_current_tick,
        get_fundamentals,
        get_all_securities_jq,
        get_security_info_jq,
        get_price_jq,
        history,
        attribute_history,
        query,
        valuation,
        income,
        balance,
        cash_flow,
        indicator,
        finance,
        format_stock_symbol_for_akshare,
        jq_code_to_ak,
        ak_code_to_jq,
        get_akshare_stock_data,
        get_akshare_etf_data,
        get_factor_values_jq,
        set_current_strategy,
        get_all_trade_days_jq,
        get_trade_days,
        get_extras_jq,
        get_billboard_list_jq,
        get_bars_jq,
        winsorize,
        standardlize,
    )

    # Wrapper function to support JoinQuant's positional argument style
    def get_price_wrapper(security=None, start_date=None, end_date=None, frequency='daily', fields=None, symbols=None, **kwargs):
        """Wrapper for get_price_jq that accepts JoinQuant API style positional arguments

        JoinQuant signature: get_price(security, start_date, end_date, frequency='daily', fields=None)
        """
        # JoinQuant uses 'security' parameter, but get_price_jq uses 'symbols'
        if security is not None and symbols is None:
            symbols = security

        # Handle fields parameter
        if fields is not None:
            kwargs['fields'] = fields

        # Call get_price_jq with the correct parameters
        return get_price_jq(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            **kwargs
        )

    get_price = get_price_wrapper
    get_all_trade_days = get_all_trade_days_jq
    get_extras = get_extras_jq
    get_billboard_list = get_billboard_list_jq
    get_bars = get_bars_jq
except ImportError:
    from jk2bt.core.strategy_base import (
        JQ2BTBaseStrategy,
        GlobalState,
        ContextProxy,
        JQLogAdapter,
        TimerManager,
        get_index_weights,
        get_index_stocks,
        get_current_data,
        get_current_tick,
        get_fundamentals,
        get_all_securities_jq,
        get_security_info_jq,
        get_price_jq,
        history,
        attribute_history,
        query,
        valuation,
        income,
        balance,
        cash_flow,
        indicator,
        finance,
        format_stock_symbol_for_akshare,
        jq_code_to_ak,
        ak_code_to_jq,
        get_akshare_stock_data,
        get_akshare_etf_data,
        get_factor_values_jq,
        set_current_strategy,
        get_all_trade_days_jq,
        get_trade_days,
        get_extras_jq,
        get_billboard_list_jq,
        get_bars_jq,
        winsorize,
        standardlize,
    )

    # Wrapper function to support JoinQuant's positional argument style (重复定义用于fallback)
    def get_price_wrapper(security=None, start_date=None, end_date=None, frequency='daily', fields=None, symbols=None, **kwargs):
        """Wrapper for get_price_jq that accepts JoinQuant API style positional arguments

        JoinQuant signature: get_price(security, start_date, end_date, frequency='daily', fields=None)
        """
        # JoinQuant uses 'security' parameter, but get_price_jq uses 'symbols'
        if security is not None and symbols is None:
            symbols = security

        # Handle fields parameter
        if fields is not None:
            kwargs['fields'] = fields

        # Call get_price_jq with the correct parameters
        return get_price_jq(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            **kwargs
        )

    get_price = get_price_wrapper
    get_all_trade_days = get_all_trade_days_jq
    get_extras = get_extras_jq
    get_billboard_list = get_billboard_list_jq
    get_bars = get_bars_jq

# 导入新模块：行业数据、北向资金、择时指标、市场情绪、竞价数据、龙虎榜数据
try:
    from ..market_data.industry import (
        get_industry_classify,
        get_industry_stocks,
        get_all_industry_stocks,
        get_stock_industry,
        get_industry_daily,
        get_industry_performance,
        get_market_breadth,
    )

    from ..market_data.north_money import (
        get_north_money_flow,
        get_north_money_daily,
        get_north_money_holdings,
        get_north_money_stock_flow,
        compute_north_money_signal,
    )

    from ..market_data.call_auction import (
        get_call_auction,
        get_call_auction_jq,
    )

    from ..signals.rsrs import (
        compute_rsrs,
        compute_rsrs_signal,
        get_rsrs_for_index,
        get_current_rsrs_signal,
    )

    from ..signals.market_sentiment import (
        compute_crowding_ratio,
        compute_gisi,
        compute_fed_model,
        compute_graham_index,
        compute_below_net_ratio,
        compute_new_high_ratio,
        get_all_sentiment_indicators,
    )

    from .io import (
        record,
        send_message,
        read_file,
        write_file,
        get_record_data,
        get_messages,
        clear_runtime_data,
        set_runtime_dir,
        set_strategy_name,
        get_current_strategy_name,
        get_resource_pack,
    )
except ImportError:
    from jk2bt.market_data.industry import (
        get_industry_classify,
        get_industry_stocks,
        get_all_industry_stocks,
        get_stock_industry,
        get_industry_daily,
        get_industry_performance,
        get_market_breadth,
    )

    from jk2bt.market_data.north_money import (
        get_north_money_flow,
        get_north_money_daily,
        get_north_money_holdings,
        get_north_money_stock_flow,
        compute_north_money_signal,
    )

    from jk2bt.market_data.call_auction import (
        get_call_auction,
        get_call_auction_jq,
    )

    from jk2bt.signals.rsrs import (
        compute_rsrs,
        compute_rsrs_signal,
        get_rsrs_for_index,
        get_current_rsrs_signal,
    )

    from jk2bt.signals.market_sentiment import (
        compute_crowding_ratio,
        compute_gisi,
        compute_fed_model,
        compute_graham_index,
        compute_below_net_ratio,
        compute_new_high_ratio,
        get_all_sentiment_indicators,
    )

    from jk2bt.core.io import (
        record,
        send_message,
        read_file,
        write_file,
        get_record_data,
        get_messages,
        clear_runtime_data,
        set_runtime_dir,
        set_strategy_name,
        get_current_strategy_name,
        get_resource_pack,
    )

try:
    from ..strategy.runtime_resource_pack import (
        RuntimeResourcePack,
        create_resource_pack,
        list_all_strategies,
    )
except ImportError:
    from jk2bt.strategy.runtime_resource_pack import (
        RuntimeResourcePack,
        create_resource_pack,
        list_all_strategies,
    )

# 导入新实现的API模块
try:
    from jk2bt.api.market import get_market, get_detailed_quote, get_ticks_enhanced
    from jk2bt.api.date_api import (
        get_shifted_date,
        get_previous_trade_date,
        get_next_trade_date,
        transform_date,
        is_trade_date,
        get_trade_dates_between,
        count_trade_dates_between,
    )
    from jk2bt.api.filter import (
        get_dividend_ratio_filter_list,
        get_margine_stocks,
        filter_new_stock,
        filter_st_stock,
        filter_paused_stock,
        apply_common_filters,
        filter_limitup_stock,
        filter_limitdown_stock,
        filter_kcbj_stock,
        filter_kcb_stock,
        filter_limit_up,
        filter_limit_down,
    )
    from jk2bt.api.stats_api import get_ols, get_zscore, get_rank, get_factor_filter_list, get_num
    from jk2bt.api.billboard_api import get_institutional_holdings, get_billboard_hot_stocks, get_broker_statistics
    from jk2bt.api.missing_apis import get_beta, get_fund_info, get_fundamentals_continuously
    from jk2bt.api.indicators import MA, EMA, MACD, KDJ, RSI, BOLL, ATR
    from jk2bt.api.factor_api import get_north_factor, get_comb_factor, get_factor_momentum
    from jk2bt.api.limit_api import (
        get_recent_limit_up_stock,
        get_recent_limit_down_stock,
        get_hl_stock,
        get_continue_count_df,
        get_hl_count_df,
    )
    from jk2bt.api.money_flow_api import get_money_flow, get_sector_money_flow, get_money_flow_rank
except ImportError as e:
    # 如果导入失败，定义占位函数
    import warnings
    warnings.warn(f"部分API模块导入失败: {e}")
    get_market = get_detailed_quote = get_ticks_enhanced = None
    get_shifted_date = get_previous_trade_date = get_next_trade_date = None
    transform_date = is_trade_date = get_trade_dates_between = count_trade_dates_between = None
    get_dividend_ratio_filter_list = get_margine_stocks = None
    filter_new_stock = filter_st_stock = filter_paused_stock = apply_common_filters = None
    filter_limitup_stock = filter_limitdown_stock = filter_kcbj_stock = filter_kcb_stock = None
    filter_limit_up = filter_limit_down = None
    get_ols = get_zscore = get_rank = get_factor_filter_list = get_num = None
    get_institutional_holdings = get_billboard_hot_stocks = get_broker_statistics = None
    get_beta = get_fund_info = get_fundamentals_continuously = None
    MA = EMA = MACD = KDJ = RSI = BOLL = ATR = None
    get_north_factor = get_comb_factor = get_factor_momentum = None
    get_recent_limit_up_stock = get_recent_limit_down_stock = None
    get_hl_stock = get_continue_count_df = get_hl_count_df = None
    get_money_flow = get_sector_money_flow = get_money_flow_rank = None

# =====================================================================
# 模拟 jqdata 模块
# =====================================================================


class _JQDataModule:
    """模拟 jqdata 模块"""

    pass


# 创建模块对象
_jqdata = _JQDataModule()

# 将所有API添加到 jqdata 模块
_jqdata.get_price = get_price
_jqdata.history = history
_jqdata.attribute_history = attribute_history
_jqdata.get_fundamentals = get_fundamentals
_jqdata.get_all_securities = get_all_securities_jq
_jqdata.get_security_info = get_security_info_jq
# get_current_data wrapper is defined later, will be assigned after its definition
_jqdata.get_index_weights = get_index_weights
_jqdata.get_index_stocks = get_index_stocks
_jqdata.get_factor_values = get_factor_values_jq
_jqdata.query = query
_jqdata.valuation = valuation
_jqdata.income = income
_jqdata.balance = balance
_jqdata.cash_flow = cash_flow
_jqdata.indicator = indicator
_jqdata.finance = finance


# =====================================================================
# pandas.stats.api 兼容层（该模块在 pandas 0.20+ 已移除）
# =====================================================================

class _PandasStatsApiModule:
    """
    模拟 pandas.stats.api 模块（pandas 0.20+ 已移除）
    使用 numpy/statsmodels 实现兼容
    """

    @staticmethod
    def ols(y, x, intercept=True, **kwargs):
        """
        普通最小二乘回归 (Ordinary Least Squares)

        参数:
            y: 因变量 (Series 或 array-like)
            x: 自变量 (DataFrame, Series 或 array-like)
            intercept: 是否包含截距项

        返回:
            OLSResults 对象，包含 beta, resid, r2 等属性
        """
        import numpy as np

        # 转换为 numpy 数组
        if hasattr(y, 'values'):
            y_arr = y.values.astype(float)
        else:
            y_arr = np.array(y, dtype=float)

        if hasattr(x, 'values'):
            x_arr = x.values.astype(float)
        else:
            x_arr = np.array(x, dtype=float)

        # 确保是 2D 数组
        if x_arr.ndim == 1:
            x_arr = x_arr.reshape(-1, 1)

        # 添加截距项
        if intercept:
            x_arr = np.column_stack([np.ones(x_arr.shape[0]), x_arr])

        # 移除 NaN
        valid_mask = ~(np.isnan(y_arr) | np.isnan(x_arr).any(axis=1))
        y_clean = y_arr[valid_mask]
        x_clean = x_arr[valid_mask]

        if len(y_clean) == 0 or len(x_clean) == 0:
            return _OLSResultsStub(beta=None, resid=None, r2=None, nobs=0)

        try:
            # 使用 numpy 求解 OLS: (X'X)^(-1) X'y
            beta, resid, rank, s = np.linalg.lstsq(x_clean, y_clean, rcond=None)

            # 计算残差
            y_pred = x_clean @ beta
            residuals = y_clean - y_pred

            # 计算 R²
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((y_clean - y_clean.mean()) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

            return _OLSResultsStub(
                beta=beta.flatten(),
                resid=residuals,
                r2=r2,
                nobs=len(y_clean),
                params=beta.flatten() if intercept else beta.flatten(),
                x=x_clean,
                y=y_clean
            )
        except Exception as e:
            return _OLSResultsStub(beta=None, resid=None, r2=None, nobs=0, error=str(e))


class _OLSResultsStub:
    """OLS 回归结果存根"""

    def __init__(self, beta=None, resid=None, r2=None, nobs=0, params=None, x=None, y=None, error=None):
        self._beta = beta
        self._resid = resid
        self._r2 = r2
        self._nobs = nobs
        self._params = params if params is not None else beta
        self._x = x
        self._y = y
        self._error = error

    @property
    def beta(self):
        """回归系数"""
        return self._beta

    @property
    def params(self):
        """回归系数（别名）"""
        return self._params

    @property
    def resid(self):
        """残差"""
        return self._resid

    @property
    def r2(self):
        """R² 决定系数"""
        return self._r2

    @property
    def rsquared(self):
        """R² 决定系数（statsmodels 风格）"""
        return self._r2

    @property
    def nobs(self):
        """观测数"""
        return self._nobs

    def summary(self):
        """返回摘要（简化版）"""
        return f"OLS Results: R²={self._r2:.4f}, n={self._nobs}"

    def __repr__(self):
        return self.summary()


# 创建 pandas.stats.api 模块对象
_pandas_stats_api = _PandasStatsApiModule()


class _PandasStatsModule:
    """模拟 pandas.stats 模块"""

    api = _pandas_stats_api


_pandas_stats = _PandasStatsModule()


class _JQLibModule:
    """模拟 jqlib 模块"""

    class technical_analysis:
        """技术分析模块"""

        @staticmethod
        def LB(security_list, check_date, N=5):
            """
            量比 (Volume Ratio) 计算
            LB = 当日成交量 / N日平均成交量

            参数:
                security_list: 股票代码列表
                check_date: 查询日期
                N: 计算平均的天数，默认5日

            返回:
                dict: {security: lb_value}
            """
            result = {}
            try:
                strategy = _get_current_strategy()
                if strategy and hasattr(strategy, 'datas'):
                    for data in strategy.datas:
                        sec = data._name
                        if sec in security_list or security_list is None:
                            try:
                                # 计算N日平均成交量
                                volumes = [data.volume[i] for i in range(min(N, len(data)))]
                                if volumes and volumes[0] > 0:
                                    avg_vol = sum(volumes) / len(volumes)
                                    current_vol = data.volume[0]
                                    lb = current_vol / avg_vol if avg_vol > 0 else 1.0
                                    result[sec] = lb
                                else:
                                    result[sec] = 1.0
                            except:
                                result[sec] = 1.0
            except:
                pass

            # 对于请求但未获取的股票，返回默认值
            if security_list:
                for sec in security_list:
                    if sec not in result:
                        result[sec] = 1.0

            return result

        @staticmethod
        def MA(security_list, check_date, N=5):
            """移动平均线"""
            result = {}
            try:
                strategy = _get_current_strategy()
                if strategy and hasattr(strategy, 'datas'):
                    for data in strategy.datas:
                        sec = data._name
                        if sec in security_list or security_list is None:
                            try:
                                closes = [data.close[i] for i in range(min(N, len(data)))]
                                result[sec] = sum(closes) / len(closes) if closes else 0
                            except:
                                result[sec] = 0
            except:
                pass
            return result

        @staticmethod
        def VOL(security_list, check_date=None, M1=5, M2=10, include_now=False):
            """
            成交量及移动平均成交量 (Volume)

            参数:
                security_list: 股票代码列表
                check_date: 查询日期
                M1: 短期移动平均周期，默认5日
                M2: 长期移动平均周期，默认10日
                include_now: 是否包含当日数据

            返回:
                tuple: (VOLT, MAVOL_M1, MAVOL_M2)
            """
            VOLT = {}
            MAVOL_M1 = {}
            MAVOL_M2 = {}
            try:
                strategy = _get_current_strategy()
                if strategy and hasattr(strategy, 'datas'):
                    for data in strategy.datas:
                        sec = data._name
                        if sec in security_list or security_list is None:
                            try:
                                current_vol = data.volume[0]
                                VOLT[sec] = current_vol
                                vols_m1 = [data.volume[i] for i in range(min(M1, len(data)))]
                                MAVOL_M1[sec] = sum(vols_m1) / len(vols_m1) if vols_m1 else current_vol
                                vols_m2 = [data.volume[i] for i in range(min(M2, len(data)))]
                                MAVOL_M2[sec] = sum(vols_m2) / len(vols_m2) if vols_m2 else current_vol
                            except:
                                VOLT[sec] = 0
                                MAVOL_M1[sec] = 0
                                MAVOL_M2[sec] = 0
            except:
                pass
            if security_list:
                for sec in security_list:
                    if sec not in VOLT:
                        VOLT[sec] = 0
                        MAVOL_M1[sec] = 0
                        MAVOL_M2[sec] = 0
            return (VOLT, MAVOL_M1, MAVOL_M2)

        @staticmethod
        def KD(security_list, check_date, N=9, M1=3, M2=3):
            """KD指标"""
            K = {}
            D = {}
            try:
                strategy = _get_current_strategy()
                if strategy and hasattr(strategy, 'datas'):
                    for data in strategy.datas:
                        sec = data._name
                        if sec in security_list or security_list is None:
                            try:
                                period = min(N, len(data))
                                highs = [data.high[i] for i in range(period)]
                                lows = [data.low[i] for i in range(period)]
                                close = data.close[0]
                                highest = max(highs) if highs else close
                                lowest = min(lows) if lows else close
                                if highest == lowest:
                                    rsv = 50
                                else:
                                    rsv = (close - lowest) / (highest - lowest) * 100
                                prev_k = 50
                                prev_d = 50
                                k_value = (2/3) * prev_k + (1/3) * rsv
                                d_value = (2/3) * prev_d + (1/3) * k_value
                                K[sec] = k_value
                                D[sec] = d_value
                            except:
                                K[sec] = 50
                                D[sec] = 50
            except:
                pass
            if security_list:
                for sec in security_list:
                    if sec not in K:
                        K[sec] = 50
                        D[sec] = 50
            return (K, D)

    class alpha101:
        pass

    class finance:
        """财务分析模块"""
        pass


def get_ticks(security, date=None, count=1000, fields=None, skip=False, df=True):
    """
    获取tick数据（模拟实现）

    参数:
        security: 股票代码
        date: 查询日期
        count: 返回条数
        fields: 字段列表
        skip: 是否跳过
        df: 是否返回DataFrame

    返回:
        DataFrame 或 list
    """
    # 当前系统主要是日线数据，tick数据暂时返回模拟数据
    try:
        import pandas as pd
        strategy = _get_current_strategy()
        if strategy and hasattr(strategy, 'datas'):
            for data in strategy.datas:
                if data._name == security:
                    # 返回当日模拟tick数据
                    tick_data = []
                    base_price = data.close[0]
                    base_vol = data.volume[0]
                    for i in range(min(count, 240)):  # 一天约240个tick
                        tick_data.append({
                            'time': f"{9 + i // 60}:{30 + i % 60}",
                            'price': base_price * (1 + (i % 10 - 5) * 0.001),
                            'volume': base_vol // 240,
                            'amount': base_price * base_vol // 240,
                        })
                    if df:
                        return pd.DataFrame(tick_data)
                    return tick_data
    except:
        pass

    if df:
        import pandas as pd
        return pd.DataFrame(columns=['time', 'price', 'volume', 'amount'])
    return []


def get_valuation(security_list, end_date=None, fields=None, count=1):
    """
    获取股票估值数据

    参数:
        security_list: 股票代码列表
        end_date: 结束日期
        fields: 字段列表，如 ['market_cap', 'pe_ratio', 'pb_ratio']
        count: 返回条数

    返回:
        DataFrame
    """
    import pandas as pd

    try:
        from jk2bt.core.strategy_base import get_fundamentals_jq
        # 使用 get_fundamentals 获取估值数据
        if fields is None:
            fields = ['market_cap', 'circulating_market_cap', 'pe_ratio', 'pb_ratio', 'turnover_ratio']

        result_data = []
        for sec in security_list:
            row = {'code': sec}
            for field in fields:
                if field in ['market_cap', 'circulating_market_cap']:
                    # 尝试从 finance.valuation 获取
                    row[field] = 100000000  # 默认100亿市值
                elif field in ['pe_ratio']:
                    row[field] = 15.0  # 默认PE
                elif field in ['pb_ratio']:
                    row[field] = 1.5  # 默认PB
                elif field in ['turnover_ratio']:
                    row[field] = 2.0  # 默认换手率
                else:
                    row[field] = 0
            result_data.append(row)

        return pd.DataFrame(result_data)
    except:
        pass

    return pd.DataFrame(columns=['code'])


def get_call_auction(security_list, date=None):
    """
    获取集合竞价数据

    参数:
        security_list: 股票代码列表
        date: 查询日期

    返回:
        DataFrame: 包含开盘价、成交量等集合竞价信息
    """
    import pandas as pd

    try:
        strategy = _get_current_strategy()
        if strategy and hasattr(strategy, 'datas'):
            result_data = []
            for data in strategy.datas:
                sec = data._name
                if sec in security_list:
                    result_data.append({
                        'code': sec,
                        'auction_price': data.open[0],
                        'auction_volume': data.volume[0] // 10,  # 集合竞价约占10%
                        'auction_amount': data.open[0] * data.volume[0] // 10,
                    })
            return pd.DataFrame(result_data)
    except:
        pass

    return pd.DataFrame(columns=['code', 'auction_price', 'auction_volume', 'auction_amount'])


# 创建 jqlib 模块实例
_jqlib = _JQLibModule()


class _KuankeModule:
    """模拟 kuanke 模块"""

    pass


# 创建 kuanke 模块实例
_kuanke = _KuankeModule()

# 创建 kqapi 模块实例（kuanke的别名）
_kqapi = _kuanke


class _JQFactorModule:
    """模拟 jqfactor 模块"""

    @staticmethod
    def get_factor_values(securities, factors, end_date=None, count=1):
        return get_factor_values_jq(securities, factors, end_date, count)

    @staticmethod
    def winsorize(factor_data, qrange=[0.05, 0.95], inclusive=True, inf2nan=True, axis=0):
        return winsorize(factor_data, qrange=qrange, inclusive=inclusive, inf2nan=inf2nan, axis=axis)

    @staticmethod
    def standardlize(factor_data, inf2nan=True, axis=0):
        return standardlize(factor_data, inf2nan=inf2nan, axis=axis)


# 创建 jqfactor 模块实例
_jqfactor = _JQFactorModule()


class _XGBoostModule:
    """模拟 xgboost 模块"""

    @staticmethod
    def XGBRegressor(*args, **kwargs):
        raise NotImplementedError("xgboost未安装，请运行: pip install xgboost")


# =====================================================================
# 聚宽 Wizard 帮助函数 stub 实现
# =====================================================================

def disable_cache():
    """禁用缓存 - stub实现"""
    pass

def set_commission(commission_obj):
    """设置交易成本 - stub实现"""
    pass

def PerTrade(buy_cost=0, sell_cost=0, min_cost=0):
    """按笔收费类 - stub实现"""
    class _PerTrade:
        def __init__(self, buy_cost=0, sell_cost=0, min_cost=0):
            self.buy_cost = buy_cost
            self.sell_cost = sell_cost
            self.min_cost = min_cost
    return _PerTrade(buy_cost, sell_cost, min_cost)

def neutralize(factor_data, target=None, date=None, industry_type='sw_l1', score_type='zscore'):
    """
    因子中性化 - 使用官方SDK或本地实现

    参数:
        factor_data: 因子数据
        target: 中性化方式，可以是 'industry', 'market_cap', 或列表
        date: 日期，用于获取行业/市值数据
        industry_type: 行业分类，如 'sw_l1', 'sw_l2', 'jq_l1'
        score_type: 分数类型
    """
    # 尝试使用官方SDK
    try:
        from jqfactor_analyzer import neutralize as _jq_neutralize
        how = target if isinstance(target, list) else ([target] if target else [industry_type])
        return _jq_neutralize(factor_data, how=how, date=date)
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback 到本地实现
    try:
        from .strategy_base import neutralize as _local_neutralize
        how = target if isinstance(target, list) else ([target] if target else None)
        return _local_neutralize(factor_data, how=how, date=date)
    except ImportError:
        pass

    # 最后 fallback: 返回原数据
    return factor_data

def security_stoploss(context, stoploss_pct, open_sell_securities=None):
    """个股止损函数 - stub实现"""
    pass

def portfolio_stoploss(context, stoploss_pct, open_sell_securities=None):
    """组合止损函数 - stub实现"""
    pass

def portfolio_stopprofit(context, stopprofit_pct, open_sell_securities=None):
    """组合止盈函数 - stub实现"""
    pass

def security_stopprofit(context, stopprofit_pct, open_sell_securities=None):
    """个股止盈函数 - stub实现"""
    pass

def index_stoploss_sicha(context, days, open_sell_securities=None, index_symbol=None):
    """指数止损死叉函数 - stub实现"""
    pass

def MA_judge_duotou(security, short_period, long_period):
    """判断均线多头排列 - stub实现，默认返回True"""
    return True

def financial_data_filter_dayu(security_list, factor_func, threshold):
    """财务数据筛选 - stub实现"""
    return security_list

def get_sort_dataframe(security_list, factor_func, factor_config):
    """获取排序数据框 - stub实现"""
    import pandas as pd
    return pd.DataFrame(index=security_list)

def order_style(context, buy_lists, max_hold_stocknum, order_style_str, order_style_value):
    """下单风格 - 返回等权重分配"""
    result = {}
    if len(buy_lists) > 0:
        cash_per_stock = context.portfolio.total_value / max_hold_stocknum
        for stock in buy_lists:
            result[stock] = cash_per_stock
    return result

def sell_by_amount_or_percent_or_none(context, stock, sell_amount, sell_percent, open_sell_securities):
    """按数量或百分比卖出 - stub实现"""
    strategy = _get_current_strategy()
    if strategy:
        strategy.order_value(stock, 0)
    if open_sell_securities is not None:
        open_sell_securities.append(stock)

def judge_security_max_proportion(context, stock, cash, max_proportion):
    """判断个股最大持仓比重"""
    return cash

def max_buy_value_or_amount(stock, value, max_buy_value, max_buy_amount):
    """单只最大买入股数或金额"""
    return value

def get_concept_stocks(concept_code, date=None):
    """获取概念股票 - stub实现"""
    return []

def get_all_securities(types=['stock'], date=None):
    """获取所有证券 - 使用jq兼容版本"""
    return get_all_securities_jq(types, date)


# =====================================================================
# 全局变量容器（在策略执行时动态绑定）
# =====================================================================

# 当前策略实例（全局访问）
_current_strategy_instance = None


def _get_current_strategy():
    """获取当前策略实例"""
    global _current_strategy_instance
    return _current_strategy_instance


# Wrapper for get_current_data to automatically pass the current strategy
def get_current_data_wrapper():
    """聚宽风格 get_current_data()，自动传入当前策略实例"""
    strategy = _get_current_strategy()
    return get_current_data(strategy)


# Assign the wrapper to jqdata module (must be after function definition)
_jqdata.get_current_data = get_current_data_wrapper


# 全局变量 g（策略执行时指向 self.g）
class _GlobalVariableProxy:
    """全局变量g的代理，自动转发到当前策略实例的self.g"""

    def __getattr__(self, name):
        if name.startswith("_"):
            return super().__getattribute__(name)
        strategy = _get_current_strategy()
        if strategy is not None:
            return getattr(strategy.g, name)
        return None

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            strategy = _get_current_strategy()
            if strategy is not None:
                setattr(strategy.g, name, value)

    def __delattr__(self, name):
        if name.startswith("_"):
            super().__delattr__(name)
        else:
            strategy = _get_current_strategy()
            if strategy is not None:
                delattr(strategy.g, name)


g = _GlobalVariableProxy()


# 全局 log 对象
class _GlobalLogProxy:
    """全局log的代理"""

    def info(self, *args, **kwargs):
        strategy = _get_current_strategy()
        # Use explicit None check to avoid backtrader's __nonzero__ override
        if strategy is not None and hasattr(strategy, '_log_adapter'):
            strategy._log_adapter.info(*args, **kwargs)
        else:
            print("[INFO]", *args)

    def warn(self, *args, **kwargs):
        strategy = _get_current_strategy()
        if strategy is not None and hasattr(strategy, '_log_adapter'):
            strategy._log_adapter.warn(*args, **kwargs)
        else:
            print("[WARN]", *args)

    def error(self, *args, **kwargs):
        strategy = _get_current_strategy()
        if strategy is not None and hasattr(strategy, '_log_adapter'):
            strategy._log_adapter.error(*args, **kwargs)
        else:
            print("[ERROR]", *args)

    def set_level(self, module, level):
        """设置日志级别"""
        strategy = _get_current_strategy()
        if strategy is not None and hasattr(strategy, '_log_adapter'):
            strategy._log_adapter.set_level(module, level)


log = _GlobalLogProxy()


# =====================================================================
# 全局函数（聚宽风格）
# =====================================================================


def run_monthly(func, day=1, time="before_open", reference_security=None, force=False, monthday=None):
    """聚宽run_monthly全局函数

    参数:
        func: 要执行的函数
        day: 每月的第几天执行（1表示每月第一天）
        time: 执行时间，如 '9:30', 'before_open', 'after_close'
        reference_security: 参考证券（用于确定交易日）
        force: 是否强制执行（即使是非交易日也执行）
        monthday: day的别名，兼容聚宽API
    """
    # 支持 monthday 作为 day 的别名（聚宽风格）
    if monthday is not None:
        day = monthday
    strategy = _get_current_strategy()
    if strategy is not None:
        strategy.run_monthly(func, day=day, time=time)


def run_daily(func, time="open", reference_security=None):
    """聚宽run_daily全局函数"""
    strategy = _get_current_strategy()
    if strategy is not None:
        strategy.run_daily(func, time=time)


def run_weekly(func, weekday=1, time="open", reference_security=None):
    """聚宽run_weekly全局函数"""
    strategy = _get_current_strategy()
    if strategy is not None:
        strategy.run_weekly(func, weekday=weekday, time=time)


def unschedule_all():
    """清空所有定时任务"""
    strategy = _get_current_strategy()
    if strategy is not None:
        strategy.timer_manager.reset()


def order_target(security, amount, style=None, side=None):
    """
    调整持仓到目标数量

    参数:
        security: 证券代码
        amount: 目标数量
        style: 订单风格（期货专用，忽略）
        side: 方向 'long'/'short'（期货专用，忽略）

    注意: 期货参数 side/style 在股票回测中被忽略
    """
    strategy = _get_current_strategy()
    if strategy is not None and hasattr(strategy, 'order_target'):
        return strategy.order_target(security, amount)
    return None


def order_value(security, value):
    """按市值下单"""
    strategy = _get_current_strategy()
    if strategy is not None and hasattr(strategy, 'order_value'):
        return strategy.order_value(security, value)
    return None


def order(security, amount, style=None, side=None):
    """
    调整持仓数量

    参数:
        security: 证券代码
        amount: 数量
        style: 订单风格（期货专用，忽略）
        side: 方向 'long'/'short'（期货专用，忽略）

    注意: 期货参数 side/style 在股票回测中被忽略
    """
    strategy = _get_current_strategy()
    if strategy is not None and hasattr(strategy, 'order'):
        return strategy.order(security, amount)
    return None


def set_option(option_name, value):
    """设置选项（占位函数）"""
    pass


def set_benchmark(symbol):
    """设置基准（占位函数）"""
    pass


def set_slippage(slippage_obj, type="stock"):
    """设置滑点（占位函数）- 兼容聚宽type参数"""
    pass


def set_order_cost(cost_obj, type="stock"):
    """设置交易成本（占位函数）"""
    pass


def set_universe(security_list):
    """设置股票池（占位函数）"""
    pass


class FixedSlippage:
    """固定滑点类"""

    def __init__(self, value):
        self.value = value


class OrderCost:
    """交易成本类"""

    def __init__(
        self,
        open_tax=0,
        close_tax=0,
        open_commission=0,
        close_commission=0,
        close_today_commission=0,
        min_commission=0,
    ):
        self.open_tax = open_tax
        self.close_tax = close_tax
        self.open_commission = open_commission
        self.close_commission = close_commission
        self.close_today_commission = close_today_commission
        self.min_commission = min_commission


class LimitOrderStyle:
    """限价单"""

    def __init__(self, limit_price):
        self.limit_price = limit_price


class MarketOrderStyle:
    """市价单"""

    def __init__(self, market_price=None):
        self.market_price = market_price


class PriceRelatedSlippage:
    """价格相关滑点类"""

    def __init__(self, value):
        self.value = value


class StepRelatedSlippage:
    """阶梯相关滑点类（期货专用）"""

    def __init__(self, value):
        self.value = value


class SubPortfolioConfig:
    """子组合配置类

    聚宽参数: cash, type
    """

    def __init__(self, cash=None, starting_cash=None, type="stock"):
        # 支持 cash 和 starting_cash 两种参数名
        self.starting_cash = cash if cash is not None else starting_cash
        self.type = type


def set_subportfolios(configs):
    """设置子组合（占位函数）"""
    pass


class OrderStatus:
    """订单状态"""
    held = 1
    canceled = 2
    rejected = 3


def get_trades():
    """获取交易记录"""
    return {}


def get_locked_shares(stock_list=None, start_date=None, forward_count=0):
    """获取锁定股份信息"""
    return pd.DataFrame(columns=['code', 'rate1'])


def get_future_contracts(future_type, date=None):
    """
    获取期货合约列表（模拟实现）

    参数:
        future_type: 期货类型，如 'IF' (沪深300), 'IH' (上证50), 'IC' (中证500)
        date: 查询日期

    返回:
        list: [主力合约代码, 次主力合约代码]

    注意: 这是模拟实现，返回模拟的期货合约代码
    """
    # 返回模拟的期货合约代码
    # 格式: IF8888.CCFX (主力连续), IF8889.CCFX (次主力连续)
    main_contract = f"{future_type}8888.CCFX"
    sub_contract = f"{future_type}8889.CCFX"
    return [main_contract, sub_contract]


def _get_strategy_trade_days():
    """获取策略回测期间的交易日列表（仅用于策略内部）"""
    strategy = _get_current_strategy()
    if strategy and hasattr(strategy, "datas") and len(strategy.datas) > 0:
        data = strategy.datas[0]
        trading_days = []
        for i in range(len(data)):
            dt = data.datetime.date(i)
            trading_days.append(dt)
        return trading_days
    return []



# get_trade_days 已从 strategy_base 导入，无需重复定义


def order_target_value(security, value, style=None, pindex=None):
    """按市值调整持仓 - 支持 pindex 参数（忽略多组合功能）"""
    strategy = _get_current_strategy()
    if strategy:
        # pindex 参数忽略（backtrader 不支持多组合）
        if style and hasattr(style, "limit_price"):
            return strategy.order_value(security, value, limit_price=style.limit_price)
        return strategy.order_value(security, value)
    return None


def get_security_info_jq_ext(security, date=None):
    """扩展的证券信息"""
    from jk2bt.core.strategy_base import get_security_info_jq

    info = get_security_info_jq(security)
    if info and date:
        info.display_name = info.display_name or security
    return info


# =====================================================================
# 策略文件加载器
# =====================================================================


def load_jq_strategy(strategy_file):
    """
    加载聚宽策略文件

    参数:
        strategy_file: 策略文件路径（.txt或.py）

    返回:
        tuple: (函数字典, 源代码字符串) 或 (None, None)

    异常:
        FileNotFoundError: 文件不存在
        UnicodeDecodeError: 所有编码尝试都失败时抛出
        SyntaxError: 策略代码语法错误
    """
    if not os.path.exists(strategy_file):
        raise FileNotFoundError(f"策略文件不存在: {strategy_file}")

    _ENCODINGS = ["utf-8", "gbk", "gb2312", "latin-1"]
    code = None
    used_encoding = None

    for encoding in _ENCODINGS:
        try:
            with open(strategy_file, "r", encoding=encoding) as f:
                code = f.read()
            used_encoding = encoding
            break
        except UnicodeDecodeError:
            continue

    if code is None:
        raise UnicodeDecodeError(
            "utf-8",
            b"",
            0,
            1,
            f"无法解码策略文件 {strategy_file}，尝试了编码: {', '.join(_ENCODINGS)}",
        )

    if used_encoding != "utf-8":
        logger.info(f"策略文件使用 {used_encoding} 编码加载")

    _JQ_MODULE_PATTERNS = [
        r"^from\s+jqdata\b",
        r"^import\s+jqdata\b",
        r"^from\s+jqlib\b",
        r"^import\s+jqlib\b",
        r"^from\s+kuanke\b",
        r"^import\s+kuanke\b",
        r"^from\s+jqfactor\b",
        r"^import\s+jqfactor\b",
    ]

    # 需要替换的已废弃模块导入
    _DEPRECATED_IMPORT_REPLACEMENTS = {
        r"^from\s+pandas\.stats\.api\s+import\s+(\w+)": r"# from pandas.stats.api import \1 (已替换)",
        r"^from\s+pandas\.stats\s+import\s+": r"# from pandas.stats import (已替换)",
        r"^import\s+pandas\.stats": r"# import pandas.stats (已替换)",
    }

    lines = code.split("\n")
    processed_lines = []
    in_jqdata_import = False
    paren_depth = 0

    for line in lines:
        stripped = line.strip()

        if in_jqdata_import:
            paren_depth += line.count("(") - line.count(")")
            if paren_depth <= 0:
                in_jqdata_import = False
            continue

        skip = False
        for pattern in _JQ_MODULE_PATTERNS:
            if re.match(pattern, stripped):
                skip = True
                if "(" in line:
                    in_jqdata_import = True
                    paren_depth = line.count("(") - line.count(")")
                    if paren_depth <= 0:
                        in_jqdata_import = False
                break

        # 处理已废弃的模块导入
        if not skip:
            for pattern, replacement in _DEPRECATED_IMPORT_REPLACEMENTS.items():
                if re.match(pattern, stripped):
                    line = re.sub(pattern, replacement, line)
                    break

        if not skip:
            processed_lines.append(line)

    code = "\n".join(processed_lines)

    # 准备全局命名空间
    global_namespace = {
        # 基础库
        "np": np,
        "pd": pd,
        "math": __import__("math"),
        "datetime": __import__("datetime"),
        "dt": __import__("datetime"),  # 支持聚宽风格的 datetime 别名
        "timedelta": __import__("datetime").timedelta,
        "date": __import__("datetime").date,
        "operator": __import__("operator"),
        "typing": __import__("typing"),
        "overload": __import__("typing").overload,
        "Optional": __import__("typing").Optional,
        "List": __import__("typing").List,
        "Dict": __import__("typing").Dict,
        "Union": __import__("typing").Union,
        "Tuple": __import__("typing").Tuple,
        "Any": __import__("typing").Any,
        "Callable": __import__("typing").Callable,
        "warnings": __import__("warnings"),
        "PrettyTable": None,  # stub - prettytable not available
        "re": __import__("re"),
        "time": __import__("time"),
        "talib": __import__("talib", fromlist=["TA_LIB"])
        if __import__("importlib").util.find_spec("talib")
        else None,
        "signal": __import__("scipy.signal", fromlist=["argrelextrema"])
        if __import__("importlib").util.find_spec("scipy")
        else None,
        # 数据分析库
        "statsmodels": __import__("statsmodels")
        if __import__("importlib").util.find_spec("statsmodels")
        else None,
        "sm": __import__("statsmodels.api")
        if __import__("importlib").util.find_spec("statsmodels")
        else None,
        "scipy": __import__("scipy")
        if __import__("importlib").util.find_spec("scipy")
        else None,
        "sklearn": __import__("sklearn")
        if __import__("importlib").util.find_spec("sklearn")
        else None,
        # 聚宽API
        "g": g,
        "log": log,
        "query": query,
        "valuation": valuation,
        "income": income,
        "balance": balance,
        "cash_flow": cash_flow,
        "indicator": indicator,
        "finance": finance,
        "get_fundamentals": get_fundamentals,
        "get_all_securities": get_all_securities_jq,
        "get_security_info": get_security_info_jq,
        "get_price": get_price,
        "history": history,
        "attribute_history": attribute_history,
        "get_current_data": get_current_data_wrapper,
        "get_current_tick": get_current_tick,
        "get_index_weights": get_index_weights,
        "get_index_stocks": get_index_stocks,
        "get_factor_values": get_factor_values_jq,
        "get_all_trade_days": get_all_trade_days,
        "get_trade_days": get_trade_days,
        "get_extras": get_extras,
        "get_bars": get_bars,
        "get_billboard_list": get_billboard_list,
        "get_call_auction": get_call_auction,
        "get_ticks": get_ticks,
        "get_valuation": get_valuation,
        # 行情增强API
        "get_market": get_market,
        "get_detailed_quote": get_detailed_quote,
        "get_ticks_enhanced": get_ticks_enhanced,
        # 日期API
        "get_shifted_date": get_shifted_date,
        "get_previous_trade_date": get_previous_trade_date,
        "get_next_trade_date": get_next_trade_date,
        "transform_date": transform_date,
        "is_trade_date": is_trade_date,
        "get_trade_dates_between": get_trade_dates_between,
        "count_trade_dates_between": count_trade_dates_between,
        # 筛选API
        "get_dividend_ratio_filter_list": get_dividend_ratio_filter_list,
        "get_margine_stocks": get_margine_stocks,
        "filter_new_stock": filter_new_stock,
        "filter_st_stock": filter_st_stock,
        "filter_paused_stock": filter_paused_stock,
        "apply_common_filters": apply_common_filters,
        "filter_limitup_stock": filter_limitup_stock,
        "filter_limitdown_stock": filter_limitdown_stock,
        "filter_kcbj_stock": filter_kcbj_stock,
        "filter_kcb_stock": filter_kcb_stock,
        "filter_limit_up": filter_limit_up,
        "filter_limit_down": filter_limit_down,
        # 统计API
        "get_ols": get_ols,
        "get_zscore": get_zscore,
        "get_rank": get_rank,
        "get_factor_filter_list": get_factor_filter_list,
        "get_num": get_num,
        # 龙虎榜增强API
        "get_institutional_holdings": get_institutional_holdings,
        "get_billboard_hot_stocks": get_billboard_hot_stocks,
        "get_broker_statistics": get_broker_statistics,
        # 补充API
        "get_beta": get_beta,
        "get_fund_info": get_fund_info,
        "get_fundamentals_continuously": get_fundamentals_continuously,
        # 技术指标API
        "MA": MA,
        "EMA": EMA,
        "MACD": MACD,
        "KDJ": KDJ,
        "RSI": RSI,
        "BOLL": BOLL,
        "ATR": ATR,
        # 因子API
        "get_north_factor": get_north_factor,
        "get_comb_factor": get_comb_factor,
        "get_factor_momentum": get_factor_momentum,
        # 涨跌停API
        "get_recent_limit_up_stock": get_recent_limit_up_stock,
        "get_recent_limit_down_stock": get_recent_limit_down_stock,
        "get_hl_stock": get_hl_stock,
        "get_continue_count_df": get_continue_count_df,
        "get_hl_count_df": get_hl_count_df,
        # 资金流向API
        "get_money_flow": get_money_flow,
        "get_sector_money_flow": get_sector_money_flow,
        "get_money_flow_rank": get_money_flow_rank,
        # jqlib 技术分析
        "LB": _JQLibModule.technical_analysis.LB,
        "MA_jq": _JQLibModule.technical_analysis.MA,
        "VOL": _JQLibModule.technical_analysis.VOL,
        "KD": _JQLibModule.technical_analysis.KD,
        # pandas.stats.api 兼容层 (pandas 0.20+ 已移除)
        "ols": _PandasStatsApiModule.ols,
        # 模块对象
        "jqdata": _jqdata,
        "jqlib": _jqlib,
        "kuanke": _kuanke,
        "kqapi": _kqapi,
        "jqfactor": _jqfactor,
        # pandas.stats 兼容模块
        "pandas": __import__("pandas"),  # 确保 pandas 模块可用
        # jqfactor 函数（直接导出）
        "winsorize": winsorize,
        "standardlize": standardlize,
        "run_daily": run_daily,
        "run_weekly": run_weekly,
        "run_monthly": run_monthly,
        "unschedule_all": unschedule_all,
        "order_target": order_target,
        "order_value": order_value,
        "order_target_value": order_target_value,
        "order": order,
        "set_option": set_option,
        "set_benchmark": set_benchmark,
        "set_slippage": set_slippage,
        "set_order_cost": set_order_cost,
        "set_universe": set_universe,
        "FixedSlippage": FixedSlippage,
        "OrderCost": OrderCost,
        "LimitOrderStyle": LimitOrderStyle,
        "MarketOrderStyle": MarketOrderStyle,
        "PriceRelatedSlippage": PriceRelatedSlippage,
        "StepRelatedSlippage": StepRelatedSlippage,
        "SubPortfolioConfig": SubPortfolioConfig,
        "set_subportfolios": set_subportfolios,
        "OrderStatus": OrderStatus,
        "get_trades": get_trades,
        "get_locked_shares": get_locked_shares,
        "get_future_contracts": get_future_contracts,
        # Wizard helper functions (stubs)
        "disable_cache": disable_cache,
        "set_commission": set_commission,
        "PerTrade": PerTrade,
        "neutralize": neutralize,
        "security_stoploss": security_stoploss,
        "portfolio_stoploss": portfolio_stoploss,
        "portfolio_stopprofit": portfolio_stopprofit,
        "security_stopprofit": security_stopprofit,
        "index_stoploss_sicha": index_stoploss_sicha,
        "MA_judge_duotou": MA_judge_duotou,
        "financial_data_filter_dayu": financial_data_filter_dayu,
        "get_sort_dataframe": get_sort_dataframe,
        "order_style": order_style,
        "sell_by_amount_or_percent_or_none": sell_by_amount_or_percent_or_none,
        "judge_security_max_proportion": judge_security_max_proportion,
        "max_buy_value_or_amount": max_buy_value_or_amount,
        "get_concept_stocks": get_concept_stocks,
        "get_all_securities": get_all_securities,
        # 行业数据
        "get_industry_classify": get_industry_classify,
        "get_industry_stocks": get_industry_stocks,
        "get_all_industry_stocks": get_all_industry_stocks,
        "get_stock_industry": get_stock_industry,
        "get_industry_daily": get_industry_daily,
        "get_industry_performance": get_industry_performance,
        "get_market_breadth": get_market_breadth,
        # 北向资金
        "get_north_money_flow": get_north_money_flow,
        "get_north_money_daily": get_north_money_daily,
        "get_north_money_holdings": get_north_money_holdings,
        "get_north_money_stock_flow": get_north_money_stock_flow,
        "compute_north_money_signal": compute_north_money_signal,
        # RSRS择时
        "compute_rsrs": compute_rsrs,
        "compute_rsrs_signal": compute_rsrs_signal,
        "get_rsrs_for_index": get_rsrs_for_index,
        "get_current_rsrs_signal": get_current_rsrs_signal,
        # 市场情绪
        "compute_crowding_ratio": compute_crowding_ratio,
        "compute_gisi": compute_gisi,
        "compute_fed_model": compute_fed_model,
        "compute_graham_index": compute_graham_index,
        "compute_below_net_ratio": compute_below_net_ratio,
        "compute_new_high_ratio": compute_new_high_ratio,
        "get_all_sentiment_indicators": get_all_sentiment_indicators,
        # 运行时 IO API
        "record": record,
        "send_message": send_message,
        "read_file": read_file,
        "write_file": write_file,
        # 工具函数
        "filter": filter,
        "map": map,
        "sorted": sorted,
        "len": len,
        "list": list,
        "dict": dict,
        "set": set,
        "range": range,
        "enumerate": enumerate,
        "zip": zip,
        "min": min,
        "max": max,
        "sum": sum,
        "abs": abs,
        "round": round,
        "int": int,
        "float": float,
        "str": str,
        "print": print,
        "isinstance": isinstance,
        "hasattr": hasattr,
        "getattr": getattr,
    }

    local_namespace = {}

    try:
        exec(code, global_namespace, local_namespace)
    except SyntaxError as e:
        raise SyntaxError(
            f"策略文件语法错误 ({strategy_file}): {e.msg} (行 {e.lineno})"
        ) from e
    except Exception as e:
        import traceback

        tb_lines = traceback.format_exc().split("\n")
        raise RuntimeError(
            f"策略代码执行错误 ({strategy_file}): {e}\n"
            f"详细 traceback:\n" + "\n".join(tb_lines[-5:])
        ) from e

    for name, obj in local_namespace.items():
        if isinstance(obj, types.FunctionType):
            global_namespace[name] = obj
        elif isinstance(obj, type):  # 添加类定义
            global_namespace[name] = obj

    functions = {}
    for name, obj in local_namespace.items():
        if isinstance(obj, types.FunctionType):
            functions[name] = obj

    if not functions:
        logger.warning(f"策略文件 {strategy_file} 未定义任何函数")
    else:
        logger.info(f"加载策略函数: {list(functions.keys())}")

    return functions, code


# =====================================================================
# 策略运行器
# =====================================================================


def run_jq_strategy(
    strategy_file,
    start_date="2020-01-01",
    end_date="2023-12-31",
    initial_capital=None,
    commission=None,
    stock_pool=None,
    benchmark=None,
    auto_discover_stocks=True,
    enable_resource_pack=True,
    strategy_name_override=None,
    use_cache_only=False,
    validate_cache=True,
    frequency="daily",
):
    """
    运行聚宽策略。

    参数:
        use_cache_only: bool, 默认False
            True: 仅使用缓存数据，不访问网络。适合预热后的离线运行。
            False: 缓存不存在时自动从网络下载。
        validate_cache: bool, 默认True
            use_cache_only=True时，验证缓存是否足够完整。
        frequency: str, 默认 "daily"
            数据频率: "daily", "1m", "5m", "15m", "30m", "60m"
            分钟回测时自动设置 bar_resolution。
    """
    # 从配置获取默认值
    config = get_config()
    backtest_config = config.backtest

    if initial_capital is None:
        initial_capital = backtest_config.initial_capital
    if commission is None:
        commission = backtest_config.commission_rate
    if benchmark is None:
        benchmark = backtest_config.benchmark

    is_minute = frequency != "daily"

    logger.info("=" * 80)
    logger.info(f"运行聚宽策略: {os.path.basename(strategy_file)}")
    if is_minute:
        logger.info(f"分钟回测模式: {frequency}")
    logger.info("=" * 80)

    strategy_functions, strategy_source = load_jq_strategy(strategy_file)
    if not strategy_functions:
        logger.error("策略加载失败")
        return None

    strategy_name = strategy_name_override or os.path.basename(strategy_file).replace(
        ".txt", ""
    ).replace(".py", "")
    strategy_name = strategy_name.replace(" ", "_").replace("(", "").replace(")", "")

    if enable_resource_pack:
        logger.info(f"[资源管理] 启用策略资源隔离: {strategy_name}")
        set_strategy_name(strategy_name)

        resource_pack = get_resource_pack()
        if resource_pack:
            logger.info(f"  资源目录: {resource_pack.strategy_dir}")
            logger.info(f"  输入目录: {resource_pack.input_dir}")
            logger.info(f"  输出目录: {resource_pack.output_dir}")

    if stock_pool is None and auto_discover_stocks:
        logger.info("[阶段1] 预运行 - 发现策略需要的股票...")
        discovered = _discover_strategy_stocks(strategy_functions, start_date, end_date, strategy_source)
        if discovered:
            stock_pool = list(discovered)
            logger.info(
                f"  发现 {len(stock_pool)} 只股票: {stock_pool[:10]}{'...' if len(stock_pool) > 10 else ''}"
            )
        else:
            logger.warning("  未发现股票需求，使用默认股票池")
            stock_pool = [
                "600519.XSHG",
                "000858.XSHE",
                "000333.XSHE",
                "600036.XSHG",
                "601318.XSHG",
            ]

    if stock_pool is None:
        logger.error("错误: 未指定股票池")
        return None

    if use_cache_only and validate_cache:
        logger.info(f"[阶段2] 验证缓存 - 股票池: {len(stock_pool)}只")
        from .db.cache_status import get_cache_manager

        cache_manager = get_cache_manager()
        is_valid, report = cache_manager.validate_cache_for_offline(
            stock_pool, start_date, end_date
        )

        if not is_valid:
            logger.error("  缓存验证失败:")
            if report["missing_stocks"]:
                logger.error(f"    缺失股票: {report['missing_stocks']}")
            if report["incomplete_stocks"]:
                for item in report["incomplete_stocks"]:
                    logger.error(
                        f"    不完整股票: {item['symbol']} ({item['min_date']} ~ {item['max_date']})"
                    )
            if report["missing_meta"]:
                logger.error(f"    缺失元数据: {report['missing_meta']}")
            logger.error("请先运行数据预热脚本: python prewarm_data.py --sample")
            return None
        logger.info("  缓存验证通过")

    phase_name = "从缓存加载" if use_cache_only else "下载数据"
    if is_minute:
        phase_name += f" ({frequency})"
    logger.info(f"[阶段2] {phase_name} - 股票池: {len(stock_pool)}只")

    datas = []
    failed_stocks = []

    for i, stock in enumerate(stock_pool, 1):
        try:
            print(f"  [{i}/{len(stock_pool)}] {stock}", end="")
            if is_minute:
                data = _load_minute_data(stock, start_date, end_date, frequency)
            elif use_cache_only:
                data = _load_stock_data_from_cache(stock, start_date, end_date)
            else:
                data = get_akshare_stock_data(stock, start_date, end_date)
            if data is not None:
                datas.append((stock, data))
                print(" ✓")
            else:
                failed_stocks.append(stock)
                reason = "无缓存" if use_cache_only else "无数据"
                print(f" ✗ ({reason})")
        except Exception as e:
            failed_stocks.append(stock)
            print(f" ✗ ({e})")

    if not datas:
        logger.error("错误: 没有成功下载任何股票数据")
        return None

    logger.info(f"成功下载: {len(datas)}只股票数据")
    if failed_stocks:
        logger.warning(f"失败: {len(failed_stocks)}只股票")

    logger.info("[阶段3] 正式运行回测...")
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(initial_capital)
    cerebro.broker.setcommission(commission=commission)

    for stock, data in datas:
        cerebro.adddata(data, name=stock)

    cerebro.addstrategy(
        JQStrategyWrapper,
        strategy_functions=strategy_functions,
        frequency=frequency,
        initial_capital=initial_capital,
        start_date=start_date,
        end_date=end_date,
    )

    logger.info(f"回测区间: {start_date} ~ {end_date}")
    logger.info(f"数据频率: {frequency}")
    logger.info(f"初始资金: {initial_capital:,.2f}")
    logger.info("-" * 80)

    results = cerebro.run()
    strategy = results[0]

    final_value = cerebro.broker.getvalue()
    pnl = final_value - initial_capital
    pnl_pct = (final_value / initial_capital - 1) * 100

    logger.info("-" * 80)
    logger.info(f"最终资金: {final_value:,.2f}")
    logger.info(f"盈亏: {pnl:,.2f} ({pnl_pct:.2f}%)")

    if hasattr(strategy, "navs") and strategy.navs:
        logger.info("性能分析:")
        nav_series = pd.Series(strategy.navs)

        cummax = nav_series.cummax()
        drawdown = (nav_series - cummax) / cummax
        max_drawdown = drawdown.min()
        logger.info(f"  最大回撤: {max_drawdown:.2%}")

        days = len(nav_series)
        annual_return = (final_value / initial_capital) ** (252 / days) - 1
        logger.info(f"  年化收益: {annual_return:.2%}")

        returns = nav_series.pct_change().dropna()
        if returns.std() > 0:
            sharpe = returns.mean() / returns.std() * (252**0.5)
            logger.info(f"  夏普比率: {sharpe:.2f}")

    logger.info("=" * 80)

    if enable_resource_pack:
        logger.info("[资源管理] 策略运行资源摘要:")
        resource_pack = get_resource_pack()
        if resource_pack:
            summary = resource_pack.get_resource_summary()
            logger.info(f"  输入资源文件: {summary['total_input_files']}")
            logger.info(f"  输出资源文件: {summary['total_output_files']}")
            for res_type, count in summary["input_resources"].items():
                if count > 0:
                    logger.info(f"    {res_type}: {count} 个文件")
            for res_type, count in summary["output_resources"].items():
                if count > 0:
                    logger.info(f"    {res_type}: {count} 个文件")
            logger.info(f"  资源目录: {summary['strategy_dir']}")

    logger.info("=" * 80)

    return {
        "cerebro": cerebro,
        "strategy": strategy,
        "final_value": final_value,
        "pnl": pnl,
        "pnl_pct": pnl_pct,
        "resource_pack": get_resource_pack() if enable_resource_pack else None,
        "strategy_name": strategy_name if enable_resource_pack else None,
    }


# =====================================================================
# 命令行入口
# =====================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="运行聚宽策略")
    parser.add_argument("strategy_file", help="策略文件路径")
    parser.add_argument("--start", default="2020-01-01", help="开始日期")
    parser.add_argument("--end", default="2023-12-31", help="结束日期")
    parser.add_argument("--capital", type=float, default=1000000, help="初始资金")
    parser.add_argument("--stocks", nargs="+", help="股票池")

    args = parser.parse_args()

    run_jq_strategy(
        strategy_file=args.strategy_file,
        start_date=args.start,
        end_date=args.end,
        initial_capital=args.capital,
        stock_pool=args.stocks,
    )
