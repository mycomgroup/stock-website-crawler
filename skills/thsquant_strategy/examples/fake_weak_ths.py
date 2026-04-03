# 假弱高开策略 - THSQuant SuperMind 格式
# 适用于同花顺量化平台回测
from mindgo_api import *


def initialize(context):
    set_benchmark("000300.SH")
    g.trades = 0
    g.wins = 0
    g.pnl_list = []
    g.signals = 0
    run_daily(select_stocks, time_rule="after_open", hours=0, minutes=0)
    run_daily(buy_stocks, time_rule="after_open", hours=0, minutes=5)
    run_daily(sell_stocks, time_rule="before_close", hours=0, minutes=10)
    run_daily(print_stats, time_rule="after_close", hours=0, minutes=0)


def select_stocks(context):
    g.target = []
    prev_date = context.previous_date.strftime("%Y-%m-%d")
    all_stocks = get_all_securities(ty="stock", date=prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]
    all_stocks = [
        s
        for s in all_stocks
        if (context.previous_date - get_security_info(s).listed_date).days > 250
    ]
    try:
        bar_dict = get_current(all_stocks)
        all_stocks = [s for s in all_stocks if s in bar_dict and not bar_dict[s].is_st]
    except:
        pass
    df = history(
        all_stocks,
        ["close", "high_limit"],
        1,
        "1d",
        is_panel=False,
        fq="pre",
    )
    df = df.dropna()
    df = df[df["close"] == df["high_limit"]]
    g.target = list(df["code"])


def buy_stocks(context):
    if not g.target:
        return
    bar_dict = get_current(g.target)
    fake_weak = []
    for s in g.target:
        if s not in bar_dict:
            continue
        cd = bar_dict[s]
        if cd.is_paused:
            continue
        prev_close = cd.prev_close
        day_open = cd.open
        if prev_close <= 0:
            continue
        limit_price = prev_close * 1.1
        open_pct = (day_open / limit_price - 1) * 100
        if 0.5 <= open_pct <= 1.5:
            try:
                date_str = context.previous_date.strftime("%Y-%m-%d")
                val = get_fundamentals(
                    query(valuation.symbol, valuation.circulating_market_cap).filter(
                        valuation.symbol == s
                    ),
                    date=date_str,
                )
                if val is not None and len(val) > 0:
                    cap = val["circulating_market_cap"].iloc[0]
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
    positions = list(context.portfolio.positions)
    for s in positions:
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            bar_dict = get_current([s])
            if s in bar_dict:
                pnl = (bar_dict[s].close - pos.avg_cost) / pos.avg_cost * 100
                g.pnl_list.append(pnl)
                if pnl > 0:
                    g.wins += 1
            order_target(s, 0)


def after_trading(context):
    pass


def print_stats(context):
    if context.current_dt.month == 12 and context.current_dt.day >= 28:
        avg_pnl = sum(g.pnl_list) / len(g.pnl_list) if g.pnl_list else 0
        win_rate = g.wins / len(g.pnl_list) * 100 if g.pnl_list else 0
        log.info(
            "信号数=%d, 交易数=%d, 胜率=%.1f%%, 平均收益=%.2f%%"
            % (g.signals, g.trades, win_rate, avg_pnl)
        )
