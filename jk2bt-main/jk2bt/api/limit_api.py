"""
涨停跌停相关API模块

提供：
- get_recent_limit_up_stock: 近期涨停股票筛选
- get_hl_stock: 高低点股票筛选
- get_continue_count_df: 连板统计
- get_recent_limit_down_stock: 近期跌停股票筛选
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings


def get_recent_limit_up_stock(context, stock_list, recent_days=5, date=None):
    """
    获取近期涨停的股票

    参数:
        context: 策略上下文（可传None）
        stock_list: 股票代码列表
        recent_days: 近几天内涨停，默认5天
        date: 基准日期（可选）

    返回:
        list: 近期涨停的股票代码列表
    """
    if not stock_list:
        return []

    try:
        from jk2bt.core.strategy_base import get_price_jq, format_stock_symbol_for_akshare

        if date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            end_date = date

        # 计算起始日期（多取几天以确保有足够交易日）
        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=recent_days + 10)).strftime('%Y-%m-%d')

        limit_up_stocks = []

        for stock in stock_list:
            try:
                # 获取历史数据
                df = get_price_jq(
                    symbols=stock,
                    start_date=start_date,
                    end_date=end_date,
                    frequency='daily',
                    fields=['close', 'high_limit']
                )

                if df is None or df.empty:
                    continue

                # 检查近期是否有涨停
                recent_df = df.tail(recent_days + 2)  # 多取几天确保覆盖

                for idx, row in recent_df.iterrows():
                    close = row.get('close')
                    high_limit = row.get('high_limit')

                    if close is not None and high_limit is not None:
                        # 涨停判断：收盘价等于涨停价（允许0.1%误差）
                        if abs(close - high_limit) / high_limit < 0.001:
                            if stock not in limit_up_stocks:
                                limit_up_stocks.append(stock)
                            break

            except Exception as e:
                continue

        return limit_up_stocks

    except Exception as e:
        warnings.warn(f"get_recent_limit_up_stock 失败: {e}")
        return []


def get_recent_limit_down_stock(context, stock_list, recent_days=5, date=None):
    """
    获取近期跌停的股票

    参数:
        context: 策略上下文（可传None）
        stock_list: 股票代码列表
        recent_days: 近几天内跌停，默认5天
        date: 基准日期（可选）

    返回:
        list: 近期跌停的股票代码列表
    """
    if not stock_list:
        return []

    try:
        from jk2bt.core.strategy_base import get_price_jq

        if date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            end_date = date

        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=recent_days + 10)).strftime('%Y-%m-%d')

        limit_down_stocks = []

        for stock in stock_list:
            try:
                df = get_price_jq(
                    symbols=stock,
                    start_date=start_date,
                    end_date=end_date,
                    frequency='daily',
                    fields=['close', 'low_limit']
                )

                if df is None or df.empty:
                    continue

                recent_df = df.tail(recent_days + 2)

                for idx, row in recent_df.iterrows():
                    close = row.get('close')
                    low_limit = row.get('low_limit')

                    if close is not None and low_limit is not None:
                        # 跌停判断
                        if abs(close - low_limit) / low_limit < 0.001:
                            if stock not in limit_down_stocks:
                                limit_down_stocks.append(stock)
                            break

            except Exception:
                continue

        return limit_down_stocks

    except Exception as e:
        warnings.warn(f"get_recent_limit_down_stock 失败: {e}")
        return []


def get_hl_stock(stock_list, n_days=20, high_pct=0.8, low_pct=0.2, date=None):
    """
    获取高低点股票

    判断股票当前价格是否处于近N天的高点或低点附近

    参数:
        stock_list: 股票代码列表
        n_days: 回看天数，默认20天
        high_pct: 高点阈值，默认0.8（即价格在80%分位以上视为高点）
        low_pct: 低点阈值，默认0.2（即价格在20%分位以下视为低点）
        date: 基准日期（可选）

    返回:
        dict: {'high': [...], 'low': [...], 'normal': [...]}
    """
    if not stock_list:
        return {'high': [], 'low': [], 'normal': []}

    try:
        from jk2bt.core.strategy_base import get_price_jq

        if date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            end_date = date

        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=n_days + 20)).strftime('%Y-%m-%d')

        result = {'high': [], 'low': [], 'normal': []}

        for stock in stock_list:
            try:
                df = get_price_jq(
                    symbols=stock,
                    start_date=start_date,
                    end_date=end_date,
                    frequency='daily',
                    fields=['close']
                )

                if df is None or df.empty or len(df) < n_days // 2:
                    result['normal'].append(stock)
                    continue

                # 取最近n_days天数据
                recent_df = df.tail(n_days)
                closes = recent_df['close'].values

                if len(closes) == 0:
                    result['normal'].append(stock)
                    continue

                current_price = closes[-1]
                high_threshold = np.percentile(closes, high_pct * 100)
                low_threshold = np.percentile(closes, low_pct * 100)

                if current_price >= high_threshold:
                    result['high'].append(stock)
                elif current_price <= low_threshold:
                    result['low'].append(stock)
                else:
                    result['normal'].append(stock)

            except Exception:
                result['normal'].append(stock)

        return result

    except Exception as e:
        warnings.warn(f"get_hl_stock 失败: {e}")
        return {'high': [], 'low': [], 'normal': stock_list}


def get_continue_count_df(stock_list, n_days=30, date=None):
    """
    获取连板统计DataFrame

    统计股票在近N天内的连续涨停天数

    参数:
        stock_list: 股票代码列表
        n_days: 回看天数，默认30天
        date: 基准日期（可选）

    返回:
        DataFrame: columns=['code', 'continue_count', 'max_continue', 'last_limit_date']
            - continue_count: 最近一次连板天数
            - max_continue: 最大连板天数
            - last_limit_date: 最近涨停日期
    """
    if not stock_list:
        return pd.DataFrame(columns=['code', 'continue_count', 'max_continue', 'last_limit_date'])

    try:
        from jk2bt.core.strategy_base import get_price_jq

        if date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            end_date = date

        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=n_days + 20)).strftime('%Y-%m-%d')

        results = []

        for stock in stock_list:
            try:
                df = get_price_jq(
                    symbols=stock,
                    start_date=start_date,
                    end_date=end_date,
                    frequency='daily',
                    fields=['close', 'high_limit', 'pre_close']
                )

                if df is None or df.empty:
                    continue

                # 判断每日是否涨停
                df['is_limit_up'] = False
                for idx in df.index:
                    close = df.loc[idx, 'close']
                    high_limit = df.loc[idx, 'high_limit']
                    pre_close = df.loc[idx, 'pre_close'] if 'pre_close' in df.columns else None

                    if high_limit is not None and close is not None:
                        # 涨停判断：收盘价等于涨停价
                        if abs(close - high_limit) / high_limit < 0.001:
                            df.loc[idx, 'is_limit_up'] = True
                        # 备用判断：涨幅>=9.8%
                        elif pre_close is not None and pre_close > 0:
                            pct = (close - pre_close) / pre_close
                            if pct >= 0.098:
                                df.loc[idx, 'is_limit_up'] = True

                # 计算连板
                is_limit = df['is_limit_up'].values
                max_continue = 0
                current_continue = 0
                last_continue = 0
                last_limit_date = None

                for i, limit in enumerate(is_limit):
                    if limit:
                        current_continue += 1
                        last_limit_date = df.index[i]
                        max_continue = max(max_continue, current_continue)
                    else:
                        if current_continue > 0:
                            last_continue = current_continue
                        current_continue = 0

                # 如果最后还在连板中
                if current_continue > 0:
                    last_continue = current_continue

                results.append({
                    'code': stock,
                    'continue_count': last_continue,
                    'max_continue': max_continue,
                    'last_limit_date': last_limit_date
                })

            except Exception:
                continue

        return pd.DataFrame(results)

    except Exception as e:
        warnings.warn(f"get_continue_count_df 失败: {e}")
        return pd.DataFrame(columns=['code', 'continue_count', 'max_continue', 'last_limit_date'])


def get_hl_count_df(stock_list, n_days=20, date=None):
    """
    获取高低点统计DataFrame

    统计股票在近N天内创新高/新低的次数

    参数:
        stock_list: 股票代码列表
        n_days: 回看天数，默认20天
        date: 基准日期（可选）

    返回:
        DataFrame: columns=['code', 'high_count', 'low_count', 'high_date', 'low_date']
    """
    if not stock_list:
        return pd.DataFrame(columns=['code', 'high_count', 'low_count', 'high_date', 'low_date'])

    try:
        from jk2bt.core.strategy_base import get_price_jq

        if date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            end_date = date

        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=n_days + 20)).strftime('%Y-%m-%d')

        results = []

        for stock in stock_list:
            try:
                df = get_price_jq(
                    symbols=stock,
                    start_date=start_date,
                    end_date=end_date,
                    frequency='daily',
                    fields=['high', 'low']
                )

                if df is None or df.empty or len(df) < 5:
                    continue

                # 取最近n_days天
                recent_df = df.tail(n_days).copy()
                recent_df['high_count'] = 0
                recent_df['low_count'] = 0

                high_count = 0
                low_count = 0
                last_high_date = None
                last_low_date = None

                highs = recent_df['high'].values
                lows = recent_df['low'].values

                for i in range(len(highs)):
                    # 创新高：当前最高价大于之前所有最高价
                    if i > 0 and highs[i] > np.max(highs[:i]):
                        high_count += 1
                        last_high_date = recent_df.index[i]

                    # 创新低：当前最低价小于之前所有最低价
                    if i > 0 and lows[i] < np.min(lows[:i]):
                        low_count += 1
                        last_low_date = recent_df.index[i]

                results.append({
                    'code': stock,
                    'high_count': high_count,
                    'low_count': low_count,
                    'high_date': last_high_date,
                    'low_date': last_low_date
                })

            except Exception:
                continue

        return pd.DataFrame(results)

    except Exception as e:
        warnings.warn(f"get_hl_count_df 失败: {e}")
        return pd.DataFrame(columns=['code', 'high_count', 'low_count', 'high_date', 'low_date'])


__all__ = [
    'get_recent_limit_up_stock',
    'get_recent_limit_down_stock',
    'get_hl_stock',
    'get_continue_count_df',
    'get_hl_count_df',
]