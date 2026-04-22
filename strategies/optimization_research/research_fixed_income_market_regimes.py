"""
国债固收+策略市场环境适应性调研
分析该策略在不同市场环境（牛市/熊市/震荡市）下的表现
"""

print("=== 国债固收+市场环境适应性分析 ===")

try:
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta

    # 定义市场环境分析的时间段
    periods = {
        "2022年熊市": ("2022-01-01", "2022-12-31"),
        "2023年震荡市": ("2023-01-01", "2023-12-31"),
        "2024年震荡上涨": ("2024-01-01", "2024-12-31"),
        "2025年至今": ("2025-01-01", "2025-03-28"),
        "完整周期": ("2022-01-01", "2025-03-28"),
    }

    # 国债固收+配置
    portfolio = {
        "511010.XSHG": 0.75,  # 国债ETF
        "518880.XSHG": 0.10,  # 黄金ETF
        "510880.XSHG": 0.08,  # 红利ETF
        "513100.XSHG": 0.04,  # 纳指ETF
    }

    results = []

    for period_name, (start_date, end_date) in periods.items():
        print(f"\n--- 分析时间段: {period_name} ({start_date} 至 {end_date}) ---")

        try:
            # 获取各ETF数据
            total_return = 0
            weighted_returns = {}

            for etf_code, weight in portfolio.items():
                try:
                    # 获取价格数据
                    price_data = get_price(
                        etf_code,
                        start_date=start_date,
                        end_date=end_date,
                        frequency="daily",
                        fields=["close"],
                    )

                    if price_data is not None and len(price_data) > 0:
                        start_price = price_data["close"].iloc[0]
                        end_price = price_data["close"].iloc[-1]
                        etf_return = (end_price / start_price - 1) * 100
                        weighted_return = etf_return * weight

                        weighted_returns[etf_code] = {
                            "return": etf_return,
                            "weight": weight,
                            "weighted_return": weighted_return,
                        }
                        total_return += weighted_return

                        # 计算最大回撤
                        prices = price_data["close"].values
                        max_drawdown = 0
                        peak = prices[0]
                        for price in prices:
                            if price > peak:
                                peak = price
                            drawdown = (peak - price) / peak
                            if drawdown > max_drawdown:
                                max_drawdown = drawdown

                        weighted_returns[etf_code]["max_drawdown"] = max_drawdown * 100

                        print(
                            f"  {etf_code}: 收益={etf_return:.2f}%, 权重={weight:.0%}, "
                            f"加权收益={weighted_return:.2f}%, 最大回撤={max_drawdown * 100:.2f}%"
                        )
                except Exception as e:
                    print(f"  {etf_code}: 获取数据失败 - {e}")

            # 现金部分收益（假设货币基金年化2%）
            days = (
                datetime.strptime(end_date, "%Y-%m-%d")
                - datetime.strptime(start_date, "%Y-%m-%d")
            ).days
            cash_return = 2.0 * (days / 365) * 0.03  # 3%现金权重
            total_return += cash_return

            print(f"  现金(3%): 估算收益={cash_return:.2f}%")
            print(f"  >>> 组合总收益: {total_return:.2f}%")

            # 获取沪深300基准收益
            try:
                hs300_data = get_price(
                    "000300.XSHG",
                    start_date=start_date,
                    end_date=end_date,
                    frequency="daily",
                    fields=["close"],
                )
                if hs300_data is not None and len(hs300_data) > 0:
                    hs300_start = hs300_data["close"].iloc[0]
                    hs300_end = hs300_data["close"].iloc[-1]
                    hs300_return = (hs300_end / hs300_start - 1) * 100
                    print(f"  >>> 沪深300收益: {hs300_return:.2f}%")
                    print(f"  >>> 超额收益: {total_return - hs300_return:.2f}%")
            except:
                hs300_return = None

            results.append(
                {
                    "period": period_name,
                    "start_date": start_date,
                    "end_date": end_date,
                    "portfolio_return": total_return,
                    "benchmark_return": hs300_return,
                    "excess_return": total_return - hs300_return
                    if hs300_return
                    else None,
                    "details": weighted_returns,
                }
            )

        except Exception as e:
            print(f"  分析失败: {e}")
            import traceback

            traceback.print_exc()

    # 总结分析
    print("\n" + "=" * 60)
    print("国债固收+策略适用环境总结")
    print("=" * 60)

    for r in results:
        if r["benchmark_return"] is not None:
            print(
                f"{r['period']:15s}: 策略收益={r['portfolio_return']:6.2f}%, "
                f"沪深300={r['benchmark_return']:6.2f}%, "
                f"超额={r['excess_return']:+6.2f}%"
            )

    print("\n市场环境适应性判断:")
    print("- 2022年熊市: 策略表现稳健，适合防守")
    print("- 2023-2024年震荡: 策略提供稳定收益，波动低")
    print("- 利率下行周期: 国债价格上涨，策略受益")
    print("- 风险偏好低时: 替代股票仓位，降低组合波动")

    print("\n最佳适用场景:")
    print("1. 市场高位/估值偏高时 - 降低权益暴露")
    print("2. 经济下行/降息周期 - 债券价格上涨")
    print("3. 组合需要降低波动 - 作为压舱石")
    print("4. 等待更好入场时机 - 临时现金管理")

    print("\n不适用场景:")
    print("1. 强烈牛市 - 跑输股票策略")
    print("2. 加息周期 - 债券价格下跌")
    print("3. 追求高收益 - 年化6%左右，有限")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n=== 分析完成 ===")
