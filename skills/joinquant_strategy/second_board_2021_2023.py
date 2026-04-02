def initialize(context):
    set_option("use_real_price", True)
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            close_today_commission=0,
            min_commission=5,
        ),
        type="stock",
    )
    g.prev_date = None
    g.prev2_date = None
    g.current_date = None
    g.trade_count = 0


def before_trading_start(context):
    g.current_date = context.current_dt.strftime("%Y-%m-%d")


def handle_data(context, data):
    date = g.current_date

    if date < "2021-01-01" or date > "2023-12-31":
        return

    if g.prev2_date is None:
        g.prev2_date = g.prev_date
        g.prev_date = date
        return

    if g.prev_date is None or g.prev2_date is None:
        g.prev2_date = g.prev_date
        g.prev_date = date
        return

    try:
        all_stocks = get_all_securities("stock", date=g.prev_date).index.tolist()
        all_stocks = [s for s in all_stocks if not s.startswith(("68", "4", "8"))]

        df = get_price(
            all_stocks,
            end_date=g.prev_date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        if df.empty:
            g.prev2_date = g.prev_date
            g.prev_date = date
            return

        zt_df = df[abs(df["close"] - df["high_limit"]) / df["high_limit"] < 0.01]
        zt_stocks = zt_df["code"].tolist()

        if len(zt_stocks) < 10:
            g.prev2_date = g.prev_date
            g.prev_date = date
            return

        df2 = get_price(
            zt_stocks,
            end_date=g.prev2_date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        if df2.empty:
            g.prev2_date = g.prev_date
            g.prev_date = date
            return

        two_board = []
        for s in zt_stocks:
            row = df2[df2["code"] == s]
            if len(row) == 0:
                continue
            if (
                abs(row["close"].iloc[0] - row["high_limit"].iloc[0])
                / row["high_limit"].iloc[0]
                < 0.01
            ):
                two_board.append(s)

        if len(two_board) == 0:
            g.prev2_date = g.prev_date
            g.prev_date = date
            return

        val = get_fundamentals(
            query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.code.in_(two_board)
            ),
            date=date,
        )
        if val.empty:
            g.prev2_date = g.prev_date
            g.prev_date = date
            return

        target = val.sort_values("circulating_market_cap").iloc[0]["code"]

        curr = get_price(
            target, end_date=date, count=1, fields=["open", "high_limit"], panel=False
        )
        if curr.empty:
            g.prev2_date = g.prev_date
            g.prev_date = date
            return

        o = float(curr["open"].iloc[0])
        hl = float(curr["high_limit"].iloc[0])

        if abs(o - hl) / hl < 0.01:
            g.prev2_date = g.prev_date
            g.prev_date = date
            return

        if context.portfolio.positions:
            for stock in list(context.portfolio.positions.keys()):
                order_target(stock, 0)

        order_value(target, context.portfolio.total_value * 0.95)
        g.trade_count += 1
        log.info(f"{date} BUY {target} trades={g.trade_count}")

    except Exception as e:
        log.error(f"{date} ERROR: {e}")

    g.prev2_date = g.prev_date
    g.prev_date = date
