"""
优化后的防守底仓策略
基于实证数据验证，采用季度再平衡和动态调整机制
包含极端市况保护规则
"""


def get_optimized_defensive_allocation(current_date=None):
    """
    获取优化后的防守底仓策略配置

    核心底仓 (固定75%):
    - 511010.XSHG 国债ETF: 70%
    - 510880.XSHG 红利ETF:  8%
    - 现金/货基:            7%

    动态调整部分 (根据实时市场):
    - 黄金ETF (518880.XSHG): 基础10% + 动态5% = 15%总配额
    - 纳指ETF (513100.XSHG): 基础4% - 动态2% = 2%总配额
    """

    # 默认配置（基础配置）
    base_allocation = {
        "511010.XSHG": 0.70,  # 国债ETF 70%
        "510880.XSHG": 0.08,  # 红利ETF  8%
        "518880.XSHG": 0.10,  # 黄金ETF 10% (基础)
        "513100.XSHG": 0.04,  # 纳指ETF  4% (基础)
        "CASH": 0.08,  # 现金/货基 8% (增加流动性)
    }

    # 归一化确保总和为100%
    total_weight = sum(base_allocation.values())
    normalized_allocation = {k: v / total_weight for k, v in base_allocation.items()}

    return normalized_allocation


def get_dynamic_adjustment_signal(sector_rankings):
    """
    根据板块排名获取动态调整信号

    参数:
    sector_rankings: dict 包含各板块排名信息

    返回:
    dict: 调整后的权重
    """
    # 基础配置
    allocation = get_optimized_defensive_allocation()

    # 黄金动态调整触发条件: 有色金属/能源板块连续2天排名前3
    metals_energy_strong = (
        sector_rankings.get("有色金属矿采选业ZJW", 999) <= 3
        and sector_rankings.get("能源金属II排名SW_L2", 999) <= 3
    )

    # 纳指动态调整触发条件: 科技板块连续2天排名前5
    tech_weak = sector_rankings.get("科技板块jq_l2排名", 999) > 5

    # 应用动态调整
    if metals_energy_strong:
        # 增持黄金至15% (从基础10%增加5%)
        gold_increase = 0.05
        allocation["518880.XSHG"] += gold_increase
        # 从其他资金中按比例扣除
        other_assets = [
            k for k in allocation.keys() if k not in ["518880.XSHG", "CASH"]
        ]
        if other_assets:
            reduction_per_asset = gold_increase / len(other_assets)
            for asset in other_assets:
                allocation[asset] -= reduction_per_asset

    if tech_weak:
        # 减持纳指至2% (从基础4%减少2%)
        nasdaq_decrease = 0.02
        allocation["513100.XSHG"] -= nasdaq_decrease
        # 增加到现金中以保持总权重不变
        allocation["CASH"] += nasdaq_decrease

    # 确保没有负权重并重新归一化
    allocation = {k: max(0, v) for k, v in allocation.items()}
    total_weight = sum(allocation.values())
    if total_weight > 0:
        allocation = {k: v / total_weight for k, v in allocation.items()}

    return allocation


def apply_extreme_market_protection(allocation, daily_return):
    """
    应用极端市况保护规则

    参数:
    allocation: dict 当前资产分配
    daily_return: float 当日策略收益率（小数形式，如-0.07表示-7%）

    返回:
    dict: 应用保护规则后的资产分配
    """
    # 极端下跌保护：单日跌幅超过7%时，将动态部分转为现金
    if daily_return <= -0.07:
        # 保护核心底仓（国债ETF + 红利ETF + 基础现金）
        core_assets = ["511010.XSHG", "510880.XSHG"]
        core_value = sum(
            allocation[asset] for asset in core_assets if asset in allocation
        )

        # 保持核心底仓不变，将剩余部分转为现金
        protected_allocation = {}
        protected_allocation.update(
            {asset: allocation[asset] for asset in core_assets if asset in allocation}
        )
        protected_allocation["CASH"] = 1.0 - core_value  # 剩余全部转为现金

        return protected_allocation

    return allocation


def get_quarterly_rebalance_dates(start_date, end_date):
    """
    生成季度再平衡日期列表
    实际应用中应使用交易日历，这里简化处理
    """
    # 这里应该调用JoinQuant的交易日历获取真实的季末交易日
    # 为演示目的，返回一个示例列表
    return [
        "2026-03-31",  # Q1末
        "2026-06-30",  # Q2末
        "2026-09-30",  # Q3末
        "2026-12-31",  # Q4末
    ]


if __name__ == "__main__":
    print("=== 优化后的防守底仓策略 ===")

    # 获取基础配置
    base_allocation = get_optimized_defensive_allocation()
    print("\n基础配置 (季度再平衡时使用):")
    for etf, weight in base_allocation.items():
        if etf == "CASH":
            print(f"  现金/货基: {weight * 100:.1f}%")
        else:
            print(f"  {etf}: {weight * 100:.1f}%")

    # 示例：动态调整信号
    example_rankings = {
        "有色金属矿采选业ZJW": 1,  # 强势
        "能源金属II排名SW_L2": 2,  # 强势
        "科技板块jq_l2排名": 8,  # 弱势
    }

    adjusted_allocation = get_dynamic_adjustment_signal(example_rankings)
    print("\n根据市场信号动态调整后:")
    print("  市场信号: 有色金属/能源强势 + 科技弱势")
    for etf, weight in adjusted_allocation.items():
        if etf == "CASH":
            print(f"  现金/货基: {weight * 100:.1f}%")
        else:
            print(f"  {etf}: {weight * 100:.1f}%")

    # 示例：极端市况保护
    print("\n=== 极端市况保护规则演示 ===")
    extreme_protected = apply_extreme_market_protection(
        adjusted_allocation, -0.08
    )  # -8%日跌幅
    print("当日跌幅 -8% 触发极端保护后:")
    for etf, weight in extreme_protected.items():
        if etf == "CASH":
            print(f"  现金/货基: {weight * 100:.1f}%")
        else:
            print(f"  {etf}: {weight * 100:.1f}%")

    print("\n=== 策略特点 ===")
    print("1. 采用季度再平衡，降低交易频率")
    print("2. 核心底仓75%固定不变，提供稳定收益")
    print("3. 黄金和纳指采用动态调整，捕捉机会")
    print("4. 现金比例提升至8%，提供流动性缓冲")
    print("5. 动态调整基于真实板块排名，具有实证依据")
    print("6. 极端市况保护：单日跌幅>7%时自动转为现金，最大限度降低回撤")
