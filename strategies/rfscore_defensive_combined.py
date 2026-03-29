"""
RFScore7 PB10% + 防守底仓组合策略

组合配置:
- RFScore7 PB10% (进攻层): 40-50% 仓位，根据市场状态动态调整
- 国债固收+ (防守层): 30% 仓位，75%国债+10%黄金+8%红利+4%纳指+3%现金
- 现金缓冲: 20-30% 仓位

回测周期: 2018-01-01 到 2025-03-28
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np


# ========== RFScore因子定义 ==========
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


# ========== 初始化函数 ==========
def initialize(context):
    # 设置基准
    set_benchmark("000300.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("order", "error")

    # 设置手续费
    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    # 防守层ETF手续费（基金）
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

    # 仓位配置参数
    g.offensive_weight = 0.50  # 进攻层RFScore默认50%
    g.defensive_weight = 0.30  # 防守层固收+默认30%
    g.cash_buffer = 0.20  # 现金缓冲默认20%

    # 防守层标的配置
    g.defensive_assets = {
        "511010.XSHG": 0.75,  # 国债ETF 75% of defensive
        "518880.XSHG": 0.10,  # 黄金ETF 10%
        "510880.XSHG": 0.08,  # 红利ETF 8%
        "513100.XSHG": 0.04,  # 纳指ETF 4%
    }
    g.defensive_rebalance_threshold = 0.15

    # RFScore参数
    g.ipo_days = 180
    g.base_hold_num = 20
    g.reduced_hold_num = 10
    g.breadth_reduce = 0.25
    g.breadth_stop = 0.15
    g.primary_pb_group = 1
    g.reduced_pb_group = 2
    g.last_market_state = {}

    # 调度任务
    run_monthly(rebalance_offensive, 1, time="9:35", reference_security="000300.XSHG")
    run_daily(rebalance_defensive, time="9:40")
    run_daily(record_state, time="14:50")


# ========== 获取股票池 ==========
def get_universe(watch_date):
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

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


# ========== 计算市场状态 ==========
def calc_market_state(watch_date):
    hs300 = get_index_stocks("000300.XSHG", date=watch_date)
    prices = get_price(
        hs300, end_date=watch_date, count=20, fields=["close"], panel=False
    )
    close = prices.pivot(index="time", columns="code", values="close")
    breadth = float((close.iloc[-1] > close.mean()).mean())

    idx = get_price("000300.XSHG", end_date=watch_date, count=20, fields=["close"])
    idx_close = float(idx["close"].iloc[-1])
    idx_ma20 = float(idx["close"].mean())
    trend_on = idx_close > idx_ma20

    return {
        "breadth": breadth,
        "trend_on": trend_on,
        "idx_close": idx_close,
        "idx_ma20": idx_ma20,
    }


# ========== 计算RFScore ==========
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
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    return df


# ========== 选股 ==========
def choose_stocks(watch_date, hold_num):
    stocks = get_universe(watch_date)
    df = calc_rfscore_table(stocks, str(watch_date))

    primary = df[(df["RFScore"] == 7) & (df["pb_group"] <= g.primary_pb_group)].copy()
    primary = primary.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
        ascending=[False, False, False, False, False, True],
    )
    picks = primary.index.tolist()

    if len(picks) < hold_num:
        secondary = df[
            (df["RFScore"] >= 6) & (df["pb_group"] <= g.reduced_pb_group)
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

    return picks[:hold_num], df


# ========== 过滤可买入 ==========
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


# ========== 进攻层调仓 ==========
def rebalance_offensive(context):
    watch_date = context.previous_date
    market_state = calc_market_state(watch_date)
    g.last_market_state = market_state

    # 根据市场状态调整仓位
    if market_state["breadth"] < g.breadth_stop and not market_state["trend_on"]:
        target_hold_num = 0
        g.current_offensive_weight = 0.0  # 空仓
    elif market_state["breadth"] < g.breadth_reduce and not market_state["trend_on"]:
        target_hold_num = g.reduced_hold_num
        g.current_offensive_weight = 0.25  # 降仓
    else:
        target_hold_num = g.base_hold_num
        g.current_offensive_weight = g.offensive_weight  # 正常仓位

    log.info(
        f"市场状态: 宽度={market_state['breadth']:.3f}, 趋势={'向上' if market_state['trend_on'] else '向下'}, "
        f"进攻仓位={g.current_offensive_weight:.0%}"
    )

    # 选股
    if target_hold_num > 0:
        target_stocks, _ = choose_stocks(watch_date, target_hold_num)
        target_stocks = filter_buyable(context, target_stocks)
    else:
        target_stocks = []

    # 清理不在目标列表的进攻层持仓
    defensive_etfs = list(g.defensive_assets.keys())
    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks and stock not in defensive_etfs:
            order_target_value(stock, 0)

    # 调仓进攻层
    if target_stocks and g.current_offensive_weight > 0:
        total_value = context.portfolio.total_value
        offensive_value = total_value * g.current_offensive_weight
        target_value_per_stock = offensive_value / len(target_stocks)

        current_data = get_current_data()
        for stock in target_stocks:
            order_target_value(stock, target_value_per_stock)


# ========== 防守层调仓 ==========
def rebalance_defensive(context):
    total_value = context.portfolio.total_value
    defensive_value = total_value * g.defensive_weight

    positions = context.portfolio.positions
    defensive_etfs = list(g.defensive_assets.keys())

    # 检查偏离度
    need_rebalance = False
    for etf, target_ratio in g.defensive_assets.items():
        target_value = defensive_value * target_ratio
        if etf in positions:
            current_value = positions[etf].value
        else:
            current_value = 0

        deviation = (
            abs(current_value - target_value) / defensive_value
            if defensive_value > 0
            else 0
        )
        if deviation > g.defensive_rebalance_threshold:
            need_rebalance = True
            break

    if need_rebalance:
        log.info("防守层再平衡触发")
        for etf, target_ratio in g.defensive_assets.items():
            target_value = defensive_value * target_ratio
            order_target_value(etf, target_value)


# ========== 记录状态 ==========
def record_state(context):
    watch_date = context.previous_date
    if watch_date:
        state = calc_market_state(watch_date)
        record(breadth=state["breadth"], hs300_close=state["idx_close"])
