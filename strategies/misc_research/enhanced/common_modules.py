"""
通用增强模块 - 情绪开关 + 风控 + 四档仓位

基于 result_06 和 result_10 的实测结论：
- 情绪层有效（宏观层无效，砍掉）
- 时间止损优于价格止损
- 四档仓位：15/12/10/0
"""

from jqdata import *
import pandas as pd
import numpy as np


class SentimentSwitch:
    """
    情绪择时开关

    基于 result_06 实测：
    - 仅情绪择时年化11.66%，回撤23.55%
    - 无择时策略样本外-28.91%

    开仓条件：
    - 涨停家数 >= 15
    - 最高连板数 >= 2
    """

    def __init__(self):
        self.hl_count = 0
        self.ll_count = 0
        self.max_lianban = 0
        self.sentiment_score = 50
        self.sentiment_state = 2

    def update(self, date):
        try:
            all_stocks = get_all_securities("stock", date=date).index.tolist()
            all_stocks = [
                s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
            ]

            sample = all_stocks[:500]
            df = get_price(
                sample,
                end_date=date,
                count=1,
                fields=["close", "high_limit", "low_limit"],
                panel=False,
            )
            df = df.dropna()

            self.hl_count = len(df[df["close"] == df["high_limit"]])
            self.ll_count = len(df[df["close"] == df["low_limit"]])

            df_lianban = get_price(
                sample,
                end_date=date,
                count=5,
                fields=["close", "high_limit"],
                panel=False,
            )
            if len(df_lianban) > 0:
                df_lianban = df_lianban.pivot(
                    index="time", columns="code", values="close"
                )
                high_limit_pivot = get_price(
                    sample,
                    end_date=date,
                    count=5,
                    fields=["high_limit"],
                    panel=False,
                ).pivot(index="time", columns="code", values="high_limit")

                lianban_counts = {}
                for code in df_lianban.columns:
                    if code in high_limit_pivot.columns:
                        consecutive = 0
                        for i in range(-1, -6, -1):
                            try:
                                if (
                                    df_lianban.iloc[i][code]
                                    == high_limit_pivot.iloc[i][code]
                                ):
                                    consecutive += 1
                                else:
                                    break
                            except:
                                break
                        if consecutive > 0:
                            lianban_counts[code] = consecutive

                self.max_lianban = max(lianban_counts.values()) if lianban_counts else 0
            else:
                self.max_lianban = 0

            score = 50

            if self.hl_count > 80:
                score += 20
            elif self.hl_count > 50:
                score += 10
            elif self.hl_count > 30:
                score += 5
            elif self.hl_count < 15:
                score -= 15
            elif self.hl_count < 25:
                score -= 5

            ratio = self.hl_count / max(self.ll_count, 1)
            if ratio > 5:
                score += 15
            elif ratio > 2:
                score += 5
            elif ratio < 0.5:
                score -= 15
            elif ratio < 1:
                score -= 5

            if self.max_lianban >= 5:
                score += 15
            elif self.max_lianban >= 3:
                score += 8
            elif self.max_lianban >= 2:
                score += 3

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
            pass

    def should_open(self):
        """
        是否应该开仓

        基于 result_06 实测结论：
        - 涨停>=15 + 连板>=2 才开仓
        """
        return self.hl_count >= 15 and self.max_lianban >= 2

    def get_position_ratio(self):
        """
        根据情绪状态获取仓位比例

        状态映射：
        - 4(狂热): 100%
        - 3(活跃): 80%
        - 2(中性): 60%
        - 1(低迷): 30%
        - 0(冰点): 0%
        """
        ratios = {4: 1.0, 3: 0.8, 2: 0.6, 1: 0.3, 0: 0.0}
        return ratios.get(self.sentiment_state, 0.6)


class FourTierPosition:
    """
    四档仓位规则

    基于 result_05 和 final_rfscore_release_v1：
    - 正常(>=40%): 15只
    - 防守(25-40% + trend_off): 12只
    - 底部(15-25%): 10只
    - 极端(<15%): 0只
    """

    def __init__(self, base_hold=15):
        self.base_hold_num = base_hold
        self.defensive_hold_num = 12
        self.bottom_hold_num = 10
        self.extreme_hold_num = 0

        self.breadth_defensive = 0.40
        self.breadth_bottom = 0.25
        self.breadth_extreme = 0.15

    def calc_breadth(self, date):
        hs300 = get_index_stocks("000300.XSHG", date=date)
        prices = get_price(
            hs300,
            end_date=date,
            count=20,
            fields=["close"],
            panel=False,
        )
        close = prices.pivot(index="time", columns="code", values="close")
        breadth = float((close.iloc[-1] > close.mean()).mean())
        return breadth

    def calc_trend(self, date):
        idx = get_price("000300.XSHG", end_date=date, count=20, fields=["close"])
        idx_close = float(idx["close"].iloc[-1])
        idx_ma20 = float(idx["close"].mean())
        return idx_close > idx_ma20

    def get_target_hold_num(self, date):
        """
        获取目标持仓数量

        四档规则：
        - breadth >= 40%: 15只 (正常)
        - breadth < 40% and trend_off: 12只 (防守)
        - breadth < 25%: 10只 (底部)
        - breadth < 15%: 0只 (极端)
        """
        breadth = self.calc_breadth(date)
        trend_on = self.calc_trend(date)

        if breadth < self.breadth_extreme:
            return self.extreme_hold_num, breadth, trend_on
        elif breadth < self.breadth_bottom:
            return self.bottom_hold_num, breadth, trend_on
        elif breadth < self.breadth_defensive and not trend_on:
            return self.defensive_hold_num, breadth, trend_on
        else:
            return self.base_hold_num, breadth, trend_on


