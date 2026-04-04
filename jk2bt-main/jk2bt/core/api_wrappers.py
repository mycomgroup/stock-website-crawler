"""
api_wrappers.py
聚宽 API 封装函数。

包含:
- get_price, get_price_jq, get_price_unified: 行情数据获取
- history, attribute_history: 历史数据获取
- get_fundamentals, get_history_fundamentals: 基本面数据获取
- get_index_stocks, get_index_weights: 指数成分股获取
- get_all_securities, get_security_info: 证券元数据获取
- get_all_trade_days: 交易日获取
- get_extras: ST/停牌等额外信息
- get_billboard_list: 龙虎榜数据
- get_factor_values: 因子数据
- get_bars: K线数据
- 期货相关API
- get_current_data, get_current_tick: 当前数据获取
- analyze_performance: 绩效分析
"""

import os
import re
import warnings
import logging
import backtrader as bt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date

try:
    import statsmodels.api as sm
except ImportError:
    sm = None

# akshare 改为延迟导入，减少启动依赖

# 从子模块导入
from .securities_utils import (
    format_stock_symbol_for_akshare,
    jq_code_to_ak,
    ak_code_to_jq,
    _stock_code_to_jq,
    _find_date_column,
    _resolve_cache_dir,
    _format_index_code,
    _normalize_index_weights,
    SUPPORTED_INDEXES,
    CONS_ONLY_INDICES,
    INDEX_FALLBACK_MAP,
    INDEX_DESCRIPTION,
    INDEX_CODE_ALIAS_MAP,
    RobustResult,
)
from .data_proxies import (
    SecurityInfo,
    _QueryBuilder,
    _Expression,
    _FieldProxy,
    _TableProxy,
    _FinanceTableProxy,
    _FinanceFieldProxy,
    _FinanceModule,
    valuation,
    income,
    cash_flow,
    balance,
    indicator,
    _CurrentDataEntry,
    _CurrentDataProxy,
    _TickDataProxy,
)
from .global_state import (
    log,
    logger,
    _prerun_mode_active,
    _prerun_requested_stocks,
)

# =====================================================================
# 指数成分股 API
# =====================================================================


def get_index_weights(index_code, date=None, cache_dir="index_cache", robust=False):
    """
    获取指数成分股权重

    参数:
        index_code: 指数代码，支持 '000300.XSHG', '000300' 等格式
        date: 查询日期，默认最新
        cache_dir: 缓存目录
        robust: bool - 是否返回 RobustResult 对象（包含成功状态和原因）

    返回:
        DataFrame 或 RobustResult, index=股票代码, columns=['weight', 'display_name']

    稳健模式示例:
        result = get_index_weights('000300.XSHG', robust=True)
        if result.success:
            weights = result.data
        else:
            log.warn(f"获取失败: {result.reason}")
    """
    try:
        from ..market_data.index_components import get_index_weights as _get_index_weights_impl
    except ImportError:
        from jk2bt.market_data.index_components import get_index_weights as _get_index_weights_impl

    try:
        use_duckdb = True
        df = _get_index_weights_impl(
            index_code,
            date=date,
            cache_dir=cache_dir,
            use_duckdb=use_duckdb,
        )

        # 转换为预期的 DataFrame 格式
        if df.empty:
            result_data = pd.DataFrame(columns=["weight", "display_name"])
        else:
            # 获取股票代码列（优先使用stock_code，fallback到code）
            code_col = "stock_code" if "stock_code" in df.columns else "code"
            stock_codes = df[code_col].tolist() if code_col in df.columns else []
            result_data = pd.DataFrame(index=stock_codes)
            result_data["weight"] = df["weight"].tolist() if "weight" in df.columns else [0] * len(stock_codes)
            # 获取股票名称列（优先使用stock_name，fallback到display_name）
            name_col = "stock_name" if "stock_name" in df.columns else "display_name"
            result_data["display_name"] = df[name_col].tolist() if name_col in df.columns else [""] * len(stock_codes)

        if robust:
            return RobustResult(
                success=not result_data.empty,
                data=result_data,
                reason=f"成功获取 {len(result_data)} 只成分股权重" if not result_data.empty else "无数据",
                source="index_components",
            )
        return result_data

    except Exception as e:
        error_msg = f"获取指数权重异常: {e}"
        logger.error(error_msg)
        if robust:
            return RobustResult(
                success=False,
                data=pd.DataFrame(columns=["weight", "display_name"]),
                reason=error_msg,
                source="fallback",
            )
        return pd.DataFrame(columns=["weight", "display_name"])


def get_index_weights_robust(index_code, date=None, cache_dir="index_cache"):
    """稳健版获取指数权重，返回 RobustResult 对象"""
    return get_index_weights(index_code, date, cache_dir, robust=True)


def get_index_stocks(index_code, date=None, cache_dir="index_cache", robust=False):
    """
    获取指数成分股列表

    参数:
        index_code: 指数代码，支持 '000300.XSHG', '000300' 等格式
        date: 查询日期，默认最新
        cache_dir: 缓存目录
        robust: bool - 是否返回 RobustResult 对象

    返回:
        list 或 RobustResult: 股票代码列表，如 ['600519.XSHG', '000858.XSHE', ...]

    稳健模式示例:
        result = get_index_stocks('000300.XSHG', robust=True)
        if result.success:
            stocks = result.data
        else:
            log.warn(f"获取失败: {result.reason}")

    注意: 空列表 [] 不代表成功，可能表示指数不支持或数据获取失败。
    使用 robust=True 可明确区分成功/失败状态。
    """
    try:
        from ..market_data.index_components import get_index_stocks as _get_index_stocks_impl
    except ImportError:
        from jk2bt.market_data.index_components import get_index_stocks as _get_index_stocks_impl

    try:
        use_duckdb = True
        stocks = _get_index_stocks_impl(
            index_code,
            cache_dir=cache_dir,
            use_duckdb=use_duckdb,
        )

        # 预运行模式下记录请求的股票
        if _prerun_mode_active and stocks:
            _prerun_requested_stocks.update(stocks)

        if robust:
            return RobustResult(
                success=bool(stocks),
                data=stocks,
                reason=f"成功获取 {len(stocks)} 只成分股" if stocks else "无数据",
                source="index_components",
            )
        return stocks

    except Exception as e:
        error_msg = f"获取指数成分股异常: {e}"
        logger.error(error_msg)
        if robust:
            return RobustResult(
                success=False,
                data=[],
                reason=error_msg,
                source="fallback",
            )
        return []


def get_index_stocks_robust(index_code, date=None, cache_dir="index_cache"):
    """稳健版获取指数成分股，返回 RobustResult 对象"""
    return get_index_stocks(index_code, date, cache_dir, robust=True)


# =====================================================================
# 行情数据 API
# =====================================================================


def get_akshare_etf_data(symbol, start, end, force_update=False):
    """
    获取 ETF 日线行情，返回 bt.feeds.PandasData 对象（供 Cerebro.adddata 使用）。
    使用 DuckDB 存储数据。
    symbol: ETF 代码，如 '518880'
    """
    try:
        from ..market_data.etf import get_etf_daily
    except ImportError:
        from market_data.etf import get_etf_daily

    df = get_etf_daily(symbol, start, end, force_update=force_update)

    if df.empty:
        raise ValueError(f"数据时间范围内无可用数据: {start} ~ {end}")

    df = df[
        ["datetime", "open", "high", "low", "close", "volume", "openinterest"]
    ].copy()

    data = bt.feeds.PandasData(
        dataname=df,
        datetime="datetime",
        open="open",
        high="high",
        low="low",
        close="close",
        volume="volume",
        openinterest="openinterest",
        name=symbol,
    )
    return data


def get_akshare_stock_data(symbol, start, end, force_update=False, adjust="qfq"):
    """
    获取 A 股日线行情，返回 bt.feeds.PandasData 对象。
    使用 DuckDB 存储数据。
    symbol: 如 'sh600519'、'sz000001'
    adjust: 'qfq' 前复权 / 'hfq' 后复权 / '' 不复权
    """
    try:
        from ..market_data.stock import get_stock_daily
    except ImportError:
        from market_data.stock import get_stock_daily

    df = get_stock_daily(symbol, start, end, force_update=force_update, adjust=adjust)

    if df.empty:
        raise ValueError(f"股票数据时间范围内无可用数据: {start} ~ {end}")

    df = df[
        ["datetime", "open", "high", "low", "close", "volume", "openinterest"]
    ].copy()

    data = bt.feeds.PandasData(
        dataname=df,
        datetime="datetime",
        open="open",
        high="high",
        low="low",
        close="close",
        volume="volume",
        openinterest="openinterest",
        name=symbol,
    )
    return data


