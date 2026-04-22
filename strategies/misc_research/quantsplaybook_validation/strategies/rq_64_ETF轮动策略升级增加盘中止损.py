# 原文链接：https://www.joinquant.com/post/38838
# 策略：ETF轮动策略升级-增加盘中止损
# 作者：长鸿
# 核心逻辑：多类别ETF动量轮动 + 日频止损（原版用60分钟K线，此处简化为日频跌幅>3%）
# 注：原版用 talib/smtplib/prettytable，此处全部用 numpy 替代

import numpy as np

ETF_MAP = {
    '000300.XSHG': '510300.XSHG',   # 沪深300
    '000905.XSHG': '510500.XSHG',   # 中证500
    '399006.XSHE': '159915.XSHE',   # 创业板
    '000016.XSHG': '510050.XSHG',   # 上证50
    '399932.XSHE': '159928.XSHE',   # 中证消费
    '399913.XSHE': '512010.XSHG',   # 医药
    '000015.XSHG': '510880.XSHG',   # 红利
}
TYPE_NUM = 1
MOMENT_PERIOD = 13
MA_PERIOD = 10
MONEY_FUND = '511880.XSHG'


def init(context):
    context.etf_map = ETF_MAP
    context.type_num = TYPE_NUM
    context.targets = []
    scheduler.run_daily(get_signal, time_rule=market_close(minute=23))
    scheduler.run_daily(etf_trade, time_rule=market_close(minute=21))
    scheduler.run_daily(check_stop, time_rule=market_close(minute=30))


def handle_bar(context, bar_dict):
    pass


def get_signal(context, bar_dict):
    scores = {}
    for idx, etf in context.etf_map.items():
        prices = history_bars(etf, MOMENT_PERIOD + MA_PERIOD + 5, '1d', 'close')
        if prices is None or len(prices) < MOMENT_PERIOD + MA_PERIOD:
            continue
        p = np.array(prices, dtype=float)
        if p[-MOMENT_PERIOD] == 0:
            continue
        momentum = p[-1] / p[-MOMENT_PERIOD] - 1
        ma_short = np.mean(p[-MOMENT_PERIOD:])
        ma_long  = np.mean(p[-MA_PERIOD:])
        if ma_long == 0:
            continue
        ma_diff = ma_short / ma_long - 1
        score = momentum * (1 + ma_diff)
        scores[etf] = score

    if not scores:
        context.targets = [MONEY_FUND]
        return

    sorted_etfs = sorted(scores, key=scores.get, reverse=True)
    # 只选正动量的
    positive = [e for e in sorted_etfs if scores[e] > 0]
    context.targets = positive[:context.type_num] if positive else [MONEY_FUND]


def etf_trade(context, bar_dict):
    targets = context.targets
    for s in list(context.portfolio.positions.keys()):
        if s not in targets:
            order_target_value(s, 0)
    if targets:
        w = 0.95 / len(targets)
        for etf in targets:
            order_target_value(etf, context.portfolio.total_value * w)


def check_stop(context, bar_dict):
    """日频止损：当日跌幅超过3%则卖出"""
    for s in list(context.portfolio.positions.keys()):
        prices = history_bars(s, 2, '1d', 'close')
        if prices is None or len(prices) < 2:
            continue
        if prices[-1] / prices[-2] - 1 < -0.03:
            order_target_value(s, 0)
            print(f"[ETF轮动升级] 止损 {s}")
