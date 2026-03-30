# RFScore7 + PB10% 增强版策略 (RiceQuant 版)
# 集成：情绪开关 + 四档仓位 + 风控模块
# 原版: JoinQuant rfscore7_pb10_enhanced_standalone.py


import pandas as pd
import numpy as np


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


def calc_rfscore_factors(stocks, watch_date):
    factor_names = [
        "roa",
        "net_operate_cash_flow",
        "total_assets",
        "total_non_current_liability",
        "gross_profit_margin",
        "operating_revenue",
    ]

    try:
        current_factors = get_factor(
            stocks, factor_names, start_date=watch_date, end_date=watch_date
        )
    except Exception as e:
        log.warn(f"get_factor failed: {e}")
        return pd.DataFrame()

    if current_factors is None or current_factors.empty:
        return pd.DataFrame()

    hist_date = watch_date - pd.Timedelta(days=365)
    try:
        hist_factors = get_factor(
            stocks, factor_names, start_date=hist_date, end_date=hist_date
        )
    except Exception as e:
        hist_factors = None

    df = pd.DataFrame(index=stocks)

    roa = current_factors.get("roa", pd.Series(index=stocks))
    df["ROA"] = roa

    if hist_factors is not None and "roa" in hist_factors:
        roa_hist = hist_factors.get("roa", pd.Series(index=stocks))
        df["DELTA_ROA"] = roa / roa_hist - 1
    else:
        df["DELTA_ROA"] = np.nan

    ocf = current_factors.get("net_operate_cash_flow", pd.Series(index=stocks))
    ta = current_factors.get("total_assets", pd.Series(index=stocks))
    if ta is not None and ta.mean() > 0:
        df["OCFOA"] = ocf / ta
    else:
        df["OCFOA"] = np.nan

    df["ACCRUAL"] = df["OCFOA"] - df["ROA"] * 0.01

    tncl = current_factors.get("total_non_current_liability", pd.Series(index=stocks))
    if hist_factors is not None and "total_non_current_liability" in hist_factors:
        tncl_hist = hist_factors.get(
            "total_non_current_liability", pd.Series(index=stocks)
        )
        ta_hist = hist_factors.get("total_assets", pd.Series(index=stocks))
        leveler = tncl / ta
        leveler_hist = tncl_hist / ta_hist
        df["DELTA_LEVELER"] = -(leveler / leveler_hist - 1)
    else:
        df["DELTA_LEVELER"] = np.nan

    gpm = current_factors.get("gross_profit_margin", pd.Series(index=stocks))
    if hist_factors is not None and "gross_profit_margin" in hist_factors:
        gpm_hist = hist_factors.get("gross_profit_margin", pd.Series(index=stocks))
        df["DELTA_MARGIN"] = gpm / gpm_hist - 1
    else:
        df["DELTA_MARGIN"] = np.nan

    rev = current_factors.get("operating_revenue", pd.Series(index=stocks))
    if hist_factors is not None and "operating_revenue" in hist_factors:
        rev_hist = hist_factors.get("operating_revenue", pd.Series(index=stocks))
        turnover = rev / ta
        turnover_hist = rev_hist / ta_hist
        df["DELTA_TURN"] = turnover / turnover_hist - 1
    else:
        df["DELTA_TURN"] = np.nan

    df = df.replace([np.inf, -np.inf], np.nan)
    df["RFScore"] = df.apply(sign).sum(axis=1)

    return df


