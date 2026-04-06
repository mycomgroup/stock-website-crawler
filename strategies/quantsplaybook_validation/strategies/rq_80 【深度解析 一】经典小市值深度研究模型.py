# 风险及免责提示：该策略由聚宽用户在聚宽社区分享，仅供学习交流使用。
# 原文一般包含策略说明，如有疑问请到原文和作者交流讨论。
# 原文网址：https://www.joinquant.com/post/44300
# 标题：【深度解析 一】经典小市值模型
# 作者：加百力

# 回测资金 10000000


# 初始化函数，设置基准等等
# context 是由系统维护的上下文环境
# 包含买入均价、持仓情况、可用资金等资产组合相关信息
def init(context):

    # context. 开头的是全局变量
    # 一经声明整个程序都可以使用

    # 设置持股数量
    context.stocknum = 10

    # 待买入股票列表
    context.buylist = []
    context.instruments_df = all_instruments('CS').set_index('order_book_id')

    # 设置沪深300股指作为基准
    # 如果不设置，默认的基准也是沪深300股指

    # 开启动态复权模式(使用真实价格)

    # 交易量不超过实际成交量的 0.1

    # 在日志中写入字符串
    # 整个回测过程中，只会在开始阶段写入一次
    print('初始函数开始运行且全局只运行一次')

    # 设置滑点
    # 0.02 的滑点设置还比较高

    # 止损函数在每个交易日的 9:45 都被调用一次
    # 主要是为了尽量控制风险
    # 止损函数调用时间在开仓、调仓函数之前
    scheduler.run_daily(stoploss, time_rule=market_open(minute=45))
    scheduler.run_weekly(filter_stocks, weekday=1, time_rule=market_open(minute=30))
    scheduler.run_weekly(market_open_func, weekday=1, time_rule=market_open(minute=31))


def handle_bar(context, bar_dict):
    pass



## 筛选、排序股票，生成待交易股票列表
def filter_stocks(context, bar_dict):

    # 在日志中输出该函数运行的时间
    # 回测历史数据时就是当时的日期时间
    print(str('函数运行时间（filter_stocks）:' + str(context.now.time())))


    # 获取当前时间的行情数据
    # 获取当前单位时间（当天/当前分钟）的涨跌停价, 是否停牌，当天的开盘价等
    # 回测时, 通过其他获取数据的API获取到的是前一个单位时间(天/分钟)的数据
    # 而有些数据, 我们在这个单位时间是知道的, 比如涨跌停价, 是否停牌, 当天的开盘价

    # 获取 上证综指和深证综指 的成份股
    # 这个股票范围也很关键
    # 如果换成其他一些股票指数的成分股，收益率可能大幅下降
    components = (index_components('000001.XSHG') or []) + (index_components('399106.XSHE') or [])
    instrument_df = context.instruments_df
    available = [stock for stock in components if stock in instrument_df.index]
    if not available:
        return
    instrument_df = instrument_df.loc[available]
    instrument_df = instrument_df[instrument_df['status'] == 'Active']
    instrument_df = instrument_df[~instrument_df.index.astype(str).str.startswith(('688', '4', '8'))]
    stocks = instrument_df.index.tolist()
    if not stocks:
        return

    try:
        factor_df = get_factor(stocks, ['market_cap'])
        if factor_df is None or factor_df.empty:
            return
        cap_df = factor_df.groupby(level=0).last().dropna()
        if not hasattr(cap_df, 'columns'):
            cap_df = cap_df.to_frame(name='market_cap')
        cap_df = cap_df[cap_df['market_cap'] > 0]
        cap_df = cap_df.sort_values('market_cap').head(context.stocknum * 40)
        scu = [stock for stock in cap_df.index.tolist() if stock in instrument_df.index]
    except Exception:
        return
    if not scu:
        return


    # 过滤 开盘就涨停、跌停 的股票
    # 过滤 当日暂停交易 的股票
    # 过滤 含有 ST、* 及退市标签 的股票
    # 外围 [] 用于生成列表
    # 内部是一个 for...in 表达式
    # 针对 scu 股票列表中的每一只股票代码做分析过滤
    # 括号里面是连续的 or 逻辑表达式，只要满足一个条件就为 True
    # 小括号外面 not 取否。任何一个条件成立都会被过滤掉
    filtered_scu = []
    for stock in scu:
        stock_info = instrument_df.loc[stock]
        stock_name = str(stock_info.get('symbol', '') or '')
        stock_special_type = str(stock_info.get('special_type', '') or '')

        close_bars = history_bars(stock, 1, '1d', 'close')
        if close_bars is None or len(close_bars) == 0:
            continue
        close = float(close_bars[-1])
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and getattr(bar, 'is_trading', False):
            day_open = float(getattr(bar, 'open', close))
            is_paused = False
        else:
            day_open = close
            is_paused = True
        limit_up = close * 1.1
        limit_down = close * 0.9

        # 过滤条件
        if not (
                (day_open == limit_up) or
                (day_open == limit_down) or
                is_paused or
                ('ST' in stock_special_type) or
                ('*' in stock_name) or
                ('退' in stock_name)
        ):
            filtered_scu.append(stock)

    scu = filtered_scu



    if len(filtered_scu) == 0:
        return
    context.buylist = list(filtered_scu)[:context.stocknum]


# 止损函数
# 每天检查是否有股票触发止损条件
# 如有触发则立即卖出平仓
def stoploss(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        cost = pos.avg_price
        if cost <= 0:
            continue
        bar_s = (bar_dict[stock] if stock in bar_dict else None)
        price = bar_s.close if bar_s else pos.avg_price
        ret = price / cost - 1
        if ret < -0.2:
            order_target_value(stock, 0)
            print('触发止损')



def market_open_func(context, bar_dict):
    print('函数运行时间（market_open）:' + str(context.now.time()))
    if len(context.buylist) == 0:
        return
    rebalance(context, context.buylist)



# 调仓 rebalance() 函数
# 第一个参数为上下文环境
# 第二个参数为待买入股票列表
def rebalance(context,buylist):

    # 根据当前资产组合的价值，计算每只股票应持仓金额
    every_stock = context.portfolio.total_value / len(buylist)

    # 如果当前没有持仓就全部买入。等额分配资金
    if len(list(context.portfolio.positions.keys())) == 0 :

        # for 循环对待买入列表中的每只股票都进行购买操作
        for stock_to_buy in buylist :

            # 根据 every_stock 价值买入股票
            order_target_value(stock_to_buy, every_stock)

    # 如果有持仓，先卖出已经持有但不在待买入列表中的股票
    # 卖出已经过时的股票
    else:

        # 遍历每一只持仓股票代码
        for stock_to_sell in list(context.portfolio.positions.keys()):

            # 如果这只股票代码不在买入列表中，说明已经过时应该清仓
            if stock_to_sell not in buylist:

                # 清仓这只股票
                # 股票的持仓价值额度为0
                order_target_value(stock_to_sell, 0)

        # 为buylist里的每支股票调整仓位
        # 这句非常重要
        # 一方面会买入当前未持仓的列表中的股票
        # 另一方面也会影响其他持仓股票的仓位
        # 低于资产组合平均价值的股票会加仓
        # 高于资产组合平均价值的股票会减仓
        # 实验证明调仓对于提高收益率很有帮助
        for i in buylist:
            order_target_value(i, every_stock)
