# -*- coding: utf-8 -*-
"""
ML多因子测试 - RiceQuant版（调试2）
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
    stocks = index_components("000905.XSHG")[:50]
    print(f"股票池: {len(stocks)}只")

    # 收集数据
    data = {}

    for i, d in enumerate(month_dates[:-1]):
        try:
            print(f"\n处理 {str(d)[:10]}...")

            # 获取因子
            val_df = get_factor(
                stocks, ["pe_ratio", "pb_ratio"], start_date=str(d), end_date=str(d)
            )

            print(f"  估值因子形状: {val_df.shape}")
            print(f"  估值因子索引类型: {type(val_df.index)}")

            # 处理MultiIndex - 取最后一个level作为股票代码
            if isinstance(val_df.index, pd.MultiIndex):
                print(f"  MultiIndex levels: {val_df.index.names}")
                # 最后一个level通常是股票代码
                val_df = val_df.reset_index()
                code_col = [
                    c
                    for c in val_df.columns
                    if "code" in str(c).lower() or "stock" in str(c).lower()
                ]
                if code_col:
                    val_df = val_df.set_index(code_col[0])
                else:
                    val_df = val_df.set_index(val_df.columns[-1])

            print(f"  处理后索引: {val_df.index[:5].tolist()}")
            feat = val_df.fillna(0)

            # 下月收益 - 使用get_price
            next_d = month_dates[i + 1]

            ret_dict = {}
            for s in stocks[:30]:
                try:
                    p0 = get_price(
                        s, start_date=str(d), end_date=str(d), fields=["close"]
                    )
                    p1 = get_price(
                        s,
                        start_date=str(next_d),
                        end_date=str(next_d),
                        fields=["close"],
                    )

                    if (
                        p0 is not None
                        and p1 is not None
                        and len(p0) > 0
                        and len(p1) > 0
                    ):
                        ret_dict[s] = p1["close"].iloc[0] / p0["close"].iloc[0] - 1
                except:
                    pass

            print(f"  收益数据: {len(ret_dict)}只")

            if len(ret_dict) < 10:
                continue

            ret = pd.Series(ret_dict)
            print(f"  收益索引: {ret.index[:5].tolist()}")

            # 对齐
            feat_stocks = set(feat.index.tolist())
            ret_stocks = set(ret.index.tolist())
            common = list(feat_stocks & ret_stocks)

            print(f"  特征股票: {len(feat_stocks)}")
            print(f"  收益股票: {len(ret_stocks)}")
            print(f"  共同股票: {len(common)}")

            if len(common) < 10:
                print(f"  对齐失败，跳过")
                continue

            label = (ret.loc[common] > ret.loc[common].median()).astype(int)

            data[i] = {"feat": feat.loc[common], "label": label, "ret": ret.loc[common]}
            print(f"  成功!")

        except Exception as e:
            print(f"  错误: {e}")
            import traceback

            traceback.print_exc()

    print(f"\n有效数据: {len(data)}个月")

    # Walk-Forward验证
    if len(data) >= 2:
        print("\n" + "=" * 50)
        print("Walk-Forward验证")

        idx = sorted(data.keys())
        rets = []

        for test_i in idx[1:]:
            train_i = idx[0]

            X_train = data[train_i]["feat"].values
            y_train = data[train_i]["label"].values
            X_test = data[test_i]["feat"].values
            ret_test = data[test_i]["ret"]

            scaler = StandardScaler()
            X_train_s = scaler.fit_transform(X_train)
            X_test_s = scaler.transform(X_test)

            model = LogisticRegression(C=100, max_iter=200)
            model.fit(X_train_s, y_train)

            proba = model.predict_proba(X_test_s)[:, 1]
            stocks_test = data[test_i]["feat"].index
            selected = pd.Series(proba, index=stocks_test).nlargest(10).index
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
