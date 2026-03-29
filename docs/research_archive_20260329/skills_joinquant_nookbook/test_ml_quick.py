#!/usr/bin/env python3
"""
机器学习多因子快速验证 - 简化版
==========================================
测试期：2024-01 至 2025-03 (15个月)
训练窗口：滚动12个月
"""

import pandas as pd
import numpy as np
from jqdata import *
from jqfactor import *
import datetime
import warnings

warnings.filterwarnings("ignore")

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

print("=" * 70)
print("机器学习多因子 - 快速验证")
print("=" * 70)

# 参数设置
INDEX = "000905.XSHG"
START_DATE = "2023-01-01"
END_DATE = "2025-03-31"
TRAIN_WINDOW = 12

FEATURE_COLS = [
    "EP",
    "BP",
    "SP",
    "CFP",
    "pe_ratio",
    "pb_ratio",
    "roe",
    "roa",
    "gross_profit_margin",
    "net_profit_to_total_revenue",
    "inc_net_profit_year_on_year",
    "inc_revenue_year_on_year",
    "log_market_cap",
]

print(f"测试区间: {START_DATE} - {END_DATE}")
print(f"训练窗口: {TRAIN_WINDOW} 个月")
print(f"股票池: 中证500")
print(f"特征数: {len(FEATURE_COLS)}")


# 工具函数
def get_stocks_filtered(date):
    stocks = get_index_stocks(INDEX, date=date)
    is_st = get_extras("is_st", stocks, end_date=date, count=1)
    stocks = [s for s in stocks if not is_st[s][0]]
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    stocks = [
        s
        for s in stocks
        if get_security_info(s).start_date
        < (date_obj - datetime.timedelta(days=365)).date()
    ]
    paused = get_price(stocks, end_date=date, count=1, fields="paused", panel=False)
    stocks = list(paused[paused["paused"] != 1]["code"])
    return stocks


def get_features(stocks, date):
    q = query(
        valuation.code,
        valuation.pe_ratio,
        valuation.pb_ratio,
        valuation.pcf_ratio,
        valuation.ps_ratio,
        valuation.market_cap,
        indicator.roe,
        indicator.roa,
        indicator.gross_profit_margin,
        indicator.net_profit_to_total_revenue,
        indicator.inc_net_profit_year_on_year,
        indicator.inc_revenue_year_on_year,
    ).filter(valuation.code.in_(stocks))
    df = get_fundamentals(q, date=date)
    df.set_index("code", inplace=True)
    df["EP"] = 1 / df["pe_ratio"].replace(0, np.nan)
    df["BP"] = 1 / df["pb_ratio"].replace(0, np.nan)
    df["SP"] = 1 / df["ps_ratio"].replace(0, np.nan)
    df["CFP"] = 1 / df["pcf_ratio"].replace(0, np.nan)
    df["log_market_cap"] = np.log(df["market_cap"])
    return df[FEATURE_COLS].dropna()


def get_forward_return(stocks, start_date, end_date):
    returns = {}
    for stock in stocks:
        try:
            prices = get_price(
                stock, start_date=start_date, end_date=end_date, fields=["close"]
            )
            if len(prices) >= 2:
                returns[stock] = prices["close"].iloc[-1] / prices["close"].iloc[0] - 1
        except:
            pass
    return pd.Series(returns)


def process_features(train_df, test_df):
    clip_params = {}
    for col in train_df.columns:
        q1 = train_df[col].quantile(0.01)
        q99 = train_df[col].quantile(0.99)
        clip_params[col] = (q1, q99)
        train_df[col] = train_df[col].clip(q1, q99)
    for col in test_df.columns:
        if col in clip_params:
            test_df[col] = test_df[col].clip(clip_params[col][0], clip_params[col][1])
    scaler = StandardScaler()
    train_scaled = pd.DataFrame(
        scaler.fit_transform(train_df), index=train_df.index, columns=train_df.columns
    )
    test_scaled = pd.DataFrame(
        scaler.transform(test_df), index=test_df.index, columns=test_df.columns
    )
    return train_scaled.fillna(0), test_scaled.fillna(0)


def create_labels(returns_series, top_pct=0.3, bottom_pct=0.3):
    returns_sorted = returns_series.sort_values(ascending=False)
    n = len(returns_sorted)
    top_n = int(n * top_pct)
    bottom_n = int(n * bottom_pct)
    labels = pd.Series(np.nan, index=returns_sorted.index)
    labels.iloc[:top_n] = 1
    labels.iloc[-bottom_n:] = 0
    return labels.dropna()


