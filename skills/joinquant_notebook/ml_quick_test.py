# -*- coding: utf-8 -*-
"""
ML多因子Walk-Forward验证 - 聚宽简化版
======================================
快速验证，减少数据量
"""

from jqdata import *
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

print("=" * 70)
print("ML多因子Walk-Forward验证 (简化版)")
print("=" * 70)

# 参数
START = "2022-01-01"
END = "2025-12-31"
TRAIN_M = 6  # 6个月训练窗口
HOLD_N = 20
COST = 0.001

FEATURE_COLS = [
    "pe_ratio",
    "pb_ratio",
    "roe",
    "roa",
    "gross_profit_margin",
    "inc_net_profit_year_on_year",
]


def get_monthly_dates(start, end):
    days = get_trade_days(start, end)
    result, last_m = [], None
    for d in days:
        if d.month != last_m:
            result.append(d)
            last_m = d.month
    return result


dates = get_monthly_dates(START, END)
print(f"调仓日期数: {len(dates)}")

# 收集数据
print("收集数据...")
monthly_data = {}
stocks = get_index_stocks("000905.XSHG")[:200]  # 只用200只加速

for i, d in enumerate(dates[:-1]):
    try:
        q = query(
            valuation.code,
            valuation.pe_ratio,
            valuation.pb_ratio,
            indicator.roe,
            indicator.roa,
            indicator.gross_profit_margin,
            indicator.inc_net_profit_year_on_year,
        ).filter(valuation.code.in_(stocks))

        feat = get_fundamentals(q, date=d).set_index("code")
        feat = feat.replace([np.inf, -np.inf], np.nan).dropna()

        if len(feat) < 50:
            continue

        # 下月收益
        p0 = get_price(
            feat.index.tolist(), end_date=str(d), count=1, fields=["close"], panel=False
        )
        p1 = get_price(
            feat.index.tolist(),
            end_date=str(dates[i + 1]),
            count=1,
            fields=["close"],
            panel=False,
        )

        if p0 is None or p1 is None:
            continue

        ret0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
        ret1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
        ret = ((ret1 / ret0) - 1).dropna()

        common = feat.index.intersection(ret.index)
        if len(common) < 50:
            continue

        label = (ret.loc[common] > ret.loc[common].median()).astype(int)

        monthly_data[i] = {
            "feat": feat.loc[common, FEATURE_COLS],
            "label": label,
            "ret": ret.loc[common],
            "date": d,
        }
    except:
        continue

print(f"有效月份: {len(monthly_data)}")

# Walk-Forward验证
models = {
    "逻辑回归": LogisticRegression(C=100, max_iter=300, random_state=42),
    "SVM": SVC(kernel="rbf", probability=True, C=1.0, random_state=42),
    "随机森林": RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42),
}

valid_indices = sorted(monthly_data.keys())
results = {name: [] for name in models}

print(f"\nWalk-Forward验证 (训练窗口={TRAIN_M}个月)...")

for test_idx in valid_indices[TRAIN_M:]:
    train_indices = [i for i in valid_indices if i < test_idx][-TRAIN_M:]

    if len(train_indices) < TRAIN_M:
        continue

    try:
        X_train = pd.concat([monthly_data[i]["feat"] for i in train_indices])
        y_train = pd.concat([monthly_data[i]["label"] for i in train_indices])
        X_test = monthly_data[test_idx]["feat"]
        ret_test = monthly_data[test_idx]["ret"]

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train.fillna(0))
        X_test_s = scaler.transform(X_test.fillna(0))

        for name, model in models.items():
            try:
                model.fit(X_train_s, y_train)
                proba = model.predict_proba(X_test_s)[:, 1]

                selected = pd.Series(proba, index=X_test.index).nlargest(HOLD_N).index
                available = [s for s in selected if s in ret_test.index]

                if available:
                    net = ret_test.loc[available].mean() - COST * 2
                    results[name].append(net)
                else:
                    results[name].append(0.0)
            except:
                results[name].append(0.0)
    except:
        for name in models:
            results[name].append(0.0)

# 结果
print("\n" + "=" * 70)
print("【验证结果】")
print("=" * 70)

for name, rets in results.items():
    if not rets:
        continue
    s = pd.Series(rets)
    cum = (1 + s).cumprod()
    ann = cum.iloc[-1] ** (12 / len(s)) - 1
    dd = (cum / cum.cummax() - 1).min()
    sharpe = s.mean() / s.std() * (12**0.5) if s.std() > 0 else 0
    win = (s > 0).mean()

    print(f"{name}: 年化={ann:.2%}, 回撤={dd:.2%}, 夏普={sharpe:.3f}, 胜率={win:.1%}")

# 结论
best = max(
    results.keys(),
    key=lambda x: pd.Series(results[x]).mean() / pd.Series(results[x]).std()
    if pd.Series(results[x]).std() > 0
    else -999,
)

print(f"\n最佳模型: {best}")
print("验证完成!")
