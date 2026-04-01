from jqdata import *
import datetime as dt


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.trades = 0
    g.wins = 0
    g.pnl_list = []
    g.signals = 0

    set_benchmark("000300.XSHG")

    run_daily(select_stocks, "9:00")
    run_daily(buy_stocks, "09:35")
    run_daily(sell_stocks, "14:50")
    run_daily(print_stats, "15:00")


def select_stocks(context):
    g.target = []
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]
    all_stocks = [
        s
        for s in all_stocks
        if (context.previous_date - get_security_info(s).start_date).days > 250
    ]

    try:
        st_df = get_extras(
            "is_st", all_stocks, start_date=prev_date, end_date=prev_date, df=True
        ).T
        st_df.columns = ["is_st"]
        all_stocks = list(st_df[st_df["is_st"] == False].index)
    except:
        pass

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
    g.target = list(df["code"])


def buy_stocks(context):
    if not g.target:
        return

    current_data = get_current_data()
    fake_weak = []

    for s in g.target:
        if s not in current_data:
            continue
        cd = current_data[s]
        if cd.paused:
            continue

        pre_close = cd.pre_close
        day_open = cd.day_open

        if pre_close <= 0:
            continue

        limit_price = pre_close * 1.1
        open_pct = (day_open / limit_price - 1) * 100

        # 假弱高开: 相对涨停价 +0.5%~+1.5%
        if 0.5 <= open_pct <= 1.5:
            try:
                val = get_valuation(s, end_date=context.previous_date, count=1)
                if val is not None and len(val) > 0:
                    cap = val["circulating_market_cap"].iloc[0]
                    # 市值30-200亿
                    if 30 <= cap <= 200:
                        fake_weak.append({"stock": s, "open_pct": open_pct, "cap": cap})
            except:
                pass

    g.signals += len(fake_weak)

    if fake_weak:
        fake_weak.sort(key=lambda x: abs(x["open_pct"] - 1.0))
        cash = context.portfolio.available_cash / min(len(fake_weak), 3)
        for item in fake_weak[:3]:
            s = item["stock"]
            order_value(s, cash)
            g.trades += 1


def sell_stocks(context):
    current_data = get_current_data()
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            cd = current_data
            if s in cd:
                pnl = (cd[s].last_price - pos.avg_cost) / pos.avg_cost * 100
                g.pnl_list.append(pnl)
                if pnl > 0:
                    g.wins += 1
            order_target(s, 0)


def print_stats(context):
    if context.current_dt.month == 12 and context.current_dt.day >= 28:
        avg_pnl = sum(g.pnl_list) / len(g.pnl_list) if g.pnl_list else 0
        win_rate = g.wins / len(g.pnl_list) * 100 if g.pnl_list else 0
        log.info(
            f"信号数={g.signals}, 交易数={g.trades}, 胜率={win_rate:.1f}%, 平均收益={avg_pnl:.2f}%"
        )
