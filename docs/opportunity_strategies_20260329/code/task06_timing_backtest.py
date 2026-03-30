#!/usr/bin/env python3
"""任务06: 宏观+情绪择时框架 - 三组对照回测"""

from jqdata import *
from jqdata import macro
import pandas as pd
import numpy as np
import datetime as dt
from scipy import optimize as op

# ============================================================
# 全局配置
# ============================================================


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    set_benchmark("000300.XSHG")
    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    # 择时模式: 0=无择时, 1=仅情绪择时, 2=宏观+情绪择时
    g.timing_mode = 2  # 默认使用宏观+情绪择时

    # 最大持仓数
    g.max_positions = 5
    g.position_value_ratio = 0.2  # 每只股票最大仓位比例

    # 宏观层状态 (月度更新)
    g.macro_state = 2  # 0=萧条, 1=衰退, 2=中性, 3=过热
    g.macro_score = 50  # 宏观综合得分 0-100
    g.last_macro_update = None

    # 市场层状态 (周度更新)
    g.market_state = 2  # 0=极度悲观, 1=悲观, 2=中性, 3=乐观, 4=极度乐观
    g.market_score = 50  # 市场综合得分 0-100
    g.last_market_update = None

    # 情绪层状态 (日度更新)
    g.sentiment_state = 2  # 0=冰点, 1=低迷, 2=中性, 3=活跃, 4=狂热
    g.sentiment_score = 50  # 情绪综合得分 0-100
    g.hl_count = 0  # 今日涨停家数
    g.ll_count = 0  # 今日跌停家数
    g.max_board = 0  # 最高连板数

    # 仓位控制
    g.total_position_ratio = 1.0  # 总仓位比例
    g.target_stocks = []  # 目标买入列表

    # 运行
    run_daily(update_macro_state, "9:00")
    run_daily(update_market_state, "9:05")
    run_daily(update_sentiment_state, "9:10")
    run_daily(calculate_position_ratio, "9:15")
    run_daily(get_stock_list, "9:20")
    run_daily(buy, "9:35")
    run_daily(sell, "14:50")
    run_daily(record_stats, "15:02")


# ============================================================
# 宏观月频层
# ============================================================
def update_macro_state(context):
    """更新宏观状态 - 月度"""
    if g.timing_mode != 2:
        return

    current_date = context.current_dt.strftime("%Y-%m")

    # 每月只更新一次
    if g.last_macro_update == current_date:
        return
    g.last_macro_update = current_date

    try:
        # 获取PMI数据
        pmi_df = macro.run_query(
            query(
                macro.MAC_MANUFACTURING_PMI.stat_month,
                macro.MAC_MANUFACTURING_PMI.pmi,
                macro.MAC_MANUFACTURING_PMI.produce_idx,
                macro.MAC_MANUFACTURING_PMI.new_orders_idx,
                macro.MAC_MANUFACTURING_PMI.raw_material_idx,
                macro.MAC_MANUFACTURING_PMI.finished_produce_idx,
            )
            .filter(
                macro.MAC_MANUFACTURING_PMI.stat_month
                >= calc_n_months_ago(current_date, 15),
                macro.MAC_MANUFACTURING_PMI.stat_month <= current_date,
            )
            .order_by(macro.MAC_MANUFACTURING_PMI.stat_month.asc())
        )

        if len(pmi_df) >= 3:
            latest_pmi = pmi_df["pmi"].iloc[-1]

            # 计算PMI斜率(3个月)
            recent_3 = pmi_df["pmi"].tail(3).values
            if len(recent_3) == 3:
                slope = np.polyfit([0, 1, 2], recent_3, 1)[0]
            else:
                slope = 0

            # 新订单扩散指数
            new_orders_diff = (
                pmi_df["new_orders_idx"].iloc[-1] - pmi_df["produce_idx"].iloc[-1]
            )

            # 库存信号
            inventory_sig = (
                pmi_df["raw_material_idx"].iloc[-1]
                - pmi_df["finished_produce_idx"].iloc[-1]
            )

            # 综合评分
            score = 50
            score += 15 if latest_pmi >= 50 else -15  # PMI荣枯线
            score += 10 * max(-1, min(1, slope / 0.5))  # 斜率方向
            score += 5 * max(-1, min(1, new_orders_diff / 5))  # 新订单扩散
            score += 5 * max(-1, min(1, -inventory_sig / 5))  # 库存(反向)

            score = max(0, min(100, score))
            g.macro_score = score

            # 状态划分
            if score >= 70:
                g.macro_state = 3  # 过热
            elif score >= 55:
                g.macro_state = 2  # 中性
            elif score >= 40:
                g.macro_state = 1  # 衰退
            else:
                g.macro_state = 0  # 萧条

            record(宏观得分=g.macro_score, 宏观状态=g.macro_state)
    except Exception as e:
        pass


