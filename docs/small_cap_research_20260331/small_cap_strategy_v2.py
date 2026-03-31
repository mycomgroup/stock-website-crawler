# 国九条小市值策略 - JoinQuant版
# 简化版，确保可运行

from jqdata import *
import numpy as np


def initialize(context):
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)

    g.stock_num = 10
    g.min_cap = 10
    g.max_cap = 300
    g.stop_loss = -0.09
    g.pass_months = [1, 4]
    g.etf = "511880.XSHG"

    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    set_slippage(FixedSlippage(0.02))

    run_daily(stop_loss_check, "14:30")
    run_weekly(rebalance, 1, "10:00")


def stop_loss_check(context):
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.price < pos.avg_cost * (1 + g.stop_loss):
            order_target_value(stock, 0)
            log.info("止损: %s" % stock)


def rebalance(context):
    today = context.current_dt

    # 空仓月份
    if today.month in g.pass_months:
        order_target_value(g.etf, context.portfolio.total_value)
        log.info("空仓月份，持有ETF")
        return

    # 获取股票池
    stocks = get_stock_pool(context)

    if len(stocks) == 0:
        return

    # 选股
    selected = select_stocks(context, stocks, g.stock_num)

    # 卖出
    for stock in list(context.portfolio.positions.keys()):
        if stock not in selected and stock != g.etf:
            order_target_value(stock, 0)

    # 买入
    if len(selected) > 0:
        value = context.portfolio.total_value / len(selected)
        for stock in selected:
            order_target_value(stock, value)
        log.info("买入: %s" % selected[:5])


def get_stock_pool(context):
    # 获取上证+深证成分股
    scu = get_index_stocks("000001.XSHG") + get_index_stocks("399106.XSHE")

    # 过滤ST、停牌
    current_data = get_current_data()
    scu = [
        s
        for s in scu
        if not (
            current_data[s].paused
            or current_data[s].is_st
            or "ST" in current_data[s].name
            or "*" in current_data[s].name
            or "退" in current_data[s].name
        )
    ]

    # 过滤次新股
    scu = [
        s
        for s in scu
        if (context.previous_date - get_security_info(s).start_date).days > 365
    ]

    # 市值+财务筛选
    q = (
        query(valuation.code, valuation.market_cap)
        .filter(
            valuation.code.in_(scu),
            valuation.market_cap.between(g.min_cap, g.max_cap),
            income.net_profit > 0,
            income.operating_revenue > 1e8,
        )
        .order_by(valuation.market_cap.asc())
    )

    df = get_fundamentals(q, date=context.previous_date)
    return list(df["code"]) if df is not None and len(df) > 0 else []


def select_stocks(context, stocks, num):
    results = []

    for stock in stocks[: min(100, len(stocks))]:
        try:
            # 获取历史价格
            h = history(60, unit="1d", field="close", security_list=[stock], df=True)

            if h is None or len(h) < 40:
                continue

            close = h[stock].values

            # 计算因子
            momentum = (close[-1] / close[-21] - 1) * 100 if len(close) >= 21 else 0
            ma20 = np.mean(close[-20:])
            ma_dev = (close[-1] / ma20 - 1) * 100

            high20 = np.max(close[-20:])
            low20 = np.min(close[-20:])
            price_pos = (
                (close[-1] - low20) / (high20 - low20) if high20 != low20 else 0.5
            )

            # 评分
            score = 0
            if momentum > 10:
                score += 3
            elif momentum > 5:
                score += 2
            elif momentum > 0:
                score += 1
            elif momentum < -10:
                score -= 2

            if -5 < ma_dev < 10:
                score += 2

            if 0.3 < price_pos < 0.7:
                score += 1

            results.append({"code": stock, "score": score})

        except Exception as e:
            continue

    results.sort(key=lambda x: -x["score"])
    return [r["code"] for r in results[:num]]
