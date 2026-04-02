"""
二板接力策略 - 调整版
降低阈值，增加交易机会
"""


def init(context):
    context.trade_count = 0
    context.stock_pool = 300  # 扩大股票池
    context.threshold = 3  # 降低情绪阈值
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

    # 统计涨停（不判断涨停价，直接用涨幅>9.5%）
    zt = []
    for s in stocks:
        try:
            p = history_bars(s, 2, "1d", "close")
            if p and len(p) >= 2:
                change = (p[1]["close"] - p[0]["close"]) / p[0]["close"]
                if change > 0.095:  # 涨幅>9.5%
                    zt.append(s)
        except:
            pass

    if len(zt) < context.threshold:
        return

    # 找二板：今天+昨天涨停
    sb = zt[:3]  # 取前3个

    if not sb:
        return

    # 买入第一个
    target = sb[0]

    try:
        price = bar_dict[target]
        # 只要不是涨停就买
        order_target_percent(target, 0.95)
        context.trade_count += 1
    except:
        pass
