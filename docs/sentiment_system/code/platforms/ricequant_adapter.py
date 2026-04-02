#!/usr/bin/env python3
"""
RiceQuant平台情绪指标适配模块

将聚宽API转换为RiceQuant API，实现跨平台兼容。

API差异对照:
┌─────────────────────────────┬───────────────────────────────────────┐
│ 聚宽 (JoinQuant)            │ RiceQuant                              │
├─────────────────────────────┼───────────────────────────────────────┤
│ get_all_securities()        │ all_instruments(type='CS')            │
│ get_price(stocks, fields)   │ get_price(stocks, fields)             │
│ get_trade_days()            │ get_trading_dates()                   │
│ high_limit                  │ limit_up                              │
│ low_limit                   │ limit_down                            │
│ panel=False                 │ 返回DataFrame，无需此参数              │
└─────────────────────────────┴───────────────────────────────────────┘

使用方法:
    from ricequant_adapter import calc_market_sentiment_rq

    sentiment = calc_market_sentiment_rq(date, prev_date)
"""

from typing import List, Dict, Optional
import pandas as pd
import numpy as np


def get_all_stocks_rq(date: str) -> List[str]:
    """
    RiceQuant版：获取所有股票列表

    参数:
        date: 日期字符串，如 '2024-01-01'

    返回:
        股票代码列表
    """
    # RiceQuant代码
    # all_stocks = all_instruments(type='CS', date=date)
    # return all_stocks['order_book_id'].tolist()

    # 过滤科创板和北交所
    # return [s for s in all_stocks if not (s.startswith('68') or s.startswith('4') or s.startswith('8'))]
    pass


def get_zt_stocks_rq(date: str) -> List[str]:
    """
    RiceQuant版：获取涨停股票列表

    参数:
        date: 日期字符串

    返回:
        涨停股票代码列表

    RiceQuant实现:
        all_stocks = get_all_stocks_rq(date)

        # 获取价格数据
        df = get_price(
            all_stocks,
            start_date=date,
            end_date=date,
            frequency='1d',
            fields=['close', 'limit_up'],
            expect_df=True
        )

        # 涨停：收盘价等于涨停价
        df = df.dropna()
        zt_df = df[df['close'] >= df['limit_up'] * 0.995]  # 允许0.5%误差
        return zt_df.index.tolist()
    """
    pass


def get_dt_stocks_rq(date: str) -> List[str]:
    """
    RiceQuant版：获取跌停股票列表

    参数:
        date: 日期字符串

    返回:
        跌停股票代码列表

    RiceQuant实现:
        all_stocks = get_all_stocks_rq(date)

        df = get_price(
            all_stocks,
            start_date=date,
            end_date=date,
            frequency='1d',
            fields=['close', 'limit_down'],
            expect_df=True
        )

        df = df.dropna()
        dt_df = df[df['close'] <= df['limit_down'] * 1.005]
        return dt_df.index.tolist()
    """
    pass


def calc_lianban_count_rq(stock: str, date: str, max_days: int = 10) -> int:
    """
    RiceQuant版：计算单只股票连板数

    参数:
        stock: 股票代码
        date: 日期字符串
        max_days: 最大回溯天数

    返回:
        连板数

    RiceQuant实现:
        # 获取历史交易日
        trading_dates = get_trading_dates(
            start_date=(pd.Timestamp(date) - pd.Timedelta(days=30)).strftime('%Y-%m-%d'),
            end_date=date
        )[-max_days:]

        if len(trading_dates) < max_days:
            return 0

        # 获取价格
        df = get_price(
            stock,
            start_date=trading_dates[0],
            end_date=trading_dates[-1],
            frequency='1d',
            fields=['close', 'limit_up'],
            expect_df=True
        )

        if len(df) < max_days:
            return 0

        # 从后向前统计连板
        count = 0
        for i in range(len(df) - 1, -1, -1):
            if df.iloc[i]['close'] >= df.iloc[i]['limit_up'] * 0.995:
                count += 1
            else:
                break
        return count
    """
    pass


def calc_market_sentiment_rq(date: str, prev_date: str) -> Dict:
    """
    RiceQuant版：计算市场情绪指标

    参数:
        date: 当前日期字符串
        prev_date: 前一交易日字符串

    返回:
        {
            'zt_count': 涨停家数,
            'dt_count': 跌停家数,
            'zt_dt_ratio': 涨跌停比,
            'max_lianban': 最高连板数,
            'jinji_rate': 晋级率
        }

    RiceQuant完整实现:
        result = {}

        # 1. 涨停家数
        zt_list = get_zt_stocks_rq(date)
        result['zt_count'] = len(zt_list)

        # 2. 跌停家数
        dt_list = get_dt_stocks_rq(date)
        result['dt_count'] = len(dt_list)

        # 3. 涨跌停比
        result['zt_dt_ratio'] = len(zt_list) / max(len(dt_list), 1)

        # 4. 最高连板数
        max_lianban = 0
        for stock in zt_list[:50]:  # 限制计算量
            lb = calc_lianban_count_rq(stock, date)
            max_lianban = max(max_lianban, lb)
        result['max_lianban'] = max_lianban

        # 5. 晋级率
        prev_zt_list = get_zt_stocks_rq(prev_date)
        if len(prev_zt_list) > 0:
            jinji_count = len(set(prev_zt_list) & set(zt_list))
            result['jinji_rate'] = jinji_count / len(prev_zt_list)
        else:
            result['jinji_rate'] = 0

        return result
    """
    pass


