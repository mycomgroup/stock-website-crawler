# -*- coding: utf-8 -*-
"""
ML多因子快速验证 - 极简版
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

print("ML多因子快速验证")
print("=" * 50)

# 只验证最近2年，每季度调仓
dates = get_trade_days("2023-01-01", "2025-12-31")
quarter_dates = []
last_q = None
for d in dates:
    q = (d.month - 1) // 3
    if q != last_q:
        quarter_dates.append(d)
        last_q = q

print(f"调仓日期: {len(quarter_dates)}个季度")

stocks = get_index_stocks("000905.XSHG")[:100]  # 只用100只
results = {"逻辑回归": [], "SVM": [], "随机森林": []}

for i in range(2, len(quarter_dates) - 1):
    train_dates = quarter_dates[i - 2 : i]
    test_date = quarter_dates[i]
    next_date = quarter_dates[i + 1] if i + 1 < len(quarter_dates) else None

    if next_date is None:
        break

    print(f"\n训练: {[str(d)[:10] for d in train_dates]}")
    print(f"测试: {str(test_date)[:10]} -> {str(next_date)[:10]}")

    # 收集训练数据
    X_train_list, y_train_list = [], []

    for td in train_dates:
        try:
            q = query(
                valuation.code,
                valuation.pe_ratio,
                valuation.pb_ratio,
                indicator.roe,
                indicator.roa,
            ).filter(valuation.code.in_(stocks))

            feat = get_fundamentals(q, date=td).set_index("code")
            feat = feat.replace([np.inf, -np.inf], np.nan).dropna()

            if len(feat) < 30:
                continue

            # 获取下期收益作为标签
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

            ret0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            ret1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
            ret = ((ret1 / ret0) - 1).dropna()

            common = feat.index.intersection(ret.index)
            if len(common) < 30:
                continue

            label = (ret.loc[common] > ret.loc[common].median()).astype(int)
            X_train_list.append(feat.loc[common])
            y_train_list.append(label)
        except:
            continue

    if not X_train_list:
        print("  训练数据不足，跳过")
        continue

    X_train = pd.concat(X_train_list).fillna(0)
    y_train = pd.concat(y_train_list)

    # 测试数据
    try:
        q = query(
            valuation.code,
            valuation.pe_ratio,
            valuation.pb_ratio,
            indicator.roe,
            indicator.roa,
        ).filter(valuation.code.in_(stocks))

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

        ret0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
        ret1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
        ret = ((ret1 / ret0) - 1).dropna()

        common = X_test.index.intersection(ret.index)
        X_test = X_test.loc[common].fillna(0)
        ret = ret.loc[common]
    except:
        print("  测试数据获取失败")
        continue

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
            selected = pd.Series(proba, index=X_test.index).nlargest(10).index
            available = [s for s in selected if s in ret.index]

            if available:
                gross = ret.loc[available].mean()
                net = gross - 0.002  # 双边成本
                results[name].append(net)
                print(f"  {name}: 选股{len(available)}只, 收益={net:.2%}")
            else:
                results[name].append(0.0)
                print(f"  {name}: 无有效选股")
        except Exception as e:
            results[name].append(0.0)
            print(f"  {name}: 错误 - {e}")

# 汇总
print("\n" + "=" * 50)
print("【汇总结果】")
print("=" * 50)

for name, rets in results.items():
    if not rets:
        continue
    s = pd.Series(rets)
    total = (1 + s).cumprod().iloc[-1] - 1
    win = (s > 0).mean()
    avg = s.mean()
    print(f"{name}: 累计={total:.2%}, 胜率={win:.1%}, 季均={avg:.2%}")

print("\n验证完成!")
