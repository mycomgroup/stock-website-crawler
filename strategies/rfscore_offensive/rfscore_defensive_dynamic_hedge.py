"""
RFScore7 PB10% 动态对冲组合版

核心优化：
1. 动态进攻仓位：基于5信号风控（0%-50%）
2. 动态防守层配置：根据市场状态调整国债/黄金比例
3. 风控增强：广度+趋势+情绪+北向资金+连续下跌
4. 尾盘调仓：14:50调仓
5. 执行优化：涨跌停/高低开过滤

组合结构：
- 进攻层（RFScore股票）：0%-50%
- 防守层（ETF组合）：30%
- 现金缓冲：20%-50%

回测周期：2018-01-01 至今
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = [
        "roa",
        "roa_4",
        "net_operate_cash_flow",
        "net_operate_cash_flow_1",
        "net_operate_cash_flow_2",
        "net_operate_cash_flow_3",
        "total_assets",
        "total_assets_1",
        "total_assets_2",
        "total_assets_3",
        "total_assets_4",
        "total_assets_5",
        "total_non_current_liability",
        "total_non_current_liability_1",
        "gross_profit_margin",
        "gross_profit_margin_4",
        "operating_revenue",
        "operating_revenue_4",
    ]

    def calc(self, data):
        roa = data["roa"]
        delta_roa = roa / data["roa_4"] - 1

        cfo_sum = (
            data["net_operate_cash_flow"]
            + data["net_operate_cash_flow_1"]
            + data["net_operate_cash_flow_2"]
            + data["net_operate_cash_flow_3"]
        )
        ta_ttm = (
            data["total_assets"]
            + data["total_assets_1"]
            + data["total_assets_2"]
            + data["total_assets_3"]
        ) / 4
        ocfoa = cfo_sum / ta_ttm
        accrual = ocfoa - roa * 0.01

        leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        delta_leveler = -(leveler / leveler1 - 1)

        delta_margin = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1

        turnover = (
            data["operating_revenue"]
            / (data["total_assets"] + data["total_assets_1"]).mean()
        )
        turnover_1 = (
            data["operating_revenue_4"]
            / (data["total_assets_4"] + data["total_assets_5"]).mean()
        )
        delta_turn = turnover / turnover_1 - 1

        indicator_tuple = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicator_tuple).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
        self.fscore = self.basic.apply(lambda x: np.where(x > 0, 1, 0)).sum(axis=1)


def initialize(context):
    set_benchmark("000300.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("order", "error")

    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0,
            open_commission=0.0002,
            close_commission=0.0002,
            close_today_commission=0,
            min_commission=5,
        ),
        type="fund",
    )

    g.max_offensive_weight = 0.50
    g.defensive_weight = 0.30
    g.min_cash_buffer = 0.20

    g.defensive_assets_base = {
        "511010.XSHG": 0.75,
        "518880.XSHG": 0.10,
        "510880.XSHG": 0.08,
        "513100.XSHG": 0.04,
    }

    g.ipo_days = 180
    g.base_hold_num = 15
    g.industry_cap_ratio = 0.30
    g.primary_pb_group = 1

    g.last_market_state = {}
    g.last_weights = {
        "offensive": 0.0,
        "defensive": 0.30,
        "cash": 0.70,
    }

    run_monthly(rebalance_offensive, 1, time="14:50", reference_security="000300.XSHG")
    run_monthly(rebalance_defensive, 1, time="14:55", reference_security="000300.XSHG")
    run_daily(record_market_state, time="14:50", reference_security="000300.XSHG")


def calc_breadth(watch_date):
    hs300 = get_index_stocks("000300.XSHG", date=watch_date)
    prices = get_price(
        hs300, end_date=watch_date, count=20, fields=["close"], panel=False
    )
    close = prices.pivot(index="time", columns="code", values="close")
    return float((close.iloc[-1] > close.mean()).mean())


def calc_trend(watch_date):
    idx = get_price("000300.XSHG", end_date=watch_date, count=20, fields=["close"])
    return float(idx["close"].iloc[-1]) > float(idx["close"].mean())


def calc_sentiment(watch_date):
    all_stocks = get_all_securities("stock", date=watch_date).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
    ]
    sample = all_stocks[:500]

    df = get_price(
        sample,
        end_date=watch_date,
        count=1,
        fields=["close", "high_limit", "low_limit"],
        panel=False,
    )
    df = df.dropna()

    hl_count = len(df[df["close"] == df["high_limit"]])
    ll_count = len(df[df["close"] == df["low_limit"]])

    score = 50
    if hl_count > 80:
        score += 20
    elif hl_count > 50:
        score += 10
    elif hl_count < 15:
        score -= 15

    if ll_count > 50:
        score -= 15

    return max(0, min(100, score))


def calc_north_flow(watch_date):
    try:
        df = get_money_flow(
            ["北向资金"], end_date=watch_date, count=5, fields=["net_amount"]
        )
        if df is not None and not df.empty:
            return float(df["net_amount"].sum())
    except:
        pass
    return 0


def calc_down_days(watch_date):
    idx = get_price("000300.XSHG", end_date=watch_date, count=10, fields=["close"])
    closes = idx["close"].values
    down_count = 0
    for i in range(len(closes) - 1, 0, -1):
        if closes[i] < closes[i - 1]:
            down_count += 1
        else:
            break
    return down_count


def calc_market_state(watch_date):
    return {
        "breadth": calc_breadth(watch_date),
        "trend": calc_trend(watch_date),
        "sentiment": calc_sentiment(watch_date),
        "north_flow": calc_north_flow(watch_date),
        "down_days": calc_down_days(watch_date),
    }


def calc_offensive_weight(state):
    score = 0

    if state["breadth"] > 0.5:
        score += 2
    elif state["breadth"] > 0.35:
        score += 1
    elif state["breadth"] < 0.2:
        score -= 1

    if state["trend"]:
        score += 1

    if state["sentiment"] > 60:
        score += 1
    elif state["sentiment"] < 30:
        score -= 1

    if state["north_flow"] > 50e8:
        score += 1
    elif state["north_flow"] < -50e8:
        score -= 1

    if state["down_days"] >= 5:
        score -= 2

    weight_map = {
        5: g.max_offensive_weight,
        4: g.max_offensive_weight * 0.8,
        3: g.max_offensive_weight * 0.6,
        2: g.max_offensive_weight * 0.4,
        1: g.max_offensive_weight * 0.2,
        0: g.max_offensive_weight * 0.1,
        -1: 0.0,
        -2: 0.0,
    }
    return weight_map.get(score, g.max_offensive_weight * 0.5)


def calc_dynamic_defensive_assets(state):
    assets = g.defensive_assets_base.copy()

    if state["sentiment"] < 40 or state["breadth"] < 0.3:
        assets["511010.XSHG"] = 0.80
        assets["518880.XSHG"] = 0.08
        assets["510880.XSHG"] = 0.08
        assets["513100.XSHG"] = 0.04

    elif state["north_flow"] > 100e8:
        assets["511010.XSHG"] = 0.65
        assets["518880.XSHG"] = 0.10
        assets["510880.XSHG"] = 0.10
        assets["513100.XSHG"] = 0.10

    elif state["down_days"] >= 3:
        assets["511010.XSHG"] = 0.70
        assets["518880.XSHG"] = 0.15
        assets["510880.XSHG"] = 0.10
        assets["513100.XSHG"] = 0.05

    return assets


def get_universe(watch_date):
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [stock for stock in stocks if not stock.startswith("688")]

    sec = get_all_securities(types=["stock"], date=watch_date)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= watch_date - pd.Timedelta(days=g.ipo_days)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    return stocks


def calc_rfscore_table(stocks, watch_date):
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=watch_date, end_date=watch_date)

    df = factor.basic.copy()
    df["RFScore"] = factor.fscore

    val = get_valuation(
        stocks, end_date=watch_date, fields=["pb_ratio", "pe_ratio"], count=1
    )
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
    df = df.join(val, how="left")

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "pb_ratio"])
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"),
            10,
            labels=False,
            duplicates="drop",
        )
        + 1
    )

    df["质量分"] = df["RFScore"] / 7 * 100
    df["估值分"] = (1 - df["pb_group"] / 10) * 100
    df["成长分"] = np.clip(df["DELTA_ROA"] * 100, -50, 50) + np.clip(
        df["DELTA_MARGIN"] * 100, -50, 50
    )
    df["综合分"] = df["质量分"] * 0.5 + df["估值分"] * 0.3 + df["成长分"] * 0.2

    return df


def get_industry_map(codes, watch_date):
    if not codes:
        return {}
    raw = get_industry(codes, date=watch_date)
    result = {}
    for code in codes:
        result[code] = (
            raw.get(code, {}).get("sw_l1", {}).get("industry_name", "Unknown")
        )
    return result


def apply_industry_cap(picks, hold_num, industry_map):
    limit_count = max(1, int(np.floor(hold_num * g.industry_cap_ratio)))
    final_picks = []
    industry_counts = {}

    for code in picks:
        if len(final_picks) >= hold_num:
            break
        industry_name = industry_map.get(code, "Unknown")
        if industry_counts.get(industry_name, 0) < limit_count:
            final_picks.append(code)
            industry_counts[industry_name] = industry_counts.get(industry_name, 0) + 1

    return final_picks


def choose_stocks(watch_date, hold_num):
    if hold_num <= 0:
        return []

    stocks = get_universe(watch_date)
    df = calc_rfscore_table(stocks, str(watch_date))

    primary = df[(df["RFScore"] == 7) & (df["pb_group"] <= g.primary_pb_group)].copy()
    primary = primary.sort_values(["综合分", "pb_ratio"], ascending=[False, True])
    picks = primary.index.tolist()

    if len(picks) < hold_num:
        secondary = df[(df["RFScore"] >= 6) & (df["pb_group"] <= 2)].copy()
        secondary = secondary.sort_values(
            ["综合分", "pb_ratio"], ascending=[False, True]
        )
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break

    industry_map = get_industry_map(picks, watch_date)
    picks = apply_industry_cap(picks, hold_num, industry_map)

    return picks[:hold_num]


def filter_buyable_enhanced(context, stocks):
    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if current_data[stock].paused:
            continue
        if current_data[stock].is_st:
            continue
        if (
            "ST" in current_data[stock].name
            or "*" in current_data[stock].name
            or "退" in current_data[stock].name
        ):
            continue
        last_price = current_data[stock].last_price
        yesterday_close = current_data[stock].yesterday_close
        high_limit = current_data[stock].high_limit
        low_limit = current_data[stock].low_limit

        if last_price >= high_limit * 0.98:
            continue
        if last_price <= low_limit * 1.02:
            continue
        if last_price < yesterday_close * 0.97:
            continue
        if last_price > yesterday_close * 1.03:
            continue

        buyable.append(stock)
    return buyable


def rebalance_offensive(context):
    watch_date = context.previous_date
    market_state = calc_market_state(watch_date)
    g.last_market_state = market_state

    offensive_weight = calc_offensive_weight(market_state)
    target_hold_num = int(g.base_hold_num * offensive_weight / g.max_offensive_weight)

    target_stocks = []
    if target_hold_num > 0:
        target_stocks = choose_stocks(watch_date, target_hold_num)
        target_stocks = filter_buyable_enhanced(context, target_stocks)

    g.last_weights["offensive"] = offensive_weight
    g.last_weights["cash"] = max(
        g.min_cash_buffer, 1 - offensive_weight - g.defensive_weight
    )

    log.info(
        "offensive rebalance date=%s breadth=%.3f trend=%s sentiment=%.0f offensive=%.0f%% hold=%d"
        % (
            str(watch_date),
            market_state["breadth"],
            str(market_state["trend"]),
            market_state["sentiment"],
            offensive_weight * 100,
            len(target_stocks),
        )
    )

    current_positions = [
        s
        for s in context.portfolio.positions
        if not s.endswith(".XSHG") or s.startswith("6")
    ]
    for stock in current_positions:
        if stock not in target_stocks and not stock.endswith(".XSHG"):
            order_target_value(stock, 0)

    if target_stocks and offensive_weight > 0:
        target_value = (
            context.portfolio.total_value * offensive_weight / len(target_stocks)
        )
        current_data = get_current_data()
        for stock in target_stocks:
            price = current_data[stock].last_price
            if price <= 0:
                continue
            target_amount = int(target_value / price / 100) * 100
            if target_amount >= 100:
                order_target(stock, target_amount)


def rebalance_defensive(context):
    watch_date = context.previous_date
    market_state = (
        g.last_market_state
        if hasattr(g, "last_market_state")
        else calc_market_state(watch_date)
    )

    defensive_assets = calc_dynamic_defensive_assets(market_state)

    log.info("defensive rebalance assets=%s" % str(defensive_assets))

    total_value = context.portfolio.total_value
    defensive_value = total_value * g.defensive_weight

    current_data = get_current_data()
    for etf_code, weight in defensive_assets.items():
        target_value = defensive_value * weight
        price = current_data[etf_code].last_price if etf_code in current_data else None

        if price and price > 0:
            target_amount = int(target_value / price / 100) * 100
            if target_amount >= 100:
                order_target(etf_code, target_amount)


def record_market_state(context):
    watch_date = context.previous_date
    state = g.last_market_state if hasattr(g, "last_market_state") else {}
    weights = g.last_weights if hasattr(g, "last_weights") else {}

    record(
        breadth=state.get("breadth", 0),
        sentiment=state.get("sentiment", 50),
        offensive_weight=weights.get("offensive", 0),
        defensive_weight=weights.get("defensive", 0.3),
        cash_weight=weights.get("cash", 0.7),
    )