def get_trade_days_rq(start_date: str, end_date: str) -> List[str]:
    """
    RiceQuant版：获取交易日列表

    参数:
        start_date: 开始日期
        end_date: 结束日期

    返回:
        交易日字符串列表

    RiceQuant实现:
        dates = get_trading_dates(start_date=start_date, end_date=end_date)
        return [d.strftime('%Y-%m-%d') for d in dates]
    """
    pass


# ============ 聚宽到RiceQuant转换辅助函数 ============


def convert_jq_to_rq_code(jq_code: str) -> str:
    """
    将聚宽股票代码转换为RiceQuant格式

    聚宽格式: 000001.XSHE
    RiceQuant格式: 000001.XSHE (相同)

    参数:
        jq_code: 聚宽股票代码

    返回:
        RiceQuant股票代码
    """
    # 两者格式相同，无需转换
    return jq_code


def convert_rq_to_jq_code(rq_code: str) -> str:
    """
    将RiceQuant股票代码转换为聚宽格式

    参数:
        rq_code: RiceQuant股票代码

    返回:
        聚宽股票代码
    """
    return rq_code


# ============ 通用情绪计算函数（跨平台） ============


def calc_market_sentiment_universal(
    get_zt_func, get_dt_func, get_lianban_func, date: str, prev_date: str
) -> Dict:
    """
    通用情绪计算函数，适配不同平台

    参数:
        get_zt_func: 获取涨停股票的函数
        get_dt_func: 获取跌停股票的函数
        get_lianban_func: 计算连板数的函数
        date: 当前日期
        prev_date: 前一交易日

    返回:
        情绪指标字典
    """
    result = {}

    # 1. 涨停家数
    zt_list = get_zt_func(date)
    result["zt_count"] = len(zt_list)

    # 2. 跌停家数
    dt_list = get_dt_func(date)
    result["dt_count"] = len(dt_list)

    # 3. 涨跌停比
    result["zt_dt_ratio"] = len(zt_list) / max(len(dt_list), 1)

    # 4. 最高连板数
    max_lianban = 0
    for stock in zt_list[:50]:
        lb = get_lianban_func(stock, date)
        max_lianban = max(max_lianban, lb)
    result["max_lianban"] = max_lianban

    # 5. 晋级率
    prev_zt_list = get_zt_func(prev_date)
    if len(prev_zt_list) > 0:
        jinji_count = len(set(prev_zt_list) & set(zt_list))
        result["jinji_rate"] = jinji_count / len(prev_zt_list)
    else:
        result["jinji_rate"] = 0

    return result


# ============ 在RiceQuant策略中使用示例 ============

"""
# 在RiceQuant策略中引入情绪开关

from ricequant_adapter import calc_market_sentiment_rq
import sys
sys.path.append('/path/to/sentiment_system/code/core')
from sentiment_switch import sentiment_switch_combo
from sentiment_phase import classify_sentiment_phase

def init(context):
    context.sentiment_threshold = 30

def before_trading(context):
    # 计算昨日情绪
    date = context.current_dt.strftime('%Y-%m-%d')
    prev_date = get_previous_trading_date(date)
    
    sentiment = calc_market_sentiment_rq(date, prev_date)
    context.sentiment = sentiment
    context.phase = classify_sentiment_phase(sentiment)
    
    # 判断是否开仓
    context.should_trade = sentiment_switch_combo(sentiment)
    
    log.info(f"情绪周期: {context.phase}")
    log.info(f"涨停家数: {sentiment['zt_count']}")
    log.info(f"是否开仓: {context.should_trade}")

def handle_bar(context, bar_dict):
    if not context.should_trade:
        return
    
    # 执行策略逻辑
    pass
"""

if __name__ == "__main__":
    print("=" * 60)
    print("RiceQuant平台情绪指标适配模块")
    print("=" * 60)
    print("""
此模块提供RiceQuant平台适配代码。
请在RiceQuant环境中运行，或参考示例代码进行适配。

API差异对照:
- get_all_securities() → all_instruments(type='CS')
- get_trade_days() → get_trading_dates()
- high_limit → limit_up
- low_limit → limit_down
""")
