# 分歧反包二板策略 - RiceQuant版本（日线简化版）
# 原文：87.5%胜率之分歧反包二板
# 作者：游资小码哥
# 原文：https://www.joinquant.com/post/34048
# 注：原版依赖分钟级数据和get_ticks，此版本用日线近似
# 逻辑：选近期有涨停、昨日高开低走（分歧）、今日反包的股票

import numpy as np


def init(context):
    context.buy_count = 3
    context.candidates = []
    context.week = -1
    scheduler.run_weekly(prepare_candidates, weekday=1, time_rule=market_open(minute=0))
    scheduler.run_daily(trade, time_rule=market_open(minute=5))
    scheduler.run_daily(check_stop, time_rule=market_open(minute=220))



def handle_bar(context, bar_dict):
    pass

def has_limit_up_recently(stock, days=10):
    """近N天是否有涨停（单日涨幅>=9.5%）"""
    try:
        prices = history_bars(stock, days + 1, '1d', 'close')
        if prices is None or len(prices) < days + 1:
            return False
        p = np.array(prices, dtype=float)
        for i in range(1, len(p)):
            if p[i] / p[i-1] >= 1.095:
                return True
        return False
    except Exception:
        return False


def prepare_candidates(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8', '3'))]

    candidates = []
    for stock in stocks[:300]:
        if has_limit_up_recently(stock, 10):
            candidates.append(stock)
        if len(candidates) >= context.buy_count * 5:
            break

    context.candidates = candidates


def trade(context, bar_dict):
    if not context.candidates:
        return

    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        # 日线近似：今日开盘高于昨收5%以上，且当前价高于开盘（反包信号）
        prices = history_bars(stock, 2, '1d', 'close')
        if prices is None or len(prices) < 2:
            continue
        pre_close = prices[-2]
        if bar.open > pre_close * 1.05 and bar.close > bar.open * 1.02:
            target.append(stock)
        if len(target) >= context.buy_count:
            break

    if not target:
        return

    context.week = context.now.isocalendar()[1]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)


def check_stop(context, bar_dict):
    """14:40 止损：跌幅超5%卖出"""
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if pos and bar:
            avg_cost = getattr(pos, 'avg_cost', getattr(pos, 'avg_price', 0))
            if avg_cost > 0 and bar.close / avg_cost - 1 < -0.05:
                order_target_value(stock, 0)
