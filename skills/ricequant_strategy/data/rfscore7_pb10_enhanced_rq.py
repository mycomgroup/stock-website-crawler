# RFScore7 + PB10% 增强版策略 (RiceQuant API 兼容版)
# 集成：情绪开关 + 四档仓位 + 风控模块


import numpy as np
import pandas as pd


class SentimentSwitch:
    def __init__(self):
        self.hl_count = 0
        self.ll_count = 0
        self.sentiment_score = 50
        self.sentiment_state = 2

    def update(self, context, bar_dict):
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
                if close >= bar.limit_up * 0.995:
                    hl_count += 1
                if close <= bar.limit_down * 1.005:
                    ll_count += 1

            self.hl_count = hl_count
            self.ll_count = ll_count

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

        except Exception as e:
            logger.warning(f"Sentiment update failed: {e}")

    def get_position_ratio(self):
        ratios = {4: 1.0, 3: 0.8, 2: 0.6, 1: 0.3, 0: 0.0}
        return ratios.get(self.sentiment_state, 0.6)


class FourTierPosition:
    def __init__(self, base_hold=15):
        self.base_hold_num = base_hold
        self.defensive_hold_num = 12
        self.bottom_hold_num = 10
        self.extreme_hold_num = 0

        self.breadth_defensive = 0.40
        self.breadth_bottom = 0.25
        self.breadth_extreme = 0.15

    def calc_breadth(self, context, bar_dict):
        hs300 = index_components("000300.XSHG")

        above_ma20 = 0
        total = 0

        for stock in hs300[:100]:
            if stock not in bar_dict:
                continue
            try:
                hist = history_bars(stock, 20, "1d", "close")
                if len(hist) < 20:
                    continue
                ma20 = hist.mean()
                close = hist[-1]
                if close > ma20:
                    above_ma20 += 1
                total += 1
            except Exception:
                continue

        return above_ma20 / max(total, 1)

    def calc_trend(self, context, bar_dict):
        try:
            idx_hist = history_bars("000300.XSHG", 20, "1d", "close")
            idx_close = idx_hist[-1]
            idx_ma20 = idx_hist.mean()
            return idx_close > idx_ma20
        except Exception:
            return False

    def get_target_hold_num(self, context, bar_dict):
        breadth = self.calc_breadth(context, bar_dict)
        trend_on = self.calc_trend(context, bar_dict)

        if breadth < self.breadth_extreme:
            return self.extreme_hold_num, breadth, trend_on
        elif breadth < self.breadth_bottom:
            return self.bottom_hold_num, breadth, trend_on
        elif breadth < self.breadth_defensive and not trend_on:
            return self.defensive_hold_num, breadth, trend_on
        else:
            return self.base_hold_num, breadth, trend_on


def init(context):
    context.benchmark = "000300.XSHG"

    context.ipo_days = 180
    context.primary_pb_group = 1
    context.reduced_pb_group = 2

    context.sentiment = SentimentSwitch()
    context.position_rule = FourTierPosition(base_hold=15)

    context.stop_loss_gap = 0.04
    context.week_loss_limit = 0.08
    context.month_loss_limit = 0.15
    context.week_start_value = 0
    context.month_start_value = 0

    context.last_rebalance_month = -1


def handle_bar(context, bar_dict):
    today = context.now

    context.sentiment.update(context, bar_dict)

    if today.month == context.last_rebalance_month:
        return

    context.last_rebalance_month = today.month
    rebalance(context, bar_dict)


def get_universe(context, bar_dict):
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300) | set(zz500))

        stocks = [s for s in stocks if not s.startswith("688")]

        all_inst = all_instruments(type="CS")
        valid_stocks = []
        today = context.now.date()

        for stock in stocks:
            inst = all_inst[all_inst["order_book_id"] == stock]
            if inst.empty:
                continue
            listed_date = pd.to_datetime(inst.iloc[0]["listed_date"])
            if (today - listed_date.date()).days >= context.ipo_days:
                valid_stocks.append(stock)

        final_stocks = []
        for stock in valid_stocks:
            if stock not in bar_dict:
                continue
            bar = bar_dict[stock]
            if bar.is_trading is False:
                continue
            instrument = instruments(stock)
            if "ST" in instrument.symbol or "*" in instrument.symbol:
                continue
            final_stocks.append(stock)

        return final_stocks
    except Exception as e:
        logger.warning(f"get_universe failed: {e}")
        return []


def calc_rfscore_simple(context, bar_dict, stocks):
    results = []

    for stock in stocks[:100]:
        try:
            bars = history_bars(stock, 20, "1d", "close")
            if bars is None or len(bars) < 20:
                continue

            close = bars[-1]
            ma20 = np.mean(bars)
            momentum = (close / bars[0] - 1) * 100

            score = 0
            if momentum > 5:
                score += 3
            elif momentum > 0:
                score += 2
            elif momentum > -5:
                score += 1

            if close > ma20:
                score += 2

            results.append(
                {
                    "code": stock,
                    "close": close,
                    "fscore": min(7, max(1, score)),
                    "momentum": momentum,
                }
            )
        except Exception:
            continue

    return results


def choose_stocks(context, bar_dict, hold_num):
    stocks = get_universe(context, bar_dict)
    if not stocks:
        return []

    metrics = calc_rfscore_simple(context, bar_dict, stocks)
    if not metrics:
        return []

    metrics.sort(key=lambda x: (-x["fscore"], -x["momentum"]))

    picks = [m["code"] for m in metrics if m["fscore"] >= 6]

    if len(picks) < hold_num:
        for m in metrics:
            if m["code"] not in picks:
                picks.append(m["code"])
            if len(picks) >= hold_num:
                break

    return picks[:hold_num]


def filter_buyable(context, bar_dict, stocks):
    buyable = []

    for stock in stocks:
        if stock not in bar_dict:
            continue

        bar = bar_dict[stock]

        if bar.is_trading is False:
            continue

        inst = instruments(stock)
        if "ST" in inst.symbol or "*" in inst.symbol or "退" in inst.symbol:
            continue

        close = bar.close
        limit_up = bar.limit_up
        limit_down = bar.limit_down

        if limit_up and close >= limit_up * 0.995:
            continue
        if limit_down and close <= limit_down * 1.005:
            continue

        buyable.append(stock)

    return buyable


def rebalance(context, bar_dict):
    watch_date = context.now.date()

    target_hold_num, breadth, trend_on = context.position_rule.get_target_hold_num(
        context, bar_dict
    )

    sentiment_ratio = context.sentiment.get_position_ratio()
    adjusted_hold_num = int(target_hold_num * sentiment_ratio)

    logger.info(
        f"rebalance: breadth={breadth:.3f}, trend={trend_on}, "
        f"sentiment_state={context.sentiment.sentiment_state}, "
        f"base_hold={target_hold_num}, adjusted_hold={adjusted_hold_num}"
    )

    if adjusted_hold_num <= 0:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    target_stocks = choose_stocks(context, bar_dict, adjusted_hold_num)
    target_stocks = filter_buyable(context, bar_dict, target_stocks)

    if len(target_stocks) < adjusted_hold_num:
        adjusted_hold_num = len(target_stocks)

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if not target_stocks:
        return

    total_value = context.portfolio.total_value * sentiment_ratio
    target_value_per_stock = total_value / max(len(target_stocks), 1)

    for stock in target_stocks:
        order_target_value(stock, target_value_per_stock)
