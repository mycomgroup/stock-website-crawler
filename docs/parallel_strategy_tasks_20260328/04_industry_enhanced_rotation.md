# 任务 04：行业增强型轮动

## 设计文档

### 任务定位

- 优先级：高
- 类型：ETF 线中观增强
- 目标：判断行业趋势、拥挤、景气与板块热度，是否真的能提升 ETF 轮动质量

### 为什么值得现在研究

- ETF 动量本身已经是一条清晰主线，但缺少“为什么买它”的解释层
- 行业增强是从代表性母策略走向更稳健组合框架的关键一步
- 这条线更偏新增价值，而不是重复做 ETF 基线

### 参考矿脉

- `ETF轮动与择时_总结与后续工作.md`
- `聚宽有价值策略558/29 【策略.行业轮动】趋势-拥挤-景气度模型看行业轮动.ipynb`
- `聚宽有价值策略558/64 A股最强板块动量趋势（最终版）.ipynb`
- `聚宽有价值策略558/51 【复现】行业有效量价因子与行业轮动策略ETF.ipynb`
- `聚宽有价值策略558/02 研究 板块轮动打分与热度追踪.ipynb`
- `聚宽有价值策略558/56 基于趋势、拥挤、景气的行业轮动，及行业强势个股的选择.txt`

### 核心假设

- 纯 ETF 动量负责“横截面排序”
- 行业增强负责“先验方向过滤”
- 板块热度与中观景气可能能提升信号解释性，但不一定直接带来更高收益

### 本轮只做什么

1. 还原 `趋势-拥挤-景气` 的三维行业评分。
2. 比较 `不做行业预筛 / 先选强行业再进 ETF / 板块热度辅助确认`。
3. 判断行业增强是改善收益、改善回撤，还是只改善可解释性。
4. 给出一版可插拔行业增强模块。

### 明确不做什么

- 不跟 ETF 基线任务重复搭候选池
- 不用几十个行业指标重新发明评分系统
- 不把“股票因子在行业上有效”默认视为“ETF 上也有效”

### 交付物

1. 一张行业增强方案对比表。
2. 一份行业信号解释：当前更偏哪些行业，为什么。
3. 一个结论：行业增强应该作为必选层、可选层，还是暂时放弃。

### 成功判据

- 能判断行业增强是否真的值得接入
- 能给 ETF 轮动增加一层更像“研究资产”而不是“黑箱净值”的解释框架

## 子任务提示词

```text
你现在是行业增强子任务。请判断行业趋势、拥挤、景气、板块热度这些中观信号，是否值得接到 ETF 轮动框架里。

请优先阅读这些材料：
- ETF轮动与择时_总结与后续工作.md
- 聚宽有价值策略558/29 【策略.行业轮动】趋势-拥挤-景气度模型看行业轮动.ipynb
- 聚宽有价值策略558/64 A股最强板块动量趋势（最终版）.ipynb
- 聚宽有价值策略558/51 【复现】行业有效量价因子与行业轮动策略ETF.ipynb
- 聚宽有价值策略558/02 研究 板块轮动打分与热度追踪.ipynb

请完成以下事情：
1. 还原行业打分框架：趋势、拥挤、景气、板块热度分别怎么定义。
2. 用统一 ETF 基线做对照，比较：
   - 不做行业预筛
   - 行业预筛后再做 ETF 排序
   - 行业预筛 + 板块热度确认
3. 明确说明：
   - 行业增强带来的收益改善是否稳定
   - 是否只是让策略更好解释，而不是更赚钱
   - 是否引入了更多参数依赖

输出要求：
- 必须给出“值不值得接入”的判断。
- 必须写出当前市场更偏哪些行业，以及这些偏好是否来自价格还是基本面。
- 如果行业增强不稳定，要直接判定降级。
```

## 实际效果验证

### 验证方式

在聚宽 Research 中验证行业增强信号（趋势、拥挤、景气）是否真的提升 ETF 轮动质量，而不是只增加复杂度。

### 验证代码