def get_index_nav(symbol, start, end, force_update=False):
    """获取指数净值序列（归一化），用于基准比较。使用 DuckDB 存储。"""
    try:
        from ..market_data.index import get_index_daily
    except ImportError:
        from market_data.index import get_index_daily

    df = get_index_daily(symbol, start, end, force_update=force_update)

    if df.empty:
        raise ValueError(f"指数数据时间范围内无可用数据: {start} ~ {end}")

    df = df.sort_values("datetime")
    df["nav"] = df["close"] / df["close"].iloc[0]
    return df.set_index("datetime")["nav"]


def get_price_unified(
    security,
    start_date=None,
    end_date=None,
    frequency="daily",
    fields=None,
    skip_paused=True,
    fq="pre",
    count=None,
    panel=True,
    fill_paused=True,
):
    """
    统一的聚宽风格行情接口（使用 market_api 兼容层）。

    参数
    ----
    security : str or list
        股票代码，如 '600519.XSHG' 或 ['600519.XSHG', '000001.XSHE']
    start_date : str
        起始日期 'YYYY-MM-DD'
    end_date : str
        结束日期 'YYYY-MM-DD'
    frequency : str
        频率，'daily', '1m', '5m', '15m', '30m', '60m'
    fields : list
        字段列表，如 ['open', 'close', 'high', 'low', 'paused', 'pre_close', 'high_limit', 'low_limit']
    skip_paused : bool
        是否跳过停牌数据
    fq : str
        复权方式，'pre'=前复权, 'post'=后复权, 'none'=不复权
    count : int
        历史数据条数
    panel : bool
        返回格式（True=dict, False=DataFrame）
    fill_paused : bool
        是否填充停牌数据

    返回
    ----
    单标的：DataFrame
    多标的：dict{symbol: DataFrame} 或 DataFrame

    示例
    ----
    df = get_price_unified('600519.XSHG', end_date='2023-12-31', count=30)
    """
    try:
        from ..api.market import get_price as _get_price_impl
    except ImportError:
        from jk2bt.api.market import get_price as _get_price_impl

    return _get_price_impl(
        security=security,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        fields=fields,
        skip_paused=skip_paused,
        fq=fq,
        count=count,
        panel=panel,
        fill_paused=fill_paused,
    )


def get_price_jq(
    symbols,
    start_date=None,
    end_date=None,
    frequency="daily",
    fields=None,
    adjust="qfq",
    count=None,
    panel=True,
    fill_paused=True,
    skip_paused=True,
    cache_dir="stock_cache",
    force_update=False,
    fq=None,
    skip_paused_flag=None,
):
    """
    JQData 风格 get_price，AkShare 适配。
    支持单只/多只，日线/分钟，复权，字段筛选，panel 参数。

    参数
    ----
    symbols : str or list
        股票代码
    start_date : str
        起始日期
    end_date : str
        结束日期
    frequency : str
        频率 'daily', '1m', '5m', '15m', '30m', '60m'
    fields : list
        字段列表，支持 ['open', 'close', 'high', 'low', 'volume', 'money', 'paused', 'pre_close', 'high_limit', 'low_limit']
    adjust : str
        复权方式 'qfq'=前复权, 'hfq'=后复权, ''=不复权
    count : int
        历史数据条数
    panel : bool
        返回格式（True=dict, False=DataFrame）
    fill_paused : bool
        是否填充停牌数据
    skip_paused : bool
        是否跳过停牌数据

    返回
    ----
    单标的：DataFrame
    多标的：dict{symbol: DataFrame}（默认，panel=True）或 DataFrame（panel=False）
    """
    try:
        from ..api.market import get_price as _get_price_impl
    except ImportError:
        from jk2bt.api.market import get_price as _get_price_impl

    fq_map = {"qfq": "pre", "hfq": "post", "": "none", None: "pre", "pre": "pre", "post": "post", "none": "none"}
    # 如果直接传入 fq 参数，优先使用它
    if fq is not None:
        fq_value = fq
    else:
        fq_value = fq_map.get(adjust, "pre")

    # 处理 skip_paused 参数兼容性
    if skip_paused_flag is not None:
        skip_paused = skip_paused_flag

    extended_fields = fields
    if fields and not any(
        f in fields for f in ["paused", "pre_close", "high_limit", "low_limit"]
    ):
        extended_fields = list(fields) + [
            "paused",
            "pre_close",
            "high_limit",
            "low_limit",
        ]

    result = _get_price_impl(
        security=symbols,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        fields=extended_fields,
        skip_paused=skip_paused,
        fq=fq_value,
        count=count,
        panel=True,
        fill_paused=fill_paused,
    )

    if fields and extended_fields != fields:
        if isinstance(result, dict):
            for sym, df in result.items():
                if not df.empty:
                    keep_cols = ["datetime"] + [f for f in fields if f in df.columns]
                    result[sym] = df[[c for c in keep_cols if c in df.columns]]
        elif isinstance(result, pd.DataFrame) and not result.empty:
            keep_cols = ["datetime"] + [f for f in fields if f in result.columns]
            result = result[[c for c in keep_cols if c in result.columns]]

    # 聚宽 Panel 格式转换
    # 当请求多个股票且 panel=True 时，聚宽返回 {field_name: DataFrame} 格式
    # DataFrame 的 index 是日期，columns 是股票代码
    if isinstance(result, dict) and len(result) > 1 and panel:
        # 将 {symbol: DataFrame} 转换为 {field_name: DataFrame} 格式
        # 这是聚宽的 panel 格式
        field_data = {}
        # 获取所有日期作为索引
        all_dates = set()
        for sym, df in result.items():
            if not df.empty:
                if 'datetime' in df.columns:
                    all_dates.update(df['datetime'].tolist())
                elif df.index.name == 'datetime' or isinstance(df.index, pd.DatetimeIndex):
                    all_dates.update(df.index.tolist())

        # 确定要转换的字段
        fields_to_convert = fields if fields else ['open', 'high', 'low', 'close', 'volume', 'money']

        for field in fields_to_convert:
            # 创建 DataFrame: index=dates, columns=symbols
            field_df = pd.DataFrame(index=sorted(all_dates))
            for sym, df in result.items():
                if not df.empty and field in df.columns:
                    if 'datetime' in df.columns:
                        # 使用 datetime 列作为索引
                        temp_df = df.set_index('datetime')[[field]]
                        field_df[sym] = temp_df[field]
                    else:
                        # 已经是 datetime 索引
                        field_df[sym] = df[field]
            if not field_df.empty:
                field_data[field] = field_df

        # 如果只有一个字段请求，直接返回该字段的 DataFrame（聚宽行为）
        if fields and len(fields) == 1 and fields[0] in field_data:
            return field_data[fields[0]]

        return field_data

    if isinstance(result, dict) and len(result) > 1 and not panel:
        combined = []
        for sym, df in result.items():
            if not df.empty:
                df_copy = df.copy()
                df_copy["code"] = sym
                combined.append(df_copy)
        if combined:
            return pd.concat(combined, ignore_index=True)
        return pd.DataFrame()

    # 单股票情况，直接返回 DataFrame
    if isinstance(result, dict) and len(result) == 1:
        return list(result.values())[0]

    return result


# 默认 get_price 指向聚宽风格版本
get_price = get_price_jq


def history(
    count,
    unit="1d",
    field="close",
    security_list=None,
    df=True,
    skip_paused=False,
    fq="pre",
    cache_dir="stock_cache",
    end_date=None,
):
    """
    聚宽风格 history：获取多个标的单个字段历史数据。
    返回 DataFrame，index=日期，columns=股票代码。

    参数
    ----
    count : int
        历史数据条数
    unit : str
        时间单位 '1d', '1m'
    field : str
        字段名，支持 'open', 'close', 'high', 'low', 'volume', 'money', 'paused', 'pre_close', 'high_limit', 'low_limit'
    security_list : list
        股票代码列表
    df : bool
        是否返回 DataFrame
    skip_paused : bool
        是否跳过停牌数据
    fq : str
        复权方式 'pre', 'post', 'none'
    end_date : str
        结束日期

    返回
    ----
    df=True: DataFrame(index=日期, columns=股票代码)
    df=False: dict{symbol: array}
    """
    try:
        from ..api.market import history as _history_impl
    except ImportError:
        from jk2bt.api.market import history as _history_impl

    if security_list is None:
        if df:
            return pd.DataFrame()
        return {}

    if isinstance(security_list, str):
        security_list = [security_list]

    result = _history_impl(
        count=count,
        unit=unit,
        field=field,
        security_list=security_list,
        df=df,
        skip_paused=skip_paused,
        fq=fq,
        end_date=end_date,
    )

    return result


