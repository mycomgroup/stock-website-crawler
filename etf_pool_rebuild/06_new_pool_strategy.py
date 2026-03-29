# 初始化函数，设定基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark("000300.XSHG")
    # 开启动态复权模式(真实价格)
    set_option("use_real_price", True)
    # 输出内容到日志 log.info()
    log.info("初始函数开始运行且全局只运行一次")

    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    # ---- 新池定义 (v2.0) - 纯 A 股 ----
    context.pool = {
        # 宽基
        "沪深300ETF": "510300.XSHG",
        "中证500ETF": "510500.XSHG",
        "创业板ETF": "159915.XSHE",
        "科创50ETF": "588000.XSHG",
        "中证1000ETF": "512100.XSHG",
        # 行业
        "医疗ETF": "512170.XSHG",
        "消费ETF": "159928.XSHE",
        "新能源ETF": "516160.XSHG",
        "半导体ETF": "512480.XSHG",
        "军工ETF": "512660.XSHG",
        "银行ETF": "512800.XSHG",
        "计算机ETF": "512720.XSHG",
    }

    # 动量参数
    context.mom_window = 20  # 动量窗口
    context.hold_days = 10  # 持有周期
    context.top_n = 3  # 持仓数量
    context.rebalance_flag = False
    context.prev_holdings = []

    # 运行频率（每天开盘前）
    run_daily(before_market_open, time="09:00", reference_security="000300.XSHG")
    run_daily(market_open, time="09:30", reference_security="000300.XSHG")


# 开盘前运行函数
def before_market_open(context):
    log.info("开盘前运行")
    context.rebalance_flag = False

    # 判断是否是调仓日
    if context.run_days % context.hold_days == 0:
        context.rebalance_flag = True
        log.info("今天是调仓日")


# 开盘时运行函数
def market_open(context):
    if not context.rebalance_flag:
        return

    log.info("执行调仓")

    # 计算动量
    codes = list(context.pool.values())
    momentum = {}

    for name, code in context.pool.items():
        try:
            # 获取动量窗口期的价格
            prices = attribute_history(
                code, context.mom_window + 1, "1d", ["close"], skip_paused=True
            )
            if len(prices) >= context.mom_window + 1:
                mom = (prices["close"].iloc[-1] / prices["close"].iloc[0]) - 1
                momentum[name] = mom
        except:
            continue

    if len(momentum) == 0:
        log.info("没有获取到动量数据")
        return

    # 按动量排序，选出 top_n
    sorted_momentum = sorted(momentum.items(), key=lambda x: x[1], reverse=True)
    selected = [context.pool[name] for name, _ in sorted_momentum[: context.top_n]]
    selected_names = [name for name, _ in sorted_momentum[: context.top_n]]

    log.info("选中ETF: %s" % str(selected_names))

    # 调仓
    adjust_portfolio(context, selected)

    context.prev_holdings = selected


def adjust_portfolio(context, target_stocks):
    """调整持仓"""
    # 获取当前持仓
    hold_list = list(context.portfolio.positions.keys())

    # 卖出不在目标列表中的股票
    for stock in hold_list:
        if stock not in target_stocks:
            order_target(stock, 0)
            log.info("卖出: %s" % stock)

    # 买入目标股票
    if len(target_stocks) == 0:
        return

    # 等权分配
    position_per_stock = context.portfolio.total_value / len(target_stocks)

    for stock in target_stocks:
        order_target_value(stock, position_per_stock)
        log.info("买入: %s, 金额: %.2f" % (stock, position_per_stock))
