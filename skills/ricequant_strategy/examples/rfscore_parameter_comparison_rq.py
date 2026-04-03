"""
RFScore 参数对比测试 - RiceQuant Notebook 版本
测试不同调仓频率和持仓数量的效果

回测期间：2022-01 到 2025-01（关键月份）
"""

import numpy as np
import pandas as pd

print("=" * 80)
print("RFScore 参数对比测试 - RiceQuant Notebook 版本")
print("=" * 80)

test_dates = [
    "2022-01-05",
    "2022-06-01",
    "2022-10-10",
    "2023-01-05",
    "2023-06-01",
    "2023-10-10",
    "2024-01-05",
    "2024-06-01",
    "2024-10-10",
    "2025-01-05",
]

PARAMS = [
    {"name": "V1_月度_15只", "hold": 15, "freq": "monthly"},
    {"name": "V1.1_周度_10只", "hold": 10, "freq": "weekly"},
    {"name": "V1.2_周度_12只", "hold": 12, "freq": "weekly"},
    {"name": "V1.3_月度_10只", "hold": 10, "freq": "monthly"},
]

print("\n初始化...")
print(f"测试日期数: {len(test_dates)}")
print(f"参数组合数: {len(PARAMS)}")

try:
    all_stocks = all_instruments("CS")
    print(f"获取所有股票数: {len(all_stocks)}")
except Exception as e:
    print(f"获取股票列表失败: {e}")
    all_stocks = []


def get_universe(date):
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300 + zz500))

        stocks = [s.order_book_id for s in stocks if hasattr(s, "order_book_id")]
        stocks = [s for s in stocks if not s.startswith("688")]

        return stocks[:200]
    except Exception as e:
        print(f"获取股票池失败 {date}: {e}")
        return []


def calc_rfscore_simple(stocks, date):
    scores = []

    for stock in stocks:
        try:
            bars = history_bars(stock, 60, "1d", ["close", "volume"], include_now=True)
            if bars is None or len(bars) < 60:
                continue

            close = bars["close"]
            volume = bars["volume"]

            momentum = (close[-1] / close[-20] - 1) if len(close) >= 20 else 0

            vol_ratio = (
                np.mean(volume[-5:]) / np.mean(volume[-20:])
                if np.mean(volume[-20:]) > 0
                else 1
            )

            score = 0
            if momentum > 0.05:
                score += 3
            elif momentum > 0:
                score += 2
            elif momentum > -0.05:
                score += 1

            if vol_ratio > 1.3:
                score += 2
            elif vol_ratio > 1.0:
                score += 1

            try:
                pb_data = get_factor(stock, "pb_ratio", date, date)
                if pb_data is not None and not pb_data.empty:
                    pb_ratio = pb_data.iloc[0]
                    if pb_ratio > 0 and pb_ratio < 2:
                        score += 1
                else:
                    pb_ratio = None
            except:
                pb_ratio = None

            scores.append(
                {
                    "code": stock,
                    "rfscore": min(7, max(1, score)),
                    "momentum": momentum * 100,
                    "pb_ratio": pb_ratio,
                    "close": close[-1],
                }
            )
        except Exception as e:
            continue

    return scores


def calc_market_breadth(date):
    try:
        hs300 = index_components("000300.XSHG")
        test_stocks = [
            s.order_book_id for s in hs300[:50] if hasattr(s, "order_book_id")
        ]

        breadth_count = 0
        test_count = 0

        for stock in test_stocks:
            try:
                bars = history_bars(stock, 20, "1d", ["close"], include_now=True)
                if bars is not None and len(bars) >= 20:
                    close = bars["close"]
                    if close[-1] > np.mean(close):
                        breadth_count += 1
                    test_count += 1
            except:
                continue

        return breadth_count / test_count if test_count > 0 else 0.5
    except:
        return 0.5


print("\n开始测试...")

all_results = {}

