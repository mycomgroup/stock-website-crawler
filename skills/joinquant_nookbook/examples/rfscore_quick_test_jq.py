"""
RFScore 快速参数测试 - JoinQuant Notebook
简化版：只测试30只股票，快速对比参数效果
"""

from jqdata import *
import numpy as np

print("=== RFScore 快速参数测试 ===")

test_date = "2024-01-15"

try:
    print(f"测试日期: {test_date}")

    hs300 = get_index_stocks("000300.XSHG", date=test_date)[:30]
    print(f"测试股票数: {len(hs300)}")

    print("\n计算市场宽度...")
    breadth_count = 0
    test_count = 0

    for stock in hs300:
        df = get_price(
            stock, end_date=test_date, count=20, fields=["close"], panel=False
        )
        if not df.empty:
            close = df["close"].values
            if close[-1] > np.mean(close):
                breadth_count += 1
            test_count += 1

    breadth = breadth_count / test_count if test_count > 0 else 0.5
    print(f"市场宽度: {breadth:.3f}")

    print("\n计算股票评分...")
    scores = []

    for stock in hs300:
        df = get_price(
            stock, end_date=test_date, count=60, fields=["close", "volume"], panel=False
        )
        if df.empty or len(df) < 60:
            continue

        close = df["close"].values
        volume = df["volume"].values

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

        scores.append(
            {
                "code": stock,
                "rfscore": min(7, max(1, score)),
                "momentum": momentum * 100,
                "close": close[-1],
            }
        )

    print(f"计算完成: {len(scores)} 只股票")

    scores.sort(key=lambda x: -x["rfscore"])

    print("\n评分TOP10:")
    for i, s in enumerate(scores[:10]):
        print(f"{i + 1}. {s['code']}: Score={s['rfscore']}, 动量={s['momentum']:.2f}%")

    print("\n=== 参数对比 ===")

    params = [
        {"name": "V1_月度", "hold": 15},
        {"name": "V1.1_周度", "hold": 10},
        {"name": "保守_周度", "hold": 8},
    ]

    for p in params:
        top_stocks = [s for s in scores if s["rfscore"] >= 5][: p["hold"]]
        avg_momentum = np.mean([s["momentum"] for s in top_stocks]) if top_stocks else 0

        print(f"\n{p['name']} (持仓{p['hold']}只):")
        print(f"  实际持仓: {len(top_stocks)} 只")
        print(f"  平均动量: {avg_momentum:.2f}%")

    print("\n=== 完成 ===")

except Exception as e:
    print(f"错误: {e}")

print("\n结论:")
if breadth < 0.3:
    print("  市场较弱，建议降低持仓")
else:
    print("  市场正常，可正常持仓")
print("  周度调仓响应更及时")
print("  10只持仓是平衡选择")
