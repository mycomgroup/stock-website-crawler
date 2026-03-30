# 影子策略 - 回测策略编辑器版本
# Ricequant 平台回测策略编辑器
# 时间范围：2014-01-01 至 2024-12-31
# 初始资金：100000

import pandas as pd
import numpy as np

# 策略参数
MAINLINE_PARAMS = {
    "market_cap_min": 50,  # 亿元
    "market_cap_max": 150,  # 亿元
    "position_limit": 0.30,  # 相对历史最高点
    "emotion_threshold": 30,  # 涨停家数阈值
    "open_change_min": 0.001,  # 开盘涨幅下限 0.1%
    "open_change_max": 0.03,  # 开盘涨幅上限 3%
    "sell_profit_threshold": 0.03,  # 冲高止盈
    "single_position_limit": 100000,  # 单票上限
    "total_position_limit": 300000,  # 总仓上限
}

OBSERVATION_PARAMS = {
    "single_position_limit": 100000,
    "total_position_limit": 300000,
}


def init(context):
    context.strategy_mode = "mainline"  # 'mainline' or 'observation'
    context.limit_up_count = 0
    context.consecutive_losses = 0
    context.stop_trading_until = None
    context.stocks_in_pool = []

    scheduler.run_daily(get_limit_up_count, time_rule=market_open(minute=1))
    scheduler.run_daily(generate_signals, time_rule=market_open(minute=5))
    scheduler.run_daily(check_sell_rules, time_rule=market_close(minute=10))


def get_limit_up_count(context, bar_dict):
    """
    获取涨停股票数量（情绪指标）
    """
    all_stocks = [inst.order_book_id for inst in all_instruments(type="CS")]
    limit_up_count = 0

    for stock in all_stocks[:500]:  # 限制数量避免超时
        try:
            price = history_bars(stock, 2, "1d", "close")
            if price and len(price) >= 2:
                prev_close = price[-2]
                curr_close = price[-1]
                if prev_close > 0:
                    pct_change = (curr_close - prev_close) / prev_close
                    if pct_change >= 0.095:
                        limit_up_count += 1
        except:
            continue

    context.limit_up_count = limit_up_count
    logger.info(f"涨停家数: {limit_up_count}")


def is_fake_weak_high_open(context, stock, bar_dict):
    """
    判断是否为假弱高开
    """
    try:
        price = history_bars(stock, 2, "1d", "close")
        if not price or len(price) < 2:
            return False

        prev_close = price[-2]
        open_price = bar_dict[stock].open

        if prev_close > 0:
            open_change = (open_price - prev_close) / prev_close
        else:
            return False

        # 开盘涨幅 > 0.1% 且 < 3%
        if (
            open_change <= MAINLINE_PARAMS["open_change_min"]
            or open_change >= MAINLINE_PARAMS["open_change_max"]
        ):
            return False

        # 判断是否有上涨空间
        high_price = bar_dict[stock].high
        if high_price > open_price:
            return True

        return False
    except:
        return False


def get_stock_market_cap(stock):
    """
    获取市值（亿元）
    """
    try:
        market_cap = get_factor(
            stock, "market_cap", start_date=context.now, end_date=context.now
        )
        if market_cap and len(market_cap) > 0:
            return market_cap.iloc[0] / 1e8
        return None
    except:
        return None


def get_stock_position_pct(stock):
    """
    获取位置（相对历史最高）
    """
    try:
        prices = history_bars(stock, 250, "1d", "high")
        if prices and len(prices) > 0:
            high_250d = prices.max()
            current_price = prices[-1]
            if high_250d > 0:
                return current_price / high_250d - 1
            return None
        return None
    except:
        return None


def has_consecutive_boards(stock):
    """
    判断是否有连板
    """
    try:
        prices = history_bars(stock, 5, "1d", "close")
        if not prices or len(prices) < 5:
            return False

        # 检查最近2天是否涨停
        for i in range(len(prices) - 2):
            if prices[i] > 0 and prices[i + 1] > 0:
                pct_change = (prices[i + 1] - prices[i]) / prices[i]
                if pct_change >= 0.095:
                    return True
        return False
    except:
        return False


