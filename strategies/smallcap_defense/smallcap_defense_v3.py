"""
小市值防守线v3 - 稳健改进版
基于v1成功经验，仅添加止损机制

核心改进：
1. 完全复制v1参数（证明有效）
2. 添加个股止损机制（15%）
3. 添加组合止损机制（20%）
4. 删除所有复杂优化（状态过滤、仓位动态等）

设计原则：单一变量，保守渐进
"""

from jqdata import *
import pandas as pd
import numpy as np


def initialize(context):
    """初始化函数"""
    set_benchmark("000852.XSHG")  # 中证1000
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("order", "error")

    # 交易成本设置
    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    # ===== v1基础参数（完全不变）=====
    g.hold_num = 15  # 持仓数量
    g.min_cap = 15  # 最小市值（亿）
    g.max_cap = 60  # 最大市值（亿）
    g.ipo_days = 180  # 上市天数过滤
    g.max_pb = 1.5  # PB上限
    g.max_pe = 20  # PE上限

    # ===== v3新增：止损机制 =====
    g.stop_loss_individual = -0.15  # 个股止损：回撤15%
    g.stop_loss_portfolio = -0.20  # 组合止损：回撤20%
    g.initial_portfolio_value = None  # 初始资金（用于计算组合回撤）
    g.max_portfolio_value = None  # 历史最高净值

    # ===== v3删除：v2的所有复杂优化 =====
    # g.min_roe = 6             # ❌ 删除：ROE门槛
    # g.zt_pause_threshold = 30 # ❌ 删除：涨停停手机制
    # g.position_dynamic = ...  # ❌ 删除：仓位动态调整

    # 月度调仓
    run_monthly(rebalance, 1, time="9:35", reference_security="000852.XSHG")

    # 每日止损检查
    run_daily(check_stop_loss, time="14:30")


def get_smallcap_universe(watch_date):
    """
    获取小市值股票池
    完全复制v1逻辑
    """
    # 获取所有股票
    all_stocks = get_all_securities(types=["stock"], date=watch_date)

    # 过滤次新股
    all_stocks = all_stocks[
        all_stocks["start_date"] <= watch_date - pd.Timedelta(days=g.ipo_days)
    ]
    stocks = all_stocks.index.tolist()

    # 过滤ST股票
    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    # 过滤停牌股票
    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    # 过滤科创板（688开头）
    stocks = [s for s in stocks if not s.startswith("688")]

    # 市值筛选
    q = query(valuation.code, valuation.market_cap).filter(
        valuation.code.in_(stocks),
        valuation.market_cap >= g.min_cap,
        valuation.market_cap <= g.max_cap,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    # 取市值最小的30%（小市值因子）
    df["cap_rank"] = df["market_cap"].rank(pct=True)
    small_stocks = df[df["cap_rank"] <= 0.3]["code"].tolist()

    return small_stocks


def select_stocks(watch_date, hold_num):
    """
    选股逻辑
    完全复制v1：低估值筛选（PB<1.5, PE<20）
    """
    stocks = get_smallcap_universe(watch_date)
    if len(stocks) < 5:
        return []

    # 查询财务数据
    q = query(
        valuation.code,
        valuation.market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
        indicator.roe,
    ).filter(
        valuation.code.in_(stocks),
        valuation.pe_ratio > 0,
        valuation.pe_ratio < g.max_pe,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < g.max_pb,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    # 数据清洗
    df = df.drop_duplicates("code")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    if len(df) == 0:
        return []

    # 价值评分：PB和PE的综合排名
    df["pb_rank"] = df["pb_ratio"].rank(pct=True)
    df["pe_rank"] = df["pe_ratio"].rank(pct=True)
    df["value_score"] = (df["pb_rank"] + df["pe_rank"]) / 2

    # 按价值评分排序，选择最低估的股票
    df = df.sort_values("value_score", ascending=True)

    return df["code"].tolist()[:hold_num]


def filter_buyable(context, stocks):
    """
    过滤可买入的股票
    排除停牌、ST、涨停的股票
    """
    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if stock not in current_data:
            continue
        if current_data[stock].paused or current_data[stock].is_st:
            continue
        if "ST" in current_data[stock].name or "*" in current_data[stock].name:
            continue
        # 排除涨停（无法买入）
        last_price = current_data[stock].last_price
        if last_price >= current_data[stock].high_limit * 0.995:
            continue
        buyable.append(stock)
    return buyable


def check_stop_loss(context):
    """
    v3核心改进：止损机制
    1. 个股止损：回撤>15%清仓
    2. 组合止损：回撤>20%清仓
    """
    # 记录初始资金和历史最高净值
    if g.initial_portfolio_value is None:
        g.initial_portfolio_value = context.portfolio.starting_cash

    current_value = context.portfolio.total_value
    if g.max_portfolio_value is None or current_value > g.max_portfolio_value:
        g.max_portfolio_value = current_value

    # ===== 1. 个股止损检查 =====
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.avg_cost > 0:
            pnl = (pos.price - pos.avg_cost) / pos.avg_cost

            # 个股回撤>15%，止损清仓
            if pnl < g.stop_loss_individual:
                order_target_value(stock, 0)
                log.info(f"个股止损: {stock}, 亏损: {pnl:.2%}")

    # ===== 2. 组合止损检查 =====
    portfolio_drawdown = (current_value - g.max_portfolio_value) / g.max_portfolio_value

    # 组合回撤>20%，清仓所有股票
    if portfolio_drawdown < g.stop_loss_portfolio:
        log.info(f"组合止损触发: 当前回撤 {portfolio_drawdown:.2%}, 清仓所有持仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)


def rebalance(context):
    """
    月度调仓逻辑
    完全复制v1，仅在盘中有止损检查
    """
    watch_date = context.previous_date

    # 1. 选股
    stocks = select_stocks(watch_date, g.hold_num)
    stocks = filter_buyable(context, stocks)

    if len(stocks) == 0:
        log.info("无符合条件的股票，跳过调仓")
        return

    # 2. 计算目标仓位
    total_value = context.portfolio.total_value
    target_value_per_stock = total_value / len(stocks)

    # 3. 卖出不在目标列表的股票
    current_positions = context.portfolio.positions
    for stock in list(current_positions.keys()):
        if stock not in stocks:
            order_target_value(stock, 0)

    # 4. 买入目标股票
    for stock in stocks:
        order_target_value(stock, target_value_per_stock)

    log.info(
        f"小市值防守线v3: 买入{len(stocks)}只股票, 每只{target_value_per_stock / 10000:.1f}万元"
    )


def after_trading_end(context):
    """
    盘后记录
    """
    # 记录当前净值
    current_value = context.portfolio.total_value
    log.info(f"收盘净值: {current_value / 10000:.2f}万元")
