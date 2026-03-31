"""
验证策略 - RiceQuant 正确格式
参考 Golden Cross 策略
"""


def init(context):
    context.s1 = "000001.XSHE"
    context.bought = False
    log.info("=== 策略初始化 ===")


def handle_bar(context, bar_dict):
    stock = context.s1

    # 获取当前持仓
    position = context.portfolio.positions.get(stock)
    current_shares = position.quantity if position else 0

    # 如果没有持仓，买入
    if current_shares == 0 and not context.bought:
        bar = bar_dict[stock]
        # 计算可买股数
        cash = context.portfolio.cash
        price = bar.close
        shares = int(cash / price / 100) * 100  # 整手

        if shares >= 100:
            order_shares(stock, shares)
            context.bought = True
            log.info(f"买入 {stock} {shares}股 @ {price:.2f}")

    # 如果有持仓且是买入后的第二天，卖出
    elif current_shares > 0 and context.bought:
        bar = bar_dict[stock]
        order_target(stock, 0)
        log.info(f"卖出 {stock} {current_shares}股 @ {bar.close:.2f}")
        context.bought = False