```python
# 行业增强型轮动验证
# 对比: 不做行业预筛 vs 行业预筛后再做 ETF 排序

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 70)
print("行业增强型轮动验证 (2021-01-01 ~ 2025-12-31)")
print("=" * 70)

START = "2021-01-01"
END   = "2025-12-31"
MOM_WINDOW = 20
HOLD_DAYS  = 10
TOP_N      = 3
COST       = 0.001

# 行业 ETF 池 (申万一级行业代表 ETF)
INDUSTRY_ETF = {
    "医药生物": "512010.XSHG",
    "食品饮料": "159928.XSHE",
    "电子":     "512480.XSHG",
    "新能源":   "516160.XSHG",
    "银行":     "512800.XSHG",
    "军工":     "512660.XSHG",
    "消费":     "159928.XSHE",
    "科技":     "515000.XSHG",
    "地产":     "512200.XSHG",
    "有色金属": "512400.XSHG",
}
CODES = list(set(INDUSTRY_ETF.values()))

def get_rebal_dates(start, end, freq_days):
    all_days = get_trade_days(start, end)
    result = [all_days[0]]
    for d in all_days[1:]:
        if (d - result[-1]).days >= freq_days:
            result.append(d)
    return result

def calc_industry_score(code, date, trend_w=20, crowd_w=60):
    """计算单个行业 ETF 的趋势+拥挤综合得分"""
    try:
        prices = get_price(code, end_date=str(date), count=crowd_w+1,
                           fields=["close","volume"], panel=False)
        if len(prices) < crowd_w:
            return 0
        close = prices["close"]
        vol   = prices["volume"]
        # 趋势分: 价格 > MA20
        trend_score = 1 if close.iloc[-1] > close.rolling(trend_w).mean().iloc[-1] else -1
        # 拥挤分: 成交量 vs 60日均量 (过热则降分)
        vol_ratio = vol.iloc[-1] / vol.rolling(crowd_w).mean().iloc[-1]
        crowd_score = -1 if vol_ratio > 2.0 else 1
        return trend_score + crowd_score
    except:
        return 0

def run_version(use_industry_filter, label, dates):
    rets = []
    prev_holdings = []
    for i, d in enumerate(dates[:-1]):
        d_str = str(d)
        next_d_str = str(dates[i+1])
        try:
            prices = get_price(CODES, end_date=d_str, count=MOM_WINDOW+1,
                               fields=["close"], panel=False)
            pivot = prices.pivot(index="time", columns="code", values="close").dropna(axis=1)
            if len(pivot) < MOM_WINDOW + 1:
                continue
            mom = (pivot.iloc[-1] / pivot.iloc[0] - 1)

            if use_industry_filter:
                # 行业预筛: 只保留趋势+拥挤得分 >= 1 的 ETF
                scores = {c: calc_industry_score(c, d) for c in mom.index}
                eligible = [c for c, sc in scores.items() if sc >= 1]
                if len(eligible) < TOP_N:
                    eligible = mom.index.tolist()  # 降级为全池
                mom = mom[eligible]

            selected = mom.nlargest(TOP_N).index.tolist()
            p0 = get_price(selected, end_date=d_str, count=1, fields=["close"], panel=False)
            p1 = get_price(selected, end_date=next_d_str, count=1, fields=["close"], panel=False)
            p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
            gross = ((p1 / p0) - 1).mean()
            turnover = len(set(selected) - set(prev_holdings)) / TOP_N
            rets.append(gross - turnover * COST * 2)
            prev_holdings = selected
        except:
            continue
    if not rets:
        return None
    s = pd.Series(rets)
    cum = (1 + s).cumprod()
    ppy = 252 / HOLD_DAYS
    ann = cum.iloc[-1] ** (ppy / len(s)) - 1
    dd = (cum / cum.cummax() - 1).min()
    sharpe = s.mean() / s.std() * (ppy ** 0.5) if s.std() > 0 else 0
    return {"方案": label, "年化(扣费)": f"{ann:.1%}", "最大回撤": f"{dd:.1%}",
            "夏普": f"{sharpe:.2f}", "样本数": len(s)}

dates = get_rebal_dates(START, END, HOLD_DAYS)
print(f"调仓次数: {len(dates)-1}")

rows = []
for use_filter, label in [(False, "不做行业预筛 (基线)"), (True, "行业趋势+拥挤预筛")]:
    print(f"  运行: {label} ...")
    r = run_version(use_filter, label, dates)
    if r:
        rows.append(r)
        print(f"    年化={r['年化(扣费)']}  回撤={r['最大回撤']}  夏普={r['夏普']}")

print("\n" + "=" * 70)
print("【行业增强对比汇总】")
print("=" * 70)
if rows:
    df_res = pd.DataFrame(rows).set_index("方案")
    print(df_res.to_string())

# 当前行业偏好
print("\n" + "=" * 70)
print("【当前行业 ETF 趋势+拥挤得分】")
print("=" * 70)
today = get_trade_days(end_date="2026-03-28", count=1)[-1]
name_map = {v: k for k, v in INDUSTRY_ETF.items()}
for code in CODES:
    sc = calc_industry_score(code, today)
    name = name_map.get(code, code)
    tag = "✓ 偏多" if sc >= 1 else ("✗ 偏空" if sc <= -1 else "中性")
    print(f"  {name}: 得分={sc}  {tag}")
print("\n验证完成!")
```

### 执行命令

```bash
cd skills/joinquant_nookbook
node run-skill.js \
  --notebook-url <your_research_notebook_url> \
  --cell-source "$(cat /tmp/verify_04.py)" \
  --timeout-ms 300000
```

### 预期输出与判断标准

| 指标 | 判断逻辑 |
|------|---------|
| 行业预筛 vs 基线年化差 | > +2% 才值得作为必选层 |
| 回撤改善 | 有改善则作为可选层 |
| 无明显改善 | 降级为"可解释性辅助"，不强制接入 |

### 结论记录

> 运行后在此填写：行业增强应作为必选层 / 可选层 / 暂时放弃，以及当前偏向哪些行业。
