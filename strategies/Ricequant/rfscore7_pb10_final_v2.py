# RFScore7 + PB10% 纯进攻策略 (RiceQuant 版)
# 基于 F-Score 改进版，结合 PB 低估值选股
# 原版: JoinQuant rfscore7_pb10_final_v2.py


import pandas as pd
import numpy as np


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


def calc_rfscore_factors(stocks, watch_date):
    """
    使用 RiceQuant get_factor 获取财务数据并计算 RFScore
    RiceQuant 使用 get_factor 而不是 jqfactor 的 Factor 类
    """
    # RiceQuant 支持的因子名称
    factor_names = [
        "roa",
        "net_operate_cash_flow",
        "total_assets",
        "total_non_current_liability",
        "gross_profit_margin",
        "operating_revenue",
    ]

    # 获取当前期因子
    try:
        current_factors = get_factor(stocks, factor_names)
    except Exception as e:
        logger.warning(f"get_factor failed: {e}")
        return pd.DataFrame()

    if current_factors is None or current_factors.empty:
        return pd.DataFrame()

    # 获取历史期因子 (用于计算变化率)
    hist_factors = None

    # 计算各指标
    df = pd.DataFrame(index=stocks)

    # ROA
    roa = current_factors.get("roa", pd.Series(index=stocks))
    df["ROA"] = roa

    # DELTA_ROA: ROA 同比变化
    if hist_factors is not None and "roa" in hist_factors:
        roa_hist = hist_factors.get("roa", pd.Series(index=stocks))
        df["DELTA_ROA"] = roa / roa_hist - 1
    else:
        df["DELTA_ROA"] = np.nan

    # OCFOA: 经营现金流 / 总资产 (4期平均)
    ocf = current_factors.get("net_operate_cash_flow", pd.Series(index=stocks))
    ta = current_factors.get("total_assets", pd.Series(index=stocks))
    if ta is not None and ta.mean() > 0:
        df["OCFOA"] = ocf / ta
    else:
        df["OCFOA"] = np.nan

    # ACCRUAL: OCFOA - ROA
    df["ACCRUAL"] = df["OCFOA"] - df["ROA"] * 0.01

    # DELTA_LEVELER: 杠杆变化
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

    # DELTA_MARGIN: 毛利率变化
    gpm = current_factors.get("gross_profit_margin", pd.Series(index=stocks))
    if hist_factors is not None and "gross_profit_margin" in hist_factors:
        gpm_hist = hist_factors.get("gross_profit_margin", pd.Series(index=stocks))
        df["DELTA_MARGIN"] = gpm / gpm_hist - 1
    else:
        df["DELTA_MARGIN"] = np.nan

    # DELTA_TURN: 资产周转率变化
    rev = current_factors.get("operating_revenue", pd.Series(index=stocks))
    if hist_factors is not None and "operating_revenue" in hist_factors:
        rev_hist = hist_factors.get("operating_revenue", pd.Series(index=stocks))
        turnover = rev / ta
        turnover_hist = rev_hist / ta_hist
        df["DELTA_TURN"] = turnover / turnover_hist - 1
    else:
        df["DELTA_TURN"] = np.nan

    # 计算 RFScore
    df = df.replace([np.inf, -np.inf], np.nan)
    df["RFScore"] = df.apply(sign).sum(axis=1)

    return df


def init(context):
    context.benchmark = "000300.XSHG"

    context.ipo_days = 180
    context.base_hold_num = 20
    context.reduced_hold_num = 10
    context.breadth_reduce = 0.25
    context.breadth_stop = 0.15
    context.primary_pb_group = 1
    context.reduced_pb_group = 2
    context.last_market_state = {}

    scheduler.run_monthly(rebalance, monthday=1)


def get_universe(context):
    """
    获取股票池: 沪深300 + 中证500, 剔除 ST、停牌、新股
    """
    bar_dict = context.bar_dict

    # 获取指数成分股
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")
    stocks = list(set(hs300) | set(zz500))

    if not stocks:
        logger.warning("get_universe: no stocks from index")
        return []

    # 剔除科创板
    stocks = [s for s in stocks if not s.startswith("688")]

    # 剔除新股、ST 和停牌
    valid_stocks = []
    today = context.now.date()

    for stock in stocks:
        if stock not in bar_dict:
            continue
        bar = bar_dict[stock]
        if bar.is_trading is False:
            continue

        # 检查 ST
        try:
            inst = instruments(stock)
            if "ST" in inst.symbol or "*" in inst.symbol:
                continue
        except:
            continue

        # 检查上市时间
        try:
            inst_df = all_instruments(type="CS")
            inst_row = inst_df[inst_df["order_book_id"] == stock]
            if not inst_row.empty:
                listed_date = pd.to_datetime(inst_row.iloc[0]["listed_date"])
                if (today - listed_date.date()).days < context.ipo_days:
                    continue
        except:
            pass

        valid_stocks.append(stock)

    logger.info(f"get_universe: {len(valid_stocks)} valid stocks")
    return valid_stocks


