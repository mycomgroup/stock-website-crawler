"""
RFScore7 + PB10% 完整策略 v2 - RiceQuant 策略编辑器版本

使用 handle_bar 手动判断调仓
"""

import numpy as np
import pandas as pd


def init(context):
    """策略初始化"""
    context.benchmark = "000300.XSHG"
    context.use_real_price = True

    # 策略参数
    context.hold_num = 20
    context.pb_pct = 0.10
    context.breadth_reduce = 0.25
    context.breadth_stop = 0.15
    context.reduced_hold_num = 10

    # 调仓控制
    context.last_rebalance_month = -1

    logger.info("RFScore7 + PB10% v2 策略初始化完成")


def handle_bar(context, bar_dict):
    """每日执行"""
    today = context.now

    # 每月第一个交易日调仓
    if context.last_rebalance_month != today.month:
        context.last_rebalance_month = today.month
        rebalance(context, bar_dict)


def get_universe(context):
    """获取股票池"""
    hs300 = set(index_components("000300.XSHG"))
    zz500 = set(index_components("000905.XSHG"))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]
    return stocks


def calc_rfscore7(context, stocks):
    """计算 RFScore7 因子"""
    date_str = context.now.strftime("%Y-%m-%d")

    try:
        # 获取财务因子
        factors = [
            "roa",
            "roe",
            "gross_profit_margin",
            "net_profit_margin",
            "net_profit_yoy",
            "or_yoy",
            "pe_ratio",
            "pb_ratio",
        ]

        df = get_factor(stocks, factors, start_date=date_str, end_date=date_str)

        if df is None or df.empty:
            logger.warn("获取因子数据失败")
            return pd.DataFrame()

        # 处理数据
        if "date" in df.columns:
            df = df.groupby("order_book_id").last().reset_index()

        # 计算 RFScore7
        df["rfscore7"] = 0

        if "roa" in df.columns:
            df.loc[df["roa"] > 0, "rfscore7"] += 1
        if "roe" in df.columns:
            df.loc[df["roe"] > 0, "rfscore7"] += 1
        if "gross_profit_margin" in df.columns:
            median_gpm = df["gross_profit_margin"].median()
            df.loc[df["gross_profit_margin"] > median_gpm, "rfscore7"] += 1
        if "net_profit_margin" in df.columns:
            df.loc[df["net_profit_margin"] > 0, "rfscore7"] += 1
        if "net_profit_yoy" in df.columns:
            df.loc[df["net_profit_yoy"] > 0, "rfscore7"] += 1
        if "or_yoy" in df.columns:
            df.loc[df["or_yoy"] > 0, "rfscore7"] += 1
        if "pe_ratio" in df.columns:
            df.loc[df["pe_ratio"] > 0, "rfscore7"] += 1

        return df

    except Exception as e:
        logger.warn(f"计算 RFScore7 出错: {e}")
        return pd.DataFrame()


def calc_market_state(context):
    """计算市场状态"""
    try:
        idx_bars = history_bars("000300.XSHG", 20, "1d", "close", include_now=True)
        if idx_bars is None or len(idx_bars) < 20:
            return {"breadth": 0.5, "trend_on": True}

        idx_close = idx_bars[-1]
        idx_ma20 = np.mean(idx_bars)
        trend_on = idx_close > idx_ma20

        hs300 = index_components("000300.XSHG")[:50]
        above_count = 0
        total_count = 0

        for stock in hs300:
            try:
                bars = history_bars(stock, 20, "1d", "close", include_now=True)
                if bars is not None and len(bars) >= 20:
                    total_count += 1
                    if bars[-1] > np.mean(bars):
                        above_count += 1
            except:
                pass

        breadth = above_count / total_count if total_count > 0 else 0.5
        return {"breadth": breadth, "trend_on": trend_on}

    except:
        return {"breadth": 0.5, "trend_on": True}


def choose_stocks(context, hold_num):
    """选股逻辑"""
    stocks = get_universe(context)
    logger.info(f"股票池: {len(stocks)} 只")

    df = calc_rfscore7(context, stocks)
    if df.empty:
        return []

    # PB 过滤
    if "pb_ratio" in df.columns:
        pb_threshold = df["pb_ratio"].quantile(context.pb_pct)
        df = df[df["pb_ratio"] <= pb_threshold]
        logger.info(f"PB10% 筛选后: {len(df)} 只")

    # 排序选股
    df = df.sort_values("rfscore7", ascending=False)

    if "order_book_id" in df.columns:
        selected = df.head(hold_num)["order_book_id"].tolist()
    else:
        selected = df.head(hold_num).index.tolist()

    logger.info(f"选股: {len(selected)} 只")
    return selected


def rebalance(context, bar_dict):
    """调仓逻辑"""
    logger.info(f"=== 调仓: {context.now} ===")

    market_state = calc_market_state(context)
    logger.info(
        f"市场: breadth={market_state['breadth']:.3f}, trend={market_state['trend_on']}"
    )

    # 确定持股数
    if market_state["breadth"] < context.breadth_stop and not market_state["trend_on"]:
        target_hold_num = 0
        logger.info("空仓")
    elif (
        market_state["breadth"] < context.breadth_reduce
        and not market_state["trend_on"]
    ):
        target_hold_num = context.reduced_hold_num
        logger.info("减仓")
    else:
        target_hold_num = context.hold_num
        logger.info("正常仓位")

    # 选股
    target_stocks = (
        choose_stocks(context, target_hold_num) if target_hold_num > 0 else []
    )

    # 卖出
    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks:
            order_target_value(stock, 0)
            logger.info(f"卖出: {stock}")

    # 买入
    if target_stocks and context.portfolio.total_value > 0:
        target_value = context.portfolio.total_value / len(target_stocks)
        for stock in target_stocks:
            try:
                current_value = (
                    context.portfolio.positions[stock].market_value
                    if stock in context.portfolio.positions
                    else 0
                )
                if abs(target_value - current_value) > target_value * 0.1:
                    order_target_value(stock, target_value)
            except:
                pass

    logger.info(f"=== 调仓完成 ===")
