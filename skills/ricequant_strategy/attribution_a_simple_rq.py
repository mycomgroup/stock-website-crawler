# 策略A：纯小市值因子 - RiceQuant简化版本
# 选股：流通市值最小的股票
# 月度调仓


def init(context):
    context.stocks = []
    scheduler.run_monthly(rebalance, 1)


def rebalance(context, bar_dict):
    logger.info("月度调仓开始")

    # 获取所有股票
    all_stocks = all_instruments("CS")
    stock_list = list(all_stocks.order_book_id)[:500]  # 限制数量避免超时

    # 获取市值数据
    stock_caps = []

    for stock in stock_list:
        try:
            df = get_factor(stock, factor=["market_cap"])
            if df is not None and len(df) > 0:
                market_cap = df["market_cap"].iloc[0]
                if market_cap > 0:
                    stock_caps.append({"stock": stock, "market_cap": market_cap})
        except:
            pass

    if not stock_caps:
        logger.info("未获取到市值数据")
        return

    # 按市值排序
    stock_caps.sort(key=lambda x: x["market_cap"])

    # 选最小的前20只
    target_stocks = [item["stock"] for item in stock_caps[:20]]

    logger.info(f"选中{len(target_stocks)}只股票")

    # 清仓
    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks:
            order_target_percent(stock, 0)

    # 等权买入
    if target_stocks:
        weight = 1.0 / len(target_stocks)
        for stock in target_stocks:
            order_target_percent(stock, weight)

    context.stocks = target_stocks


def handle_bar(context, bar_dict):
    pass
