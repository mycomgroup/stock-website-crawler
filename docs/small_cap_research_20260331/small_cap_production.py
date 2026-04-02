"""
小市值策略 - 完整可运行版
包含：情绪开关 + 停手机制 + 不追涨停 + 小市值

运行方式：
1. 复制到JoinQuant策略编辑器
2. 设置回测参数：
   - 开始日期：2022-01-01
   - 结束日期：2024-12-31
   - 初始资金：100000
   - 频率：日线
"""

from jqdata import *
import numpy as np


def initialize(context):
    """初始化策略"""
    set_benchmark("000905.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)

    # 策略参数
    g.stock_num = 10
    g.min_cap = 5
    g.max_cap = 200
    g.stop_loss = -0.09

    # 情绪开关参数
    g.emotion_threshold = 30  # 涨停家数>=30才开仓

    # 停手机制参数
    g.loss_count = 0
    g.pause_days = 0
    g.max_loss_count = 3
    g.pause_duration = 3

    # 交易费用
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

    # 每日止损检查
    run_daily(stop_loss_check, "14:30")

    # 每周调仓
    run_weekly(rebalance, 1, "10:00")


def stop_loss_check(context):
    """止损检查"""
    if g.pause_days > 0:
        return

    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.price < pos.avg_cost * (1 + g.stop_loss):
            order_target_value(stock, 0)

            # 记录亏损
            g.loss_count += 1
            if g.loss_count >= g.max_loss_count and g.pause_days == 0:
                g.pause_days = g.pause_duration
                log.info("触发停手：连亏%d笔，停手%d天" % (g.loss_count, g.pause_days))


def get_emotion_score(context):
    """
    计算情绪指标：涨停家数
    使用昨日数据
    """
    try:
        # 获取所有股票
        all_stocks = list(get_all_securities("stock", context.previous_date).index)

        # 过滤科创北交
        all_stocks = [
            s
            for s in all_stocks
            if not s.startswith("688")
            and not s.startswith("8")
            and not s.startswith("4")
        ]

        # 采样计算
        sample_stocks = all_stocks[:300]

        # 获取昨日数据
        df_price = get_price(
            sample_stocks,
            end_date=context.previous_date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )

        zt_count = 0
        for s in sample_stocks:
            try:
                if s in df_price.index:
                    close = df_price.loc[s, "close"]
                    high_limit = df_price.loc[s, "high_limit"]

                    if close and high_limit and close >= high_limit * 0.99:
                        zt_count += 1
            except:
                continue

        # 估算全市场
        zt_total = int(zt_count * len(all_stocks) / len(sample_stocks))

        return zt_total

    except Exception as e:
        log.error("情绪计算错误: %s" % e)
        return 100  # 出错时默认允许交易


def rebalance(context):
    """每周调仓"""

    # 1. 停手检查
    if g.pause_days > 0:
        g.pause_days -= 1
        log.info("停手中，剩余%d天" % g.pause_days)
        return

    # 2. 情绪检查
    emotion_score = get_emotion_score(context)
    log.info("昨日涨停家数: %d, 阈值: %d" % (emotion_score, g.emotion_threshold))

    if emotion_score < g.emotion_threshold:
        log.info("情绪不足，观望")
        return

    # 3. 获取股票池
    stocks = get_stock_pool(context)

    if len(stocks) == 0:
        log.info("无符合条件的股票")
        return

    log.info("候选股票: %d只" % len(stocks))

    # 4. 选股
    selected = select_stocks(context, stocks, g.stock_num)

    if len(selected) == 0:
        log.info("选股失败")
        return

    log.info("选中股票: %s" % selected)

    # 5. 调仓
    # 卖出
    for stock in list(context.portfolio.positions.keys()):
        if stock not in selected:
            pos = context.portfolio.positions[stock]
            pnl = (pos.price / pos.avg_cost - 1) if pos.avg_cost > 0 else 0

            # 更新连亏计数
            if pnl > 0:
                g.loss_count = 0
            else:
                g.loss_count += 1

            order_target_value(stock, 0)

    # 买入
    value = context.portfolio.total_value / len(selected)
    for stock in selected:
        order_target_value(stock, value)


def get_stock_pool(context):
    """获取股票池"""
    try:
        # 上证+深证成分股
        scu = get_index_stocks(
            "000001.XSHG", date=context.previous_date
        ) + get_index_stocks("399106.XSHE", date=context.previous_date)

        # 市值筛选
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

        if df is not None and len(df) > 0:
            return list(df["code"])
        else:
            return []

    except Exception as e:
        log.error("获取股票池错误: %s" % e)
        return []


def select_stocks(context, stocks, num):
    """多因子评分选股"""
    results = []

    for stock in stocks[:50]:  # 限制数量
        try:
            # 获取历史数据
            df_hist = get_price(
                stock,
                end_date=context.previous_date,
                count=40,
                fields=["close"],
                panel=False,
            )

            if df_hist is None or len(df_hist) < 21:
                continue

            close = df_hist["close"].values

            # 计算因子
            momentum = (close[-1] / close[-21] - 1) * 100
            ma20 = np.mean(close[-20:])
            ma_dev = (close[-1] / ma20 - 1) * 100

            # 价格位置
            high20 = np.max(close[-20:])
            low20 = np.min(close[-20:])
            price_pos = (
                (close[-1] - low20) / (high20 - low20) if high20 != low20 else 0.5
            )

            # 评分
            score = 0

            # 动量（适度为佳）
            if 5 < momentum < 20:
                score += 3
            elif 0 < momentum <= 5:
                score += 2
            elif -10 < momentum <= 0:
                score += 1

            # MA乖离
            if -5 < ma_dev < 5:
                score += 2
            elif -10 < ma_dev < 10:
                score += 1

            # 价格位置
            if 0.3 < price_pos < 0.6:
                score += 2
            elif 0.6 < price_pos < 0.8:
                score += 1

            results.append({"code": stock, "score": score, "momentum": momentum})

        except Exception as e:
            continue

    # 排序
    results.sort(key=lambda x: -x["score"])

    return [r["code"] for r in results[:num]]
