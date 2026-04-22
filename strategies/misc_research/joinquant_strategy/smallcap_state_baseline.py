from jqdata import *
import json


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.trade_records = []
    g.daily_records = []

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

    g.position_size = 10

    run_daily(record_state, time="09:00")
    run_daily(select_and_buy, time="09:35")
    run_daily(sell_all, time="14:50")

    set_benchmark("000300.XSHG")


def record_state(context):
    date = context.current_dt.strftime("%Y-%m-%d")
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    hs300_stocks = get_index_stocks("000300.XSHG")

    above_ma20 = 0
    total = 0

    for stock in hs300_stocks:
        try:
            prices = get_price(
                stock,
                end_date=prev_date,
                count=20,
                fields=["close"],
                panel=False,
                fill_paused=False,
            )
            if len(prices) >= 20:
                ma20 = prices["close"].mean()
                last_close = prices["close"].iloc[-1]
                if last_close >= ma20:
                    above_ma20 += 1
                total += 1
        except:
            continue

    market_breadth = above_ma20 / max(total, 1)

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

    try:
        df = get_price(
            all_stocks,
            end_date=prev_date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
        )
        if not df.empty:
            df = df.dropna()
            zt_count = len(df[df["close"] == df["high_limit"]])
        else:
            zt_count = 0
    except:
        zt_count = 0

    breadth_state = get_state_name(market_breadth, g.market_breadth_bins)
    sentiment_state = get_state_name(zt_count, g.sentiment_bins)

    g.current_state = {
        "date": date,
        "market_breadth": market_breadth,
        "breadth_state": breadth_state,
        "zt_count": zt_count,
        "sentiment_state": sentiment_state,
    }

    log.info(
        f"{date}: 广度={market_breadth:.1%}({breadth_state}), 涨停={zt_count}({sentiment_state})"
    )


def get_state_name(value, bins):
    for name, (low, high) in bins.items():
        if low <= value < high:
            return name
    return list(bins.keys())[-1]


def select_and_buy(context):
    date = context.current_dt.strftime("%Y-%m-%d")

    q = query(valuation.code, valuation.circulating_market_cap).filter(
        valuation.circulating_market_cap >= 5, valuation.circulating_market_cap <= 30
    )

    df = get_fundamentals(q, date=date)

    if df.empty:
        return

    smallcap_stocks = list(df["code"])[: g.position_size]

    current_data = get_current_data()

    buy_stocks = []
    for stock in smallcap_stocks:
        if stock in current_data:
            cd = current_data[stock]
            if not cd.paused and cd.last_price > 0:
                buy_stocks.append(stock)

    if not buy_stocks:
        return

    cash_per_stock = context.portfolio.available_cash / len(buy_stocks)

    g.buy_prices = {}

    for stock in buy_stocks:
        cd = current_data[stock]
        price = cd.last_price
        shares = int(cash_per_stock / price / 100) * 100

        if shares >= 100:
            order(stock, shares)
            g.buy_prices[stock] = price

            g.trade_records.append(
                {
                    "buy_date": date,
                    "stock": stock,
                    "buy_price": price,
                    "shares": shares,
                    "market_breadth": g.current_state["market_breadth"],
                    "breadth_state": g.current_state["breadth_state"],
                    "zt_count": g.current_state["zt_count"],
                    "sentiment_state": g.current_state["sentiment_state"],
                }
            )


def sell_all(context):
    date = context.current_dt.strftime("%Y-%m-%d")
    current_data = get_current_data()

    for stock in list(context.portfolio.positions):
        pos = context.portfolio.positions[stock]
        if pos.closeable_amount > 0:
            sell_price = current_data[stock].last_price
            pnl = (sell_price - pos.avg_cost) / pos.avg_cost * 100

            for record in g.trade_records:
                if record["buy_date"] == date and record["stock"] == stock:
                    record["sell_price"] = sell_price
                    record["pnl"] = pnl
                    record["sell_date"] = date

            order_target(stock, 0)

    portfolio_value = context.portfolio.total_value
    g.daily_records.append(
        {
            "date": date,
            "portfolio_value": portfolio_value,
            "market_breadth": g.current_state["market_breadth"],
            "breadth_state": g.current_state["breadth_state"],
            "zt_count": g.current_state["zt_count"],
            "sentiment_state": g.current_state["sentiment_state"],
        }
    )


