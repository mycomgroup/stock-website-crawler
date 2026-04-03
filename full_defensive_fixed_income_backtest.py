print("=== 防守底仓策略完整回测 (2023-01-01 ~ 2025-12-31) ===")

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

    # 策略配置 - 我们优化后的防守底仓
    TARGET_WEIGHTS = {
        "511010.XSHG": 0.75,  # 国债ETF 75%
        "518880.XSHG": 0.10,  # 黄金ETF 10%
        "510880.XSHG": 0.08,  # 红利ETF 8%
        "513100.XSHG": 0.04,  # 纳指ETF 4%
    }

    REBALANCE_THRESHOLD = 0.15  # 15%偏离触发再平衡

    # 获取交易日列表
    trade_days = get_trade_days(START_DATE, END_DATE)
    print(f"交易日总数: {len(trade_days)}")

    # 月度调仓日期（每月第一个交易日）
    monthly_dates = []
    last_month = None
    for day in trade_days:
        if day.month != last_month:
            monthly_dates.append(day)
            last_month = day.month

    print(f"调仓次数: {len(monthly_dates)}")

    # 持仓和收益追踪
    portfolio_value = INITIAL_CAPITAL
    holdings = {}  # ETF代码 -> 持有份额
    monthly_returns = []
    daily_values = []  # 记录每日组合价值用于计算回撤

    print("\n开始回测...")

    for i, current_date in enumerate(monthly_dates):
        date_str = str(current_date)

        # 在最后一个月后获取下一个月的日期用于计算收益
        if i < len(monthly_dates) - 1:
            next_date = monthly_dates[i + 1]
            next_date_str = str(next_date)
        else:
            # 最后一个月，使用下一个交易日或最后一天
            if i < len(trade_days) - 1:
                next_date = trade_days[trade_days.index(current_date) + 1]
                next_date_str = str(next_date)
            else:
                break  # 最后一天没有后续数据

        try:
            # 获取当月所有ETF的价格数据
            etf_codes = list(TARGET_WEIGHTS.keys())
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
                for etf, target_weight in TARGET_WEIGHTS.items():
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

            # 检查是否需要再平衡
            need_rebalance = False
            for etf, target_weight in TARGET_WEIGHTS.items():
                current_weight = current_weights.get(etf, 0)
                deviation = abs(current_weight - target_weight)
                if deviation > REBALANCE_THRESHOLD:
                    need_rebalance = True
                    print(
                        f"  {date_str}: {etf} 偏离 {deviation * 100:.1f}% (>15%)，触发再平衡"
                    )
                    break

            # 执行再平衡
            if need_rebalance:
                print(f"  {date_str}: 执行再平衡")
                for etf, target_weight in TARGET_WEIGHTS.items():
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
            if i < len(monthly_dates) - 1:
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
                    monthly_returns.append(period_return)
                    portfolio_value = next_value

                    print(
                        f"  {date_str} → {next_date_str}: 收益 {period_return:+.2f}% (组合价值: ¥{portfolio_value:,.0f})"
                    )
                else:
                    print(f"  {date_str}: 无法获取下期价格数据")
            else:
                break  # 最后一个月

        except Exception as e:
            print(f"  {date_str}: 处理出错 - {e}")
            continue

    # 计算回测结果
    if monthly_returns:
        total_return = (portfolio_value / INITIAL_CAPITAL - 1) * 100
        years = (pd.to_datetime(END_DATE) - pd.to_datetime(START_DATE)).days / 365.25
        annualized_return = (portfolio_value / INITIAL_CAPITAL) ** (1 / years) - 1
        annualized_return_pct = annualized_return * 100

        # 计算最大回撤
        # 这里简化处理，实际应该追踪每日净值
        max_dd = 0
        peak = INITIAL_CAPITAL
        for ret in monthly_returns:
            peak = max(peak, peak * (1 + ret / 100))
            dd = (peak - peak * (1 + ret / 100)) / peak * 100
            max_dd = max(max_dd, dd)

        # 计算夏普比率（假设无风险利率2%）
        if len(monthly_returns) > 1:
            returns_array = np.array(monthly_returns)
            excess_returns = returns_array - 2.0 / 12  # 月度无风险利率
            sharpe_ratio = (
                np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(12)
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
            f"月胜率: {sum(1 for r in monthly_returns if r > 0) / len(monthly_returns) * 100:.1f}%"
        )
        print(
            f"调仓次数: {len([d for d in monthly_dates if d < pd.to_datetime(END_DATE)])}"
        )
        print("=" * 60)

        # 显示最终持仓建议
        print("\n最终持仓建议 (30%防守仓):")
        for etf, target_weight in TARGET_WEIGHTS.items():
            actual_alloc = target_weight * 0.30
            print(
                f"  {etf}: {target_weight * 100:.0f}% → {actual_alloc * 100:.1f}% 总资金"
            )
        cash_final = (1 - sum(TARGET_WEIGHTS.values())) * 0.30
        print(f"  现金/货基: {cash_final * 100:.1f}% 总资金")

    else:
        print("错误: 没有获得任何收益数据")

except Exception as e:
    print(f"回测过程中发生错误: {e}")
    import traceback

    traceback.print_exc()

print("\n=== 回测完成 ===")
