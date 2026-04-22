# RiceQuant 策略编辑器版本 - ETF动量轮动
# 完整回测版本

from rqalpha import *
from rqalpha.apis import *
import numpy as np


def init(context):
    """策略初始化"""
    # ETF池
    context.etf_pool = [
        "510300.XSHG",  # 沪深300ETF
        "510500.XSHG",  # 中证500ETF
        "159915.XSHE",  # 创业板ETF
        "512100.XSHG",  # 中证1000ETF
        "510050.XSHG",  # 上证50ETF
    ]

    context.momentum_period = 20  # 动量周期
    context.top_n = 2  # 持仓ETF数量
    context.trade_count = 0

    set_benchmark("000300.XSHG")

    # ETF交易成本较低
    set_order_cost(
        OrderCost(
            open_commission=0.0001,  # ETF佣金较低
            close_commission=0.0001,
            close_tax=0.0,  # ETF无印花税
        ),
        type="stock",
    )

    set_slippage(FixedSlippage(0.001))

    # 每月调仓
    scheduler.run_monthly(rebalance, tradingday=1)


def rebalance(context, bar_dict):
    """每月调仓"""
    # 计算动量
    etf_momentum = []

    for etf in context.etf_pool:
        momentum = calculate_momentum(etf, context)
        if momentum is not None:
            etf_momentum.append((etf, momentum))
            logger.info(f"{etf} 动量: {momentum:.2f}%")

    if not etf_momentum:
        logger.warning("无法计算动量")
        return

    # 按动量排序
    etf_momentum.sort(key=lambda x: x[1], reverse=True)

    # 选择动量最强的ETF
    target_etfs = [etf for etf, _ in etf_momentum[: context.top_n]]

    logger.info(f"选中ETF: {target_etfs}")

    # 调整持仓
    adjust_positions(target_etfs, context, bar_dict)

    context.trade_count += 1


def calculate_momentum(etf, context):
    """计算动量"""
    try:
        # 获取历史价格
        prices = history_bars(etf, context.momentum_period + 1, "1d", "close")

        if prices is None or len(prices) < context.momentum_period + 1:
            return None

        # 计算动量: (最新价 / N天前价格 - 1) * 100
        momentum = (prices[-1] / prices[0] - 1) * 100

        return momentum

    except Exception as e:
        logger.error(f"计算 {etf} 动量错误: {e}")
        return None


def adjust_positions(target_etfs, context, bar_dict):
    """调整持仓"""
    current_positions = list(context.portfolio.positions.keys())

    # 卖出不在目标列表中的ETF
    for etf in current_positions:
        if etf not in target_etfs:
            order_target_percent(etf, 0)
            logger.info(f"卖出: {etf}")

    # 等权重买入目标ETF
    if target_etfs:
        weight = 1.0 / len(target_etfs)

        for etf in target_etfs:
            if etf not in current_positions:
                if etf in bar_dict and bar_dict[etf].is_trading:
                    order_target_percent(etf, weight)
                    logger.info(f"买入: {etf}, 权重: {weight:.2%}")


__config__ = {
    "base": {
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "frequency": "1d",
        "accounts": {"stock": 1000000},
    },
    "extra": {
        "log_level": "info",
    },
    "mod": {
        "sys_progress": {
            "enabled": True,
            "show": True,
        }
    },
}