class RiskControl:
    """
    风控模块

    基于 result_08 实测结论：
    - 时间止损优于价格止损
    - 10:30未盈利即走
    - 组合熔断：周亏8%强制休息3天
    - 月亏15%强制休息一周
    """

    def __init__(self):
        self.stop_loss_gap = 0.04
        self.time_stop_1030 = True
        self.stop_profit_1330 = 0.03

        self.week_loss_limit = 0.08
        self.month_loss_limit = 0.15

        self.week_start_value = 0
        self.month_start_value = 0
        self.week_start_date = None
        self.month_start_date = None

        self.forced_rest_days = 0
        self.rest_start_date = None

    def init_period(self, context):
        current_dt = context.current_dt
        if self.week_start_date is None:
            self.week_start_date = current_dt
            self.week_start_value = context.portfolio.total_value
        if self.month_start_date is None:
            self.month_start_date = current_dt
            self.month_start_value = context.portfolio.total_value

        if self.rest_start_date:
            days_passed = (current_dt.date() - self.rest_start_date).days
            if days_passed >= self.forced_rest_days:
                self.forced_rest_days = 0
                self.rest_start_date = None

    def check_week_loss(self, context):
        current_dt = context.current_dt
        if (current_dt.date() - self.week_start_date.date()).days >= 7:
            loss_pct = (
                context.portfolio.total_value - self.week_start_value
            ) / self.week_start_value
            self.week_start_date = current_dt
            self.week_start_value = context.portfolio.total_value

            if loss_pct < -self.week_loss_limit:
                self.forced_rest_days = 3
                self.rest_start_date = current_dt.date()
                return True
        return False

    def check_month_loss(self, context):
        current_dt = context.current_dt
        if (current_dt.date() - self.month_start_date.date()).days >= 30:
            loss_pct = (
                context.portfolio.total_value - self.month_start_value
            ) / self.month_start_value
            self.month_start_date = current_dt
            self.month_start_value = context.portfolio.total_value

            if loss_pct < -self.month_loss_limit:
                self.forced_rest_days = 5
                self.rest_start_date = current_dt.date()
                return True
        return False

    def is_in_rest(self, context):
        if self.forced_rest_days > 0 and self.rest_start_date:
            days_passed = (context.current_dt.date() - self.rest_start_date).days
            return days_passed < self.forced_rest_days
        return False

    def time_stop_check(self, context, stock, current_time):
        """
        时间止损检查

        10:30未盈利即走 (优于价格止损)
        """
        if stock not in context.portfolio.positions:
            return False

        position = context.portfolio.positions[stock]
        if position.closeable_amount == 0:
            return False

        current_data = get_current_data()
        if current_data[stock].last_price == current_data[stock].high_limit:
            return False

        cost = position.avg_cost
        price = current_data[stock].last_price

        if current_time.hour == 10 and current_time.minute == 30:
            if price <= cost:
                return True

        return False

    def gap_stop_check(self, context, stock):
        """
        跳空止损

        低开超过4%止损
        """
        if stock not in context.portfolio.positions:
            return False

        position = context.portfolio.positions[stock]
        if position.closeable_amount == 0:
            return False

        current_data = get_current_data()
        cost = position.avg_cost
        price = current_data[stock].last_price

        if price < cost * (1 - self.stop_loss_gap):
            return True

        return False

    def stop_profit_check(self, context, stock, current_time):
        """
        止盈检查

        13:30盈利未达3%即走
        """
        if stock not in context.portfolio.positions:
            return False

        position = context.portfolio.positions[stock]
        if position.closeable_amount == 0:
            return False

        current_data = get_current_data()
        if current_data[stock].last_price == current_data[stock].high_limit:
            return False

        cost = position.avg_cost
        price = current_data[stock].last_price

        if current_time.hour == 13 and current_time.minute == 30:
            if price < cost * (1 + self.stop_profit_1330):
                return True

        return False
