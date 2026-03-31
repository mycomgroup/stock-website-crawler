"""
Step 2: 因子有效性测试

目标：找出对小市值股票收益预测最有效的因子
方法：单因子IC测试、因子收益预测能力分析

RiceQuant Notebook 运行方式：
node run-strategy.js --strategy step2_factor_test.py --timeout-ms 600000
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

print("=" * 60)
print("Step 2: 因子有效性测试")
print("=" * 60)

# ============================================================
# 1. 定义因子池
# ============================================================
print("\n[1. 因子池定义]")

"""
基于聚宽策略分析，重点测试以下因子：

估值类因子：
- PE（市盈率）：低PE股票可能被低估
- PB（市净率）：低PB股票可能被低估
- PS（市销率）：低PS股票可能被低估

质量类因子：
- ROE（净资产收益率）：高ROE代表公司质量好
- ROA（总资产收益率）：高ROA代表资产效率高
- 毛利率：高毛利率代表竞争力强

成长类因子：
- 营收增长率：高增长代表公司成长性好
- 净利润增长率：利润增长代表盈利能力提升

技术类因子：
- 换手率：适度换手率代表活跃度
- 动量：近期涨幅代表趋势
- MA乖离率：偏离均线程度
"""


# 定义因子计算函数
def calc_momentum(close_prices, period=20):
    """计算动量因子"""
    if len(close_prices) < period:
        return None
    return (close_prices[-1] / close_prices[0] - 1) * 100


def calc_ma_deviation(close_prices, period=20):
    """计算MA乖离率"""
    if len(close_prices) < period:
        return None
    ma = np.mean(close_prices)
    if ma == 0:
        return None
    return (close_prices[-1] / ma - 1) * 100


def calc_volatility(close_prices, period=20):
    """计算波动率"""
    if len(close_prices) < period:
        return None
    returns = np.diff(close_prices) / close_prices[:-1]
    return np.std(returns) * 100


def calc_volume_ratio(volumes, period=20):
    """计算量比"""
    if len(volumes) < period:
        return None
    recent_vol = np.mean(volumes[-5:])
    total_vol = np.mean(volumes)
    if total_vol == 0:
        return None
    return recent_vol / total_vol


# ============================================================
# 2. 获取测试股票池
# ============================================================
print("\n[2. 获取测试股票池]")

test_stocks = []
try:
    # RiceQuant: 获取沪深300+中证500成分股作为测试
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")

    # 合并并去重
    test_stocks = list(set(hs300) | set(zz500))

    # 过滤掉科创北交
    test_stocks = [
        s
        for s in test_stocks
        if not s.startswith("688") and not s.startswith("8") and not s.startswith("4")
    ]

    print(f"测试股票池数量: {len(test_stocks)}")
    print(f"（使用沪深300+中证500成分股进行因子测试）")

except Exception as e:
    print(f"获取股票池失败: {e}")
    test_stocks = []

# ============================================================
# 3. 计算因子值
# ============================================================
print("\n[3. 计算因子值]")

factor_results = []

if test_stocks:
    # 限制数量避免超时
    sample_stocks = test_stocks[:100]

    print(f"对{len(sample_stocks)}只股票计算因子...")

    for i, stock in enumerate(sample_stocks):
        if i % 20 == 0:
            print(f"  处理进度: {i}/{len(sample_stocks)}")

        try:
            # 获取历史数据
            bars = history_bars(stock, 60, "1d", ["close", "volume"])

            if bars is None or len(bars) < 40:
                continue

            close = bars["close"]
            volume = bars["volume"]

            # 计算因子
            momentum_20 = calc_momentum(close, 20)
            ma_deviation = calc_ma_deviation(close, 20)
            volatility = calc_volatility(close, 20)
            volume_ratio = calc_volume_ratio(volume, 20)

            # 计算未来收益（用于IC测试）
            # 用后5天收益作为目标
            if len(close) >= 25:
                future_return = (close[-1] / close[-6] - 1) * 100
            else:
                future_return = None

            if all(
                v is not None
                for v in [momentum_20, ma_deviation, volatility, volume_ratio]
            ):
                factor_results.append(
                    {
                        "code": stock,
                        "momentum_20": momentum_20,
                        "ma_deviation": ma_deviation,
                        "volatility": volatility,
                        "volume_ratio": volume_ratio,
                        "future_return": future_return,
                    }
                )

        except Exception as e:
            continue

# ============================================================
# 4. 因子IC计算
# ============================================================
print("\n[4. 因子IC计算]")

if factor_results:
    df = pd.DataFrame(factor_results)

    # 过滤掉未来收益为空的记录
    df = df.dropna(subset=["future_return"])

    print(f"\n有效样本数: {len(df)}")

    # 计算IC（Information Coefficient）
    # IC = 因子值与未来收益的相关系数
    ic_results = {}

    factor_names = ["momentum_20", "ma_deviation", "volatility", "volume_ratio"]

    for factor in factor_names:
        if factor in df.columns:
            corr = df[factor].corr(df["future_return"])
            ic_results[factor] = corr

            # 判断IC强弱
            abs_corr = abs(corr)
            if abs_corr >= 0.05:
                strength = "强"
            elif abs_corr >= 0.03:
                strength = "中"
            else:
                strength = "弱"

            direction = "正" if corr > 0 else "负"

            print(f"  {factor:20s}: IC = {corr:+.4f} ({strength}, {direction}相关)")

    # 排序
    print("\n因子IC排序（绝对值）:")
    sorted_ic = sorted(ic_results.items(), key=lambda x: abs(x[1]), reverse=True)
    for i, (factor, ic) in enumerate(sorted_ic, 1):
        print(f"  {i}. {factor}: {ic:+.4f}")

# ============================================================
# 5. 因子分组收益测试
# ============================================================
print("\n[5. 因子分组收益测试]")

if factor_results and len(df) > 0:
    # 对动量因子进行分组测试
    print("\n动量因子分组收益测试:")

    try:
        # 按动量因子分组
        df["momentum_group"] = pd.qcut(
            df["momentum_20"], 5, labels=["最低", "低", "中", "高", "最高"]
        )

        # 计算各组平均收益
        group_returns = df.groupby("momentum_group")["future_return"].mean()

        print("\n分组收益:")
        for group in ["最低", "低", "中", "高", "最高"]:
            if group in group_returns.index:
                ret = group_returns[group]
                print(f"  {group}: {ret:+.2f}%")

        # 最高组 vs 最低组
        if "最高" in group_returns.index and "最低" in group_returns.index:
            spread = group_returns["最高"] - group_returns["最低"]
            print(f"\n多空收益差: {spread:+.2f}%")

    except Exception as e:
        print(f"分组测试失败: {e}")

# ============================================================
# 6. 因子相关性分析
# ============================================================
print("\n[6. 因子相关性分析]")

if factor_results and len(df) > 0:
    # 计算因子间相关系数
    factor_cols = ["momentum_20", "ma_deviation", "volatility", "volume_ratio"]
    factor_df = df[factor_cols]

    corr_matrix = factor_df.corr()

    print("\n因子相关性矩阵:")
    print(corr_matrix.round(3).to_string())

    # 找出高相关因子对
    print("\n高相关因子对（|相关性| > 0.5）:")
    for i in range(len(factor_cols)):
        for j in range(i + 1, len(factor_cols)):
            f1, f2 = factor_cols[i], factor_cols[j]
            corr = corr_matrix.loc[f1, f2]
            if abs(corr) > 0.5:
                print(f"  {f1} <-> {f2}: {corr:.3f}")

# ============================================================
# 7. 验证结论
# ============================================================
print("\n" + "=" * 60)
print("[验证结论]")
print("=" * 60)

if ic_results:
    # 找出最有效因子
    best_factor = max(ic_results.items(), key=lambda x: abs(x[1]))

    print(f"""
因子有效性测试完成：

1. 最有效因子：
   - {best_factor[0]}: IC = {best_factor[1]:+.4f}

2. 因子有效性排序：
""")

    sorted_ic = sorted(ic_results.items(), key=lambda x: abs(x[1]), reverse=True)
    for i, (factor, ic) in enumerate(sorted_ic, 1):
        status = "✓ 可用" if abs(ic) >= 0.03 else "✗ 效果弱"
        print(f"   {i}. {factor}: {ic:+.4f} {status}")

    print(f"""
3. 下一步建议：
   - Step3: 使用有效因子构建机器学习模型
   - 重点使用: {", ".join([f[0] for f in sorted_ic if abs(f[1]) >= 0.03])}
   - 注意因子相关性，避免共线性

4. 注意事项：
   - IC值较低可能与样本数量、时间段有关
   - 需要更长时间段的数据验证
   - 建议在策略编辑器中进行完整回测
""")
else:
    print("因子测试失败，请检查数据获取")

print("\n" + "=" * 60)
print("Step 2 完成")
print("=" * 60)
