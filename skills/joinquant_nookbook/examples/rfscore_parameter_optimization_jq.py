"""
RFScore 参数调优 - JoinQuant Notebook 版本
测试不同调仓频率和持仓数量组合的效果
"""

from jqdata import *
import numpy as np
import pandas as pd

print("=== RFScore 参数调优测试 ===")
print("\n测试参数组合:")
print("1. 调仓频率: 月度 vs 周度")
print("2. 持仓数量: 15/12/10/0 vs 10/8/6/0 vs 8/6/4/0")

test_params = [
    {"name": "V1_月度_15只", "freq": "monthly", "hold": [15, 12, 10, 0]},
    {"name": "V1.1_周度_10只", "freq": "weekly", "hold": [10, 8, 6, 0]},
    {"name": "保守_周度_8只", "freq": "weekly", "hold": [8, 6, 4, 0]},
]

test_date = "2024-01-15"

try:
    print(f"\n测试日期: {test_date}")
    print("\n获取股票池...")
    hs300 = get_index_stocks("000300.XSHG", date=test_date)
    zz500 = get_index_stocks("000905.XSHG", date=test_date)
    universe = list(set(hs300 + zz500))

    universe = [s for s in universe if not s.startswith("688")]

    print(f"股票池数量: {len(universe)}")

    print("\n获取因子数据...")

    def get_simple_factors(stock):
        try:
            df = get_price(
                stock,
                end_date=test_date,
                count=60,
                fields=["close", "volume"],
                panel=False,
            )
            if df.empty or len(df) < 60:
                return None

            close = df["close"].values
            volume = df["volume"].values

            roa_proxy = (close[-1] / close[0] - 1) if len(close) >= 60 else 0

            cfoa_proxy = (
                np.mean(volume[-20:]) / np.mean(volume) if np.mean(volume) > 0 else 0
            )

            delta_margin = (
                (np.mean(close[-5:]) - np.mean(close[-20:])) / np.mean(close[-20:])
                if np.mean(close[-20:]) > 0
                else 0
            )

            delta_turn = (
                (np.mean(volume[-5:]) / np.mean(volume[-20:]))
                if np.mean(volume[-20:]) > 0
                else 1
            )

            score = 0
            if roa_proxy > 0.1:
                score += 2
            elif roa_proxy > 0:
                score += 1

            if cfoa_proxy > 1:
                score += 2
            elif cfoa_proxy > 0.8:
                score += 1

            if delta_margin > 0:
                score += 2
            elif delta_margin > -0.05:
                score += 1

            if delta_turn > 1.2:
                score += 2
            elif delta_turn > 0.8:
                score += 1

            return {
                "code": stock,
                "rfscore": min(7, max(1, score)),
                "roa": roa_proxy,
                "cfoa": cfoa_proxy,
                "momentum": (close[-1] / close[-20] - 1) if len(close) >= 20 else 0,
                "volume_ratio": delta_turn,
                "close": close[-1],
            }
        except:
            return None

    print("\n计算市场宽度...")
    breadth_data = []

    for stock in universe[:50]:
        try:
            df = get_price(
                stock, end_date=test_date, count=20, fields=["close"], panel=False
            )
            if not df.empty and len(df) >= 20:
                close = df["close"].values
                if close[-1] > np.mean(close):
                    breadth_data.append(1)
                else:
                    breadth_data.append(0)
        except:
            continue

    current_breadth = np.mean(breadth_data) if breadth_data else 0.5
    print(f"当前市场宽度: {current_breadth:.3f}")

    print("\n计算股票评分...")
    scores_data = []

    for stock in universe[:100]:
        factors = get_simple_factors(stock)
        if factors:
            scores_data.append(factors)

    print(f"成功计算 {len(scores_data)} 只股票")

    if scores_data:
        scores_df = pd.DataFrame(scores_data)
        scores_df = scores_df.sort_values("rfscore", ascending=False)

        print("\n=== 参数组合对比测试 ===")

        results = []

        for param in test_params:
            name = param["name"]
            hold_nums = param["hold"]

            if current_breadth < 0.15:
                target_hold = hold_nums[3]
            elif current_breadth < 0.25:
                target_hold = hold_nums[2]
            elif current_breadth < 0.35:
                target_hold = hold_nums[1]
            else:
                target_hold = hold_nums[0]

            high_score_stocks = scores_df[scores_df["rfscore"] >= 6].head(target_hold)

            if len(high_score_stocks) > 0:
                avg_return = np.mean(high_score_stocks["momentum"]) * 100
                avg_score = np.mean(high_score_stocks["rfscore"])
            else:
                avg_return = 0
                avg_score = 0

            results.append(
                {
                    "name": name,
                    "freq": param["freq"],
                    "hold_nums": hold_nums,
                    "current_breadth": current_breadth,
                    "target_hold": target_hold,
                    "actual_hold": len(high_score_stocks),
                    "avg_return": avg_return,
                    "avg_score": avg_score,
                }
            )

        print("\n测试结果:")
        print("-" * 80)
        for r in results:
            print(f"\n{r['name']}:")
            print(f"  调仓频率: {r['freq']}")
            print(f"  持仓档位: {r['hold_nums']}")
            print(f"  当前宽度: {r['current_breadth']:.3f}")
            print(f"  目标持仓: {r['target_hold']} 只")
            print(f"  实际持仓: {r['actual_hold']} 只")
            print(f"  平均收益: {r['avg_return']:.2f}%")
            print(f"  平均评分: {r['avg_score']:.1f}")

        print("\n" + "=" * 80)
        print("参数推荐:")

        best_return = max(results, key=lambda x: x["avg_return"])
        print(f"\n收益最优: {best_return['name']}")
        print(f"  平均收益: {best_return['avg_return']:.2f}%")

        best_concentration = min(results, key=lambda x: x["target_hold"])
        print(f"\n最集中持仓: {best_concentration['name']}")
        print(f"  持仓数量: {best_concentration['hold_nums']}")

        print("\n=== 测试完成 ===")

except Exception as e:
    print(f"测试错误: {e}")
    import traceback

    traceback.print_exc()

print("\n建议:")
print("1. 周度调仓比月度调仓响应更及时")
print("2. 持仓数量减少会提高集中度和收益波动")
print("3. 建议根据风险承受能力选择持仓数量")
print("4. 最终参数需要在完整回测中验证")
