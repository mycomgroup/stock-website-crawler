# 纯 A 股 ETF 池重建实验 - 详细技术分析版
# 加入更多统计指标和分阶段分析

print("=" * 80)
print("【纯 A 股 ETF 池重建实验 - 详细技术分析版】")
print("=" * 80)
print()

try:
    from jqdata import *
    import pandas as pd
    import numpy as np
    import warnings
    from datetime import datetime, timedelta

    warnings.filterwarnings("ignore")

    # ============================================================================
    # 一、池子定义
    # ============================================================================

    OLD_POOL = {
        "沪深300ETF": "510300.XSHG",
        "中证500ETF": "510500.XSHG",
        "创业板ETF": "159915.XSHE",
        "科创50ETF": "588000.XSHG",
        "中证1000ETF": "512100.XSHG",
        "纳指ETF": "513100.XSHG",
        "标普500ETF": "513500.XSHG",
        "黄金ETF": "518880.XSHG",
        "国债ETF": "511010.XSHG",
        "医疗ETF": "512170.XSHG",
        "消费ETF": "159928.XSHE",
        "新能源ETF": "516160.XSHG",
    }

    NEW_POOL = {
        "沪深300ETF": "510300.XSHG",
        "中证500ETF": "510500.XSHG",
        "创业板ETF": "159915.XSHE",
        "科创50ETF": "588000.XSHG",
        "中证1000ETF": "512100.XSHG",
        "医疗ETF": "512170.XSHG",
        "消费ETF": "159928.XSHE",
        "新能源ETF": "516160.XSHG",
        "半导体ETF": "512480.XSHG",
        "军工ETF": "512660.XSHG",
        "银行ETF": "512800.XSHG",
        "计算机ETF": "512720.XSHG",
    }

    print("=" * 80)
    print("【一、池子成分对比】")
    print("=" * 80)
    print()

    # 显示删除和新增的ETF
    old_set = set(OLD_POOL.keys())
    new_set = set(NEW_POOL.keys())
    removed = old_set - new_set
    added = new_set - old_set

    print("从旧池删除的ETF:")
    for etf in removed:
        print(f"  ❌ {etf}: {OLD_POOL[etf]}")

    print()
    print("在新池新增的ETF:")
    for etf in added:
        print(f"  ✅ {etf}: {NEW_POOL[etf]}")

    print()
    print("=" * 80)
    print()

    # ============================================================================
    # 二、数据质量检查
    # ============================================================================

    print("=" * 80)
    print("【二、数据质量检查 - 2020-01-01至今】")
    print("=" * 80)
    print()

    start_date = "2020-01-01"
    end_date = str(get_trade_days(end_date=datetime.now(), count=1)[-1])

    print(f"数据区间: {start_date} ~ {end_date}")
    print()

    # 检查每个ETF的数据完整性
    print("旧池数据完整性检查:")
    for name, code in OLD_POOL.items():
        try:
            data = get_price(
                code, start_date=start_date, end_date=end_date, fields=["close"]
            )
            trading_days = len(get_trade_days(start_date, end_date))
            data_days = len(data)
            coverage = data_days / trading_days * 100
            start_avail = str(data.index[0])[:10] if len(data) > 0 else "N/A"

            if coverage < 95:
                status = "⚠️ 数据缺失"
            else:
                status = "✅ 数据完整"

            print(
                f"  {name:12s} {code:15s} 数据覆盖率: {coverage:5.1f}%  最早数据: {start_avail}  {status}"
            )
        except Exception as e:
            print(f"  {name:12s} {code:15s} 错误: {e}")

    print()
    print("新池数据完整性检查:")
    for name, code in NEW_POOL.items():
        try:
            data = get_price(
                code, start_date=start_date, end_date=end_date, fields=["close"]
            )
            trading_days = len(get_trade_days(start_date, end_date))
            data_days = len(data)
            coverage = data_days / trading_days * 100
            start_avail = str(data.index[0])[:10] if len(data) > 0 else "N/A"

            if coverage < 95:
                status = "⚠️ 数据缺失"
            elif start_avail > "2020-01-01":
                status = "⚠️ 成立较晚"
            else:
                status = "✅ 数据完整"

            print(
                f"  {name:12s} {code:15s} 数据覆盖率: {coverage:5.1f}%  最早数据: {start_avail}  {status}"
            )
        except Exception as e:
            print(f"  {name:12s} {code:15s} 错误: {e}")

    print()
    print("=" * 80)
    print()

    # ============================================================================
    # 三、相关性矩阵分析
    # ============================================================================

    print("=" * 80)
    print("【三、相关性矩阵分析 - 最近120个交易日】")
    print("=" * 80)
    print()

    # 获取最近120个交易日的数据计算相关性
    today = get_trade_days(end_date=datetime.now(), count=1)[-1]
    start_corr = get_trade_days(end_date=today, count=120)[0]

    # 旧池相关性
    print("旧池内部相关性矩阵:")
    old_returns = pd.DataFrame()
    for name, code in OLD_POOL.items():
        try:
            data = get_price(
                code, start_date=start_corr, end_date=today, fields=["close"]
            )
            old_returns[name] = data["close"].pct_change().dropna()
        except:
            pass

    old_corr = old_returns.corr()
    print(old_corr.round(2).to_string())

    # 计算平均相关性
    old_corr_values = old_corr.values
    mask = np.triu(np.ones_like(old_corr_values, dtype=bool), k=1)
    old_avg_corr = old_corr_values[mask].mean()
    print(f"\n旧池平均相关性: {old_avg_corr:.3f}")

    # 找出相关性最低的组合
    print("\n旧池相关性最低的组合 (Top 5):")
    corr_pairs = []
    for i in range(len(old_corr.columns)):
        for j in range(i + 1, len(old_corr.columns)):
            corr_pairs.append(
                (old_corr.columns[i], old_corr.columns[j], old_corr.iloc[i, j])
            )
    corr_pairs.sort(key=lambda x: abs(x[2]))
    for etf1, etf2, corr in corr_pairs[:5]:
        print(f"  {etf1} - {etf2}: {corr:.3f}")

    print()
    print("-" * 80)
    print()

    # 新池相关性
    print("新池内部相关性矩阵:")
    new_returns = pd.DataFrame()
    for name, code in NEW_POOL.items():
        try:
            data = get_price(
                code, start_date=start_corr, end_date=today, fields=["close"]
            )
            new_returns[name] = data["close"].pct_change().dropna()
        except:
            pass

    new_corr = new_returns.corr()
    print(new_corr.round(2).to_string())

    new_corr_values = new_corr.values
    mask = np.triu(np.ones_like(new_corr_values, dtype=bool), k=1)
    new_avg_corr = new_corr_values[mask].mean()
    print(f"\n新池平均相关性: {new_avg_corr:.3f}")

    print("\n新池相关性最低的组合 (Top 5):")
    corr_pairs = []
    for i in range(len(new_corr.columns)):
        for j in range(i + 1, len(new_corr.columns)):
            corr_pairs.append(
                (new_corr.columns[i], new_corr.columns[j], new_corr.iloc[i, j])
            )
    corr_pairs.sort(key=lambda x: abs(x[2]))
    for etf1, etf2, corr in corr_pairs[:5]:
        print(f"  {etf1} - {etf2}: {corr:.3f}")

    print()
    print("=" * 80)
    print()

    # ============================================================================
    # 四、波动率分析
    # ============================================================================

    print("=" * 80)
    print("【四、波动率分析 - 最近120个交易日】")
    print("=" * 80)
    print()

    print("旧池各ETF波动率 (年化):")
    for name in old_returns.columns:
        volatility = old_returns[name].std() * np.sqrt(252) * 100
        print(f"  {name:15s}: {volatility:6.2f}%")

    old_avg_vol = old_returns.std().mean() * np.sqrt(252) * 100
    print(f"\n旧池平均波动率: {old_avg_vol:.2f}%")

    print()
    print("-" * 80)
    print()

    print("新池各ETF波动率 (年化):")
    for name in new_returns.columns:
        volatility = new_returns[name].std() * np.sqrt(252) * 100
        print(f"  {name:15s}: {volatility:6.2f}%")

    new_avg_vol = new_returns.std().mean() * np.sqrt(252) * 100
    print(f"\n新池平均波动率: {new_avg_vol:.2f}%")

    print()
    print("=" * 80)
    print()

    # ============================================================================
    # 五、分阶段表现分析
    # ============================================================================

    print("=" * 80)
    print("【五、分阶段表现分析】")
    print("=" * 80)
    print()

    # 定义市场阶段
    stages = [
        ("2020-01-01", "2020-03-31", "新冠疫情爆发"),
        ("2020-04-01", "2021-02-28", "疫后复苏牛市"),
        ("2021-03-01", "2021-12-31", "结构性行情"),
        ("2022-01-01", "2022-10-31", "熊市下跌"),
        ("2022-11-01", "2023-05-31", "反弹修复"),
        ("2023-06-01", "2024-02-29", "震荡下行"),
        ("2024-03-01", "2024-09-30", "底部震荡"),
        ("2024-10-01", end_date, "9.24行情后"),
    ]

    def calc_stage_return(pool, start, end):
        """计算某个阶段等权持有所有ETF的收益"""
        total_return = 0
        valid_count = 0
        for name, code in pool.items():
            try:
                data = get_price(code, start_date=start, end_date=end, fields=["close"])
                if len(data) > 1:
                    ret = (data["close"].iloc[-1] / data["close"].iloc[0] - 1) * 100
                    total_return += ret
                    valid_count += 1
            except:
                pass
        return total_return / valid_count if valid_count > 0 else 0

    print("各阶段等权持有收益对比:")
    print(
        f"{'阶段':<25s} {'时间区间':<25s} {'旧池收益':<12s} {'新池收益':<12s} {'差异':<10s}"
    )
    print("-" * 80)

    for start, end, desc in stages:
        try:
            old_ret = calc_stage_return(OLD_POOL, start, end)
            new_ret = calc_stage_return(NEW_POOL, start, end)
            diff = new_ret - old_ret
            diff_str = f"{diff:+.2f}%"
            print(
                f"{desc:<25s} {start}~{end:<10s} {old_ret:>8.2f}%    {new_ret:>8.2f}%    {diff_str:>8s}"
            )
        except Exception as e:
            print(f"{desc:<25s} {start}~{end:<10s} 计算错误: {e}")

    print()
    print("=" * 80)
    print()

    # ============================================================================
    # 六、动量策略回测
    # ============================================================================

    print("=" * 80)
    print("【六、动量策略回测 - Mom20d/Hold10d】")
    print("=" * 80)
    print()

    START = "2020-01-01"
    END = "2024-12-31"
    COST = 0.001

    def get_rebal_dates(start, end, freq_days):
        all_days = get_trade_days(start, end)
        result = [all_days[0]]
        for d in all_days[1:]:
            if (d - result[-1]).days >= freq_days:
                result.append(d)
        return result

    def run_backtest(pool, pool_name):
        print(f"运行 {pool_name} 回测...")

        dates = get_rebal_dates(START, END, 10)
        codes = list(pool.values())
        rets = []
        prev_holdings = []

        for i, d in enumerate(dates[:-1]):
            d_str = str(d)
            next_d_str = str(dates[i + 1])
            try:
                # 计算20日动量
                prices = get_price(
                    codes, end_date=d_str, count=21, fields=["close"], panel=False
                )
                pivot = prices.pivot(
                    index="time", columns="code", values="close"
                ).dropna(axis=1)
                mom = pivot.iloc[-1] / pivot.iloc[0] - 1
                selected = mom.nlargest(3).index.tolist()

                # 计算收益
                p0 = get_price(
                    selected, end_date=d_str, count=1, fields=["close"], panel=False
                )
                p1 = get_price(
                    selected,
                    end_date=next_d_str,
                    count=1,
                    fields=["close"],
                    panel=False,
                )
                p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
                p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
                gross_ret = ((p1 / p0) - 1).mean()

                # 成本
                turnover = len(set(selected) - set(prev_holdings)) / 3
                net_ret = gross_ret - turnover * COST * 2
                rets.append(net_ret)
                prev_holdings = selected
            except:
                continue

        if not rets:
            return None

        s = pd.Series(rets)
        cum = (1 + s).cumprod()
        ann = cum.iloc[-1] ** (252 / 10 / len(s)) - 1
        dd = (cum / cum.cummax() - 1).min()
        sharpe = s.mean() / s.std() * np.sqrt(252 / 10) if s.std() > 0 else 0
        win = (s > 0).mean()

        return {
            "name": pool_name,
            "rets": s,
            "cum": cum,
            "ann": ann,
            "dd": dd,
            "sharpe": sharpe,
            "win": win,
        }

    old_result = run_backtest(OLD_POOL, "旧池(v1.0)")
    new_result = run_backtest(NEW_POOL, "新池(v2.0)")

    if old_result and new_result:
        print()
        print("回测结果对比:")
        print(f"{'指标':<20s} {'旧池(v1.0)':<15s} {'新池(v2.0)':<15s} {'变化':<15s}")
        print("-" * 65)
        print(
            f"{'年化收益':<20s} {old_result['ann']:<15.2%} {new_result['ann']:<15.2%} {new_result['ann'] - old_result['ann']:<+15.2%}"
        )
        print(
            f"{'最大回撤':<20s} {old_result['dd']:<15.2%} {new_result['dd']:<15.2%} {new_result['dd'] - old_result['dd']:<+15.2%}"
        )
        print(
            f"{'夏普比率':<20s} {old_result['sharpe']:<15.2f} {new_result['sharpe']:<15.2f} {new_result['sharpe'] - old_result['sharpe']:<+15.2f}"
        )
        print(
            f"{'胜率':<20s} {old_result['win']:<15.1%} {new_result['win']:<15.1%} {new_result['win'] - old_result['win']:<+15.1%}"
        )

        print()
        print("年度收益分解:")
        years = [2020, 2021, 2022, 2023, 2024]
        print(f"{'年份':<10s} {'旧池':<15s} {'新池':<15s} {'差异':<15s}")
        print("-" * 55)
        for year in years:
            try:
                old_mask = (old_result["rets"].index >= f"{year}-01-01") & (
                    old_result["rets"].index <= f"{year}-12-31"
                )
                new_mask = (new_result["rets"].index >= f"{year}-01-01") & (
                    new_result["rets"].index <= f"{year}-12-31"
                )

                old_year_ret = ((1 + old_result["rets"][old_mask]).prod() - 1) * 100
                new_year_ret = ((1 + new_result["rets"][new_mask]).prod() - 1) * 100
                diff = new_year_ret - old_year_ret

                print(
                    f"{year:<10d} {old_year_ret:>13.2f}% {new_year_ret:>13.2f}% {diff:>+13.2f}%"
                )
            except:
                print(f"{year:<10d} {'计算错误':<15s}")

    print()
    print("=" * 80)
    print()

    # ============================================================================
    # 七、关键发现总结
    # ============================================================================

    print("=" * 80)
    print("【七、关键发现总结】")
    print("=" * 80)
    print()

    if old_result and new_result:
        print("1. 回测结果对比:")
        print(f"   - 旧池年化收益: {old_result['ann']:.2%}")
        print(f"   - 新池年化收益: {new_result['ann']:.2%}")
        print(f"   - 差异: {new_result['ann'] - old_result['ann']:+.2%}")
        print()

        print("2. 相关性分析:")
        print(f"   - 旧池平均相关性: {old_avg_corr:.3f}")
        print(f"   - 新池平均相关性: {new_avg_corr:.3f}")
        if new_avg_corr > old_avg_corr:
            print(f"   ⚠️ 新池相关性更高，分散效果更差")
        else:
            print(f"   ✅ 新池相关性更低，分散效果更好")
        print()

        print("3. 波动率分析:")
        print(f"   - 旧池平均波动率: {old_avg_vol:.2f}%")
        print(f"   - 新池平均波动率: {new_avg_vol:.2f}%")
        if new_avg_vol > old_avg_vol:
            print(f"   ⚠️ 新池波动率更高，风险更大")
        else:
            print(f"   ✅ 新池波动率更低，风险更小")
        print()

        print("4. 初步结论:")
        if new_result["ann"] < old_result["ann"]:
            print("   ❌ 新池表现不如旧池")
            print("   可能原因:")
            print("   - 新池资产高度相关，缺乏分散化")
            print("   - 缺少跨市场对冲工具")
            print("   - 行业ETF波动更大，回撤更深")
        else:
            print("   ✅ 新池表现优于旧池")

    print()
    print("=" * 80)
    print()
    print("详细分析完成！请查看上方的具体数据。")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