def attribute_history(
    security,
    count,
    unit="1d",
    fields=None,
    skip_paused=True,
    df=True,
    fq="pre",
    cache_dir="stock_cache",
    end_date=None,
):
    """
    聚宽风格 attribute_history：获取单个标的多字段历史数据。
    返回 DataFrame，index=日期，columns=字段名。

    参数
    ----
    security : str
        股票代码
    count : int
        历史数据条数
    unit : str
        时间单位 '1d', '1m'
    fields : list
        字段列表，支持 ['open', 'close', 'high', 'low', 'volume', 'money', 'paused', 'pre_close', 'high_limit', 'low_limit']
    skip_paused : bool
        是否跳过停牌数据
    df : bool
        是否返回 DataFrame
    fq : str
        复权方式 'pre', 'post', 'none'
    end_date : str
        结束日期

    返回
    ----
    df=True: DataFrame(index=日期, columns=字段)
    df=False: dict{field: array}
    """
    try:
        from ..api.market import attribute_history as _attribute_history_impl
    except ImportError:
        from jk2bt.api.market import attribute_history as _attribute_history_impl

    if fields is None:
        fields = ["open", "close", "high", "low", "volume", "money"]

    result = _attribute_history_impl(
        security=security,
        count=count,
        unit=unit,
        fields=fields,
        skip_paused=skip_paused,
        df=df,
        fq=fq,
        end_date=end_date,
    )

    return result


def get_bars_jq(
    security,
    count,
    unit="1d",
    fields=None,
    include_now=False,
    end_dt=None,
    fq="pre",
    skip_paused=False,
):
    """
    JQData 风格 get_bars，分钟/日线历史 K 线。

    参数
    ----
    security : str or list
        股票代码
    count : int
        历史数据条数
    unit : str
        时间单位 '1d', '1m', '5m', '15m', '30m', '60m'
    fields : list
        字段列表，支持 ['open', 'close', 'high', 'low', 'volume', 'money', 'paused', 'pre_close', 'high_limit', 'low_limit']
    include_now : bool
        是否包含当前 bar
    end_dt : datetime
        结束时间
    fq : str
        复权方式 'pre', 'post', 'none'
    skip_paused : bool
        是否跳过停牌

    返回
    ----
    DataFrame
    """
    try:
        from ..api.market import get_bars as _get_bars_impl
    except ImportError:
        from jk2bt.api.market import get_bars as _get_bars_impl

    result = _get_bars_impl(
        security=security,
        count=count,
        unit=unit,
        fields=fields,
        include_now=include_now,
        end_dt=end_dt,
        fq=fq,
        skip_paused=skip_paused,
    )

    return result


get_bars = get_bars_jq


# =====================================================================
# Current Data API
# =====================================================================


def get_current_data(bt_strategy=None):
    """
    聚宽风格 get_current_data()。
    在回测场景中建议传入当前 bt.Strategy 实例以直接读取 bar 数据。
    示例：
        current = get_current_data(context)
        price = current['sh600519'].last_price
    """
    return _CurrentDataProxy(bt_strategy)


def get_current_tick(security, bt_strategy=None):
    """
    获取当前tick数据（聚宽兼容接口）。

    参数:
        security: 股票代码，如 '000001.XSHG'
        bt_strategy: bt.Strategy 实例

    返回:
        _TickDataProxy 对象，具有 .current 属性表示当前价格

    示例：
        tick = get_current_tick('000001.XSHG')
        price = tick.current  # 当前价格
    """
    # 如果没有传入策略实例，尝试获取当前策略实例
    if bt_strategy is None:
        try:
            from jk2bt.core.runner import _get_current_strategy
            bt_strategy = _get_current_strategy()
        except ImportError:
            pass
    return _TickDataProxy(security, bt_strategy)


# =====================================================================
# Performance Analysis
# =====================================================================


def analyze_performance(strategy_nav, benchmark_nav):
    """输出策略绩效指标：年化收益、夏普、信息比率、Alpha/Beta、最大回撤、索提诺。"""
    strategy_nav = pd.Series(strategy_nav)
    # 兼容 pandas 3.0（fillna method= 已由文件头部 patch 处理）
    benchmark_nav = (
        pd.Series(benchmark_nav).reindex(strategy_nav.index).fillna(method="ffill")
    )

    strategy_ret = strategy_nav.pct_change().dropna()
    benchmark_ret = benchmark_nav.pct_change().dropna()
    benchmark_ret.name = "benchmark"
    benchmark_ret = benchmark_ret.reindex(strategy_ret.index).fillna(0)

    days = len(strategy_ret)
    total_return = strategy_nav.iloc[-1] / strategy_nav.iloc[0] - 1
    annual_return = (strategy_nav.iloc[-1] / strategy_nav.iloc[0]) ** (
        252 / max(days, 1)
    ) - 1
    excess_ret = strategy_ret - benchmark_ret

    sharpe_ratio = (
        strategy_ret.mean() / strategy_ret.std() * np.sqrt(252)
        if strategy_ret.std() != 0
        else np.nan
    )
    info_ratio = (
        excess_ret.mean() / excess_ret.std() * np.sqrt(252)
        if excess_ret.std() != 0
        else np.nan
    )

    if sm is not None:
        X = sm.add_constant(benchmark_ret)
        model = sm.OLS(strategy_ret, X).fit()
        alpha = model.params.get("const", 0) * 252
        beta = model.params.get(benchmark_ret.name, 0)
    else:
        # statsmodels 不可用时回退到 numpy 线性回归，避免导入阻断。
        slope, intercept = np.polyfit(benchmark_ret.values, strategy_ret.values, 1)
        beta = float(slope)
        alpha = float(intercept) * 252

    roll_max = strategy_nav.cummax()
    max_dd = ((strategy_nav - roll_max) / roll_max).min()

    neg_ret = strategy_ret[strategy_ret < 0]
    sortino_down = np.sqrt(np.mean(neg_ret**2)) if len(neg_ret) > 0 else 0
    sortino_ratio = (
        strategy_ret.mean() / sortino_down * np.sqrt(252)
        if sortino_down != 0
        else np.nan
    )

    logger.info(f"策略总收益率: {total_return:.2%}")
    logger.info(f"策略年化收益率: {annual_return:.2%}")
    logger.info(f"夏普比率: {sharpe_ratio:.3f}")
    logger.info(f"信息比率: {info_ratio:.3f}")
    logger.info(f"阿尔法(年化): {alpha:.3%}")
    logger.info(f"贝塔: {beta:.3f}")
    logger.info(f"最大回撤: {max_dd:.2%}")
    logger.info(f"索提诺比率: {sortino_ratio:.3f}")


# =====================================================================
# 导出 query 函数
# =====================================================================


def query(*tables):
    """聚宽风格 query()，返回 _QueryBuilder。"""
    return _QueryBuilder(list(tables))


# =====================================================================
# 财务数据 API
# =====================================================================


# 聚宽财务字段 → AkShare 字段的映射表
_FIELD_MAP = {
    # 现金流
    "cash_equivalents": "货币资金",
    "net_deposit_increase": "客户存款和同业存放款项净增加额",
    # 利润表
    "total_operating_revenue": "营业总收入",
    "operating_revenue": "营业收入",
    "interest_income": "利息收入",
    "total_operating_cost": "营业总成本",
    "operating_cost": "营业成本",
    "operating_tax_surcharges": "营业税金及附加",
    "sale_expense": "销售费用",
    "administration_expense": "管理费用",
    "financial_expense": "财务费用",
    "asset_impairment_loss": "资产减值损失",
    "fair_value_variable_income": "公允价值变动收益",
    "investment_income": "投资收益",
    "operating_profit": "营业利润",
    "non_operating_revenue": "营业外收入",
    "non_operating_expense": "营业外支出",
    "total_profit": "利润总额",
    "income_tax_expense": "所得税费用",
    "net_profit": "净利润",
    "np_parent_company_owners": "归属于母公司股东的净利润",
    "minority_profit": "少数股东损益",
    "basic_eps": "基本每股收益",
    "diluted_eps": "稀释每股收益",
    # 资产负债
    "total_assets": "资产总计",
    "total_liability": "负债合计",
    "total_equity": "所有者权益合计",
    "accounts_receivable": "应收账款",
    "accounts_payable": "应付账款",
}

