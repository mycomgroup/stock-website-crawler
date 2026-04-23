# -*- coding: utf-8 -*-
"""
ML多因子Walk-Forward验证 - 聚宽版本
====================================
使用真实数据验证 LR/SVM/RF/XGBoost
严格walk-forward，防泄露
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")

# sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

try:
    from xgboost import XGBClassifier

    HAS_XGB = True
except:
    HAS_XGB = False

print("=" * 70)
print("ML多因子Walk-Forward验证 (聚宽真实数据)")
print("=" * 70)

# ============ 参数设置 ============
START_DATE = "2020-01-01"
END_DATE = "2025-12-31"
TRAIN_MONTHS = 12  # 训练窗口
HOLD_N = 20  # 持仓数量
COST = 0.001  # 单边交易成本
STOCK_POOL = "000905.XSHG"  # 中证500

# 特征列
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

# ============ 工具函数 ============


def get_monthly_dates(start, end):
    """获取每月第一个交易日"""
    days = get_trade_days(start, end)
    result, last_m = [], None
    for d in days:
        if d.month != last_m:
            result.append(d)
            last_m = d.month
    return result


def get_stock_pool(date, index=STOCK_POOL):
    """获取股票池（排除ST、停牌、次新股）"""
    stocks = get_index_stocks(index, date=date)
    # 排除上市不足180天的
    valid_stocks = []
    for s in stocks:
        info = get_security_info(s)
        if info and (date - info.start_date).days > 180:
            valid_stocks.append(s)
    # 排除ST
    is_st = get_extras("is_st", valid_stocks, end_date=date, count=1)
    valid_stocks = [s for s in valid_stocks if not is_st[s][0]]
    return valid_stocks


def get_features(stocks, date):
    """获取因子特征（只使用date时刻可获取的数据）"""
    q = query(
        valuation.code,
        valuation.pe_ratio,
        valuation.pb_ratio,
        valuation.ps_ratio,
        valuation.pcf_ratio,
        valuation.market_cap,
        indicator.roe,
        indicator.roa,
        indicator.gross_profit_margin,
        indicator.net_profit_to_total_revenue,
        indicator.inc_net_profit_year_on_year,
        indicator.inc_revenue_year_on_year,
    ).filter(valuation.code.in_(stocks))

    df = get_fundamentals(q, date=date).set_index("code")

    # 计算衍生因子
    df["EP"] = 1 / df["pe_ratio"].replace(0, np.nan)
    df["BP"] = 1 / df["pb_ratio"].replace(0, np.nan)
    df["SP"] = 1 / df["ps_ratio"].replace(0, np.nan)
    df["CFP"] = 1 / df["pcf_ratio"].replace(0, np.nan)
    df["log_market_cap"] = np.log(df["market_cap"].replace(0, np.nan))

    # 去极值
    for col in FEATURE_COLS:
        if col in df.columns:
            q01 = df[col].quantile(0.01)
            q99 = df[col].quantile(0.99)
            df[col] = df[col].clip(q01, q99)

    df = df.replace([np.inf, -np.inf], np.nan)
    return df


def get_next_month_return(stocks, date_start, date_end):
    """获取下月收益率"""
    try:
        p0 = get_price(
            stocks, end_date=str(date_start), count=1, fields=["close"], panel=False
        )
        p1 = get_price(
            stocks, end_date=str(date_end), count=1, fields=["close"], panel=False
        )
        if p0 is None or p1 is None or len(p0) == 0 or len(p1) == 0:
            return pd.Series()
        p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
        p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
        return ((p1 / p0) - 1).dropna()
    except Exception as e:
        print(f"  获取收益失败: {e}")
        return pd.Series()


# ============ 数据收集 ============

print(f"\n股票池: {STOCK_POOL}")
print(f"时间范围: {START_DATE} ~ {END_DATE}")
print(f"训练窗口: {TRAIN_MONTHS}个月")

dates = get_monthly_dates(START_DATE, END_DATE)
print(f"调仓次数: {len(dates) - 1}")

print("\n收集历史特征数据...")
monthly_data = {}
success_count = 0

for i, d in enumerate(dates[:-1]):
    try:
        # 获取股票池
        stocks = get_stock_pool(d)
        if len(stocks) < 50:
            continue

        # 获取特征
        feat = get_features(stocks, d)
        if len(feat) < 50:
            continue

        # 获取下月收益
        ret = get_next_month_return(feat.index.tolist(), d, dates[i + 1])
        if len(ret) < 50:
            continue

        # 对齐
        common = feat.index.intersection(ret.index)
        if len(common) < 50:
            continue

        feat = feat.loc[common]
        ret = ret.loc[common]

        # 创建标签（高于中位数为1）
        label = (ret > ret.median()).astype(int)

        monthly_data[i] = {"feat": feat, "label": label, "ret": ret, "date": d}
        success_count += 1

        if success_count % 12 == 0:
            print(f"  已处理 {success_count} 个月 ({d})")

    except Exception as e:
        continue

print(f"有效月份: {len(monthly_data)}")

if len(monthly_data) < TRAIN_MONTHS + 6:
    print("数据不足，无法进行walk-forward验证")
else:
    # ============ Walk-Forward验证 ============

    models = {
        "逻辑回归": LogisticRegression(C=100, max_iter=500, random_state=42),
        "SVM": SVC(kernel="rbf", probability=True, C=1.0, random_state=42),
        "随机森林": RandomForestClassifier(
            n_estimators=100, max_depth=5, random_state=42, n_jobs=-1
        ),
    }

    if HAS_XGB:
        models["XGBoost"] = XGBClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42,
            use_label_encoder=False,
            eval_metric="logloss",
        )

    valid_indices = sorted(monthly_data.keys())
    print(f"\n开始Walk-Forward验证...")
    print(f"样本外月数: {len(valid_indices) - TRAIN_MONTHS}")

    results = {name: [] for name in models}
    accuracies = {name: [] for name in models}

    for test_idx in valid_indices[TRAIN_MONTHS:]:
        # 训练窗口索引
        train_indices = [i for i in valid_indices if i < test_idx][-TRAIN_MONTHS:]

        if len(train_indices) < TRAIN_MONTHS:
            continue

        # 准备训练数据
        X_train_list, y_train_list = [], []
        for i in train_indices:
            if i in monthly_data:
                feat = monthly_data[i]["feat"]
                label = monthly_data[i]["label"]
                common = feat.index.intersection(label.index)
                if len(common) > 10:
                    valid_cols = [c for c in FEATURE_COLS if c in feat.columns]
                    X_train_list.append(feat.loc[common, valid_cols].fillna(0))
                    y_train_list.append(label.loc[common])

        if not X_train_list:
            continue

        X_train = pd.concat(X_train_list)
        y_train = pd.concat(y_train_list)

        # 测试数据
        X_test = monthly_data[test_idx]["feat"]
        ret_test = monthly_data[test_idx]["ret"]
        y_test = monthly_data[test_idx]["label"]

        valid_cols = [c for c in FEATURE_COLS if c in X_train.columns]
        X_test = X_test[valid_cols].fillna(0)

        # 标准化
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # 对每个模型预测
        for name, model in models.items():
            try:
                model.fit(X_train_scaled, y_train)

                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(X_test_scaled)[:, 1]
                else:
                    proba = model.decision_function(X_test_scaled)

                # 选股
                pred_series = pd.Series(proba, index=X_test.index)
                selected = pred_series.nlargest(HOLD_N).index.tolist()

                # 计算收益
                available = [s for s in selected if s in ret_test.index]
                if available:
                    gross = ret_test.loc[available].mean()
                    net = gross - COST * 2
                    results[name].append(net)

                    # 准确率
                    pred_binary = (proba > np.median(proba)).astype(int)
                    common_test = X_test.index.intersection(y_test.index)
                    if len(common_test) > 0:
                        acc = accuracy_score(
                            y_test.loc[common_test], pred_binary[: len(common_test)]
                        )
                        accuracies[name].append(acc)
                else:
                    results[name].append(0.0)
                    accuracies[name].append(0.0)
            except Exception as e:
                results[name].append(0.0)
                accuracies[name].append(0.0)

    # ============ 结果汇总 ============

    print("\n" + "=" * 70)
    print("【ML Walk-Forward 真实数据验证结果】")
    print("=" * 70)

    summary_rows = []
    for name in models.keys():
        rets = results[name]
        if not rets:
            continue

        s = pd.Series(rets)
        cum = (1 + s).cumprod()

        total_months = len(s)
        ann_return = cum.iloc[-1] ** (12 / total_months) - 1
        max_dd = (cum / cum.cummax() - 1).min()
        sharpe = s.mean() / s.std() * (12**0.5) if s.std() > 0 else 0
        win_rate = (s > 0).mean()
        avg_acc = np.mean(accuracies[name]) if accuracies[name] else 0

        summary_rows.append(
            {
                "模型": name,
                "年化收益": f"{ann_return:.2%}",
                "最大回撤": f"{max_dd:.2%}",
                "夏普比率": f"{sharpe:.3f}",
                "月胜率": f"{win_rate:.1%}",
                "平均准确率": f"{avg_acc:.1%}",
                "样本月数": total_months,
            }
        )

    df_res = pd.DataFrame(summary_rows).set_index("模型")
    print(df_res.to_string())

    # ============ 判断结论 ============

    print("\n" + "=" * 70)
    print("【判断结论】")
    print("=" * 70)

    # 找出最好的模型
    best_sharpe = -999
    best_model = ""
    worst_sharpe = 999
    worst_model = ""

    for row in summary_rows:
        sharpe = float(row["夏普比率"])
        if sharpe > best_sharpe:
            best_sharpe = sharpe
            best_model = row.name if hasattr(row, "name") else row["模型"]
        if sharpe < worst_sharpe:
            worst_sharpe = sharpe
            worst_model = row.name if hasattr(row, "name") else row["模型"]

    print(f"最值得保留的模型: {best_model}")
    print(f"  夏普比率: {best_sharpe:.3f}")

    print(f"\n淘汰理由最充分的模型: {worst_model}")
    print(f"  夏普比率: {worst_sharpe:.3f}")

    print("\n" + "-" * 70)
    if best_sharpe > 0.8:
        print("结论: 夏普 > 0.8，ML线值得考虑工程化")
    elif best_sharpe > 0.3:
        print("结论: 夏普在0.3-0.8之间，ML线需要进一步研究")
    elif best_sharpe > 0:
        print("结论: 夏普 > 0 但 < 0.3，ML线优势不明显")
    else:
        print("结论: 夏普 < 0，ML线暂不值得先跑")

    print("\n注意: 以上为严格walk-forward样本外结果")
    print("如与文档历史数字差异大，说明原结果存在数据泄露风险")

    # ============ 与文档对比 ============

    print("\n" + "=" * 70)
    print("【与文档声称值对比】")
    print("=" * 70)

    doc_claims = {
        "SVM": {"收益": "78.62%", "月胜率": "68.4%"},
        "逻辑回归": {"收益": "73.34%", "月胜率": "68.4%"},
    }

    for name in ["SVM", "逻辑回归"]:
        if name in results and results[name]:
            s = pd.Series(results[name])
            cum = (1 + s).cumprod()
            actual_return = f"{(cum.iloc[-1] - 1):.2%}"
            actual_win = f"{(s > 0).mean():.1%}"

            print(f"\n{name}:")
            print(
                f"  文档声称: 收益={doc_claims[name]['收益']}, 胜率={doc_claims[name]['月胜率']}"
            )
            print(f"  实测结果: 收益={actual_return}, 胜率={actual_win}")

print("\n验证完成!")
