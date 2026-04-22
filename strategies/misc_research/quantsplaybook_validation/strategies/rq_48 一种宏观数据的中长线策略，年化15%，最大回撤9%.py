# 原文链接：https://www.joinquant.com/post/一种宏观数据的中长线策略年化15最大回撤9
# 策略：一种宏观数据的中长线策略，年化15%，最大回撤9%
# 核心逻辑：用大盘PE/PB作为宏观代理，PE低于历史均值时持股，否则持债ETF(511010)。

import numpy as np

def init(context):
    context.n_stocks = 10
    context.bond_etf = '511010.XSHG'
    context.index_code = '000300.XSHG'
    context.pe_history = []
    context.pe_window = 60  # 历史PE均值窗口（月）
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 获取沪深300成分股的整体PE作为宏观代理
    hs300 = index_components(context.index_code)
    prev_date = context.now.date()
    factor_df = get_factor(
        hs300,
        ['pe_ratio', 'pb_ratio', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 100.0]
    df = df.head(300)
    candidates = df.index.tolist()
    if df.empty:
        return

    current_pe = df['pe_ratio'].median()
    context.pe_history.append(current_pe)

    # 保持历史窗口
    if len(context.pe_history) > context.pe_window:
        context.pe_history = context.pe_history[-context.pe_window:]

    hist_pe_mean = np.mean(context.pe_history)
    hist_pe_std = np.std(context.pe_history)

    logger.info(f"当前PE中位数={current_pe:.1f}，历史均值={hist_pe_mean:.1f}，历史标准差={hist_pe_std:.1f}")

    if current_pe < hist_pe_mean:
        # PE低于历史均值，市场低估，持股
        target_stocks = list(df[df['pe_ratio'] < hist_pe_mean].sort_values(
            'roe', ascending=False
        ).index[:context.n_stocks])

        if context.bond_etf in context.portfolio.positions:
            order_target_value(context.bond_etf, 0)

        for s in list(context.portfolio.positions.keys()):
            if s not in target_stocks:
                order_target_value(s, 0)

        n = len(target_stocks)
        if n > 0:
            value = context.portfolio.total_value * 0.95 / n
            for s in target_stocks:
                if s in bar_dict and bar_dict[s].is_trading:
                    order_target_value(s, value)
        logger.info(f"PE低估，持股: {target_stocks[:5]}")

    else:
        # PE高于历史均值，市场高估，持债
        for s in list(context.portfolio.positions.keys()):
            if s != context.bond_etf:
                order_target_value(s, 0)
        order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        logger.info(f"PE高估（{current_pe:.1f}>{hist_pe_mean:.1f}），持债ETF")
