# -*- coding: utf-8 -*-
"""
ML多因子测试 - RiceQuant版（使用fundamentals）
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

            # 方法1: 用get_factor获取估值因子
            val_df = get_factor(
                stocks, ["pe_ratio", "pb_ratio"], start_date=str(d), end_date=str(d)
            )

            print(f"  估值因子形状: {val_df.shape}")

            # 方法2: 用fundamentals获取财务因子
            try:
                fund = get_fundamentals(
                    query(
                        fundamentals.eod_derivative_indicator.stock_code,
                        fundamentals.financial_indicator.roe,
                        fundamentals.financial_indicator.roa,
                    ).filter(
                        fundamentals.eod_derivative_indicator.stock_code.in_(stocks)
                    ),
                    entry_date=str(d),
                )

                print(f"  财务因子形状: {fund.shape if fund is not None else 'None'}")

                if fund is not None and not fund.empty:
                    # 重置索引
                    fund = fund.reset_index()
                    # 提取股票代码
                    if "stock_code" in fund.columns:
                        fund["code"] = fund["stock_code"].apply(
                            lambda x: x.split(".")[0] + "." + x.split(".")[1]
                        )
                    elif "level_1" in fund.columns:
                        fund["code"] = fund["level_1"]
                    else:
                        # 尝试从索引提取
                        fund["code"] = fund.index.astype(str)

                    fund = fund.set_index("code")
                    print(f"  财务因子索引: {fund.index[:5].tolist()}")

            except Exception as e:
                print(f"  财务因子获取失败: {e}")
                fund = None

            # 简化：只用估值因子
            feat = val_df.fillna(0)

            # 处理MultiIndex
            if isinstance(feat.index, pd.MultiIndex):
                # 取最后一个日期的数据
                feat = feat.reset_index(level=0, drop=True)

            print(f"  最终特征形状: {feat.shape}")

            # 下月收益
            next_d = month_dates[i + 1]

            ret_dict = {}
            for s in stocks[:30]:
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

            if len(ret_dict) < 10:
                continue

            ret = pd.Series(ret_dict)
            label = (ret > ret.median()).astype(int)

            # 对齐
            common = list(set(feat.index.tolist()) & set(ret.index.tolist()))
            if len(common) < 10:
                continue

            data[i] = {
                "feat": feat.loc[common],
                "label": label.loc[common],
                "ret": ret.loc[common],
            }
            print(f"  成功! 共{len(common)}只")

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
