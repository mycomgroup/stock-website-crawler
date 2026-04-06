# 风险及免责提示：该策略由聚宽用户在聚宽社区分享，仅供学习交流使用。
# 原文一般包含策略说明，如有疑问请到原文和作者交流讨论。
# 原文网址：https://www.joinquant.com/post/46876
# 标题：大市值价值投资优化一波
# 作者：七八十

# 原文网址：https://www.joinquant.com/post/41921
# 标题：大市值价值投资，从2005年至今超额稳定
# 作者：Ahfu

# 米筐平台移植版本

"""
一直担心天天想着年化N倍的圣杯策略，到最后发现都是白折腾，徒耗光阴，蓦然回首还是价值投资才是最终的归宿？毕竟这条路上有无数成功的先例。

思路：
1、选上市200天以上主板成熟个股；
2、价格低于价值（pb< 1）；
3、公司真的在不断赚钱，赚真钱，主要用到：
（1）经营现金流：这个比利润真实，不像利润容易作假；
（2）扣非净利润：别靠做账做出假利润；
（3）总资产收益率：别靠负债做高ROE；
（4）净利润同比增长：说明经营良好；

再加上排序指标，取前5支，每月调仓。

随着股市波动，在大牛市顶端会自动空仓留住利润，因为那个位置选不出有价值的票了。
"""

import datetime


def init(context):
    # 设定沪深300作为基准

    print('初始函数开始运行且全局只运行一次')

    # 股票池
    context.buy_stock_count = 1
    context.check_out_lists = []

    # 国债 ETF
    context.etf = "511010.XSHG"

    # 昨日涨停列表
    context.yesterday_HL_list = []

    # 月份追踪（用于手动判断每月调仓）
    context.last_rebalance_month = -1

    # 定时任务
    scheduler.run_daily(before_market_open, time_rule=market_open(minute=0))   # 9:00
    scheduler.run_daily(check_limit_up_14, time_rule=market_close(minute=60))    # 14:00
    scheduler.run_daily(check_limit_up_1450, time_rule=market_close(minute=10))  # 14:50


def handle_bar(context, bar_dict):
    # 每月第一个交易日执行选股+交易
    today = context.now
    if context.last_rebalance_month != today.month:
        context.last_rebalance_month = today.month
        check_stocks(context, bar_dict)
        my_trade(context, bar_dict)


## 开盘前运行函数
def before_market_open(context, bar_dict):
    # 获取股票已持有列表（排除ETF）
    hold_list = [s for s in context.portfolio.positions if s != context.etf]

    # 获取昨日涨停列表
    context.yesterday_HL_list = []
    for stock in hold_list:
        try:
            closes = history_bars(stock, 1, '1d', 'close')
            _pre_stock = history_bars(stock, 1, '1d', 'close')
            limit_ups = _pre_stock * 1.1 if _pre_stock is not None else None
            if closes is not None and limit_ups is not None and len(closes) > 0 and len(limit_ups) > 0:
                if abs(closes[-1] - limit_ups[-1]) < 0.01:
                    context.yesterday_HL_list.append(stock)
        except Exception:
            continue


## 开盘时运行函数
def my_trade(context, bar_dict):
    # 过滤涨跌停
    stocks = filter_limitup_stock(context, bar_dict, context.check_out_lists)
    stocks = filter_limitdown_stock(context, bar_dict, stocks)

    # 卖出不在目标池的持仓
    for stock in list(context.portfolio.positions.keys()):
        if stock == context.etf:
            continue

        if stock in stocks:
            print("已持仓，本次不买入：[%s]" % stock)
            continue

        if stock in context.yesterday_HL_list:
            continue

        # 判断是否涨停
        _pre_stock = history_bars(stock, 1, '1d', 'close')
        bars = _pre_stock * 1.1 if _pre_stock is not None else None
        if bars is None or len(bars) == 0:
            order_target_value(stock, 0)
            continue

        limit_up_price = bars[-1]
        last_price = bar_dict[stock].close if stock in bar_dict else None

        if last_price is not None and last_price < limit_up_price:
            print("调出平仓：[%s]" % stock)
            order_target_value(stock, 0)
        else:
            context.yesterday_HL_list.append(stock)

    # 分仓买入
    position_count = len([s for s in context.portfolio.positions if s != context.etf])
    if context.buy_stock_count > position_count:
        value = context.portfolio.cash / (context.buy_stock_count - position_count)

        for stock in stocks:
            if stock in context.portfolio.positions:
                continue

            order_target_value(stock, value)
            if len([s for s in context.portfolio.positions if s != context.etf]) >= context.buy_stock_count:
                break


