"""
二板策略 Notebook 格式 - RiceQuant
任务04v2：二板2021-2023实测验证

Notebook 格式说明：
- 直接执行代码，不依赖策略框架
- 使用 print 输出结果
- 手动实现循环和统计
"""

print("=" * 80)
print("任务04v2：二板策略2021-2023实测验证（RiceQuant Notebook版）")
print("=" * 80)

import numpy as np

# 全局结果存储
results_by_year = {}


def get_zt_stocks(date, limit=500):
    """获取指定日期的涨停股票"""
    all_inst = all_instruments("CS")
    stock_list = all_inst["order_book_id"].tolist()

    # 过滤科创板、北交所
    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]
    stocks = stocks[:limit]

    zt_list = []
    for stock in stocks:
        try:
            bars = history_bars(stock, 1, "1d", ["close", "limit_up"], end_date=date)
            if bars is not None and len(bars) > 0:
                if bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99:
                    zt_list.append(stock)
        except:
            pass
    return zt_list


def is_zt_on_date(stock, date):
    """检查指定日期是否涨停"""
    try:
        bars = history_bars(stock, 1, "1d", ["close", "limit_up"], end_date=date)
        if bars is not None and len(bars) > 0:
            return bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99
    except:
        pass
    return False


def check_second_board(stock, date):
    """
    检查是否是二板股票
    二板定义：昨天涨停，前天也涨停，大前天不涨停
    """
    try:
        # 获取最近3天数据
        bars = history_bars(stock, 3, "1d", ["close", "limit_up"], end_date=date)
        if bars is None or len(bars) < 3:
            return False, None

        # 昨天（-1）涨停
        if bars[-1]["close"] < bars[-1]["limit_up"] * 0.99:
            return False, None

        # 前天（-2）涨停
        if bars[-2]["close"] < bars[-2]["limit_up"] * 0.99:
            return False, None

        # 大前天（-3）不涨停
        if bars[-3]["close"] >= bars[-3]["limit_up"] * 0.99:
            return False, None

        # 检查缩量
        vol_bars = history_bars(stock, 2, "1d", ["volume"], end_date=date)
        if vol_bars is not None and len(vol_bars) >= 2:
            vol_ratio = vol_bars[-1]["volume"] / vol_bars[-2]["volume"]
            if vol_ratio > 1.875:
                return False, None

        return True, bars[-1]["limit_up"]
    except:
        pass
    return False, None


