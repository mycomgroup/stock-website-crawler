from jqdata import *
import pandas as pd
import numpy as np


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.market_breadth_bins = {
        "极弱": (0, 0.15),
        "弱": (0.15, 0.25),
        "中": (0.25, 0.35),
        "强": (0.35, 1.0),
    }

    g.sentiment_bins = {
        "冰点": (0, 30),
        "启动": (30, 50),
        "发酵": (50, 80),
        "高潮": (80, 9999),
    }

    g.results = {
        "no_filter": {"returns": [], "drawdowns": []},
        "breadth_filtered": {"returns": [], "drawdowns": []},
        "sentiment_filtered": {"returns": [], "drawdowns": []},
        "both_filtered": {"returns": [], "drawdowns": []},
    }

    g.state_results = {}
    for breadth_state in g.market_breadth_bins.keys():
        for sentiment_state in g.sentiment_bins.keys():
            key = f"{breadth_state}_{sentiment_state}"
            g.state_results[key] = {"returns": [], "count": 0}

    g.trade_log = []
    g.position_value = 0
    g.max_value = 0
    g.drawdown = 0

    g.hs300_stocks = get_hs300_stocks()

    set_benchmark("000300.XSHG")

    run_daily(record_state, time="09:00")
    run_daily(select_stocks, time="09:25")
    run_daily(buy_stocks, time="09:35")
    run_daily(sell_stocks, time="14:50")
    run_daily(record_end, time="15:00")


def get_hs300_stocks():
    return get_index_stocks("000300.XSHG")


