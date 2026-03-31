"""
验证交易 - RiceQuant 正确 API
关键发现：
1. order_target 不存在，要用 order_target_value(stock, 0) 清仓
2. order_target_quantity(stock, amount) 调整到目标数量
3. order_shares(stock, amount) 买入/卖出指定数量
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

    # 如果没有持仓，买入
    if cur_position == 0:
        # 计算可买股数
        shares = context.portfolio.cash / bar_dict[stock].close
        order_shares(stock, int(shares))
        logger.info(f"买入 {stock} {int(shares)}股 @ {bar_dict[stock].close:.2f}")

    # 如果有持仓，卖出（用 order_target_value 清仓）
    elif cur_position > 0:
        order_target_value(stock, 0)  # 正确的清仓方式
        logger.info(f"卖出 {stock} {cur_position}股 @ {bar_dict[stock].close:.2f}")
