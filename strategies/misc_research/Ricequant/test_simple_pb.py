# RiceQuant 简化测试策略
# 直接买入低 PB 股票


def init(context):
    context.benchmark = "000300.XSHG"
    scheduler.run_monthly(rebalance, tradingday=1)


def rebalance(context, bar_dict):
    # 获取沪深300成分股
    stocks = index_components("000300.XSHG")

    # 获取 PB 数据
    try:
        pb_data = get_factor(
            stocks,
            "pb_ratio",
            start_date=context.now.date(),
            end_date=context.now.date(),
        )
        if pb_data is None or pb_data.empty:
            logger.warning("No PB data")
            return
    except Exception as e:
        logger.warning(f"get_factor error: {e}")
        return

    # 选择 PB 最低的 10 只
    pb_series = pb_data.get("pb_ratio")
    if pb_series is None:
        return

    # 过滤无效值
    valid = pb_series[pb_series > 0].sort_values()
    if len(valid) < 5:
        return

    selected = valid.head(10).index.tolist()

    # 调仓
    for stock in context.portfolio.positions:
        if stock not in selected:
            order_target_value(stock, 0)

    # 买入
    total = context.portfolio.total_value
    per_stock = total / len(selected)

    for stock in selected:
        if stock in bar_dict and bar_dict[stock].is_trading:
            order_target_value(stock, per_stock)

    logger.info(f"Selected {len(selected)} stocks")
