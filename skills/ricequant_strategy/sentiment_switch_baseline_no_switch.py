"""
任务02基准：无情绪开关版本
RiceQuant 策略编辑器格式
作为对照组
"""


def init(context):
    """初始化"""
    context.max_positions = 5
    context.position_size = 0.2

    scheduler.run_monthly(rebalance, monthday=1)

    print(f"策略初始化完成（无情绪开关）")


def rebalance(context, bar_dict):
    """月度调仓"""
    current_date = context.now.strftime("%Y-%m-%d")

    zt_count = get_zt_count(context)

    print(f"\n{'=' * 60}")
    print(f"日期：{current_date}")
    print(f"涨停家数：{zt_count}")
    print(f"无情绪开关，直接开仓")

    selected = select_stocks(context, bar_dict)

    if len(selected) == 0:
        print("无选中股票")
        return

    adjust_positions(context, selected)


def get_zt_count(context):
    """获取涨停家数（仅用于日志）"""
    try:
        all_stocks = all_instruments("CS")
        stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        zt_count = 0
        for stock in stocks[:500]:
            try:
                bars = history_bars(stock, 1, "1d", ["close", "limit_up"])
                if bars is not None and len(bars) > 0:
                    if bars[0]["close"] >= bars[0]["limit_up"] * 0.99:
                        zt_count += 1
            except:
                continue

        estimated_zt = int(zt_count * (len(stocks) / 500))
        return estimated_zt
    except:
        return 100


def select_stocks(context, bar_dict):
    """首板低开选股"""
    try:
        all_stocks = all_instruments("CS")
        stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        prev_zt = []
        for stock in stocks[:300]:
            try:
                bars = history_bars(stock, 1, "1d", ["close", "limit_up"])
                if bars and len(bars) > 0:
                    if bars[0]["close"] >= bars[0]["limit_up"] * 0.99:
                        prev_zt.append(stock)
            except:
                continue

        if len(prev_zt) == 0:
            return []

        selected = []
        for stock in prev_zt[:20]:
            try:
                prev_close = history_bars(stock, 2, "1d", "close")
                curr_open = history_bars(stock, 1, "1d", "open")
                curr_limit = history_bars(stock, 1, "1d", "limit_up")

                if prev_close is None or curr_open is None or len(prev_close) < 2:
                    continue

                prev_c = prev_close[-2]
                curr_o = curr_open[-1]
                limit_u = curr_limit[-1] if curr_limit is not None else curr_o * 1.1

                open_pct = (curr_o / prev_c - 1) * 100
                if 0.5 <= open_pct <= 1.5 and curr_o < limit_u * 0.99:
                    selected.append(stock)
            except:
                continue

        return selected[: context.max_positions]
    except Exception as e:
        print(f"选股错误：{e}")
        return []


def adjust_positions(context, selected):
    """调整仓位"""
    for stock in list(context.portfolio.positions.keys()):
        if stock not in selected:
            order_target(stock, 0)
            print(f"卖出：{stock}")

    for stock in selected:
        if stock not in context.portfolio.positions:
            order_target_percent(stock, context.position_size)
            print(f"买入：{stock}，仓位{context.position_size * 100:.0f}%")


__config__ = {
    "base": {
        "start_date": "2024-01-01",
        "end_date": "2025-03-28",
        "benchmark": "000300.XSHG",
        "accounts": {"stock": 1000000},
    },
    "extra": {"log_level": "verbose"},
}
