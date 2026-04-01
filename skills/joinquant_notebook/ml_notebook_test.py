# -*- coding: utf-8 -*-
"""
ML多因子Walk-Forward验证 - JoinQuant Notebook版
================================================
简化测试，快速验证
"""

print("=" * 60)
print("ML多因子Walk-Forward验证")
print("=" * 60)

from jqdata import *
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

try:
    from xgboost import XGBClassifier

    HAS_XGB = True
except:
    HAS_XGB = False
    print("XGBoost不可用")

# ============ 参数设置 ============
START = "2023-01-01"
END = "2025-12-31"
TRAIN_M = 6
HOLD_N = 20
COST = 0.001
FEATURES = ["pe_ratio", "pb_ratio", "roe", "roa", "market_cap"]


# ============ 工具函数 ============
def get_monthly_dates(start, end):
    days = get_trade_days(start, end)
    result, last_m = [], None
    for d in days:
        if d.month != last_m:
            result.append(d)
            last_m = d.month
    return result


print(f"\n参数: 训练窗口={TRAIN_M}月, 持仓={HOLD_N}只")
print(f"时间: {START} ~ {END}")

# ============ 获取调仓日期 ============
dates = get_monthly_dates(START, END)
print(f"调仓日期数: {len(dates)}")

# ============ 收集数据 ============
print("\n收集数据中...")
stocks = get_index_stocks("000905.XSHG")  # 中证500
print(f"股票池: {len(stocks)}只")

monthly_data = {}
success = 0

for i, d in enumerate(dates[:-1]):
    try:
        # 获取因子
        q = query(
            valuation.code,
            valuation.pe_ratio,
            valuation.pb_ratio,
            valuation.market_cap,
            indicator.roe,
            indicator.roa,
        ).filter(valuation.code.in_(stocks))

        feat = get_fundamentals(q, date=d)
        if feat is None or len(feat) < 50:
            continue

        feat = feat.set_index("code")
        feat = feat.replace([np.inf, -np.inf], np.nan).dropna()

        if len(feat) < 50:
            continue

        # 获取下月收益
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
            "feat": feat.loc[common, FEATURES],
            "label": label,
            "ret": ret.loc[common],
            "date": d,
        }
        success += 1

    except Exception as e:
        continue

print(f"成功收集: {success}个月")

if success < TRAIN_M + 3:
    print("数据不足!")
else:
    # ============ Walk-Forward验证 ============
    print("\n" + "=" * 60)
    print("Walk-Forward验证开始")
    print("=" * 60)

    models = {
        "逻辑回归": LogisticRegression(C=100, max_iter=300, random_state=42),
        "SVM": SVC(kernel="rbf", probability=True, C=1.0, random_state=42),
        "随机森林": RandomForestClassifier(
            n_estimators=50, max_depth=5, random_state=42
        ),
    }

    if HAS_XGB:
        models["XGBoost"] = XGBClassifier(
            n_estimators=50,
            max_depth=5,
            random_state=42,
            use_label_encoder=False,
            eval_metric="logloss",
        )

    valid_indices = sorted(monthly_data.keys())
    results = {name: [] for name in models}

    for test_idx in valid_indices[TRAIN_M:]:
        train_idx = [i for i in valid_indices if i < test_idx][-TRAIN_M:]

        if len(train_idx) < TRAIN_M:
            continue

        try:
            X_train = pd.concat([monthly_data[i]["feat"] for i in train_idx])
            y_train = pd.concat([monthly_data[i]["label"] for i in train_idx])
            X_test = monthly_data[test_idx]["feat"]
            ret_test = monthly_data[test_idx]["ret"]

            scaler = StandardScaler()
            X_train_s = scaler.fit_transform(X_train.fillna(0))
            X_test_s = scaler.transform(X_test.fillna(0))

            for name, model in models.items():
                try:
                    model.fit(X_train_s, y_train)
                    proba = model.predict_proba(X_test_s)[:, 1]
                    selected = (
                        pd.Series(proba, index=X_test.index).nlargest(HOLD_N).index
                    )
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

    # ============ 结果汇总 ============
    print("\n" + "=" * 60)
    print("【验证结果】")
    print("=" * 60)

    summary = []
    for name, rets in results.items():
        if not rets:
            continue

        s = pd.Series(rets)
        cum = (1 + s).cumprod()

        months = len(s)
        ann = cum.iloc[-1] ** (12 / months) - 1
        dd = (cum / cum.cummax() - 1).min()
        sharpe = s.mean() / s.std() * (12**0.5) if s.std() > 0 else 0
        win = (s > 0).mean()

        print(f"\n{name}:")
        print(f"  年化收益: {ann:.2%}")
        print(f"  最大回撤: {dd:.2%}")
        print(f"  夏普比率: {sharpe:.3f}")
        print(f"  月胜率: {win:.1%}")
        print(f"  样本月数: {months}")

        summary.append({"模型": name, "年化收益": ann, "夏普": sharpe, "胜率": win})

    # ============ 结论 ============
    print("\n" + "=" * 60)
    print("【结论】")
    print("=" * 60)

    df_summary = pd.DataFrame(summary)
    best = df_summary.loc[df_summary["夏普"].idxmax(), "模型"]
    worst = df_summary.loc[df_summary["夏普"].idxmin(), "模型"]
    best_sharpe = df_summary["夏普"].max()

    print(f"最佳模型: {best} (夏普={best_sharpe:.3f})")
    print(f"最差模型: {worst}")

    if best_sharpe > 0.8:
        print("\n结论: 夏普>0.8，值得考虑")
    elif best_sharpe > 0.3:
        print("\n结论: 夏普0.3-0.8，需要进一步研究")
    elif best_sharpe > 0:
        print("\n结论: 夏普>0但<0.3，优势不明显")
    else:
        print("\n结论: 夏普<0，暂不值得")

print("\n" + "=" * 60)
print("验证完成!")
print("=" * 60)
