# 原文链接：https://www.joinquant.com/post/44780
# 策略：利用宏观经济数据的中长线策略深度研究
# 作者：宏观研究员
# 核心逻辑：用大盘PE偏离均值判断市场估值，低估时持股，高估时持债ETF
# 注：原版用jqdata.macro宏观数据，此处改为用沪深300PE/PB作为宏观代理指标

import numpy as np


STOCK_ETF = '510300.XSHG'   # 沪深300ETF（股票）
BOND_ETF  = '511010.XSHG'   # 国债ETF（债券）


def init(context):
    context.stock_etf = STOCK_ETF
    context.bond_etf = BOND_ETF
    context.pe_history = []
    context.in_stock = False
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度再平衡：根据大盘PE估值切换股债"""
    # 获取沪深300 PE
    stocks_300 = index_components('000300.XSHG')
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks_300,
        ['pe_ratio'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 200.0]
    candidates = df.index.tolist()

    if df is None or len(df) == 0:
        logger.info("[宏观策略] 无PE数据")
        return

    median_pe = float(df['pe_ratio'].median())
    context.pe_history.append(median_pe)

    # 需要至少12个月历史PE
    if len(context.pe_history) < 12:
        logger.info(f"[宏观策略] 积累PE历史中 {len(context.pe_history)}/12 当前PE={median_pe:.1f}")
        # 默认持股
        _hold_stock(context, bar_dict)
        return

    pe_arr = np.array(context.pe_history[-24:], dtype=float)
    pe_mean = np.mean(pe_arr)
    pe_std = np.std(pe_arr)

    # 低估：PE < 均值 - 0.5*std → 持股
    # 高估：PE > 均值 + 1.0*std → 持债
    if median_pe < pe_mean - 0.5 * pe_std:
        logger.info(f"[宏观策略] 低估 PE={median_pe:.1f} 均值={pe_mean:.1f} → 持股")
        _hold_stock(context, bar_dict)
    elif median_pe > pe_mean + 1.0 * pe_std:
        logger.info(f"[宏观策略] 高估 PE={median_pe:.1f} 均值={pe_mean:.1f} → 持债")
        _hold_bond(context, bar_dict)
    else:
        logger.info(f"[宏观策略] 中性 PE={median_pe:.1f} 均值={pe_mean:.1f} → 维持")


def _hold_stock(context, bar_dict):
    order_target_value(context.bond_etf, 0)
    if context.stock_etf in bar_dict and bar_dict[context.stock_etf].is_trading:
        order_target_value(context.stock_etf, context.portfolio.total_value * 0.95)


def _hold_bond(context, bar_dict):
    order_target_value(context.stock_etf, 0)
    if context.bond_etf in bar_dict and bar_dict[context.bond_etf].is_trading:
        order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
