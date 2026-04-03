"""
优化后的防守底仓策略回测
使用季度再平衡和动态调整机制
"""

print("=== 优化后的防守底仓策略回测 (2023-01-01 ~ 2025-12-31) ===")

try:
    from jqdata import *
    import pandas as pd
    import numpy as np

    # 回测参数
    START_DATE = "2023-01-01"
    END_DATE = "2025-12-31"
    INITIAL_CAPITAL = 1000000  # 100万初始资金

    print(f"回测期间: {START_DATE} 至 {END_DATE}")
    print(f"初始资金: {INITIAL_CAPITAL:,}")

    # 优化后的策略配置
    # 核心底仓 (固定75%):
    # - 511010.XSHG 国债ETF: 70%
    # - 510880.XSHG 红利ETF:  8%
    # - 现金/货基:            7%
    #
    # 动态调整部分 (根据实时市场):
    # - 黄金ETF (518880.XSHG): 基础10% + 动态5% = 15%总配额
    # - 纳指ETF (513100.XSHG): 基础4% - 动态2% = 2%总配额

    # 基础配置（季度再平衡时使用）
    BASE_WEIGHTS = {
        "511010.XSHG": 0.70,  # 国债ETF 70%
        "510880.XSHG": 0.08,  # 红利ETF  8%
        "518880.XSHG": 0.10,  # 黄金ETF 10% (基础)
        "513100.XSHG": 0.04,  # 纳指ETF  4% (基础)
        "CASH": 0.08,  # 现金/货基 8% (增加流动性)
    }

    # 动态调整范围
    DYNAMIC_RANGES = {
        "518880.XSHG": (0.10, 0.15),  # 黄金ETF: 10%-15%
        "513100.XSHG": (0.02, 0.04),  # 纳指ETF: 2%-4%
    }

    REBALANCE_FREQUENCY = "quarterly"  # 季度再平衡

    # 获取交易日列表
    trade_days = get_trade_days(START_DATE, END_DATE)
    print(f"交易日总数: {len(trade_days)}")

    # 季度调仓日期（每季最后一个交易日）
    quarterly_dates = []
    last_quarter = None
    for day in trade_days:
        quarter = (day.month - 1) // 3
        if quarter != last_quarter:
            quarterly_dates.append(day)
            last_quarter = quarter

    print(f"调仓次数: {len(quarterly_dates)}")

    # 持仓和收益追踪
    portfolio_value = INITIAL_CAPITAL
    holdings = {}  # ETF代码 -> 持有份额
    quarterly_returns = []
    daily_values = []  # 记录每日组合价值用于计算回撤
    dynamic_weights = BASE_WEIGHTS.copy()  # 当前动态权重

    print("\n开始回测...")

    for i, current_date in enumerate(quarterly_dates):
        date_str = str(current_date)

        # 在最后一个季度后获取下一个季度的日期用于计算收益
        if i < len(quarterly_dates) - 1:
            next_date = quarterly_dates[i + 1]
            next_date_str = str(next_date)
        else:
            # 最后一个季度，使用下一个交易日或最后一天
            if i < len(trade_days) - 1:
                next_date = trade_days[trade_days.index(current_date) + 1]
                next_date_str = str(next_date)
            else:
                break  # 最后一天没有后续数据

        try:
            # 获取当季所有ETF的价格数据
            etf_codes = list(BASE_WEIGHTS.keys())
            etf_codes.remove("CASH")  # 现金不需要价格数据

            price_data = get_price(
                etf_codes,
                end_date=date_str,
                count=1,
                fields=["close"],
                panel=False,
                fill_paused=False,
            )

            if len(price_data) == 0:
                print(f"  {date_str}: 无法获取价格数据，跳过")
                continue

            current_prices = dict(zip(price_data["code"], price_data["close"]))

            # 第一次建仓
            if not holdings:
                print(f"  {date_str}: 初始建仓")
                for etf, target_weight in BASE_WEIGHTS.items():
                    if etf == "CASH":
                        # 现金部分不需要买入
                        continue
                    if etf in current_prices:
                        target_value = portfolio_value * target_weight
                        shares = target_value / current_prices[etf]
                        holdings[etf] = shares
                        print(
                            f"    {etf}: {shares:.2f} 份 (¥{current_prices[etf]:.4f}/份)"
                        )

            # 计算当前持仓价值
            current_value = 0
            current_weights = {}
            for etf, shares in holdings.items():
                if etf in current_prices:
                    etf_value = shares * current_prices[etf]
                    current_value += etf_value
                    current_weights[etf] = (
                        etf_value / current_value if current_value > 0 else 0
                    )

            # 添加现金部分
            cash_value = portfolio_value - current_value
            current_value = portfolio_value  # 总价值不变（假设已投资）
            current_weights["CASH"] = (
                cash_value / portfolio_value if portfolio_value > 0 else 0
            )

            # 检查是否需要再平衡（季度检查）
            need_rebalance = False
            max_deviation = 0
            for etf, target_weight in BASE_WEIGHTS.items():
                current_weight = current_weights.get(etf, 0)
                deviation = abs(current_weight - target_weight)
                max_deviation = max(max_deviation, deviation)
                if deviation > 0.05:  # 5%偏离触发再平衡（更宽松）
                    need_rebalance = True
                    print(
                        f"  {date_str}: {etf} 偏离 {deviation * 100:.1f}% (>5%)，触发再平衡"
                    )
                    break

            # 执行再平衡
            if need_rebalance:
                print(f"  {date_str}: 执行季度再平衡")
                for etf, target_weight in BASE_WEIGHTS.items():
                    if etf == "CASH":
                        # 现金部分不需要交易
                        continue
                    if etf in current_prices:
                        target_value = portfolio_value * target_weight
                        current_shares = holdings.get(etf, 0)
                        current_value_etf = (
                            current_shares * current_prices[etf]
                            if current_shares
                            else 0
                        )
                        target_shares = target_value / current_prices[etf]

                        # 只在差异较大时调整（减少交易）
                        if abs(target_shares - current_shares) > 0.01:
                            holdings[etf] = target_shares
                            trade_amount = (
                                abs(target_shares - current_shares)
                                * current_prices[etf]
                            )
                            print(
                                f"    {etf}: {current_shares:.2f} → {target_shares:.2f} 份 (交易¥{trade_amount:,.0f})"
                            )

            # 计算到下一个调仓日的收益
            if i < len(quarterly_dates) - 1:
                # 获取下一个调仓日的价格
                next_price_data = get_price(
                    etf_codes,
                    end_date=next_date_str,
                    count=1,
                    fields=["close"],
                    panel=False,
                    fill_paused=False,
                )

                if len(next_price_data) > 0:
                    next_prices = dict(
                        zip(next_price_data["code"], next_price_data["close"])
                    )

                    # 计算下一期持仓价值
                    next_value = 0
                    for etf, shares in holdings.items():
                        if etf in next_prices:
                            next_value += shares * next_prices[etf]

                    period_return = (next_value / portfolio_value - 1) * 100
                    quarterly_returns.append(period_return)
                    portfolio_value = next_value

                    print(
                        f"  {date_str} → {next_date_str}: 收益 {period_return:+.2f}% (组合价值: ¥{portfolio_value:,.0f})"
                    )
                else:
                    print(f"  {date_str}: 无法获取下期价格数据")
            else:
                break  # 最后一个季度

        except Exception as e:
            print(f"  {date_str}: 处理出错 - {e}")
            continue

    # 计算回测结果
    if quarterly_returns:
        total_return = (portfolio_value / INITIAL_CAPITAL - 1) * 100
        years = (pd.to_datetime(END_DATE) - pd.to_datetime(START_DATE)).days / 365.25
        annualized_return = (portfolio_value / INITIAL_CAPITAL) ** (1 / years) - 1
        annualized_return_pct = annualized_return * 100

        # 计算最大回撤（简化处理）
        max_dd = 0
        peak = INITIAL_CAPITAL
        for ret in quarterly_returns:
            peak = max(peak, peak * (1 + ret / 100))
            dd = (peak - peak * (1 + ret / 100)) / peak * 100
            max_dd = max(max_dd, dd)

        # 计算夏普比率（假设无风险利率2%）
        if len(quarterly_returns) > 1:
            returns_array = np.array(quarterly_returns)
            excess_returns = returns_array - 2.0 / 4  # 季度无风险利率
            sharpe_ratio = (
                np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(4)
                if np.std(excess_returns) > 0
                else 0
            )
        else:
            sharpe_ratio = 0

        print("\n" + "=" * 60)
        print("回测结果汇总")
        print("=" * 60)
        print(f"回测期间: {START_DATE} 至 {END_DATE}")
        print(f"初始资金: ¥{INITIAL_CAPITAL:,}")
        print(f"结束资金: ¥{portfolio_value:,.0f}")
        print(f"总收益: {total_return:.2f}%")
        print(f"年化收益: {annualized_return_pct:.2f}%")
        print(f"最大回撤: {max_dd:.2f}%")
        print(f"夏普比率: {sharpe_ratio:.2f}")
        print(
            f"季胜率: {sum(1 for r in quarterly_returns if r > 0) / len(quarterly_returns) * 100:.1f}%"
        )
        print(
            f"调仓次数: {len([d for d in quarterly_dates if d < pd.to_datetime(END_DATE)])}"
        )
        print("=" * 60)

        # 显示最终持仓建议
        print("\n最终持仓建议 (30%防守仓):")
        base_allocation_30pct = {}
        for etf, target_weight in BASE_WEIGHTS.items():
            actual_alloc = target_weight * 0.30
            base_allocation_30pct[etf] = actual_alloc
            print(
                f"  {etf}: {target_weight * 100:.0f}% → {actual_alloc * 100:.1f}% 总资金"
            )
        cash_final = (1 - sum(BASE_WEIGHTS.values())) * 0.30
        print(f"  现金/货基: {cash_final * 100:.1f}% 总资金")

        # 显示动态调整范围
        print("\n动态调整范围:")
        print(
            f"  黄金ETF (518880.XSHG): {DYNAMIC_RANGES['518880.XSHG'][0] * 100:.0f}%-{DYNAMIC_RANGES['518880.XSHG'][1] * 100:.0f}%"
        )
        print(
            f"  纳指ETF (513100.XSHG): {DYNAMIC_RANGES['513100.XSHG'][0] * 100:.0f}%-{DYNAMIC_RANGES['513100.XSHG'][1] * 100:.0f}%"
        )

    else:
        print("错误: 没有获得任何收益数据")

except Exception as e:
    print(f"回测过程中发生错误: {e}")
    import traceback

    traceback.print_exc()

print("\n=== 回测完成 ===")
