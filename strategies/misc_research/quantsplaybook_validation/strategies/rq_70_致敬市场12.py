# RiceQuant Python格式策略
# 来源: JoinQuant - 70 致敬市场(12)——赚钱的策略
# 克隆自聚宽文章：https://www.joinquant.com/post/41444
# 标题：致敬市场(12)——赚钱的策略
# 作者：Gyro^.^

def init(context):

    context.index = '399310.XSHE'
    context.n = 50
    context.rente_ratio = 0.05
    context.cash_ratio = 2 * context.rente_ratio
    context.treasury_ratio = 0.4
    context.treasury_fund = '000012.XSHG'

    scheduler.run_daily(iUpdate, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def iUpdate(context, bar_dict):
    index = context.index
    n = context.n
    rente_ratio = context.rente_ratio
    cash_ratio = context.cash_ratio
    treasury_ratio = context.treasury_ratio
    treasury_fund = context.treasury_fund

    # 每年第一天分红，再平衡（JQR不支持inout_cash，跳过现金操作）
    if context.now.month == 1 and context.now.day == 1:
        print('!!!新年再平衡!!!')

    stocks = index_components(index)
    if not stocks:
        return

    for s in list(context.portfolio.positions.keys()):
        if s not in stocks:
            # 用history_bars判断是否停牌
            bars = history_bars(s, 1, '1d', 'close')
            if bars is not None and len(bars) > 0:
                print('sell', s, instruments(s).symbol)
                order_target_value(s, 0)

    cash_size = cash_ratio * context.portfolio.total_value
    position_size = (1.0 - cash_ratio - treasury_ratio) / n * context.portfolio.total_value

    for s in stocks:
        if context.portfolio.cash < cash_size:
            break
        if s not in context.portfolio.positions:
            bars = history_bars(s, 1, '1d', 'close')
            if bars is not None and len(bars) > 0:
                print('buy', s, instruments(s).symbol)
                order_target_value(s, position_size)

