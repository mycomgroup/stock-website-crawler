# 行业指数顶部和底部信号策略 - RiceQuant版本
# 来源：《行业指数顶部和底部信号：净新高占比（(NH-NL)%）》
# 核心逻辑：计算行业成分股中创年度新高与新低之差的占比（NHNL%），
#           NHNL%极低时买入（底部信号），极高时卖出（顶部信号）

import numpy as np


def init(context):
    # 以沪深300为代理标的，用其成分股计算NHNL%
    context.index = '000300.XSHG'
    context.security = '510300.XSHG'  # 沪深300ETF
    context.nhnl_window = 252          # 年度新高新低窗口
    context.signal_window = 20         # 信号平滑窗口
    context.buy_threshold = -0.3       # NHNL%低于此值买入（底部）
    context.sell_threshold = 0.5       # NHNL%高于此值卖出（顶部）
    context.pos = False
    context.nhnl_history = []


def handle_bar(context, bar_dict):
    security = context.security

    # 获取沪深300成分股
    stocks = index_components(context.index)
    if not stocks:
        return

    # 取样本（避免计算量过大，取前100只）
    sample = stocks[:100]

    # 获取历史价格计算年度新高新低
    new_high_count = 0
    new_low_count = 0
    valid_count = 0

    for stock in sample:
        try:
            prices = history_bars(stock, context.nhnl_window, '1d', 'close')
            if prices is None or len(prices) < context.nhnl_window:
                continue
            current = prices[-1]
            year_high = np.max(prices[:-1])
            year_low = np.min(prices[:-1])
            valid_count += 1
            if current >= year_high:
                new_high_count += 1
            elif current <= year_low:
                new_low_count += 1
        except:
            continue

    if valid_count == 0:
        return

    # 计算净新高占比
    nhnl_pct = (new_high_count - new_low_count) / valid_count
    context.nhnl_history.append(nhnl_pct)

    if len(context.nhnl_history) < context.signal_window:
        return

    # 平滑信号
    smooth_nhnl = np.mean(context.nhnl_history[-context.signal_window:])

    # 交易逻辑：反转策略
    if smooth_nhnl < context.buy_threshold and not context.pos:
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入(底部信号): NHNL%={smooth_nhnl:.3f}")

    elif smooth_nhnl > context.sell_threshold and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出(顶部信号): NHNL%={smooth_nhnl:.3f}")
