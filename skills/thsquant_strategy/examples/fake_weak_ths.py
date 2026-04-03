# 假弱高开策略 - THSQuant SuperMind 格式
from mindgo_api import *


def init(context):
    set_benchmark("000300.SH")
    g.trades = 0
    g.wins = 0
    g.pnl_list = []
    g.signals = 0
    g.target = []
    g.selection_done = False


def handle_bar(context, bar_dict):
    current_time = context.current_dt.strftime("%H:%M")

    if current_time == "09:30" and not g.selection_done:
        prev_date_str = context.previous_date.strftime("%Y-%m-%d")
        all_stocks = get_all_securities(ty="stock", date=prev_date_str).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

        zt_stocks = []
        for s in all_stocks[:500]:
            try:
                info = get_security_info(s)
                if info and (context.previous_date - info.listed_date).days > 250:
                    bars = history(
                        [s], ["close", "high_limit"], 1, "1d", is_panel=False, fq="pre"
                    )
                    if bars is not None and len(bars) > 0:
                        if bars["close"].iloc[0] == bars["high_limit"].iloc[0]:
                            zt_stocks.append(s)
            except:
                pass

        g.target = zt_stocks
        g.selection_done = True

        if g.target:
            buy_stocks(context, bar_dict)

    elif current_time == "14:50":
        sell_stocks(context, bar_dict)
    elif current_time == "15:00":
        g.selection_done = False
        if context.current_dt.month == 12 and context.current_dt.day >= 28:
            avg_pnl = sum(g.pnl_list) / len(g.pnl_list) if g.pnl_list else 0
            win_rate = g.wins / len(g.pnl_list) * 100 if g.pnl_list else 0
            log.info(
                "信号数=%d, 交易数=%d, 胜率=%.1f%%, 平均收益=%.2f%%"
                % (g.signals, g.trades, win_rate, avg_pnl)
            )


def buy_stocks(context, bar_dict):
    if not g.target:
        return
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
            fake_weak.append({"stock": s, "open_pct": open_pct})

    g.signals += len(fake_weak)
    if fake_weak:
        fake_weak.sort(key=lambda x: abs(x["open_pct"] - 1.0))
        cash = context.portfolio.available_cash / min(len(fake_weak), 3)
        for item in fake_weak[:3]:
            order_value(item["stock"], cash)
            g.trades += 1


def sell_stocks(context, bar_dict):
    positions = list(context.portfolio.positions)
    for s in positions:
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            if s in bar_dict:
                pnl = (bar_dict[s].close - pos.avg_cost) / pos.avg_cost * 100
                g.pnl_list.append(pnl)
                if pnl > 0:
                    g.wins += 1
            order_target(s, 0)
