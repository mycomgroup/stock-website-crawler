# 双均线策略示例
# 策略逻辑：当短期均线上穿长期均线时买入，下穿时卖出


def init(context):
    # 设置基准
    context.benchmark = "000300.XSHG"
    # 设置回测频率
    context.frequency = "day"
    # 设置股票池
    context.security = "000001.XSHE"
    # 设置均线周期
    context.short_window = 5
    context.long_window = 20


def handle_bar(context, bar_dict):
    # 获取当前股票
    security = context.security

    # 获取历史价格
    hist = history_bars(security, context.long_window + 10, "1d", "close")

    if len(hist) < context.long_window:
        return

    # 计算均线
    short_ma = hist[-context.short_window :].mean()
    long_ma = hist[-context.long_window :].mean()

    # 获取当前持仓
    position = context.portfolio.positions[security].quantity

    # 交易逻辑
    if short_ma > long_ma and position == 0:
        # 金叉买入
        order_value(security, context.portfolio.available_cash * 0.95)
        log.info(f"Buy {security} at {bar_dict[security].close}")
    elif short_ma < long_ma and position > 0:
        # 死叉卖出
        order_target(security, 0)
        log.info(f"Sell {security} at {bar_dict[security].close}")
