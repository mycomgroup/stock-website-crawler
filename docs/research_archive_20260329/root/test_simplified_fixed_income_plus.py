# 风险及免责提示：该策略由opencode基于分析创建，仅用于验证目的。
# 标题：简化版国债固收+ 防守底仓策略
# 作者：opencode

from jqdata import *
import numpy as np


# 初始化函数
def initialize(context):
    # 设定基准为国债ETF
    set_benchmark("511010.XSHG")
    # 开启动态复权模式(真实价格)
    set_option("use_real_price", True)
    # 设置手续费 - 基金交易
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0,
            open_commission=0.0002,
            close_commission=0.0002,
            close_today_commission=0,
            min_commission=5,
        ),
        type="fund",
    )
    # 关闭部分log
    log.set_level("order", "error")

    # 定义目标权重
    g.target_weights = {
        "511010.XSHG": 0.75,  # 国债ETF 75%
        "518880.XSHG": 0.10,  # 黄金ETF 10%
        "510880.XSHG": 0.08,  # 红利ETF 8%
        "513100.XSHG": 0.04,  # 纳指ETF 4%
        # 现金不需要交易，由持有不足的部分自动填补
    }

    # 调仓阈值
    g.rebalance_threshold = 0.15  # 15%偏离触发再平衡

    # 每天执行交易
    run_daily(trade, time="9:35")


# 交易函数
def trade(context):
    # 获取当前投资组合总价值
    total_value = context.portfolio.total_value

    # 获取当前持仓
    positions = context.portfolio.positions

    # 计算当前权重
    current_weights = {}
    for stock, weight in g.target_weights.items():
        if stock in positions:
            current_value = positions[stock].value
            current_weights[stock] = (
                current_value / total_value if total_value > 0 else 0
            )
        else:
            current_weights[stock] = 0

    # 检查是否需要再平衡（任意一只ETF偏离超过阈值）
    need_rebalance = False
    for stock, target_weight in g.target_weights.items():
        current_weight = current_weights.get(stock, 0)
        deviation = abs(current_weight - target_weight)
        if deviation > g.rebalance_threshold:
            need_rebalance = True
            break

    # 如果需要再平衡，则执行调仓
    if need_rebalance:
        log.info("触发再平衡: 持仓偏离超过15%")
        for stock, target_weight in g.target_weights.items():
            target_value = total_value * target_weight

            if stock in positions:
                current_value = positions[stock].value
                diff_value = target_value - current_value

                # 只在差值超过最小交易额时执行
                if abs(diff_value) > 1000:  # 最小交易1000元
                    if diff_value > 0:
                        # 需要买入
                        order_target_value(stock, target_value)
                    else:
                        # 需要卖出
                        order_target_value(stock, target_value)
            else:
                # 没有持仓，直接买入目标价值
                if target_value > 1000:  # 最小交易1000元
                    order_target_value(stock, target_value)


# 收盘后运行函数
def after_market_close(context):
    # 记录当前持仓情况用于分析
    positions = context.portfolio.positions
    total_value = context.portfolio.total_value

    log.info("=== 收盘持仓报告 ===")
    for stock, weight in g.target_weights.items():
        if stock in positions:
            current_value = positions[stock].value
            current_weight = current_value / total_value if total_value > 0 else 0
            log.info(
                f"{stock}: 目标权重{weight:.2%}, 实际权重{current_weight:.2%}, 持仓价值{current_value:.2f}"
            )
        else:
            log.info(f"{stock}: 目标权重{weight:.2%}, 实际权重0.00%, 未持有")

    # 记录现金比例
    cash_ratio = (
        context.portfolio.available_cash / total_value if total_value > 0 else 0
    )
    log.info(f"现金比例: {cash_ratio:.2%}")
    log.info("=====================")
