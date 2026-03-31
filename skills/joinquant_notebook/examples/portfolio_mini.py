# 简单测试
from jqdata import *
import numpy as np

print("=" * 50)
print("组合策略测试")
print("=" * 50)

# 获取测试期间的交易日
trade_days = list(get_trade_days("2024-01-01", "2024-03-31"))
print(f"交易日总数: {len(trade_days)}")

# 存储结果
first_board_returns = []
weak_to_strong_returns = []

# 测试前10个交易日
test_days = trade_days[:10]

for i, date in enumerate(test_days):
    if i == 0:
        continue

    prev_date = test_days[i - 1]
    date_str = str(date)
    prev_str = str(prev_date)

    print(f"\n处理: {date_str}")

    try:
        # 获取股票池（限制数量）
        stocks = get_all_securities("stock", date_str).index.tolist()[:200]
        stocks = [s for s in stocks if s[:2] != "68" and s[0] not in ["4", "8"]]

        # 获取昨日涨停股
        df = get_price(
            stocks,
            end_date=prev_str,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        if df.empty:
            continue
        df = df.dropna()
        hl_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()

        if not hl_stocks:
            print(f"  无涨停股")
            continue

        # 今日开盘
        today_df = get_price(
            hl_stocks[:30],
            end_date=date_str,
            frequency="daily",
            fields=["open", "close", "high_limit"],
            count=1,
            panel=False,
        )
        if today_df.empty:
            continue
        today_df = today_df.dropna()
        today_df["open_ratio"] = today_df["open"] / (today_df["high_limit"] / 1.1)

        # 首板低开信号: 假弱高开 0.5%-1.5%
        fb = today_df[
            (today_df["open_ratio"] > 1.005) & (today_df["open_ratio"] < 1.015)
        ]
        if len(fb) > 0:
            fb_ret = ((fb["close"] - fb["open"]) / fb["open"]).mean()
            first_board_returns.append(fb_ret)
            print(f"  首板低开: {len(fb)}个, 收益: {fb_ret * 100:.2f}%")

        # 弱转强信号: 高开0-6%
        wts = today_df[(today_df["open_ratio"] > 1.0) & (today_df["open_ratio"] < 1.06)]
        if len(wts) > 0:
            wts_ret = ((wts["close"] - wts["open"]) / wts["open"]).mean()
            weak_to_strong_returns.append(wts_ret)
            print(f"  弱转强: {len(wts)}个, 收益: {wts_ret * 100:.2f}%")

    except Exception as e:
        print(f"  错误: {e}")

# 汇总结果
print("\n" + "=" * 50)
print("汇总结果")
print("=" * 50)

if first_board_returns:
    avg_fb = np.mean(first_board_returns) * 100
    win_fb = (
        sum(1 for r in first_board_returns if r > 0) / len(first_board_returns) * 100
    )
    print(f"\n首板低开策略:")
    print(f"  信号日数: {len(first_board_returns)}")
    print(f"  平均收益: {avg_fb:.2f}%")
    print(f"  胜率: {win_fb:.1f}%")

if weak_to_strong_returns:
    avg_wts = np.mean(weak_to_strong_returns) * 100
    win_wts = (
        sum(1 for r in weak_to_strong_returns if r > 0)
        / len(weak_to_strong_returns)
        * 100
    )
    print(f"\n弱转强竞价策略:")
    print(f"  信号日数: {len(weak_to_strong_returns)}")
    print(f"  平均收益: {avg_wts:.2f}%")
    print(f"  胜率: {win_wts:.1f}%")

# 组合分析
if first_board_returns and weak_to_strong_returns:
    # 等权组合
    min_len = min(len(first_board_returns), len(weak_to_strong_returns))
    combined_returns = [
        (first_board_returns[i] + weak_to_strong_returns[i]) / 2 for i in range(min_len)
    ]
    avg_comb = np.mean(combined_returns) * 100
    win_comb = sum(1 for r in combined_returns if r > 0) / len(combined_returns) * 100

    print(f"\n等权组合:")
    print(f"  平均收益: {avg_comb:.2f}%")
    print(f"  胜率: {win_comb:.1f}%")

    # 相关性
    if min_len > 1:
        corr = np.corrcoef(
            first_board_returns[:min_len], weak_to_strong_returns[:min_len]
        )[0, 1]
        print(f"  策略相关性: {corr:.4f}")

print("\n" + "=" * 50)
print("测试完成")
print("=" * 50)