def calc_rfscore(features_df):
    df = features_df.copy()
    df["fscore"] = 0
    df.loc[df["roe"] > 0, "fscore"] += 1
    df.loc[df["roa"] > 0, "fscore"] += 1
    df.loc[df["gross_profit_margin"] > 30, "fscore"] += 1
    df.loc[df["inc_net_profit_year_on_year"] > 0, "fscore"] += 1
    df.loc[df["inc_revenue_year_on_year"] > 0, "fscore"] += 1
    df.loc[(df["pe_ratio"] > 0) & (df["pe_ratio"] < 30), "fscore"] += 1
    df.loc[df["pb_ratio"] < 5, "fscore"] += 1
    return df["fscore"]


# 获取交易日
trade_days = get_trade_days(START_DATE, END_DATE)
month_ends = []
for i in range(len(trade_days) - 1):
    if trade_days[i].month != trade_days[i + 1].month:
        month_ends.append(trade_days[i].strftime("%Y-%m-%d"))

print(f"\n总月数: {len(month_ends)}")
print(f"可用测试月: {len(month_ends) - TRAIN_WINDOW} 个月\n")

# 模型定义
models = {
    "Logistic": LogisticRegression(C=100, max_iter=500, random_state=42),
    "SVM": SVC(probability=True, kernel="rbf", C=1.0, random_state=42),
    "RandomForest": RandomForestClassifier(
        n_estimators=100, max_depth=5, random_state=42
    ),
    "XGBoost": xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss",
    ),
}

# 结果存储
all_results = {
    "Logistic": [],
    "SVM": [],
    "RandomForest": [],
    "XGBoost": [],
    "RFScore": [],
}
all_benchmark = []

print("开始滚动验证...")
print("-" * 70)

# 滚动验证
for test_idx in range(TRAIN_WINDOW, len(month_ends)):
    test_date = month_ends[test_idx]
    train_dates = month_ends[test_idx - TRAIN_WINDOW : test_idx]

    print(
        f"\n[测试 {test_idx - TRAIN_WINDOW + 1}/{len(month_ends) - TRAIN_WINDOW}] {test_date}"
    )

    try:
        # 训练数据
        train_features_list, train_labels_list = [], []
        for i, train_date in enumerate(train_dates[:-1]):
            try:
                stocks = get_stocks_filtered(train_date)
                if len(stocks) < 50:
                    continue
                features = get_features(stocks, train_date)
                next_date = train_dates[i + 1]
                returns = get_forward_return(
                    features.index.tolist(), train_date, next_date
                )
                labels = create_labels(returns)
                common_stocks = features.index.intersection(labels.index)
                if len(common_stocks) > 20:
                    train_features_list.append(features.loc[common_stocks])
                    train_labels_list.append(labels.loc[common_stocks])
            except:
                continue

        if len(train_features_list) < 6:
            print(f"  训练数据不足，跳过")
            continue

        train_features = pd.concat(train_features_list)
        train_labels = pd.concat(train_labels_list)

        # 测试数据
        stocks_test = get_stocks_filtered(test_date)
        if len(stocks_test) < 50:
            print(f"  测试股票不足")
            continue

        test_features = get_features(stocks_test, test_date)

        test_idx_next = test_idx + 1 if test_idx + 1 < len(month_ends) else None
        if test_idx_next is None:
            continue

        test_next_date = month_ends[test_idx_next]
        test_returns = get_forward_return(
            test_features.index.tolist(), test_date, test_next_date
        )

        # 特征处理
        train_X, test_X = process_features(train_features.copy(), test_features.copy())

        # 训练和预测
        for model_name, model in models.items():
            try:
                model.fit(train_X, train_labels)
                proba = model.predict_proba(test_X)[:, 1]
                pred_df = pd.DataFrame({"code": test_X.index, "prob": proba})
                pred_df = pred_df.sort_values("prob", ascending=False)
                top_n = max(int(len(pred_df) * 0.3), 10)
                selected = pred_df.head(top_n)["code"].tolist()
                selected_returns = test_returns[test_returns.index.isin(selected)]
                port_return = (
                    selected_returns.mean() if len(selected_returns) > 0 else np.nan
                )
                all_results[model_name].append(port_return)
            except:
                all_results[model_name].append(np.nan)

        # RFScore基线
        try:
            rfscore = calc_rfscore(test_features)
            rfscore_selected = rfscore.nlargest(int(len(rfscore) * 0.3)).index.tolist()
            rfscore_returns = test_returns[test_returns.index.isin(rfscore_selected)]
            rfscore_return = (
                rfscore_returns.mean() if len(rfscore_returns) > 0 else np.nan
            )
            all_results["RFScore"].append(rfscore_return)
        except:
            all_results["RFScore"].append(np.nan)

        benchmark_return = test_returns.mean()
        all_benchmark.append(benchmark_return)
        print(f"  Benchmark: {benchmark_return:.2%}")

    except Exception as e:
        print(f"  错误: {e}")
        continue

