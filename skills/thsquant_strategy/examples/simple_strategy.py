# 简单双均线策略 - THSQuant SuperMind 格式
# 适用于同花顺量化平台回测
from mindgo_api import *

def init(context):
    context.stock = '000001.SZ'  # 平安银行
    set_benchmark('000300.SH')
    set_commission(PerShare(type='stock', cost=0.0002, min_trade_cost=0.0))
    set_slippage(PriceSlippage(0.002))

def handle_bar(context, bar_dict):
    stock = context.stock
    prices = history(stock, ['close'], 20, '1d', False, 'pre')
    if prices.empty or len(prices) < 20:
        return
    ma5 = prices['close'].iloc[-5:].mean()
    ma20 = prices['close'].mean()
    pos = context.portfolio.positions.get(stock)
    if ma5 > ma20 and not pos:
        order_target_percent(stock, 1.0)
        log.info('买入 ' + stock)
    elif ma5 < ma20 and pos:
        order_target_percent(stock, 0)
        log.info('卖出 ' + stock)
