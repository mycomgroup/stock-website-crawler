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
    g.trade_count = 0
    g.win_count = 0
    g.total_profit = 0


def handle_data(context, data):
    date = context.current_dt.strftime("%Y-%m-%d")

    if date < "2021-01-01" or date > "2023-12-31":
        return

    trade_days = list(get_trade_days(end_date=date, count=5))
    if len(trade_days) < 2:
        return
    prev_date = str(trade_days[-2])[:10]
    prev2_date = str(trade_days[-3])[:10] if len(trade_days) >= 3 else prev_date

    all_stocks = get_all_securities("stock", date=prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if not s.startswith(("68", "4", "8"))]

    df = get_price(
        all_stocks,
        end_date=prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
    )
    if df.empty:
        return

    zt_df = df[abs(df["close"] - df["high_limit"]) / df["high_limit"] < 0.01]
    zt_stocks = zt_df["code"].tolist()

    if len(zt_stocks) < 10:
        return

    df2 = get_price(
        zt_stocks,
        end_date=prev2_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
    )
    if df2.empty:
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
        return

    val = get_fundamentals(
        query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code.in_(two_board)
        ),
        date=date,
    )
    if val.empty:
        return

    target = val.sort_values("circulating_market_cap").iloc[0]["code"]

    curr = get_price(
        target, end_date=date, count=1, fields=["open", "high_limit"], panel=False
    )
    if curr.empty:
        return

    o = float(curr["open"].iloc[0])
    hl = float(curr["high_limit"].iloc[0])

    if abs(o - hl) / hl < 0.01:
        return

    if context.portfolio.positions:
        for stock in list(context.portfolio.positions.keys()):
            order_target(stock, 0)

    order_value(target, context.portfolio.total_value * 0.95)
    g.trade_count += 1
    log.info(f"{date} 买入 {target}")
