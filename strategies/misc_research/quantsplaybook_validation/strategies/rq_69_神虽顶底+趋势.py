# RiceQuant Python格式策略
# 来源: JoinQuant - 69 神虽顶底+趋势
# 克隆自聚宽文章：https://www.joinquant.com/post/29276
# 标题：（12.3更新v1.2）朱虽自用1号（神虽顶底+趋势）
# 作者：Fibonabbit

import numpy as np
import datetime


def init(context):
    print('初始函数开始运行且全局只运行一次')


    context.security = '399001.XSHE'  # 默认使用深证综指

    scheduler.run_daily(before_market_open, time_rule=market_open(minute=0))
    scheduler.run_daily(market_open_trade, time_rule=market_open(minute=30))
    scheduler.run_daily(after_market_close, time_rule=market_close(minute=30))


def handle_bar(context, bar_dict):
    pass


def ema(c_list, n):
    y_list = []
    _n = 1
    for i in range(len(c_list)):
        if _n == 1:
            y = c_list[0]
        elif _n > 1 and _n <= n:
            y = c_list[i] * 2 / (_n + 1) + (1 - 2 / (_n + 1)) * y_list[-1]
        else:
            y = c_list[i] * 2 / (n + 1) + (1 - 2 / (n + 1)) * y_list[-1]
        y_list.append(y)
        _n = _n + 1
    return y_list


def macdx(c_list):
    dif = np.array(ema(c_list, 12)) - np.array(ema(c_list, 26))
    dea = ema(dif, 9)
    macd = (dif - dea) * 2
    return [dif, dea, macd]


def trend(high, low):
    shortLong = ema(high, 25)
    shortShort = ema(low, 25)
    longLong = ema(high, 90)
    longShort = ema(low, 90)
    return [shortLong, shortShort, longLong, longShort]


def hasCross(data):
    deadcross = []
    goldcross = []
    macd_result = macdx(data)
    for i in range(1, len(data)):
        if macd_result[2][i] < 0 and macd_result[2][i - 1] >= 0:
            deadcross.append(True)
        else:
            deadcross.append(False)
        if macd_result[2][i] > 0 and macd_result[2][i - 1] <= 0:
            goldcross.append(True)
        else:
            goldcross.append(False)
    return [deadcross, goldcross]


def barslast(xlist):
    barslast_list = []
    for i in range(len(xlist)):
        if xlist[i] == True:
            barslast_list.append(199 - i)
    return barslast_list


def before_market_open(context, bar_dict):
    if context.now >= datetime.datetime(2017, 1, 1):
        context.security = '399001.XSHE'
    else:
        context.security = '000001.XSHG'


def market_open_trade(context, bar_dict):
    print('函数运行时间(market_open):' + str(context.now.time()))
    security = context.security

    today_closes = history_bars(security, 1, '1d', 'close')
    today_highs = history_bars(security, 1, '1d', 'high')
    today_lows = history_bars(security, 1, '1d', 'low')
    cash = context.portfolio.cash
    tv = context.portfolio.total_value

    hist_closes = history_bars(security, 199, '1d', 'close')
    if hist_closes is None or len(hist_closes) == 0:
        return
    hist_highs = history_bars(security, 199, '1d', 'high')
    hist_lows = history_bars(security, 199, '1d', 'low')
    closes = np.append(hist_closes, today_closes[-1])
    highs = np.append(hist_highs, today_highs[-1])
    lows = np.append(hist_lows, today_lows[-1])

    trends = trend(highs, lows)

    current_price = today_closes[-1]
    security = '159901.XSHE'

    if (context.now.hour == 14 and context.now.minute >= 55):
        if current_price < trends[1][-1] and current_price < trends[3][-1]:
            print("价格低于长短期趋势下轨, 交易 %s至空仓" % (security))
            order_target_value(security, 0)
        elif current_price > trends[0][-1] and current_price < trends[3][-1]:
            print("价格低于长期趋势下轨但高于短期趋势上轨, 交易 %s至4成仓" % (security))
            order_target_value(security, 0.4 * tv)
        elif current_price > trends[2][-1] and current_price < trends[1][-1]:
            print("价格低于短期趋势下轨但高于长期趋势上轨, 交易 %s至6成仓" % (security))
            order_target_value(security, 0.6 * tv)
        elif current_price > trends[0][-1] and current_price > trends[2][-1]:
            print("价格高于长短期趋势上轨, 交易 %s至满仓" % (security))
            order_target_value(security, tv)


def after_market_close(context, bar_dict):
    print('##############################################################')
