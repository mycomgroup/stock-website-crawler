# -*- coding: utf-8 -*-
"""
ML多因子验证 - 修复幸存者偏差版本
===================================
修复点:
1. 每个调仓日使用历史时点的中证500成分股
2. 添加ST/次新股过滤
3. 固定排序规则（按股票代码排序）
4. 扩展测试期至2020-2025
5. 训练窗口扩展至6个季度
6. 添加基准对比（中证500等权）
"""

from jqdata import *
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings("ignore")

print("ML多因子验证 - 修复幸存者偏差版")
print("=" * 60)


def get_pool_at_date(date):
    """获取历史时点的中证500成分股，排除ST和次新股"""
    stocks = get_index_stocks("000905.XSHG", date=date)
    # 排除上市不足180天
    valid = []
    for s in stocks:
        try:
            info = get_security_info(s)
            if info and (date - info.start_date).days > 180:
                valid.append(s)
        except:
            continue
    # 排除ST
    if valid:
        try:
            is_st = get_extras("is_st", valid, end_date=date, count=1)
            valid = [s for s in valid if not is_st[s][0]]
        except:
            pass
    # 固定排序
    valid.sort()
    return valid[:100]


# 参数
START_DATE = "2020-01-01"
END_DATE = "2025-12-31"
TRAIN_QUARTERS = 6  # 修复：从2季扩展到6季
HOLD_N = 10
COST = 0.002  # 双边成本