# 结果汇总
print("\n" + "=" * 70)
print("验证结果汇总")
print("=" * 70)

results_df = pd.DataFrame(all_results)
results_df["Benchmark"] = all_benchmark[: len(results_df)]
cum_returns = (1 + results_df).cumprod()

print("\n=== 累计收益排名 ===")
final_returns = cum_returns.iloc[-1].sort_values(ascending=False)
for i, (name, ret) in enumerate(final_returns.items()):
    marker = (
        " ← ML最佳"
        if i == 0 and name != "RFScore" and name != "Benchmark"
        else (" ← 基线" if name == "RFScore" else "")
    )
    print(f"  {i + 1}. {name:15s}: {ret:.4f}{marker}")

print("\n=== 月度统计 ===")
stats_list = []
for col in results_df.columns:
    ret = results_df[col].dropna()
    if len(ret) == 0:
        continue
    excess = (
        ret - results_df["Benchmark"].dropna()[: len(ret)]
        if col != "Benchmark"
        else pd.Series([0])
    )
    stats = {
        "Model": col,
        "月均收益(%)": ret.mean() * 100,
        "月胜率(%)": (ret > 0).mean() * 100,
        "月均超额(%)": excess.mean() * 100 if col != "Benchmark" else 0,
        "超额胜率(%)": (excess > 0).mean() * 100 if col != "Benchmark" else 0,
        "收益波动(%)": ret.std() * 100,
        "夏普": ret.mean() / ret.std() if ret.std() > 0 else 0,
        "累计收益": cum_returns[col].iloc[-1],
    }
    stats_list.append(stats)

stats_df = pd.DataFrame(stats_list)
stats_df = stats_df.sort_values("累计收益", ascending=False)
print(stats_df.to_string(index=False))

# 对比RFScore
print("\n=== 与RFScore基线对比 ===")
rfscore_cum = cum_returns["RFScore"].iloc[-1]
for col in ["Logistic", "SVM", "RandomForest", "XGBoost"]:
    if col in cum_returns.columns:
        model_cum = cum_returns[col].iloc[-1]
        diff = model_cum - rfscore_cum
        status = "✓ 优于" if diff > 0 else "✗ 劣于"
        print(f"  {col:15s}: {status} RFScore {abs(diff) * 100:.2f}%")

print("\n" + "=" * 70)
print("最终结论")
print("=" * 70)

# 找出最佳ML模型
ml_models = ["Logistic", "SVM", "RandomForest", "XGBoost"]
ml_returns = {
    col: cum_returns[col].iloc[-1] for col in ml_models if col in cum_returns.columns
}
best_ml_name = max(ml_returns, key=ml_returns.get) if ml_returns else None
best_ml_return = ml_returns.get(best_ml_name, 0) if best_ml_name else 0

print(f"\n最佳ML模型: {best_ml_name}")
print(f"ML累计收益: {best_ml_return:.4f}")
print(f"RFScore累计: {rfscore_cum:.4f}")

# 判定
if best_ml_return > rfscore_cum * 1.05:
    verdict = "Go"
    reason = f"{best_ml_name}显著优于RFScore基线(>5%)，建议投入实盘"
elif best_ml_return > rfscore_cum:
    verdict = "Watch"
    reason = f"{best_ml_name}略优于RFScore，需扩大样本验证"
else:
    verdict = "No-Go"
    reason = "ML模型未能证明优于传统因子方法，建议降级"

print(f"\n★ 最终判定: {verdict}")
print(f"  理由: {reason}")

print("\n" + "=" * 70)
print("验证完成!")
print("=" * 70)
