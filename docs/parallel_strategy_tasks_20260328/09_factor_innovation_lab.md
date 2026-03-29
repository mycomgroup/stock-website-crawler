# 任务 09：新因子探索实验室

## 设计文档

### 任务定位

- 优先级：中
- 类型：新策略探索方向
- 目标：从行为、量价、微观结构、自动挖掘里找出下一批可能长成母策略的信号

### 为什么值得现在研究

- 你的第三个目标是“找到新的策略探索方向”
- 根目录文档已经指出：仓库里不仅有经典多因子，还有 `CGO / 潮汐 / 成交量激增 / 球队硬币 / 遗传算法 / 高频价量相关性`
- 这一条线不一定马上变成实盘策略，但最适合挖“未来两周最值得继续试”的新 alpha

### 参考矿脉

- `多因子选股_notebook梳理.md`
- `聚宽有价值策略558/37 研究 处置效应的CGO因子（行为金融学因子）.ipynb`
- `聚宽有价值策略558/40 研究 基于遗传算法挖掘因子2.ipynb`
- `聚宽有价值策略558/75 方正多因子选股系列研究之一 小镇做题家 成交量激增时刻蕴含的信息.ipynb`
- `聚宽有价值策略558/75 方正多因子选股系列研究之二 小镇做题家 潮汐因子构建.ipynb`
- `聚宽有价值策略558/75 方正多因子选股系列研究之三 小镇做题家 勇攀高峰因子.ipynb`
- `聚宽有价值策略558/81 方正多因子选股系列研究之四 小镇做题家版本：个股动量效应识别及球队硬币因子构建.ipynb`
- `聚宽有价值策略558/96 【复现】高频价量相关性，意想不到的选股因子.txt`

### 核心假设

- 新 alpha 的价值不在于一开始就做成完整策略，而在于找出可叠加、可验证、与已有策略低相关的信号
- 真正有价值的新因子，应该能说明“和 RFScore / ETF 动量不同的东西”
- 因子探索必须关注可实现性与换手成本

### 本轮只做什么

1. 从所有候选里筛出最值得继续试的 3 个信号。
2. 对每个信号做简单有效性检验：IC、分层、稳定性、实现难度。
3. 看它们更适合接到 `股票多因子`、`ETF` 还是 `状态路由器`。
4. 输出一份“下一批值得深挖的新方向榜单”。

### 明确不做什么

- 不做无限制因子海选
- 不因为表达式新奇就判定有效
- 不忽略交易摩擦和数据可得性

### 交付物

1. 一个前三名新因子榜单。
2. 每个因子的有效性与可实现性说明。
3. 一个建议：下一步最值得接到哪条母策略上试。

### 成功判据

- 能从大量“研究味很浓”的材料里，筛出少数真正值得继续挖的信号
- 能明确说出哪些新因子只是故事好听

## 子任务提示词

```text
你现在是新因子探索子任务。你的目标是从仓库里的行为金融、量价、微观结构、自动挖掘材料中，筛出 3 个最值得继续深挖的新信号。

请优先阅读这些材料：
- 多因子选股_notebook梳理.md
- 聚宽有价值策略558/37 研究 处置效应的CGO因子（行为金融学因子）.ipynb
- 聚宽有价值策略558/40 研究 基于遗传算法挖掘因子2.ipynb
- 聚宽有价值策略558/75 方正多因子选股系列研究之一 小镇做题家 成交量激增时刻蕴含的信息.ipynb
- 聚宽有价值策略558/75 方正多因子选股系列研究之二 小镇做题家 潮汐因子构建.ipynb
- 聚宽有价值策略558/75 方正多因子选股系列研究之三 小镇做题家 勇攀高峰因子.ipynb
- 聚宽有价值策略558/81 方正多因子选股系列研究之四 小镇做题家版本：个股动量效应识别及球队硬币因子构建.ipynb
- 聚宽有价值策略558/96 【复现】高频价量相关性，意想不到的选股因子.txt

请完成以下事情：
1. 先列一个候选因子池。
2. 从中筛出最值得继续试的 3 个。
3. 对每个因子回答：
   - 有效性证据够不够
   - 实现难度高不高
   - 更适合接到股票多因子、ETF，还是状态识别
   - 是否容易因为高换手而失真

输出要求：
- 必须输出前三名和淘汰理由。
- 必须区分“研究价值高”和“短期可落地”。
- 如果因子只适合做探索，不适合马上工程化，要直说。
```

