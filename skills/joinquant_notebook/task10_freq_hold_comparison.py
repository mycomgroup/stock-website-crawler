# -*- coding: utf-8 -*-
"""
任务10: ML调仓频率与持仓数轻量比较 - 聚宽Notebook验证
======================================================
固定：逻辑回归 + 中证500 + 基础因子
比较：季频/月频 × 10只/15只 = 4档配置
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

print("=" * 70)
print("任务10: ML调仓频率与持仓数轻量比较")
print("=" * 70)

# ============ 固定参数 ============
START_DATE = "2020-01-01"
END_DATE = "2025-09-30"
TRAIN_MONTHS = 12
COST = 0.001
STOCK_POOL = "000905.XSHG"

# 基础因子集（4因子基线，来自07结果）
FEATURE_COLS = ["pe_ratio", "pb_ratio", "roe", "roa"]

# 4档配置
CONFIGS = {
    "季频+10只": {"freq": "quarterly", "hold_n": 10},
    "季频+15只": {"freq": "quarterly", "hold_n": 15},
    "月频+10只": {"freq": "monthly", "hold_n": 10},
    "月频+15只": {"freq": "monthly", "hold_n": 15},
}


# ============ 工具函数 ============
def get_monthly_dates(start, end):
    days = get_trade_days(start, end)
    result, last_m = [], None
    for d in days:
        if d.month != last_m:
            result.append(d)
            last_m = d.month
    return result


def get_stock_pool(date):
    stocks = get_index_stocks(STOCK_POOL, date=date)
    valid = []
    for s in stocks:
        info = get_security_info(s)
        if info and (date - info.start_date).days > 180:
            valid.append(s)
    is_st = get_extras("is_st", valid, end_date=date, count=1)
    valid = [s for s in valid if not is_st[s][0]]
    return valid


def get_features(stocks, date):
    q = query(
        valuation.code,
        valuation.pe_ratio,
        valuation.pb_ratio,
        indicator.roe,
        indicator.roa,
    ).filter(valuation.code.in_(stocks))

    df = get_fundamentals(q, date=date).set_index("code")

    for col in FEATURE_COLS:
        if col in df.columns:
            q01 = df[col].quantile(0.01)
            q99 = df[col].quantile(0.99)
            df[col] = df[col].clip(q01, q99)

    df = df.replace([np.inf, -np.inf], np.nan)
    return df


def get_period_return(stocks, date_start, date_end):
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
    except:
        return pd.Series()


# ============ 数据收集 ============
print(f"\n股票池: {STOCK_POOL}")
print(f"时间范围: {START_DATE} ~ {END_DATE}")
print(f"因子: {FEATURE_COLS}")

monthly_dates = get_monthly_dates(START_DATE, END_DATE)
quarterly_dates = [d for d in monthly_dates if d.month in (1, 4, 7, 10)]

print(f"月度日期数: {len(monthly_dates)}")
print(f"季度日期数: {len(quarterly_dates)}")

print("\n收集数据...")
monthly_data = {}
success = 0

for i, d in enumerate(monthly_dates[:-1]):
    try:
        stocks = get_stock_pool(d)
        if len(stocks) < 50:
            continue

        feat = get_features(stocks, d)
        if len(feat) < 50:
            continue

        next_date = monthly_dates[i + 1]
        ret = get_period_return(feat.index.tolist(), d, next_date)
        if len(ret) < 50:
            continue

        common = feat.index.intersection(ret.index)
        if len(common) < 50:
            continue

        feat = feat.loc[common]
        ret = ret.loc[common]
        label = (ret > ret.median()).astype(int)

        monthly_data[i] = {"feat": feat, "label": label, "ret": ret, "date": d}
        success += 1
        if success % 12 == 0:
            print(f"  已处理 {success} 个月 ({d})")
    except:
        continue

print(f"有效月度: {len(monthly_data)}")

if len(monthly_data) < TRAIN_MONTHS + 6:
    print("数据不足")
else:
    monthly_indices = sorted(monthly_data.keys())

    # 季度索引映射
    quarterly_indices = []
    for qd in quarterly_dates:
        for mi, md in enumerate(monthly_dates):
            if md == qd and mi in monthly_data:
                quarterly_indices.append(mi)
                break

    print(f"有效季度: {len(quarterly_indices)}")

    # ============ Walk-Forward 验证 ============
    print("\n开始4档配置Walk-Forward验证...")

    all_results = {}

    for config_name, config in CONFIGS.items():
        print(f"\n{'=' * 50}")
        print(f"配置: {config_name}")
        print(f"{'=' * 50}")

        freq = config["freq"]
        hold_n = config["hold_n"]

        if freq == "quarterly":
            test_indices = quarterly_indices[4:]  # 4个季度训练窗口
            train_window = 4
        else:
            test_indices = monthly_indices[TRAIN_MONTHS:]
            train_window = TRAIN_MONTHS

        config_rets = []
        config_dates = []
        prev_selected = set()

        for test_idx in test_indices:
            # 训练窗口
            if freq == "quarterly":
                train_candidates = [qi for qi in quarterly_indices if qi < test_idx][
                    -train_window:
                ]
                train_indices = []
                for qi in train_candidates:
                    for mi in monthly_indices:
                        if mi <= qi and mi > qi - 3:
                            if mi not in train_indices:
                                train_indices.append(mi)
            else:
                train_indices = [i for i in monthly_indices if i < test_idx][
                    -train_window:
                ]

            if len(train_indices) < train_window * 0.5:
                continue

            # 训练数据
            X_train_list, y_train_list = [], []
            for i in train_indices:
                if i in monthly_data:
                    feat = monthly_data[i]["feat"]
                    label = monthly_data[i]["label"]
                    common = feat.index.intersection(label.index)
                    if len(common) > 10:
                        X_train_list.append(feat.loc[common, FEATURE_COLS].fillna(0))
                        y_train_list.append(label.loc[common])

            if not X_train_list:
                continue

            X_train = pd.concat(X_train_list)
            y_train = pd.concat(y_train_list)

            X_test = monthly_data[test_idx]["feat"][FEATURE_COLS].fillna(0)
            ret_test = monthly_data[test_idx]["ret"]

            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            try:
                model = LogisticRegression(C=100, max_iter=500, random_state=42)
                model.fit(X_train_scaled, y_train)
                proba = model.predict_proba(X_test_scaled)[:, 1]

                selected = (
                    pd.Series(proba, index=X_test.index).nlargest(hold_n).index.tolist()
                )
                available = [s for s in selected if s in ret_test.index]

                if available:
                    gross = ret_test.loc[available].mean()
                    net = gross - COST * 2
                    config_rets.append(net)
                    config_dates.append(monthly_data[test_idx]["date"])

                    # 换手率
                    curr_set = set(available)
                    if prev_selected and len(prev_selected) > 0:
                        turnover = 1 - len(prev_selected & curr_set) / len(
                            prev_selected
                        )
                    else:
                        turnover = 1.0
                    prev_selected = curr_set

            except Exception as e:
                continue

        if config_rets:
            rets = pd.Series(config_rets)
            cum = (1 + rets).cumprod()
            n = len(rets)

            if freq == "monthly":
                ann = cum.iloc[-1] ** (12 / n) - 1
            else:
                ann = cum.iloc[-1] ** (4 / n) - 1

            max_dd = (cum / cum.cummax() - 1).min()
            sharpe = rets.mean() / rets.std() * (12**0.5) if rets.std() > 0 else 0
            win_rate = (rets > 0).mean()

            all_results[config_name] = {
                "累计收益": f"{(cum.iloc[-1] - 1):.2%}",
                "年化收益": f"{ann:.2%}",
                "最大回撤": f"{max_dd:.2%}",
                "夏普": f"{sharpe:.3f}",
                "胜率": f"{win_rate:.1%}",
                "盈利/总期": f"{(rets > 0).sum()}/{n}",
                "期数": n,
                "rets": rets,
            }

            print(f"  累计收益: {all_results[config_name]['累计收益']}")
            print(f"  年化收益: {all_results[config_name]['年化收益']}")
            print(f"  最大回撤: {all_results[config_name]['最大回撤']}")
            print(f"  夏普: {all_results[config_name]['夏普']}")
            print(f"  胜率: {all_results[config_name]['胜率']}")
            print(f"  盈利/总期: {all_results[config_name]['盈利/总期']}")

    # ============ 汇总 ============
    print("\n" + "=" * 70)
    print("【4档配置对比汇总】")
    print("=" * 70)

    rows = []
    for name, res in all_results.items():
        rows.append(
            {
                "配置": name,
                "累计收益": res["累计收益"],
                "年化收益": res["年化收益"],
                "最大回撤": res["最大回撤"],
                "夏普": res["夏普"],
                "胜率": res["胜率"],
                "盈利/总期": res["盈利/总期"],
                "期数": res["期数"],
            }
        )

    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

    # ============ 结论 ============
    print("\n" + "=" * 70)
    print("【结论】")
    print("=" * 70)

    # 找胜率最高的
    best_wr = max(all_results.items(), key=lambda x: float(x[1]["胜率"].strip("%")))
    # 找夏普最高的
    best_sharpe = max(all_results.items(), key=lambda x: float(x[1]["夏普"]))

    print(f"胜率最高: {best_wr[0]} ({best_wr[1]['胜率']})")
    print(f"夏普最高: {best_sharpe[0]} ({best_sharpe[1]['夏普']})")

    # 综合推荐（胜率+夏普加权）
    scores = {}
    for name, res in all_results.items():
        wr = float(res["胜率"].strip("%"))
        sh = float(res["夏普"])
        dd = abs(float(res["最大回撤"].strip("%")))
        score = wr * 0.5 + sh * 20 - dd * 0.3
        scores[name] = score

    print("\n综合评分（胜率50% + 夏普*20 - 回撤*0.3）:")
    for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {score:.2f}")

    best = max(scores, key=scores.get)
    print(f"\n主推荐: {best}")

print("\n验证完成!")