def test_single_year(year):
    """测试单年表现"""
    print(f"\n{'=' * 60}")
    print(f"测试 {year} 年")
    print(f"{'=' * 60}")

    # 获取交易日
    try:
        trading_days = get_trading_dates(f"{year}-01-01", f"{year}-12-31")
    except:
        print(f"无法获取{year}年交易日")
        return None

    print(f"交易日数: {len(trading_days)}")

    results = {
        "year": year,
        "signals": 0,
        "trades": 0,
        "wins": 0,
        "profits": [],
        "max_profits": [],
    }

    for i in range(len(trading_days) - 1):
        date = trading_days[i]
        next_date = trading_days[i + 1]

        # 进度显示
        if i % 20 == 0:
            print(f"处理中: {i}/{len(trading_days)}")

        try:
            # 获取涨停股票
            zt_stocks = get_zt_stocks(date, limit=400)

            # 情绪过滤：涨停数>=10
            if len(zt_stocks) < 10:
                continue

            results["signals"] += len(zt_stocks)

            # 找二板股票
            candidates = []
            for stock in zt_stocks:
                is_2b, limit_up = check_second_board(stock, date)
                if is_2b:
                    candidates.append((stock, limit_up))

            if len(candidates) == 0:
                continue

            # 选择第一只（实际应该按市值排序，这里简化）
            target, limit_up = candidates[0]

            # 获取次日开盘价
            next_bars = history_bars(
                target, 1, "1d", ["open", "high", "close"], end_date=next_date
            )
            if next_bars is None or len(next_bars) == 0:
                continue

            open_price = next_bars[-1]["open"]
            high_price = next_bars[-1]["high"]
            close_price = next_bars[-1]["close"]

            # 非涨停开盘才买入
            if open_price >= limit_up * 0.99:
                continue

            # 计算收益（买入价=开盘价*1.005，考虑滑点）
            buy_price = open_price * 1.005
            profit = (close_price / buy_price - 1) * 100
            max_profit = (high_price / buy_price - 1) * 100

            results["trades"] += 1
            results["profits"].append(profit)
            results["max_profits"].append(max_profit)
            if profit > 0:
                results["wins"] += 1

        except Exception as e:
            continue

    # 计算统计指标
    if results["trades"] > 0:
        results["win_rate"] = results["wins"] / results["trades"] * 100
        results["avg_profit"] = np.mean(results["profits"])
        results["avg_max_profit"] = np.mean(results["max_profits"])

        # 计算盈亏比
        wins = [p for p in results["profits"] if p > 0]
        losses = [p for p in results["profits"] if p <= 0]
        avg_win = np.mean(wins) if wins else 0
        avg_loss = np.mean(np.abs(losses)) if losses else 1
        results["pl_ratio"] = avg_win / avg_loss if avg_loss > 0 else 0

        # 计算累计收益和最大回撤
        cum = np.cumsum(results["profits"])
        results["cumulative"] = cum[-1]
        peak = np.maximum.accumulate(cum)
        results["max_dd"] = np.max(peak - cum) if len(cum) > 0 else 0

        print(f"\n{year}年结果:")
        print(f"  信号数: {results['signals']}")
        print(f"  交易数: {results['trades']}")
        print(f"  胜率: {results['win_rate']:.2f}%")
        print(f"  平均收益: {results['avg_profit']:.2f}%")
        print(f"  平均最大收益: {results['avg_max_profit']:.2f}%")
        print(f"  盈亏比: {results['pl_ratio']:.2f}")
        print(f"  累计收益: {results['cumulative']:.2f}%")
        print(f"  最大回撤: {results['max_dd']:.2f}%")
    else:
        print(f"\n{year}年: 无交易")
        results["win_rate"] = 0
        results["avg_profit"] = 0
        results["avg_max_profit"] = 0
        results["pl_ratio"] = 0
        results["cumulative"] = 0
        results["max_dd"] = 0

    return results


print("\n开始逐年测试...")

# 测试2021-2023年
for year in [2021, 2022, 2023]:
    try:
        result = test_single_year(year)
        if result:
            results_by_year[year] = result
    except Exception as e:
        print(f"{year}年测试失败: {e}")
        import traceback

        traceback.print_exc()

# 汇总结果
print("\n" + "=" * 80)
print("汇总结果")
print("=" * 80)
print(
    f"{'年份':<6} {'信号':<6} {'交易':<6} {'胜率':<10} {'日均收益':<12} {'最大收益':<12} {'盈亏比':<8} {'累计收益':<12} {'最大回撤':<10}"
)
print("-" * 80)

for year in [2021, 2022, 2023]:
    r = results_by_year.get(year)
    if r and r.get("trades", 0) > 0:
        print(
            f"{year:<6} {r['signals']:<6} {r['trades']:<6} {r['win_rate']:<10.2f}% {r['avg_profit']:<12.2f}% {r['avg_max_profit']:<12.2f}% {r['pl_ratio']:<8.2f} {r['cumulative']:<12.2f}% {r['max_dd']:<10.2f}%"
        )
    else:
        print(f"{year:<6} {'-':<6} {'-':<6} {'未完成':<10}")

# 稳定性判定
print("\n" + "=" * 80)
print("稳定性判定")
print("=" * 80)

win_rates = [r["win_rate"] for r in results_by_year.values() if r.get("trades", 0) > 0]
cumulative = [r["cumulative"] for r in results_by_year.values()]

positive_years = len([c for c in cumulative if c > 0])
win_diff = max(win_rates) - min(win_rates) if len(win_rates) >= 2 else 100

print(f"正收益年份: {positive_years}/3 (需≥2)")
print(f"胜率差异: {win_diff:.2f}% (需<15%)")

if positive_years >= 2 and win_diff < 15:
    print("\n判定: 稳定 ✓")
    decision = "Go"
elif positive_years >= 1 or win_diff < 20:
    print("\n判定: 需观察")
    decision = "Watch"
else:
    print("\n判定: 不稳定")
    decision = "No-Go"

print(f"\n最终决策: {decision}")
print("=" * 80)