## 实际效果验证

### 验证方式

在聚宽 Research 中对 CGO、潮汐因子、成交量激增三个候选新因子做 IC 检验和分层回测，用真实数据判断有效性。

### 验证代码

```python
# 新因子探索实验室 - IC 检验 + 分层回测
# 候选: CGO因子, 潮汐因子, 成交量激增因子

from jqdata import *
import pandas as pd
import numpy as np
from scipy import stats

print("=" * 70)
print("新因子 IC 检验 + 分层回测 (2022-01-01 ~ 2025-12-31)")
print("=" * 70)

START  = "2022-01-01"
END    = "2025-12-31"
UNIVERSE_CODE = "000906.XSHG"  # 中证800

def get_monthly_dates(start, end):
    days = get_trade_days(start, end)
    result, last_m = [], None
    for d in days:
        if d.month != last_m:
            result.append(d)
            last_m = d.month
    return result

def get_universe(date):
    return get_index_stocks(UNIVERSE_CODE, date=date)

# ---- 因子1: CGO (资本利得悬挂) ----
def calc_cgo(stocks, date, window=52):
    """CGO = (P - RP) / RP, RP为过去window周的成本价估计"""
    try:
        prices = get_price(stocks, end_date=str(date), count=window*5,
                           fields=["close","volume"], panel=False)
        pivot_c = prices.pivot(index="time", columns="code", values="close").dropna(axis=1)
        pivot_v = prices.pivot(index="time", columns="code", values="volume").dropna(axis=1)
        common = pivot_c.columns.intersection(pivot_v.columns)
        pivot_c, pivot_v = pivot_c[common], pivot_v[common]
        if len(pivot_c) < window:
            return pd.Series()
        # 成本价 = 成交量加权平均价
        rp = (pivot_c * pivot_v).rolling(window).sum() / pivot_v.rolling(window).sum()
        cgo = (pivot_c.iloc[-1] - rp.iloc[-1]) / rp.iloc[-1].replace(0, np.nan)
        return cgo.dropna()
    except:
        return pd.Series()

# ---- 因子2: 潮汐因子 (量价背离) ----
def calc_tide(stocks, date, window=20):
    """潮汐因子: 价格涨幅 / 成交量涨幅 的比值 (量价背离程度)"""
    try:
        prices = get_price(stocks, end_date=str(date), count=window+1,
                           fields=["close","volume"], panel=False)
        pivot_c = prices.pivot(index="time", columns="code", values="close").dropna(axis=1)
        pivot_v = prices.pivot(index="time", columns="code", values="volume").dropna(axis=1)
        common = pivot_c.columns.intersection(pivot_v.columns)
        if len(pivot_c) < window + 1:
            return pd.Series()
        price_ret = pivot_c[common].iloc[-1] / pivot_c[common].iloc[0] - 1
        vol_ret   = pivot_v[common].iloc[-1] / pivot_v[common].iloc[0] - 1
        # 价涨量缩 = 正潮汐 (看多)
        tide = price_ret / (vol_ret.abs() + 0.01)
        return tide.dropna()
    except:
        return pd.Series()

# ---- 因子3: 成交量激增 ----
def calc_vol_surge(stocks, date, short_w=5, long_w=60):
    """成交量激增: 近5日均量 / 近60日均量"""
    try:
        prices = get_price(stocks, end_date=str(date), count=long_w+1,
                           fields=["volume"], panel=False)
        pivot_v = prices.pivot(index="time", columns="code", values="volume").dropna(axis=1)
        if len(pivot_v) < long_w:
            return pd.Series()
        short_avg = pivot_v.rolling(short_w).mean().iloc[-1]
        long_avg  = pivot_v.rolling(long_w).mean().iloc[-1]
        surge = short_avg / long_avg.replace(0, np.nan)
        return surge.dropna()
    except:
        return pd.Series()

def calc_ic_series(factor_fn, dates, label):
    """计算月度 IC 序列"""
    ics = []
    for i, d in enumerate(dates[:-1]):
        try:
            stks = get_universe(str(d))[:300]
            factor = factor_fn(stks, d)
            if len(factor) < 30:
                continue
            # 下月收益
            p0 = get_price(factor.index.tolist(), end_date=str(d), count=1,
                           fields=["close"], panel=False)
            p1 = get_price(factor.index.tolist(), end_date=str(dates[i+1]), count=1,
                           fields=["close"], panel=False)
            p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
            ret = ((p1 / p0) - 1).dropna()
            common = factor.index.intersection(ret.index)
            if len(common) < 20:
                continue
            ic, _ = stats.spearmanr(factor[common], ret[common])
            ics.append(ic)
        except:
            continue
    if not ics:
        return None
    s = pd.Series(ics)
    return {
        "因子": label,
        "IC均值": f"{s.mean():.4f}",
        "IC标准差": f"{s.std():.4f}",
        "ICIR": f"{s.mean()/s.std():.2f}" if s.std() > 0 else "N/A",
        "IC>0比例": f"{(s > 0).mean():.0%}",
        "样本月数": len(s)
    }

dates = get_monthly_dates(START, END)
print(f"调仓次数: {len(dates)-1}")

factor_fns = [
    (lambda stks, d: calc_cgo(stks, d),       "CGO因子"),
    (lambda stks, d: calc_tide(stks, d),      "潮汐因子"),
    (lambda stks, d: calc_vol_surge(stks, d), "成交量激增"),
]

rows = []
for fn, label in factor_fns:
    print(f"  计算 IC: {label} ...")
    r = calc_ic_series(fn, dates, label)
    if r:
        rows.append(r)
        print(f"    IC均值={r['IC均值']}  ICIR={r['ICIR']}  IC>0={r['IC>0比例']}")

print("\n" + "=" * 70)
print("【新因子 IC 检验汇总】")
print("=" * 70)
if rows:
    df_res = pd.DataFrame(rows).set_index("因子")
    print(df_res.to_string())

print("\n【判断标准】")
print("  ICIR > 0.5: 有效，值得继续深挖")
print("  ICIR 0.3-0.5: 弱有效，可作为辅助因子")
print("  ICIR < 0.3: 无效，暂不工程化")
print("\n验证完成!")
```

