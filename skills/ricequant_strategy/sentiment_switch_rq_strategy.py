# 情绪择时框架 - RiceQuant策略编辑器版本
# 验证情绪开关（涨停家数>=30）对首板低开策略的增益

import numpy as np
import pandas as pd


def init(context):
    """策略初始化"""
    print("=" * 80)
    print("情绪择时框架 - RiceQuant策略编辑器版本")
    print("=" * 80)

    # 策略参数
    context.sentiment_threshold = 30  # 涨停家数阈值
    context.lianban_threshold = 2  # 连板数阈值
    context.max_stocks = 3  # 最大持仓数
    context.low_open_min = -5  # 低开下限
    context.low_open_max = -1  # 低开上限

    # 统计变量
    context.total_trades = 0
    context.sentiment_on_days = 0
    context.sentiment_off_days = 0

    # 每日运行
    scheduler.run_daily(rebalance, time_rule=market_open(minute=5))

    print(f"涨停阈值: {context.sentiment_threshold}")
    print(f"连板阈值: {context.lianban_threshold}")
    print(f"最大持仓: {context.max_stocks}")
    print("=" * 80)


def get_zt_count(context, bar_dict):
    """获取涨停家数"""
    zt_count = 0
    max_lianban = 0

    try:
        all_stocks = all_instruments("CS")
        # 限制股票数量避免超时
        check_stocks = all_stocks[:500]

        for stock in check_stocks:
            try:
                # 获取前一日数据
                bars = history_bars(
                    stock.order_book_id, 2, "1d", ["close", "high_limit"]
                )
                if bars is None or len(bars) < 2:
                    continue

                prev_close = bars[-2]["close"]
                prev_limit = bars[-2]["high_limit"]

                # 判断涨停（收盘价接近涨停价）
                if prev_limit > 0 and abs(prev_close - prev_limit) / prev_limit < 0.005:
                    zt_count += 1

                    # 检查连板数（获取更多历史数据）
                    lianban_bars = history_bars(
                        stock.order_book_id, 10, "1d", ["close", "high_limit"]
                    )
                    if lianban_bars is not None:
                        lianban = 1
                        for j in range(len(lianban_bars) - 2, -1, -1):
                            if (
                                abs(
                                    lianban_bars[j]["close"]
                                    - lianban_bars[j]["high_limit"]
                                )
                                / lianban_bars[j]["high_limit"]
                                < 0.005
                            ):
                                lianban += 1
                            else:
                                break
                        if lianban > max_lianban:
                            max_lianban = lianban
            except:
                continue

        return zt_count, max_lianban
    except:
        return 0, 0


def get_low_open_stocks(context, bar_dict, zt_stocks):
    """获取低开股票"""
    candidates = []

    for stock in zt_stocks:
        try:
            # 获取前一日收盘价
            bars = history_bars(stock.order_book_id, 2, "1d", "close")
            if bars is None or len(bars) < 2:
                continue

            prev_close = bars[-2]

            # 获取今日开盘价
            if stock.order_book_id in bar_dict:
                curr_open = bar_dict[stock.order_book_id].open
            else:
                continue

            # 计算开盘涨幅
            open_pct = (curr_open - prev_close) / prev_close * 100

            # 低开条件：-5% ~ -1%
            if context.low_open_min <= open_pct <= context.low_open_max:
                candidates.append({"stock": stock.order_book_id, "open_pct": open_pct})
        except:
            continue

    return candidates


def rebalance(context, bar_dict):
    """每日调仓"""
    # 获取情绪指标
    zt_count, max_lianban = get_zt_count(context, bar_dict)

    # 情绪开关判断
    sentiment_on = (
        zt_count >= context.sentiment_threshold
        and max_lianban >= context.lianban_threshold
    )

    if sentiment_on:
        context.sentiment_on_days += 1
    else:
        context.sentiment_off_days += 1

    # 清仓
    for stock in list(context.portfolio.positions):
        order_target_value(stock, 0)

    # 情绪开启时才开仓
    if sentiment_on:
        # 获取昨日涨停股票
        zt_stocks = []
        all_stocks = all_instruments("CS")[:500]

        for stock in all_stocks:
            try:
                bars = history_bars(
                    stock.order_book_id, 2, "1d", ["close", "high_limit"]
                )
                if bars and len(bars) >= 2:
                    prev_close = bars[-2]["close"]
                    prev_limit = bars[-2]["high_limit"]
                    if (
                        prev_limit > 0
                        and abs(prev_close - prev_limit) / prev_limit < 0.005
                    ):
                        zt_stocks.append(stock)
            except:
                continue

        # 获取低开候选
        candidates = get_low_open_stocks(context, bar_dict, zt_stocks)

        if len(candidates) > 0:
            # 按低开幅度排序（越低越好）
            candidates.sort(key=lambda x: x["open_pct"])

            # 选择前N只
            selected = candidates[: context.max_stocks]

            # 买入
            value = context.portfolio.total_value / context.max_stocks
            for item in selected:
                order_value(item["stock"], value)
                context.total_trades += 1

            print(
                f"{context.now}: 涨停{zt_count}, 连板{max_lianban}, 买入{len(selected)}只"
            )


def after_trading(context, bar_dict):
    """收盘后统计"""
    if context.sentiment_on_days + context.sentiment_off_days == 242:  # 全年交易日
        print("=" * 80)
        print(f"全年统计:")
        print(f"  情绪开启天数: {context.sentiment_on_days}")
        print(f"  情绪关闭天数: {context.sentiment_off_days}")
        print(f"  总交易次数: {context.total_trades}")
        print("=" * 80)