# ============================================================
# 市场周频层
# ============================================================
def update_market_state(context):
    """更新市场状态 - 周度"""
    current_date = context.current_dt

    # 每周一只更新
    weekday = current_date.weekday()
    week_key = current_date.strftime("%Y-W%W")
    if g.last_market_update == week_key:
        return
    if weekday != 0:  # 只在周一更新
        if g.last_market_update is None:
            g.last_market_update = week_key
        return
    g.last_market_update = week_key

    try:
        # 指数趋势
        hs300 = get_price(
            "000300.XSHG",
            end_date=context.previous_date,
            count=60,
            fields=["close"],
            panel=False,
        )
        if len(hs300) >= 60:
            close_series = hs300["close"].values
            ma20 = np.mean(close_series[-20:])
            ma60 = np.mean(close_series[-60:])
            current_price = close_series[-1]

            trend_score = 50
            if current_price > ma20:
                trend_score += 15
            else:
                trend_score -= 15
            if ma20 > ma60:
                trend_score += 10
            else:
                trend_score -= 10

            # 周度收益
            week_return = (
                (close_series[-1] / close_series[-5] - 1) * 100
                if len(close_series) >= 5
                else 0
            )
            trend_score += max(-10, min(10, week_return * 5))

            trend_score = max(0, min(100, trend_score))
            g.market_score = trend_score

            if trend_score >= 75:
                g.market_state = 4  # 极度乐观
            elif trend_score >= 60:
                g.market_state = 3  # 乐观
            elif trend_score >= 45:
                g.market_state = 2  # 中性
            elif trend_score >= 30:
                g.market_state = 1  # 悲观
            else:
                g.market_state = 0  # 极度悲观

            record(市场得分=g.market_score, 市场状态=g.market_state)
    except Exception as e:
        pass


# ============================================================
# 情绪日频层
# ============================================================
def update_sentiment_state(context):
    """更新情绪状态 - 日度"""
    current_date = context.previous_date

    try:
        # 获取当日涨停跌停
        all_stocks = get_all_securities("stock", date=current_date).index.tolist()
        all_stocks = [
            s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
        ]

        # 取样计算(性能优化)
        sample_stocks = all_stocks[:500]
        df = get_price(
            sample_stocks,
            end_date=current_date,
            count=1,
            fields=["close", "high_limit", "low_limit"],
            panel=False,
        )
        df = df.dropna()

        hl_count = len(df[df["close"] == df["high_limit"]])
        ll_count = len(df[df["close"] == df["low_limit"]])

        g.hl_count = hl_count
        g.ll_count = ll_count

        # 计算情绪得分
        score = 50

        # 涨停家数得分(相对于历史分位)
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

        # 涨跌停比
        ratio = hl_count / max(ll_count, 1)
        if ratio > 5:
            score += 15
        elif ratio > 2:
            score += 5
        elif ratio < 0.5:
            score -= 15
        elif ratio < 1:
            score -= 5

        # 最高连板数(近似估算)
        try:
            hl_stocks = df[df["close"] == df["high_limit"]].index.tolist()[:50]
            if len(hl_stocks) > 0:
                board_df = get_price(
                    hl_stocks,
                    end_date=current_date,
                    count=5,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                board_df = board_df.dropna()

                max_board = 1
                for stock in hl_stocks[:20]:
                    stock_data = board_df[board_df["code"] == stock]
                    if len(stock_data) < 2:
                        continue
                    consecutive = 1
                    prices = stock_data["close"].values
                    limits = stock_data["high_limit"].values
                    for j in range(len(prices) - 2, -1, -1):
                        if prices[j] == limits[j]:
                            consecutive += 1
                        else:
                            break
                    max_board = max(max_board, consecutive)

                g.max_board = max_board

                if max_board >= 6:
                    score += 10
                elif max_board >= 4:
                    score += 5
                elif max_board <= 2:
                    score -= 5
        except:
            pass

        score = max(0, min(100, score))
        g.sentiment_score = score

        if score >= 75:
            g.sentiment_state = 4  # 狂热
        elif score >= 60:
            g.sentiment_state = 3  # 活跃
        elif score >= 45:
            g.sentiment_state = 2  # 中性
        elif score >= 30:
            g.sentiment_state = 1  # 低迷
        else:
            g.sentiment_state = 0  # 冰点

        record(
            情绪得分=g.sentiment_score,
            情绪状态=g.sentiment_state,
            涨停数=g.hl_count,
            跌停数=g.ll_count,
            最高连板=g.max_board,
        )
    except Exception as e:
        pass


# ============================================================
# 仓位计算
# ============================================================
def calculate_position_ratio(context):
    """根据三层状态计算目标仓位"""
    if g.timing_mode == 0:
        # 无择时: 全仓
        g.total_position_ratio = 1.0
    elif g.timing_mode == 1:
        # 仅情绪择时
        if g.sentiment_state >= 3:  # 活跃/狂热
            g.total_position_ratio = 1.0
        elif g.sentiment_state == 2:  # 中性
            g.total_position_ratio = 0.6
        elif g.sentiment_state == 1:  # 低迷
            g.total_position_ratio = 0.3
        else:  # 冰点
            g.total_position_ratio = 0.0
    elif g.timing_mode == 2:
        # 宏观+情绪择时
        # 首先由宏观层决定基础仓位
        if g.macro_state == 3:  # 过热
            base_ratio = 0.8
        elif g.macro_state == 2:  # 中性
            base_ratio = 0.6
        elif g.macro_state == 1:  # 衰退
            base_ratio = 0.3
        else:  # 萧条
            base_ratio = 0.0

        # 情绪层调节
        if g.sentiment_state >= 3:  # 活跃/狂热
            sent_adj = 1.0
        elif g.sentiment_state == 2:  # 中性
            sent_adj = 0.8
        elif g.sentiment_state == 1:  # 低迷
            sent_adj = 0.5
        else:  # 冰点
            sent_adj = 0.2

        g.total_position_ratio = min(1.0, base_ratio * sent_adj)

    record(目标仓位=g.total_position_ratio * 100)


# ============================================================
# 选股 (简化版首板低开策略)
# ============================================================
def get_stock_list(context):
    """选股 - 首板低开策略"""
    g.target_stocks = []

    # 如果仓位为0则不选股
    if g.total_position_ratio <= 0:
        return

    prev_date = context.previous_date

    try:
        # 获取股票池
        all_stocks = get_all_securities("stock", date=prev_date).index.tolist()
        all_stocks = [
            s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
        ]

        # 过滤ST
        st_df = get_extras(
            "is_st", all_stocks, start_date=prev_date, end_date=prev_date, df=True
        )
        if st_df is not None and len(st_df) > 0:
            st_df = st_df.T
            non_st = st_df[st_df.iloc[:, 0] == False].index.tolist()
            all_stocks = non_st

        # 过滤停牌
        paused_df = get_price(
            all_stocks,
            end_date=prev_date,
            count=1,
            fields=["paused"],
            panel=False,
            fill_paused=True,
        )
        if paused_df is not None and len(paused_df) > 0:
            paused_df = paused_df[paused_df["paused"] == 0]
            all_stocks = paused_df["code"].tolist()

        # 获取昨日涨停股票
        df = get_price(
            all_stocks,
            end_date=prev_date,
            count=2,
            fields=["close", "high_limit", "low_limit", "money"],
            panel=False,
        )
        df = df.dropna()

        # 找出昨日涨停的股票
        hl_today = df[df["close"] == df["high_limit"]]["code"].unique()

        # 找出今日预期低开的股票(前日涨停，当日开盘价低于前日收盘价)
        # 注意: 这里用的是prev_date的涨停，实际交易时是下一个交易日

        # 简化逻辑: 选取流通市值较小、成交额较大的涨停股
        if len(hl_today) > 0:
            # 获取市值信息
            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.code.in_(list(hl_today[:100]))
            )
            val_df = get_fundamentals(q, date=prev_date)

            if val_df is not None and len(val_df) > 0:
                # 流通市值 < 100亿
                val_df = val_df[val_df["circulating_market_cap"] < 100]
                val_df = val_df.sort_values("circulating_market_cap")

                candidates = val_df["code"].tolist()[:20]
                g.target_stocks = candidates[: g.max_positions]
    except Exception as e:
        pass