### 执行命令

```bash
cd skills/joinquant_nookbook
node run-skill.js \
  --notebook-url <your_research_notebook_url> \
  --cell-source "$(cat /tmp/verify_09.py)" \
  --timeout-ms 300000
```

### 预期输出与判断标准

| 指标 | 判断逻辑 |
|------|---------|
| ICIR > 0.5 | 有效，值得工程化 |
| ICIR 0.3-0.5 | 弱有效，作为辅助因子 |
| ICIR < 0.3 | 无效，暂不投入 |
| IC>0 比例 > 55% | 信号方向稳定 |

### 结论记录

> 运行后在此填写：前三名新因子排名，以及最适合接到哪条母策略上。

---

## 实验结果（2026-03-28 验证）

### IC 检验结果

| 因子 | IC均值 | IC标准差 | ICIR | IC>0比例 |
|------|--------|----------|------|----------|
| CGO因子 | -0.0433 | 0.1980 | **-0.22** | 43% |
| 潮汐因子 | -0.0266 | 0.1757 | **-0.15** | 38% |
| 成交量激增 | -0.0153 | 0.1282 | **-0.12** | 45% |

### 结论

- 三个因子 IC 均为**负值**，说明方向与理论预期相反
- |ICIR| 均 < 0.3，按照判断标准为**无效因子**
- **不推荐**作为主因子工程化

### 验证报告

详见：`09_factor_innovation_lab_validation_report.md`

---

## V2 实验结果（改进版）

### IC 检验结果

| 因子 | IC均值 | ICIR | IC>0比例 |
|------|--------|------|----------|
| CGO因子(反转) | 0.0433 | **0.22** | 57% |
| 潮汐因子(反转) | 0.0266 | **0.15** | 62% |
| 成交量激增(反转) | 0.0153 | **0.12** | 55% |
| 勇攀高峰因子 | 0.0131 | **0.07** | 51% |
| 球队硬币因子 | -0.0083 | **-0.07** | 51% |
| 换手率因子 | -0.0405 | **-0.32** | 38% |

### 结论

- 所有因子 |ICIR| < 0.3，严格标准下无"有效"因子
- CGO(反转) 和潮汐(反转) 相对较好
- 换手率因子负向显著，可做风险过滤

### V2 验证报告

详见：`09_factor_innovation_lab_v2_validation_report.md`