_VALUATION_FIELD_MAP = {
    "code": "code",
    "pe_ratio": "PE_ratio",
    "pe_ratio_dynamic": "PE_ratio_dynamic",
    "pb_ratio": "PB_ratio",
    "ps_ratio": "PS_ratio",
    "market_cap": "market_cap",
    "circulating_market_cap": "circulating_market_cap",
    "dividend_ratio": "dividend_ratio",
}

_FUNDAMENTALS_SCHEMA = {
    "valuation": [
        "code",
        "pe_ratio",
        "pb_ratio",
        "ps_ratio",
        "market_cap",
        "circulating_market_cap",
        "dividend_ratio",
    ],
    "income": ["code", "statDate", "营业收入", "营业成本", "净利润", "营业利润"],
    "balance": [
        "code",
        "statDate",
        "资产总计",
        "负债合计",
        "所有者权益合计",
        "应收账款",
        "应付账款",
    ],
    "cash_flow": ["code", "statDate", "货币资金", "净利润", "投资收益", "营业利润"],
}


def get_cashflow_sina(
    symbol, stat_date=None, cache_dir="stock_cache", force_update=False
):
    """获取现金流量表（新浪接口），支持缓存和 stat_date 筛选。"""
    cache_dir = _resolve_cache_dir(cache_dir)
    akshare_symbol = symbol.lower() if symbol.startswith(("sh", "sz")) else symbol
    cache_file = os.path.join(cache_dir, f"{akshare_symbol}_cashflow_sina.pkl")
    os.makedirs(cache_dir, exist_ok=True)
    need_download = force_update or (not os.path.exists(cache_file))
    if not need_download:
        try:
            df = pd.read_pickle(cache_file)
        except Exception:
            need_download = True
    if need_download:
        try:
            import akshare as ak
            df = ak.stock_financial_report_sina(stock=akshare_symbol, symbol="现金流量表")
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        if df.empty:
            raise ValueError(f"No cashflow data for {symbol}")
        df.to_pickle(cache_file)
    if stat_date:
        date_col = _find_date_column(df, "financial")
        if date_col is None:
            raise ValueError("找不到报告日期字段")
        df = df[df[date_col] == stat_date]
    return df.reset_index(drop=True)


def get_income_ths(
    symbol, indicator="按报告期", cache_dir="stock_cache", force_update=False
):
    """获取利润表（同花顺接口），支持缓存和 indicator 筛选。"""
    cache_dir = _resolve_cache_dir(cache_dir)
    akshare_symbol = symbol[2:] if symbol.startswith(("sh", "sz")) else symbol
    cache_file = os.path.join(cache_dir, f"{akshare_symbol}_income_ths_{indicator}.pkl")
    os.makedirs(cache_dir, exist_ok=True)
    need_download = force_update or (not os.path.exists(cache_file))
    if not need_download:
        try:
            df = pd.read_pickle(cache_file)
        except Exception:
            need_download = True
    if need_download:
        try:
            import akshare as ak
            df = ak.stock_financial_benefit_ths(symbol=akshare_symbol, indicator=indicator)
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        if df.empty:
            raise ValueError(f"No income data for {symbol}")
        df.to_pickle(cache_file)
    return df.reset_index(drop=True)


def get_balance_sina(
    symbol, stat_date=None, cache_dir="stock_cache", force_update=False
):
    """获取资产负债表（新浪接口），支持缓存和 stat_date 筛选。"""
    cache_dir = _resolve_cache_dir(cache_dir)
    akshare_symbol = symbol.lower() if symbol.startswith(("sh", "sz")) else symbol
    cache_file = os.path.join(cache_dir, f"{akshare_symbol}_balance_sina.pkl")
    os.makedirs(cache_dir, exist_ok=True)
    need_download = force_update or (not os.path.exists(cache_file))
    if not need_download:
        try:
            df = pd.read_pickle(cache_file)
        except Exception:
            need_download = True
    if need_download:
        try:
            import akshare as ak
            df = ak.stock_financial_report_sina(stock=akshare_symbol, symbol="资产负债表")
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        if df.empty:
            raise ValueError(f"No balance data for {symbol}")
        df.to_pickle(cache_file)
    if stat_date:
        date_col = _find_date_column(df, "financial")
        if date_col is None:
            raise ValueError("找不到报告日期字段")
        df = df[df[date_col] == stat_date]
    return df.reset_index(drop=True)


def get_fundamentals(
    query_obj,
    date=None,
    statDate=None,
    cache_dir="stock_cache",
    force_update=False,
    robust=False,
):
    """
    聚宽风格get_fundamentals

    支持:
    - valuation表: 市值、PE、PB、PS、股息率等
    - income表: 利润表
    - balance表: 资产负债表
    - cash_flow表: 现金流量表

    参数:
        query_obj: query对象或dict
        date: 估值查询日期
        statDate: 财报季度（如 '2020q1'）
        cache_dir: 缓存目录
        force_update: 强制更新缓存
        robust: bool - 是否返回 RobustResult 对象

    返回:
        DataFrame 或 RobustResult

    示例:
        df = get_fundamentals(
            query(valuation).filter(
                valuation.code.in_(stocks),
                valuation.pb_ratio > 0,
                valuation.pe_ratio > 0,
            )
        )

        # 稳健模式
        result = get_fundamentals(query(valuation).filter(...), robust=True)
        if result.success:
            df = result.data
        else:
            log.warn(f"查询失败: {result.reason}")
    """
    schema_cols = ["code"]
    result_reason = ""
    result_source = "network"

    try:
        symbols = None
        table_name = None
        filters = []
        limit_n = None

        if isinstance(query_obj, dict):
            table_name = query_obj.get("table", "balance")
            symbols = query_obj.get("symbol") or query_obj.get("symbols")
            if isinstance(symbols, str):
                symbols = [symbols]
            result_reason = f"dict格式查询: table={table_name}, symbols={len(symbols) if symbols else 0}"

        elif isinstance(query_obj, _QueryBuilder):
            symbols = query_obj._symbols
            table_name = (
                query_obj._tables[0]._name if query_obj._tables else "valuation"
            )
            if isinstance(table_name, _TableProxy):
                table_name = table_name._name
            filters = getattr(query_obj, "_filter_expressions", [])
            limit_n = getattr(query_obj, "_limit_n", None)
            result_reason = f"query格式查询: table={table_name}, symbols={len(symbols) if symbols else 0}"

        if symbols is None or len(symbols) == 0:
            schema_cols = (
                _FUNDAMENTALS_SCHEMA.get(table_name, ["code"])
                if table_name
                else ["code"]
            )
            empty_df = pd.DataFrame(columns=schema_cols)
            result_reason = "symbols为空，未提供股票代码列表"
            if robust:
                return RobustResult(
                    success=False,
                    data=empty_df,
                    reason=result_reason,
                    source="fallback",
                )
            warnings.warn(result_reason)
            return empty_df

        if table_name not in _FUNDAMENTALS_SCHEMA:
            result_reason = f"不支持的表类型: {table_name}"
            if robust:
                return RobustResult(
                    success=False,
                    data=pd.DataFrame(columns=["code"]),
                    reason=result_reason,
                    source="fallback",
                )
            warnings.warn(result_reason)
            return pd.DataFrame(columns=["code"])

        schema_cols = _FUNDAMENTALS_SCHEMA[table_name]

        if table_name == "valuation":
            df = _get_valuation_fundamentals(
                symbols, date, filters, cache_dir, force_update
            )
        elif table_name == "income":
            df = _get_income_fundamentals(symbols, statDate, cache_dir, force_update)
        elif table_name == "balance":
            df = _get_balance_fundamentals(symbols, statDate, cache_dir, force_update)
        elif table_name == "cash_flow":
            df = _get_cashflow_fundamentals(symbols, statDate, cache_dir, force_update)
        else:
            df = pd.DataFrame(columns=schema_cols)

        if limit_n and not df.empty:
            df = df.head(limit_n)

        if df.empty:
            result_reason = f"查询返回空数据 (表: {table_name}, 股票数: {len(symbols)})"
            empty_df = pd.DataFrame(columns=schema_cols)
            if robust:
                return RobustResult(
                    success=False, data=empty_df, reason=result_reason, source="network"
                )
            return empty_df

        for col in schema_cols:
            if col not in df.columns:
                df[col] = None

        result_reason = f"成功获取 {len(df)} 条记录 (表: {table_name})"
        if robust:
            return RobustResult(
                success=True, data=df, reason=result_reason, source=result_source
            )
        return df

    except Exception as e:
        result_reason = f"get_fundamentals异常: {e}"
        warnings.warn(result_reason)
        empty_df = pd.DataFrame(columns=schema_cols if schema_cols else ["code"])
        if robust:
            return RobustResult(
                success=False, data=empty_df, reason=result_reason, source="fallback"
            )
        return empty_df


