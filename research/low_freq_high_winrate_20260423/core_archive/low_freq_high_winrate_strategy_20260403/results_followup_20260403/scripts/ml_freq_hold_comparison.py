# -*- coding: utf-8 -*-
"""
ML调仓频率与持仓数轻量比较 - 聚宽Walk-Forward验证脚本
=====================================================
固定模型：逻辑回归 (LogisticRegression)
固定股票池：中证500
固定因子：13因子短名单（来自result_09）

比较4档配置：
  A. 季频 + 10只
  B. 季频 + 15只
  C. 月频 + 10只
  D. 月频 + 15只
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

print("=" * 70)
print("ML调仓频率与持仓数轻量比较 (逻辑回归固定)")
print("=" * 70)

# ============ 固定参数 ============
START_DATE = "2020-01-01"
END_DATE = "2025-12-31"
TRAIN_MONTHS = 12  # 训练窗口
COST = 0.001  # 单边交易成本
STOCK_POOL = "000905.XSHG"  # 中证500

# 13因子短名单（来自result_09）
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

# 4档配置
CONFIGS = {
    "季频+10只": {"freq": "quarterly", "hold_n": 10},
    "季频+15只": {"freq": "quarterly", "hold_n": 15},
    "月频+10只": {"freq": "monthly", "hold_n": 10},
    "月频+15只": {"freq": "monthly", "hold_n": 15},
}


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


def get_quarterly_dates(monthly_dates):
    """从月度日期中提取季度日期（每季度第一个月）"""
    return [d for d in monthly_dates if d.month in (1, 4, 7, 10)]


def get_stock_pool(date, index=STOCK_POOL):
    """获取股票池（排除ST、停牌、次新股）"""
    stocks = get_index_stocks(index, date=date)
    valid_stocks = []
    for s in stocks:
        info = get_security_info(s)
        if info and (date - info.start_date).days > 180:
            valid_stocks.append(s)
    is_st = get_extras("is_st", valid_stocks, end_date=date, count=1)
    valid_stocks = [s for s in valid_stocks if not is_st[s][0]]
    return valid_stocks


def get_features(stocks, date):
    """获取因子特征"""
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

    df["EP"] = 1 / df["pe_ratio"].replace(0, np.nan)
    df["BP"] = 1 / df["pb_ratio"].replace(0, np.nan)
    df["SP"] = 1 / df["ps_ratio"].replace(0, np.nan)
    df["CFP"] = 1 / df["pcf_ratio"].replace(0, np.nan)
    df["log_market_cap"] = np.log(df["market_cap"].replace(0, np.nan))

    for col in FEATURE_COLS:
        if col in df.columns:
            q01 = df[col].quantile(0.01)
            q99 = df[col].quantile(0.99)
            df[col] = df[col].clip(q01, q99)

    df = df.replace([np.inf, -np.inf], np.nan)
    return df


def get_period_return(stocks, date_start, date_end):
    """获取期间收益率"""
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


def get_next_quarter_end(date):
    """获取下一个季度末日期"""
    month = date.month
    if month in (1, 2, 3):
        target_month = 4
    elif month in (4, 5, 6):
        target_month = 7
    elif month in (7, 8, 9):
        target_month = 10
    else:
        target_month = 1
    target_year = date.year if target_month > month else date.year + 1
    # 获取目标月第一个交易日，然后取前一天作为季度末
    trade_days = get_trade_days(
        f"{target_year}-{target_month:02d}-01",
        f"{target_year}-{target_month:02d}-28",
    )
    if len(trade_days) > 0:
        return trade_days[0]
    return date + timedelta(days=90)


# ============ 数据收集 ============
print(f"\n股票池: {STOCK_POOL}")
print(f"时间范围: {START_DATE} ~ {END_DATE}")
print(f"训练窗口: {TRAIN_MONTHS}个月")

monthly_dates = get_monthly_dates(START_DATE, END_DATE)
quarterly_dates = get_quarterly_dates(monthly_dates)

print(f"月度调仓日期数: {len(monthly_dates)}")
print(f"季度调仓日期数: {len(quarterly_dates)}")

print("\n收集历史特征数据（月度）...")
monthly_data = {}
success_count = 0

for i, d in enumerate(monthly_dates[:-1]):
    try:
        stocks = get_stock_pool(d)
        if len(stocks) < 50:
            continue

        feat = get_features(stocks, d)
        if len(feat) < 50:
            continue

        # 获取下期收益
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
        success_count += 1

        if success_count % 12 == 0:
            print(f"  已处理 {success_count} 个月 ({d})")

    except Exception as e:
        continue

print(f"有效月度数据: {len(monthly_data)}")

if len(monthly_data) < TRAIN_MONTHS + 6:
    print("数据不足，无法进行walk-forward验证")
else:
    # ============ 构建季度数据索引映射 ============
    # 将月度数据索引映射到季度
    monthly_indices = sorted(monthly_data.keys())

    # 找到季度对应的月度索引
    quarterly_indices = []
    for qd in quarterly_dates:
        for mi, md in enumerate(monthly_dates):
            if md == qd and mi in monthly_data:
                quarterly_indices.append(mi)
                break

    print(f"\n有效季度索引数: {len(quarterly_indices)}")

    # ============ Walk-Forward验证 ============
    model_params = {"C": 100, "max_iter": 500, "random_state": 42}

    print(f"\n开始Walk-Forward验证 4 档配置...")

    all_results = {}

    for config_name, config in CONFIGS.items():
        print(f"\n{'=' * 50}")
        print(f"配置: {config_name}")
        print(f"  频率: {config['freq']}, 持仓数: {config['hold_n']}")
        print(f"{'=' * 50}")

        # 选择对应频率的测试索引
        if config["freq"] == "quarterly":
            test_indices = quarterly_indices[TRAIN_MONTHS // 3 :]  # 季度训练窗口
            train_window_size = TRAIN_MONTHS // 3  # 4个季度
        else:
            test_indices = monthly_indices[TRAIN_MONTHS:]
            train_window_size = TRAIN_MONTHS

        config_results = []
        config_turnover = []
        config_hold_periods = []

        for test_idx in test_indices:
            # 确定训练窗口
            if config["freq"] == "quarterly":
                # 季度模式：找最近的4个季度索引
                train_candidates = [qi for qi in quarterly_indices if qi < test_idx][
                    -train_window_size:
                ]
                # 扩展到月度索引用于数据获取
                train_indices = []
                for qi in train_candidates:
                    # 包含该季度对应的月度数据及前后月份
                    for mi in monthly_indices:
                        if mi <= qi and mi > qi - 3:
                            if mi not in train_indices:
                                train_indices.append(mi)
            else:
                train_indices = [i for i in monthly_indices if i < test_idx][
                    -train_window_size:
                ]

            if len(train_indices) < train_window_size * 0.5:
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

            # 逻辑回归预测
            try:
                model = LogisticRegression(**model_params)
                model.fit(X_train_scaled, y_train)
                proba = model.predict_proba(X_test_scaled)[:, 1]

                # 选股
                pred_series = pd.Series(proba, index=X_test.index)
                selected = pred_series.nlargest(config["hold_n"]).index.tolist()

                # 计算收益
                available = [s for s in selected if s in ret_test.index]
                if available:
                    gross = ret_test.loc[available].mean()
                    net = gross - COST * 2
                    config_results.append(
                        {
                            "date": monthly_data[test_idx]["date"],
                            "return": net,
                            "n_selected": len(available),
                        }
                    )

                    # 计算换手率（与上期重叠度）
                    if len(config_results) > 1:
                        prev_selected = set(config_results[-2].get("stocks", []))
                        curr_selected = set(available)
                        if len(prev_selected) > 0:
                            turnover = 1 - len(prev_selected & curr_selected) / len(
                                prev_selected
                            )
                            config_turnover.append(turnover)

                    # 保存当前选股用于下期换手计算
                    config_results[-1]["stocks"] = available

            except Exception as e:
                print(f"  预测失败 at {monthly_data[test_idx]['date']}: {e}")
                continue

        # 汇总该配置结果
        if config_results:
            rets = pd.Series([r["return"] for r in config_results])
            dates = [r["date"] for r in config_results]

            cum = (1 + rets).cumprod()
            total_periods = len(rets)

            # 年化
            if config["freq"] == "monthly":
                ann_return = cum.iloc[-1] ** (12 / total_periods) - 1
            else:
                ann_return = cum.iloc[-1] ** (4 / total_periods) - 1

            max_dd = (cum / cum.cummax() - 1).min()
            sharpe = rets.mean() / rets.std() * (12**0.5) if rets.std() > 0 else 0
            win_rate = (rets > 0).mean()

            avg_turnover = np.mean(config_turnover) if config_turnover else 0
            # 年化换手次数
            if config["freq"] == "monthly":
                annual_turns = 12
            else:
                annual_turns = 4
            annual_turnover_cost = annual_turns * avg_turnover * COST * 2

            all_results[config_name] = {
                "累计收益": f"{(cum.iloc[-1] - 1):.2%}",
                "年化收益": f"{ann_return:.2%}",
                "最大回撤": f"{max_dd:.2%}",
                "夏普比率": f"{sharpe:.3f}",
                "胜率": f"{win_rate:.1%}",
                "盈利期数": f"{(rets > 0).sum()}/{total_periods}",
                "平均换手率": f"{avg_turnover:.1%}",
                "年化换手成本": f"{annual_turnover_cost:.2%}",
                "测试期数": total_periods,
                "freq": config["freq"],
                "hold_n": config["hold_n"],
                "rets": rets,
                "cum": cum,
                "avg_turnover": avg_turnover,
            }

            print(f"  累计收益: {all_results[config_name]['累计收益']}")
            print(f"  年化收益: {all_results[config_name]['年化收益']}")
            print(f"  最大回撤: {all_results[config_name]['最大回撤']}")
            print(f"  夏普比率: {all_results[config_name]['夏普比率']}")
            print(f"  胜率: {all_results[config_name]['胜率']}")
            print(f"  平均换手率: {all_results[config_name]['平均换手率']}")
            print(f"  年化换手成本: {all_results[config_name]['年化换手成本']}")

    # ============ 4档对比汇总 ============
    print("\n" + "=" * 70)
    print("【4档配置对比汇总】")
    print("=" * 70)

    summary_rows = []
    for name, res in all_results.items():
        summary_rows.append(
            {
                "配置": name,
                "累计收益": res["累计收益"],
                "年化收益": res["年化收益"],
                "最大回撤": res["最大回撤"],
                "夏普比率": res["夏普比率"],
                "胜率": res["胜率"],
                "盈利期数": res["盈利期数"],
                "平均换手率": res["平均换手率"],
                "年化换手成本": res["年化换手成本"],
                "测试期数": res["测试期数"],
            }
        )

    df_summary = pd.DataFrame(summary_rows)
    print(df_summary.to_string(index=False))

    # ============ 综合评分 ============
    print("\n" + "=" * 70)
    print("【综合评分与推荐】")
    print("=" * 70)

    # 评分维度（针对"低频主仓"定位）
    # 1. 胜率权重 30%
    # 2. 夏普比率权重 25%
    # 3. 最大回撤权重 20%
    # 4. 换手成本低权重 15%
    # 5. 稳定性（收益标准差倒数）权重 10%

    scores = {}
    for name, res in all_results.items():
        rets = res["rets"]
        # 归一化评分（简单排名法）
        score = 0
        # 胜率越高越好
        score += float(res["胜率"].strip("%")) / 100 * 30
        # 夏普越高越好
        score += float(res["夏普比率"]) * 25
        # 回撤越小越好（取绝对值后取负）
        score += (1 - abs(float(res["最大回撤"].strip("%"))) / 100) * 20
        # 换手成本越低越好
        score += (1 - float(res["年化换手成本"].strip("%")) / 100) * 15
        # 稳定性
        score += (1 / (rets.std() + 0.01)) * 10
        scores[name] = score

    for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {score:.2f}")

    best_config = max(scores, key=scores.get)
    print(f"\n主推荐: {best_config}")
    print(f"  综合评分: {scores[best_config]:.2f}")

    print("\n验证完成!")
