# 原文链接：https://www.joinquant.com/post/53xxx
# 策略：超跌网格交易大法V1.2：稳健跑赢大盘-年化13%回撤7%
# 核心逻辑：超跌网格，选近期大幅下跌的股票，用网格方式分批买入，分批卖出

import numpy as np

OVERSOLD_DAYS = 20
OVERSOLD_RATIO = -0.15   # 超跌阈值：近20日跌幅>15%
GRID_LEVELS = 3          # 网格层数
HOLD_NUM = 5

def init(context):
    context.grid_positions = {}  # {stock: {'base_price': x, 'level': n}}
    scheduler.run_monthly(select_oversold, tradingday=1, time_rule=market_open(minute=30))
    scheduler.run_daily(grid_trade, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def select_oversold(context, bar_dict):
    """选超跌股票"""
    stocks = index_components('000300.XSHG')
    oversold = {}

    for stock in stocks:
        try:
            closes = history_bars(stock, OVERSOLD_DAYS + 1, '1d', 'close')
            if len(closes) < OVERSOLD_DAYS + 1:
                continue
            ret = (closes[-1] - closes[0]) / closes[0]
            if ret < OVERSOLD_RATIO:
                oversold[stock] = ret
        except Exception:
            continue

    if not oversold:
        return

    # 选跌幅最大的股票
    sorted_stocks = sorted(oversold, key=oversold.get, reverse=False)
    selected = sorted_stocks[:HOLD_NUM]

    for stock in selected:
        if stock not in context.grid_positions:
            try:
                base_price = bar_dict[stock].close
                context.grid_positions[stock] = {'base_price': base_price, 'level': 1}
                value = context.portfolio.cash * 0.1
                order_target_value(stock, value)
                logger.info(f"网格初始买入 {stock}，基准价 {base_price:.2f}")
            except Exception:
                pass

def grid_trade(context, bar_dict):
    """网格交易逻辑"""
    for stock, grid in list(context.grid_positions.items()):
        try:
            current_price = bar_dict[stock].close
            base_price = grid['base_price']
            level = grid['level']
            grid_step = 0.05  # 每格5%

            # 下跌一格，加仓
            if current_price < base_price * (1 - grid_step * level) and level < GRID_LEVELS:
                add_value = context.portfolio.cash * 0.05
                order_target_value(stock, context.portfolio.positions[stock].value + add_value)
                context.grid_positions[stock]['level'] = level + 1
                logger.info(f"{stock} 网格加仓，第{level+1}层")

            # 上涨一格，减仓
            elif current_price > base_price * (1 + grid_step) and level > 0:
                pos_value = context.portfolio.positions.get(stock)
                if pos_value:
                    reduce = pos_value.value * 0.3
                    order_target_value(stock, pos_value.value - reduce)
                    context.grid_positions[stock]['level'] = max(0, level - 1)
                    logger.info(f"{stock} 网格减仓")
        except Exception:
            continue