def get_fundamentals_robust(
    query_obj, date=None, statDate=None, cache_dir="stock_cache", force_update=False
):
    """稳健版基本面查询，返回 RobustResult 对象"""
    return get_fundamentals(
        query_obj, date, statDate, cache_dir, force_update, robust=True
    )


def _get_valuation_fundamentals(
    symbols, date=None, filters=None, cache_dir="stock_cache", force_update=False
):
    """获取估值数据"""
    try:
        try:
            from ..factors.factor_zoo import get_factor_values_jq
        except ImportError:
            import sys
            import os as _os

            _util_dir = _os.path.dirname(os.path.abspath(__file__))
            if _util_dir not in sys.path:
                sys.path.insert(0, _util_dir)
            from factors.factor_zoo import get_factor_values_jq

        factor_names = [
            "PE_ratio",
            "PE_ratio_dynamic",
            "PB_ratio",
            "PS_ratio",
            "market_cap",
            "circulating_market_cap",
            "dividend_ratio",
        ]

        ak_symbols = [jq_code_to_ak(sym) if "." in sym else sym for sym in symbols]

        result_dict = get_factor_values_jq(
            securities=ak_symbols,
            factors=factor_names,
            end_date=date,
            count=1,
            cache_dir=cache_dir,
            force_update=force_update,
        )

        df = pd.DataFrame(index=symbols)
        df["code"] = symbols

        for factor_name in factor_names:
            if factor_name in result_dict and not result_dict[factor_name].empty:
                factor_df = result_dict[factor_name]
                latest_values = (
                    factor_df.iloc[-1] if len(factor_df) > 0 else pd.Series()
                )
                for i, sym in enumerate(symbols):
                    ak_sym = ak_symbols[i]
                    if ak_sym in latest_values.index:
                        col_name = _VALUATION_FIELD_MAP.get(factor_name, factor_name)
                        if col_name not in df.columns:
                            df[col_name] = None
                        df.loc[sym, col_name] = latest_values[ak_sym]

        df = df.reset_index(drop=True)

        if filters:
            for expr in filters:
                df = _apply_filter(df, expr)

        return df

    except Exception as e:
        warnings.warn(f"获取估值数据失败: {e}")
        return pd.DataFrame()


def _apply_filter(df, filter_expr):
    """应用过滤条件"""
    if not hasattr(filter_expr, "_field"):
        return df

    field = filter_expr._field
    op = filter_expr._operator
    value = filter_expr._value

    if field not in df.columns:
        return df

    if op == ">":
        return df[df[field] > value]
    elif op == ">=":
        return df[df[field] >= value]
    elif op == "<":
        return df[df[field] < value]
    elif op == "<=":
        return df[df[field] <= value]
    elif op == "==":
        return df[df[field] == value]

    return df


