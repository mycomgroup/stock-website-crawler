# 小市值事件策略容量与滑点测试 - 简化版
# 仅首板低开(5-15亿) - 快速测试

from jqdata import *
import datetime as dt

SLIPPAGE_BPS = 0


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    if SLIPPAGE_BPS > 0:
        set_slippage(FixedSlippage(SLIPPAGE_BPS / 10000))

    g.trades = 0
    g.pnl_list = []

    set_benchmark("000300.XSHG")

    run_daily(select_stocks, "09:00")
    run_daily(buy_stocks, "09:31")
    run_daily(sell_stocks, "14:50")


def select_stocks(context):
    g.target = []

    prev_date = context.previous_date.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

    try:
        df = get_price(
            all_stocks,
            end_date=prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        df = df.dropna()
        df = df[df["close"] == df["high_limit"]]
        g.target = list(df["code"])[:30]
    except Exception as e:
        log.info(f"select error: {e}")


def buy_stocks(context):
    if not g.target:
        return

    current_data = get_current_data()
    qualified = []

    for s in g.target[:20]:
        if s not in current_data:
            continue

        cd = current_data[s]
        if cd.paused or cd.is_st:
            continue

        prev_close = cd.pre_close
        if prev_close <= 0:
            continue

        day_open = cd.day_open
        open_pct = (day_open - prev_close) / prev_close * 100

        if -1.5 <= open_pct <= 1.5:
            try:
                val = get_valuation(
                    s, end_date=context.previous_date, count=1, panel=False
                )
                if val is not None and len(val) > 0:
                    cap = val["circulating_market_cap"].iloc[0]
                    if 5 <= cap <= 15:
                        qualified.append(s)
            except Exception as e:
                pass

    if qualified:
        cash = context.portfolio.available_cash / min(len(qualified), 3)
        for s in qualified[:3]:
            price = current_data[s].last_price
            if price > 0:
                shares = int(cash / price / 100) * 100
                if shares >= 100:
                    order(s, shares)
                    g.trades += 1


def sell_stocks(context):
    current_data = get_current_data()
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            cd = current_data[s]
            if cd.last_price > 0 and pos.avg_cost > 0:
                pnl = (cd.last_price - pos.avg_cost) / pos.avg_cost * 100
                g.pnl_list.append(pnl)
            order_target(s, 0)


def after_trading_end(context):
    if len(g.pnl_list) > 0:
        avg_pnl = sum(g.pnl_list) / len(g.pnl_list)
        win_rate = len([p for p in g.pnl_list if p > 0]) / len(g.pnl_list) * 100
        log.info(
            f"Trades: {len(g.pnl_list)}, Avg PnL: {avg_pnl:.2f}%, WinRate: {win_rate:.1f}%"
        )
