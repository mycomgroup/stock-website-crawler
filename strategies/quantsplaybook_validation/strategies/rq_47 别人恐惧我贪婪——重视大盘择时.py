# 原文链接：https://www.joinquant.com/post/别人恐惧我贪婪重视大盘择时
# 策略：别人恐惧我贪婪——重视大盘择时
# 核心逻辑：用大盘恐慌指数（VIX代理：大盘波动率）择时，高恐慌时买入，低恐慌时卖出。

import numpy as np

def init(context):
    context.n_stocks = 10
    context.bond_etf = '511010.XSHG'
    context.index_etf = '510300.XSHG'
    context.vol_high = 0.025   # 高恐慌阈值（波动率）
    context.vol_low = 0.012    # 低恐慌阈值
    context.in_market = False
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 计算大盘近20日波动率作为恐慌代理
    prices = history_bars(context.index_etf, 21, '1d', 'close')
    if len(prices) < 21:
        return
    returns = np.diff(prices) / prices[:-1]
    vol = np.std(returns)

    if vol > context.vol_high:
        # 高恐慌：别人恐惧我贪婪，买入低PE高ROE股票
        stocks = all_instruments('CS')['order_book_id'].tolist()
        stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pe_ratio', 'market_cap', 'roe'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['pe_ratio'] < 20.0]
        df = df[df['roe'] > 0.15]
        df = df.head(context.n_stocks + 5)
        candidates = df.index.tolist()
        target = list(df.index)[:context.n_stocks]

        if context.bond_etf in context.portfolio.positions:
            order_target_value(context.bond_etf, 0)
        for s in list(context.portfolio.positions.keys()):
            if s not in target:
                order_target_value(s, 0)

        n = len(target)
        if n > 0:
            value = context.portfolio.total_value * 0.95 / n
            for s in target:
                if s in bar_dict and bar_dict[s].is_trading:
                    order_target_value(s, value)
        context.in_market = True
        logger.info(f"波动率={vol:.4f}（高恐慌），贪婪买入: {target}")

    elif vol < context.vol_low and context.in_market:
        # 低恐慌：别人贪婪我恐惧，切换债券
        for s in list(context.portfolio.positions.keys()):
            if s != context.bond_etf:
                order_target_value(s, 0)
        order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        context.in_market = False
        logger.info(f"波动率={vol:.4f}（低恐慌），恐惧切换债券")