def _get_income_fundamentals(
    symbols, statDate=None, cache_dir="stock_cache", force_update=False
):
    """获取利润表数据"""
    dfs = []
    for symbol in symbols:
        try:
            ak_code = jq_code_to_ak(symbol)
            df = get_income_ths(ak_code, cache_dir=cache_dir, force_update=force_update)
            if df is not None and not df.empty:
                df["code"] = symbol
                dfs.append(df)
        except Exception as e:
            warnings.warn(f"_get_income_fundamentals: {symbol} 获取失败: {e}")
            continue

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def _get_balance_fundamentals(
    symbols, statDate=None, cache_dir="stock_cache", force_update=False
):
    """获取资产负债表数据"""
    dfs = []
    for symbol in symbols:
        try:
            ak_code = jq_code_to_ak(symbol)
            df = get_balance_sina(
                ak_code,
                stat_date=statDate,
                cache_dir=cache_dir,
                force_update=force_update,
            )
            if df is not None and not df.empty:
                df["code"] = symbol
                dfs.append(df)
        except Exception as e:
            warnings.warn(f"_get_balance_fundamentals: {symbol} 获取失败: {e}")
            continue

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def _get_cashflow_fundamentals(
    symbols, statDate=None, cache_dir="stock_cache", force_update=False
):
    """获取现金流量表数据"""
    dfs = []
    for symbol in symbols:
        try:
            ak_code = jq_code_to_ak(symbol)
            df = get_cashflow_sina(
                ak_code,
                stat_date=statDate,
                cache_dir=cache_dir,
                force_update=force_update,
            )
            if df is not None and not df.empty:
                df["code"] = symbol
                dfs.append(df)
        except Exception as e:
            warnings.warn(f"_get_cashflow_fundamentals: {symbol} 获取失败: {e}")
            continue

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def get_history_fundamentals(
    security=None,
    fields=None,
    watch_date=None,
    stat_date=None,
    count=1,
    interval="1q",
    stat_by_year=False,
    cache_dir="stock_cache",
    force_update=False,
    entity=None,
    robust=False,
):
    """
    聚宽风格批量财报获取接口，支持多股票多期。

    参数
    ----
    security : str or list
        股票代码，如 '600519.XSHG' 或 ['600519.XSHG', '000001.XSHE']
    fields : list
        字段列表，格式：["cash_flow.xxx", "income.xxx", "balance.xxx"]
    watch_date : str
        观察日期（暂未实现）
    stat_date : str
        报告期，如 '2020q1' 或 '2020-03-31'
    count : int
        获取期数
    interval : str
        间隔（暂未实现）
    stat_by_year : bool
        按年统计（暂未实现）
    cache_dir : str
        缓存目录
    force_update : bool
        强制更新缓存
    robust : bool
        是否返回 RobustResult 对象

    返回
    ----
    DataFrame 或 RobustResult
        index=['code','statDate']
    """

    def _parse_stat_date(sd):
        if sd is None:
            return None
        m = re.match(r"(\d{4})q([1-4])", sd, re.I)
        if m:
            y, q = m.group(1), m.group(2)
            qmap = {"1": "03-31", "2": "06-30", "3": "09-30", "4": "12-31"}
            return f"{y}-{qmap[q]}"
        return sd

    result_reason = ""
    result_source = "network"
    failed_stocks = []
    failed_details = {}

    if entity is not None:
        security = entity

    if security is None:
        result_reason = "security 参数为空，必须提供股票代码"
        empty_df = pd.DataFrame(columns=["code", "statDate"]).set_index(
            ["code", "statDate"]
        )
        if robust:
            return RobustResult(
                success=False,
                data=empty_df,
                reason=result_reason,
                source="fallback",
            )
        warnings.warn(result_reason)
        return empty_df

    if fields is None or len(fields) == 0:
        result_reason = "fields 参数为空，必须提供字段列表"
        empty_df = pd.DataFrame(columns=["code", "statDate"]).set_index(
            ["code", "statDate"]
        )
        if robust:
            return RobustResult(
                success=False,
                data=empty_df,
                reason=result_reason,
                source="fallback",
            )
        warnings.warn(result_reason)
        return empty_df

    if isinstance(security, str):
        security = [security]

    if len(security) == 0:
        result_reason = "security 列表为空"
        empty_df = pd.DataFrame(columns=["code", "statDate"]).set_index(
            ["code", "statDate"]
        )
        if robust:
            return RobustResult(
                success=False,
                data=empty_df,
                reason=result_reason,
                source="fallback",
            )
        warnings.warn(result_reason)
        return empty_df

    stat_date_fmt = _parse_stat_date(stat_date)

    cash_fields = [f.split(".", 1)[1] for f in fields if f.startswith("cash_flow.")]
    income_fields = [f.split(".", 1)[1] for f in fields if f.startswith("income.")]
    balance_fields = [f.split(".", 1)[1] for f in fields if f.startswith("balance.")]
    valid_field_count = len(cash_fields) + len(income_fields) + len(balance_fields)

    for f in fields:
        if not any(f.startswith(p) for p in ("cash_flow.", "income.", "balance.")):
            warnings.warn(f"字段 {f} 未指定表前缀（cash_flow/income/balance），已跳过")

    if valid_field_count == 0:
        result_reason = "无有效字段（所有字段都需要 cash_flow./income./balance. 前缀）"
        empty_df = pd.DataFrame(columns=["code", "statDate"]).set_index(
            ["code", "statDate"]
        )
        if robust:
            return RobustResult(
                success=False,
                data=empty_df,
                reason=result_reason,
                source="fallback",
            )
        warnings.warn(result_reason)
        return empty_df

    def _slice(df, date_col, sdate, cnt):
        if sdate:
            idx = df[df[date_col] == sdate].index
            start_i = idx[0] if not idx.empty else 0
        else:
            start_i = 0
        return df.iloc[start_i : start_i + cnt]

    dfs = []
    for code in security:
        ak_code = jq_code_to_ak(code)
        out = pd.DataFrame()
        stock_failed = False
        stock_errors = []

        try:
            if cash_fields:
                try:
                    df = get_cashflow_sina(
                        ak_code, cache_dir=cache_dir, force_update=force_update
                    )
                    if df.empty:
                        stock_failed = True
                        stock_errors.append("现金流量表返回空数据")
                        warnings.warn(f"{code}: 现金流量表返回空数据")
                    else:
                        date_col = _find_date_column(df, "financial")
                        if date_col is None:
                            stock_failed = True
                            stock_errors.append("现金流量表找不到报告日期字段")
                            warnings.warn(f"{code}: 现金流量表找不到报告日期字段")
                        else:
                            df = _slice(df, date_col, stat_date_fmt, count)
                            out["code"] = code
                            out["statDate"] = df[date_col].values
                            for f in cash_fields:
                                col = _FIELD_MAP.get(f, f)
                                out[f"cash_flow.{f}"] = (
                                    df[col].values if col in df.columns else None
                                )
                except ValueError as e:
                    stock_failed = True
                    stock_errors.append(f"现金流量表获取失败: {e}")
                    warnings.warn(f"{code}: 现金流量表获取失败 - {e}")
                except Exception as e:
                    stock_failed = True
                    stock_errors.append(f"现金流量表异常: {e}")
                    warnings.warn(f"{code}: 现金流量表异常 - {e}")

            if income_fields:
                try:
                    df = get_income_ths(
                        ak_code, cache_dir=cache_dir, force_update=force_update
                    )
                    if df.empty:
                        stock_failed = True
                        stock_errors.append("利润表返回空数据")
                        warnings.warn(f"{code}: 利润表返回空数据")
                    else:
                        date_col = _find_date_column(df, "financial")
                        if date_col is None:
                            stock_failed = True
                            stock_errors.append("利润表找不到报告日期字段")
                            warnings.warn(f"{code}: 利润表找不到报告日期字段")
                        else:
                            df = _slice(df, date_col, stat_date_fmt, count)
                            if out.empty:
                                out["code"] = code
                                out["statDate"] = df[date_col].values
                            for f in income_fields:
                                col = _FIELD_MAP.get(f, f)
                                out[f"income.{f}"] = (
                                    df[col].values if col in df.columns else None
                                )
                except ValueError as e:
                    stock_failed = True
                    stock_errors.append(f"利润表获取失败: {e}")
                    warnings.warn(f"{code}: 利润表获取失败 - {e}")
                except Exception as e:
                    stock_failed = True
                    stock_errors.append(f"利润表异常: {e}")
                    warnings.warn(f"{code}: 利润表异常 - {e}")

            if balance_fields:
                try:
                    df = get_balance_sina(
                        ak_code,
                        stat_date=statDate,
                        cache_dir=cache_dir,
                        force_update=force_update,
                    )
                    if df.empty:
                        stock_failed = True
                        stock_errors.append("资产负债表返回空数据")
                        warnings.warn(f"{code}: 资产负债表返回空数据")
                    else:
                        date_col = _find_date_column(df, "financial")
                        if date_col is None:
                            stock_failed = True
                            stock_errors.append("资产负债表找不到报告日期字段")
                            warnings.warn(f"{code}: 资产负债表找不到报告日期字段")
                        else:
                            df = _slice(df, date_col, stat_date_fmt, count)
                            if out.empty:
                                out["code"] = code
                                out["statDate"] = df[date_col].values
                            for f in balance_fields:
                                col = _FIELD_MAP.get(f, f)
                                out[f"balance.{f}"] = (
                                    df[col].values if col in df.columns else None
                                )
                except ValueError as e:
                    stock_failed = True
                    stock_errors.append(f"资产负债表获取失败: {e}")
                    warnings.warn(f"{code}: 资产负债表获取失败 - {e}")
                except Exception as e:
                    stock_failed = True
                    stock_errors.append(f"资产负债表异常: {e}")
                    warnings.warn(f"{code}: 资产负债表异常 - {e}")

        except Exception as e:
            stock_failed = True
            stock_errors.append(f"整体处理异常: {e}")
            warnings.warn(f"{code}: 整体处理异常 - {e}")

        if stock_failed:
            failed_stocks.append(code)
            failed_details[code] = stock_errors

        if not out.empty:
            dfs.append(out)

    if dfs:
        result = pd.concat(dfs, ignore_index=True)
        result.set_index(["code", "statDate"], inplace=True)
    else:
        result = pd.DataFrame(columns=["code", "statDate"]).set_index(
            ["code", "statDate"]
        )

    success_count = len(dfs)
    failed_count = len(failed_stocks)
    total_count = len(security)

    if failed_count > 0:
        failed_summary = ", ".join(failed_stocks[:5])
        if failed_count > 5:
            failed_summary += f" ... (共 {failed_count} 只)"
        result_reason = (
            f"成功 {success_count}/{total_count} 只股票，失败: {failed_summary}"
        )
    elif success_count == 0:
        result_reason = f"所有 {total_count} 只股票数据获取失败"
    else:
        result_reason = f"成功获取 {success_count}/{total_count} 只股票数据"

    if robust:
        rr = RobustResult(
            success=(success_count > 0),
            data=result,
            reason=result_reason,
            source=result_source,
        )
        rr.failed_stocks = failed_stocks
        rr.failed_details = failed_details
        rr.success_count = success_count
        rr.failed_count = failed_count
        rr.total_count = total_count
        return rr

    return result


def get_history_fundamentals_robust(
    security,
    fields,
    watch_date=None,
    stat_date=None,
    count=1,
    interval="1q",
    stat_by_year=False,
    cache_dir="stock_cache",
    force_update=False,
):
    """稳健版财报获取接口，返回 RobustResult 对象"""
    return get_history_fundamentals(
        security,
        fields,
        watch_date=watch_date,
        stat_date=stat_date,
        count=count,
        interval=interval,
        stat_by_year=stat_by_year,
        cache_dir=cache_dir,
        force_update=force_update,
        robust=True,
    )


# 别名
get_fundamentals_jq = get_fundamentals
get_history_fundamentals_jq = get_history_fundamentals


# =====================================================================
# 证券元数据 API
# =====================================================================


