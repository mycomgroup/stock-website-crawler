"""
纯现金防守策略（对比基准）

策略配置:
- 100% 现金（不投资任何资产）
- 作为零风险的绝对基准

回测周期: 2022-01-01 到 2025-03-28
"""

from jqdata import *


# 初始化函数
def initialize(context):
    # 设定基准为国债ETF（仅作参考）
    set_benchmark("511010.XSHG")
    # 开启动态复权模式
    set_option("use_real_price", True)

    # 设置极低的成本（实际上不交易）
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0,
            open_commission=0,
            close_commission=0,
            min_commission=0,
        ),
        type="stock",
    )

    log.set_level("order", "error")

    # 每天记录状态
    run_daily(record_state, time="15:00")


# 记录状态
def record_state(context):
    total_value = context.portfolio.total_value
    cash = context.portfolio.available_cash
    log.info(
        f"总资金: {total_value:.2f}, 现金: {cash:.2f}, 收益率: {(total_value / 1000000 - 1) * 100:.2f}%"
    )

    # 现金策略不产生任何收益，始终保持100%现金
    # 这是为了对比其他防守策略的机会成本
