from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy.stats import linregress


# ============================================================================
# 第一部分：RFScore因子定义
# ============================================================================


class RFScore(Factor):
    """RFScore 7因子模型"""

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

        def sign(ser):
            return ser.apply(lambda x: np.where(x > 0, 1, 0))

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
        self.fscore = self.basic.apply(sign).sum(axis=1)


# ============================================================================
# 第二部分：通用机制实现（精简版，避免超时）
# ============================================================================


class EnhancedStateRouter:
    """改进版状态路由器 - 通用机制03"""

    def __init__(self, index="000300.XSHG"):
        self.index = index

    def calculate_breadth(self, watch_date):
        """计算市场宽度"""
        try:
            hs300 = get_index_stocks(self.index, date=watch_date)
            prices = get_price(
                hs300, end_date=watch_date, count=20, fields=["close"], panel=False
            )
            close = prices.pivot(index="time", columns="code", values="close")
            breadth = float((close.iloc[-1] > close.mean()).mean())
            return breadth
        except:
            return 0.5

    def route(self, watch_date):
        """路由市场状态"""
        breadth = self.calculate_breadth(watch_date)

        if breadth < 0.15:
            return 0.0, 0, "极弱停手", breadth
        elif breadth < 0.25:
            return 0.5, 10, "底部防守", breadth
        elif breadth < 0.35:
            return 0.75, 15, "震荡平衡", breadth
        elif breadth >= 0.40:
            return 1.0, 20, "强趋势", breadth
        else:
            return 0.75, 15, "趋势正常", breadth


class RSRSIndicator:
    """RSRS择时指标 - 通用机制08"""

    def __init__(self, N=18, M=600):
        self.N = N
        self.M = M
        self.slope_series = []

    def calculate_rsrs(self, watch_date, security="000300.XSHG"):
        """计算RSRS指标"""
        try:
            prices = get_price(
                security,
                end_date=watch_date,
                fields=["high", "low"],
                count=self.N,
                panel=False,
            )

            high = prices["high"].values
            low = prices["low"].values

            if len(high) < self.N:
                return None, None

            slope, intercept, r_value, p_value, std_err = linregress(low, high)
            beta = slope
            r2 = r_value**2

            self.slope_series.append(beta)
            if len(self.slope_series) > self.M:
                self.slope_series.pop(0)

            if len(self.slope_series) < 50:
                return None, None

            mean = np.mean(self.slope_series)
            std = np.std(self.slope_series)
            zscore = (beta - mean) / std

            rsrs_rightdev = zscore * beta * r2
            return rsrs_rightdev, beta
        except:
            return None, None

    def get_signal(self, watch_date, buy_threshold=0.7, sell_threshold=-0.7):
        """获取RSRS信号"""
        rsrs_value, beta = self.calculate_rsrs(watch_date)

        if rsrs_value is None:
            return "NEUTRAL", 0.0

        if rsrs_value > buy_threshold:
            return "BULLISH", rsrs_value
        elif rsrs_value < sell_threshold:
            return "BEARISH", rsrs_value
        return "NEUTRAL", rsrs_value


class VolatilityPositionManager:
    """波动率仓位管理 - 通用机制10"""

    def __init__(self, atr_period=20):
        self.atr_period = atr_period
        self.low_vol_threshold = 0.02
        self.high_vol_threshold = 0.05

    def calculate_atr_ratio(self, security, watch_date):
        """计算ATR/价格比率"""
        try:
            df = get_price(
                security,
                end_date=watch_date,
                fields=["high", "low", "close"],
                count=self.atr_period + 1,
                panel=False,
            )

            if len(df) < self.atr_period + 1:
                return None

            high = df["high"].values
            low = df["low"].values
            close = df["close"].values

            tr1 = high - low
            tr2 = np.abs(high - np.roll(close, 1))
            tr3 = np.abs(low - np.roll(close, 1))
            tr = np.maximum(tr1, np.maximum(tr2, tr3))
            tr[0] = high[0] - low[0]

            atr = np.mean(tr[-self.atr_period :])
            current_price = close[-1]

            return atr / current_price
        except:
            return None

    def get_volatility_multiplier(self, security, watch_date):
        """获取波动率乘数"""
        atr_ratio = self.calculate_atr_ratio(security, watch_date)

        if atr_ratio is None:
            return 1.0, "UNKNOWN"

        if atr_ratio < self.low_vol_threshold:
            return 1.2, "LOW"
        elif atr_ratio > self.high_vol_threshold:
            return 0.5, "HIGH"
        else:
            return 1.0, "NORMAL"


