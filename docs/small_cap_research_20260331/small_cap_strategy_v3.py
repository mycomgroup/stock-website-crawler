# 小市值策略 V3 - 借鉴研究成果的改进版
#
# 改进点：
# 1. 加入情绪开关（涨停家数>=30）
# 2. 加入停手机制（连亏3停3天）
# 3. 优化选股逻辑（借鉴二板思路）
# 4. 放宽市值范围

from jqdata import *
import numpy as np


def initialize(context):
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)

    # 策略参数
    g.stock_num = 10
    g.min_cap = 5  # 放宽到5亿
    g.max_cap = 200  # 缩小到200亿
    g.stop_loss = -0.09

    # 情绪开关参数
    g.emotion_threshold = 30  # 涨停家数>=30
    g.emotion_high = 50  # 高情绪阈值

    # 停手机制参数
    g.loss_count = 0  # 连续亏损计数
    g.pause_days = 0  # 剩余停手天数
    g.max_loss_count = 3  # 连亏3笔触发
    g.pause_duration = 3  # 停手3天

    # 交易记录
    g.trade_history = []

    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    set_slippage(FixedSlippage(0.02))

    run_daily(before_trading, "09:00")
    run_daily(after_trading, "15:00")
    run_daily(stop_loss_check, "14:30")
    run_weekly(rebalance, 1, "10:00")


def before_trading(context):
    """盘前检查"""
    # 更新停手状态
    if g.pause_days > 0:
        g.pause_days -= 1
        log.info("停手中，剩余%d天" % g.pause_days)

    # 计算情绪指标
    g.emotion_score = get_emotion_score(context)
    log.info("昨日涨停家数: %d, 情绪阈值: %d" % (g.emotion_score, g.emotion_threshold))


def after_trading(context):
    """盘后更新"""
    pass


def get_emotion_score(context):
    """计算情绪指标：涨停家数"""
    all_stocks = list(get_all_securities("stock", context.previous_date).index)

    # 过滤科创北交
    all_stocks = [
        s
        for s in all_stocks
        if not s.startswith("688") and not s.startswith("8") and not s.startswith("4")
    ]

    # 获取涨停股票
    current_data = get_current_data()
    zt_count = 0

    for stock in all_stocks[:500]:  # 限制数量避免超时
        if stock in current_data:
            bar = current_data[stock]
            if bar.high_limit and bar.last_price >= bar.high_limit * 0.995:
                zt_count += 1

    return zt_count


def stop_loss_check(context):
    """止损检查"""
    if g.pause_days > 0:
        return

    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.price < pos.avg_cost * (1 + g.stop_loss):
            order_target_value(stock, 0)
            log.info(
                "止损: %s, 亏损%.2f%%" % (stock, (pos.price / pos.avg_cost - 1) * 100)
            )


def record_trade_result(context, stock, pnl_pct):
    """记录交易结果并更新停手状态"""
    g.trade_history.append({"stock": stock, "pnl": pnl_pct})

    # 更新连亏计数
    if pnl_pct < 0:
        g.loss_count += 1
        log.info("亏损: %s, %.2f%%, 连亏%d笔" % (stock, pnl_pct, g.loss_count))
    else:
        g.loss_count = 0
        log.info("盈利: %s, %.2f%%" % (stock, pnl_pct))

    # 触发停手
    if g.loss_count >= g.max_loss_count and g.pause_days == 0:
        g.pause_days = g.pause_duration
        log.info("触发停手：连亏%d笔，停手%d天" % (g.loss_count, g.pause_days))


