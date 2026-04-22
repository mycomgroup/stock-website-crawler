# 首板低开策略-终极版 - RiceQuant版本
# 原文：https://www.joinquant.com/post/49434
# 作者：蓝猫量化
# 逻辑：找昨日涨停（首板）、今日低开的股票，过滤ST/停牌/市值，
#       按动量排序买入前5只，止损-6%，最多持有3天

import numpy as np


def init(context):
    # set_benchmark removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    # set_option removed (not needed in RQ)
    context.stock_num = 5
    context.stop_loss = 0.06       # 止损比例
    context.max_hold_days = 3      # 最大持仓天数
    context.cap_min = 10e8         # 最小市值 10亿
    context.cap_max = 100e8        # 最大市值 100亿
    # 记录每只股票的买入价和持仓天数
    context.buy_price = {}
    context.hold_days = {}
    scheduler.run_daily(my_trade, time_rule=market_open(minute=5))


def handle_bar(context, bar_dict):
    pass


# ── 判断昨日是否涨停 ──────────────────────────────────────────────────────────

def _was_limit_up_yesterday(stock):
    """取最近2日收盘价，判断昨日是否涨停（涨幅 >= 9.5%）"""
    data_close = history_bars(stock, 3, '1d', 'close')
    data_high = history_bars(stock, 3, '1d', 'high')
    if data_close is None or data_high is None or len(data_close) < 3:
        return False
    prev_close = data_close[-3]   # 前天收盘
    yest_close = data_close[-2]   # 昨天收盘
    yest_high = data_high[-2]
    if prev_close <= 0:
        return False
    pct = (yest_close - prev_close) / prev_close
    # 涨停：涨幅 >= 9.5% 且收盘 == 最高（封板）
    return pct >= 0.095 and abs(yest_close - yest_high) < 0.01


# ── 判断今日是否低开 ──────────────────────────────────────────────────────────

def _is_gap_down_today(stock, bar_dict):
    """今日开盘价 < 昨日收盘价"""
    data = history_bars(stock, 2, '1d', 'close')
    if data is None or len(data) < 2:
        return False
    yest_close = data[-2]
    if stock not in bar_dict:
        return False
    today_open = bar_dict[stock].open
    return today_open < yest_close * 0.999  # 低开至少 0.1%


# ── 市值过滤 ──────────────────────────────────────────────────────────────────

def _in_cap_range(stock, context):
    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            [stock],
            ['market_cap'],
        )
        if factor_df is None or factor_df.empty:
            return False
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return False
        if not hasattr(df, 'columns'):
            df = df.to_frame(name='market_cap')
        cap = df.loc[stock, 'market_cap'] if stock in df.index else None
        if cap is None:
            return False
        return context.cap_min <= cap <= context.cap_max
    except Exception:
        return False
# ── 动量评分 ──────────────────────────────────────────────────────────────────

def _momentum_score(stock):
    closes = history_bars(stock, 6, '1d', 'close')
    if closes is None or len(closes) < 6:
        return 0.0
    return float(closes[-1] / closes[0] - 1)


# ── 止损 & 超期清仓 ───────────────────────────────────────────────────────────

def _check_stop_loss(context, bar_dict):
    for s in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(s)
        if pos is None: continue
        if pos.quantity <= 0:
            continue
        # 持仓天数计数
        context.hold_days[s] = context.hold_days.get(s, 0) + 1
        # 止损
        buy_price = context.buy_price.get(s, pos.avg_price)
        if s in bar_dict:
            current = bar_dict[s].close
            if current > 0 and (current - buy_price) / buy_price <= -context.stop_loss:
                print(f'止损卖出 {s}，亏损 {(current-buy_price)/buy_price:.2%}')
                order_target_value(s, 0)
                context.buy_price.pop(s, None)
                context.hold_days.pop(s, None)
                continue
        # 超期清仓
        if context.hold_days.get(s, 0) >= context.max_hold_days:
            print(f'超期清仓 {s}，持仓 {context.hold_days[s]} 天')
            order_target_value(s, 0)
            context.buy_price.pop(s, None)
            context.hold_days.pop(s, None)


# ── 选股 ──────────────────────────────────────────────────────────────────────

def get_candidates(context, bar_dict):
    instruments_df = all_instruments('CS')
    stock_ids = [s for s in instruments_df['order_book_id'].tolist() if not s.startswith(('688', '4', '8'))]
    # 全A股（排除科创板688、北交所4/8开头、ST）
    instruments_df = all_instruments('CS')['order_book_id'].tolist()
    candidates = []
    for s in stock_ids:
        # 排除科创板、北交所
        code = s.split('.')[0]
        if code.startswith('688') or code.startswith('4') or code.startswith('8'):
            continue
        # 排除ST
        try:
            info = instruments(s)
            if info is None:
                continue
            if 'ST' in info.symbol or '*' in info.symbol:
                continue
        except Exception:
            continue
        if s not in bar_dict or not bar_dict[s].is_trading:
            continue
        try:
            if not _was_limit_up_yesterday(s):
                continue
            if not _is_gap_down_today(s, bar_dict):
                continue
            if not _in_cap_range(s, context):
                continue
            candidates.append(s)
        except Exception:
            continue

    # 按动量排序
    scored = [(s, _momentum_score(s)) for s in candidates]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in scored[: context.stock_num]]


# ── 交易主函数 ────────────────────────────────────────────────────────────────

def my_trade(context, bar_dict):
    # 先检查止损和超期
    _check_stop_loss(context, bar_dict)

    # 当前持仓数量
    current_positions = [s for s, p in context.portfolio.positions.items() if p.quantity > 0]
    slots = context.stock_num - len(current_positions)
    if slots <= 0:
        return

    target = get_candidates(context, bar_dict)
    # 只买还没持有的
    to_buy = [s for s in target if s not in current_positions][:slots]
    if not to_buy:
        return

    per_value = context.portfolio.total_value * 0.95 / context.stock_num
    for s in to_buy:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, per_value)
            context.buy_price[s] = bar_dict[s].open
            context.hold_days[s] = 0
            print(f'买入首板低开股 {s}')
