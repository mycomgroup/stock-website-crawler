# RiceQuant 策略编辑器版本 - 完整回测策略
# 直接在 RiceQuant 策略编辑器中使用

from rqalpha import *
from rqalpha.apis import *


def init(context):
    """策略初始化"""
    # 设置策略参数
    context.stock_num = 10  # 持仓股票数量
    context.trade_count = 0

    # 设置基准
    set_benchmark("000300.XSHG")

    # 设置手续费
    set_order_cost(
        OrderCost(
            open_commission=0.0003,  # 开仓佣金 0.03%
            close_commission=0.0003,  # 平仓佣金 0.03%
            close_tax=0.001,  # 平仓印花税 0.1%
        ),
        type="stock",
    )

    # 设置滑点
    set_slippage(FixedSlippage(0.00))

    # 每月第一个交易日调仓
    scheduler.run_monthly(rebalance, tradingday=1)


def rebalance(context, bar_dict):
    """每月调仓"""
    # 1. 获取股票池
    stocks = get_stock_pool(context)

    if not stocks:
        logger.info("未找到符合条件的股票")
        return

    # 2. 按市值排序，选择小市值股票
    selected = filter_by_market_cap(stocks, context)

    if not selected:
        logger.info("筛选后无股票")
        return

    # 限制数量
    target_stocks = selected[: context.stock_num]

    # 3. 调整持仓
    adjust_positions(target_stocks, context, bar_dict)

    context.trade_count += 1
    logger.info(f"第 {context.trade_count} 次调仓，选中 {len(target_stocks)} 只股票")


def get_stock_pool(context):
    """获取股票池"""
    # 获取沪深300成分股
    hs300 = index_components("000300.XSHG")
    # 获取中证500成分股
    zz500 = index_components("000905.XSHG")

    # 合并去重
    stocks = list(set(hs300) | set(zz500))

    # 排除科创板
    stocks = [s for s in stocks if not s.startswith("688")]
    # 排除北交所
    stocks = [s for s in stocks if not s.startswith(("4", "8"))]

    logger.info(f"初始股票池: {len(stocks)} 只")
    return stocks


def filter_by_market_cap(stocks, context):
    """按市值筛选小市值股票"""
    try:
        # 使用财务数据查询
        q = (
            query(fundamentals.eod_derivative_indicator.market_cap)
            .filter(
                fundamentals.eod_derivative_indicator.order_book_id.in_(stocks),
                fundamentals.eod_derivative_indicator.market_cap > 0,
            )
            .order_by(fundamentals.eod_derivative_indicator.market_cap.asc())
            .limit(30)
        )

        df = get_fundamentals(q, entry_date=context.now.date())

        if df is None or df.empty:
            logger.warning("未获取到市值数据")
            return []

        # 提取股票代码
        selected = df.index.get_level_values(1).tolist()
        logger.info(f"市值筛选: {len(selected)} 只")

        return selected

    except Exception as e:
        logger.error(f"市值筛选错误: {e}")
        return []


def adjust_positions(target_stocks, context, bar_dict):
    """调整持仓"""
    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())

    # 卖出不在目标列表中的股票
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_percent(stock, 0)
            logger.info(f"卖出: {stock}")

    # 买入目标股票
    if target_stocks:
        # 等权重配置
        weight = 1.0 / len(target_stocks)

        for stock in target_stocks:
            if stock not in current_positions:
                # 检查是否可交易
                if is_tradable(stock, bar_dict):
                    order_target_percent(stock, weight)
                    logger.info(f"买入: {stock}, 权重: {weight:.2%}")


def is_tradable(stock, bar_dict):
    """检查股票是否可交易"""
    if stock not in bar_dict:
        return False

    bar = bar_dict[stock]

    # 检查是否停牌
    if not bar.is_trading:
        return False

    # 检查是否涨跌停
    if bar.close >= bar.limit_up or bar.close <= bar.limit_down:
        return False

    return True


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
