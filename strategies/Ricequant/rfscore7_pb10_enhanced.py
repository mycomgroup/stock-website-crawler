# RFScore PB10 增强版策略 (RiceQuant 策略编辑器版)
# 使用 handle_bar 框架
# 集成：四档仓位 + 情绪开关

import numpy as np


def init(context):
    context.benchmark = "000300.XSHG"
    context.frequency = "day"

    context.hold_num = 15
    context.min_stocks = 5

    context.breadth_extreme = 0.15
    context.breadth_bottom = 0.25
    context.breadth_defensive = 0.40

    context.last_rebalance_month = -1
    context.in_cash_mode = False


def handle_bar(context, bar_dict):
    """每日执行"""
    today = context.now

    # 极端市场检测（每日）
    breadth = calc_breadth(context, bar_dict)

    if not context.in_cash_mode:
        if breadth < context.breadth_extreme:
            logger.info(f"极端市场清仓 breadth={breadth:.2f}")
            clear_all(context)
            context.in_cash_mode = True
            return
    else:
        if breadth > context.breadth_bottom:
            logger.info(f"市场恢复 breadth={breadth:.2f}")
            context.in_cash_mode = False

    # 月度调仓
    if today.month != context.last_rebalance_month:
        context.last_rebalance_month = today.month
        do_rebalance(context, bar_dict)


def do_rebalance(context, bar_dict):
    """调仓"""
    if context.in_cash_mode:
        return

    breadth = calc_breadth(context, bar_dict)
    sentiment = calc_sentiment(context, bar_dict)

    logger.info(f"do_rebalance: breadth={breadth:.2f} sentiment={sentiment}")

    # 四档仓位
    if breadth < context.breadth_bottom:
        hold_num = 10
    elif breadth < context.breadth_defensive and sentiment < 15:
        hold_num = 8
    else:
        hold_num = context.hold_num

    # 选股
    stocks = select_stocks(context, bar_dict, hold_num)

    logger.info(f"selected {len(stocks)} stocks")

    if len(stocks) < context.min_stocks:
        logger.info("股票不足，跳过调仓")
        return

    # 调仓
    clear_all(context)

    per_stock = context.portfolio.total_value / len(stocks)
    for s in stocks:
        try:
            order_value(s, per_stock)
        except Exception as e:
            logger.warning(f"order {s} failed: {e}")

    logger.info(f"买入 {len(stocks)} 只股票")


def calc_breadth(context, bar_dict):
    """计算广度"""
    try:
        hs300 = index_components("000300.XSHG")
    except:
        return 0.5

    above = 0
    total = 0

    for s in hs300[:80]:
        try:
            hist = history_bars(s, 20, "1d", "close")
            if hist is not None and len(hist) >= 20:
                if hist[-1] > np.mean(hist):
                    above += 1
                total += 1
        except:
            pass

    return above / max(total, 1)


def calc_sentiment(context, bar_dict):
    """计算情绪"""
    try:
        all_stocks = get_all_securities(["stock"])
        sample = all_stocks["order_book_id"].tolist()[:300]
    except:
        return 20

    hl = 0
    for s in sample:
        if s in bar_dict:
            bar = bar_dict[s]
            if bar.is_trading and bar.close >= bar.limit_up * 0.995:
                hl += 1

    return hl


def select_stocks(context, bar_dict, hold_num):
    """选股：低估值过滤"""
    try:
        stocks = index_components("000300.XSHG")
        stocks = [s for s in stocks if not s.startswith("688")]
    except:
        return []

    # 过滤 ST、停牌、涨停
    valid = []
    for s in stocks:
        if s not in bar_dict:
            continue
        bar = bar_dict[s]
        if not bar.is_trading:
            continue
        # 过滤涨停
        if bar.close >= bar.limit_up * 0.99:
            continue
        try:
            inst = instruments(s)
            if "ST" in inst.symbol or "*" in inst.symbol:
                continue
        except:
            pass
        valid.append(s)

    logger.info(f"valid stocks: {len(valid)}")

    if len(valid) < hold_num:
        return valid

    # 简单选股：按价格排序（低价股往往估值较低）
    candidates = []
    for s in valid:
        try:
            bar = bar_dict[s]
            candidates.append((s, bar.close))
        except:
            pass

    # 按价格升序排序
    candidates.sort(key=lambda x: x[1])

    # 选择价格最低的 N 只
    selected = [c[0] for c in candidates[:hold_num]]

    return selected


def clear_all(context):
    """清仓"""
    for s in list(context.portfolio.positions.keys()):
        try:
            order_target(s, 0)
        except:
            pass
