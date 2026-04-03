# Fake weak high open - simplified THSQuant
from mindgo_api import *


def init(context):
    set_benchmark("000300.SH")
    g.trades = 0
    g.wins = 0
    g.pnl_list = []
    g.signals = 0
    g.target = []


def handle_bar(context, bar_dict):
    current_time = context.current_dt.strftime("%H:%M")

    if current_time == "09:30":
        prev_date_str = context.previous_date.strftime("%Y-%m-%d")
        all_stocks = get_all_securities(ty="stock", date=prev_date_str).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]
        df = history(
            all_stocks[:100], ["close", "high_limit"], 1, "1d", is_panel=False, fq="pre"
        )
        df = df.dropna()
        df = df[df["close"] == df["high_limit"]]
        g.target = list(df["code"])[:3]

        for s in g.target:
            if s in bar_dict:
                cd = bar_dict[s]
                if not cd.is_paused and cd.prev_close > 0:
                    order_target_percent(s, 0.1)
                    g.trades += 1
                    log.info("BUY: %s" % s)
    elif current_time == "14:50":
        for s in list(context.portfolio.positions):
            order_target(s, 0)
