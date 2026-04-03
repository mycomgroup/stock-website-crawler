"""
小市值策略 V11 - 情绪开关修复版
修复：使用更可靠的情绪计算方式

运行方式：
1. 复制到JoinQuant策略编辑器
2. 回测参数：2022-01-01 至 2024-12-31，初始资金10万
"""

from jqdata import *


def initialize(context):
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)

    g.stock_num = 10
    g.min_cap = 5
    g.max_cap = 200
    g.stop_loss = -0.09

    # 情绪开关 - 降低阈值确保能交易
    g.emotion_threshold = 15

    # 停手机制
    g.loss_count = 0
    g.pause_days = 0

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

    run_daily(stop_loss_check, "14:30")
    run_weekly(rebalance, 1, "10:00")


def stop_loss_check(context):
    """止损 + 更新停手"""
    if g.pause_days > 0:
        g.pause_days -= 1
        log.info("停手中，剩余%d天" % g.pause_days)
        return

    for s in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[s]
        if pos.price < pos.avg_cost * (1 + g.stop_loss):
            order_target_value(s, 0)
            g.loss_count += 1
            if g.loss_count >= 3:
                g.pause_days = 3
                log.info("触发停手")


def get_emotion(context):
    """
    计算情绪指标
    使用简单方法：统计涨停股票数量
    """
    try:
        # 获取所有股票
        all_stocks = list(get_all_securities("stock", context.previous_date).index)

        # 过滤
        all_stocks = [
            s for s in all_stocks if not s.startswith("688") and not s.startswith("8")
        ]

        # 采样
        sample_size = min(500, len(all_stocks))
        sample = all_stocks[:sample_size]

        # 获取价格数据
        df = get_price(
            sample,
            end_date=context.previous_date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )

        zt_count = 0
        for s in sample:
            try:
                if s in df.index:
                    close = df.loc[s, "close"]
                    high_limit = df.loc[s, "high_limit"]
                    if close >= high_limit * 0.99:
                        zt_count += 1
            except:
                continue

        # 估算全市场
        estimated = int(zt_count * len(all_stocks) / sample_size)

        return estimated
    except Exception as e:
        log.error("情绪计算错误: %s" % e)
        return 100  # 出错时默认允许交易


def rebalance(context):
    """调仓"""
    # 停手检查
    if g.pause_days > 0:
        return

    # 情绪检查
    emotion = get_emotion(context)
    log.info("涨停数: %d, 阈值: %d" % (emotion, g.emotion_threshold))

    if emotion < g.emotion_threshold:
        log.info("情绪不足，观望")
        return

    # 获取股票池
    scu = get_index_stocks("000001.XSHG") + get_index_stocks("399106.XSHE")

    current = get_current_data()
    scu = [
        s
        for s in scu
        if not (
            current[s].paused
            or current[s].is_st
            or "ST" in current[s].name
            or "*" in current[s].name
        )
    ]

    q = (
        query(valuation.code, valuation.market_cap)
        .filter(
            valuation.code.in_(scu),
            valuation.market_cap.between(g.min_cap, g.max_cap),
            income.net_profit > 0,
        )
        .order_by(valuation.market_cap.asc())
    )

    df = get_fundamentals(q, date=context.previous_date)

    if df is None or len(df) == 0:
        return

    selected = list(df["code"])[: g.stock_num]
    log.info("选中: %s" % selected[:5])

    # 调仓
    for s in list(context.portfolio.positions.keys()):
        if s not in selected:
            pos = context.portfolio.positions[s]
            if pos.price > pos.avg_cost:
                g.loss_count = 0
            order_target_value(s, 0)

    value = context.portfolio.total_value / len(selected)
    for s in selected:
        order_target_value(s, value)
