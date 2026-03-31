# 股息率价值策略 - RiceQuant 版本
# 高股息 + 低PE + 低PB 策略
# 测试日期: 2024-01-01 到 2024-12-31


def init(context):
    context.stock_num = 20
    context.dividend_threshold = 0.03
    context.pe_threshold = 20
    context.pb_threshold = 2.0

    scheduler.run_monthly(rebalance, monthday=1)


def get_stock_list(context):
    """获取股票池：高股息 + 低估值"""
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")
    stocks = list(set(hs300) | set(zz500))

    stocks = [s for s in stocks if not s.startswith("688")]

    logger.info(f"初始股票池: {len(stocks)}")

    return filter_dividend_and_valuation(stocks, context)


def filter_dividend_and_valuation(stocks, context):
    """按股息率和估值筛选"""
    from rqalpha.apis import *

    q = (
        query(
            fundamentals.eod_derivative_indicator.pe_ratio,
            fundamentals.eod_derivative_indicator.pb_ratio,
        )
        .filter(
            fundamentals.eod_derivative_indicator.order_book_id.in_(stocks),
            fundamentals.eod_derivative_indicator.pe_ratio > 0,
            fundamentals.eod_derivative_indicator.pe_ratio < context.pe_threshold,
            fundamentals.eod_derivative_indicator.pb_ratio > 0,
            fundamentals.eod_derivative_indicator.pb_ratio < context.pb_threshold,
        )
        .order_by(fundamentals.eod_derivative_indicator.pe_ratio.asc())
        .limit(50)
    )

    df = get_fundamentals(q, entry_date=context.now.date())

    if df is None or df.empty:
        logger.warning("未获取到估值数据")
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
                    logger.info(f"买入: {stock}")
                except Exception as e:
                    logger.warning(f"买入 {stock} 失败: {e}")
