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
    RiceQuant 因子名称: return_on_asset, return_on_equity 等
    """
    # RiceQuant 支持的因子名称
    factor_names = [
        "return_on_asset",
        "return_on_equity",
        "pb_ratio",
        "pe_ratio",
        "market_cap",
    ]

    # 获取因子数据
    try:
        factor_data = get_factor(stocks, factor_names)
        logger.info(
            f"get_factor returned: shape={factor_data.shape if hasattr(factor_data, 'shape') else 'N/A'}"
        )
        if factor_data is not None and not factor_data.empty:
            logger.info(f"get_factor columns: {factor_data.columns.tolist()}")
    except Exception as e:
        logger.warning(f"get_factor failed: {e}")
        return pd.DataFrame()

    if factor_data is None or factor_data.empty:
        logger.warning("get_factor returned empty")
        return pd.DataFrame()

    # factor_data 是 DataFrame，索引为 (order_book_id, date)
    # 需要提取最新数据
    df = pd.DataFrame(index=stocks)

    for factor_name in factor_names:
        if factor_name in factor_data.columns:
            # 获取每个股票的最新因子值
            for stock in stocks:
                try:
                    stock_data = factor_data[factor_name]
                    # 尝试获取该股票的数据
                    if hasattr(stock_data, "loc"):
                        try:
                            value = stock_data.loc[stock]
                            if hasattr(value, "iloc"):
                                value = value.iloc[-1] if len(value) > 0 else np.nan
                            df.loc[stock, factor_name] = value
                        except:
                            df.loc[stock, factor_name] = np.nan
                    else:
                        df.loc[stock, factor_name] = np.nan
                except:
                    df.loc[stock, factor_name] = np.nan

    # 计算 RFScore (简化版)
    # ROA > 0: 1分
    # ROE > 0: 1分
    # PB 低估值: 作为筛选条件而非分数
    df["RFScore"] = 0
    df["RFScore"] += (df["return_on_asset"] > 0).astype(int)
    df["RFScore"] += (df["return_on_equity"] > 10).astype(int)  # ROE > 10%

    logger.info(f"RFScore distribution: {df['RFScore'].value_counts().to_dict()}")
    logger.info(
        f"return_on_asset range: min={df['return_on_asset'].min()}, max={df['return_on_asset'].max()}"
    )
    logger.info(
        f"return_on_equity range: min={df['return_on_equity'].min()}, max={df['return_on_equity'].max()}"
    )

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
    优化版：减少 API 调用次数
    """
    # 获取指数成分股
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")
    stocks = list(set(hs300) | set(zz500))

    if not stocks:
        logger.warning("get_universe: no stocks from index")
        return []

    # 剔除科创板
    stocks = [s for s in stocks if not s.startswith("688")]

    # 预加载所有股票信息
    try:
        all_inst = all_instruments(type="CS")
        inst_dict = {row["order_book_id"]: row for _, row in all_inst.iterrows()}
    except:
        inst_dict = {}

    # 预加载所有 ST 状态
    st_stocks = set()
    for stock in stocks:
        if stock in inst_dict:
            symbol = inst_dict[stock].get("symbol", "")
            if "ST" in symbol or "*" in symbol:
                st_stocks.add(stock)

    # 简化：只检查 ST，跳过停牌检查（由 get_factor 返回空值自然过滤）
    valid_stocks = [s for s in stocks if s not in st_stocks]

    logger.info(f"get_universe: {len(valid_stocks)} valid stocks")
    return valid_stocks


def calc_market_state(context):
    """
    计算市场状态: 市场宽度 + 指数趋势
    RiceQuant 的 bar_dict 不包含个股数据, 使用 history_bars
    """
    # 沪深300成分股
    hs300 = index_components("000300.XSHG")

    # 计算市场宽度: 价格 > 20日均线的比例
    above_ma20 = 0
    total = 0

    for stock in hs300:
        # 获取20日历史价格
        try:
            hist = history_bars(stock, 20, "1d", "close")
            if hist is None or len(hist) < 20:
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

    logger.info(f"calc_market_state: breadth={breadth:.3f}, trend_on={trend_on}")

    return {
        "breadth": breadth,
        "trend_on": trend_on,
        "idx_close": idx_close,
        "idx_ma20": idx_ma20,
    }


