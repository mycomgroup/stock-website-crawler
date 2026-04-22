# 红利/价值/质量 策略 V3: 静态组合版 (60/40) - RiceQuant 版
# RFScore7进攻60% + 红利小盘防守40%
# 原版: strategies/dividend_value_quality_v1/v3_combo_static_60_40.py (JoinQuant)
# 迁移说明:
#   - initialize -> init
#   - run_monthly/run_daily -> handle_bar 内月度检查
#   - get_fundamentals(query(...)) -> get_factor / get_fundamentals (RQ风格)
#   - order_value -> order_target_value
#   - log.info -> logger.info
#   - get_current_data()[s].paused -> instruments(s) + history_bars 检查
#   - valuation.market_cap 单位: RQ 为 万元, JQ 为 亿元 (已换算)

import pandas as pd
import numpy as np


# ─────────────────────────────────────────────
# 初始化
# ─────────────────────────────────────────────
def init(context):
    context.benchmark = "000300.XSHG"

    # 组合配置
    context.rfscore_weight = 0.6   # RFScore7 权重
    context.dividend_weight = 0.4  # 红利小盘权重
    context.rfscore_num = 15       # RFScore7 持仓数
    context.dividend_num = 10      # 红利小盘持仓数

    context.target_rfscore = []
    context.target_dividend = []
    context.hold_list = []
    context.last_rebalance_month = -1

    logger.info("V3 Combo 60/40 initialized")


# ─────────────────────────────────────────────
# 主循环
# ─────────────────────────────────────────────
def handle_bar(context, bar_dict):
    today = context.now

    # 每月第一个交易日调仓
    if today.month != context.last_rebalance_month:
        context.last_rebalance_month = today.month
        adjust_position(context, bar_dict)

    # 每日 14:00 前后检查涨停 (handle_bar 为收盘前，近似处理)
    check_limit_up(context, bar_dict)


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────
def is_tradable(stock, bar_dict):
    """判断股票是否可交易（非停牌、非ST、非退市）"""
    if stock not in bar_dict:
        return False
    if not bar_dict[stock].is_trading:
        return False
    try:
        inst = instruments(stock)
        name = inst.symbol
        if "ST" in name or "*" in name or "退" in name:
            return False
    except Exception:
        return False
    return True


def get_pb_roa(stocks, watch_date):
    """
    获取 pb_ratio 和 return_on_asset (ROA)
    RiceQuant get_factor 返回 MultiIndex DataFrame: (order_book_id, date)
    """
    try:
        df = get_factor(
            stocks,
            ["pb_ratio", "return_on_asset", "return_on_equity", "pe_ratio"],
            start_date=watch_date,
            end_date=watch_date,
        )
    except Exception as e:
        logger.warning(f"get_factor failed: {e}")
        return pd.DataFrame()

    if df is None or df.empty:
        return pd.DataFrame()

    # 展平 MultiIndex: 取最后一个日期的数据
    if isinstance(df.index, pd.MultiIndex):
        df = df.reset_index()
        # 列名可能是 order_book_id 或 stock
        id_col = "order_book_id" if "order_book_id" in df.columns else df.columns[0]
        df = df.rename(columns={id_col: "code"})
        df = df.drop_duplicates(subset="code", keep="last")
        df = df.set_index("code")
    return df


def get_market_cap_pe(stocks, watch_date):
    """
    获取市值和PE，用于红利小盘筛选
    market_cap 单位: RQ 为 元，需转换为亿元
    """
    try:
        df = get_factor(
            stocks,
            ["market_cap", "pe_ratio", "pb_ratio"],
            start_date=watch_date,
            end_date=watch_date,
        )
    except Exception as e:
        logger.warning(f"get_factor (market_cap) failed: {e}")
        return pd.DataFrame()

    if df is None or df.empty:
        return pd.DataFrame()

    if isinstance(df.index, pd.MultiIndex):
        df = df.reset_index()
        id_col = "order_book_id" if "order_book_id" in df.columns else df.columns[0]
        df = df.rename(columns={id_col: "code"})
        df = df.drop_duplicates(subset="code", keep="last")
        df = df.set_index("code")

    # market_cap 单位转换: 元 -> 亿元
    if "market_cap" in df.columns:
        df["market_cap_yi"] = df["market_cap"] / 1e8

    return df


# ─────────────────────────────────────────────
# 选股逻辑
# ─────────────────────────────────────────────
def select_rfscore7(context, bar_dict, n=15):
    """RFScore7 + PB低20% 选股 (沪深300 + 中证500)"""
    watch_date = context.now.date()

    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")
    stocks = list(set(hs300) | set(zz500))

    # 过滤可交易 + 排除科创板
    stocks = [
        s for s in stocks
        if not s.startswith("688") and is_tradable(s, bar_dict)
    ]

    if not stocks:
        return []

    df = get_pb_roa(stocks, str(watch_date))
    if df.empty:
        return []

    # 过滤条件: PE > 0, PB > 0, ROA > 0
    df = df[
        (df["pe_ratio"] > 0) &
        (df["pb_ratio"] > 0) &
        (df["return_on_asset"] > 0)
    ].dropna(subset=["pb_ratio", "return_on_asset"])

    if df.empty:
        return []

    # 取 PB 最低 20%
    pb_threshold = df["pb_ratio"].quantile(0.2)
    df_low_pb = df[df["pb_ratio"] <= pb_threshold]

    # 按 ROA 降序排列
    df_low_pb = df_low_pb.sort_values("return_on_asset", ascending=False)

    result = df_low_pb.index.tolist()[:n]
    logger.info(f"RFScore7 selected: {len(result)} stocks")
    return result


