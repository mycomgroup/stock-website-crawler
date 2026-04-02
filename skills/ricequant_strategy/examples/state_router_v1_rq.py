# 状态路由器 v1 - RiceQuant 实时验证版本
# 优化：批量获取数据，减少API调用次数

import rqalpha as rq
from rqalpha.api import *
import pandas as pd
import numpy as np


def init(context):
    context.state = "正常"
    context.target_position = 0.7
    context.hs300_stocks = []
    context.last_breadth_date = None
    context.cached_breadth = 50

    scheduler.run_daily(update_breadth, time_rule=market_open(minute=5))
    scheduler.run_daily(rebalance, time_rule=market_open(minute=10))


def update_breadth(context, bar_dict):
    today = context.now.strftime("%Y-%m-%d")

    if context.last_breadth_date == today:
        return

    try:
        hs300 = index_components("000300.XSHG", today)

        if not hs300:
            context.cached_breadth = 50
            return

        sample_stocks = list(hs300)[:50]

        count_above = 0
        total = 0

        for stock in sample_stocks:
            try:
                prices = history_bars(stock, 21, "1d", "close")
                if prices is not None and len(prices) >= 21:
                    ma20 = np.mean(prices[:-1])
                    current = prices[-1]
                    if current > ma20:
                        count_above += 1
                    total += 1
            except:
                continue

        if total > 0:
            context.cached_breadth = count_above / total * 100
        else:
            context.cached_breadth = 50

        context.last_breadth_date = today

    except Exception as e:
        print(f"广度计算错误: {e}")
        context.cached_breadth = 50


def get_zt_count(context, bar_dict):
    try:
        all_stocks = list(all_instruments(type="CS").order_book_id)
        sample = all_stocks[:300]

        zt_count = 0
        for stock in sample:
            try:
                bar = bar_dict[stock]
                if bar.close >= bar.limit_up * 0.995:
                    zt_count += 1
            except:
                continue

        return zt_count
    except:
        return 40


def classify_state(breadth_pct, zt_count):
    if breadth_pct < 15:
        return "关闭", 0.0

    breadth_level = (
        1
        if breadth_pct < 15
        else (2 if breadth_pct < 25 else (3 if breadth_pct < 35 else 4))
    )
    sentiment_level = (
        1 if zt_count < 30 else (2 if zt_count < 50 else (3 if zt_count < 80 else 4))
    )

    if breadth_level == 1:
        return "关闭", 0.0
    elif breadth_level == 2:
        if sentiment_level <= 2:
            return "防守", 0.3
        else:
            return "轻仓", 0.5
    elif breadth_level == 3:
        if sentiment_level == 2:
            return "轻仓", 0.5
        elif sentiment_level == 3:
            return "正常", 0.7
        elif sentiment_level == 4:
            return "进攻", 1.0
        else:
            return "防守", 0.3
    else:
        if sentiment_level == 4:
            return "进攻", 1.0
        elif sentiment_level == 3:
            return "正常", 0.7
        else:
            return "轻仓", 0.5


def rebalance(context, bar_dict):
    breadth_pct = context.cached_breadth
    zt_count = get_zt_count(context, bar_dict)

    state, target_position = classify_state(breadth_pct, zt_count)

    context.state = state
    context.target_position = target_position

    print(
        f"{context.now.date()} | 广度:{breadth_pct:.1f}% | 涨停:{zt_count} | 状态:{state} | 仓位:{target_position * 100:.0f}%"
    )

    portfolio_value = context.portfolio.total_value
    target_value = portfolio_value * target_position

    current_value = 0
    if "000300.XSHG" in context.portfolio.positions:
        current_value = context.portfolio.positions["000300.XSHG"].market_value

    diff_value = target_value - current_value

    if abs(diff_value) > portfolio_value * 0.05:
        if target_position == 0:
            for stock in list(context.portfolio.positions.keys()):
                order_target_percent(stock, 0)
        else:
            order_target_value("000300.XSHG", target_value)


__config__ = {
    "base": {
        "start_date": "2022-01-01",
        "end_date": "2024-12-31",
        "frequency": "1d",
        "accounts": {"stock": 100000},
    },
    "extra": {"log_level": "error"},
    "mod": {"sys_analyser": {"enabled": True, "plot": False}},
}
