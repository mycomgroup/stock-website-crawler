# -*- coding: utf-8 -*-
"""
ML多因子测试 - RiceQuant版
"""

print("=" * 50)
print("ML多因子测试 (RiceQuant)")

import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# 获取交易日
dates = get_trading_dates("2024-07-01", "2024-12-31")
month_dates = []
last_m = None
for d in dates:
    if d.month != last_m:
        month_dates.append(d)
        last_m = d.month

print(f"调仓日期: {len(month_dates)}个月")

# 股票池
stocks = index_components("000905.XSHG")[:100]
print(f"股票池: {len(stocks)}只")

# 收集数据
data = {}
for i, d in enumerate(month_dates[:-1]):
    try:
        # 获取因子
        feat = get_factor(stocks, ["pe_ratio", "pb_ratio", "roe", "roa"], d, d)
        if feat is None or len(feat) < 30:
            continue

        feat = feat.iloc[0].to_frame().T if len(feat.shape) == 1 else feat
        feat = feat.replace([np.inf, -np.inf], np.nan).dropna()

        if len(feat) < 30:
            continue

        # 下月收益
        next_d = month_dates[i + 1]
        p0 = history_bars(feat.index.tolist(), 1, "1d", "close", end_date=str(d))
        p1 = history_bars(feat.index.tolist(), 1, "1d", "close", end_date=str(next_d))

        if p0 is None or p1 is None:
            continue

        # 计算收益
        ret = {}
        for s in feat.index:
            if s in p0 and s in p1 and len(p0[s]) > 0 and len(p1[s]) > 0:
                ret[s] = p1[s][-1] / p0[s][-1] - 1

        if len(ret) < 30:
            continue

        ret = pd.Series(ret)
        label = (ret > ret.median()).astype(int)

        data[i] = {"feat": feat, "label": label, "ret": ret}
        print(f"  {str(d)[:10]}: {len(feat)}只股票")

    except Exception as e:
        print(f"  {str(d)[:10]}: 错误 {e}")

print(f"\n有效数据: {len(data)}个月")

# Walk-Forward
if len(data) >= 4:
    print("\nWalk-Forward验证 (逻辑回归)...")

    idx = sorted(data.keys())
    rets = []

    for test_i in idx[2:]:
        train_i = [i for i in idx if i < test_i][-2:]

        X_train = pd.concat([data[i]["feat"] for i in train_i])
        y_train = pd.concat([data[i]["label"] for i in train_i])
        X_test = data[test_i]["feat"]
        ret_test = data[test_i]["ret"]

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train.fillna(0))
        X_test_s = scaler.transform(X_test.fillna(0))

        model = LogisticRegression(C=100, max_iter=200)
        model.fit(X_train_s, y_train)

        proba = model.predict_proba(X_test_s)[:, 1]
        selected = pd.Series(proba, index=X_test.index).nlargest(10).index
        available = [s for s in selected if s in ret_test.index]

        if available:
            net = ret_test.loc[available].mean() - 0.002
            rets.append(net)
            print(f"  月{test_i}: 选{len(available)}只, 收益={net:.2%}")

    if rets:
        s = pd.Series(rets)
        total = (1 + s).prod() - 1
        win = (s > 0).mean()

        print(f"\n结果: 累计={total:.2%}, 胜率={win:.1%}")

print("\n完成!")
