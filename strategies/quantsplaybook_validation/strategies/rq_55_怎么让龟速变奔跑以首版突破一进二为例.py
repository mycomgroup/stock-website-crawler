# RiceQuant策略 - 怎么让龟速变奔跑？以"首版突破一进二"为例
# 原文：https://www.joinquant.com/post/45733
# 作者：jqz1226


def init(context):

    context.help_stock = {}  # dict: {股票代码: 今日涨停价}
    context.max_stock_num = 20
    # 用中证500/1000替代全市场扫描，兼顾短线活跃度和平台负载。
    stock_pool = list(dict.fromkeys((index_components('000905.XSHG') or []) + (index_components('000852.XSHG') or [])))
    instruments_df = all_instruments('CS').set_index('order_book_id')
    context.stock_pool = []
    for stock in stock_pool:
        if not isinstance(stock, str) or stock.startswith(('688', '4', '8')):
            continue
        if stock not in instruments_df.index:
            continue
        info = instruments_df.loc[stock]
        symbol = str(info.get('symbol', '') or '')
        special_type = str(info.get('special_type', '') or '')
        if 'ST' in symbol or '退' in symbol or special_type in ('PT', 'StarST'):
            continue
        context.stock_pool.append(stock)
    print('初始化股票池数量:', len(context.stock_pool))

    scheduler.run_daily(before_market_open, time_rule=market_open(minute=0))
    scheduler.run_daily(market_run, time_rule=market_open(minute=2))


def handle_bar(context, bar_dict):
    pass


def before_market_open(context, bar_dict):
    """盘前准备：找昨日涨停股"""
    context.help_stock = {}
    for stock in context.stock_pool:
        try:
            bars = history_bars(stock, 1, '1d', ['close', 'limit_up'])
            if bars is None or len(bars) == 0:
                continue
            close = float(bars[-1]['close'])
            limit_up = float(bars[-1]['limit_up'])
            if limit_up > 0 and abs(close - limit_up) / limit_up < 0.005:
                context.help_stock[stock] = limit_up
        except Exception:
            continue
    print('昨日涨停候选数:', len(context.help_stock))


def market_run(context, bar_dict):
    """盘中运行"""
    # 买入
    cash = context.portfolio.cash
    if cash > 5000 and len(context.portfolio.positions) < context.max_stock_num:
        for stock in context.help_stock:
            if stock in context.portfolio.positions:
                continue
            if stock not in bar_dict:
                continue
            try:
                bar = bar_dict[stock]
                last_price = getattr(bar, 'close', None)
                if last_price is None or not getattr(bar, 'is_trading', False):
                    continue
                if last_price >= context.help_stock[stock] * 0.995:
                    function_buy(context, stock)
            except Exception:
                continue

    # 卖出
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        sellable_qty = getattr(pos, 'sellable_quantity', None)
        if sellable_qty is None:
            sellable_qty = getattr(pos, 'quantity', 0)
        if sellable_qty <= 0:
            continue
        if stock not in bar_dict:
            continue
        try:
            bar = bar_dict[stock]
            today_limit_up = getattr(bar, 'limit_up', None)
            last_price = getattr(bar, 'close', None)
            if today_limit_up is None or last_price is None:
                continue
            if last_price < today_limit_up * 0.995:
                order_target_value(stock, 0)
        except Exception:
            continue


def function_buy(context, stock):
    """买入函数"""
    cash = context.portfolio.cash
    if cash > 5000:
        num_to_buy = max(1, context.max_stock_num - len(context.portfolio.positions))
        order_target_value(stock, min(cash / num_to_buy, cash))
