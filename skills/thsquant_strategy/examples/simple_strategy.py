# 简单策略测试示例
# 同花顺量化平台策略模板


def initialize(context):
    """初始化函数"""
    g.stock = "000001.XSHE"  # 平安银行
    g.buy_price = 0
    g.sell_price = 0


def handle_data(context, data):
    """每日运行函数"""
    stock = g.stock

    # 获取当前价格
    current_price = data[stock].close

    # 简单的买入卖出逻辑
    if context.portfolio.positions.get(stock, 0) == 0:
        # 没有持仓，买入
        order_target_percent(stock, 1.0)
        log.info(f"买入 {stock}, 价格: {current_price}")
    else:
        # 有持仓，检查是否需要卖出
        if current_price > context.portfolio.starting_cash * 1.1:
            order_target_percent(stock, 0)
            log.info(f"卖出 {stock}, 价格: {current_price}")