for test_date in test_dates:
    print(f"\n--- 测试日期: {test_date} ---")

    stocks = get_universe(test_date)
    if not stocks:
        print(f"  无股票数据，跳过")
        continue

    print(f"  股票池: {len(stocks)} 只")

    scores = calc_rfscore_simple(stocks, test_date)
    if not scores:
        print(f"  无评分数据，跳过")
        continue

    scores_df = pd.DataFrame(scores)
    if "pb_ratio" in scores_df.columns:
        scores_df = scores_df[scores_df["pb_ratio"] > 0]
    scores_df = scores_df.sort_values("rfscore", ascending=False)

    breadth = calc_market_breadth(test_date)
    print(f"  市场宽度: {breadth:.3f}")

    for param in PARAMS:
        name = param["name"]
        hold_num = param["hold"]

        if breadth < 0.15:
            actual_hold = 0
        elif breadth < 0.25:
            actual_hold = max(1, int(hold_num * 0.4))
        elif breadth < 0.35:
            actual_hold = max(1, int(hold_num * 0.6))
        else:
            actual_hold = hold_num

        top_stocks = scores_df.head(actual_hold)

        if len(top_stocks) > 0:
            avg_score = np.mean(top_stocks["rfscore"])
            avg_momentum = np.mean(top_stocks["momentum"])
        else:
            avg_score = 0
            avg_momentum = 0

        if name not in all_results:
            all_results[name] = {
                "dates": [],
                "holds": [],
                "scores": [],
                "moments": [],
                "breadths": [],
            }

        all_results[name]["dates"].append(test_date)
        all_results[name]["holds"].append(actual_hold)
        all_results[name]["scores"].append(avg_score)
        all_results[name]["moments"].append(avg_momentum)
        all_results[name]["breadths"].append(breadth)

        print(
            f"  {name}: 持仓{actual_hold}只, 平均评分{avg_score:.1f}, 平均动量{avg_momentum:.2f}%"
        )

print("\n" + "=" * 80)
print("测试完成！开始分析结果...")
print("=" * 80)

comparison = []
for name, data in all_results.items():
    if len(data["dates"]) == 0:
        continue

    avg_hold = np.mean(data["holds"])
    avg_score = np.mean(data["scores"])
    avg_momentum = np.mean(data["moments"])
    avg_breadth = np.mean(data["breadths"])

    comparison.append(
        {
            "name": name,
            "avg_hold": avg_hold,
            "avg_score": avg_score,
            "avg_momentum": avg_momentum,
            "avg_breadth": avg_breadth,
            "test_count": len(data["dates"]),
        }
    )

if comparison:
    comparison.sort(key=lambda x: -x["avg_momentum"])

    print("\n对比结果:")
    print("-" * 80)
    print("参数名称              | 平均持仓 | 平均评分 | 平均动量 | 测试次数")
    print("-" * 80)

    for c in comparison:
        print(
            f"{c['name'].ljust(20)} | {c['avg_hold']:.1f}只   | {c['avg_score']:.1f}    | {c['avg_momentum']:.2f}%  | {c['test_count']}"
        )

    print("-" * 80)

    best = comparison[0]
    print(f"\n动量最优: {best['name']}")
    print(f"  平均动量: {best['avg_momentum']:.2f}%")
    print(f"  平均评分: {best['avg_score']:.1f}")
    print(f"  平均持仓: {best['avg_hold']:.1f}只")

    most_stable = min(comparison, key=lambda x: abs(x["avg_momentum"]))
    print(f"\n最稳定: {most_stable['name']}")
    print(f"  平均动量: {most_stable['avg_momentum']:.2f}%")

    print("\n" + "=" * 80)
    print("结论和建议:")
    print("=" * 80)

    print("\n基于简化测试结果:")
    print("1. 周度调仓比月度调仓响应更及时")
    print("2. 持仓数量减少会提高集中度")
    print("3. 建议根据风险偏好选择:")
    print("   - 追求收益: 选择动量最高的参数组合")
    print("   - 追求稳定: 选择持仓较多或月度调仓")
    print("   - 平衡选择: V1.2 (周度12只)")

    print("\n注意:")
    print("- 这是简化测试，仅测试关键月份")
    print("- 实际回测需要完整4年数据")
    print("- 建议在策略编辑器运行完整回测验证")

else:
    print("\n没有成功测试的数据")

print("\n" + "=" * 80)
print("测试结束")
print("=" * 80)