def get_pb_ratio(stocks, watch_date):
    """
    获取 PB 市净率
    使用 get_factor 获取 pb_ratio
    """
    try:
        pb_data = get_factor(stocks, "pb_ratio")
        if pb_data is not None and not pb_data.empty:
            # pb_data 是 Series，索引为股票代码
            return pb_data
    except Exception as e:
        logger.warning(f"get pb_ratio failed: {e}")

    return pd.Series(index=stocks)


def calc_rfscore_table(context, stocks, watch_date):
    """
    计算 RFScore + PB 因子表
    """
    df = calc_rfscore_factors(stocks, watch_date)

    if df.empty:
        return df

    # PB 已在 calc_rfscore_factors 中获取
    if "pb_ratio" not in df.columns:
        pb = get_pb_ratio(stocks, watch_date)
        # pb 是 Series，需要正确合并
        for stock in stocks:
            if stock in pb.index:
                df.loc[stock, "pb_ratio"] = pb.loc[stock]

    # 剔除无效数据
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "pb_ratio"])

    logger.info(f"calc_rfscore_table: {len(df)} stocks with valid data")

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
        logger.info(f"pb_group distribution: {df['pb_group'].value_counts().to_dict()}")

    return df


def choose_stocks(context, watch_date, hold_num):
    """
    选股: ROA>0 + ROE>10 + PB低估值
    简化版 RFScore (0-2分)
    """
    stocks = get_universe(context)
    df = calc_rfscore_table(context, stocks, watch_date)

    if df.empty:
        return [], df

    # 主选池: RFScore=2 (ROA>0 且 ROE>10), PB<=10%
    primary = df[
        (df["RFScore"] == 2) & (df["pb_group"] <= context.primary_pb_group)
    ].copy()
    primary = primary.sort_values(
        ["return_on_equity", "return_on_asset", "pb_ratio"],
        ascending=[False, False, True],
    )
    picks = primary.index.tolist()
    logger.info(f"primary pool: {len(picks)} stocks")

    # 补充池: RFScore>=1, PB<=20%
    if len(picks) < hold_num:
        secondary = df[
            (df["RFScore"] >= 1) & (df["pb_group"] <= context.reduced_pb_group)
        ].copy()
        secondary = secondary.sort_values(
            ["RFScore", "return_on_equity", "return_on_asset", "pb_ratio"],
            ascending=[False, False, False, True],
        )
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break
        logger.info(f"secondary pool added: {len(picks)} total")

    # 兜底池: 按因子排序
    if len(picks) < hold_num:
        fallback = df.sort_values(
            ["RFScore", "return_on_equity", "return_on_asset", "pb_ratio"],
            ascending=[False, False, False, True],
        )
        for code in fallback.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break
        logger.info(f"fallback pool added: {len(picks)} total")

    return picks[:hold_num], df


def filter_buyable(context, stocks):
    """
    过滤可买入股票: 剔除涨停、停牌等
    RiceQuant 的 bar_dict 不包含个股数据, 使用 history_bars
    """
    buyable = []

    for stock in stocks:
        # ST 检查
        try:
            inst = instruments(stock)
            if "ST" in inst.symbol or "*" in inst.symbol or "退" in inst.symbol:
                continue
        except:
            continue

        # 获取最新交易数据
        try:
            hist = history_bars(stock, 1, "1d", ["close", "limit_up", "limit_down"])
            if hist is None or len(hist) == 0:
                continue

            close = hist[-1]["close"]
            limit_up = hist[-1]["limit_up"]
            limit_down = hist[-1]["limit_down"]

            # 涨跌停检查
            if limit_up and close >= limit_up * 0.995:
                continue
            if limit_down and close <= limit_down * 1.005:
                continue
        except:
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
        # 检查是否可交易
        try:
            hist = history_bars(stock, 1, "1d", "close")
            if hist is None or len(hist) == 0:
                continue
        except:
            continue

        current_position = portfolio.positions.get(stock)
        current_value = current_position.market_value if current_position else 0

        # 调整到目标市值
        if abs(current_value - target_value_per_stock) > target_value_per_stock * 0.05:
            order_target_value(stock, target_value_per_stock)


def after_trading(context):
    pass