def get_all_securities_jq(
    types=None, date=None, cache_dir="meta_cache", force_update=False, use_duckdb=True
):
    """JQData 风格 get_all_securities，返回全市场 A 股元数据 DataFrame。

    Args:
        types: 证券类型列表，默认 ["stock"]
        date: 指定日期（暂未使用）
        cache_dir: pickle 缓存目录（作为 fallback）
        force_update: 是否强制更新
        use_duckdb: 是否优先使用 DuckDB 缓存
    """
    if use_duckdb:
        try:
            from ..db.meta_cache_api import get_securities_from_cache

            df = get_securities_from_cache(
                types=types, force_update=force_update, use_duckdb=True
            )
            if not df.empty:
                return df
        except Exception as e:
            logger.warning(f"DuckDB 缓存获取失败，fallback 到 pickle: {e}")

    cache_dir = _resolve_cache_dir(cache_dir)
    if types is None:
        types = ["stock"]
    os.makedirs(cache_dir, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    cache_file = os.path.join(cache_dir, f"securities_{today}.pkl")
    need_dl = force_update or not os.path.exists(cache_file)
    if not need_dl:
        try:
            df = pd.read_pickle(cache_file)
        except Exception:
            need_dl = True
    if need_dl:
        try:
            import akshare as ak
            df = ak.stock_info_a_code_name()
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        df["code"] = df["code"].apply(
            lambda x: (
                "sz" + x
                if x.startswith(("0", "3"))
                else ("sh" + x if x.startswith("6") else x)
            )
        )
        df["jq_code"] = df["code"].apply(
            lambda x: (
                x[2:]
                + (
                    ".XSHE"
                    if x.startswith("sz")
                    else ".XSHG"
                    if x.startswith("sh")
                    else ""
                )
            )
        )
        df.to_pickle(cache_file)
    # 设置 index 为 jq_code（聚宽 API 风格）
    if "jq_code" in df.columns and df.index.dtype != object:
        df = df.set_index("jq_code")
    # 预运行模式下记录请求的股票
    if _prerun_mode_active and not df.empty:
        if "jq_code" in df.columns:
            sample_stocks = df["jq_code"].head(100).tolist()
        else:
            sample_stocks = df.index[:100].tolist()
        _prerun_requested_stocks.update(sample_stocks)
    return df


# 兼容不带 _jq 后缀的聚宽原始调用
get_all_securities = get_all_securities_jq


def get_security_info_jq(
    code, cache_dir="meta_cache", force_update=False, use_duckdb=True
):
    """JQData 风格 get_security_info，返回单只股票元数据对象。

    支持缓存和离线兜底。网络失败时返回默认结构。

    Args:
        code: 证券代码
        cache_dir: pickle 缓存目录（作为 fallback）
        force_update: 是否强制更新
        use_duckdb: 是否优先使用 DuckDB 缓存

    Returns:
        SecurityInfo: 兼容聚宽的对象风格访问（.code, .display_name, .start_date 等）
    """
    if use_duckdb:
        try:
            from ..db.meta_cache_api import get_security_info_from_cache

            info = get_security_info_from_cache(
                code, force_update=force_update, use_duckdb=True
            )
            if info:
                return SecurityInfo(info)
        except Exception as e:
            logger.warning(f"DuckDB 缓存获取失败，fallback 到 pickle: {e}")

    cache_dir = _resolve_cache_dir(cache_dir)
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"security_info_{code}.pkl")

    if not force_update and os.path.exists(cache_file):
        try:
            cached = pd.read_pickle(cache_file)
            return SecurityInfo(cached)
        except Exception:
            pass

    try:
        df = get_all_securities_jq(cache_dir=cache_dir, force_update=force_update)
        code_num = format_stock_symbol_for_akshare(code)
        code_with_prefix = ("sh" if code_num.startswith("6") else "sz") + code_num
        row = df[df["code"] == code_with_prefix]
        if row.empty:
            row = df[df["code"] == code_num]
        if row.empty:
            result = {
                "code": code_with_prefix,
                "display_name": code_num,
                "name": code_num,
                "start_date": None,
                "end_date": None,
                "type": "stock",
            }
        else:
            result = row.iloc[0].to_dict()
        pd.to_pickle(result, cache_file)
        return SecurityInfo(result)
    except Exception as e:
        warnings.warn(f"获取股票信息失败: {e}，返回默认结构")
        code_num = format_stock_symbol_for_akshare(code)
        code_with_prefix = ("sh" if code_num.startswith("6") else "sz") + code_num
        return SecurityInfo({
            "code": code_with_prefix,
            "display_name": code_num,
            "name": code_num,
            "start_date": None,
            "end_date": None,
            "type": "stock",
        })


get_security_info = get_security_info_jq


def get_all_trade_days_jq(cache_dir="meta_cache", force_update=False, use_duckdb=True):
    """JQData 风格 get_all_trade_days，返回所有交易日 Timestamp 列表。支持缓存。

    Args:
        cache_dir: pickle 缓存目录（作为 fallback）
        force_update: 是否强制更新
        use_duckdb: 是否优先使用 DuckDB 缓存
    """
    def _fallback_trade_days():
        # 离线/网络受限场景的兜底：使用工作日近似交易日，保证 API 稳定可用。
        return pd.bdate_range(start="2000-01-01", end=pd.Timestamp.today()).tolist()

    if use_duckdb:
        try:
            from ..db.meta_cache_api import get_trade_days_from_cache

            days = get_trade_days_from_cache(force_update=force_update, use_duckdb=True)
            if days is not None and len(days) > 0:
                return list(pd.to_datetime(days))
        except Exception as e:
            logger.warning(f"DuckDB 缓存获取失败，fallback 到 pickle: {e}")

    cache_dir = _resolve_cache_dir(cache_dir)
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "trade_days.pkl")

    need_dl = force_update or not os.path.exists(cache_file)
    if not need_dl:
        try:
            cached = pd.read_pickle(cache_file)
            if isinstance(cached, pd.DataFrame):
                date_col = _find_date_column(cached, category="market") or "trade_date"
                if date_col in cached.columns:
                    days = pd.to_datetime(cached[date_col]).tolist()
                else:
                    days = pd.to_datetime(cached.index).tolist()
            else:
                days = pd.to_datetime(cached).tolist()

            if days:
                return list(days)
        except Exception:
            need_dl = True

    try:
        import akshare as ak
        raw = ak.tool_trade_date_hist_sina()
        if isinstance(raw, pd.DataFrame):
            date_col = _find_date_column(raw, category="market") or "trade_date"
            if date_col in raw.columns:
                days = pd.to_datetime(raw[date_col]).tolist()
            else:
                days = pd.to_datetime(raw.index).tolist()
            raw.to_pickle(cache_file)
        else:
            days = pd.to_datetime(raw).tolist()
            pd.Series(days, name="trade_date").to_pickle(cache_file)

        if days:
            return list(days)
    except ImportError:
        warnings.warn("未安装 akshare，使用本地工作日作为交易日历近似值。")
    except Exception as e:
        warnings.warn(f"获取线上交易日历失败，使用本地工作日近似值: {e}")

    return _fallback_trade_days()


get_all_trade_days = get_all_trade_days_jq


# =====================================================================
# 额外 API 函数
# =====================================================================


def get_factor_values_jq(
    securities,
    factors,
    end_date=None,
    count=1,
    cache_dir="factors_cache",
    force_update=False,
):
    """
    JQData 风格 get_factor_values。

    已实现本地因子计算，支持估值、技术、财务、成长类因子。
    """
    cache_dir = _resolve_cache_dir(cache_dir)
    try:
        try:
            from ..factors.factor_zoo import (
                get_factor_values_jq as _get_factor_values_jq,
            )
        except ImportError:
            import sys
            import os as _os

            _util_dir = _os.path.dirname(os.path.abspath(__file__))
            if _util_dir not in sys.path:
                sys.path.insert(0, _util_dir)
            from factors.factor_zoo import get_factor_values_jq as _get_factor_values_jq

        return _get_factor_values_jq(
            securities=securities,
            factors=factors,
            end_date=end_date,
            count=count,
            cache_dir=cache_dir,
            force_update=force_update,
        )
    except ImportError as e:
        raise NotImplementedError(
            f"因子模块导入失败: {e}。请确保 factors/ 目录存在且依赖完整。"
        )


get_factor_values = get_factor_values_jq