class SentimentSwitch:
    def __init__(self):
        self.hl_count = 0
        self.ll_count = 0
        self.sentiment_score = 50
        self.sentiment_state = 2

    def update(self, context, bar_dict):
        try:
            all_stocks = all_instruments(type="CS")
            sample = all_stocks["order_book_id"].tolist()[:500]

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

            if hl_count > 80:
                score += 20
            elif hl_count > 50:
                score += 10
            elif hl_count > 30:
                score += 5
            elif hl_count < 15:
                score -= 15
            elif hl_count < 25:
                score -= 5

            ratio = hl_count / max(ll_count, 1)
            if ratio > 5:
                score += 15
            elif ratio > 2:
                score += 5
            elif ratio < 0.5:
                score -= 15
            elif ratio < 1:
                score -= 5

            self.sentiment_score = max(0, min(100, score))

            if score >= 75:
                self.sentiment_state = 4
            elif score >= 60:
                self.sentiment_state = 3
            elif score >= 45:
                self.sentiment_state = 2
            elif score >= 30:
                self.sentiment_state = 1
            else:
                self.sentiment_state = 0

        except Exception as e:
            log.warn(f"Sentiment update failed: {e}")

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

        for stock in hs300:
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

    def calc_trend(self, context):
        try:
            idx_hist = history_bars("000300.XSHG", 20, "1d", "close")
            idx_close = idx_hist[-1]
            idx_ma20 = idx_hist.mean()
            return idx_close > idx_ma20
        except Exception:
            return False

    def get_target_hold_num(self, context, bar_dict):
        breadth = self.calc_breadth(context, bar_dict)
        trend_on = self.calc_trend(context)

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
    set_slippage(FixedSlippage(0))
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))

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
    context.forced_rest_days = 0

    scheduler.run_monthly(rebalance, tradingday=1)
    scheduler.run_daily(morning_check, rule=market_open)


def morning_check(context, bar_dict):
    context.sentiment.update(context, bar_dict)
    plot("sentiment_state", context.sentiment.sentiment_state)
    plot("sentiment_score", context.sentiment.sentiment_score)
    plot("hl_count", context.sentiment.hl_count)


def get_universe(context, bar_dict):
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


def get_pb_ratio(stocks, watch_date):
    try:
        pb_data = get_factor(
            stocks, "pb_ratio", start_date=watch_date, end_date=watch_date
        )
        if pb_data is not None and not pb_data.empty:
            return pb_data.get("pb_ratio", pd.Series())
    except Exception as e:
        log.warn(f"get pb_ratio failed: {e}")

    pb_dict = {}
    for stock in stocks:
        pb_dict[stock] = np.nan

    return pd.Series(pb_dict)


def calc_rfscore_table(context, stocks, watch_date):
    df = calc_rfscore_factors(stocks, watch_date)

    if df.empty:
        return df

    pb = get_pb_ratio(stocks, watch_date)
    df["pb_ratio"] = pb

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "pb_ratio"])

    if len(df) > 0:
        df["pb_group"] = (
            pd.qcut(
                df["pb_ratio"].rank(method="first"),
                10,
                labels=False,
                duplicates="drop",
            )
            + 1
        )

    return df


def choose_stocks(context, watch_date, hold_num, bar_dict):
    stocks = get_universe(context, bar_dict)
    df = calc_rfscore_table(context, stocks, watch_date)

    if df.empty:
        return [], df

    primary = df[
        (df["RFScore"] == 7) & (df["pb_group"] <= context.primary_pb_group)
    ].copy()
    primary = primary.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
        ascending=[False, False, False, False, False, True],
    )
    picks = primary.index.tolist()

    if len(picks) < hold_num:
        secondary = df[
            (df["RFScore"] >= 6) & (df["pb_group"] <= context.reduced_pb_group)
        ].copy()
        secondary = secondary.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break

    if len(picks) < hold_num:
        fallback = df.sort_values(
            ["RFScore", "ROA", "OCFOA", "pb_ratio"],
            ascending=[False, False, False, True],
        )
        for code in fallback.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break

    return picks[:hold_num], df


def filter_buyable(context, stocks, bar_dict):
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

    log.info(
        f"rebalance: breadth={breadth:.3f}, trend={trend_on}, "
        f"sentiment_state={context.sentiment.sentiment_state}, "
        f"base_hold={target_hold_num}, adjusted_hold={adjusted_hold_num}"
    )

    plot("breadth", breadth)
    plot("target_hold_num", target_hold_num)
    plot("adjusted_hold_num", adjusted_hold_num)

    if adjusted_hold_num <= 0:
        for stock in context.portfolio.positions:
            order_target_value(stock, 0)
        return

    target_stocks, factor_table = choose_stocks(
        context, watch_date, adjusted_hold_num, bar_dict
    )
    target_stocks = filter_buyable(context, target_stocks, bar_dict)

    if len(target_stocks) < adjusted_hold_num:
        adjusted_hold_num = len(target_stocks)

    for stock in context.portfolio.positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if not target_stocks:
        return

    total_value = context.portfolio.total_value * sentiment_ratio
    target_value_per_stock = total_value / max(len(target_stocks), 1)

    for stock in target_stocks:
        order_target_value(stock, target_value_per_stock)
