# 双均线策略示例
# 同花顺量化平台策略模板


def initialize(context):
    """初始化函数"""
    # 设置基准
    set_benchmark("000001.SH")

    # 设置股票池
    g.stocks = ["000001.XSHE", "000002.XSHE", "600000.XSHG"]

    # 设置均线参数
    g.short_window = 5  # 短期均线
    g.long_window = 20  # 长期均线

    # 设置交易频率
    run_daily(rebalance, time="before_open")


def rebalance(context):
    """每日调仓函数"""
    for stock in g.stocks:
        # 获取历史价格
        prices = attribute_history(stock, g.long_window, "1d", ["close"])

        if len(prices["close"]) < g.long_window:
            continue

        # 计算均线
        short_ma = prices["close"][-g.short_window :].mean()
        long_ma = prices["close"][-g.long_window :].mean()

        # 获取当前持仓
        position = context.portfolio.positions.get(stock, 0)

        # 交易逻辑
        if short_ma > long_ma and position == 0:
            # 金叉买入
            order_target_percent(stock, 0.33)
            log.info(
                f"金叉买入 {stock}, 短期均线: {short_ma:.2f}, 长期均线: {long_ma:.2f}"
            )
        elif short_ma < long_ma and position > 0:
            # 死叉卖出
            order_target_percent(stock, 0)
            log.info(
                f"死叉卖出 {stock}, 短期均线: {short_ma:.2f}, 长期均线: {long_ma:.2f}"
            )


def handle_data(context, data):
    """分钟线运行函数（如果使用分钟线）"""
    pass
