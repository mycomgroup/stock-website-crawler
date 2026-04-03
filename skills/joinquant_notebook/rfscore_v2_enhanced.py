#!/usr/bin/env python3
"""
RFScore PB10 改进版策略 v2.0
整合通用机制库：状态路由 + RSRS择时 + 波动率仓位 + 底部信号 + 换手率过滤 + 移动止盈止损
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy.stats import linregress

print("=" * 80)
print("RFScore PB10 改进版策略 v2.0 - 通用机制整合")
print("=" * 80)

# ============================================================================
# 第一部分：RFScore因子定义（保持不变）
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

        indicators = pd.concat(
            [roa, delta_roa, ocfoa, accrual, delta_leveler, delta_margin, delta_turn],
            axis=1,
        )
        indicators.columns = [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
        self.basic = indicators.replace([-np.inf, np.inf], np.nan)
        self.fscore = self.basic.apply(sign).sum(axis=1)


# ============================================================================
# 第二部分：通用机制实现
# ============================================================================


class EnhancedStateRouter:
    """改进版状态路由器 - 通用机制03"""

    def __init__(self, index="000300.XSHG"):
        self.index = index
        self.state_history = []

    def calculate_breadth(self, watch_date):
        """计算市场宽度 - 沪深300站上MA20比例"""
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

    def calculate_sentiment(self, watch_date):
        """计算情绪 - 涨停家数"""
        try:
            all_stocks = get_all_securities(
                types=["stock"], date=watch_date
            ).index.tolist()
            all_stocks = [s for s in all_stocks if not s.startswith(("68", "4", "8"))][
                :3000
            ]
            df = get_price(
                all_stocks,
                end_date=watch_date,
                fields=["close", "high_limit"],
                count=1,
                panel=False,
            )
            zt_count = len(df[df["close"] >= df["high_limit"] * 0.99])
            return zt_count
        except:
            return 50

    def route(self, watch_date):
        """路由市场状态 - 返回(仓位比例, 持仓数, 状态描述)"""
        breadth = self.calculate_breadth(watch_date)
        zt_count = self.calculate_sentiment(watch_date)

        # 通用机制03状态档位（适配RFScore）
        if breadth < 0.15 or zt_count < 20:
            return 0.0, 0, "极弱停手", breadth, zt_count
        elif breadth < 0.25:
            return 0.5, 10, "底部防守", breadth, zt_count
        elif breadth < 0.35:
            return 0.75, 15, "震荡平衡", breadth, zt_count
        elif breadth >= 0.40 and zt_count >= 80:
            return 1.0, 20, "强趋势", breadth, zt_count
        else:
            return 0.75, 15, "趋势正常", breadth, zt_count


class RSRSIndicator:
    """RSRS择时指标 - 通用机制08"""

    def __init__(self, N=18, M=600):
        self.N = N
        self.M = M
        self.slope_series = []

    def calculate_beta_r2(self, prices):
        """计算斜率和拟合度"""
        high = prices["high"].values
        low = prices["low"].values

        if len(high) < self.N:
            return None, None

        high = high[-self.N :]
        low = low[-self.N :]

        slope, intercept, r_value, p_value, std_err = linregress(low, high)
        return slope, r_value**2

    def calculate_rsrs(self, watch_date, security="000300.XSHG"):
        """计算RSRS指标（右偏修正版）"""
        try:
            prices = get_price(
                security,
                end_date=watch_date,
                fields=["high", "low"],
                count=self.N,
                panel=False,
            )

            beta, r2 = self.calculate_beta_r2(prices)
            if beta is None:
                return None

            self.slope_series.append(beta)
            if len(self.slope_series) > self.M:
                self.slope_series.pop(0)

            if len(self.slope_series) < 50:
                return None

            mean = np.mean(self.slope_series)
            std = np.std(self.slope_series)
            zscore = (beta - mean) / std

            # 右偏修正
            rsrs_rightdev = zscore * beta * r2
            return rsrs_rightdev
        except:
            return None

    def get_signal(self, watch_date, buy_threshold=0.7, sell_threshold=-0.7):
        """获取RSRS信号"""
        rsrs_value = self.calculate_rsrs(watch_date)

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
            return 1.2, "LOW"  # 低波动，可加仓
        elif atr_ratio > self.high_vol_threshold:
            return 0.5, "HIGH"  # 高波动，必须减仓
        else:
            return 1.0, "NORMAL"


class BottomSignalsChecker:
    """底部9项信号检查器 - 通用机制23（简化版5项核心）"""

    def __init__(self):
        pass

    def check_breadth(self, watch_date, threshold=0.15):
        """信号1: 市场宽度"""
        try:
            hs300 = get_index_stocks("000300.XSHG", date=watch_date)
            prices = get_price(
                hs300, end_date=watch_date, count=20, fields=["close"], panel=False
            )
            close = prices.pivot(index="time", columns="code", values="close")
            breadth = (close.iloc[-1] > close.mean()).mean()
            return breadth, breadth < threshold
        except:
            return 0.5, False

    def check_fed(self, watch_date, threshold=2.0):
        """信号2: FED估值"""
        try:
            df = get_fundamentals(
                query(valuation.pe_ratio).filter(valuation.code == "000300.XSHG"),
                date=watch_date,
            )
            pe = float(df["pe_ratio"].iloc[0]) if len(df) > 0 else 15.0
            bond_yield = 2.5
            fed = (100.0 / pe) - bond_yield
            return fed, fed > threshold
        except:
            return 0, False

    def check_pb_below_1(self, watch_date, threshold=0.15):
        """信号3: 破净占比"""
        try:
            df = get_fundamentals(
                query(valuation.code, valuation.pb_ratio)
                .filter(valuation.pb_ratio > 0)
                .limit(2000),
                date=watch_date,
            )
            below_1 = (df["pb_ratio"] < 1).mean()
            return below_1, below_1 > threshold
        except:
            return 0.05, False

    def check_volume(self, watch_date, threshold=5000e8):
        """信号4: 两市成交额"""
        try:
            df = get_price(
                "000001.XSHG", end_date=watch_date, fields="money", count=1, panel=False
            )
            sh_vol = float(df["money"].iloc[-1]) if len(df) > 0 else 1e12
            total_vol = sh_vol * 1.8
            return total_vol, total_vol < threshold
        except:
            return 1e12, False

    def check_limit_up(self, watch_date, threshold=20):
        """信号5: 涨停家数"""
        try:
            stocks = get_all_securities(types=["stock"], date=watch_date).index.tolist()
            stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))][:3000]
            df = get_price(
                stocks,
                end_date=watch_date,
                fields=["close", "high_limit"],
                count=1,
                panel=False,
            )
            zt_count = len(df[df["close"] >= df["high_limit"] * 0.99])
            return zt_count, zt_count < threshold
        except:
            return 50, False

    def check_all(self, watch_date):
        """检查5项核心底部信号"""
        breadth, s1 = self.check_breadth(watch_date)
        fed, s2 = self.check_fed(watch_date)
        pb_below, s3 = self.check_pb_below_1(watch_date)
        volume, s4 = self.check_volume(watch_date)
        zt_count, s5 = self.check_limit_up(watch_date)

        signals = [s1, s2, s3, s4, s5]
        satisfied = sum(signals)

        details = {
            "市场宽度": f"{breadth:.1%} {'✅' if s1 else '❌'}",
            "FED估值": f"{fed:.2f}% {'✅' if s2 else '❌'}",
            "破净占比": f"{pb_below:.1%} {'✅' if s3 else '❌'}",
            "成交额": f"{volume / 1e8:.0f}亿 {'✅' if s4 else '❌'}",
            "涨停家数": f"{zt_count}家 {'✅' if s5 else '❌'}",
        }

        return satisfied, details


class TurnoverFilter:
    """换手率过滤 - 通用机制19 + 任务04验证"""

    def __init__(self, keep_ratio=0.8):
        self.keep_ratio = keep_ratio

    def filter_stocks(self, stocks, watch_date):
        """过滤换手率过高的股票"""
        try:
            # 使用聚宽因子（如果可用）
            df = get_factor_values(
                stocks, factors=["turnover_volatility"], end_date=watch_date, count=1
            )

            if df is None or len(df) == 0:
                return stocks[: int(len(stocks) * self.keep_ratio)]

            factor = df.iloc[-1].dropna().sort_values(ascending=True)
            target_num = int(len(factor) * self.keep_ratio)
            return factor.head(target_num).index.tolist()
        except:
            # 降级方案：返回前80%
            return stocks[: int(len(stocks) * self.keep_ratio)]


class TrailingStopManager:
    """移动止盈止损 - 通用机制17"""

    def __init__(self, stop_loss=-0.10, trailing_stop=0.15):
        self.stop_loss = stop_loss
        self.trailing_stop = trailing_stop
        self.high_prices = {}

    def update_high_price(self, stock, current_price):
        """更新持仓期间最高价"""
        if stock not in self.high_prices:
            self.high_prices[stock] = current_price
        else:
            if current_price > self.high_prices[stock]:
                self.high_prices[stock] = current_price

    def should_close(self, stock, current_price, avg_cost):
        """判断是否应该平仓"""
        if avg_cost <= 0:
            return False, None

        pnl_ratio = (current_price - avg_cost) / avg_cost

        # 止损
        if pnl_ratio <= self.stop_loss:
            return True, "STOP_LOSS"

        # 移动止盈
        if stock in self.high_prices:
            drawdown = (current_price - self.high_prices[stock]) / self.high_prices[
                stock
            ]
            if drawdown <= -self.trailing_stop and pnl_ratio > 0:
                return True, "TRAILING_STOP"

        return False, None

    def remove_position(self, stock):
        """移除持仓记录"""
        self.high_prices.pop(stock, None)


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

    # 基础参数
    g.ipo_days = 180
    g.base_hold_num = 20
    g.reduced_hold_num = 10
    g.primary_pb_group = 1
    g.reduced_pb_group = 2

    # 通用机制实例化
    g.state_router = EnhancedStateRouter()
    g.rsrs = RSRSIndicator(N=18, M=600)
    g.vol_mgr = VolatilityPositionManager(atr_period=20)
    g.bottom_checker = BottomSignalsChecker()
    g.turnover_filter = TurnoverFilter(keep_ratio=0.8)
    g.trailing_stop = TrailingStopManager(stop_loss=-0.10, trailing_stop=0.15)

    # 运行定时任务
    run_monthly(rebalance, 1, time="9:35", reference_security="000300.XSHG")
    run_daily(check_stop_loss, time="14:50", reference_security="000300.XSHG")
    run_weekly(record_state, 5, time="15:00", reference_security="000300.XSHG")


def get_universe(watch_date):
    """获取基础股票池 - 通用机制04"""
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))]

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

    # 应用换手率过滤 - 通用机制19
    stocks = g.turnover_filter.filter_stocks(df.index.tolist(), watch_date)
    df = df.loc[df.index.intersection(stocks)]

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

    # ===== 步骤1: 状态路由 - 通用机制03 =====
    position_ratio, target_hold_num, state, breadth, zt_count = g.state_router.route(
        watch_date
    )

    # ===== 步骤2: RSRS择时确认 - 通用机制08 =====
    rsrs_signal, rsrs_value = g.rsrs.get_signal(watch_date)

    # ===== 步骤3: 波动率仓位调整 - 通用机制10 =====
    vol_multiplier, vol_state = g.vol_mgr.get_volatility_multiplier(
        "000300.XSHG", watch_date
    )

    # ===== 步骤4: 底部信号检查 - 通用机制23 =====
    bottom_satisfied, bottom_details = g.bottom_checker.check_all(watch_date)

    # ===== 综合决策 =====
    # 基础仓位来自状态路由器
    final_ratio = position_ratio

    # RSRS调整
    if rsrs_signal == "BEARISH":
        final_ratio *= 0.7  # RSRS看空，降低30%仓位
    elif rsrs_signal == "BULLISH":
        final_ratio = min(final_ratio * 1.1, 1.0)  # RSRS看多，最多增加10%

    # 波动率调整
    final_ratio *= vol_multiplier
    final_ratio = min(max(final_ratio, 0), 1.0)  # 限制在0-1

    # 底部信号调整（极端底部时，即使状态路由看空也保持一定仓位）
    if bottom_satisfied >= 4 and position_ratio < 0.3:
        final_ratio = max(final_ratio, 0.3)  # 底部信号强烈时，最少30%仓位
        log.info(
            f"⚠️ 底部信号{bottom_satisfied}/5强烈， override仓位至{final_ratio:.0%}"
        )

    # 计算最终持仓数
    target_hold_num = int(g.base_hold_num * final_ratio)
    target_hold_num = (
        max(target_hold_num, 5) if final_ratio > 0 else 0
    )  # 最少5只，除非空仓

    # 日志输出
    log.info("=" * 60)
    log.info(f"【{watch_date}】RFScore v2.0 调仓决策")
    log.info(f"  状态路由: {state} | 宽度: {breadth:.1%} | 涨停: {zt_count}家")
    log.info(
        f"  RSRS信号: {rsrs_signal} | 值: {rsrs_value:.2f}"
        if rsrs_value
        else f"  RSRS信号: {rsrs_signal}"
    )
    log.info(f"  波动率状态: {vol_state} | 乘数: {vol_multiplier:.1f}")
    log.info(f"  底部信号: {bottom_satisfied}/5项满足")
    for k, v in bottom_details.items():
        log.info(f"    {k}: {v}")
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
            g.trailing_stop.remove_position(stock)

    if target_stocks:
        current_data = get_current_data()
        target_value = context.portfolio.total_value * final_ratio / len(target_stocks)
        for stock in target_stocks:
            price = current_data[stock].last_price
            if price > 0:
                target_amount = int(target_value / price / 100) * 100
                if target_amount >= 100:
                    order_target(stock, target_amount)
                    # 记录初始价格用于移动止盈
                    if stock not in g.trailing_stop.high_prices:
                        g.trailing_stop.update_high_price(stock, price)


def check_stop_loss(context):
    """每日检查移动止盈止损 - 通用机制17"""
    current_data = get_current_data()

    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        current_price = pos.price
        avg_cost = pos.avg_cost

        # 更新最高价
        g.trailing_stop.update_high_price(stock, current_price)

        # 检查止盈止损
        should_close, reason = g.trailing_stop.should_close(
            stock, current_price, avg_cost
        )

        if should_close:
            order_target_value(stock, 0)
            g.trailing_stop.remove_position(stock)
            log.info(
                f"🛑 {stock} 触发{reason}平仓 | 成本:{avg_cost:.2f} 现价:{current_price:.2f}"
            )


def record_state(context):
    """每周记录状态"""
    watch_date = context.previous_date
    position_ratio, _, state, breadth, zt_count = g.state_router.route(watch_date)
    rsrs_signal, rsrs_value = g.rsrs.get_signal(watch_date)

    record(
        breadth=breadth,
        zt_count=zt_count,
        position_ratio=position_ratio,
        state=state,
        rsrs_signal=rsrs_signal,
        rsrs_value=rsrs_value if rsrs_value else 0,
    )
