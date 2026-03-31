# 小市值成长股策略 - RiceQuant 版本
# 基于 JoinQuant 策略迁移，简化因子计算
# 测试日期: 2024-01-01 到 2024-12-31


def init(context):
    context.stock_num = 10
    context.limit_days = 20
    context.hold_list = []
    context.history_hold_list = []
    context.not_buy_again_list = []

    scheduler.run_monthly(rebalance, monthday=1)
    scheduler.run_daily(check_limit_up, time_rule=market_open(minute=30))


def get_stock_list(context):
    """获取股票池：小市值 + 成长性"""
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")
    stocks = list(set(hs300) | set(zz500))

    stocks = [s for s in stocks if not s.startswith("688")]

    logger.info(f"初始股票池: {len(stocks)}")

    return filter_by_market_cap_and_growth(stocks, context)


def filter_by_market_cap_and_growth(stocks, context):
    """按市值和成长性筛选"""
    from rqalpha.apis import *

    q = (
        query(
            fundamentals.eod_derivative_indicator.market_cap,
            fundamentals.financial_indicator.roe,
            fundamentals.financial_indicator.net_profit_growth_rate,
        )
        .filter(
            fundamentals.eod_derivative_indicator.order_book_id.in_(stocks),
            fundamentals.eod_derivative_indicator.market_cap > 0,
            fundamentals.financial_indicator.roe > 0.05,
        )
        .order_by(fundamentals.eod_derivative_indicator.market_cap.asc())
        .limit(30)
    )

    df = get_fundamentals(q, entry_date=context.now.date())

    if df is None or df.empty:
        logger.warning("未获取到财务数据")
        return []

    selected = df.index.get_level_values(1).tolist()[: context.stock_num]
    logger.info(f"筛选后股票数: {len(selected)}")

    return selected


def rebalance(context, bar_dict):
    """每月调仓"""
    target_list = get_stock_list(context)

    if not target_list:
        logger.warning("无目标股票")
        return

    current_positions = list(context.portfolio.positions.keys())

    for stock in current_positions:
        if stock not in target_list:
            order_target_value(stock, 0)
            logger.info(f"卖出: {stock}")

    if target_list:
        value_per_stock = context.portfolio.total_value / len(target_list)

        for stock in target_list:
            if stock not in context.portfolio.positions:
                try:
                    order_target_value(stock, value_per_stock)
                    logger.info(f"买入: {stock}, 金额: {value_per_stock:.0f}")
                except Exception as e:
                    logger.warning(f"买入 {stock} 失败: {e}")


def check_limit_up(context, bar_dict):
    """检查涨停股票"""
    positions = list(context.portfolio.positions.keys())

    for stock in positions:
        try:
            bars = history_bars(stock, 1, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) > 0:
                close = bars[-1]["close"]
                limit_up = bars[-1]["limit_up"]

                if abs(close - limit_up) < 0.01:
                    logger.info(f"{stock} 涨停")
        except:
            pass