def check_limit_up_14(context, bar_dict):
    _check_limit_up(context, bar_dict)


def check_limit_up_1450(context, bar_dict):
    _check_limit_up(context, bar_dict)


def _check_limit_up(context, bar_dict):
    # 对昨日涨停股票观察，如不涨停则提前卖出
    for stock in list(context.yesterday_HL_list):
        if stock not in bar_dict:
            continue

        _pre_stock = history_bars(stock, 1, '1d', 'close')
        bars = _pre_stock * 1.1 if _pre_stock is not None else None
        if bars is None or len(bars) == 0:
            continue

        limit_up_price = bars[-1]
        last_price = bar_dict[stock].close

        if last_price < limit_up_price:
            print("[%s]涨停打开，卖出" % stock)
            order_target_value(stock, 0)
        else:
            print("[%s]涨停，继续持有" % stock)

    # 可用资金买入 ETF
    order_target_value(context.etf, context.portfolio.cash)


def check_stocks(context, bar_dict):
    today = context.now

    # 获取上市满200天的股票：取200个交易日前的日期作为上市截止
    trade_dates = get_trading_dates(
        start_date=today - datetime.timedelta(days=300),
        end_date=today
    )
    if len(trade_dates) >= 200:
        list_before_date = trade_dates[-200]
    else:
        list_before_date = trade_dates[0]

    # 获取全市场股票（上市满200天）
    all_inst = all_instruments('CS')
    all_stocks = all_inst['order_book_id'].tolist()

    # 过滤科创板、北交所、ST、停牌、退市
    filtered = []
    for stock in all_stocks:
        if stock.startswith('68') or stock.startswith('8') or stock.startswith('4'):
            continue
        if stock not in bar_dict:
            continue
        bar = bar_dict[stock]
        if not bar.is_trading:
            continue
        inst = instruments(stock)
        if inst is None:
            continue
        if inst.special_type in ('ST', '*ST'):
            continue
        if '退' in inst.symbol:
            continue
        filtered.append(stock)

    if not filtered:
        context.check_out_lists = []
        return

    # 用 get_factor 获取选股因子
    try:
        factor_df = get_factor(
            filtered,
            ['pb_ratio', 'operating_cash_flow', 'net_profit', 'roa', 'inc_net_profit_year_on_year']
        )
        if factor_df is None or len(factor_df) == 0:
            context.check_out_lists = []
            return
        df = factor_df.groupby(level=0).last().dropna()
    except Exception:
        context.check_out_lists = []
        return

    # 筛选条件
    if df is None or len(df) == 0:
        context.check_out_lists = []
        return
    df = df.dropna()
    df = df[
        (df['pb_ratio'] < 1) &
        (df['operating_cash_flow'] > 1e6) &
        (df['net_profit'] > 1e6) &
        (df['roa'] > 0.15) &
        (df['inc_net_profit_year_on_year'] > 0)
    ]

    # 按 roa 降序排列，取前 buy_stock_count * 3 再截取
    df = df.sort_values('roa', ascending=False)
    candidates = df.index.tolist()[:context.buy_stock_count * 3]

    context.check_out_lists = candidates[:context.buy_stock_count]
    print("今日股票池：%s" % context.check_out_lists)


def filter_limitup_stock(context, bar_dict, stock_list):
    result = []
    for stock in stock_list:
        if stock in context.portfolio.positions:
            result.append(stock)
            continue
        if stock not in bar_dict:
            continue
        _pre_stock = history_bars(stock, 1, '1d', 'close')
        bars = _pre_stock * 1.1 if _pre_stock is not None else None
        if bars is None or len(bars) == 0:
            result.append(stock)
            continue
        if bar_dict[stock].close < bars[-1]:
            result.append(stock)
    return result


def filter_limitdown_stock(context, bar_dict, stock_list):
    result = []
    for stock in stock_list:
        if stock in context.portfolio.positions:
            result.append(stock)
            continue
        if stock not in bar_dict:
            continue
        _pre_stock = history_bars(stock, 1, '1d', 'close')
        bars = _pre_stock * 0.9 if _pre_stock is not None else None
        if bars is None or len(bars) == 0:
            result.append(stock)
            continue
        if bar_dict[stock].close > bars[-1]:
            result.append(stock)
    return result
