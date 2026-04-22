# RiceQuant 策略编辑器版本 - 股息率价值策略
# 完整回测版本

from rqalpha import *
from rqalpha.apis import *


def init(context):
    """策略初始化"""
    context.stock_num = 20
    context.pe_threshold = 20
    context.pb_threshold = 2.0
    context.trade_count = 0

    set_benchmark("000300.XSHG")

    set_order_cost(
        OrderCost(open_commission=0.0003, close_commission=0.0003, close_tax=0.001),
        type="stock",
    )

    set_slippage(FixedSlippage(0.00))

    scheduler.run_monthly(rebalance, tradingday=1)


def rebalance(context, bar_dict):
    """每月调仓"""
    stocks = get_stock_pool(context)

    if not stocks:
        return

    selected = filter_by_valuation(stocks, context)

    if not selected:
        return

    target_stocks = selected[: context.stock_num]
    adjust_positions(target_stocks, context, bar_dict)

    context.trade_count += 1
    logger.info(f"第 {context.trade_count} 次调仓，选中 {len(target_stocks)} 只股票")


def get_stock_pool(context):
    """获取股票池"""
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")

    stocks = list(set(hs300) | set(zz500))
    stocks = [s for s in stocks if not s.startswith("688")]
    stocks = [s for s in stocks if not s.startswith(("4", "8"))]

    return stocks


def filter_by_valuation(stocks, context):
    """按估值筛选"""
    try:
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
            return []

        return df.index.get_level_values(1).tolist()

    except Exception as e:
        logger.error(f"估值筛选错误: {e}")
        return []


def adjust_positions(target_stocks, context, bar_dict):
    """调整持仓"""
    current_positions = list(context.portfolio.positions.keys())

    for stock in current_positions:
        if stock not in target_stocks:
            order_target_percent(stock, 0)

    if target_stocks:
        weight = 1.0 / len(target_stocks)
        for stock in target_stocks:
            if stock not in current_positions:
                if stock in bar_dict and bar_dict[stock].is_trading:
                    order_target_percent(stock, weight)


__config__ = {
    "base": {
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "frequency": "1d",
        "accounts": {"stock": 1000000},
    },
    "extra": {
        "log_level": "info",
    },
    "mod": {
        "sys_progress": {
            "enabled": True,
            "show": True,
        }
    },
}
