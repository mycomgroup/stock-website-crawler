# 龙头底分型战法 - RiceQuant策略编辑器版本
# 完整回测：2021-2026

import numpy as np


def init(context):
    context.benchmark = "000300.XSHG"
    context.max_holdings = 1
    context.hold_days = {}

    # 每日选股
    scheduler.run_daily(select_stocks, time_rule=market_open(minute=5))
    # 尾盘卖出检查
    scheduler.run_daily(check_sell, time_rule=market_close(minute=10))


def select_stocks(context, bar_dict):
    if len(context.portfolio.positions) >= context.max_holdings:
        return

    today = context.now.date()
    date_str = today.strftime("%Y-%m-%d")

    # 获取所有股票
    all_stocks_df = all_instruments("CS", date_str)
    stock_list = all_stocks_df["order_book_id"].tolist()

    # 排除科创板、创业板
    stock_list = [
        s for s in stock_list if not (s.startswith("68") or s.startswith("300"))
    ]

    # 筛选涨停股票
    limit_up_stocks = []
    sample_size = min(500, len(stock_list))

    for stock in stock_list[:sample_size]:
        try:
            bars = history_bars(stock, 1, "1d", ["close", "high_limit"], date_str)
            if bars is not None and len(bars) > 0:
                close = bars[-1]["close"]
                high_limit = bars[-1]["high_limit"]
                if close >= high_limit * 0.995:
                    limit_up_stocks.append(stock)
        except:
            pass

    if len(limit_up_stocks) == 0:
        return

    # 检查底分型
    signals = []
    for stock in limit_up_stocks[:30]:
        try:
            # 获取最近3天数据
            bars_3 = history_bars(
                stock, 3, "1d", ["open", "close", "high", "low", "high_limit"], date_str
            )
            if bars_3 is None or len(bars_3) < 3:
                continue

            # 获取60日数据
            bars_60 = history_bars(stock, 60, "1d", ["close"], date_str)
            if bars_60 is None or len(bars_60) < 60:
                continue

            ma60 = np.mean([b["close"] for b in bars_60])

            # T-2日（十字星）
            t2 = bars_3[1]
            t2_close = t2["close"]
            t2_open = t2["open"]
            t2_high = t2["high"]
            t2_low = t2["low"]

            body_ratio = abs(t2_close - t2_open) / ((t2_close + t2_open) / 2)
            swing_ratio = abs(t2_high - t2_low) / ((t2_high + t2_low) / 2)

            # T-1日（涨停）
            t1 = bars_3[2]
            t1_close = t1["close"]
            t1_open = t1["open"]
            t1_high_limit = t1["high_limit"]

            # 底分型条件（简化）
            is_doji = body_ratio < 0.03 and swing_ratio < 0.10
            above_ma60 = t2_close > ma60
            is_limit_up = t1_close >= t1_high_limit * 0.995
            gap_up = t1_open > t2_close * 1.02
            strong_close = t1_close > t2_close * 1.05

            if is_doji and above_ma60 and is_limit_up and gap_up and strong_close:
                signals.append(stock)

        except:
            pass

    if len(signals) == 0:
        return

    # 选择第一只信号股
    target = signals[0]

    # 检查是否可交易
    if target not in bar_dict:
        return

    bar = bar_dict[target]
    if not bar.is_trading:
        return

    # 检查开盘是否高开
    if bar.open < bar_dict[target].last_price * 1.01:
        return

    # 买入
    try:
        order_value(target, context.portfolio.cash * 0.95)
        context.hold_days[target] = 0
        logger.info(f"{date_str}: 买入 {target}")
    except Exception as e:
        logger.info(f"买入失败: {e}")


def check_sell(context, bar_dict):
    positions = list(context.portfolio.positions.keys())

    for stock in positions:
        if stock not in context.portfolio.positions:
            continue

        pos = context.portfolio.positions[stock]
        if pos.sellable_quantity == 0:
            continue

        # 增加持仓天数
        context.hold_days[stock] = context.hold_days.get(stock, 0) + 1

        # 获取当前价格
        if stock not in bar_dict:
            continue

        bar = bar_dict[stock]
        current_price = bar.last

        # 止损：亏损5%
        if current_price < pos.avg_price * 0.95:
            order_target_value(stock, 0)
            logger.info(f"止损卖出 {stock}")
            continue

        # 止盈：盈利40%
        if current_price > pos.avg_price * 1.4:
            order_target_value(stock, 0)
            logger.info(f"止盈卖出 {stock} @ {current_price:.2f}")
            continue

        # 时间止损：持有超过5天且未涨停
        if context.hold_days[stock] >= 5:
            if stock in bar_dict:
                if bar_dict[stock].last < bar_dict[stock].limit_up * 0.99:
                    order_target_value(stock, 0)
                    logger.info(f"时间止盈 {stock}")
