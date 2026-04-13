"""
首板低开策略 - JoinQuant回测版本

信号定义：
- 首板：昨日涨停（非连板）
- 低开：次日开盘涨跌幅 -2% ~ +1.5%
- 流通市值：5-15亿
- 15日位置：≤30%

退出方式：
- 次日收盘卖出（可改为次日最高、10:30等）
"""

from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.trade_count = 0
    g.win_count = 0
    g.pnl_list = []
    g.daily_signals = []

    run_daily(select_stocks, "9:00")
    run_daily(buy_stocks, "9:35")
    run_daily(record_signals, "15:00")
    run_daily(sell_stocks, "14:50")


def select_stocks(context):
    g.target = []
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    all_stocks = get_all_securities(types=["stock"], date=prev_date).index.tolist()

    all_stocks = [
        s
        for s in all_stocks
        if not (
            s.startswith("688")
            or s.startswith("300")
            or s.startswith("4")
            or s.startswith("8")
        )
    ]

    df = get_price(
        all_stocks,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )

    df = df.dropna()
    zt_df = df[df["close"] == df["high_limit"]]
    zt_stocks = zt_df["code"].tolist()

    if not zt_stocks:
        return

    prev_dates = get_trade_days(end_date=prev_date, count=2)
    if len(prev_dates) < 2:
        return

    prev_prev_date = prev_dates[0]

    df_prev = get_price(
        zt_stocks,
        end_date=prev_prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )

    df_prev = df_prev.dropna()
    prev_zt_df = df_prev[df_prev["close"] == df_prev["high_limit"]]
    prev_zt_stocks = prev_zt_df["code"].tolist()

    first_board = [s for s in zt_stocks if s not in prev_zt_stocks]

    g.first_board_stocks = first_board


def buy_stocks(context):
    if not hasattr(g, "first_board_stocks") or not g.first_board_stocks:
        return

    current_data = get_current_data()
    qualified = []

    date = context.current_dt.strftime("%Y-%m-%d")

    for stock in g.first_board_stocks[:50]:
        if stock not in current_data:
            continue

        cd = current_data[stock]
        if cd.paused:
            continue

        prev_close = cd.pre_close
        day_open = cd.day_open

        open_pct = (day_open - prev_close) / prev_close * 100

        if not (-2.0 <= open_pct <= 1.5):
            continue

        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code == stock
        )
        df_cap = get_fundamentals(q, date)

        if df_cap.empty:
            continue

        market_cap = float(df_cap["circulating_market_cap"].iloc[0])

        if not (5 <= market_cap <= 15):
            continue

        df_pos = get_price(
            stock,
            end_date=date,
            frequency="daily",
            fields=["close"],
            count=15,
            panel=False,
        )

        if len(df_pos) < 5:
            continue

        high_15d = df_pos["close"].max()
        low_15d = df_pos["close"].min()
        curr_close = df_pos["close"].iloc[-1]

        if high_15d == low_15d:
            continue

        position = (curr_close - low_15d) / (high_15d - low_15d)

        if position > 0.30:
            continue

        qualified.append(
            {
                "stock": stock,
                "open_pct": open_pct,
                "market_cap": market_cap,
                "position": position,
                "buy_price": day_open,
            }
        )

    if qualified:
        cash = context.portfolio.available_cash / min(len(qualified), 5)

        for item in qualified[:5]:
            stock = item["stock"]
            buy_price = item["buy_price"]

            shares = int(cash / buy_price / 100) * 100

            if shares >= 100:
                order(stock, shares)
                g.trade_count += 1

                g.daily_signals.append(
                    {
                        "date": date,
                        "stock": stock,
                        "open_pct": item["open_pct"],
                        "market_cap": item["market_cap"],
                        "position": item["position"],
                        "buy_price": buy_price,
                    }
                )


def record_signals(context):
    if g.daily_signals:
        date = context.current_dt.strftime("%Y-%m-%d")
        log.info(f"{date}: {len(g.daily_signals)} signals")

        for sig in g.daily_signals:
            log.info(
                f"  {sig['stock']}: open={sig['open_pct']:.2f}%, cap={sig['market_cap']:.1f}B, pos={sig['position']:.2f}"
            )

    g.daily_signals = []


def sell_stocks(context):
    current_data = get_current_data()

    for stock in list(context.portfolio.positions):
        pos = context.portfolio.positions[stock]

        if pos.closeable_amount > 0:
            cd = current_data[stock]

            pnl = (cd.last_price - pos.avg_cost) / pos.avg_cost * 100

            g.pnl_list.append(pnl)

            if pnl > 0:
                g.win_count += 1

            order_target(stock, 0)


def after_trading_end(context):
    if g.trade_count > 0:
        avg_pnl = sum(g.pnl_list) / len(g.pnl_list) if g.pnl_list else 0
        win_rate = g.win_count / g.trade_count * 100 if g.trade_count > 0 else 0

        log.info(f"Total trades: {g.trade_count}")
        log.info(f"Win rate: {win_rate:.1f}%")
        log.info(f"Average PnL: {avg_pnl:.2f}%")
        log.info(f"Total PnL: {sum(g.pnl_list):.2f}%")
