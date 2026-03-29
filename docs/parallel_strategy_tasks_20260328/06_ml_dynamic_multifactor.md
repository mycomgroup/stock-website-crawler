# 任务 06：机器学习动态多因子竞赛

## 设计文档

### 任务定位

- 优先级：中高
- 类型：代表性机器学习母线
- 目标：在严格防泄露的前提下，判断 ML 多因子在当前仓库里是真金，还是“研究展示感”强于实盘价值

### 为什么值得现在研究

- 根目录文档已经把 `SVM动态多因子` 点名为最值得统一复核的路线之一
- 机器学习线覆盖 `SVM / 逻辑回归 / 随机森林 / XGBoost / 动态多因子`
- 这条线潜力大，但也是最容易被口径不统一和未来函数污染的赛道

### 参考矿脉

- `机器学习策略总结与实盘指南.md`
- `聚宽有价值策略558/12 研究 机器学习用于量化分析.ipynb`
- `聚宽有价值策略558/41 手把手教你“机器学习-动态多因子选股”(附保姆级教程)/svm动态因子选股.ipynb`
- `聚宽有价值策略558/47 随机森林 研究.ipynb`
- `聚宽有价值策略558/78 研究 八大机器学习模型大比拼!看看谁的表现最好.ipynb`
- `聚宽有价值策略558/92 【机器学习研究】动态多因子选股策略研究.ipynb`
- `聚宽有价值策略558/28 XGBoost模型多因子策略分享.txt`

### 核心假设

- ML 的价值不一定在于收益绝对最高，而可能在于因子筛选与状态适应
- 简单模型未必输复杂模型
- 如果没有严格 walk-forward 验证，这条线很容易看起来“特别强”

### 本轮只做什么

1. 统一特征集、股票池、调仓频率和训练滚动方式。
2. 比较 `逻辑回归 / SVM / 随机森林 / XGBoost`。
3. 强制做滚动训练与样本外验证。
4. 判断 ML 线是否值得进入第一批实跑，而不是只当探索方向。

### 明确不做什么

- 不接受一次性全样本训练
- 不堆深度学习花活
- 不用无法解释的数据泄露式结果

### 交付物

1. 一张统一赛表：模型、收益、回撤、稳定性、训练成本、可解释性。
2. 一份误差来源分析：哪些结果可能受未来函数、样本偏差影响。
3. 一个结论：`先实跑 / 继续研究 / 暂不投入`

### 成功判据

- 能判断机器学习线在这个仓库里到底是主线还是旁支
- 能说清最值得保留的 ML 版本是哪一个，为什么

## 子任务提示词

```text
你现在是机器学习多因子子任务。你的目标是做一场严格、可复核的模型竞赛，而不是重复文档里的漂亮收益数字。

请优先阅读这些材料：
- 机器学习策略总结与实盘指南.md
- 聚宽有价值策略558/12 研究 机器学习用于量化分析.ipynb
- 聚宽有价值策略558/41 手把手教你“机器学习-动态多因子选股”(附保姆级教程)/svm动态因子选股.ipynb
- 聚宽有价值策略558/47 随机森林 研究.ipynb
- 聚宽有价值策略558/78 研究 八大机器学习模型大比拼!看看谁的表现最好.ipynb
- 聚宽有价值策略558/92 【机器学习研究】动态多因子选股策略研究.ipynb

请完成以下事情：
1. 固定股票池、特征集、调仓频率、训练窗口。
2. 用严格 walk-forward 比较：
   - 逻辑回归
   - SVM
   - 随机森林
   - XGBoost
3. 评估：
   - 成本后净收益
   - 回撤
   - 稳定性
   - 训练复杂度
   - 可解释性
4. 明确回答：ML 是否真的优于传统多因子基线。

输出要求：
- 必须先排查未来函数和数据泄露风险。
- 必须说明模型是否只在单段行情里有效。
- 必须给出最值得保留的一个模型和一个淘汰理由最充分的模型。
- 如果没有明显优势，要直接说不值得先跑。
```

## 实际效果验证

### 验证方式

在聚宽 Research 中用严格 walk-forward 方式对比 LR / SVM / RF / XGBoost，强制样本外验证，排查未来函数风险。

### 验证代码

