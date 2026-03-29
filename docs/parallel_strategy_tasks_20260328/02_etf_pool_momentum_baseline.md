# 任务 02：ETF 候选池 + 动量基线

## 设计文档

### 任务定位

- 优先级：最高
- 类型：低摩擦代表性母策略
- 目标：在 ETF 线上先建立一个统一、干净、可复用的基线版本

### 为什么值得现在研究

- 根目录多份文档的共识都指向：ETF 线最重要的不是堆因子，而是“先建池，再排序，最后择时”
- 资源有限时，最该先跑的是代表性强、可扩展、低交易摩擦的母策略
- ETF 基线一旦稳定，后续择时、行业增强、组合层都能往上叠

### 参考矿脉

- `ETF轮动与择时_总结与后续工作.md`
- `聚宽有价值策略558/43 轮动ETF策略中的动量因子分析.ipynb`
- `聚宽有价值策略558/66 手把手教你构建ETF策略候选池.ipynb`
- `聚宽有价值策略558/86 手把手教你构建ETF策略候选池优化版.ipynb`
- `聚宽有价值策略558/05 8年10倍回撤小,有滑点,ETF动量简单轮动策略.txt`
- `聚宽有价值策略558/17 8年13倍的ETF动量轮动策略,有滑点,无未来函数,回撤小.txt`
- `聚宽有价值策略558/31 ETF核心资产轮动动量因子加RSRS择时每日策略.txt`

### 核心假设

- 干净候选池的价值高于复杂排序器
- `10` 到 `20` 日动量是最应优先验证的主信号
- 应先做“不择时基线”，再看择时是否真的提升了质量

### 本轮只做什么

1. 复刻 `66/86` 的候选池逻辑，做一个可复用池版本。
2. 比较 `10/20/30` 日动量排序与 `5/10/20` 日持有周期。
3. 固定交易成本口径，输出一个最小可用 ETF 基线。
4. 记录每次入池 ETF 的原因，避免黑箱。

### 明确不做什么

- 不把择时、行业增强、北向资金一起堆进去
- 不一开始就追求“最强组合”
- 不用股票因子硬套 ETF

### 交付物

1. 一份候选池版本说明：保留哪些 ETF、去掉哪些 ETF、原因是什么。
2. 一张基线对比表：动量窗口、持有周期、收益、回撤、换手、成本后净收益。
3. 一个推荐基线：`候选池版本 + 排序因子 + 调仓频率`
4. 一份后续可直接给择时任务复用的标准接口说明

### 成功判据

- 能给出一个足够稳定、足够简单、可被其他任务复用的 ETF 基线
- 能解释“为什么这个基线值得当母策略”

## 子任务提示词

```text
你现在是 ETF 母策略子任务，目标不是找 ETF 圣杯，而是建立一个后续所有 ETF 研究都能复用的基线版本。

请优先阅读这些材料：
- ETF轮动与择时_总结与后续工作.md
- 聚宽有价值策略558/43 轮动ETF策略中的动量因子分析.ipynb
- 聚宽有价值策略558/66 手把手教你构建ETF策略候选池.ipynb
- 聚宽有价值策略558/86 手把手教你构建ETF策略候选池优化版.ipynb
- 聚宽有价值策略558/05 8年10倍回撤小,有滑点,ETF动量简单轮动策略.txt
- 聚宽有价值策略558/17 8年13倍的ETF动量轮动策略,有滑点,无未来函数,回撤小.txt

请完成以下事情：
1. 还原候选池构建逻辑：成立时间、成交额、聚类去重、相关性去重。
2. 做一个统一 ETF 池版本，写清每个筛选条件。
3. 在不叠加择时的前提下，比较：
   - 10日动量
   - 20日动量
   - 30日动量
4. 比较：
   - 5日持有
   - 10日持有
   - 20日持有
5. 选出一个可复用基线，供后续择时和行业增强任务直接调用。

输出要求：
- 必须有一张“候选池入池/出池理由表”。
- 必须给出成本后净收益，不接受只看毛收益。
- 必须明确推荐一个 baseline version。
- 如果发现候选池过度依赖经验参数，要点名说明。
```

## 实际效果验证

### 验证方式

通过 `skills/joinquant_nookbook` 在聚宽 Research 环境中运行以下代码，对 ETF 候选池 + 不同动量窗口 / 持有周期做真实数据对比。

### 验证代码

