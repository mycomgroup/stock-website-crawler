"""
影子策略简化版 - Ricequant回测
主线策略：假弱高开 + 情绪开关
观察线策略：二板策略
"""

import pandas as pd
import numpy as np


def init(context):
    context.strategy_mode = "mainline"
    context.limit_up_count = 0
    context.consecutive_losses = 0
    context.stop_trading_until = None

    scheduler.run_daily(check_emotion, time_rule=market_open(minute=1))
    scheduler.run_daily(generate_signals, time_rule=market_open(minute=5))
    scheduler.run_daily(check_sell, time_rule=market_close(minute=5))


def get_candidate_pool(context, bar_dict):
    """
    获取候选池：沪深300 + 中证500
    """
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300) | set(zz500))

        # 过滤
        valid_stocks = []
        for stock in stocks:
            if stock.startswith("688"):  # 排除科创板
                continue
            if stock not in bar_dict:
                continue
            bar = bar_dict[stock]
            if bar.is_trading is False:
                continue

            # 排除ST
            try:
                inst = instruments(stock)
                if "ST" in inst.symbol or "*" in inst.symbol:
                    continue
            except:
                continue

            valid_stocks.append(stock)

        return valid_stocks[:200]  # 限制数量
    except Exception as e:
        return []


def check_emotion(context, bar_dict):
    """
    检查情绪：涨停家数
    """
    try:
        stocks = get_candidate_pool(context, bar_dict)
        limit_up_count = 0

        for stock in stocks:
            try:
                hist = history_bars(stock, 2, "1d", "close")
                if hist and len(hist) >= 2:
                    prev_close = hist[-2]
                    curr_close = hist[-1]
                    if prev_close > 0:
                        pct = (curr_close - prev_close) / prev_close
                        if pct >= 0.095:
                            limit_up_count += 1
            except:
                continue

        context.limit_up_count = limit_up_count
    except Exception as e:
        context.limit_up_count = 0


def generate_signals(context, bar_dict):
    """
    生成信号并买入
    """
    # 检查停手
    if context.stop_trading_until and context.now < context.stop_trading_until:
        return

    # 检查持仓数量
    if len(context.portfolio.positions) >= 3:
        return

    stocks = get_candidate_pool(context, bar_dict)
    signals = []

    for stock in stocks:
        try:
            # 主线策略：假弱高开
            if context.strategy_mode == "mainline":
                # 情绪过滤
                if context.limit_up_count < 30:
                    continue

                # 假弱高开判断
                hist = history_bars(stock, 2, "1d", "close")
                if not hist or len(hist) < 2:
                    continue

                prev_close = hist[-2]
                open_price = bar_dict[stock].open

                if prev_close > 0:
                    open_change = (open_price - prev_close) / prev_close

                    # 开盘涨幅 0.1%-3%
                    if 0.001 < open_change < 0.03:
                        # 有上涨空间
                        if bar_dict[stock].high > open_price:
                            signals.append(stock)

            # 观察线策略：二板
            elif context.strategy_mode == "observation":
                hist = history_bars(stock, 5, "1d", "close")
                if not hist or len(hist) < 5:
                    continue

                # 计算连板
                boards = 0
                for i in range(len(hist) - 1):
                    if hist[i] > 0:
                        pct = (hist[i + 1] - hist[i]) / hist[i]
                        if pct >= 0.095:
                            boards += 1
                        else:
                            break

                # 只做二板
                if boards == 2:
                    signals.append(stock)

        except:
            continue

    # 买入（最多1只）
    if signals:
        stock = signals[0]
        price = bar_dict[stock].close
        max_amount = min(100000, context.portfolio.total_value * 0.3)
        shares = int(max_amount / price / 100) * 100

        if shares > 0:
            order_shares(stock, shares)


def check_sell(context, bar_dict):
    """
    检查卖出规则
    """
    to_sell = []

    for stock in context.portfolio.positions:
        pos = context.portfolio.positions[stock]
        buy_price = pos.avg_price
        curr_price = bar_dict[stock].close

        profit_pct = (curr_price - buy_price) / buy_price

        # 主线：冲高+3%即卖或次日卖
        if context.strategy_mode == "mainline":
            if profit_pct >= 0.03:
                to_sell.append(stock)
            else:
                hold_days = (context.now - pos.entry_date).days
                if hold_days >= 1:
                    to_sell.append(stock)

        # 观察线：次日卖
        elif context.strategy_mode == "observation":
            hold_days = (context.now - pos.entry_date).days
            if hold_days >= 1:
                to_sell.append(stock)

    # 执行卖出
    for stock in to_sell:
        pos = context.portfolio.positions[stock]
        profit = (bar_dict[stock].close - pos.avg_price) * pos.quantity

        order_shares(stock, -pos.quantity)

        # 更新连亏
        if profit < 0:
            context.consecutive_losses += 1
        else:
            context.consecutive_losses = 0

    # 停手机制
    if context.consecutive_losses >= 3:
        context.stop_trading_until = context.now + pd.Timedelta(days=3)
        context.consecutive_losses = 0


def after_trading(context, bar_dict):
    """
    每日收盘后记录
    """
    pass
