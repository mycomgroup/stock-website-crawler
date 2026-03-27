"""
机器学习模型对比测试 - 基于最近数据实测
测试逻辑回归、随机森林、SVM、XGBoost在中证500成分股上的选股效果
测试期：2024-01-01 至今
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
from sklearn.model_selection import cross_val_score
import xgboost as xgb

print("=" * 60)
print("机器学习模型选股对比测试")
print("=" * 60)

# ==================== 参数设置 ====================
START_DATE = "2022-01-01"
TRAIN_END = "2024-06-30"
TEST_START = "2024-07-01"
TEST_END = datetime.datetime.now().strftime("%Y-%m-%d")
INDEX = "000905.XSHG"  # 中证500

print(f"训练期: {START_DATE} 至 {TRAIN_END}")
print(f"测试期: {TEST_START} 至 {TEST_END}")
print()


# ==================== 工具函数 ====================
def get_stocks_filtered(date, indexID=INDEX):
    """获取过滤后的股票池"""
    stocks = get_index_stocks(indexID, date=date)
    # 去除ST
    is_st = get_extras("is_st", stocks, end_date=date, count=1)
    stocks = [s for s in stocks if not is_st[s][0]]
    # 去除上市不足1年
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    stocks = [
        s
        for s in stocks
        if get_security_info(s).start_date
        < (date_obj - datetime.timedelta(days=365)).date()
    ]
    # 去除停牌
    paused = get_price(stocks, end_date=date, count=1, fields="paused", panel=False)
    stocks = list(paused[paused["paused"] != 1]["code"])
    return stocks


def get_features(stocks, date):
    """获取特征数据"""
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

    # 计算衍生因子
    df["EP"] = 1 / df["pe_ratio"]
    df["BP"] = 1 / df["pb_ratio"]
    df["SP"] = 1 / df["ps_ratio"]
    df["CFP"] = 1 / df["pcf_ratio"]
    df["log_market_cap"] = np.log(df["market_cap"])

    # 获取技术指标
    for stock in stocks[:100]:  # 限制数量避免超时
        try:
            prices = get_price(
                stock, end_date=date, count=60, fields=["close", "volume"]
            )
            if len(prices) >= 20:
                df.loc[stock, "return_20d"] = (
                    prices["close"].iloc[-1] / prices["close"].iloc[0] - 1
                ) * 100
                df.loc[stock, "vol_20d"] = (
                    prices["close"].pct_change().std() * np.sqrt(252) * 100
                )
                df.loc[stock, "volume_ratio"] = (
                    prices["volume"].iloc[-5:].mean() / prices["volume"].mean()
                )
        except:
            pass

    return df.dropna()


def get_forward_return(stocks, start_date, end_date, period=20):
    """获取未来N日收益率"""
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


def process_features(df, date):
    """特征预处理"""
    # 去极值
    for col in df.select_dtypes(include=[np.number]).columns:
        q1 = df[col].quantile(0.01)
        q99 = df[col].quantile(0.99)
        df[col] = df[col].clip(q1, q99)
    # 标准化
    df = (df - df.mean()) / df.std()
    return df.fillna(0)


# ==================== 数据准备 ====================
print("正在获取训练数据...")

# 获取月末交易日
trade_days = get_trade_days(START_DATE, TEST_END)
month_ends = []
for i in range(len(trade_days) - 1):
    if trade_days[i].month != trade_days[i + 1].month:
        month_ends.append(trade_days[i].strftime("%Y-%m-%d"))

train_months = [d for d in month_ends if d <= TRAIN_END]
test_months = [d for d in month_ends if d >= TEST_START]

print(f"训练期月数: {len(train_months)}")
print(f"测试期月数: {len(test_months)}")

# 准备训练数据
train_data = []
for date in train_months:
    try:
        stocks = get_stocks_filtered(date)
        if len(stocks) < 50:
            continue
        features = get_features(stocks[:100], date)

        # 获取下月收益
        next_month_idx = month_ends.index(date) + 1
        if next_month_idx < len(month_ends):
            next_date = month_ends[next_month_idx]
            returns = get_forward_return(features.index.tolist(), date, next_date)

            # 合并数据
            features["return"] = returns
            features = features.dropna()

            # 标签: 前30%为1，后30%为0
            features = features.sort_values("return", ascending=False)
            n = len(features) // 3
            features["label"] = np.nan
            features.iloc[:n, -1] = 1
            features.iloc[-n:, -1] = 0
            features = features.dropna()

            train_data.append(features)
        print(f"  处理完成: {date}")
    except Exception as e:
        print(f"  跳过 {date}: {e}")

train_df = pd.concat(train_data)
print(f"\n训练样本数: {len(train_df)}")

# 特征列
feature_cols = [
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

X_train = process_features(train_df[feature_cols], None)
y_train = train_df["label"]

# ==================== 模型训练 ====================
print("\n正在训练模型...")

models = {
    "Logistic": LogisticRegression(C=100, max_iter=500),
    "RandomForest": RandomForestClassifier(
        n_estimators=100, max_depth=5, random_state=42
    ),
    "SVM": SVC(probability=True, kernel="rbf", random_state=42),
    "XGBoost": xgb.XGBClassifier(
        n_estimators=100, max_depth=5, random_state=42, use_label_encoder=False
    ),
}

trained_models = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    trained_models[name] = model
    # 交叉验证
    cv_score = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy").mean()
    print(f"  {name}: CV Accuracy = {cv_score:.4f}")

# ==================== 样本外测试 ====================
print("\n正在进行样本外测试...")

results = {name: [] for name in models.keys()}
benchmark_returns = []

for date in test_months:
    try:
        stocks = get_stocks_filtered(date)
        if len(stocks) < 50:
            continue
        features = get_features(stocks[:100], date)

        # 获取下月收益
        next_month_idx = test_months.index(date) + 1
        if next_month_idx < len(test_months):
            next_date = test_months[next_month_idx]
            forward_returns = get_forward_return(
                features.index.tolist(), date, next_date
            )

            # 特征处理
            X_test = process_features(features[feature_cols], None)

            for name, model in trained_models.items():
                try:
                    # 预测概率
                    proba = model.predict_proba(X_test)[:, 1]
                    # 选前30%股票
                    pred_df = pd.DataFrame({"code": X_test.index, "prob": proba})
                    pred_df = pred_df.sort_values("prob", ascending=False)
                    top_n = len(pred_df) // 3
                    selected = pred_df.head(top_n)["code"].tolist()
                    # 计算组合收益
                    if selected:
                        port_return = forward_returns[
                            forward_returns.index.isin(selected)
                        ].mean()
                        results[name].append(port_return)
                except Exception as e:
                    results[name].append(np.nan)

            # 基准收益
            benchmark_returns.append(forward_returns.mean())

        print(f"  测试完成: {date}")
    except Exception as e:
        print(f"  跳过 {date}: {e}")

# ==================== 结果汇总 ====================
print("\n" + "=" * 60)
print("测试结果汇总")
print("=" * 60)

results_df = pd.DataFrame(results)
results_df["Benchmark"] = benchmark_returns[: len(results_df)]

# 计算累计收益
cum_returns = (1 + results_df).cumprod()

print("\n--- 累计收益 ---")
print(cum_returns.iloc[-1].sort_values(ascending=False))

print("\n--- 月度统计 ---")
for col in results_df.columns:
    ret = results_df[col].dropna()
    print(f"\n{col}:")
    print(f"  月均收益: {ret.mean() * 100:.2f}%")
    print(f"  月胜率: {(ret > 0).mean() * 100:.1f}%")
    print(f"  最大单月亏损: {ret.min() * 100:.2f}%")
    print(f"  最大单月盈利: {ret.max() * 100:.2f}%")
    if col != "Benchmark":
        excess = ret - results_df["Benchmark"].dropna()
        print(f"  月均超额: {excess.mean() * 100:.2f}%")
        print(f"  超额胜率: {(excess > 0).mean() * 100:.1f}%")

print("\n--- 净值曲线 ---")
print(cum_returns.tail())

print("\n测试完成!")
