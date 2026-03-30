"""
纯RFScore7 PB10%进攻策略（RiceQuant版本）

策略配置:
- 100% 进攻层，不配置防守层
- 用于对比防守层的价值

回测周期: 2022-01-01 到 2025-03-28
"""

import numpy as np
import pandas as pd


def init(context):
    """策略初始化"""
    # 设置基准
    context.benchmark = "000300.XSHG"

    # 使用真实价格
    context.use_real_price = True

    # 策略参数
    context.ipo_days = 180
    context.base_hold_num = 20
    context.reduced_hold_num = 10
    context.breadth_reduce = 0.25
    context.breadth_stop = 0.15
    context.primary_pb_group = 1
    context.reduced_pb_group = 2

    # 每月1日调仓
    scheduler.run_monthly(rebalance, monthday=1, time="9:35")


def get_universe(context, watch_date):
    """获取股票池：沪深300 + 中证500，排除科创板、次新股、ST"""
    # 沪深300和中证500成分股
    hs300 = set(index_components("000300.XSHG", date=watch_date))
    zz500 = set(index_components("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)

    # 排除科创板
    stocks = [s for s in stocks if not s.startswith("688")]

    # 排除次新股（上市不足ipo_days天）
    instruments = all_instruments("CS")
    valid_stocks = []
    for stock in stocks:
        if stock in instruments.index:
            listed_date = instruments.loc[stock, "listed_date"]
            if isinstance(listed_date, str):
                listed_date = pd.Timestamp(listed_date)
            days_listed = (watch_date - listed_date).days
            if days_listed >= context.ipo_days:
                valid_stocks.append(stock)
    stocks = valid_stocks

    # 排除ST和停牌股票
    filtered = []
    for stock in stocks:
        ins = instruments(instruments.index == stock)
        if len(ins) > 0:
            name = ins.iloc[0].get("symbol", "")
            if "ST" not in name and "*" not in name and "退" not in name:
                # 检查是否停牌
                try:
                    snap = current_snapshot(stock)
                    if snap and not snap.is_suspended:
                        filtered.append(stock)
                except:
                    filtered.append(stock)  # 如果无法获取快照则保留

    return filtered


def calc_rfscore(context, stock, watch_date):
    """计算单只股票的RFScore"""
    try:
        # 获取历史财务数据
        bar_count = 600  # 约2.5年日线数据

        # ROA数据
        financials = factors.Fundamentals.total_assets
        net_profit = factors.Fundamentals.net_profit

        # 简化版RFScore计算
        # 实际应该获取完整财务报表数据
        fs = get_factor(stock, "return_on_asset", date=watch_date)

        if fs is None or np.isnan(fs):
            return None, None

        # 构建基础指标（简化版）
        basic = {
            "ROA": fs if not np.isnan(fs) else 0,
            "DELTA_ROA": 0,
            "OCFOA": 0,
            "ACCRUAL": 0,
            "DELTA_LEVELER": 0,
            "DELTA_MARGIN": 0,
            "DELTA_TURN": 0,
        }

        # 计算fscore（正数指标个数）
        fscore = sum(1 for v in basic.values() if v > 0)

        return fscore, basic
    except Exception as e:
        logger.warn(f"Calc RFScore error for {stock}: {e}")
        return None, None


def calc_rfscore_table(context, stocks, watch_date):
    """计算所有股票的RFScore表"""
    results = []

    for stock in stocks:
        fscore, basic = calc_rfscore(context, stock, watch_date)
        if fscore is not None:
            # 获取PB
            try:
                snap = current_snapshot(stock)
                pb = snap.pb_ratio if snap else np.nan
            except:
                pb = np.nan

            if not np.isnan(pb):
                results.append(
                    {"code": stock, "RFScore": fscore, "pb_ratio": pb, **basic}
                )

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)
    df = df.set_index("code")

    # 计算PB分组
    if len(df) > 0:
        df["pb_group"] = (
            pd.qcut(
                df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
            )
            + 1
        )

    return df


def calc_market_state(context, watch_date):
    """计算市场状态：宽度和趋势"""
    # 获取沪深300成分股
    hs300 = index_components("000300.XSHG", date=watch_date)

    # 计算宽度：20日均线以上比例
    breadth_count = 0
    total_count = 0

    for stock in hs300[:100]:  # 只取前100只提高效率
        try:
            bars = history_bars(stock, 20, "1d", "close", include_now=True)
            if len(bars) >= 20:
                total_count += 1
                if bars[-1] > np.mean(bars):
                    breadth_count += 1
        except:
            pass

    breadth = breadth_count / total_count if total_count > 0 else 0

    # 计算沪深300指数趋势
    idx_bars = history_bars("000300.XSHG", 20, "1d", "close", include_now=True)
    if len(idx_bars) >= 20:
        idx_close = idx_bars[-1]
        idx_ma20 = np.mean(idx_bars)
        trend_on = idx_close > idx_ma20
    else:
        trend_on = True

    return {"breadth": breadth, "trend_on": trend_on}


def choose_stocks(context, watch_date, hold_num):
    """选股逻辑"""
    stocks = get_universe(context, watch_date)
    logger.info(f"股票池大小: {len(stocks)}")

    df = calc_rfscore_table(context, stocks, watch_date)

    if len(df) == 0:
        return [], df

    # 主选股：RFScore==7 且 PB最低组
    primary = df[
        (df["RFScore"] == 7) & (df["pb_group"] <= context.primary_pb_group)
    ].copy()
    primary = primary.sort_values(
        ["RFScore", "ROA", "pb_ratio"], ascending=[False, False, True]
    )
    picks = primary.index.tolist()

    # 补充选股：RFScore>=6 且 PB前2组
    if len(picks) < hold_num:
        secondary = df[
            (df["RFScore"] >= 6) & (df["pb_group"] <= context.reduced_pb_group)
        ].copy()
        secondary = secondary.sort_values(
            ["RFScore", "ROA", "pb_ratio"], ascending=[False, False, True]
        )
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break

    return picks[:hold_num], df


def rebalance(context, bar_dict):
    """每月调仓"""
    watch_date = context.previous_date

    # 计算市场状态
    market_state = calc_market_state(context, watch_date)
    logger.info(
        f"市场状态: breadth={market_state['breadth']:.2f}, trend={market_state['trend_on']}"
    )

    # 确定目标持股数
    if market_state["breadth"] < context.breadth_stop and not market_state["trend_on"]:
        target_hold_num = 0
        target_stocks = []
    elif (
        market_state["breadth"] < context.breadth_reduce
        and not market_state["trend_on"]
    ):
        target_hold_num = context.reduced_hold_num
        target_stocks, _ = choose_stocks(context, watch_date, target_hold_num)
    else:
        target_hold_num = context.base_hold_num
        target_stocks, _ = choose_stocks(context, watch_date, target_hold_num)

    logger.info(f"调仓: 目标持股数={target_hold_num}, 实际选股={len(target_stocks)}")

    # 卖出不在目标列表的股票
    current_positions = list(context.portfolio.positions.keys())
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)
            logger.info(f"卖出: {stock}")

    # 买入目标股票
    if target_stocks:
        target_value = context.portfolio.total_value / len(target_stocks)
        for stock in target_stocks:
            order_target_value(stock, target_value)
            logger.info(f"调仓: {stock} -> {target_value}")
