from jqdata import *
import datetime as dt


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.trades = 0
    g.wins = 0
    g.pnl_list = []
    g.daily_trades = []

    run_daily(select_stocks, "9:00")
    run_daily(buy_stocks, "09:35")
    run_daily(sell_stocks, "14:50")


def select_stocks(context):
    g.target = []
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

    # 过滤新股
    all_stocks = [
        s
        for s in all_stocks
        if (context.previous_date - get_security_info(s).start_date).days > 250
    ]

    # 过滤ST
    st_df = get_extras(
        "is_st", all_stocks, start_date=prev_date, end_date=prev_date, df=True
    ).T
    st_df.columns = ["is_st"]
    all_stocks = list(st_df[st_df["is_st"] == False].index)

    # 获取昨日涨停
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
    qualified = []

    for s in g.target:
        if s not in current_data:
            continue
        cd = current_data[s]
        if cd.paused:
            continue

        high_limit = cd.high_limit
        day_open = cd.day_open
        pre_close = cd.pre_close

        if pre_close <= 0 or high_limit <= 0:
            continue

        # 假弱高开: 开盘价相对涨停价 +0.5%~+1.5%
        # 涨停价 = pre_close * 1.1
        limit_price = pre_close * 1.1
        open_ratio = day_open / limit_price

        if 1.005 <= open_ratio <= 1.015:
            # 市值过滤: 50-150亿
            val = get_valuation(s, end_date=context.previous_date, count=1)
            if val is not None and len(val) > 0:
                cap = val["circulating_market_cap"].iloc[0]
                if 50 <= cap <= 150:
                    qualified.append(
                        {
                            "stock": s,
                            "open_price": day_open,
                            "open_ratio": open_ratio,
                            "cap": cap,
                        }
                    )

    if qualified:
        cash = context.portfolio.available_cash / min(len(qualified), 3)
        for q in qualified[:3]:
            s = q["stock"]
            price = current_data[s].last_price
            shares = int(cash / price / 100) * 100
            if shares >= 100:
                order(s, shares)
                g.trades += 1
                g.daily_trades.append(
                    {
                        "date": context.current_dt.strftime("%Y-%m-%d"),
                        "stock": s,
                        "open_ratio": q["open_ratio"],
                    }
                )


def sell_stocks(context):
    current_data = get_current_data()
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            cd = current_data[s]
            pnl = (cd.last_price - pos.avg_cost) / pos.avg_cost * 100
            g.pnl_list.append(pnl)
            if pnl > 0:
                g.wins += 1
            order_target(s, 0)

    # 年末统计
    if context.current_dt.month == 12 and context.current_dt.day >= 28:
        total_pnl = sum(g.pnl_list)
        avg_pnl = total_pnl / len(g.pnl_list) if g.pnl_list else 0
        win_rate = g.wins / len(g.pnl_list) * 100 if g.pnl_list else 0
        log.info(
            f"Trades={g.trades}, Wins={g.wins}, WinRate={win_rate:.1f}%, AvgPnL={avg_pnl:.2f}%"
        )
