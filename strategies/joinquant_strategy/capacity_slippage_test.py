# 小市值事件策略容量与滑点测试
# 首板低开(5-15亿) + 二板接力(<30亿)
# 参数化: 滑点bps, 容量限制成交额占比

from jqdata import *
import datetime as dt

CAPACITY_LIMIT_RATIO = 0.05
SLIPPAGE_BPS = 0


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    if SLIPPAGE_BPS > 0:
        set_slippage(FixedSlippage(SLIPPAGE_BPS / 10000))

    g.trade_records = []
    g.signal_count = 0
    g.executed_count = 0
    g.rejected_capacity = 0

    set_benchmark("000300.XSHG")

    run_daily(prepare_signals, "09:00")
    run_daily(buy_stocks, "09:31")
    run_daily(sell_stocks, "14:50")


def prepare_signals(context):
    g.signals = []
    g.first_board_signals = []
    g.second_board_signals = []

    date = context.previous_date.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]
    all_stocks = [
        s
        for s in all_stocks
        if (context.previous_date - get_security_info(s).start_date).days > 250
    ]

    df = get_price(
        all_stocks,
        end_date=date,
        frequency="daily",
        fields=["close", "high_limit", "volume", "money"],
        count=1,
        panel=False,
    )
    df = df.dropna()
    hl_df = df[df["close"] == df["high_limit"]]
    hl_stocks = list(hl_df["code"])

    if len(hl_stocks) == 0:
        return

    for s in hl_stocks[:50]:
        val = get_valuation(s, end_date=date, count=1, panel=False)
        if val is None or len(val) == 0:
            continue

        cap = val["circulating_market_cap"].iloc[0]
        avg_money = (
            df[df["code"] == s]["money"].iloc[0] if len(df[df["code"] == s]) > 0 else 0
        )

        if 5 <= cap <= 15:
            g.first_board_signals.append(
                {"code": s, "cap": cap, "avg_money": avg_money, "type": "first_board"}
            )

    prev_date = get_shifted_date(date, -1)
    prev2_date = get_shifted_date(date, -2)

    prev_hl = get_hl_stocks(prev_date)
    prev2_hl = get_hl_stocks(prev2_date)

    second_board = list(set(prev_hl) - set(prev2_hl))

    for s in second_board[:50]:
        val = get_valuation(s, end_date=date, count=1, panel=False)
        if val is None or len(val) == 0:
            continue

        cap = val["circulating_market_cap"].iloc[0]
        avg_money = get_avg_money(s, date)

        if cap < 30:
            g.second_board_signals.append(
                {"code": s, "cap": cap, "avg_money": avg_money, "type": "second_board"}
            )

    g.signals = g.first_board_signals + g.second_board_signals
    g.signal_count = len(g.signals)


def buy_stocks(context):
    if len(g.signals) == 0:
        return

    current_data = get_current_data()
    qualified = []

    for sig in g.signals:
        s = sig["code"]
        if s not in current_data:
            continue

        cd = current_data[s]
        if cd.paused or cd.is_st:
            continue

        if sig["type"] == "first_board":
            pre_close = cd.pre_close
            high_limit = cd.high_limit
            day_open = cd.day_open

            if pre_close <= 0:
                continue

            open_pct = (day_open - pre_close) / pre_close * 100
            if -1.5 <= open_pct <= 1.5:
                max_buy_value = sig["avg_money"] * CAPACITY_LIMIT_RATIO
                qualified.append(
                    {"code": s, "max_buy": max_buy_value, "type": "first_board"}
                )
        else:
            if cd.last_price == cd.high_limit:
                continue

            max_buy_value = sig["avg_money"] * CAPACITY_LIMIT_RATIO
            qualified.append(
                {"code": s, "max_buy": max_buy_value, "type": "second_board"}
            )

    if len(qualified) == 0:
        return

    total_cash = context.portfolio.available_cash
    per_signal = total_cash / min(len(qualified), 5)

    for q in qualified[:5]:
        s = q["code"]
        max_buy = q["max_buy"]
        buy_value = min(per_signal, max_buy)

        if buy_value < 10000:
            g.rejected_capacity += 1
            continue

        cd = current_data[s]
        if cd.last_price <= 0:
            continue

        try:
            order_value(s, buy_value)
            g.executed_count += 1

            g.trade_records.append(
                {
                    "date": context.current_dt.strftime("%Y-%m-%d"),
                    "code": s,
                    "type": q["type"],
                    "buy_value": buy_value,
                    "buy_price": cd.last_price,
                }
            )
        except Exception as e:
            log.info(f"buy error {s}: {e}")


def sell_stocks(context):
    current_data = get_current_data()

    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount == 0:
            continue

        cd = current_data[s]
        sell_price = cd.last_price
        buy_price = pos.avg_cost

        pnl_pct = (sell_price - buy_price) / buy_price * 100

        try:
            order_target_value(s, 0)

            for rec in g.trade_records:
                if rec["code"] == s and "sell_price" not in rec:
                    rec["sell_price"] = sell_price
                    rec["pnl_pct"] = pnl_pct
                    rec["hold_days"] = (
                        (
                            context.current_dt
                            - context.portfolio.positions[s].init_time
                        ).days
                        if s in context.portfolio.positions
                        else 1
                    )
        except Exception as e:
            log.info(f"sell error {s}: {e}")


def get_hl_stocks(date):
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

    df = get_price(
        all_stocks,
        end_date=date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    df = df.dropna()
    hl_df = df[df["close"] == df["high_limit"]]
    return list(hl_df["code"])


def get_shifted_date(date, days):
    all_days = [d.strftime("%Y-%m-%d") for d in get_all_trade_days()]
    if date in all_days:
        idx = all_days.index(date)
        new_idx = idx + days
        if 0 <= new_idx < len(all_days):
            return all_days[new_idx]
    return date


def get_avg_money(stock, date):
    df = get_price(
        stock,
        end_date=date,
        frequency="daily",
        fields=["money"],
        count=5,
        panel=False,
    )
    if len(df) > 0:
        return df["money"].mean()
    return 0


def after_trading_end(context):
    total_return = context.portfolio.total_value / context.portfolio.starting_cash - 1

    log.info(
        f"信号数: {g.signal_count}, 执行数: {g.executed_count}, 容量拒绝: {g.rejected_capacity}"
    )
    log.info(f"总收益: {total_return * 100:.2f}%")

    if len(g.trade_records) > 0:
        pnls = [r.get("pnl_pct", 0) for r in g.trade_records if "pnl_pct" in r]
        if len(pnls) > 0:
            avg_pnl = sum(pnls) / len(pnls)
            win_rate = len([p for p in pnls if p > 0]) / len(pnls) * 100
            log.info(f"平均收益: {avg_pnl:.2f}%, 胜率: {win_rate:.1f}%")