def get_extras_jq(
    field,
    securities,
    start_date=None,
    end_date=None,
    count=None,
    df=True,
    cache_dir="extras_cache",
    force_update=False,
):
    """JQData 风格 get_extras，支持 is_st / is_paused。"""
    cache_dir = _resolve_cache_dir(cache_dir)
    os.makedirs(cache_dir, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    if isinstance(securities, str):
        securities = [securities]

    # 标准化股票代码格式
    securities_str = []
    code_nums = []
    for s in securities:
        s_str = str(s)
        securities_str.append(s_str)
        if s_str.startswith("sh") or s_str.startswith("sz"):
            code_nums.append(s_str[2:])
        elif "." in s_str:
            code_nums.append(s_str.split(".")[0])
        else:
            code_nums.append(s_str)

    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if isinstance(end_date, datetime):
        end_date = end_date.strftime("%Y-%m-%d")

    result_data = {}
    for sec, code in zip(securities_str, code_nums):
        result_data[sec] = False

    if field == "is_st":
        cache_file = os.path.join(cache_dir, f"is_st_{today}.pkl")
        need_dl = force_update or not os.path.exists(cache_file)
        st_df = None
        if not need_dl:
            try:
                st_df = pd.read_pickle(cache_file)
            except Exception:
                need_dl = True
        if need_dl:
            try:
                import akshare as ak
                st_df = ak.stock_zh_a_st_em()
                st_df.to_pickle(cache_file)
            except Exception as e:
                warnings.warn(f"获取 ST 数据失败: {e}")
                st_df = None

        if st_df is not None and "代码" in st_df.columns:
            st_codes = set(st_df["代码"].tolist())
            for sec, code in zip(securities_str, code_nums):
                if code in st_codes:
                    result_data[sec] = True

        result_df = pd.DataFrame(result_data, index=[pd.Timestamp(end_date)])
        return result_df

    elif field == "is_paused":
        cache_file = os.path.join(cache_dir, f"is_paused_{today}.pkl")
        need_dl = force_update or not os.path.exists(cache_file)
        stop_df = None
        if not need_dl:
            try:
                stop_df = pd.read_pickle(cache_file)
            except Exception:
                need_dl = True
        if need_dl:
            try:
                import akshare as ak
                stop_df = ak.stock_zh_a_stop_em()
                stop_df.to_pickle(cache_file)
            except Exception as e:
                warnings.warn(f"获取停牌数据失败: {e}")
                stop_df = None

        if stop_df is not None and "代码" in stop_df.columns:
            paused_codes = set(stop_df["代码"].tolist())
            for sec, code in zip(securities_str, code_nums):
                if code in paused_codes:
                    result_data[sec] = True

        result_df = pd.DataFrame(result_data, index=[pd.Timestamp(end_date)])
        return result_df

    else:
        raise NotImplementedError(f"暂不支持的 extras 字段: {field}")


get_extras = get_extras_jq


def get_billboard_list_jq(
    stock_list=None,
    end_date=None,
    count=30,
    cache_dir="billboard_cache",
    force_update=False,
):
    """JQData 风格 get_billboard_list，龙虎榜数据。"""
    cache_dir = _resolve_cache_dir(cache_dir)
    os.makedirs(cache_dir, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    cache_file = os.path.join(cache_dir, f"billboard_{today}.pkl")
    need_dl = force_update or not os.path.exists(cache_file)
    if not need_dl:
        try:
            df = pd.read_pickle(cache_file)
        except Exception:
            need_dl = True
    if need_dl:
        try:
            import akshare as ak
            df = ak.stock_lhb_detail_em()
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        df.to_pickle(cache_file)

    if df is None or df.empty:
        return pd.DataFrame(columns=["code", "date", "net_value"])

    df = df.copy()

    jq_columns_map = {
        "代码": "code",
        "上榜日": "date",
        "名称": "name",
        "收盘价": "close_price",
        "涨跌幅": "change_pct",
        "龙虎榜净买额": "net_value",
        "龙虎榜买入额": "buy_value",
        "龙虎榜卖出额": "sell_value",
        "龙虎榜成交额": "total_value",
    }

    for ak_col, jq_col in jq_columns_map.items():
        if ak_col in df.columns:
            df[jq_col] = df[ak_col]

    if stock_list:
        if isinstance(stock_list, str):
            stock_list = [stock_list]
        codes = []
        for s in stock_list:
            if s.startswith(("sh", "sz", "SH", "SZ")):
                codes.append(s[2:])
            elif "." in s:
                codes.append(s.split(".", 1)[0])
            else:
                codes.append(s)
        df = df[df["code"].isin(codes)]

    if end_date:
        if "date" in df.columns:
            df = df[df["date"].astype(str) <= str(end_date)]

    if count and len(df) > count:
        df = df.tail(count)

    return df


get_billboard_list = get_billboard_list_jq


def winsorize_med(factor_data, scale=3, inclusive=True, inf2nan=True, axis=0):
    """聚宽风格的去极值函数（MAD法）。

    优先使用官方 jqfactor_analyzer 版本，如果未安装则使用本地实现。

    注意：官方版本 scale 默认值为 1，本地版本默认值为 3，调用时请显式指定。
    """
    # 优先尝试使用官方SDK
    try:
        from jqfactor_analyzer import winsorize_med as _jq_winsorize_med
        # 官方版本 axis 参数默认为 1，需要适配
        return _jq_winsorize_med(
            factor_data, scale=scale, inclusive=inclusive, inf2nan=inf2nan, axis=axis
        )
    except ImportError:
        pass

    # Fallback 到本地实现
    try:
        try:
            from ..factors.preprocess import winsorize_med as _winsorize_med
        except ImportError:
            import sys
            import os as _os

            _util_dir = _os.path.dirname(os.path.abspath(__file__))
            if _util_dir not in sys.path:
                sys.path.insert(0, _util_dir)
            from factors.preprocess import winsorize_med as _winsorize_med

        return _winsorize_med(
            factor_data, scale=scale, inclusive=inclusive, inf2nan=inf2nan, axis=axis
        )
    except ImportError:
        raise NotImplementedError("winsorize_med 需要安装 jqfactor_analyzer 或 factors.preprocess 模块")


def winsorize(factor_data, qrange=[0.05, 0.95], inclusive=True, inf2nan=True, axis=0):
    """聚宽风格的去极值函数（分位数法）。

    优先使用官方 jqfactor_analyzer 版本，如果未安装则使用本地实现。
    """
    # 优先尝试使用官方SDK
    try:
        from jqfactor_analyzer import winsorize as _jq_winsorize
        return _jq_winsorize(
            factor_data, qrange=qrange, inclusive=inclusive, inf2nan=inf2nan, axis=axis
        )
    except ImportError:
        pass

    # Fallback 到本地实现
    import numpy as np

    if inf2nan:
        factor_data = np.where(np.isinf(factor_data), np.nan, factor_data)

    if hasattr(factor_data, 'values'):
        data = factor_data.values.copy()
    else:
        data = np.array(factor_data, dtype=float)

    if data.ndim == 1:
        data = data.reshape(-1)
        valid_data = data[~np.isnan(data)]
        if len(valid_data) > 0:
            lower_q = np.quantile(valid_data, qrange[0])
            upper_q = np.quantile(valid_data, qrange[1])
            data = np.clip(data, lower_q, upper_q)
        return data

    return data


def standardlize(factor_data, inf2nan=True, axis=0):
    """聚宽风格的标准化函数（Z-Score）。

    优先使用官方 jqfactor_analyzer 版本，如果未安装则使用本地实现。
    """
    # 优先尝试使用官方SDK
    try:
        from jqfactor_analyzer import standardlize as _jq_standardlize
        return _jq_standardlize(factor_data, inf2nan=inf2nan, axis=axis)
    except ImportError:
        pass

    # Fallback 到本地实现
    try:
        try:
            from ..factors.preprocess import standardlize as _standardlize
        except ImportError:
            import sys
            import os as _os

            _util_dir = _os.path.dirname(os.path.abspath(__file__))
            if _util_dir not in sys.path:
                sys.path.insert(0, _util_dir)
            from factors.preprocess import standardlize as _standardlize

        return _standardlize(factor_data, inf2nan=inf2nan, axis=axis)
    except ImportError:
        raise NotImplementedError("standardlize 需要安装 jqfactor_analyzer 或 factors.preprocess 模块")


# 别名
get_trade_days = get_all_trade_days_jq


# =====================================================================
# 导出列表
# =====================================================================

__all__ = [
    # 指数相关
    'get_index_weights',
    'get_index_weights_robust',
    'get_index_stocks',
    'get_index_stocks_robust',
    # 行情数据
    'get_akshare_etf_data',
    'get_akshare_stock_data',
    'get_index_nav',
    'get_price_unified',
    'get_price_jq',
    'get_price',
    'history',
    'attribute_history',
    'get_bars_jq',
    'get_bars',
    # 财务数据
    'get_cashflow_sina',
    'get_income_ths',
    'get_balance_sina',
    'get_fundamentals',
    'get_fundamentals_robust',
    'get_fundamentals_jq',
    'get_history_fundamentals',
    'get_history_fundamentals_robust',
    'get_history_fundamentals_jq',
    # 证券元数据
    'get_all_securities',
    'get_all_securities_jq',
    'get_security_info',
    'get_security_info_jq',
    'get_all_trade_days',
    'get_all_trade_days_jq',
    'get_trade_days',
    # 额外数据
    'get_extras_jq',
    'get_extras',
    'get_billboard_list_jq',
    'get_billboard_list',
    'get_factor_values_jq',
    'get_factor_values',
    # 因子处理
    'winsorize',
    'winsorize_med',
    'standardlize',
    # 当前数据
    'get_current_data',
    'get_current_tick',
    # 绩效分析
    'analyze_performance',
    # Query
    'query',
]