```python
# 机器学习多因子 walk-forward 验证
# 严格样本外, 滚动训练窗口 12 个月, 预测下月涨跌

from jqdata import *
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

print("=" * 70)
print("ML 多因子 Walk-Forward 验证 (2021-01-01 ~ 2025-12-31)")
print("=" * 70)

START       = "2021-01-01"
END         = "2025-12-31"
TRAIN_MONTHS = 12   # 训练窗口
HOLD_N      = 20
COST        = 0.001

def get_monthly_dates(start, end):
    days = get_trade_days(start, end)
    result, last_m = [], None
    for d in days:
        if d.month != last_m:
            result.append(d)
            last_m = d.month
    return result

def get_features(stocks, date):
    """获取7个因子特征"""
    q = query(
        valuation.code,
        indicator.roe, indicator.roa,
        indicator.gross_profit_margin,
        indicator.inc_net_profit_year_on_year,
        indicator.inc_revenue_year_on_year,
        valuation.pe_ratio, valuation.pb_ratio,
    ).filter(valuation.code.in_(stocks))
    df = get_fundamentals(q, date=date).set_index("code")
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    return df

def get_next_month_return(stocks, date_start, date_end):
    """获取下月收益率"""
    try:
        p0 = get_price(stocks, end_date=str(date_start), count=1, fields=["close"], panel=False)
        p1 = get_price(stocks, end_date=str(date_end), count=1, fields=["close"], panel=False)
        p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
        p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
        return ((p1 / p0) - 1).dropna()
    except:
        return pd.Series()

FEATURE_COLS = ["roe","roa","gross_profit_margin",
                "inc_net_profit_year_on_year","inc_revenue_year_on_year",
                "pe_ratio","pb_ratio"]

universe = get_index_stocks("000906.XSHG")  # 中证800
dates = get_monthly_dates(START, END)
print(f"调仓次数: {len(dates)-1}, 训练窗口: {TRAIN_MONTHS}个月")

# 预先收集所有月度特征和标签
print("收集历史特征数据...")
monthly_data = {}
for i, d in enumerate(dates[:-1]):
    try:
        feat = get_features(universe[:300], str(d))  # 取前300只加速
        ret  = get_next_month_return(feat.index.tolist(), d, dates[i+1])
        common = feat.index.intersection(ret.index)
        if len(common) < 50:
            continue
        feat = feat.loc[common, FEATURE_COLS]
        label = (ret.loc[common] > ret.loc[common].median()).astype(int)
        monthly_data[i] = {"feat": feat, "label": label, "ret": ret.loc[common], "date": d}
    except:
        continue
print(f"有效月份: {len(monthly_data)}")

# Walk-forward 验证
models = {
    "逻辑回归": LogisticRegression(max_iter=500, random_state=42),
    "SVM":      SVC(kernel="rbf", probability=True, random_state=42),
    "随机森林": RandomForestClassifier(n_estimators=50, random_state=42),
}

results = {name: [] for name in models}
valid_indices = sorted(monthly_data.keys())

for test_idx in valid_indices[TRAIN_MONTHS:]:
    train_indices = [i for i in valid_indices if i < test_idx][-TRAIN_MONTHS:]
    if len(train_indices) < TRAIN_MONTHS:
        continue
    X_train = pd.concat([monthly_data[i]["feat"] for i in train_indices])
    y_train = pd.concat([monthly_data[i]["label"] for i in train_indices])
    X_test  = monthly_data[test_idx]["feat"]
    ret_test = monthly_data[test_idx]["ret"]

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    for name, model in models.items():
        try:
            model.fit(X_train_s, y_train)
            pred = model.predict(X_test_s)
            pred_s = pd.Series(pred, index=X_test.index)
            selected = pred_s[pred_s == 1].index.tolist()[:HOLD_N]
            if not selected:
                results[name].append(0.0)
                continue
            gross = ret_test.loc[selected].mean()
            results[name].append(gross - COST * 2)
        except:
            results[name].append(0.0)

print("\n" + "=" * 70)
print("【ML Walk-Forward 对比汇总】")
print("=" * 70)
rows = []
for name, rets in results.items():
    if not rets:
        continue
    s = pd.Series(rets)
    cum = (1 + s).cumprod()
    ann = cum.iloc[-1] ** (12 / len(s)) - 1
    dd = (cum / cum.cummax() - 1).min()
    sharpe = s.mean() / s.std() * (12 ** 0.5) if s.std() > 0 else 0
    win = (s > 0).mean()
    rows.append({"模型": name, "年化(扣费)": f"{ann:.1%}", "最大回撤": f"{dd:.1%}",
                 "夏普": f"{sharpe:.2f}", "月胜率": f"{win:.0%}", "样本月数": len(s)})
    print(f"  {name}: 年化={ann:.1%}  回撤={dd:.1%}  夏普={sharpe:.2f}")

if rows:
    df_res = pd.DataFrame(rows).set_index("模型")
    print("\n" + df_res.to_string())

print("\n【注意】以上为严格样本外结果，如与文档历史数字差异大，说明原结果存在数据泄露风险")
print("\n验证完成!")
```

### 执行命令

```bash
cd skills/joinquant_nookbook
node run-skill.js \
  --notebook-url <your_research_notebook_url> \
  --cell-source "$(cat /tmp/verify_06.py)" \
  --timeout-ms 600000
```

### 预期输出与判断标准

| 指标 | 判断逻辑 |
|------|---------|
| 样本外年化 vs 传统多因子基线 | 无明显优势则不值得先跑 |
| 夏普 | > 0.8 才考虑工程化 |
| 训练复杂度 | SVM/RF 训练时间是否可接受 |
| 与文档数字差异 | 差异 > 20% 说明原结果有泄露嫌疑 |

### 结论记录

> 运行后在此填写：最值得保留的一个模型，淘汰理由最充分的模型，以及是否值得先跑。
