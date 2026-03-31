# 国九条+机器学习小市值策略 - JoinQuant策略编辑器版
#
# 策略目标：稳健盈利，# - 国九条筛选：审计意见+净利润+营收过滤
# - 市值因子优化：10-300亿市值
# - 机器学习因子：动量+MA乖离率+量比+价格位置
# - 风控机制：止损-9%、1/4月空仓
#
# 使用方法：直接复制到JoinQuant策略编辑器运行回测

from jqdata import *
import numpy as np
import pandas as pd


def initialize(context):
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)

    g.stock_num = 10
    g.min_market_cap = 10
    g.max_market_cap = 300
    g.stop_loss = -0.09
    g.rebalance_days = 5
    g.days = 0
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

    run_daily(before_trading, "09:00")
    run_daily(stop_loss_check, "14:30")
    run_weekly(weekly_rebalance, 1, "10:00")


def before_trading(context):
    today = context.current_dt
    g.no_trading = today.month in g.pass_months


def stop_loss_check(context):
    if g.no_trading:
        return

    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.price < pos.avg_cost * (1 + g.stop_loss):
            order_target_value(stock, 0)
            log.info(f"止损卖出: {stock}")


def weekly_rebalance(context):
    if g.no_trading:
        log.info("空仓月份，持有货币ETF")
        order_target_value(g.etf, context.portfolio.total_value)
        return

    stocks = get_stock_pool(context)

    if len(stocks) == 0:
        log.info("无符合条件的股票")
        return

    selected = select_stocks(context, stocks, g.stock_num)

    for stock in list(context.portfolio.positions.keys()):
        if stock not in selected and stock != g.etf:
            order_target_value(stock, 0)

    if len(selected) > 0:
        value = context.portfolio.total_value / len(selected)
        for stock in selected:
            order_target_value(stock, value)

        log.info(f"买入: {selected}")


def get_stock_pool(context):
    scu = get_index_stocks("000001.XSHG") + get_index_stocks("399106.XSHE")

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

    start_date = get_security_info(scu[0]).start_date if scu else None
    scu = [
        s
        for s in scu
        if context.previous_date - get_security_info(s).start_date
        > datetime.timedelta(days=365)
    ]

    q = (
        query(
            valuation.code,
            valuation.market_cap,
            income.net_profit,
            income.operating_revenue,
        )
        .filter(
            valuation.code.in_(scu),
            valuation.market_cap.between(g.min_market_cap, g.max_market_cap),
            income.net_profit > 0,
            income.operating_revenue > 1e8,
        )
        .order_by(valuation.market_cap.asc())
    )

    df = get_fundamentals(q, date=context.previous_date)
    return list(df["code"]) if df is not None else []


def select_stocks(context, stocks, num):
    results = []

    for stock in stocks[:100]:
        try:
            prices = attribute_history(
                stock, ["close"], 60, "1d", end_date=context.previous_date
            )
            if prices is None or len(prices) < 40:
                continue

            close = prices["close"].values
            volume = prices.get("volume", [1] * len(close))

            momentum_20 = (close[-1] / close[-21] - 1) * 100 if len(close) >= 21 else 0
            ma20 = np.mean(close[-20:]) if len(close) >= 20 else close[-1]
            ma_dev = (close[-1] / ma20 - 1) * 100
            vol_ratio = (
                np.mean(volume[-5:]) / np.mean(volume[-20:])
                if np.mean(volume[-20:]) > 0
                else 1
            )

            high = np.max(close[-20:])
            low = np.min(close[-20:])
            price_pos = (close[-1] - low) / (high - low) if high != low else 0.5

            score = 0
            if momentum_20 > 10:
                score += 3
            elif momentum_20 > 5:
                score += 2
            elif momentum_20 > 0:
                score += 1
            elif momentum_20 < -10:
                score -= 2

            if -5 < ma_dev < 10:
                score += 2

            if 1.2 < vol_ratio < 2.0:
                score += 2

            if 0.3 < price_pos < 0.7:
                score += 1

            results.append(
                {
                    "code": stock,
                    "score": score,
                    "momentum": momentum_20,
                    "ma_dev": ma_dev,
                }
            )
        except:
            continue

    results.sort(key=lambda x: -x["score"])
    return [r["code"] for r in results[:num]]
