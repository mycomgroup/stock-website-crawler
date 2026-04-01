# -*- coding: utf-8 -*-
"""
ML多因子测试 - RiceQuant版（修正）
"""

print("=" * 50)
print("ML多因子测试 (RiceQuant)")

import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

try:
    # 获取交易日
    dates = get_trading_dates("2024-07-01", "2024-12-31")
    print(f"交易日数: {len(dates)}")

    # 提取每月第一个交易日
    month_dates = []
    last_m = None
    for d in dates:
        if d.month != last_m:
            month_dates.append(d)
            last_m = d.month

    print(f"调仓日期: {len(month_dates)}个月")

    # 股票池
    stocks = index_components("000905.XSHG")[:80]  # 减少股票数
    print(f"股票池: {len(stocks)}只")

    # 收集数据
    data = {}

    for i, d in enumerate(month_dates[:-1]):
        try:
            print(f"\n处理 {str(d)[:10]}...")

            # 获取因子 - 使用正确的方式
            start_d = str(d)
            end_d = str(d)

            factor_df = get_factor(
                stocks,
                ["pe_ratio", "pb_ratio", "roe", "roa"],
                start_date=start_d,
                end_date=end_d,
            )

            print(
                f"  因子数据形状: {factor_df.shape if factor_df is not None else 'None'}"
            )

            if factor_df is None or factor_df.empty:
                print(f"  无因子数据")
                continue

            # 处理数据格式
            if isinstance(factor_df.index, pd.MultiIndex):
                # 多级索引，取第一天的数据
                feat = factor_df.iloc[0].unstack()
            else:
                feat = factor_df

            feat = feat.replace([np.inf, -np.inf], np.nan).dropna()

            print(f"  有效股票: {len(feat)}只")

            if len(feat) < 20:
                continue

            # 下月收益
            next_d = month_dates[i + 1]

            # 获取价格
            p0_data = {}
            p1_data = {}

            for s in feat.index.tolist()[:50]:  # 限制股票数
                try:
                    bars0 = history_bars(s, 1, "1d", "close", end_date=start_d)
                    bars1 = history_bars(s, 1, "1d", "close", end_date=str(next_d))

                    if bars0 is not None and len(bars0) > 0:
                        p0_data[s] = bars0[-1]
                    if bars1 is not None and len(bars1) > 0:
                        p1_data[s] = bars1[-1]
                except:
                    continue

            print(f"  价格数据: {len(p0_data)}, {len(p1_data)}")

            if len(p0_data) < 20 or len(p1_data) < 20:
                continue

            # 计算收益
            common = (
                set(p0_data.keys()) & set(p1_data.keys()) & set(feat.index.tolist())
            )
            print(f"  共同股票: {len(common)}只")

            if len(common) < 20:
                continue

            ret = pd.Series({s: p1_data[s] / p0_data[s] - 1 for s in common})
            label = (ret > ret.median()).astype(int)

            feat = feat.loc[list(common)]

            data[i] = {"feat": feat, "label": label, "ret": ret}
            print(f"  成功!")

        except Exception as e:
            print(f"  错误: {e}")
            import traceback

            traceback.print_exc()

    print(f"\n有效数据: {len(data)}个月")

    # Walk-Forward
    if len(data) >= 3:
        print("\n" + "=" * 50)
        print("Walk-Forward验证...")

        idx = sorted(data.keys())
        rets = []

        for test_i in idx[1:]:  # 用1个月训练
            train_i = [i for i in idx if i < test_i][-1:]

            if not train_i:
                continue

            X_train = data[train_i[0]]["feat"]
            y_train = data[train_i[0]]["label"]
            X_test = data[test_i]["feat"]
            ret_test = data[test_i]["ret"]

            # 对齐特征
            common_feat = X_train.columns.intersection(X_test.columns)
            X_train = X_train[common_feat]
            X_test = X_test[common_feat]

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
            avg = s.mean()

            print(f"\n结果汇总:")
            print(f"  累计收益: {total:.2%}")
            print(f"  月胜率: {win:.1%}")
            print(f"  月均收益: {avg:.2%}")
    else:
        print("数据不足，无法验证")

except Exception as e:
    print(f"执行错误: {e}")
    import traceback

    traceback.print_exc()

print("\n完成!")
