from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.trades = 0
    g.wins = 0
    g.pnl_list = []

    set_benchmark("000300.XSHG")

    # 每周一买入
    run_weekly(buy_and_sell, 1, time="09:35")


def buy_and_sell(context):
    date = context.current_dt.date()

    # 先卖
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            pnl = (
                context.portfolio.positions[s].avg_cost
                - context.portfolio.positions[s].avg_cost
            ) / context.portfolio.positions[s].avg_cost
            order_target(s, 0)

    # 获取昨日涨停
    prev_date = (date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

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
        hl_stocks = list(df["code"])

        if not hl_stocks:
            log.info(f"{date}: 无涨停股")
            return

        current_data = get_current_data()
        fake_weak = []

        for s in hl_stocks[:30]:
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
                fake_weak.append(s)

        if fake_weak:
            cash = context.portfolio.available_cash / len(fake_weak)
            for s in fake_weak[:3]:
                order_value(s, cash)
                g.trades += 1
            log.info(
                f"{date}: 假弱高开 {len(fake_weak)} 只, 买入 {min(len(fake_weak), 3)} 只"
            )
        else:
            log.info(f"{date}: 涨停{len(hl_stocks)}只, 无假弱高开")

    except Exception as e:
        log.info(f"{date}: 错误 {e}")


import datetime
