# RiceQuant策略迁移
# 原文标题：海龟突破系统，19-21年化150，无未来函数和过拟合
# 原文作者：Trading Robot
# 原文网址：https://www.joinquant.com/post/33654

# 管道突破系统
# 1.选股。选取沪深300的股票，突破55日最高价买入，突破21日最低价卖出
# 2.仓位控制 买入当前仓位的0.25

import pandas as pd

def init(context):
    print('初始函数开始运行且全局只运行一次')
    context.security = None
    context.security_initialized = False
    context.p55 = 81
    scheduler.run_daily(chicang, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    if not context.security_initialized:
        context.security = index_components('000300.XSHG')
        if not context.security:
            # Fallback: use a broad set of A-share stocks
            _instr = all_instruments('CS')
            context.security = [s for s in _instr['order_book_id'].tolist()
                                 if not s.startswith(('688', '4', '8', '3'))][:300]
        context.security_initialized = True


def chicang(context, bar_dict):
    # 先处理止损止盈（快照持仓列表，避免迭代中修改）
    need_reselect = False
    for stock in list(context.portfolio.positions.keys()):
        print('当前持仓总数%s,代码%s' % (len(context.portfolio.positions), stock))
        bar_close = history_bars(stock, 1, '1d', 'close')
        bar_open = history_bars(stock, 1, '1d', 'open')
        bar_high = history_bars(stock, 1, '1d', 'high')
        bar_low = history_bars(stock, 1, '1d', 'low')
        if bar_close is None or bar_open is None or bar_high is None or bar_low is None:
            continue
        p = bar_close[-1]
        pos = context.portfolio.positions.get(stock)
        cost = pos.avg_cost if pos else 0
        if cost == 0:
            continue
        df5_high = history_bars(stock, 3, '1d', 'high')
        df5_low = history_bars(stock, 3, '1d', 'low')
        if df5_high is None or df5_low is None:
            continue
        bf_p = ((df5_high - df5_low) / df5_low).max()
        stop_p1 = cost * (1 - abs(bf_p))
        stop_p2 = cost * (1 + abs(bf_p * 2))
        if p <= stop_p1:
            print('止损卖出，然后选股')
            order_target_value(stock, 0)
            need_reselect = True
        elif p >= stop_p2:
            order_target_value(stock, 0)
            print('止盈卖出，然后选股')
            need_reselect = True

    # 无持仓或触发止损/止盈后重新选股
    if len(context.portfolio.positions) < 1 or need_reselect:
        print('当前不持仓，开始选股')
        choice_stock(context, bar_dict)


def choice_stock(context, bar_dict):
    if context.security is None:
        return
    list_stock = []
    for stock in context.security:
        if '300' in str(stock)[0:3] or '900' in str(stock)[0:3] or '688' in str(stock)[0:3] or '200' in str(stock)[0:3]:
            continue
        bar_close = history_bars(stock, 1, '1d', 'close')
        bar_open = history_bars(stock, 1, '1d', 'open')
        if bar_close is None or bar_open is None:
            continue
        if len(bar_close) == 0 or len(bar_open) == 0:
            continue
        p = bar_close[-1]
        df55_close = history_bars(stock, context.p55, '1d', 'close')
        df55_high = history_bars(stock, context.p55, '1d', 'high')
        if df55_close is None or df55_high is None or len(df55_close) == 0 or len(df55_high) == 0:
            continue
        df1 = history_bars(stock, 9, '1d', 'close')
        if df1 is None or len(df1) < 2:
            continue
        zdf = (df1[-1] - df1[0]) / df1[0]
        p_max = df55_high.max()
        if p > p_max and zdf < 0:
            list_stock.append(stock)

    if not list_stock:
        return

    # Sort by PE ratio (get fundamentals for list_stock)
    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            list_stock,
            ['pe_ratio'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df.head(len(list_stock))
        candidates = df.index.tolist()
        if df is not None and len(df) > 0:
            df = df[df['pe_ratio'] > 0]
            pe_series = df['pe_ratio'].sort_values(ascending=False)
            list_pe = pe_series.index.tolist()
        else:
            list_pe = list_stock
    except Exception:
        list_pe = list_stock

    for stock in list_pe[0:1]:
        print('买入股票' + stock)
        order_target_value(stock, context.portfolio.cash)
        print('当前持仓%s' % context.portfolio.positions)
