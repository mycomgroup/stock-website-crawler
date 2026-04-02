# -*- coding: utf-8 -*-
"""
风控A/B测试 - RiceQuant策略编辑器版本
基线版（A组）：仅尾盘清仓
"""

import datetime as dt


def init(context):
    context.month_count = 0
    context.last_month = None
    context.trades_count = 0

    print("=== 风控测试A组（基线版）启动 ===")


def handle_bar(context, bar_dict):
    current_month = context.now.month

    if context.month_count == 0 or current_month != context.last_month:
        rebalance(context, bar_dict)
        context.last_month = current_month
        context.month_count += 1

    if context.now.hour == 14 and context.now.minute >= 50:
        for stock in list(context.portfolio.positions.keys()):
            pos = context.portfolio.positions[stock]
            if pos.quantity > 0:
                try:
                    if bar_dict[stock].last < bar_dict[stock].limit_up * 0.995:
                        order_target_percent(stock, 0)
                except:
                    pass


def rebalance(context, bar_dict):
    date = context.now.strftime("%Y-%m-%d")

    print(f"\n[{date}] 月度调仓 #{context.month_count + 1}")

    try:
        all_stocks = all_instruments("CS")
        stocks = [
            s.order_book_id
            for s in all_stocks
            if s.order_book_id[:2] != "68" and s.order_book_id[0] not in ["3", "4", "8"]
        ]

        limit_up_stocks = []

        prev_date = context.now.date() - dt.timedelta(days=1)

        for stock in stocks[:200]:
            try:
                bars = history_bars(stock, 1, "1d", "close,limit_up,volume", prev_date)

                if bars is None or len(bars) == 0:
                    continue

                close = bars[-1]["close"]
                limit_up = bars[-1]["limit_up"]
                volume = bars[-1]["volume"]

                if close >= limit_up * 0.99 and volume > 1000000:
                    limit_up_stocks.append(stock)

            except:
                continue

        print(f"昨日涨停股: {len(limit_up_stocks)}")

        if len(limit_up_stocks) == 0:
            return

        qualified = []

        for stock in limit_up_stocks[:20]:
            try:
                today_bars = history_bars(
                    stock, 1, "1d", "open,limit_up", context.now.date()
                )

                if today_bars is None or len(today_bars) == 0:
                    continue

                open_price = today_bars[-1]["open"]
                limit_up = today_bars[-1]["limit_up"]

                if limit_up <= 0:
                    continue

                open_ratio = open_price / (limit_up / 1.1)

                if 1 < open_ratio < 1.06:
                    qualified.append(
                        {
                            "stock": stock,
                            "open_price": open_price,
                        }
                    )

            except:
                continue

        print(f"符合弱转强: {len(qualified)}")

        if len(qualified) == 0:
            return

        for holding in list(context.portfolio.positions.keys()):
            order_target_percent(holding, 0)

        weight = 1.0 / min(len(qualified), 3)

        for q in qualified[:3]:
            order_target_percent(q["stock"], weight)
            context.trades_count += 1
            print(f"买入 {q['stock']}")

    except Exception as e:
        print(f"错误: {e}")