# 获取季度调仓日
dates = get_trade_days(START_DATE, END_DATE)
quarter_dates = []
last_q = None
for d in dates:
    q = (d.year, (d.month - 1) // 3)
    if q != last_q:
        quarter_dates.append(d)
        last_q = q

print(f"调仓日期: {len(quarter_dates)}个季度")
print(f"季度列表: {[str(d)[:10] for d in quarter_dates]}")

results = {"逻辑回归": [], "SVM": [], "随机森林": []}
benchmark_rets = []  # 中证500等权基准
quarter_labels = []

for i in range(TRAIN_QUARTERS, len(quarter_dates) - 1):
    train_dates = quarter_dates[i - TRAIN_QUARTERS : i]
    test_date = quarter_dates[i]
    next_date = quarter_dates[i + 1]

    print(f"\n--- 测试: {str(test_date)[:10]} -> {str(next_date)[:10]} ---")

    # 修复：使用历史时点股票池
    test_stocks = get_pool_at_date(test_date)
    print(f"  测试期股票池: {len(test_stocks)}只 (历史时点成分股)")
    quarter_labels.append(f"{test_date.year}-Q{(test_date.month - 1) // 3 + 1}")

    # 收集训练数据
    X_train_list, y_train_list = [], []

    for td in train_dates:
        try:
            # 修复：使用历史时点股票池
            train_stocks = get_pool_at_date(td)

            q = query(
                valuation.code,
                valuation.pe_ratio,
                valuation.pb_ratio,
                indicator.roe,
                indicator.roa,
            ).filter(valuation.code.in_(train_stocks))

            feat = get_fundamentals(q, date=td).set_index("code")
            feat = feat.replace([np.inf, -np.inf], np.nan).dropna()

            if len(feat) < 30:
                continue

            # 获取下期收益
            idx = quarter_dates.index(td)
            if idx + 1 >= len(quarter_dates):
                continue
            next_td = quarter_dates[idx + 1]

            p0 = get_price(
                feat.index.tolist(),
                end_date=str(td),
                count=1,
                fields=["close"],
                panel=False,
            )
            p1 = get_price(
                feat.index.tolist(),
                end_date=str(next_td),
                count=1,
                fields=["close"],
                panel=False,
            )

            if p0 is None or p1 is None or len(p0) == 0 or len(p1) == 0:
                continue

            ret0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            ret1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
            ret = ((ret1 / ret0) - 1).dropna()

            common = feat.index.intersection(ret.index)
            if len(common) < 30:
                continue

            label = (ret.loc[common] > ret.loc[common].median()).astype(int)
            X_train_list.append(feat.loc[common])
            y_train_list.append(label)
        except Exception as e:
            continue

    if not X_train_list:
        print("  训练数据不足，跳过")
        continue

    X_train = pd.concat(X_train_list).fillna(0)
    y_train = pd.concat(y_train_list)
    print(f"  训练样本: {len(X_train)}条, 来自{len(train_dates)}个季度")

    # 测试数据
    try:
        q = query(
            valuation.code,
            valuation.pe_ratio,
            valuation.pb_ratio,
            indicator.roe,
            indicator.roa,
        ).filter(valuation.code.in_(test_stocks))

        X_test = get_fundamentals(q, date=test_date).set_index("code")
        X_test = X_test.replace([np.inf, -np.inf], np.nan).dropna()

        p0 = get_price(
            X_test.index.tolist(),
            end_date=str(test_date),
            count=1,
            fields=["close"],
            panel=False,
        )
        p1 = get_price(
            X_test.index.tolist(),
            end_date=str(next_date),
            count=1,
            fields=["close"],
            panel=False,
        )

        if p0 is None or p1 is None or len(p0) == 0 or len(p1) == 0:
            print("  价格数据为空，跳过")
            continue

        ret0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
        ret1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
        ret = ((ret1 / ret0) - 1).dropna()

        common = X_test.index.intersection(ret.index)
        X_test = X_test.loc[common].fillna(0)
        ret = ret.loc[common]
    except Exception as e:
        print(f"  测试数据获取失败: {e}")
        continue

    # 基准收益（中证500等权）
    bench_ret = ret.mean() - COST
    benchmark_rets.append(bench_ret)
    print(f"  基准(中证500等权): {bench_ret:.2%}")

    # 标准化
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    # 模型
    models = {
        "逻辑回归": LogisticRegression(C=100, max_iter=200, random_state=42),
        "SVM": SVC(kernel="rbf", probability=True, C=1.0, random_state=42),
        "随机森林": RandomForestClassifier(
            n_estimators=50, max_depth=3, random_state=42
        ),
    }

    for name, model in models.items():
        try:
            model.fit(X_train_s, y_train)
            proba = model.predict_proba(X_test_s)[:, 1]
            selected = pd.Series(proba, index=X_test.index).nlargest(HOLD_N).index
            available = [s for s in selected if s in ret.index]

            if available:
                gross = ret.loc[available].mean()
                net = gross - COST
                results[name].append(net)
                excess = net - bench_ret
                print(
                    f"  {name}: 选股{len(available)}只, 收益={net:.2%}, 超额={excess:.2%}"
                )
            else:
                results[name].append(0.0)
                print(f"  {name}: 无有效选股")
        except Exception as e:
            results[name].append(0.0)
            print(f"  {name}: 错误 - {e}")

# 汇总
print("\n" + "=" * 60)
print("【汇总结果 - 修复幸存者偏差版】")
print("=" * 60)

# 基准汇总
bench_series = pd.Series(benchmark_rets)
bench_cum = (1 + bench_series).cumprod().iloc[-1] - 1
bench_win = (bench_series > 0).mean()
print(f"\n基准(中证500等权): 累计={bench_cum:.2%}, 胜率={bench_win:.1%}")

# 季度明细
print(f"\n{'季度':<12} {'基准':>8} {'逻辑回归':>10} {'SVM':>8} {'随机森林':>10}")
print("-" * 60)
for idx, ql in enumerate(quarter_labels):
    bench_str = f"{benchmark_rets[idx]:.2%}" if idx < len(benchmark_rets) else "N/A"
    lr_str = (
        f"{results['逻辑回归'][idx]:.2%}" if idx < len(results["逻辑回归"]) else "N/A"
    )
    svm_str = f"{results['SVM'][idx]:.2%}" if idx < len(results["SVM"]) else "N/A"
    rf_str = (
        f"{results['随机森林'][idx]:.2%}" if idx < len(results["随机森林"]) else "N/A"
    )
    print(f"{ql:<12} {bench_str:>8} {lr_str:>10} {svm_str:>8} {rf_str:>10}")

for name, rets in results.items():
    if not rets:
        continue
    s = pd.Series(rets)
    total = (1 + s).cumprod().iloc[-1] - 1
    win = (s > 0).mean()
    avg = s.mean()
    ann = (1 + total) ** (4 / len(s)) - 1
    sharpe = s.mean() / s.std() * 2 if s.std() > 0 else 0
    max_dd = ((1 + s).cumprod() / (1 + s).cumprod().cummax() - 1).min()

    # 信息比率
    bench_aligned = pd.Series(benchmark_rets[: len(s)])
    excess = s - bench_aligned
    ir = excess.mean() / excess.std() * 2 if excess.std() > 0 else 0

    print(f"\n{name}:")
    print(f"  累计收益: {total:.2%}")
    print(f"  年化收益: {ann:.2%}")
    print(f"  季度胜率: {win:.1%} ({int((s > 0).sum())}/{len(s)})")
    print(f"  季均收益: {avg:.2%}")
    print(f"  夏普比率: {sharpe:.3f}")
    print(f"  信息比率: {ir:.3f}")
    print(f"  最大回撤: {max_dd:.2%}")

print("\n验证完成!")
