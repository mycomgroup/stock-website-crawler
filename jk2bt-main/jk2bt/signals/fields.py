"""
indicator表字段补充模块
提供完整的财务指标字段映射和实现

聚宽indicator表字段包括:
- roe, roa等盈利能力指标
- gross_profit_margin等利润率指标
- inc_net_profit_year_on_year等增长指标
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings

INDICATOR_FIELD_MAPPING = {
    "roe": {
        "akshare_field": "roe",
        "description": "净资产收益率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "roa": {
        "akshare_field": "roa",
        "description": "总资产收益率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "gross_profit_margin": {
        "akshare_field": "grossprofitmargin",
        "description": "毛利率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "net_profit_margin": {
        "akshare_field": "netprofitmargin",
        "description": "净利率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "operating_margin": {
        "akshare_field": "operatingmargin",
        "description": "营业利润率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "ebit_margin": {
        "akshare_field": "ebitmargin",
        "description": "EBIT利润率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "total_asset_turnover": {
        "akshare_field": "totalassetturnover",
        "description": "总资产周转率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "inc_net_profit_year_on_year": {
        "akshare_field": "incnetprofityearonyear",
        "description": "净利润同比增长率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "inc_net_profit_annual": {
        "akshare_field": "incnetprofitannual",
        "description": "净利润年增长率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "inc_net_profit_to_shareholders_annual": {
        "akshare_field": "incnetprofittoshareholdersannual",
        "description": "归母净利润年增长率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "inc_revenue_year_on_year": {
        "akshare_field": "increvenueyearonyear",
        "description": "营收同比增长率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "inc_revenue_annual": {
        "akshare_field": "increvenueannual",
        "description": "营收年增长率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "current_ratio": {
        "akshare_field": "currentratio",
        "description": "流动比率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "quick_ratio": {
        "akshare_field": "quickratio",
        "description": "速动比率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "debt_asset_ratio": {
        "akshare_field": "debtassetratio",
        "description": "资产负债率",
        "data_source": "stock_financial_analysis_indicator",
    },
    "eps": {
        "akshare_field": "eps",
        "description": "每股收益",
        "data_source": "stock_financial_analysis_indicator",
    },
    "adjusted_profit": {
        "akshare_field": "adjustedprofit",
        "description": "调整后净利润",
        "data_source": "stock_financial_analysis_indicator",
    },
    "operating_profit": {
        "akshare_field": "operatingprofit",
        "description": "营业利润",
        "data_source": "stock_financial_analysis_indicator",
    },
    "operating_cash_flow_per_share": {
        "akshare_field": "operatingcashflowpershare",
        "description": "每股经营现金流",
        "data_source": "stock_financial_analysis_indicator",
    },
    "book_value_per_share": {
        "akshare_field": "bps",
        "description": "每股净资产",
        "data_source": "stock_financial_analysis_indicator",
    },
    "dividend_per_share": {
        "akshare_field": "dividendpershare",
        "description": "每股股利",
        "data_source": "stock_financial_analysis_indicator",
    },
}


def get_indicator_data(
    symbol, date=None, fields=None, cache_dir="indicator_cache", force_update=False
):
    """
    获取财务指标数据

    参数:
        symbol: 股票代码，如 'sh600519' 或 '600519.XSHG'
        date: 查询日期（可选）
        fields: 需要的字段列表（可选）
        cache_dir: 缓存目录
        force_update: 是否强制更新

    返回:
        DataFrame，包含指标数据

    示例:
        df = get_indicator_data('sh600519', fields=['roe', 'roa', 'inc_net_profit_year_on_year'])
    """
    import os
    from jk2bt.core.strategy_base import (
        format_stock_symbol_for_akshare,
        _resolve_cache_dir,
    )

    cache_dir = _resolve_cache_dir(cache_dir)
    os.makedirs(cache_dir, exist_ok=True)

    code_num = format_stock_symbol_for_akshare(symbol)
    cache_file = os.path.join(cache_dir, f"{code_num}_indicator.pkl")

    need_download = force_update or not os.path.exists(cache_file)

    if not need_download:
        try:
            df = pd.read_pickle(cache_file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - file_mtime).days > 7:
                need_download = True
        except Exception:
            need_download = True

    if need_download:
        try:
            import akshare as ak
        except ImportError:
            warnings.warn("akshare 未安装，无法获取 indicator 数据")
            return pd.DataFrame()

        try:
            df = ak.stock_financial_analysis_indicator(symbol=code_num)
            if df is not None and not df.empty:
                df.to_pickle(cache_file)
        except Exception as e:
            warnings.warn(f"获取indicator数据失败: {symbol}, {e}")
            return pd.DataFrame()

    if df is None or df.empty:
        return pd.DataFrame()

    if date:
        date_col = _find_date_column(df)
        if date_col:
            df = df[pd.to_datetime(df[date_col]) <= pd.to_datetime(date)].tail(1)

    result = pd.DataFrame()
    result["code"] = symbol

    if fields is None:
        fields = list(INDICATOR_FIELD_MAPPING.keys())

    for field in fields:
        if field in INDICATOR_FIELD_MAPPING:
            ak_field = INDICATOR_FIELD_MAPPING[field]["akshare_field"]
            if ak_field in df.columns:
                result[field] = df[ak_field].values

    return result


def _find_date_column(df):
    """查找日期列"""
    candidates = ["日期", "date", "报告期", "statDate"]
    for col in candidates:
        if col in df.columns:
            return col
    return None


def get_indicator_field_description(field_name):
    """
    获取指标字段的描述

    参数:
        field_name: 字段名

    返回:
        字段描述
    """
    if field_name in INDICATOR_FIELD_MAPPING:
        return INDICATOR_FIELD_MAPPING[field_name]["description"]
    return None


def get_supported_indicator_fields():
    """
    获取支持的indicator字段列表

    返回:
        list: 支持的字段名
    """
    return list(INDICATOR_FIELD_MAPPING.keys())


def get_indicator_batch(symbols, date=None, fields=None, cache_dir="indicator_cache"):
    """
    批量获取多个股票的财务指标

    参数:
        symbols: 股票代码列表
        date: 查询日期
        fields: 需要的字段列表
        cache_dir: 缓存目录

    返回:
        DataFrame，index为股票代码

    示例:
        df = get_indicator_batch(['sh600519', 'sz000001'], fields=['roe', 'roa'])
    """
    dfs = []
    for symbol in symbols:
        try:
            df = get_indicator_data(
                symbol, date=date, fields=fields, cache_dir=cache_dir
            )
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            warnings.warn(f"{symbol} indicator数据获取失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame()

    result = pd.concat(dfs, ignore_index=True)
    if "code" in result.columns:
        result = result.set_index("code")

    return result


def calculate_custom_indicator(df, formula):
    """
    计算自定义财务指标

    参数:
        df: 包含基础指标的DataFrame
        formula: 计算公式，如 'roe * gross_profit_margin'

    返回:
        Series: 计算结果

    示例:
        df = get_indicator_batch(['sh600519'], fields=['roe', 'gross_profit_margin'])
        custom = calculate_custom_indicator(df, 'roe * gross_profit_margin')
    """
    try:
        result = df.eval(formula)
        return result
    except Exception as e:
        warnings.warn(f"自定义指标计算失败: {e}")
        return pd.Series()


def get_indicator_ranking(symbols, field, date=None, ascending=False, top_n=10):
    """
    按指标排序获取排名靠前的股票

    参数:
        symbols: 股票代码列表
        field: 排序指标，如 'roe'
        date: 查询日期
        ascending: 是否升序
        top_n: 返回数量

    返回:
        DataFrame: 排名前top_n的股票

    示例:
        stocks = get_index_stocks('000300.XSHG')
        top_roe = get_indicator_ranking(stocks, 'roe', top_n=10)
    """
    df = get_indicator_batch(symbols, date=date, fields=[field])

    if df.empty or field not in df.columns:
        return pd.DataFrame()

    df = df.sort_values(field, ascending=ascending)
    return df.head(top_n)


def get_indicator_distribution(symbols, field, date=None):
    """
    获取指标分布统计

    参数:
        symbols: 股票代码列表
        field: 指标字段
        date: 查询日期

    返回:
        dict: 分布统计信息

    示例:
        stocks = get_index_stocks('000300.XSHG')
        dist = get_indicator_distribution(stocks, 'roe')
    """
    df = get_indicator_batch(symbols, date=date, fields=[field])

    if df.empty or field not in df.columns:
        return {}

    values = df[field].dropna()

    return {
        "mean": values.mean(),
        "median": values.median(),
        "std": values.std(),
        "min": values.min(),
        "max": values.max(),
        "q25": values.quantile(0.25),
        "q75": values.quantile(0.75),
        "count": len(values),
    }


def filter_by_indicator(symbols, field, min_value=None, max_value=None, date=None):
    """
    按指标范围筛选股票

    参数:
        symbols: 股票代码列表
        field: 筛选指标
        min_value: 最小值（可选）
        max_value: 最大值（可选）
        date: 查询日期

    返回:
        list: 筛选后的股票列表

    示例:
        stocks = get_index_stocks('000300.XSHG')
        high_roe = filter_by_indicator(stocks, 'roe', min_value=0.15)
    """
    df = get_indicator_batch(symbols, date=date, fields=[field])

    if df.empty or field not in df.columns:
        return symbols

    if min_value is not None:
        df = df[df[field] >= min_value]

    if max_value is not None:
        df = df[df[field] <= max_value]

    return list(df.index)


def get_indicator_change(symbol, field, periods=4):
    """
    获取指标的历史变化

    参数:
        symbol: 股票代码
        field: 指标字段
        periods: 历史期数

    返回:
        Series: 指标历史变化

    示例:
        roe_history = get_indicator_change('sh600519', 'roe', periods=8)
    """
    df = get_indicator_data(symbol, fields=[field])

    if df.empty or field not in df.columns:
        return pd.Series()

    return df[field].tail(periods)


def compare_indicator_stocks(symbols, field, date=None):
    """
    对比多个股票的指标

    参数:
        symbols: 股票代码列表
        field: 对比指标
        date: 查询日期

    返回:
        DataFrame: 对比结果

    示例:
        symbols = ['sh600519', 'sz000858', 'sz000333']
        comparison = compare_indicator_stocks(symbols, 'roe')
    """
    df = get_indicator_batch(symbols, date=date, fields=[field])

    if df.empty:
        return pd.DataFrame()

    return df[[field]].sort_values(field, ascending=False)


def get_financial_score(symbols, weights=None, date=None):
    """
    计算财务综合评分

    参数:
        symbols: 股票代码列表
        weights: dict {指标字段: 权重}
        date: 查询日期

    返回:
        DataFrame: 综合评分

    示例:
        weights = {
            'roe': 0.3,
            'gross_profit_margin': 0.2,
            'inc_revenue_year_on_year': 0.3,
            'current_ratio': 0.2
        }
        scores = get_financial_score(['sh600519', 'sz000001'], weights)
    """
    if weights is None:
        weights = {
            "roe": 0.4,
            "inc_net_profit_year_on_year": 0.3,
            "gross_profit_margin": 0.3,
        }

    fields = list(weights.keys())
    df = get_indicator_batch(symbols, date=date, fields=fields)

    if df.empty:
        return pd.DataFrame()

    scores = pd.Series(0.0, index=df.index)

    for field, weight in weights.items():
        if field in df.columns:
            normalized = (df[field] - df[field].min()) / (
                df[field].max() - df[field].min()
            )
            scores += normalized.fillna(0) * weight

    result = pd.DataFrame({"score": scores})
    result = result.sort_values("score", ascending=False)

    return result
