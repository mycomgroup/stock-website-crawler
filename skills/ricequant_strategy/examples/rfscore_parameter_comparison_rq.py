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


def get_universe():
    try:
        hs300 = index_components("000300.XSHG")
        print(f"  沪深300成分股: {len(hs300)}")

        zz500 = index_components("000905.XSHG")
        print(f"  中证500成分股: {len(zz500)}")

        stocks = []

        for item in hs300[:100]:
            if hasattr(item, "order_book_id"):
                sid = item.order_book_id
            else:
                sid = str(item)

            if not sid.startswith("688"):
                stocks.append(sid)

        for item in zz500[:100]:
            if hasattr(item, "order_book_id"):
                sid = item.order_book_id
            else:
                sid = str(item)

            if not sid.startswith("688") and sid not in stocks:
                stocks.append(sid)

        return stocks[:200]
    except Exception as e:
        print(f"获取股票池失败: {e}")
        import traceback

        traceback.print_exc()
        return []


def calc_rfscore_simple(stocks):
    scores = []

    for i, stock in enumerate(stocks):
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

            pb_ratio = None
            try:
                pb_data = get_factor(stock, "pb_ratio", "2024-01-01", "2024-01-01")
                if pb_data is not None and not pb_data.empty:
                    pb_ratio = float(pb_data.iloc[0])
                    if pb_ratio > 0 and pb_ratio < 2:
                        score += 1
            except:
                pass

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


def calc_market_breadth(stocks):
    try:
        test_stocks = stocks[:50]

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


print("\n获取股票池...")
stocks = get_universe()
print(f"最终股票池: {len(stocks)} 只")

if not stocks:
    print("错误: 无法获取股票池")
else:
    print("\n开始测试...")

    print("\n计算股票评分...")
    scores = calc_rfscore_simple(stocks)
    print(f"成功评分: {len(scores)} 只")

    if scores:
        scores_df = pd.DataFrame(scores)
        if "pb_ratio" in scores_df.columns:
            scores_df = scores_df[scores_df["pb_ratio"] > 0]
        scores_df = scores_df.sort_values("rfscore", ascending=False)

        print(f"\n评分TOP10:")
        for i, row in scores_df.head(10).iterrows():
            print(f"  {row['code']}: 评分{row['rfscore']}, 动量{row['momentum']:.2f}%")

        print("\n计算市场宽度...")
        breadth = calc_market_breadth(stocks)
        print(f"市场宽度: {breadth:.3f}")

        print("\n参数对比:")
        print("-" * 80)

        all_results = {}

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

            all_results[name] = {
                "hold": actual_hold,
                "score": avg_score,
                "momentum": avg_momentum,
            }

            print(f"{name}:")
            print(f"  持仓: {actual_hold}只")
            print(f"  平均评分: {avg_score:.1f}")
            print(f"  平均动量: {avg_momentum:.2f}%")
            print()

        print("-" * 80)

        sorted_results = sorted(all_results.items(), key=lambda x: -x[1]["momentum"])
        best = sorted_results[0]

        print(f"\n动量最优: {best[0]}")
        print(f"  平均动量: {best[1]['momentum']:.2f}%")
        print(f"  平均评分: {best[1]['score']:.1f}")

        print("\n" + "=" * 80)
        print("结论:")
        print("=" * 80)
        print("\n基于当前市场状态:")
        print(f"  市场宽度: {breadth:.3f}", end="")
        if breadth < 0.15:
            print(" (极弱)")
        elif breadth < 0.25:
            print(" (较弱)")
        elif breadth < 0.35:
            print(" (中性)")
        else:
            print(" (较强)")

        print("\n建议:")
        if breadth < 0.25:
            print("  市场较弱，建议降低持仓或空仓观望")
        elif breadth < 0.35:
            print("  市场中性，建议中等持仓")
        else:
            print("  市场较强，可正常持仓")

        print(f"\n最优参数: {best[0]}")
    else:
        print("错误: 无法计算评分")

print("\n" + "=" * 80)
print("测试结束")
print("=" * 80)
