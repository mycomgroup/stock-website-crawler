# 组合策略完整测试
from jqdata import *
import numpy as np

print("=" * 50)
print("任务07：组合策略回测")
print("=" * 50)

# 获取交易日（测试2024全年）
trade_days = list(get_trade_days("2024-01-01", "2024-06-30"))
print(f"交易日总数: {len(trade_days)}")

# 存储结果
fb_returns = []  # 首板低开
wts_returns = []  # 弱转强
dates_with_signals = []

# 遍历交易日
for i in range(1, min(len(trade_days), 60)):  # 测试约3个月
    date = trade_days[i]
    prev_date = trade_days[i - 1]
    date_str = str(date)
    prev_str = str(prev_date)

    if i % 10 == 0:
        print(f"进度: {date_str}")

    try:
        # 获取股票池
        stocks = get_all_securities("stock", date_str).index.tolist()
        stocks = [s for s in stocks if s[:2] != "68" and s[0] not in ["4", "8"]][:300]

        # 昨日涨停股
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
        hl = df[df["close"] == df["high_limit"]]["code"].tolist()

        if not hl:
            continue

        # 今日数据
        today = get_price(
            hl[:50],
            end_date=date_str,
            frequency="daily",
            fields=["open", "close", "high_limit"],
            count=1,
            panel=False,
        )
        if today.empty:
            continue
        today = today.dropna()
        today["ratio"] = today["open"] / (today["high_limit"] / 1.1)

        # 首板低开: 假弱高开 0.5%-1.5%
        fb = today[(today["ratio"] > 1.005) & (today["ratio"] < 1.015)]
        if len(fb) > 0:
            r = ((fb["close"] - fb["open"]) / fb["open"]).mean()
            fb_returns.append(r)

        # 弱转强: 高开0-6%
        wts = today[(today["ratio"] > 1.0) & (today["ratio"] < 1.06)]
        if len(wts) > 0:
            r = ((wts["close"] - wts["open"]) / wts["open"]).mean()
            wts_returns.append(r)
            dates_with_signals.append(date_str)

    except:
        pass

# 计算统计
print("\n" + "=" * 50)
print("回测结果 (2024H1)")
print("=" * 50)

# 首板低开
if fb_returns:
    fb_avg = np.mean(fb_returns) * 100
    fb_win = sum(1 for r in fb_returns if r > 0) / len(fb_returns) * 100
    fb_total = (1 + np.array(fb_returns)).prod() - 1
    print(f"\n首板低开策略:")
    print(f"  信号日数: {len(fb_returns)}")
    print(f"  平均单日收益: {fb_avg:.2f}%")
    print(f"  胜率: {fb_win:.1f}%")
    print(f"  累计收益: {fb_total * 100:.1f}%")

# 弱转强
if wts_returns:
    wts_avg = np.mean(wts_returns) * 100
    wts_win = sum(1 for r in wts_returns if r > 0) / len(wts_returns) * 100
    wts_total = (1 + np.array(wts_returns)).prod() - 1
    print(f"\n弱转强竞价策略:")
    print(f"  信号日数: {len(wts_returns)}")
    print(f"  平均单日收益: {wts_avg:.2f}%")
    print(f"  胜率: {wts_win:.1f}%")
    print(f"  累计收益: {wts_total * 100:.1f}%")

# 组合分析
if fb_returns and wts_returns:
    min_len = min(len(fb_returns), len(wts_returns))
    fb_arr = np.array(fb_returns[:min_len])
    wts_arr = np.array(wts_returns[:min_len])

    # 相关性
    corr = np.corrcoef(fb_arr, wts_arr)[0, 1]
    print(f"\n策略相关性: {corr:.3f}")

    # 等权组合
    eq_ret = (fb_arr + wts_arr) / 2
    eq_avg = np.mean(eq_ret) * 100
    eq_win = sum(1 for r in eq_ret if r > 0) / len(eq_ret) * 100
    eq_total = (1 + eq_ret).prod() - 1
    print(f"\n等权组合:")
    print(f"  平均单日收益: {eq_avg:.2f}%")
    print(f"  胜率: {eq_win:.1f}%")
    print(f"  累计收益: {eq_total * 100:.1f}%")

    # 风险平价 (60%首板, 40%弱转强)
    rp_ret = fb_arr * 0.6 + wts_arr * 0.4
    rp_avg = np.mean(rp_ret) * 100
    rp_win = sum(1 for r in rp_ret if r > 0) / len(rp_ret) * 100
    rp_total = (1 + rp_ret).prod() - 1
    print(f"\n风险平价组合 (60%/40%):")
    print(f"  平均单日收益: {rp_avg:.2f}%")
    print(f"  胜率: {rp_win:.1f}%")
    print(f"  累计收益: {rp_total * 100:.1f}%")

# 最终结论
print("\n" + "=" * 50)
print("结论")
print("=" * 50)

if fb_returns and wts_returns:
    best_single = "首板低开" if fb_total > wts_total else "弱转强"
    best_ret = max(fb_total, wts_total)

    print(f"\n最强单策略: {best_single}")
    print(f"  累计收益: {best_ret * 100:.1f}%")
    print(f"\n等权组合收益: {eq_total * 100:.1f}%")
    print(f"风险平价组合收益: {rp_total * 100:.1f}%")

    if eq_total > best_ret or rp_total > best_ret:
        print("\n结论: Go - 组合有效")
    else:
        print("\n结论: No-Go - 组合不如单策略")

print("\n测试完成")
