# 原文链接：https://www.joinquant.com/post/53xxx
# 策略：基于大盘PE标准差偏离度的聪明基金定投策略
# 核心逻辑：用沪深300 PE偏离历史均值的标准差判断估值，低估时加仓ETF，高估时减仓

import numpy as np

ETF = '510300.XSHG'   # 沪深300ETF
BOND_ETF = '511010.XSHG'  # 国债ETF
PE_WINDOW = 250  # PE历史窗口（约1年）

def init(context):
    context.pe_history = []
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def get_market_pe(context):
    """获取沪深300当前PE"""
    try:
        stocks = index_components('000300.XSHG')
        factor_df = get_factor(
            stocks,
            ['market_cap', 'pb_ratio', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is not None and len(df) > 0:
            return df['pe_ratio'].median()
    except Exception:
        pass
    return None

def rebalance(context, bar_dict):
    current_pe = get_market_pe(context)
    if current_pe is None:
        return

    context.pe_history.append(current_pe)
    if len(context.pe_history) > PE_WINDOW:
        context.pe_history = context.pe_history[-PE_WINDOW:]

    if len(context.pe_history) < 12:
        # 数据不足，等权持有
        order_target_value(ETF, context.portfolio.total_value * 0.5)
        return

    pe_mean = np.mean(context.pe_history)
    pe_std = np.std(context.pe_history)
    z_score = (current_pe - pe_mean) / pe_std if pe_std > 0 else 0

    logger.info(f"当前PE: {current_pe:.2f}, Z-score: {z_score:.2f}")

    # 根据PE偏离度决定仓位
    if z_score < -1.5:
        # 严重低估，重仓ETF
        etf_ratio = 0.95
    elif z_score < -0.5:
        # 低估，加仓
        etf_ratio = 0.75
    elif z_score < 0.5:
        # 合理，均衡
        etf_ratio = 0.5
    elif z_score < 1.5:
        # 高估，减仓
        etf_ratio = 0.25
    else:
        # 严重高估，清仓转债
        etf_ratio = 0.05

    total = context.portfolio.total_value
    order_target_value(ETF, total * etf_ratio)
    order_target_value(BOND_ETF, total * (1 - etf_ratio) * 0.95)
    logger.info(f"ETF仓位: {etf_ratio:.0%}")