def record_state(context):
    date = context.current_dt.strftime("%Y-%m-%d")
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    hs300_stocks = g.hs300_stocks

    prices = get_price(
        hs300_stocks,
        end_date=prev_date,
        count=20,
        fields=["close"],
        panel=False,
        fill_paused=False,
    )

    if prices.empty:
        g.market_breadth = 0
    else:
        above_ma20 = 0
        total = 0
        for stock in hs300_stocks:
            stock_prices = prices[prices["code"] == stock]["close"]
            if len(stock_prices) >= 20:
                ma20 = stock_prices.mean()
                last_close = stock_prices.iloc[-1]
                if last_close >= ma20:
                    above_ma20 += 1
                total += 1

        g.market_breadth = above_ma20 / max(total, 1) if total > 0 else 0

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

    df = get_price(
        all_stocks,
        end_date=prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()

    zt_count = len(df[df["close"] == df["high_limit"]])
    g.zt_count = zt_count

    g.breadth_state = get_state_name(g.market_breadth, g.market_breadth_bins)
    g.sentiment_state = get_state_name(g.zt_count, g.sentiment_bins)

    g.breadth_filter = g.market_breadth >= 0.25
    g.sentiment_filter = g.zt_count >= 50

    g.date = date
    log.info(
        f"日期:{date} 广度:{g.market_breadth:.2%}({g.breadth_state}) 涨停:{g.zt_count}({g.sentiment_state})"
    )


def get_state_name(value, bins):
    for name, (low, high) in bins.items():
        if low <= value < high:
            return name
    return list(bins.keys())[-1]


def select_stocks(context):
    g.target = []

    date = context.current_dt.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

    q = query(valuation.code, valuation.circulating_market_cap).filter(
        valuation.circulating_market_cap >= 5, valuation.circulating_market_cap <= 30
    )
    df = get_fundamentals(q, date=date)
    smallcap_stocks = list(df["code"])

    g.target = smallcap_stocks[:50]


def buy_stocks(context):
    if not g.target:
        return

    current_data = get_current_data()

    buy_no_filter = True
    buy_breadth = g.breadth_filter
    buy_sentiment = g.sentiment_filter
    buy_both = g.breadth_filter and g.sentiment_filter

    filter_modes = []
    if buy_no_filter:
        filter_modes.append("no_filter")
    if buy_breadth:
        filter_modes.append("breadth_filtered")
    if buy_sentiment:
        filter_modes.append("sentiment_filtered")
    if buy_both:
        filter_modes.append("both_filtered")

    for mode in filter_modes:
        stocks_to_buy = g.target[:10]

        if len(stocks_to_buy) == 0:
            continue

        value_per_stock = context.portfolio.total_value / 10

        for stock in stocks_to_buy:
            if stock not in current_data:
                continue

            cd = current_data[stock]
            if cd.paused:
                continue

            price = cd.last_price
            if price <= 0:
                continue

            shares = int(value_per_stock / price / 100) * 100
            if shares >= 100:
                order(stock, shares)

                g.trade_log.append(
                    {
                        "date": g.date,
                        "mode": mode,
                        "stock": stock,
                        "price": price,
                        "shares": shares,
                        "breadth_state": g.breadth_state,
                        "sentiment_state": g.sentiment_state,
                        "market_breadth": g.market_breadth,
                        "zt_count": g.zt_count,
                    }
                )

                key = f"{g.breadth_state}_{g.sentiment_state}"
                g.state_results[key]["count"] += 1


def sell_stocks(context):
    current_data = get_current_data()

    for stock in list(context.portfolio.positions):
        pos = context.portfolio.positions[stock]
        if pos.closeable_amount > 0:
            cd = current_data[stock]
            pnl = (cd.last_price - pos.avg_cost) / pos.avg_cost * 100

            for trade in g.trade_log:
                if trade["stock"] == stock and trade["date"] == g.date:
                    mode = trade["mode"]
                    g.results[mode]["returns"].append(pnl)

                    key = f"{trade['breadth_state']}_{trade['sentiment_state']}"
                    g.state_results[key]["returns"].append(pnl)

            order_target(stock, 0)


def record_end(context):
    current_value = context.portfolio.total_value
    g.max_value = max(g.max_value, current_value)

    if g.max_value > 0:
        current_dd = (g.max_value - current_value) / g.max_value * 100
        g.drawdown = max(g.drawdown, current_dd)


def after_trading_end(context):
    if g.trade_log:
        output_results()


def output_results():
    log.info("\n========== 状态分层结果 ==========")

    log.info("\n【市场广度分层】")
    breadth_summary = {}
    for breadth_state in g.market_breadth_bins.keys():
        returns = []
        count = 0
        for key, data in g.state_results.items():
            if key.startswith(breadth_state):
                returns.extend(data["returns"])
                count += data["count"]

        if returns:
            avg_return = np.mean(returns)
            breadth_summary[breadth_state] = {"avg_return": avg_return, "count": count}
            log.info(f"{breadth_state}: 平均收益={avg_return:.2f}%, 交易次数={count}")

    log.info("\n【情绪分层】")
    sentiment_summary = {}
    for sentiment_state in g.sentiment_bins.keys():
        returns = []
        count = 0
        for key, data in g.state_results.items():
            if key.endswith(sentiment_state):
                returns.extend(data["returns"])
                count += data["count"]

        if returns:
            avg_return = np.mean(returns)
            sentiment_summary[sentiment_state] = {
                "avg_return": avg_return,
                "count": count,
            }
            log.info(f"{sentiment_state}: 平均收益={avg_return:.2f}%, 交易次数={count}")

    log.info("\n【状态过滤效果对比】")
    for mode in [
        "no_filter",
        "breadth_filtered",
        "sentiment_filtered",
        "both_filtered",
    ]:
        returns = g.results[mode]["returns"]
        if returns:
            avg_return = np.mean(returns)
            log.info(f"{mode}: 平均收益={avg_return:.2f}%, 交易次数={len(returns)}")

    log.info(f"\n最大回撤: {g.drawdown:.2f}%")

    log.info("\n========== 交易明细 ==========")
    for trade in g.trade_log[-20:]:
        log.info(
            f"{trade['date']} {trade['mode']} {trade['stock']} "
            f"广度:{trade['breadth_state']} 涨停:{trade['sentiment_state']}"
        )
