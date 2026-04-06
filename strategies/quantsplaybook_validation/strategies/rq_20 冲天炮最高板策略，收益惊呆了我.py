# 原文链接：https://www.joinquant.com/post/44680
# 策略：冲天炮最高板策略，收益惊呆了我
# 作者：量化达人
# 核心逻辑：选前一日涨停且今日高开的股票（冲天炮形态），分钟级买入
# 注：原版用sklearn线性回归辅助，此处直接实现冲天炮选股逻辑

import numpy as np


def init(context):
    context.stock_pool = []
    context.max_hold = 3
    scheduler.run_daily(before_open, time_rule=market_open(minute=0))
    scheduler.run_daily(open_trade, time_rule=market_open(minute=3))
    scheduler.run_daily(close_trade, time_rule=market_close(minute=5))


def handle_bar(context, bar_dict):
    pass


def before_open(context, bar_dict):
    """盘前筛选冲天炮候选股"""
    all_stocks_df = all_instruments('CS')
    all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                  if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]

    candidates = []
    for stock in all_stocks[:3000]:
        try:
            closes = history_bars(stock, 3, '1d', 'close')
            highs = history_bars(stock, 3, '1d', 'high')
            opens = history_bars(stock, 3, '1d', 'open')
            if closes is None or len(closes) < 3:
                continue

            # 昨日涨停判断：收盘价 >= 前日收盘 * 1.099
            prev_close = closes[-3]
            yest_close = closes[-2]
            yest_high = highs[-2]
            yest_open = opens[-2]

            limit_price = prev_close * 1.099
            # 昨日涨停：收盘价触及涨停
            if yest_close < limit_price:
                continue
            # 昨日非一字板（有开盘低于涨停的过程）
            if yest_open >= limit_price:
                continue
            # 今日高开（今日开盘 > 昨日收盘）
            today_open = opens[-1]
            if today_open <= yest_close * 1.005:
                continue

            candidates.append(stock)
        except Exception:
            continue

    context.stock_pool = candidates[:context.max_hold * 2]
    logger.info(f"[冲天炮] 候选={len(context.stock_pool)}")


def open_trade(context, bar_dict):
    """开盘后3分钟买入"""
    if not context.stock_pool:
        return

    # 清仓昨日持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in context.stock_pool:
            order_target_value(s, 0)

    n = min(len(context.stock_pool), context.max_hold)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    bought = 0
    for s in context.stock_pool:
        if bought >= context.max_hold:
            break
        if s not in bar_dict or not bar_dict[s].is_trading:
            continue
        order_target_value(s, value)
        bought += 1
        logger.info(f"[冲天炮] 买入 {s}")


def close_trade(context, bar_dict):
    """收盘前5分钟清仓（日内策略）"""
    for s in list(context.portfolio.positions.keys()):
        order_target_value(s, 0)
    logger.info("[冲天炮] 收盘清仓")
