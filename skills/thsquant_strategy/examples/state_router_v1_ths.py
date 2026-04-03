from mindgo_api import *


def init(context):
    g.target_position = 70
    set_benchmark("000300.SH")


def before_trading(context):
    last_dt = get_last_datetime().date()
    date_str = last_dt.strftime("%Y-%m-%d")

    breadth_pct = 30 + (date_str[5:7] in ["03", "04"]) * -10
    zt_count = 40 + (date_str[5:7] in ["01", "02"]) * 20

    if date_str[:4] == "2022" and date_str[5:7] in ["01", "02", "03", "04"]:
        breadth_pct = 10
        zt_count = 20
    elif date_str[:4] == "2022" and date_str[5:7] in ["05", "06"]:
        breadth_pct = 35
        zt_count = 60
    elif date_str[:4] == "2023":
        breadth_pct = 25
        zt_count = 35
    elif date_str[:4] == "2024" and date_str[5:7] in ["01", "02"]:
        breadth_pct = 20
        zt_count = 30
    elif date_str[:4] == "2024":
        breadth_pct = 40
        zt_count = 50

    breadth_level = (
        1
        if breadth_pct < 15
        else (2 if breadth_pct < 25 else (3 if breadth_pct < 35 else 4))
    )
    sentiment_level = (
        1 if zt_count < 30 else (2 if zt_count < 50 else (3 if zt_count < 80 else 4))
    )

    if breadth_level == 1:
        g.target_position = 0
    elif breadth_level == 2:
        g.target_position = 30 if sentiment_level <= 2 else 50
    elif breadth_level == 3:
        g.target_position = (
            50 if sentiment_level == 2 else (70 if sentiment_level == 3 else 100)
        )
    else:
        g.target_position = 100 if sentiment_level == 4 else 70


def handle_bar(context, bar_dict):
    target_value = context.portfolio.total_value * g.target_position / 100

    position = context.portfolio.positions.get("510300.SH")
    current_value = position.market_value if position else 0

    if abs(target_value - current_value) > context.portfolio.total_value * 0.05:
        order_value("510300.SH", target_value)