def rebalance(context):
    """调仓"""
    today = context.current_dt

    # 检查停手状态
    if g.pause_days > 0:
        log.info("停手中，跳过交易")
        return

    # 检查情绪开关
    if g.emotion_score < g.emotion_threshold:
        log.info("情绪不足(涨停%d<%d)，观望" % (g.emotion_score, g.emotion_threshold))
        # 持有货币ETF
        if len(context.portfolio.positions) == 0:
            order_target_value("511880.XSHG", context.portfolio.total_value)
        return

    # 获取股票池
    stocks = get_stock_pool(context)

    if len(stocks) == 0:
        log.info("无符合条件的股票")
        return

    # 选股
    selected = select_stocks(context, stocks, g.stock_num)

    # 记录卖出
    for stock in list(context.portfolio.positions.keys()):
        if stock not in selected and stock != "511880.XSHG":
            pos = context.portfolio.positions[stock]
            pnl = (pos.price / pos.avg_cost - 1) * 100
            record_trade_result(context, stock, pnl)
            order_target_value(stock, 0)

    # 买入
    if len(selected) > 0:
        value = context.portfolio.total_value / len(selected)
        for stock in selected:
            order_target_value(stock, value)
        log.info("买入: %s" % selected[:5])


def get_stock_pool(context):
    """获取股票池 - 加入更多筛选条件"""
    # 获取全A股票
    scu = get_index_stocks("000001.XSHG") + get_index_stocks("399106.XSHE")

    # 过滤ST、停牌
    current_data = get_current_data()
    scu = [
        s
        for s in scu
        if not (
            current_data[s].paused
            or current_data[s].is_st
            or "ST" in current_data[s].name
            or "*" in current_data[s].name
            or "退" in current_data[s].name
        )
    ]

    # 过滤次新股（上市满1年）
    scu = [
        s
        for s in scu
        if (context.previous_date - get_security_info(s).start_date).days > 365
    ]

    # 过滤涨跌停
    scu = [
        s
        for s in scu
        if current_data[s].last_price < current_data[s].high_limit * 0.98
        and current_data[s].last_price > current_data[s].low_limit * 1.02
    ]

    # 市值+财务筛选
    q = (
        query(
            valuation.code,
            valuation.market_cap,
            valuation.turnover_ratio,
            indicator.roe,
        )
        .filter(
            valuation.code.in_(scu),
            valuation.market_cap.between(g.min_cap, g.max_cap),
            income.net_profit > 0,
            income.operating_revenue > 1e8,
            valuation.turnover_ratio > 2,  # 换手率>2%
            indicator.roe > 5,  # ROE>5%
        )
        .order_by(valuation.market_cap.asc())
    )

    df = get_fundamentals(q, date=context.previous_date)
    return list(df["code"]) if df is not None and len(df) > 0 else []


def select_stocks(context, stocks, num):
    """选股 - 多因子评分"""
    results = []

    for stock in stocks[: min(80, len(stocks))]:
        try:
            # 获取历史数据
            h = history(60, unit="1d", field="close", security_list=[stock], df=True)

            if h is None or len(h) < 40:
                continue

            close = h[stock].values

            # 因子计算
            momentum = (close[-1] / close[-21] - 1) * 100 if len(close) >= 21 else 0
            ma20 = np.mean(close[-20:])
            ma_dev = (close[-1] / ma20 - 1) * 100

            # 价格位置
            high20 = np.max(close[-20:])
            low20 = np.min(close[-20:])
            price_pos = (
                (close[-1] - low20) / (high20 - low20) if high20 != low20 else 0.5
            )

            # 评分系统（借鉴二板策略思路）
            score = 0

            # 动量因子（不要太强也不要太弱）
            if 5 < momentum < 20:
                score += 3
            elif 0 < momentum < 5:
                score += 2
            elif -10 < momentum < 0:
                score += 1
            elif momentum > 30:
                score -= 2  # 追高风险

            # MA乖离率
            if -5 < ma_dev < 5:
                score += 2
            elif -10 < ma_dev < 10:
                score += 1
            elif ma_dev > 15:
                score -= 2  # 偏离过大风险

            # 价格位置（中等位置更好）
            if 0.3 < price_pos < 0.6:
                score += 2
            elif 0.6 < price_pos < 0.8:
                score += 1
            elif price_pos > 0.9:
                score -= 2  # 接近新高风险

            results.append({"code": stock, "score": score, "momentum": momentum})

        except Exception as e:
            continue

    # 按评分排序
    results.sort(key=lambda x: (-x["score"], -x["momentum"]))
    return [r["code"] for r in results[:num]]
