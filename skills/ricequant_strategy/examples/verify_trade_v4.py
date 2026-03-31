"""
验证交易 - RiceQuant 最终版本
参考 Golden Cross 策略的正确格式
"""


def init(context):
    context.s1 = "000001.XSHE"
    logger.info("=== 策略初始化 ===")


def handle_bar(context, bar_dict):
    stock = context.s1

    # 获取历史价格
    prices = history_bars(stock, 5, "1d", "close")

    if len(prices) < 5:
        return

    # 获取当前持仓数量
    cur_position = context.portfolio.positions[stock].quantity

    # 计算可买股数
    shares = context.portfolio.cash / bar_dict[stock].close

    # 如果没有持仓，买入
    if cur_position == 0:
        order_shares(stock, int(shares))
        logger.info(f"买入 {stock} {int(shares)}股 @ {bar_dict[stock].close:.2f}")

    # 如果有持仓，卖出
    elif cur_position > 0:
        order_target(stock, 0)
        logger.info(f"卖出 {stock} {cur_position}股 @ {bar_dict[stock].close:.2f}")
