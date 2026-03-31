"""
Step 3: 机器学习因子选择模型

目标：构建动态因子选择模型，预测未来收益
方法：XGBoost回归，提供因子重要性

RiceQuant Notebook 运行方式：
node run-strategy.js --strategy step3_ml_model.py --timeout-ms 600000

注意：RiceQuant环境可能没有XGBoost库
      这里提供两种方案：
      1. 如果有XGBoost，使用XGBoost
      2. 如果没有，使用简单的线性回归作为替代
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

print("=" * 60)
print("Step 3: 机器学习因子选择模型")
print("=" * 60)

# ============================================================
# 1. 检查机器学习库
# ============================================================
print("\n[1. 检查机器学习库]")

try:
    import xgboost as xgb

    HAS_XGBOOST = True
    print("✓ XGBoost可用")
except ImportError:
    HAS_XGBOOST = False
    print("✗ XGBoost不可用，将使用线性回归替代")

try:
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, r2_score

    HAS_SKLEARN = True
    print("✓ sklearn可用")
except ImportError:
    HAS_SKLEARN = False
    print("✗ sklearn不可用，将使用简化方法")

# ============================================================
# 2. 数据准备函数
# ============================================================
print("\n[2. 数据准备]")


def prepare_training_data(stock_list, lookback_days=60):
    """
    准备训练数据

    返回：
    - X: 因子矩阵
    - y: 未来收益（目标变量）
    - stock_codes: 股票代码列表
    """

    X_list = []
    y_list = []
    codes_list = []

    for stock in stock_list:
        try:
            # 获取历史数据
            bars = history_bars(stock, lookback_days + 10, "1d", ["close", "volume"])

            if bars is None or len(bars) < lookback_days:
                continue

            close = bars["close"]
            volume = bars["volume"]

            # 计算因子（特征）
            momentum_20 = (
                (close[-1] / close[-21] - 1) * 100 if len(close) >= 21 else None
            )
            momentum_10 = (
                (close[-1] / close[-11] - 1) * 100 if len(close) >= 11 else None
            )
            ma_deviation = (
                (close[-1] / np.mean(close[-20:]) - 1) * 100
                if len(close) >= 20
                else None
            )
            volatility = (
                np.std(np.diff(close[-20:]) / close[-21:-1]) * 100
                if len(close) >= 21
                else None
            )
            volume_ratio = (
                np.mean(volume[-5:]) / np.mean(volume[-20:])
                if len(volume) >= 20 and np.mean(volume[-20:]) > 0
                else None
            )

            # 价格位置（相对高低点）
            price_high = np.max(close[-20:])
            price_low = np.min(close[-20:])
            price_pos = (
                (close[-1] - price_low) / (price_high - price_low)
                if price_high != price_low
                else 0.5
            )

            # 未来收益（目标变量）
            # 用后5天的收益作为预测目标
            future_return = (
                (close[-1] / close[-6] - 1) * 100 if len(close) >= 6 else None
            )

            # 检查所有值都有效
            features = [
                momentum_20,
                momentum_10,
                ma_deviation,
                volatility,
                volume_ratio,
                price_pos,
            ]
            if (
                all(v is not None and not np.isnan(v) for v in features)
                and future_return is not None
            ):
                X_list.append(features)
                y_list.append(future_return)
                codes_list.append(stock)

        except Exception as e:
            continue

    if not X_list:
        return None, None, None

    X = np.array(X_list)
    y = np.array(y_list)

    return X, y, codes_list


# ============================================================
# 3. 获取训练数据
# ============================================================
print("\n[3. 获取训练数据]")

try:
    # 使用沪深300成分股作为训练样本
    hs300 = index_components("000300.XSHG")
    test_stocks = [s for s in hs300 if not s.startswith("688")][:80]

    print(f"训练股票数量: {len(test_stocks)}")

    X, y, codes = prepare_training_data(test_stocks, lookback_days=60)

    if X is not None:
        print(f"训练样本数: {len(X)}")
        print(f"特征数: {X.shape[1]}")
        print(f"目标变量范围: [{y.min():.2f}%, {y.max():.2f}%]")
    else:
        print("数据准备失败")

except Exception as e:
    print(f"获取数据失败: {e}")
    X, y, codes = None, None, None

# ============================================================
# 4. 模型训练
# ============================================================
print("\n[4. 模型训练]")

model = None
feature_importance = None

if X is not None and HAS_SKLEARN:
    # 分割训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"训练集大小: {len(X_train)}")
    print(f"测试集大小: {len(X_test)}")

    if HAS_XGBOOST:
        # 使用XGBoost
        print("\n使用XGBoost模型...")
        model = xgb.XGBRegressor(
            n_estimators=50, max_depth=3, learning_rate=0.1, random_state=42
        )
        model.fit(X_train, y_train)

        # 获取特征重要性
        feature_importance = model.feature_importances_

    else:
        # 使用线性回归
        print("\n使用线性回归模型...")
        model = LinearRegression()
        model.fit(X_train, y_train)

        # 使用系数绝对值作为重要性
        feature_importance = np.abs(model.coef_)

    # 预测
    y_pred = model.predict(X_test)

    # 评估
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\n模型评估:")
    print(f"  MSE: {mse:.4f}")
    print(f"  R²: {r2:.4f}")

    if r2 > 0:
        print("  ✓ 模型有一定预测能力")
    else:
        print("  ✗ 模型预测能力较弱")

# ============================================================
# 5. 因子重要性分析
# ============================================================
print("\n[5. 因子重要性分析]")

if feature_importance is not None:
    feature_names = [
        "momentum_20",
        "momentum_10",
        "ma_deviation",
        "volatility",
        "volume_ratio",
        "price_pos",
    ]

    # 创建重要性DataFrame
    importance_df = pd.DataFrame(
        {"factor": feature_names, "importance": feature_importance}
    )

    # 排序
    importance_df = importance_df.sort_values("importance", ascending=False)

    print("\n因子重要性排序:")
    for i, row in importance_df.iterrows():
        print(f"  {row['factor']:20s}: {row['importance']:.4f}")

    # 归一化重要性
    total_importance = importance_df["importance"].sum()
    if total_importance > 0:
        importance_df["weight"] = importance_df["importance"] / total_importance

        print("\n因子权重（归一化）:")
        for i, row in importance_df.iterrows():
            print(f"  {row['factor']:20s}: {row['weight'] * 100:.1f}%")

# ============================================================
# 6. 选股示例
# ============================================================
print("\n[6. 选股示例]")

if model is not None and X is not None:
    # 对所有股票预测收益
    y_all_pred = model.predict(X)

    # 创建结果DataFrame
    result_df = pd.DataFrame({"code": codes, "predicted_return": y_all_pred})

    # 按预测收益排序
    result_df = result_df.sort_values("predicted_return", ascending=False)

    print("\n预测收益最高的10只股票:")
    print(result_df.head(10).to_string(index=False))

    print("\n预测收益最低的10只股票:")
    print(result_df.tail(10).to_string(index=False))

# ============================================================
# 7. 模型保存建议
# ============================================================
print("\n" + "=" * 60)
print("[模型总结]")
print("=" * 60)

if model is not None:
    print(f"""
机器学习因子选择模型构建完成：

1. 模型类型：
   {"XGBoost" if HAS_XGBOOST else "线性回归"}

2. 因子重要性排序：
""")

    if importance_df is not None:
        for i, row in importance_df.head(3).iterrows():
            print(f"   {i + 1}. {row['factor']}: {row['importance']:.4f}")

    print(f"""
3. 模型评估：
   - R²: {r2:.4f}
   - {"预测能力尚可" if r2 > 0 else "预测能力较弱，需改进"}

4. 改进建议：
   - 增加训练样本数量
   - 尝试不同的特征组合
   - 加入基本面因子（PE/PB/ROE等）
   - 使用滚动训练更新模型

5. 下一步：
   - Step4: 将模型应用于选股策略
   - 验证策略回测表现
""")
else:
    print("""
模型构建失败，可能的原因：
- 数据不足
- 缺少机器学习库
- API限制

建议：
- 在策略编辑器环境中运行
- 使用JoinQuant平台的机器学习API
""")

print("\n" + "=" * 60)
print("Step 3 完成")
print("=" * 60)
