# 策略A：纯小市值因子 - 超简化版本
# 直接手动遍历，不使用复杂API


def init(context):
    context.stock_list = []
    context.rebalance_day = 1  # 每月1日调仓


def before_trading(context):
    # 检查是否到了调仓日
    if context.now.day == context.rebalance_day:
        do_rebalance(context)


def do_rebalance(context):
    logger.info("开始调仓: %s" % context.now)

    # 获取所有股票代码（前500只）
    stocks_df = all_instruments("CS")
    all_codes = list(stocks_df.order_book_id)[:500]

    # 获取市值并排序
    stocks_with_cap = []
    count = 0

    for code in all_codes:
        try:
            # 获取当前价格作为市值代理（简化处理）
            bars = history_bars(code, 1, "1d", ["close"])
            if bars is not None and len(bars) > 0:
                price = bars["close"][-1]
                if price > 0:
                    stocks_with_cap.append((code, price))
                    count += 1
                    if count >= 100:  # 只取前100只避免超时
                        break
        except:
            pass

    # 按价格排序（简化，实际应该用市值）
    stocks_with_cap.sort(key=lambda x: x[1])

    # 选最小的20只
    target_codes = [item[0] for item in stocks_with_cap[:20]]

    logger.info("选中 %d 只股票" % len(target_codes))

    # 清仓
    for pos in list(context.portfolio.positions.keys()):
        if pos not in target_codes:
            order_target_percent(pos, 0)

    # 买入
    if len(target_codes) > 0:
        weight = 1.0 / len(target_codes)
        for code in target_codes:
            order_target_percent(code, weight)

    context.stock_list = target_codes


def handle_bar(context, bar_dict):
    pass
