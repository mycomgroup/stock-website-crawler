# Simplified fake_weak_ths for debugging
from mindgo_api import *


def initialize(context):
    set_benchmark("000300.SH")
    g.trades = 0
    g.wins = 0
    g.pnl_list = []
    g.signals = 0


def handle_bar(context, bar_dict):
    current_time = context.current_dt.strftime("%H:%M")
    log.info("HANDLE_BAR at " + current_time)

    if current_time == "09:30":
        log.info("Running selection logic")
        prev_date_str = context.previous_date.strftime("%Y-%m-%d")
        log.info("Prev date: " + prev_date_str)

        all_stocks = get_all_securities(ty="stock", date=prev_date_str).index.tolist()
        log.info("Total stocks: %d" % len(all_stocks))

        all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]
        log.info("After filter: %d" % len(all_stocks))

        g.target = all_stocks[:10]
        log.info("Target set to first 10 stocks for test")

        buy_stocks(context, bar_dict)
    elif current_time == "14:50":
        sell_stocks(context, bar_dict)


def buy_stocks(context, bar_dict):
    if not g.target:
        log.info("No target stocks")
        return
    log.info("Processing %d target stocks" % len(g.target))
    for s in g.target[:3]:
        if s in bar_dict:
            cd = bar_dict[s]
            log.info("Stock %s: open=%s, prev_close=%s" % (s, cd.open, cd.prev_close))
            order_target_percent(s, 0.1)
            log.info("Ordered 10%% of %s" % s)
            g.trades += 1


def sell_stocks(context, bar_dict):
    positions = list(context.portfolio.positions)
    log.info("Selling %d positions" % len(positions))
    for s in positions:
        order_target(s, 0)