def calc_market_state(context):
    """
    计算市场状态: 市场宽度 + 指数趋势
    """
    bar_dict = context.bar_dict

    # 沪深300成分股
    hs300 = index_components("000300.XSHG")

    # 计算市场宽度: 价格 > 20日均线的比例
    above_ma20 = 0
    total = 0

    for stock in hs300:
        if stock not in bar_dict:
            continue
        # 获取20日历史价格
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

    breadth = above_ma20 / max(total, 1)

    # 沪深300指数趋势
    try:
        idx_hist = history_bars("000300.XSHG", 20, "1d", "close")
        idx_close = idx_hist[-1]
        idx_ma20 = idx_hist.mean()
        trend_on = idx_close > idx_ma20
    except Exception:
        idx_close = 0
        idx_ma20 = 0
        trend_on = False

    return {
        "breadth": breadth,
        "trend_on": trend_on,
        "idx_close": idx_close,
        "idx_ma20": idx_ma20,
    }


def get_pb_ratio(stocks, watch_date):
    """
    获取 PB 市净率
    RiceQuant 使用 get_factor 获取估值因子
    """
    try:
        pb_data = get_factor(stocks, "pb_ratio")
        if pb_data is not None and not pb_data.empty:
            return pb_data.get("pb_ratio", pd.Series())
    except Exception as e:
        logger.warning(f"get pb_ratio failed: {e}")

    # 备用: 使用 instruments 获取估值信息
    pb_dict = {}
    for stock in stocks:
        try:
            inst = instruments(stock)
            # RiceQuant instruments 可能包含估值信息
            pb_dict[stock] = getattr(inst, "pb", np.nan)
        except Exception:
            pb_dict[stock] = np.nan

    return pd.Series(pb_dict)


def calc_rfscore_table(context, stocks, watch_date):
    """
    计算 RFScore + PB 因子表
    """
    df = calc_rfscore_factors(stocks, watch_date)

    if df.empty:
        return df

    # 获取 PB
    pb = get_pb_ratio(stocks, watch_date)
    df["pb_ratio"] = pb

    # 剔除无效数据
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "pb_ratio"])

    # PB 分组 (10档)
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


def choose_stocks(context, watch_date, hold_num):
    """
    选股: RFScore=7 + PB低估值
    """
    stocks = get_universe(context)
    df = calc_rfscore_table(context, stocks, watch_date)

    if df.empty:
        return [], df

    # 主选池: RFScore=7, PB<=10%
    primary = df[
        (df["RFScore"] == 7) & (df["pb_group"] <= context.primary_pb_group)
    ].copy()
    primary = primary.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
        ascending=[False, False, False, False, False, True],
    )
    picks = primary.index.tolist()

    # 补充池: RFScore>=6, PB<=20%
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

    # 兜底池: 按因子排序
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
    """
    过滤可买入股票: 剔除涨停、停牌等
    """
    bar_dict = context.bar_dict
    buyable = []

    for stock in stocks:
        if stock not in bar_dict:
            continue

        bar = bar_dict[stock]

        # 停牌
        if bar.is_trading is False:
            continue

        # ST 检查
        inst = instruments(stock)
        if "ST" in inst.symbol or "*" in inst.symbol or "退" in inst.symbol:
            continue

        # 涨跌停检查
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
    """
    月度调仓
    """
    # 保存 bar_dict 到 context 供其他函数使用
    context.bar_dict = bar_dict

    watch_date = context.now.date()
    market_state = calc_market_state(context)
    context.last_market_state = market_state

    # 根据市场状态决定仓位
    if market_state["breadth"] < context.breadth_stop and (
        not market_state["trend_on"]
    ):
        target_stocks = []
        target_hold_num = 0
    elif market_state["breadth"] < context.breadth_reduce and (
        not market_state["trend_on"]
    ):
        target_hold_num = context.reduced_hold_num
        target_stocks, factor_table = choose_stocks(
            context, watch_date, target_hold_num
        )
        target_stocks = filter_buyable(context, target_stocks)
    else:
        target_hold_num = context.base_hold_num
        target_stocks, factor_table = choose_stocks(
            context, watch_date, target_hold_num
        )
        target_stocks = filter_buyable(context, target_stocks)

    logger.info(
        "rebalance: date=%s breadth=%.3f trend=%s hold_num=%s count=%s"
        % (
            str(watch_date),
            market_state["breadth"],
            str(market_state["trend_on"]),
            str(target_hold_num),
            str(len(target_stocks)),
        )
    )

    # 清仓不在目标池的股票
    for stock in context.portfolio.positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if not target_stocks:
        return

    # 等权买入
    portfolio = context.portfolio
    total_value = portfolio.total_value
    cash = portfolio.cash

    # 计算目标市值
    current_positions_value = sum(
        portfolio.positions[s].market_value
        for s in portfolio.positions
        if s in target_stocks
    )
    available_for_new = cash + sum(
        portfolio.positions[s].market_value
        for s in portfolio.positions
        if s not in target_stocks
    )

    target_value_per_stock = total_value / max(len(target_stocks), 1)

    for stock in target_stocks:
        if stock not in bar_dict:
            continue

        current_position = portfolio.positions.get(stock)
        current_value = current_position.market_value if current_position else 0

        # 调整到目标市值
        if abs(current_value - target_value_per_stock) > target_value_per_stock * 0.05:
            order_target_value(stock, target_value_per_stock)


def after_trading(context):
    pass
