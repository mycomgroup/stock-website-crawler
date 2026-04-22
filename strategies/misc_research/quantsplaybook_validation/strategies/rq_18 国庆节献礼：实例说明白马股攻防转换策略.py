# 原文链接：https://www.joinquant.com/post/44563
# 策略：国庆节献礼：实例说明白马股攻防转换策略
# 作者：蚂蚁量化
# 核心逻辑：根据市场温度（冷/暖/热）切换选股条件，从沪深300中选PB低/ROA高的白马股，每月调仓

import numpy as np


def init(context):
    context.buy_count = 5
    context.stock_pool = []
    context.market_temp = "warm"
    scheduler.run_monthly(before_market_open, tradingday=1, time_rule=market_open(minute=5))
    scheduler.run_monthly(my_trade, tradingday=1, time_rule=market_open(minute=45))


def handle_bar(context, bar_dict):
    pass


def before_market_open(context, bar_dict):
    # 市场温度判断
    idx = history_bars('000300.XSHG', 220, '1d', 'close')
    if idx is not None and len(idx) >= 60:
        p = np.array(idx, dtype=float)
        height = (np.mean(p[-5:]) - np.min(p)) / (np.max(p) - np.min(p) + 1e-9)
        if height < 0.20:
            context.market_temp = "cold"
        elif height > 0.90:
            context.market_temp = "hot"
        else:
            context.market_temp = "warm"

    stocks = index_components('000300.XSHG')
    # 过滤ST/科创/北交
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]

    if context.market_temp == "cold":
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'roe'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['pb_ratio'] < 1.0]
        df = df.sort_values('roe', ascending=False)
        df = df.head(context.buy_count + 2)
        candidates = df.index.tolist()
    context.stock_pool = list(df.index)[:context.buy_count]
    logger.info(f"[白马股] 市场温度={context.market_temp} 股票池={context.stock_pool}")


def my_trade(context, bar_dict):
    # 卖出不在池中的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in context.stock_pool:
            order_target_value(s, 0)
    # 等权买入
    n = len(context.stock_pool)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in context.stock_pool:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
