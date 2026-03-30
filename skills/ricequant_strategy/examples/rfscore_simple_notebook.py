"""
RFScore 简化策略 - Notebook 版本

用于快速验证选股逻辑
"""

import numpy as np

print("=== RFScore 简化策略 Notebook 测试 ===")

try:
    print("获取沪深300成分股...")
    hs300 = index_components("000300.XSHG")[:30]
    print(f"测试股票数: {len(hs300)}")

    scores = []
    for stock in hs300:
        try:
            bars = history_bars(stock, 20, "1d", ["close", "volume"], include_now=True)
            if bars is None or len(bars) < 20:
                continue

            close = bars["close"]
            volume = bars["volume"]

            momentum = (close[-1] / close[0] - 1) * 100

            vol_ratio = (
                np.mean(volume[-5:]) / np.mean(volume) if np.mean(volume) > 0 else 0
            )

            price_pos = (
                (close[-1] - np.min(close)) / (np.max(close) - np.min(close))
                if np.max(close) != np.min(close)
                else 0.5
            )

            score = 0
            if momentum > 0:
                score += 2
            elif momentum > -5:
                score += 1

            if vol_ratio > 1.2:
                score += 2
            elif vol_ratio > 0.8:
                score += 1

            if price_pos > 0.7:
                score += 2
            elif price_pos > 0.3:
                score += 1

            fscore = min(7, max(1, score + 1))

            scores.append(
                {
                    "code": stock,
                    "close": close[-1],
                    "momentum": momentum,
                    "fscore": fscore,
                }
            )

        except Exception as e:
            continue

    print(f"\n成功计算 {len(scores)} 只股票的评分")

    if scores:
        scores.sort(key=lambda x: -x["fscore"])

        print("\n评分最高的5只股票:")
        for i, s in enumerate(scores[:5]):
            print(
                f"  {i + 1}. {s['code']}: FScore={s['fscore']}, 动量={s['momentum']:.2f}%"
            )

        high_score_stocks = [s["code"] for s in scores if s["fscore"] >= 6]
        print(f"\nFScore >= 6 的股票数: {len(high_score_stocks)}")

        print("\n策略逻辑验证成功!")

except Exception as e:
    print(f"策略测试错误: {e}")
    print("可能需要在 RiceQuant Notebook 平台上运行")

print("\n=== 测试完成 ===")