def on_end(context):
    log.info("\n" + "=" * 60)
    log.info("小市值状态分层基线研究结果")
    log.info("=" * 60)

    if not g.trade_records:
        log.info("没有交易记录")
        return

    log.info("\n【总体概况】")
    total_trades = len(g.trade_records)
    total_pnl = sum([r["pnl"] for r in g.trade_records])
    avg_pnl = total_pnl / total_trades
    win_count = sum([1 for r in g.trade_records if r["pnl"] > 0])
    win_rate = win_count / total_trades * 100

    log.info(f"总交易次数: {total_trades}")
    log.info(f"平均单笔收益: {avg_pnl:.2f}%")
    log.info(f"胜率: {win_rate:.1f}%")

    log.info("\n【市场广度分层结果】")
    breadth_groups = {}
    for state in ["极弱", "弱", "中", "强"]:
        trades = [r for r in g.trade_records if r["breadth_state"] == state]
        if trades:
            avg_pnl_state = sum([r["pnl"] for r in trades]) / len(trades)
            win_rate_state = (
                sum([1 for r in trades if r["pnl"] > 0]) / len(trades) * 100
            )
            breadth_groups[state] = {
                "count": len(trades),
                "avg_pnl": avg_pnl_state,
                "win_rate": win_rate_state,
            }
            log.info(
                f"{state}: 平均收益={avg_pnl_state:.2f}%, 胜率={win_rate_state:.1f}%, 交易数={len(trades)}"
            )

    log.info("\n【情绪分层结果】")
    sentiment_groups = {}
    for state in ["冰点", "启动", "发酵", "高潮"]:
        trades = [r for r in g.trade_records if r["sentiment_state"] == state]
        if trades:
            avg_pnl_state = sum([r["pnl"] for r in trades]) / len(trades)
            win_rate_state = (
                sum([1 for r in trades if r["pnl"] > 0]) / len(trades) * 100
            )
            sentiment_groups[state] = {
                "count": len(trades),
                "avg_pnl": avg_pnl_state,
                "win_rate": win_rate_state,
            }
            log.info(
                f"{state}: 平均收益={avg_pnl_state:.2f}%, 胜率={win_rate_state:.1f}%, 交易数={len(trades)}"
            )

    log.info("\n【状态过滤效果对比】")

    no_filter_avg = avg_pnl
    log.info(f"无过滤: 平均收益={no_filter_avg:.2f}%, 交易数={total_trades}")

    breadth_filter_trades = [r for r in g.trade_records if r["market_breadth"] >= 0.25]
    if breadth_filter_trades:
        bf_avg = sum([r["pnl"] for r in breadth_filter_trades]) / len(
            breadth_filter_trades
        )
        bf_improve = bf_avg - no_filter_avg
        log.info(
            f"广度过滤(≥25%): 平均收益={bf_avg:.2f}%, 交易数={len(breadth_filter_trades)}, 提升={bf_improve:.2f}%"
        )

    sentiment_filter_trades = [r for r in g.trade_records if r["zt_count"] >= 50]
    if sentiment_filter_trades:
        sf_avg = sum([r["pnl"] for r in sentiment_filter_trades]) / len(
            sentiment_filter_trades
        )
        sf_improve = sf_avg - no_filter_avg
        log.info(
            f"情绪过滤(涨停≥50): 平均收益={sf_avg:.2f}%, 交易数={len(sentiment_filter_trades)}, 提升={sf_improve:.2f}%"
        )

    both_filter_trades = [
        r
        for r in g.trade_records
        if r["market_breadth"] >= 0.25 and r["zt_count"] >= 50
    ]
    if both_filter_trades:
        both_avg = sum([r["pnl"] for r in both_filter_trades]) / len(both_filter_trades)
        both_improve = both_avg - no_filter_avg
        log.info(
            f"双过滤: 平均收益={both_avg:.2f}%, 交易数={len(both_filter_trades)}, 提升={both_improve:.2f}%"
        )

    log.info("\n【极弱市场详细分析】")
    extreme_weak_trades = [r for r in g.trade_records if r["breadth_state"] == "极弱"]
    if extreme_weak_trades:
        ew_avg = sum([r["pnl"] for r in extreme_weak_trades]) / len(extreme_weak_trades)
        ew_win = (
            sum([1 for r in extreme_weak_trades if r["pnl"] > 0])
            / len(extreme_weak_trades)
            * 100
        )
        ew_neg = sum([1 for r in extreme_weak_trades if r["pnl"] < -3])
        log.info(f"极弱市场平均收益: {ew_avg:.2f}%")
        log.info(f"极弱市场胜率: {ew_win:.1f}%")
        log.info(f"极弱市场亏损>3%次数: {ew_neg}/{len(extreme_weak_trades)}")

        if ew_avg < 0:
            log.info("⚠️ 极弱市场小市值策略系统性失效！")

    log.info("\n【情绪冰点详细分析】")
    freeze_trades = [r for r in g.trade_records if r["sentiment_state"] == "冰点"]
    if freeze_trades:
        fz_avg = sum([r["pnl"] for r in freeze_trades]) / len(freeze_trades)
        fz_win = (
            sum([1 for r in freeze_trades if r["pnl"] > 0]) / len(freeze_trades) * 100
        )
        fz_neg = sum([1 for r in freeze_trades if r["pnl"] < -3])
        log.info(f"情绪冰点平均收益: {fz_avg:.2f}%")
        log.info(f"情绪冰点胜率: {fz_win:.1f}%")
        log.info(f"情绪冰点亏损>3%次数: {fz_neg}/{len(freeze_trades)}")

        if fz_avg < 0:
            log.info("⚠️ 情绪冰点时小市值策略系统性失效！")

    log.info("\n【状态组合矩阵】")
    for breadth in ["极弱", "弱", "中", "强"]:
        for sentiment in ["冰点", "启动", "发酵", "高潮"]:
            trades = [
                r
                for r in g.trade_records
                if r["breadth_state"] == breadth and r["sentiment_state"] == sentiment
            ]
            if trades:
                avg_pnl_comb = sum([r["pnl"] for r in trades]) / len(trades)
                log.info(
                    f"{breadth}+{sentiment}: 平均收益={avg_pnl_comb:.2f}%, 交易数={len(trades)}"
                )

    log.info("\n【建议】")
    if breadth_groups.get("极弱", {}).get("avg_pnl", 0) < 0:
        log.info("1. 建议在极弱市场(广度<15%)停手")
    if sentiment_groups.get("冰点", {}).get("avg_pnl", 0) < 0:
        log.info("2. 建议在情绪冰点(涨停<30)停手")

    if both_filter_trades and breadth_filter_trades and sentiment_filter_trades:
        both_avg = sum([r["pnl"] for r in both_filter_trades]) / len(both_filter_trades)
        bf_avg = sum([r["pnl"] for r in breadth_filter_trades]) / len(
            breadth_filter_trades
        )
        sf_avg = sum([r["pnl"] for r in sentiment_filter_trades]) / len(
            sentiment_filter_trades
        )

        if both_avg > bf_avg and both_avg > sf_avg:
            log.info("3. 建议同时使用广度和情绪过滤")
        elif bf_avg > sf_avg:
            log.info("3. 建议优先使用广度过滤")
        else:
            log.info("3. 建议优先使用情绪过滤")

    log.info("\n" + "=" * 60)
