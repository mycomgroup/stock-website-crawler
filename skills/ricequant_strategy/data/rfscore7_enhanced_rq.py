# RFScore7 PB10% 增强策略 (RiceQuant API 兼容版)
# 基于成功的简化模板，添加情绪开关 + 四档仓位


import numpy as np


class SentimentSwitch:
    def __init__(self):
        self.sentiment_score = 50
        self.sentiment_state = 2

    def update(self, bar_dict):
        try:
            all_stocks = all_instruments(type="CS")
            sample = all_stocks["order_book_id"].tolist()[:200]

            hl_count = 0
            ll_count = 0

            for stock in sample:
                if stock not in bar_dict:
                    continue
                bar = bar_dict[stock]
                if not bar.is_trading:
                    continue
                close = bar.close
                if bar.limit_up and close >= bar.limit_up * 0.995:
                    hl_count += 1
                if bar.limit_down and close <= bar.limit_down * 1.005:
                    ll_count += 1

            score = 50

            if hl_count > 30:
                score += 15
            elif hl_count > 15:
                score += 5
            elif hl_count < 10:
                score -= 10

            ratio = hl_count / max(ll_count, 1)
            if ratio > 3:
                score += 10
            elif ratio > 1:
                score += 3
            elif ratio < 0.5:
                score -= 10
            elif ratio < 1:
                score -= 3

            self.sentiment_score = max(0, min(100, score))

            if score >= 70:
                self.sentiment_state = 4
            elif score >= 55:
                self.sentiment_state = 3
            elif score >= 40:
                self.sentiment_state = 2
            elif score >= 25:
                self.sentiment_state = 1
            else:
                self.sentiment_state = 0

        except Exception:
            pass

    def get_position_ratio(self):
        ratios = {4: 1.0, 3: 0.8, 2: 0.6, 1: 0.3, 0: 0.0}
        return ratios.get(self.sentiment_state, 0.6)


def init(context):
    context.benchmark = "000300.XSHG"
    context.base_hold_num = 15
    context.defensive_hold_num = 12
    context.bottom_hold_num = 10
    context.extreme_hold_num = 0
    context.breadth_defensive = 0.40
    context.breadth_bottom = 0.25
    context.breadth_extreme = 0.15
    context.sentiment = SentimentSwitch()
    context.last_rebalance_month = -1


def handle_bar(context, bar_dict):
    today = context.now

    context.sentiment.update(bar_dict)

    if today.month == context.last_rebalance_month:
        return

    context.last_rebalance_month = today.month

    logger.info(f"Monthly rebalance: {today}")

    stocks = get_universe(context, bar_dict)

    if not stocks:
        return

    market_state = calc_market_state(context, bar_dict)

    breadth = market_state["breadth"]
    trend_on = market_state["trend_on"]

    if breadth < context.breadth_extreme:
        target_hold_num = context.extreme_hold_num
    elif breadth < context.breadth_bottom:
        target_hold_num = context.bottom_hold_num
    elif breadth < context.breadth_defensive and not trend_on:
        target_hold_num = context.defensive_hold_num
    else:
        target_hold_num = context.base_hold_num

    sentiment_ratio = context.sentiment.get_position_ratio()
    adjusted_hold_num = int(target_hold_num * sentiment_ratio)

    logger.info(
        f"breadth={breadth:.2f}, trend={trend_on}, sentiment={context.sentiment.sentiment_state}, base={target_hold_num}, adjusted={adjusted_hold_num}"
    )

    if adjusted_hold_num <= 0:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    picks = choose_stocks(context, bar_dict, stocks, adjusted_hold_num)

    logger.info(f"Selected {len(picks)} stocks")

    for stock in list(context.portfolio.positions.keys()):
        if stock not in picks:
            order_target_value(stock, 0)

    if picks:
        total_value = context.portfolio.total_value * sentiment_ratio
        target_value = total_value / len(picks)
        for stock in picks:
            order_target_value(stock, target_value)


def get_universe(context, bar_dict):
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300) | set(zz500))
        stocks = [s for s in stocks if not s.startswith("688")]
        return stocks[:100]
    except Exception as e:
        logger.warning(f"get_universe failed: {e}")
        return []


def calc_market_state(context, bar_dict):
    try:
        hs300 = index_components("000300.XSHG")

        above_ma20 = 0
        total = 0

        for stock in hs300[:50]:
            try:
                bars = history_bars(stock, 20, "1d", "close")
                if bars is None or len(bars) < 20:
                    continue
                if bars[-1] > np.mean(bars):
                    above_ma20 += 1
                total += 1
            except Exception:
                continue

        breadth = above_ma20 / max(total, 1)

        idx_bars = history_bars("000300.XSHG", 20, "1d", "close")
        trend_on = (
            idx_bars[-1] > np.mean(idx_bars)
            if idx_bars and len(idx_bars) >= 20
            else False
        )

        return {"breadth": breadth, "trend_on": trend_on}
    except Exception as e:
        logger.warning(f"calc_market_state failed: {e}")
        return {"breadth": 0.5, "trend_on": True}


def choose_stocks(context, bar_dict, stocks, hold_num):
    results = []

    for stock in stocks[:50]:
        try:
            bars = history_bars(stock, 20, "1d", "close")
            if bars is None or len(bars) < 20:
                continue

            close = bars[-1]
            ma20 = np.mean(bars)
            momentum = (close / bars[0] - 1) * 100

            if close > ma20 and momentum > 0:
                results.append({"code": stock, "momentum": momentum})
        except Exception:
            continue

    results.sort(key=lambda x: -x["momentum"])

    return [r["code"] for r in results[:hold_num]]
