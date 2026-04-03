# 价量共振择时策略 - RiceQuant版本
# 来源：《华创证券-成交量的奥秘：另类价量共振指标的择时》
# 价量共振：价格与成交量的协同变化

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.period = 20
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    period = context.period

    # 获取历史数据（收盘价和成交量）
    bars = history_bars(security, period + 10, '1d', ['close', 'volume'])
    if bars is None or len(bars) < period:
        return

    closes = np.array(bars['close'])
    volumes = np.array(bars['volume'])

    # 计算价格变化率
    price_change = (closes[-1] - closes[-2]) / closes[-2]

    # 计算成交量变化率
    vol_change = (volumes[-1] - volumes[-2]) / volumes[-2] if volumes[-2] > 0 else 0

    # 价量共振指标
    # 价涨量增 → 正共振（强势）
    # 价跌量缩 → 负共振（弱势调整）
    # 价涨量缩 → 量价背离（可能反转）
    # 价跌量增 → 量价背离（可能反转）

    resonance = price_change * vol_change  # 正值为共振，负值为背离

    # 计算历史共振序列
    resonance_history = []
    for i in range(2, period + 2):
        pc = (closes[-i] - closes[-i-1]) / closes[-i-1]
        vc = (volumes[-i] - volumes[-i-1]) / volumes[-i-1] if volumes[-i-1] > 0 else 0
        resonance_history.append(pc * vc)

    resonance_ma = np.mean(resonance_history)
    resonance_std = np.std(resonance_history)

    # 标准化共振指标
    if resonance_std > 0:
        z_score = (resonance - resonance_ma) / resonance_std
    else:
        z_score = 0

    # 交易逻辑
    # 强正共振（z > 1）→ 买入信号
    # 强负共振（z < -1）或价跌量增背离 → 卖出信号

    if z_score > 1.0 and not context.pos:
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入价量共振: z={z_score:.2f}, resonance={resonance:.4f}")
    elif z_score < -1.0 and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出价量背离: z={z_score:.2f}, resonance={resonance:.4f}")