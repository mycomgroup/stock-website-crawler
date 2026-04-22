# 风险及免责提示：该策略由聚宽用户分享，仅供学习交流使用。
# 原文一般包含策略说明，如有疑问建议到原文和作者交流讨论。
# 克隆自聚宽文章：https://www.joinquant.com/post/27759
# 标题：ETF网格交易策略
# 作者：pia19

"""
ETF网格交易策略
- 核心逻辑：基于价格区间和网格间距进行高抛低吸
- 标的选择：512900.XSHG (ETF基金)
- 风险提示：网格策略在单边行情中可能失效
"""

def init(context):
    # 定义一个全局变量, 保存要操作的股票
    context.security = '512900.XSHG'
    # 设定沪深300作为基准
    # 开启动态复权模式(真实价格)
    # 设置滑点
    # 设置交易成本

    # 设置参数 区间 网格间距
    uplimit = 1.5
    downlimit = 0.9
    space = 6
    number = 3  # cash分隔份数

    # 单位间隔
    context.unitprice = (uplimit - downlimit) / space
    # 2019-04-01 收盘价格
    context.initialprice = 0.976
    context.initial_buy = downlimit + 0 * context.unitprice
    context.initial_sell = downlimit + 1 * context.unitprice
    # 将现金分割成几份
    context.cash = context.portfolio.cash / number

    # 打印每个买卖区间
    for i in range(0, space + 1):
        print(uplimit - i * context.unitprice)

    scheduler.run_daily(market_open_trade, time_rule=market_open(minute=30))
    scheduler.run_daily(after_market, time_rule=market_close(minute=30))


def handle_bar(context, bar_dict):
    pass


def market_open_trade(context, bar_dict):
    security = context.security
    cash = context.cash
    current_time = context.now

    # 获取股票的收盘价 - RiceQuant方式
    close_data = history_bars(security, 5, '1d', 'close')[-1]
    context.current_cash = context.portfolio.cash

    if close_data < context.initial_buy:
        # 计算可买入数量
        shares = int(cash / close_data)
        if shares > 0:
            order_shares(security, shares)
            print("Buying %s at price %s" % (security, close_data))
    elif close_data > context.initial_sell:
        # 卖出ETF
        position = context.portfolio.positions.get(security)
        if position and position.quantity > 0:
            order_shares(security, -position.quantity)
            print("Selling %s at price %s" % (security, close_data))


def after_market(context, bar_dict):
    close_cash = context.portfolio.cash
    print(context.current_cash, close_cash)

    # 卖出ETF 则盘后cash余额高于盘中 信号位置上升
    if context.current_cash < close_cash:
        context.initial_buy = context.initial_buy + context.unitprice
        context.initial_sell = context.initial_sell + context.unitprice
        print(context.initial_sell)
    # 买入ETF 则盘后cash余额低于盘中 信号位置下降
    elif context.current_cash > close_cash:
        context.initial_buy = context.initial_buy - context.unitprice
        context.initial_sell = context.initial_sell - context.unitprice
        print(context.initial_buy)
