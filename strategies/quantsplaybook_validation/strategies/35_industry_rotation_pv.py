# 行业有效量价因子与行业轮动策略 - RiceQuant版本
# 来源：《行业有效量价因子与行业轮动策略》
# 核心逻辑：计算各行业ETF的量价动量因子，选择动量最强的行业ETF持仓

import numpy as np


# 主要行业ETF代码
INDUSTRY_ETFS = {
    '510880.XSHG': '红利ETF',
    '512010.XSHG': '军工ETF',
    '512660.XSHG': '军工ETF2',
    '512800.XSHG': '银行ETF',
    '515000.XSHG': '科技ETF',
    '515030.XSHG': '新能源ETF',
    '159928.XSHE': '消费ETF',
    '159915.XSHE': '创业板ETF',
    '159905.XSHE': '油气ETF',
    '159869.XSHE': '医疗ETF',
}


def calc_pv_momentum(prices, volumes, window=20):
    """量价动量因子：价格动量 * 成交量趋势"""
    if len(prices) < window + 1:
        return None
    p = np.array(prices[-window-1:], dtype=float)
    v = np.array(volumes[-window:], dtype=float)

    price_mom = (p[-1] / p[0]) - 1
    vol_trend = np.corrcoef(np.arange(window), v)[0, 1] if np.std(v) > 0 else 0

    return price_mom * (1 + vol_trend)


def init(context):
    context.etfs = list(INDUSTRY_ETFS.keys())
    context.window = 20
    context.top_n = 3       # 持仓行业数
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    scores = {}
    for etf in context.etfs:
        try:
            prices = history_bars(etf, context.window + 2, '1d', 'close')
            volumes = history_bars(etf, context.window + 1, '1d', 'volume')
            if prices is None or volumes is None:
                continue
            factor = calc_pv_momentum(
                np.array(prices, dtype=float),
                np.array(volumes, dtype=float),
                context.window
            )
            if factor is not None:
                scores[etf] = factor
        except Exception:
            continue

    if not scores:
        return

    sorted_etfs = sorted(scores, key=scores.get, reverse=True)
    target = sorted_etfs[:context.top_n]

    for etf in list(context.portfolio.positions.keys()):
        if etf not in target:
            order_to(etf, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for etf in target:
        order_target_value(etf, total_value * weight * 0.95)
