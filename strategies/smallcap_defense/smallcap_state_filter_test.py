from jqdata import *
import pandas as pd
import numpy as np


def initialize(context):
    set_benchmark("000852.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("order", "error")

    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    g.hold_num = 15
    g.min_cap = 15
    g.max_cap = 60
    g.ipo_days = 180
    g.max_pb = 1.5
    g.max_pe = 20

    g.results = {
        "baseline": {"trades": [], "daily_values": []},
        "freeze_stop": {"trades": [], "daily_values": []},
        "reduce_half": {"trades": [], "daily_values": []},
        "normal_only": {"trades": [], "daily_values": []},
    }

    g.zt_count = 50

    run_daily(get_sentiment, time="9:30")
    run_monthly(rebalance, 1, time="9:35")
    run_daily(record_daily, time="15:00")


def get_sentiment(context):
    prev_date = context.previous_date

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
            g.zt_count = len(df[df["close"] == df["high_limit"]])
        else:
            g.zt_count = 0
    except:
        g.zt_count = 0


def get_smallcap_universe(watch_date):
    all_stocks = get_all_securities(types=["stock"], date=watch_date)
    all_stocks = all_stocks[
        all_stocks["start_date"] <= watch_date - pd.Timedelta(days=g.ipo_days)
    ]
    stocks = all_stocks.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    stocks = [s for s in stocks if not s.startswith("688")]

    q = query(valuation.code, valuation.market_cap).filter(
        valuation.code.in_(stocks),
        valuation.market_cap >= g.min_cap,
        valuation.market_cap <= g.max_cap,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    df["cap_rank"] = df["market_cap"].rank(pct=True)
    small_stocks = df[df["cap_rank"] <= 0.3]["code"].tolist()

    return small_stocks


def select_stocks(watch_date, hold_num):
    stocks = get_smallcap_universe(watch_date)
    if len(stocks) < 5:
        return []

    q = query(
        valuation.code,
        valuation.market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
        indicator.roe,
    ).filter(
        valuation.code.in_(stocks),
        valuation.pe_ratio > 0,
        valuation.pe_ratio < g.max_pe,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < g.max_pb,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    df = df.drop_duplicates("code")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    if len(df) == 0:
        return []

    df["pb_rank"] = df["pb_ratio"].rank(pct=True)
    df["pe_rank"] = df["pe_ratio"].rank(pct=True)
    df["value_score"] = (df["pb_rank"] + df["pe_rank"]) / 2

    df = df.sort_values("value_score", ascending=True)

    return df["code"].tolist()[:hold_num]


def filter_buyable(context, stocks):
    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if current_data[stock].paused or current_data[stock].is_st:
            continue
        if "ST" in current_data[stock].name or "*" in current_data[stock].name:
            continue
        last_price = current_data[stock].last_price
        if last_price >= current_data[stock].high_limit * 0.995:
            continue
        buyable.append(stock)
    return buyable


def rebalance(context):
    watch_date = context.previous_date
    current_date = context.current_dt.strftime("%Y-%m-%d")
    zt_count = g.zt_count

    stocks = select_stocks(watch_date, g.hold_num)
    stocks = filter_buyable(context, stocks)

    if len(stocks) == 0:
        return

    total_value = context.portfolio.total_value

    strategies = {
        "baseline": (1.0, True),
        "freeze_stop": (1.0, zt_count >= 30),
        "reduce_half": (0.5 if zt_count < 50 else 1.0, True),
        "normal_only": (1.0, zt_count >= 50),
    }

    current_positions = list(context.portfolio.positions.keys())

    for strategy_name, (position_ratio, should_trade) in strategies.items():
        if not should_trade:
            for stock in current_positions:
                order_target_value(stock, 0)
            g.results[strategy_name]["trades"].append(
                {
                    "date": current_date,
                    "action": "skip",
                    "zt_count": zt_count,
                    "reason": f"涨停数{zt_count}不满足条件",
                }
            )
        else:
            target_stocks = stocks[: g.hold_num]
            target_value_per_stock = total_value * position_ratio / len(target_stocks)

            for stock in current_positions:
                if stock not in target_stocks:
                    order_target_value(stock, 0)

            for stock in target_stocks:
                order_target_value(stock, target_value_per_stock)

            g.results[strategy_name]["trades"].append(
                {
                    "date": current_date,
                    "action": "rebalance",
                    "zt_count": zt_count,
                    "position_ratio": position_ratio,
                    "stock_count": len(target_stocks),
                }
            )


def record_daily(context):
    current_date = context.current_dt.strftime("%Y-%m-%d")
    total_value = context.portfolio.total_value

    for strategy_name in g.results:
        g.results[strategy_name]["daily_values"].append(
            {"date": current_date, "value": total_value, "zt_count": g.zt_count}
        )


def on_end(context):
    log.info("\n" + "=" * 80)
    log.info("状态过滤回测结果")
    log.info("=" * 80)

    for strategy_name in g.results:
        daily_values = g.results[strategy_name]["daily_values"]
        if len(daily_values) == 0:
            continue

        values = [dv["value"] for dv in daily_values]
        dates = [dv["date"] for dv in daily_values]

        total_return = (values[-1] - values[0]) / values[0]
        years = len(values) / 252
        annual_return = (1 + total_return) ** (1 / years) - 1

        peak = values[0]
        max_dd = 0
        for v in values:
            if v > peak:
                peak = v
            dd = (peak - v) / peak
            if dd > max_dd:
                max_dd = dd

        returns = []
        for i in range(1, len(values)):
            ret = (values[i] - values[i - 1]) / values[i - 1]
            returns.append(ret)

        sharpe = (
            np.mean(returns) / np.std(returns) * np.sqrt(252)
            if np.std(returns) > 0
            else 0
        )

        trades = g.results[strategy_name]["trades"]
        trade_count = len([t for t in trades if t["action"] == "rebalance"])

        log.info(f"\n策略: {strategy_name}")
        log.info(f"总收益率: {total_return:.2%}")
        log.info(f"年化收益率: {annual_return:.2%}")
        log.info(f"最大回撤: {max_dd:.2%}")
        log.info(f"夏普比率: {sharpe:.2f}")
        log.info(f"调仓次数: {trade_count}")

        zt_counts = [dv["zt_count"] for dv in daily_values]
        log.info(f"平均涨停数: {np.mean(zt_counts):.1f}")
        log.info(f"涨停数<30天数: {len([z for z in zt_counts if z < 30])}")
        log.info(f"涨停数30-50天数: {len([z for z in zt_counts if 30 <= z < 50])}")
        log.info(f"涨停数>=50天数: {len([z for z in zt_counts if z >= 50])}")

    log.info("\n" + "=" * 80)
    log.info("对比总结")
    log.info("=" * 80)

    baseline_dd = 0.3773

    for strategy_name in g.results:
        daily_values = g.results[strategy_name]["daily_values"]
        if len(daily_values) == 0:
            continue

        values = [dv["value"] for dv in daily_values]
        peak = values[0]
        max_dd = 0
        for v in values:
            if v > peak:
                peak = v
            dd = (peak - v) / peak
            if dd > max_dd:
                max_dd = dd

        dd_reduction = (baseline_dd - max_dd) / baseline_dd * 100

        log.info(f"\n{strategy_name}:")
        log.info(f"  最大回撤: {max_dd:.2%}")
        log.info(f"  回撤降低: {dd_reduction:.1f}%")
        log.info(f"  vs基准回撤(37.73%): {'✓ 达标' if max_dd < 0.25 else '✗ 未达标'}")
