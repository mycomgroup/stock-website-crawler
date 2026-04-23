# 因子剥离验证：版本D - 无市场状态风控
# 移除market_state风控模块，始终保持满仓
# 目的：验证市场状态择时是否有效

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

        indicators = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicators).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
        self.fscore = self.basic.apply(sign).sum(axis=1)


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

    g.release_name = "RFScore7_Attribution_D_No_Market_State"
    g.ipo_days = 180
    g.primary_pb_group = 1
    g.secondary_pb_group = 2
    g.max_pe_ratio = 100
    g.min_roa = 0.5
    g.industry_cap_ratio = 0.30

    # 固定持仓数，不做市场状态调整
    g.hold_num_fixed = 15

    g.last_selection = {
        "target_hold_num": 0,
        "actual_hold_num": 0,
        "cash_ratio": 1.0,
        "max_industry_ratio": 0.0,
    }

    run_monthly(rebalance, 1, time="9:35", reference_security="000300.XSHG")


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
    df = df.dropna(subset=["RFScore", "ROA", "OCFOA", "pb_ratio", "pe_ratio"])
    df = df[
        (df["pb_ratio"] > 0)
        & (df["pe_ratio"] > 0)
        & (df["pe_ratio"] < g.max_pe_ratio)
        & (df["ROA"] > g.min_roa)
    ].copy()

    if df.empty:
        return df

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


def sort_candidates(df):
    if df.empty:
        return df
    return df.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
        ascending=[False, False, False, False, False, True],
    )


def get_industry_map(codes, watch_date):
    if not codes:
        return {}
    raw = get_industry(codes, date=watch_date)
    result = {}
    for code in codes:
        result[code] = raw.get(code, {}).get("sw_l1", {}).get("industry_name", "Unknown")
    return result


def append_with_cap(picks, candidates, industry_map, industry_counts, limit_count, target_hold_num):
    added = 0
    for code in candidates:
        if len(picks) >= target_hold_num:
            break
        if code in picks:
            continue
        industry_name = industry_map.get(code, "Unknown")
        count = industry_counts.get(industry_name, 0)
        if count >= limit_count:
            continue
        picks.append(code)
        industry_counts[industry_name] = count + 1
        added += 1
    return added


def summarize_industry_ratio(picks, industry_map):
    if not picks:
        return 0.0, {}
    counts = {}
    for code in picks:
        name = industry_map.get(code, "Unknown")
        counts[name] = counts.get(name, 0) + 1
    max_ratio = max(counts.values()) / float(len(picks))
    return max_ratio, counts


def choose_stocks(watch_date, target_hold_num):
    stocks = get_universe(watch_date)
    df = calc_rfscore_table(stocks, str(watch_date))
    if target_hold_num <= 0 or df.empty:
        return [], {
            "primary_count": 0,
            "secondary_count": 0,
            "actual_count": 0,
            "industry_summary": {},
            "max_industry_ratio": 0.0,
        }

    limit_count = max(1, int(np.floor(target_hold_num * g.industry_cap_ratio)))

    primary = sort_candidates(
        df[(df["RFScore"] == 7) & (df["pb_group"] == g.primary_pb_group)].copy()
    )
    secondary = sort_candidates(
        df[(df["RFScore"] == 7) & (df["pb_group"] == g.secondary_pb_group)].copy()
    )

    ordered_codes = primary.index.tolist() + [
        code for code in secondary.index.tolist() if code not in primary.index
    ]
    industry_map = get_industry_map(ordered_codes, watch_date)

    picks = []
    industry_counts = {}
    primary_added = append_with_cap(
        picks,
        primary.index.tolist(),
        industry_map,
        industry_counts,
        limit_count,
        target_hold_num,
    )
    secondary_added = append_with_cap(
        picks,
        secondary.index.tolist(),
        industry_map,
        industry_counts,
        limit_count,
        target_hold_num,
    )
    max_ratio, industry_summary = summarize_industry_ratio(picks, industry_map)

    return picks, {
        "primary_count": primary_added,
        "secondary_count": secondary_added,
        "actual_count": len(picks),
        "industry_summary": industry_summary,
        "max_industry_ratio": max_ratio,
    }


def filter_buyable(context, stocks):
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
        if last_price >= current_data[stock].high_limit * 0.995:
            continue
        if last_price <= current_data[stock].low_limit * 1.005:
            continue
        buyable.append(stock)
    return buyable


def rebalance(context):
    watch_date = context.previous_date

    # 固定持仓数，不做市场状态判断
    target_hold_num = g.hold_num_fixed

    target_stocks, meta = choose_stocks(watch_date, target_hold_num)
    target_stocks = filter_buyable(context, target_stocks)
    meta["actual_count"] = len(target_stocks)
    if target_stocks:
        industry_map = get_industry_map(target_stocks, watch_date)
        max_ratio, industry_summary = summarize_industry_ratio(target_stocks, industry_map)
        meta["industry_summary"] = industry_summary
        meta["max_industry_ratio"] = max_ratio
    else:
        meta["industry_summary"] = {}
        meta["max_industry_ratio"] = 0.0

    cash_ratio = 1.0
    if target_hold_num > 0:
        cash_ratio = max(0.0, 1.0 - len(target_stocks) / float(target_hold_num))

    g.last_selection = {
        "target_hold_num": target_hold_num,
        "actual_hold_num": len(target_stocks),
        "cash_ratio": cash_ratio,
        "max_industry_ratio": meta["max_industry_ratio"],
    }

    log.info(
        "release=%s watch_date=%s target_hold_num=%s actual_hold_num=%s primary_count=%s secondary_count=%s cash_ratio=%.2f"
        % (
            g.release_name,
            str(watch_date),
            str(target_hold_num),
            str(len(target_stocks)),
            str(meta["primary_count"]),
            str(meta["secondary_count"]),
            cash_ratio,
        )
    )

    current_positions = list(context.portfolio.positions.keys())
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if not target_stocks:
        return

    current_data = get_current_data()
    target_value = context.portfolio.total_value / float(len(target_stocks))
    for stock in target_stocks:
        price = current_data[stock].last_price
        if price <= 0:
            continue
        target_amount = int(target_value / price / 100) * 100
        if target_amount < 100:
            continue
        order_target(stock, target_amount)
