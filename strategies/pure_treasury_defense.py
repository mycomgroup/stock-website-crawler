"""
纯国债ETF防守策略（对比基准）

策略配置:
- 100% 511010.XSHG 国债ETF
- 作为最保守的防守基准

回测周期: 2022-01-01 到 2025-03-28
"""

from jqdata import *


# 初始化函数
def initialize(context):
    # 设定基准为国债ETF
    set_benchmark("511010.XSHG")
    # 开启动态复权模式
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

    # 每天检查一次
    run_daily(trade, time="9:35")


# 交易函数
def trade(context):
    # 满仓持有国债ETF
    target_stock = "511010.XSHG"

    # 如果当前没有满仓持有
    current_value = (
        context.portfolio.positions[target_stock].value
        if target_stock in context.portfolio.positions
        else 0
    )
    target_value = context.portfolio.total_value * 0.99  # 保留1%现金缓冲

    if current_value < target_value * 0.98:  # 仓位低于98%时调整
        order_target_value(target_stock, target_value)


# 收盘后记录
def after_market_close(context):
    log.info(
        f"持仓: 国债ETF = {context.portfolio.positions['511010.XSHG'].value:.2f}, "
        f"现金 = {context.portfolio.available_cash:.2f}"
    )
