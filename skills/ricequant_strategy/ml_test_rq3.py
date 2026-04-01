# -*- coding: utf-8 -*-
"""
ML多因子测试 - RiceQuant版（简化）
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

    # 提取每月第一个交易日
    month_dates = []
    last_m = None
    for d in dates:
        if d.month != last_m:
            month_dates.append(d)
            last_m = d.month

    print(f"调仓日期: {len(month_dates)}个月")

    # 股票池
    stocks = index_components("000905.XSHG")[:80]
    print(f"股票池: {len(stocks)}只")

    # 收集数据
    data = {}

    for i, d in enumerate(month_dates[:-1]):
        try:
            print(f"\n处理 {str(d)[:10]}...")

            # 获取因子 - 直接使用，shape是 (股票数, 因子数)
            factor_df = get_factor(
                stocks,
                ["pe_ratio", "pb_ratio", "roe", "roa"],
                start_date=str(d),
                end_date=str(d),
            )

            print(f"  因子形状: {factor_df.shape}")

            if factor_df is None or factor_df.empty:
                print(f"  无因子数据")
                continue

            # 直接清理数据
            feat = factor_df.replace([np.inf, -np.inf], np.nan).dropna()

            print(f"  有效股票: {len(feat)}只")

            if len(feat) < 20:
                continue

            # 下月收益
            next_d = month_dates[i + 1]

            # 获取价格 - 简化
            ret_dict = {}
            for s in feat.index.tolist()[:50]:
                try:
                    bars0 = history_bars(s, 1, "1d", "close", end_date=str(d))
                    bars1 = history_bars(s, 1, "1d", "close", end_date=str(next_d))

                    if (
                        bars0 is not None
                        and bars1 is not None
                        and len(bars0) > 0
                        and len(bars1) > 0
                    ):
                        ret_dict[s] = bars1[-1] / bars0[-1] - 1
                except:
                    pass

            print(f"  收益数据: {len(ret_dict)}只")

            if len(ret_dict) < 20:
                continue

            ret = pd.Series(ret_dict)
            label = (ret > ret.median()).astype(int)

            # 对齐
            common = list(set(feat.index.tolist()) & set(ret.index.tolist()))
            if len(common) < 20:
                continue

            data[i] = {
                "feat": feat.loc[common],
                "label": label.loc[common],
                "ret": ret.loc[common],
            }
            print(f"  成功! 共{len(common)}只")

        except Exception as e:
            print(f"  错误: {e}")

    print(f"\n有效数据: {len(data)}个月")

    # Walk-Forward验证
    if len(data) >= 3:
        print("\n" + "=" * 50)
        print("Walk-Forward验证")

        idx = sorted(data.keys())
        rets = []

        for test_i in idx[1:]:
            train_i = idx[0]  # 用第一个月训练

            X_train = data[train_i]["feat"]
            y_train = data[train_i]["label"]
            X_test = data[test_i]["feat"]
            ret_test = data[test_i]["ret"]

            # 对齐列
            cols = list(X_train.columns)
            X_test = X_test[cols]

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
                print(f"  月{test_i}: 收益={net:.2%}")

        if rets:
            s = pd.Series(rets)
            total = (1 + s).prod() - 1
            win = (s > 0).mean()

            print(f"\n结果: 累计={total:.2%}, 胜率={win:.1%}")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n完成!")
