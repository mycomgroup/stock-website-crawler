# QRS择时策略 - RiceQuant版本
# 来源：《中金公司-量化择时系列（1）：金融工程视角下的技术择时艺术》
# QRS = Quantitative Relative Strength，基于相对强弱的技术择时

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.lookback = 20  # 回看周期
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    lookback = context.lookback

    # 获取历史收盘价
    prices = history_bars(security, lookback + 5, '1d', 'close')
    if prices is None or len(prices) < lookback:
        return

    closes = np.array(prices)

    # 计算QRS指标
    # 相对强弱 = 当前价格相对于过去N天的位置
    current_close = closes[-1]
    min_close = np.min(closes[-lookback:])
    max_close = np.max(closes[-lookback:])

    # QRS = (Close - Min) / (Max - Min)
    if max_close == min_close:
        qrs = 0.5
    else:
        qrs = (current_close - min_close) / (max_close - min_close)

    # 计算QRS的移动平均（平滑）
    qrs_values = []
    for i in range(lookback, len(closes)):
        c = closes[i]
        min_c = np.min(closes[i-lookback:i])
        max_c = np.max(closes[i-lookback:i])
        if max_c == min_c:
            qrs_values.append(0.5)
        else:
            qrs_values.append((c - min_c) / (max_c - min_c))

    qrs_ma = np.mean(qrs_values[-5:])  # 5日平滑

    # 交易逻辑
    # QRS > 0.7 且 QRS_MA上升趋势 → 买入
    # QRS < 0.3 且 QRS_MA下降趋势 → 卖出

    if qrs > 0.7 and qrs_ma > 0.5 and not context.pos:
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入: QRS={qrs:.2f}, QRS_MA={qrs_ma:.2f}")
    elif qrs < 0.3 and qrs_ma < 0.5 and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: QRS={qrs:.2f}, QRS_MA={qrs_ma:.2f}")