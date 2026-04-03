"""
任务02对比：单阈值50
"""


def init(context):
    context.threshold = 50
    context.max_positions = 5
    context.position_size = 0.2
    scheduler.run_monthly(rebalance, monthday=1)
    print("单阈值策略初始化：50")


def rebalance(context, bar_dict):
    zt_count = get_zt_count(context)
    print(f"涨停家数：{zt_count}")

    if zt_count < context.threshold:
        print(f"情绪过低，空仓")
        clear_all(context)
        return

    selected = select_stocks(context)
    if len(selected) > 0:
        adjust_positions(context, selected)


def get_zt_count(context):
    try:
        stocks = all_instruments("CS")
        stocks = [
            s
            for s in stocks.order_book_id
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]
        zt = 0
        for s in stocks[:500]:
            try:
                bars = history_bars(s, 1, "1d", ["close", "limit_up"])
                if bars is not None and len(bars) > 0:
                    if bars[0]["close"] >= bars[0]["limit_up"] * 0.99:
                        zt += 1
            except:
                pass
        return int(zt * len(stocks) / 500)
    except:
        return 100


def select_stocks(context):
    try:
        stocks = all_instruments("CS")
        stocks = [
            s
            for s in stocks.order_book_id
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        prev_zt = []
        for s in stocks[:300]:
            try:
                bars = history_bars(s, 1, "1d", ["close", "limit_up"])
                if (
                    bars
                    and len(bars) > 0
                    and bars[0]["close"] >= bars[0]["limit_up"] * 0.99
                ):
                    prev_zt.append(s)
            except:
                pass

        if len(prev_zt) == 0:
            return []

        selected = []
        for s in prev_zt[:20]:
            try:
                prev = history_bars(s, 2, "1d", "close")
                curr = history_bars(s, 1, "1d", ["open", "limit_up"])
                if prev is not None and curr is not None and len(prev) >= 2:
                    pct = (curr[0]["open"] / prev[-2] - 1) * 100
                    if (
                        0.5 <= pct <= 1.5
                        and curr[0]["open"] < curr[0]["limit_up"] * 0.99
                    ):
                        selected.append(s)
            except:
                pass
        return selected[: context.max_positions]
    except:
        return []


def adjust_positions(context, selected):
    for stock in list(context.portfolio.positions.keys()):
        if stock not in selected:
            order_target(stock, 0)
    for stock in selected:
        if stock not in context.portfolio.positions:
            order_target_percent(stock, context.position_size)


def clear_all(context):
    for stock in list(context.portfolio.positions.keys()):
        order_target(stock, 0)