```python
# ETF 候选池 + 动量基线验证
# 不叠加择时，纯动量排序，固定成本口径

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 70)
print("ETF 动量基线验证 (2020-01-01 ~ 2025-12-31)")
print("=" * 70)

START = "2020-01-01"
END   = "2025-12-31"
COST  = 0.001  # 单边万一手续费

# ---- 候选池定义 (基于 66/86 文档逻辑) ----
ETF_POOL = {
    "沪深300ETF":  "510300.XSHG",
    "中证500ETF":  "510500.XSHG",
    "创业板ETF":   "159915.XSHE",
    "科创50ETF":   "588000.XSHG",
    "中证1000ETF": "512100.XSHG",
    "纳指ETF":     "159941.XSHE",
    "标普500ETF":  "513500.XSHG",
    "黄金ETF":     "518880.XSHG",
    "国债ETF":     "511010.XSHG",
    "医疗ETF":     "512170.XSHG",
    "消费ETF":     "159928.XSHE",
    "新能源ETF":   "516160.XSHG",
}

def get_rebal_dates(start, end, freq_days):
    """按固定天数间隔取调仓日"""
    all_days = get_trade_days(start, end)
    result = [all_days[0]]
    for d in all_days[1:]:
        if (d - result[-1]).days >= freq_days:
            result.append(d)
    return result

def run_etf_version(mom_window, hold_days, label, top_n=3):
    """运行一个动量窗口 + 持有周期版本"""
    dates = get_rebal_dates(START, END, hold_days)
    codes = list(ETF_POOL.values())
    monthly_rets = []
    prev_holdings = []

    for i, d in enumerate(dates[:-1]):
        d_str = str(d)
        next_d_str = str(dates[i+1])
        try:
            # 计算动量
            prices = get_price(codes, end_date=d_str, count=mom_window+1,
                               fields=["close"], panel=False)
            pivot = prices.pivot(index="time", columns="code", values="close").dropna(axis=1)
            if len(pivot) < mom_window + 1:
                continue
            mom = (pivot.iloc[-1] / pivot.iloc[0] - 1)
            selected = mom.nlargest(top_n).index.tolist()

            # 计算持有收益
            p0 = get_price(selected, end_date=d_str, count=1, fields=["close"], panel=False)
            p1 = get_price(selected, end_date=next_d_str, count=1, fields=["close"], panel=False)
            p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
            gross_ret = ((p1 / p0) - 1).mean()

            # 扣除换手成本
            turnover = len(set(selected) - set(prev_holdings)) / top_n
            net_ret = gross_ret - turnover * COST * 2
            monthly_rets.append(net_ret)
            prev_holdings = selected
        except:
            continue

    if not monthly_rets:
        return None
    s = pd.Series(monthly_rets)
    cum = (1 + s).cumprod()
    periods_per_year = 252 / hold_days
    ann = cum.iloc[-1] ** (periods_per_year / len(s)) - 1
    dd = (cum / cum.cummax() - 1).min()
    sharpe = s.mean() / s.std() * (periods_per_year ** 0.5) if s.std() > 0 else 0
    win = (s > 0).mean()
    return {"版本": label, "年化(扣费)": f"{ann:.1%}", "最大回撤": f"{dd:.1%}",
            "夏普": f"{sharpe:.2f}", "胜率": f"{win:.0%}", "样本数": len(s)}

# 验证矩阵
configs = [
    (10, 5,  "动量10d / 持有5d"),
    (10, 10, "动量10d / 持有10d"),
    (20, 10, "动量20d / 持有10d"),
    (20, 20, "动量20d / 持有20d"),
    (30, 10, "动量30d / 持有10d"),
    (30, 20, "动量30d / 持有20d"),
]

rows = []
for mom_w, hold_d, label in configs:
    print(f"  运行: {label} ...")
    r = run_etf_version(mom_w, hold_d, label)
    if r:
        rows.append(r)
        print(f"    年化={r['年化(扣费)']}  回撤={r['最大回撤']}  夏普={r['夏普']}")

print("\n" + "=" * 70)
print("【ETF 基线对比汇总】")
print("=" * 70)
if rows:
    df_res = pd.DataFrame(rows).set_index("版本")
    print(df_res.to_string())

# 当前动量排名
print("\n" + "=" * 70)
print("【当前 ETF 动量排名 (20日)】")
print("=" * 70)
today = get_trade_days(end_date="2026-03-28", count=1)[-1]
codes = list(ETF_POOL.values())
names = list(ETF_POOL.keys())
prices = get_price(codes, end_date=str(today), count=21, fields=["close"], panel=False)
pivot = prices.pivot(index="time", columns="code", values="close").dropna(axis=1)
mom = (pivot.iloc[-1] / pivot.iloc[0] - 1).sort_values(ascending=False)
name_map = dict(zip(ETF_POOL.values(), ETF_POOL.keys()))
for code, val in mom.items():
    print(f"  {name_map.get(code, code)}: {val:+.2%}")
print("\n验证完成!")
```

### 执行命令

```bash
cd skills/joinquant_nookbook
node run-skill.js \
  --notebook-url <your_research_notebook_url> \
  --cell-source "$(cat /tmp/verify_02.py)" \
  --timeout-ms 300000
```

### 预期输出与判断标准

| 指标 | 通过标准 |
|------|---------|
| 最优版本扣费年化 | > 10% |
| 最大回撤 | < 25% |
| 夏普 | > 0.7 |
| 推荐基线 | 明确选出一个动量窗口+持有周期组合 |

### 结论记录

> 运行后在此填写：推荐基线版本（动量窗口 + 持有周期），以及候选池入池/出池理由。
