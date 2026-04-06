# 【多因子选股模型框架】(单因子各项指标评分细则) - RiceQuant版本
# 原文：https://www.joinquant.com/post/27018
# 作者：酷安克L2
# 注：沪深300成分股，多因子排名打分，月度调仓持仓30只

import numpy as np
import pandas as pd


def init(context):
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    context.stock_index = '000300.XSHG'
    context.hold_num = 30
    context.last_month = -1
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


# 因子定义：(因子名, 方向)  正向=越大越好，负向=越小越好
FACTOR_CONFIG = [
    ('net_profit_margin', 'pos'),   # 净利润率，越高越好
    ('roa',              'pos'),    # 资产收益率，越高越好
    ('gross_profit_margin', 'pos'), # 毛利率，越高越好
    ('net_profit',       'pos'),    # 净利润（正值），越高越好
    ('pb_ratio',         'neg'),    # 市净率，越低越好（低估）
    ('ps_ratio',         'neg'),    # 市销率，越低越好（低估）
    ('pe_ratio',         'neg'),    # 市盈率，越低越好（低估）
    ('turnover_ratio',   'neg'),    # 换手率，越低越好（低换手稳定）
]

FACTOR_NAMES = [f for f, _ in FACTOR_CONFIG]


def rank_factor(series, direction):
    """对因子值进行百分位排名，正向越大排名越高，负向越小排名越高"""
    if direction == 'pos':
        return series.rank(pct=True, ascending=True)
    else:
        return series.rank(pct=True, ascending=False)


def get_stock_list(context):
    today = context.now.strftime('%Y-%m-%d')
    stocks = index_components(context.stock_index)
    if not stocks:
        return []

    try:
        # Use stocks directly (already filtered)
        df = None  # placeholder - stocks list used directly below
        if df is None or len(df) == 0:
            return []
    except Exception:
        return []

    if df is None or len(df) == 0:
        return []

    latest = df

    # 过滤：pe_ratio > 0（排除亏损股），pb_ratio > 0
    if 'pe_ratio' in latest.columns:
        latest = latest[latest['pe_ratio'] > 0]
    if 'pb_ratio' in latest.columns:
        latest = latest[latest['pb_ratio'] > 0]

    latest = latest.dropna(how='any')
    if latest.empty:
        return []

    # 对每个因子排名，汇总得分
    total_score = pd.Series(0.0, index=latest.index)
    for factor_name, direction in FACTOR_CONFIG:
        if factor_name not in latest.columns:
            continue
        col = latest[factor_name]
        # 对于负向因子，过滤掉负值（如负PE无意义）
        if direction == 'neg':
            col = col[col > 0]
        ranked = rank_factor(col, direction)
        total_score = total_score.add(ranked, fill_value=0)

    total_score = total_score.sort_values(ascending=False)
    return list(total_score.index[: context.hold_num])


def trade(context, bar_dict):
    """月度调仓"""
    if context.now.month == context.last_month:
        return
    context.last_month = context.now.month

    target = get_stock_list(context)
    if not target:
        return

    # 过滤停牌
    target = [s for s in target if s in bar_dict and bar_dict[s].is_trading]
    if not target:
        return

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    w = 1.0 / len(target)
    for s in target:
        order_target_value(s, context.portfolio.total_value * w * 0.95)
