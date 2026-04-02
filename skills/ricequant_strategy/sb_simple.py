"""
二板接力策略 - 简化版
"""


def init(context):
    context.trade_count = 0
    context.stock_pool = 200
    context.threshold = 10
    context.volume_ratio = 1.875


def handle_bar(context, bar_dict):
    date = context.now.date()

    # 卖出持仓
    for stock in list(context.portfolio.positions.keys()):
        order_target_percent(stock, 0)

    # 获取股票
    stocks = all_instruments("CS")["order_book_id"].tolist()
    stocks = [
        s for s in stocks if isinstance(s, str) and not s.startswith(("688", "4", "8"))
    ][: context.stock_pool]

    # 统计涨停
    zt = []
    for s in stocks:
        try:
            p = history_bars(s, 1, "1d", "close,limit_up")
            if p and p[0]["close"] >= p[0]["limit_up"] * 0.99:
                zt.append(s)
        except:
            pass

    if len(zt) < context.threshold:
        return

    # 找二板（简化：只看昨天涨停）
    prev_zt = []
    for s in stocks:
        try:
            p = history_bars(s, 2, "1d", "close,limit_up")
            if p and len(p) >= 2 and p[1]["close"] >= p[1]["limit_up"] * 0.99:
                prev_zt.append(s)
        except:
            pass

    # 二板 = 今天+昨天涨停
    sb = list(set(zt) & set(prev_zt))[:1]

    if not sb:
        return

    # 买入第一个
    target = sb[0]

    try:
        price = bar_dict[target]
        if price.last_price < price.limit_up * 0.99:
            order_target_percent(target, 0.95)
            context.trade_count += 1
    except:
        pass
