# -*- coding: utf-8 -*-
"""
ML多因子Walk-Forward严格验证框架
=================================
目标：在防泄露前提下，对比 LR/SVM/RF/XGBoost
验证方式：滚动训练窗口，严格样本外预测

核心原则：
1. 所有特征计算只使用当前时点可获取的数据
2. 标签基于未来收益率，训练时需严格错位
3. 特征标准化只在训练窗口内拟合
4. 模型每个调仓日重新训练
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")

# sklearn模型
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score

try:
    from xgboost import XGBClassifier

    HAS_XGB = True
except ImportError:
    HAS_XGB = False
    print("Warning: XGBoost not available, will skip XGB model")


class MLWalkForwardValidator:
    """ML多因子Walk-Forward验证器"""

    def __init__(
        self,
        train_months=12,  # 训练窗口（月）
        hold_n=20,  # 持仓数量
        cost=0.001,  # 单边交易成本
        top_pct=0.3,  # 选股比例（预测概率前30%）
        feature_cols=None,
    ):  # 特征列
        self.train_months = train_months
        self.hold_n = hold_n
        self.cost = cost
        self.top_pct = top_pct

        # 默认特征列（与文档保持一致）
        self.feature_cols = feature_cols or [
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

        # 初始化模型
        self.models = {
            "逻辑回归": LogisticRegression(C=100, max_iter=500, random_state=42),
            "SVM": SVC(kernel="rbf", probability=True, C=1.0, random_state=42),
            "随机森林": RandomForestClassifier(
                n_estimators=100, max_depth=5, random_state=42, n_jobs=-1
            ),
        }

        if HAS_XGB:
            self.models["XGBoost"] = XGBClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42,
                use_label_encoder=False,
                eval_metric="logloss",
            )

    def prepare_features(self, df):
        """
        特征工程：计算衍生因子
        注意：只使用当前时点可获取的数据
        """
        df = df.copy()

        # 计算衍生因子（倒数）
        if "pe_ratio" in df.columns:
            df["EP"] = 1 / df["pe_ratio"].replace(0, np.nan)
        if "pb_ratio" in df.columns:
            df["BP"] = 1 / df["pb_ratio"].replace(0, np.nan)
        if "ps_ratio" in df.columns:
            df["SP"] = 1 / df["ps_ratio"].replace(0, np.nan)
        if "pcf_ratio" in df.columns:
            df["CFP"] = 1 / df["pcf_ratio"].replace(0, np.nan)
        if "market_cap" in df.columns:
            df["log_market_cap"] = np.log(df["market_cap"].replace(0, np.nan))

        # 去极值（1%/99%分位数）
        for col in self.feature_cols:
            if col in df.columns:
                q01 = df[col].quantile(0.01)
                q99 = df[col].quantile(0.99)
                df[col] = df[col].clip(q01, q99)

        return df

    def create_labels(self, returns, method="median"):
        """
        创建分类标签
        method: 'median' - 高于中位数为1，否则0
                'positive' - 正收益为1，否则0
        """
        if method == "median":
            return (returns > returns.median()).astype(int)
        elif method == "positive":
            return (returns > 0).astype(int)
        else:
            raise ValueError(f"Unknown label method: {method}")

    def validate_single_model(self, model_name, model, monthly_data, valid_indices):
        """
        对单个模型进行walk-forward验证

        参数:
            model_name: 模型名称
            model: sklearn模型实例
            monthly_data: dict, {idx: {'feat': df, 'label': series, 'ret': series}}
            valid_indices: list, 有效的月份索引

        返回:
            results: list of dict, 每月的收益和指标
        """
        results = []
        scaler = StandardScaler()

        for test_idx in valid_indices[self.train_months :]:
            # 获取训练窗口的索引
            train_indices = [i for i in valid_indices if i < test_idx][
                -self.train_months :
            ]

            if len(train_indices) < self.train_months:
                continue

            try:
                # 准备训练数据（只使用训练窗口内的数据）
                X_train_list = []
                y_train_list = []

                for i in train_indices:
                    if i in monthly_data:
                        feat = monthly_data[i]["feat"]
                        label = monthly_data[i]["label"]
                        common = feat.index.intersection(label.index)
                        if len(common) > 10:
                            X_train_list.append(feat.loc[common, self.feature_cols])
                            y_train_list.append(label.loc[common])

                if not X_train_list:
                    results.append({"return": 0.0, "accuracy": 0.0, "selected": 0})
                    continue

                X_train = pd.concat(X_train_list)
                y_train = pd.concat(y_train_list)

                # 准备测试数据
                X_test = monthly_data[test_idx]["feat"]
                ret_test = monthly_data[test_idx]["ret"]

                # 确保特征列存在
                valid_cols = [c for c in self.feature_cols if c in X_train.columns]
                if len(valid_cols) < 3:
                    results.append({"return": 0.0, "accuracy": 0.0, "selected": 0})
                    continue

                X_train = X_train[valid_cols].fillna(0)
                X_test = X_test[valid_cols].fillna(0)

                # 标准化（只在训练集上拟合）
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                # 训练模型
                model.fit(X_train_scaled, y_train)

                # 预测
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(X_test_scaled)[:, 1]
                else:
                    proba = model.decision_function(X_test_scaled)

                pred_series = pd.Series(proba, index=X_test.index)

                # 选股：选择预测概率最高的前N只
                selected = pred_series.nlargest(self.hold_n).index.tolist()

                if not selected:
                    results.append({"return": 0.0, "accuracy": 0.0, "selected": 0})
                    continue

                # 计算收益（扣除双边成本）
                available_stocks = [s for s in selected if s in ret_test.index]
                if available_stocks:
                    gross_return = ret_test.loc[available_stocks].mean()
                    net_return = gross_return - self.cost * 2

                    # 计算准确率
                    y_test = monthly_data[test_idx]["label"]
                    common_test = X_test.index.intersection(y_test.index)
                    if len(common_test) > 0:
                        pred_binary = (
                            proba[: len(common_test)] > np.median(proba)
                        ).astype(int)
                        acc = accuracy_score(
                            y_test.loc[common_test], pred_binary[: len(common_test)]
                        )
                    else:
                        acc = 0.0

                    results.append(
                        {
                            "return": net_return,
                            "accuracy": acc,
                            "selected": len(available_stocks),
                        }
                    )
                else:
                    results.append({"return": 0.0, "accuracy": 0.0, "selected": 0})

            except Exception as e:
                print(f"Error at test_idx {test_idx}: {e}")
                results.append({"return": 0.0, "accuracy": 0.0, "selected": 0})

        return results

    def run_validation(self, monthly_data):
        """
        运行完整的walk-forward验证

        参数:
            monthly_data: dict, {idx: {'feat': df, 'label': series, 'ret': series, 'date': date}}

        返回:
            results_df: DataFrame, 各模型的评估指标汇总
            raw_results: dict, 各模型的原始月度收益
        """
        valid_indices = sorted(monthly_data.keys())

        if len(valid_indices) < self.train_months + 6:
            raise ValueError(
                f"数据不足：需要至少{self.train_months + 6}个月，当前只有{len(valid_indices)}个月"
            )

        print(f"有效月数: {len(valid_indices)}")
        print(f"训练窗口: {self.train_months}个月")
        print(f"样本外月数: {len(valid_indices) - self.train_months}")

        raw_results = {}

        for name, model in self.models.items():
            print(f"\n验证模型: {name}")
            results = self.validate_single_model(
                name, model, monthly_data, valid_indices
            )
            raw_results[name] = [r["return"] for r in results]

        # 汇总结果
        summary_rows = []
        for name, rets in raw_results.items():
            if not rets:
                continue

            s = pd.Series(rets)
            cum = (1 + s).cumprod()

            # 计算指标
            total_months = len(s)
            ann_return = cum.iloc[-1] ** (12 / total_months) - 1
            max_dd = (cum / cum.cummax() - 1).min()
            sharpe = s.mean() / s.std() * (12**0.5) if s.std() > 0 else 0
            win_rate = (s > 0).mean()
            avg_return = s.mean()
            volatility = s.std()

            summary_rows.append(
                {
                    "模型": name,
                    "年化收益": ann_return,
                    "最大回撤": max_dd,
                    "夏普比率": sharpe,
                    "月胜率": win_rate,
                    "月均收益": avg_return,
                    "月波动率": volatility,
                    "样本月数": total_months,
                }
            )

        results_df = pd.DataFrame(summary_rows).set_index("模型")
        return results_df, raw_results

    def check_data_leakage(self, monthly_data):
        """
        检查潜在的数据泄露风险
        """
        print("\n" + "=" * 60)
        print("数据泄露风险检查")
        print("=" * 60)

        valid_indices = sorted(monthly_data.keys())

        # 检查1：特征和标签的时间错位
        for idx in valid_indices[:3]:
            data = monthly_data[idx]
            date = data.get("date", "Unknown")
            feat_stocks = set(data["feat"].index)
            ret_stocks = set(data["ret"].index)

            overlap = feat_stocks.intersection(ret_stocks)
            print(f"\n月份 {date}:")
            print(f"  特征股票数: {len(feat_stocks)}")
            print(f"  收益股票数: {len(ret_stocks)}")
            print(f"  重叠股票数: {len(overlap)}")

        # 检查2：训练窗口是否包含未来数据
        print(f"\n训练窗口检查:")
        print(f"  训练窗口长度: {self.train_months}个月")
        print(f"  最早数据索引: {valid_indices[0]}")
        print(f"  最晚数据索引: {valid_indices[-1]}")
        print(f"  第一个预测月: {valid_indices[self.train_months]}")

        # 检查3：特征标准化是否泄露
        print(f"\n特征处理检查:")
        print(f"  特征列数: {len(self.feature_cols)}")
        print(f"  去极值: 使用1%/99%分位数")
        print(f"  标准化: 仅在训练窗口内拟合")

        print("\n" + "=" * 60)
        print("检查完成。如上设置正确，则无明显的未来函数泄露。")
        print("=" * 60)


def generate_sample_data(n_months=48, n_stocks=300, seed=42):
    """
    生成模拟数据用于验证框架测试
    实际使用时应替换为真实数据
    """
    np.random.seed(seed)

    dates = pd.date_range("2020-01-01", periods=n_months, freq="ME")
    stocks = [f"STOCK_{i:04d}" for i in range(n_stocks)]

    monthly_data = {}

    for idx, date in enumerate(dates):
        # 生成特征（模拟基本面因子）
        feat = pd.DataFrame(
            np.random.randn(n_stocks, 14),
            index=stocks,
            columns=[
                "EP",
                "BP",
                "SP",
                "CFP",
                "pe_ratio",
                "pb_ratio",
                "ps_ratio",
                "pcf_ratio",
                "roe",
                "roa",
                "gross_profit_margin",
                "net_profit_to_total_revenue",
                "inc_net_profit_year_on_year",
                "inc_revenue_year_on_year",
            ],
        )

        # 添加市值
        feat["market_cap"] = np.random.lognormal(15, 1.5, n_stocks)
        feat["log_market_cap"] = np.log(feat["market_cap"])

        # 生成收益率（加入微弱的因子预测性）
        base_return = np.random.randn(n_stocks) * 0.1
        factor_signal = 0.02 * (feat["EP"] + feat["BP"] + feat["roe"])
        returns = base_return + factor_signal

        # 创建标签
        label = (returns > returns.median()).astype(int)

        monthly_data[idx] = {
            "feat": feat,
            "label": label,
            "ret": pd.Series(returns, index=stocks),
            "date": date,
        }

    return monthly_data


def format_results(results_df):
    """格式化结果输出"""
    formatted = results_df.copy()

    formatted["年化收益"] = formatted["年化收益"].apply(lambda x: f"{x:.2%}")
    formatted["最大回撤"] = formatted["最大回撤"].apply(lambda x: f"{x:.2%}")
    formatted["夏普比率"] = formatted["夏普比率"].apply(lambda x: f"{x:.3f}")
    formatted["月胜率"] = formatted["月胜率"].apply(lambda x: f"{x:.1%}")
    formatted["月均收益"] = formatted["月均收益"].apply(lambda x: f"{x:.4f}")
    formatted["月波动率"] = formatted["月波动率"].apply(lambda x: f"{x:.4f}")

    return formatted


# ========== 主程序 ==========
if __name__ == "__main__":
    print("=" * 70)
    print("ML多因子Walk-Forward验证框架")
    print("=" * 70)

    # 生成模拟数据（实际使用时替换为真实数据）
    print("\n生成模拟数据...")
    monthly_data = generate_sample_data(n_months=48, n_stocks=300)
    print(f"生成 {len(monthly_data)} 个月的数据")

    # 初始化验证器
    validator = MLWalkForwardValidator(
        train_months=12, hold_n=20, cost=0.001, top_pct=0.3
    )

    # 运行数据泄露检查
    validator.check_data_leakage(monthly_data)

    # 运行验证
    print("\n开始Walk-Forward验证...")
    results_df, raw_results = validator.run_validation(monthly_data)

    # 输出结果
    print("\n" + "=" * 70)
    print("【ML Walk-Forward 对比汇总】")
    print("=" * 70)

    formatted = format_results(results_df)
    print(formatted.to_string())

    # 判断标准
    print("\n" + "=" * 70)
    print("【判断标准】")
    print("=" * 70)

    best_model = results_df["夏普比率"].idxmax()
    worst_model = results_df["夏普比率"].idxmin()

    print(f"最值得保留的模型: {best_model}")
    print(f"  - 夏普比率: {results_df.loc[best_model, '夏普比率']:.3f}")
    print(f"  - 年化收益: {results_df.loc[best_model, '年化收益']:.2%}")

    print(f"\n淘汰理由最充分的模型: {worst_model}")
    print(f"  - 夏普比率: {results_df.loc[worst_model, '夏普比率']:.3f}")
    print(f"  - 年化收益: {results_df.loc[worst_model, '年化收益']:.2%}")

    # 结论
    print("\n" + "=" * 70)
    print("【结论判断】")
    print("=" * 70)

    best_sharpe = results_df.loc[best_model, "夏普比率"]
    if best_sharpe > 0.8:
        print("夏普 > 0.8，ML线值得考虑工程化")
    elif best_sharpe > 0.3:
        print("夏普在0.3-0.8之间，ML线需要进一步研究")
    else:
        print("夏普 < 0.3，ML线暂不值得先跑")

    print("\n注意：以上为模拟数据验证，实际结果需用真实聚宽数据运行")
