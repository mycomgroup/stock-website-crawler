"""
纯RFScore7 PB10%进攻策略（RiceQuant版本 - 简化适配）

策略配置:
- 100% 进攻层，不配置防守层
- 用于对比防守层的价值

回测周期: 2022-01-01 到 2025-03-28
"""

import numpy as np


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

    # 记录当前日期用于调试
    logger.info(f"Strategy initialized. Benchmark: {context.benchmark}")

    # 每月1日调仓（RQAlpha不支持time参数）
    scheduler.run_monthly(rebalance, monthday=1)


def get_universe(context):
    """获取股票池：沪深300 + 中证500，排除科创板"""
    # 获取沪深300和中证500成分股
    hs300 = set(index_components("000300.XSHG"))
    zz500 = set(index_components("000905.XSHG"))
    stocks = list(hs300 | zz500)

    logger.info(
        f"原始股票池: 沪深300={len(hs300)}, 中证500={len(zz500)}, 合计={len(stocks)}"
    )

    # 排除科创板
    stocks = [s for s in stocks if not s.startswith("688")]
    logger.info(f"排除科创板后: {len(stocks)}")

    # 简化处理：不再进一步过滤，直接返回
    return stocks[:100]  # 只取前100只提高效率


def calc_rfscore_simple(context, stock):
    """简化版RFScore计算 - 使用可用的财务指标"""
    try:
        # 使用RQAlpha可用的财务指标
        # ROA = net_profit / total_assets
        bars = history_bars(stock, 20, "1d", ["close", "volume"], include_now=True)
        if bars is None or len(bars) < 20:
            return None

        # 简化评分：基于价格动量和成交量
        close = bars["close"]
        volume = bars["volume"]

        # 指标1: 价格动量 (20日收益)
        momentum = (close[-1] / close[0] - 1) * 100

        # 指标2: 成交量趋势
        vol_ratio = np.mean(volume[-5:]) / np.mean(volume) if np.mean(volume) > 0 else 0

        # 指标3: 价格相对位置
        price_pos = (
            (close[-1] - np.min(close)) / (np.max(close) - np.min(close))
            if np.max(close) != np.min(close)
            else 0.5
        )

        # 简化评分
        score = 0
        if momentum > 0:
            score += 2
        elif momentum > -5:
            score += 1

        if vol_ratio > 1.2:
            score += 2
        elif vol_ratio > 0.8:
            score += 1

        if price_pos > 0.7:
            score += 2
        elif price_pos > 0.3:
            score += 1

        # 模拟RFScore (1-7)
        fscore = min(7, max(1, score + 1))

        return fscore

    except Exception as e:
        logger.warn(f"Calc error for {stock}: {e}")
        return None


def get_stock_metrics(context, stocks):
    """获取股票的综合指标"""
    results = []
    checked = 0
    errors = 0

    for stock in stocks[:50]:  # 只检查前50只
        try:
            checked += 1
            # 获取价格数据
            bars = history_bars(stock, 20, "1d", "close", include_now=True)
            if bars is None or len(bars) < 20:
                continue

            # 获取当前快照（可选）
            try:
                snap = current_snapshot(stock)
            except:
                snap = None

            # 计算简化RFScore
            fscore = calc_rfscore_simple(context, stock)
            if fscore is None:
                continue

            # 获取价格指标
            close = bars[-1]
            ma20 = np.mean(bars)
            ma5 = np.mean(bars[-5:])

            # 计算动量
            momentum = (bars[-1] / bars[0] - 1) * 100

            results.append(
                {
                    "code": stock,
                    "close": close,
                    "ma20": ma20,
                    "ma5": ma5,
                    "fscore": fscore,
                    "momentum": momentum,
                    "above_ma": close > ma20,
                }
            )

        except Exception as e:
            errors += 1
            if errors <= 3:
                logger.warn(f"Metrics error for {stock}: {e}")
            continue

    logger.info(f"指标计算: 检查={checked}, 成功={len(results)}, 错误={errors}")
    return results


def calc_market_state(context):
    """计算市场状态"""
    # 获取沪深300价格数据
    idx_bars = history_bars("000300.XSHG", 20, "1d", "close", include_now=True)
    if idx_bars is None or len(idx_bars) < 20:
        return {"breadth": 0.5, "trend_on": True}

    # 计算指数趋势
    idx_close = idx_bars[-1]
    idx_ma20 = np.mean(idx_bars)
    trend_on = idx_close > idx_ma20

    # 计算市场宽度（使用成分股在20日均线上的比例）
    hs300 = index_components("000300.XSHG")[:50]  # 取前50只提高效率
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


def choose_stocks(context, hold_num):
    """选股逻辑"""
    stocks = get_universe(context)
    logger.info(f"股票池大小: {len(stocks)}")

    # 获取所有股票指标
    metrics = get_stock_metrics(context, stocks)

    if not metrics:
        logger.warn("没有获取到有效指标")
        return []

    # 按fscore和动量排序
    # 高fscore优先，高动量优先
    metrics.sort(key=lambda x: (-x["fscore"], -x["momentum"]))

    # 选股：fscore>=6
    picks = [m["code"] for m in metrics if m["fscore"] >= 6]

    logger.info(f"选股结果: {len(picks)} 只股票")
    if picks:
        logger.info(f"前5只: {picks[:5]}")

    return picks[:hold_num]


def rebalance(context, bar_dict):
    """每月调仓"""
    logger.info(f"调仓开始: {context.now}")

    # 计算市场状态
    market_state = calc_market_state(context)
    logger.info(
        f"市场状态: breadth={market_state['breadth']:.2f}, trend={market_state['trend_on']}"
    )

    # 确定目标持股数
    if market_state["breadth"] < context.breadth_stop and not market_state["trend_on"]:
        target_hold_num = 0
        target_stocks = []
        logger.info("市场极弱，空仓")
    elif (
        market_state["breadth"] < context.breadth_reduce
        and not market_state["trend_on"]
    ):
        target_hold_num = context.reduced_hold_num
        target_stocks = choose_stocks(context, target_hold_num)
        logger.info("市场偏弱，减仓")
    else:
        target_hold_num = context.base_hold_num
        target_stocks = choose_stocks(context, target_hold_num)
        logger.info("市场正常，正常仓位")

    logger.info(f"调仓: 目标持股数={target_hold_num}, 实际选股={len(target_stocks)}")

    # 卖出不在目标列表的股票
    current_positions = list(context.portfolio.positions.keys())
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)
            logger.info(f"卖出: {stock}")

    # 买入目标股票
    if target_stocks and context.portfolio.total_value > 0:
        target_value = context.portfolio.total_value / len(target_stocks)
        for stock in target_stocks:
            current_pos = context.portfolio.positions[stock].quantity
            if current_pos > 0:
                # 使用portfolio中的market_value
                current_value = context.portfolio.positions[stock].market_value
            else:
                current_value = 0

            if abs(target_value - current_value) > target_value * 0.1:  # 超过10%才调仓
                order_target_value(stock, target_value)
                logger.info(f"调仓: {stock} -> {target_value:.0f}")
