# ETF动量轮动策略 - RiceQuant 版本
# 基于动量的ETF轮动策略
# 测试日期: 2024-01-01 到 2024-12-31


def init(context):
    context.etf_list = [
        "510300.XSHG",  # 沪深300ETF
        "510500.XSHG",  # 中证500ETF
        "159915.XSHE",  # 创业板ETF
        "512100.XSHG",  # 中证1000ETF
        "510050.XSHG",  # 上证50ETF
    ]

    context.momentum_period = 20
    context.top_n = 2

    scheduler.run_monthly(rebalance, monthday=1)


def calc_momentum(etf, period):
    """计算动量"""
    bars = history_bars(etf, period + 1, "1d", "close")

    if bars is None or len(bars) < period + 1:
        return None

    return (bars[-1] / bars[0] - 1) * 100


def get_top_etfs(context):
    """获取动量最强的ETF"""
    momentum_scores = []

    for etf in context.etf_list:
        try:
            momentum = calc_momentum(etf, context.momentum_period)
            if momentum is not None:
                momentum_scores.append((etf, momentum))
                logger.info(f"{etf} 动量: {momentum:.2f}%")
        except Exception as e:
            logger.warning(f"计算 {etf} 动量失败: {e}")

    if not momentum_scores:
        logger.warning("无有效动量数据")
        return []

    momentum_scores.sort(key=lambda x: x[1], reverse=True)
    top_etfs = [etf for etf, _ in momentum_scores[: context.top_n]]

    logger.info(f"选中ETF: {top_etfs}")

    return top_etfs


def rebalance(context, bar_dict):
    """每月调仓"""
    target_etfs = get_top_etfs(context)

    if not target_etfs:
        logger.warning("无目标ETF")
        return

    current_positions = list(context.portfolio.positions.keys())

    for etf in current_positions:
        if etf not in target_etfs:
            order_target_value(etf, 0)
            logger.info(f"卖出ETF: {etf}")

    if target_etfs:
        value_per_etf = context.portfolio.total_value / len(target_etfs)

        for etf in target_etfs:
            if etf not in context.portfolio.positions:
                try:
                    order_target_value(etf, value_per_etf)
                    logger.info(f"买入ETF: {etf}, 金额: {value_per_etf:.0f}")
                except Exception as e:
                    logger.warning(f"买入 {etf} 失败: {e}")