# ============================================================
# 交易执行
# ============================================================
def buy(context):
    """买入执行"""
    if g.total_position_ratio <= 0 or len(g.target_stocks) == 0:
        return

    current_data = get_current_data()
    total_value = context.portfolio.total_value
    target_per_stock = total_value * g.total_position_ratio * g.position_value_ratio

    for stock in g.target_stocks:
        if stock in context.portfolio.positions:
            continue

        if context.portfolio.available_cash < target_per_stock * 0.5:
            break

        try:
            price = current_data[stock].last_price
            if price > 0:
                order_value(
                    stock, min(target_per_stock, context.portfolio.available_cash)
                )
        except:
            continue


def sell(context):
    """卖出执行 - 涨停持有，否则次日冲高卖出"""
    hold_list = list(context.portfolio.positions)
    current_data = get_current_data()

    for stock in hold_list:
        try:
            position = context.portfolio.positions[stock]
            if position.closeable_amount == 0:
                continue

            current_price = current_data[stock].last_price
            high_limit = current_data[stock].high_limit

            # 涨停持有
            if current_price == high_limit:
                continue

            # 不涨停则卖出
            cost = position.avg_cost
            ret = (current_price / cost - 1) * 100

            # 已盈利或持有超过2天
            if ret > 0:
                order_target_value(stock, 0)
        except:
            continue


# ============================================================
# 统计记录
# ============================================================
def record_stats(context):
    """记录统计信息"""
    position_pct = (
        100 * context.portfolio.positions_value / max(context.portfolio.total_value, 1)
    )
    ret_pct = 100 * (
        context.portfolio.total_value / context.portfolio.starting_cash - 1
    )

    record(实际仓位=position_pct, 累计收益=ret_pct)


# ============================================================
# 工具函数
# ============================================================
def calc_n_months_ago(date_str, n):
    """计算n个月前的日期字符串 YYYY-MM"""
    year = int(date_str[:4])
    month = int(date_str[5:7])

    month -= n
    while month <= 0:
        year -= 1
        month += 12

    return f"{year:04d}-{month:02d}"
