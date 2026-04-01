# -*- coding: utf-8 -*-
"""ML多因子快速测试 - 极简版"""

print("=" * 50)
print("ML多因子快速测试")

from jqdata import *
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# 只测试最近6个月
dates = get_trade_days("2024-07-01", "2024-12-31")
month_dates = []
last_m = None
for d in dates:
    if d.month != last_m:
        month_dates.append(d)
        last_m = d.month

print(f"调仓日期: {len(month_dates)}个月")

# 股票池
stocks = get_index_stocks("000905.XSHG")[:100]
print(f"股票池: {len(stocks)}只")

# 收集数据
data = {}
for i, d in enumerate(month_dates[:-1]):
    try:
        q = query(
            valuation.code,
            valuation.pe_ratio,
            valuation.pb_ratio,
            indicator.roe,
            indicator.roa,
        ).filter(valuation.code.in_(stocks))

        feat = get_fundamentals(q, date=d).set_index("code")
        feat = feat.replace([np.inf, -np.inf], np.nan).dropna()

        if len(feat) < 30:
            continue

        # 下月收益
        p0 = get_price(
            feat.index.tolist(), end_date=str(d), count=1, fields=["close"], panel=False
        )
        p1 = get_price(
            feat.index.tolist(),
            end_date=str(month_dates[i + 1]),
            count=1,
            fields=["close"],
            panel=False,
        )

        if p0 is None or p1 is None:
            continue

        r0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
        r1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
        ret = ((r1 / r0) - 1).dropna()

        common = feat.index.intersection(ret.index)
        if len(common) < 30:
            continue

        label = (ret.loc[common] > ret.loc[common].median()).astype(int)

        data[i] = {"feat": feat.loc[common], "label": label, "ret": ret.loc[common]}
        print(f"  {str(d)[:10]}: {len(common)}只股票")
    except Exception as e:
        print(f"  {str(d)[:10]}: 错误 {e}")

print(f"\n有效数据: {len(data)}个月")

# Walk-Forward
if len(data) >= 4:
    print("\nWalk-Forward验证...")

    idx = sorted(data.keys())
    rets = []

    for test_i in idx[2:]:  # 用2个月训练
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
            print(f"  测试月{test_i}: 选{len(available)}只, 收益={net:.2%}")

    if rets:
        s = pd.Series(rets)
        cum = (1 + s).cumprod()
        total = cum.iloc[-1] - 1
        win = (s > 0).mean()

        print(f"\n结果: 累计收益={total:.2%}, 胜率={win:.1%}")

print("\n完成!")
