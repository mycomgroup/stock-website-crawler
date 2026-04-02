# 策略A：纯小市值因子 - RiceQuant策略编辑器版本
# 选股：流通市值最小的前10%
# 月度等权调仓
# 持仓20只


def init(context):
    context.month_count = 0
    context.last_month = None


def handle_bar(context, bar_dict):
    # 手动判断月份调仓（scheduler.run_monthly可能不触发）
    current_month = context.now.month

    if context.month_count == 0 or current_month != context.last_month:
        rebalance(context, bar_dict)
        context.last_month = current_month
        context.month_count += 1


def rebalance(context, bar_dict):
    stocks = all_instruments("CS")
    stock_ids = list(stocks.order_book_id)

    date_str = context.now.strftime("%Y-%m-%d")

    # RiceQuant API: get_factor获取市值
    factor_data = get_factor(stock_ids, ["market_cap"], date_str, date_str)

    if factor_data is None or len(factor_data) == 0:
        return

    # 按市值排序
    factor_data = factor_data.sort_values("market_cap", ascending=True)

    # 选最小的前10%，最多20只
    target_count = max(1, int(len(factor_data) * 0.1))
    target_stocks = list(factor_data.index)[: min(target_count, 20)]

    # 清仓不在目标池的股票
    for stock in context.portfolio.positions:
        if stock not in target_stocks:
            order_target_percent(stock, 0)

    # 等权买入目标股票
    if target_stocks:
        weight = 1.0 / len(target_stocks)
        for stock in target_stocks:
            order_target_percent(stock, weight)