def generate_signals(context, bar_dict):
    """
    生成信号
    """
    if context.stop_trading_until and context.now < context.stop_trading_until:
        logger.info(f"停手期间，不生成信号")
        return

    # 主线策略
    if context.strategy_mode == "mainline":
        # 情绪过滤
        if context.limit_up_count < MAINLINE_PARAMS["emotion_threshold"]:
            logger.info(
                f"涨停家数不足({context.limit_up_count}<{MAINLINE_PARAMS['emotion_threshold']})"
            )
            return

        # 获取候选池
        all_stocks = [inst.order_book_id for inst in all_instruments(type="CS")]
        signals = []

        for stock in all_stocks[:200]:  # 限制数量
            # 市值过滤
            market_cap = get_stock_market_cap(stock)
            if (
                market_cap is None
                or market_cap < MAINLINE_PARAMS["market_cap_min"]
                or market_cap > MAINLINE_PARAMS["market_cap_max"]
            ):
                continue

            # 位置过滤
            position_pct = get_stock_position_pct(stock)
            if position_pct and position_pct > MAINLINE_PARAMS["position_limit"]:
                continue

            # 无连板
            if has_consecutive_boards(stock):
                continue

            # 假弱高开
            if is_fake_weak_high_open(context, stock, bar_dict):
                signals.append(stock)

        context.stocks_in_pool = signals
        logger.info(f"主线信号数量: {len(signals)}")

        # 买入（最多1只）
        if signals and len(context.portfolio.positions) < 3:
            stock = signals[0]
            price = bar_dict[stock].close
            max_amount = min(
                MAINLINE_PARAMS["single_position_limit"],
                MAINLINE_PARAMS["total_position_limit"]
                - get_total_position_value(context),
            )
            shares = int(max_amount / price / 100) * 100

            if shares > 0:
                order_shares(stock, shares)
                logger.info(f"买入 {stock}, 数量 {shares}")

    # 观察线策略
    elif context.strategy_mode == "observation":
        all_stocks = [inst.order_book_id for inst in all_instruments(type="CS")]
        signals = []

        for stock in all_stocks[:200]:
            prices = history_bars(stock, 5, "1d", "close")
            if not prices or len(prices) < 5:
                continue

            # 计算连板数量
            consecutive_boards = 0
            for i in range(len(prices) - 1):
                if prices[i] > 0:
                    pct_change = (prices[i + 1] - prices[i]) / prices[i]
                    if pct_change >= 0.095:
                        consecutive_boards += 1
                    else:
                        break

            # 只做二板
            if consecutive_boards == 2:
                # 排除今日涨停
                curr_close = bar_dict[stock].close
                prev_close = prices[-2]
                if prev_close > 0:
                    pct_today = (curr_close - prev_close) / prev_close
                    if pct_today < 0.095:
                        signals.append(stock)

        context.stocks_in_pool = signals
        logger.info(f"观察线信号数量: {len(signals)}")

        # 买入
        if signals and len(context.portfolio.positions) < 3:
            stock = signals[0]
            price = bar_dict[stock].close
            max_amount = min(
                OBSERVATION_PARAMS["single_position_limit"],
                OBSERVATION_PARAMS["total_position_limit"]
                - get_total_position_value(context),
            )
            shares = int(max_amount / price / 100) * 100

            if shares > 0:
                order_shares(stock, shares)
                logger.info(f"买入 {stock}, 数量 {shares}")


def get_total_position_value(context):
    """
    获取总持仓市值
    """
    total_value = 0
    for stock in context.portfolio.positions:
        total_value += context.portfolio.positions[stock].market_value
    return total_value


def check_sell_rules(context, bar_dict):
    """
    检查卖出规则
    """
    stocks_to_sell = []

    for stock in context.portfolio.positions:
        position = context.portfolio.positions[stock]
        buy_price = position.avg_price
        current_price = bar_dict[stock].close

        profit_pct = (current_price - buy_price) / buy_price

        # 主线：冲高+3%即卖
        if context.strategy_mode == "mainline":
            if profit_pct >= MAINLINE_PARAMS["sell_profit_threshold"]:
                stocks_to_sell.append((stock, "冲高+3%止盈"))
            else:
                # 持仓超过1天，尾盘卖出
                hold_days = (context.now - position.entry_date).days
                if hold_days >= 1:
                    stocks_to_sell.append((stock, "尾盘卖出"))

        # 观察线：次日卖出
        elif context.strategy_mode == "observation":
            hold_days = (context.now - position.entry_date).days
            if hold_days >= 1:
                stocks_to_sell.append((stock, "次日卖出"))

    # 执行卖出
    for stock, reason in stocks_to_sell:
        order_shares(stock, -context.portfolio.positions[stock].quantity)
        logger.info(f"卖出 {stock}, 原因: {reason}")

        # 记录盈亏
        position = context.portfolio.positions.get(stock)
        if position:
            profit = (bar_dict[stock].close - position.avg_price) * position.quantity
            if profit < 0:
                context.consecutive_losses += 1
            else:
                context.consecutive_losses = 0

    # 停手机制
    if context.consecutive_losses >= 3:
        context.stop_trading_until = context.now + pd.Timedelta(days=3)
        context.consecutive_losses = 0
        logger.info(f"连亏3笔，停手3天")


def after_trading(context, bar_dict):
    """
    每日收盘后
    """
    logger.info(f"日期: {context.now}")
    logger.info(f"涨停家数: {context.limit_up_count}")
    logger.info(f"持仓数量: {len(context.portfolio.positions)}")
    logger.info(f"总资产: {context.portfolio.total_value:.2f}")
    logger.info(f"连亏次数: {context.consecutive_losses}")


# 配置
config = {
    "base": {
        "start_date": "2014-01-01",
        "end_date": "2024-12-31",
        "frequency": "1d",
        "accounts": {"stock": 100000},
    },
    "extra": {
        "log_level": "info",
    },
}