def select_small_dividend(context, bar_dict, n=10):
    """红利小盘选股: 市值10-100亿, PE<30, 净利润增速>5%"""
    watch_date = context.now.date()

    # 全A股作为候选池（排除科创板、北交所）
    # all_instruments 返回 DataFrame，取 order_book_id 列
    try:
        inst_df = all_instruments("CS")
        all_stocks = inst_df["order_book_id"].tolist()
    except Exception:
        all_stocks = index_components("000985.XSHG")  # 中证全指备用

    stocks = [
        s for s in all_stocks
        if not s.startswith("688")
        and not s.startswith("8")
        and not s.startswith("4")
        and is_tradable(s, bar_dict)
    ]

    if not stocks:
        return []

    df = get_market_cap_pe(stocks, str(watch_date))
    if df.empty:
        return []

    # 市值筛选: 10亿 ~ 100亿
    df = df[
        (df["market_cap_yi"] >= 10) &
        (df["market_cap_yi"] <= 100) &
        (df["pe_ratio"] > 0) &
        (df["pe_ratio"] < 30)
    ].dropna(subset=["pe_ratio", "market_cap_yi"])

    if df.empty:
        return []

    # 获取净利润增速 (inc_net_profit_year_on_year -> net_profit_growth_rate)
    candidates = df.index.tolist()
    try:
        growth_df = get_factor(
            candidates,
            ["net_profit_growth_rate"],
            start_date=str(watch_date),
            end_date=str(watch_date),
        )
        if growth_df is not None and not growth_df.empty:
            if isinstance(growth_df.index, pd.MultiIndex):
                growth_df = growth_df.reset_index()
                id_col = "order_book_id" if "order_book_id" in growth_df.columns else growth_df.columns[0]
                growth_df = growth_df.rename(columns={id_col: "code"})
                growth_df = growth_df.drop_duplicates(subset="code", keep="last")
                growth_df = growth_df.set_index("code")
            df = df.join(growth_df[["net_profit_growth_rate"]], how="left")
            df = df[df["net_profit_growth_rate"] > 5]
    except Exception as e:
        logger.warning(f"net_profit_growth_rate failed: {e}, skip growth filter")

    # 按 PE 升序排列
    df = df.sort_values("pe_ratio", ascending=True)

    result = df.index.tolist()[:n]
    logger.info(f"Small dividend selected: {len(result)} stocks")
    return result


# ─────────────────────────────────────────────
# 调仓
# ─────────────────────────────────────────────
def adjust_position(context, bar_dict):
    """月度调仓"""
    context.target_rfscore = select_rfscore7(context, bar_dict, context.rfscore_num)
    context.target_dividend = select_small_dividend(context, bar_dict, context.dividend_num)
    target_list = context.target_rfscore + context.target_dividend

    # 卖出不在目标列表的持仓
    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_list:
            if bar_dict.get(stock) and bar_dict[stock].is_trading:
                order_target_value(stock, 0)
                logger.info(f"卖出: {stock}")

    total_value = context.portfolio.total_value

    # 买入 RFScore7 股票 (60%)
    rfscore_value = total_value * context.rfscore_weight / max(len(context.target_rfscore), 1)
    for stock in context.target_rfscore:
        if bar_dict.get(stock) and bar_dict[stock].is_trading:
            order_target_value(stock, rfscore_value)
            logger.info(f"买入RFScore7: {stock}")

    # 买入红利小盘股票 (40%)
    dividend_value = total_value * context.dividend_weight / max(len(context.target_dividend), 1)
    for stock in context.target_dividend:
        if bar_dict.get(stock) and bar_dict[stock].is_trading:
            order_target_value(stock, dividend_value)
            logger.info(f"买入红利小盘: {stock}")

    context.hold_list = list(context.portfolio.positions.keys())


def check_limit_up(context, bar_dict):
    """检查涨停股，涨停打开时卖出"""
    for stock in list(context.portfolio.positions.keys()):
        if stock not in bar_dict:
            continue
        bar = bar_dict[stock]
        # 当前价低于涨停价 = 涨停已打开（RQ 用 bar.close，涨停价用 bar.limit_up）
        if bar.close < bar.limit_up:
            if stock in context.hold_list:
                order_target_value(stock, 0)
                logger.info(f"涨停打开卖出: {stock}")


def after_trading(context):
    """收盘后更新持仓列表"""
    context.hold_list = list(context.portfolio.positions.keys())