# ============================================================================
# 第三部分：策略主函数
# ============================================================================


def initialize(context):
    """初始化"""
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

    g.ipo_days = 180
    g.base_hold_num = 20
    g.reduced_hold_num = 10
    g.primary_pb_group = 1
    g.reduced_pb_group = 2

    # 通用机制实例化（精简版）
    g.state_router = EnhancedStateRouter()
    g.rsrs = RSRSIndicator(N=18, M=600)
    g.vol_mgr = VolatilityPositionManager(atr_period=20)

    # 运行定时任务
    run_monthly(rebalance, 1, time="9:35", reference_security="000300.XSHG")
    run_weekly(record_state, 5, time="15:00", reference_security="000300.XSHG")


def get_universe(watch_date):
    """获取基础股票池"""
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))]

    sec = get_all_securities(types=["stock"], date=watch_date)
    sec = sec.loc[sec.index.intersection(stocks)]
    cutoff_date = (pd.Timestamp(watch_date) - pd.Timedelta(days=g.ipo_days)).date()
    sec = sec[sec["start_date"].apply(lambda x: x <= cutoff_date)]
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
    """计算RFScore表"""
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


def choose_stocks(watch_date, hold_num):
    """选股逻辑"""
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


def filter_buyable(context, stocks):
    """过滤可买入股票"""
    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if stock not in current_data:
            continue
        cd = current_data[stock]
        if cd.paused or cd.is_st:
            continue
        if "ST" in (cd.name or "") or "*" in (cd.name or ""):
            continue
        if cd.last_price >= cd.high_limit * 0.995:
            continue
        if cd.last_price <= cd.low_limit * 1.005:
            continue
        buyable.append(stock)
    return buyable


def rebalance(context):
    """月度调仓主函数"""
    watch_date = context.previous_date

    # 步骤1: 状态路由
    position_ratio, target_hold_num, state, breadth = g.state_router.route(watch_date)

    # 步骤2: RSRS择时确认
    rsrs_signal, rsrs_value = g.rsrs.get_signal(watch_date)

    # 步骤3: 波动率仓位调整
    vol_multiplier, vol_state = g.vol_mgr.get_volatility_multiplier(
        "000300.XSHG", watch_date
    )

    # 综合决策
    final_ratio = position_ratio

    # RSRS调整
    if rsrs_signal == "BEARISH":
        final_ratio *= 0.7
    elif rsrs_signal == "BULLISH":
        final_ratio = min(final_ratio * 1.1, 1.0)

    # 波动率调整
    final_ratio *= vol_multiplier
    final_ratio = min(max(final_ratio, 0), 1.0)

    # 计算最终持仓数
    target_hold_num = int(g.base_hold_num * final_ratio)
    target_hold_num = max(target_hold_num, 5) if final_ratio > 0 else 0

    # 日志输出
    log.info("=" * 60)
    log.info(f"【{watch_date}】RFScore v2.0 调仓决策")
    log.info(f"  状态路由: {state} | 宽度: {breadth:.1%}")
    log.info(
        f"  RSRS信号: {rsrs_signal} | 值: {rsrs_value:.2f}"
        if rsrs_value
        else f"  RSRS信号: {rsrs_signal}"
    )
    log.info(f"  波动率状态: {vol_state} | 乘数: {vol_multiplier:.1f}")
    log.info(f"  最终仓位: {final_ratio:.0%} | 目标持仓: {target_hold_num}只")
    log.info("=" * 60)

    # 执行选股
    if target_hold_num > 0:
        target_stocks, _ = choose_stocks(watch_date, target_hold_num)
        target_stocks = filter_buyable(context, target_stocks)
    else:
        target_stocks = []

    # 执行调仓
    current_positions = list(context.portfolio.positions.keys())
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if target_stocks:
        current_data = get_current_data()
        target_value = context.portfolio.total_value * final_ratio / len(target_stocks)
        for stock in target_stocks:
            price = current_data[stock].last_price
            if price > 0:
                target_amount = int(target_value / price / 100) * 100
                if target_amount >= 100:
                    order_target(stock, target_amount)


def record_state(context):
    """每周记录状态"""
    watch_date = context.previous_date
    position_ratio, _, state, breadth = g.state_router.route(watch_date)
    rsrs_signal, rsrs_value = g.rsrs.get_signal(watch_date)

    record(
        breadth=breadth,
        position_ratio=position_ratio,
        state=state,
        rsrs_signal=rsrs_signal,
        rsrs_value=rsrs_value if rsrs_value else 0,
    )
