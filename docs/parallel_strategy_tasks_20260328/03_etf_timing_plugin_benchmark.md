# 任务 03：ETF 择时插件对比

## 设计文档

### 任务定位

- 优先级：高
- 类型：ETF 线风控增强
- 目标：判断择时层到底是提升收益，还是主要负责降回撤

### 为什么值得现在研究

- 仓库里的 ETF 线素材很多，但结论高度一致：择时层更像过滤器，不应替代主排序逻辑
- 当前本地市场快照显示宽度偏低，择时插件对当前市场尤其重要
- 资源有限时，要先知道哪些择时插件值得保留，哪些只是让策略变复杂

### 参考矿脉

- `ETF轮动与择时_总结与后续工作.md`
- `聚宽有价值策略558/52 市场宽度——简洁版.ipynb`
- `聚宽有价值策略558/59 研究 【复现】RSRS择时改进.ipynb`
- `聚宽有价值策略558/60 研究 【分享】对RSRS模型的一次修改.ipynb`
- `聚宽有价值策略558/45 研究 市场宽度.ipynb`
- `聚宽有价值策略558/85 【深度解析 七】BBI指标-大盘涨跌-宽基轮动 模型.txt`
- `聚宽有价值策略558/33 研究 基于风险溢价的沪深300择时.ipynb`

### 核心假设

- 宽度更适合做仓位过滤
- RSRS 更适合做趋势确认
- 择时插件的价值主要在控制回撤和降低误判，不一定体现在最高收益

### 本轮只做什么

1. 固定 ETF 基线，不更改候选池与排序规则。
2. 比较 `不择时 / 宽度 / RSRS / 改进RSRS / 宽度+RSRS / BBI`。
3. 看每种插件对回撤、换手、信号覆盖率的影响。
4. 给出“当前市场环境下最值得保留的 1 到 2 个插件”。

### 明确不做什么

- 不重新设计 ETF 排序主因子
- 不把行业增强、北向资金、宏观全叠进去
- 不只看收益最高的一列

### 交付物

1. 一张插件对比表：收益、回撤、夏普、换手、空仓占比、信号覆盖率。
2. 一份解释：每个插件主要改善了什么，代价是什么。
3. 一个推荐结论：ETF 基线最该接哪一个或哪两个择时插件。

### 成功判据

- 能说清择时层的真实作用
- 能把“看起来有道理”和“真值得接到基线里”区分开

## 子任务提示词

```text
你现在是 ETF 择时插件子任务。你的目标不是再造一个 ETF 策略，而是在固定 ETF 基线之上，比较哪些择时插件值得保留。

如果 ETF 基线任务还没完成，请临时采用这个基线：
- 候选池：66/86 文档里的 clean ETF pool
- 主排序：20日动量
- 持有周期：10日

请优先阅读这些材料：
- ETF轮动与择时_总结与后续工作.md
- 聚宽有价值策略558/52 市场宽度——简洁版.ipynb
- 聚宽有价值策略558/59 研究 【复现】RSRS择时改进.ipynb
- 聚宽有价值策略558/60 研究 【分享】对RSRS模型的一次修改.ipynb
- 聚宽有价值策略558/85 【深度解析 七】BBI指标-大盘涨跌-宽基轮动 模型.txt

请完成以下事情：
1. 比较以下插件：
   - 不择时
   - 仅市场宽度
   - 仅 RSRS
   - 改进 RSRS
   - 宽度 + RSRS
   - BBI
2. 重点看：
   - 最大回撤改善
   - 成本后净收益
   - 空仓率
   - 是否让信号变得过度稀疏
3. 输出当前市场状态下，最适合启用哪一个插件。

输出要求：
- 必须明确区分“收益增强型插件”和“回撤控制型插件”。
- 必须指出哪些插件只是看起来高级，实际不值得加。
- 结论必须能指导工程落地，而不是停留在指标比较。
```

## 实际效果验证

### 验证方式

固定 ETF 基线（20日动量 / 10日持有 / 中证800 ETF 池），在聚宽 Research 中对比各择时插件的真实效果。

### 验证代码

```python
# ETF 择时插件对比验证
# 固定基线: 20日动量, 10日持有, top3 ETF

from jqdata import *
import pandas as pd
import numpy as np
from scipy import stats

print("=" * 70)
print("ETF 择时插件对比验证 (2020-01-01 ~ 2025-12-31)")
print("=" * 70)

START = "2020-01-01"
END   = "2025-12-31"
MOM_WINDOW = 20
HOLD_DAYS  = 10
TOP_N      = 3
COST       = 0.001

ETF_POOL = {
    "510300.XSHG": "沪深300ETF",
    "510500.XSHG": "中证500ETF",
    "159915.XSHE": "创业板ETF",
    "588000.XSHG": "科创50ETF",
    "518880.XSHG": "黄金ETF",
    "511010.XSHG": "国债ETF",
    "159941.XSHE": "纳指ETF",
    "513500.XSHG": "标普500ETF",
}
CODES = list(ETF_POOL.keys())

def get_rebal_dates(start, end, freq_days):
    all_days = get_trade_days(start, end)
    result = [all_days[0]]
    for d in all_days[1:]:
        if (d - result[-1]).days >= freq_days:
            result.append(d)
    return result

# ---- 择时信号函数 ----
def signal_breadth(date, threshold=0.4):
    """市场宽度: 沪深300成分股中 close>MA20 比例 > threshold 才做多"""
    try:
        stks = get_index_stocks("000300.XSHG", date=date)[:200]
        prices = get_price(stks, end_date=str(date), count=21, fields=["close"], panel=False)
        pivot = prices.pivot(index="time", columns="code", values="close").dropna(axis=1)
        if len(pivot) < 21:
            return True
        ma20 = pivot.rolling(20).mean().iloc[-1]
        ratio = (pivot.iloc[-1] > ma20).mean()
        return ratio > threshold
    except:
        return True

def signal_rsrs(date, n=18, m=600, buy_thresh=0.7, sell_thresh=-0.7):
    """RSRS 标准化右偏分"""
    try:
        prices = get_price("000300.XSHG", end_date=str(date), count=m+n,
                           fields=["high","low"], panel=False).set_index("time")
        if len(prices) < m + n:
            return True
        slopes = []
        for i in range(n, len(prices)):
            sl, _, _, _, _ = stats.linregress(
                prices["low"].values[i-n:i], prices["high"].values[i-n:i])
            slopes.append(sl)
        s = pd.Series(slopes)
        z = (s - s.rolling(m).mean()) / s.rolling(m).std()
        right = s * z
        latest = right.dropna().iloc[-1]
        return latest > buy_thresh
    except:
        return True

def signal_bbi(date):
    """BBI 大盘趋势: 收盘 > BBI(3,6,12,24) 才做多"""
    try:
        prices = get_price("000300.XSHG", end_date=str(date), count=25,
                           fields=["close"], panel=False)["close"]
        bbi = (prices.rolling(3).mean() + prices.rolling(6).mean() +
               prices.rolling(12).mean() + prices.rolling(24).mean()) / 4
        return prices.iloc[-1] > bbi.iloc[-1]
    except:
        return True

def run_with_timing(timing_fn, label, dates):
    """运行带择时插件的版本"""
    rets, empty_periods = [], 0
    prev_holdings = []
    for i, d in enumerate(dates[:-1]):
        d_str = str(d)
        next_d_str = str(dates[i+1])
        try:
            # 择时判断
            if timing_fn is not None and not timing_fn(d):
                rets.append(0.0)
                empty_periods += 1
                prev_holdings = []
                continue
            # 动量选 ETF
            prices = get_price(CODES, end_date=d_str, count=MOM_WINDOW+1,
                               fields=["close"], panel=False)
            pivot = prices.pivot(index="time", columns="code", values="close").dropna(axis=1)
            if len(pivot) < MOM_WINDOW + 1:
                continue
            mom = (pivot.iloc[-1] / pivot.iloc[0] - 1)
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
    empty_pct = empty_periods / len(s)
    return {"插件": label, "年化(扣费)": f"{ann:.1%}", "最大回撤": f"{dd:.1%}",
            "夏普": f"{sharpe:.2f}", "空仓率": f"{empty_pct:.0%}", "样本数": len(s)}

dates = get_rebal_dates(START, END, HOLD_DAYS)
print(f"调仓次数: {len(dates)-1}")

plugins = [
    (None,                                    "不择时 (基线)"),
    (signal_breadth,                          "仅市场宽度"),
    (signal_rsrs,                             "仅 RSRS"),
    (signal_bbi,                              "仅 BBI"),
    (lambda d: signal_breadth(d) and signal_rsrs(d), "宽度 + RSRS"),
]

rows = []
for fn, label in plugins:
    print(f"  运行: {label} ...")
    r = run_with_timing(fn, label, dates)
    if r:
        rows.append(r)
        print(f"    年化={r['年化(扣费)']}  回撤={r['最大回撤']}  空仓率={r['空仓率']}")

print("\n" + "=" * 70)
print("【择时插件对比汇总】")
print("=" * 70)
if rows:
    df_res = pd.DataFrame(rows).set_index("插件")
    print(df_res.to_string())

# 当前信号状态
print("\n" + "=" * 70)
print("【当前市场择时信号状态】")
print("=" * 70)
today = get_trade_days(end_date="2026-03-28", count=1)[-1]
print(f"  市场宽度信号: {'做多' if signal_breadth(today) else '空仓'}")
print(f"  RSRS 信号:    {'做多' if signal_rsrs(today) else '空仓'}")
print(f"  BBI 信号:     {'做多' if signal_bbi(today) else '空仓'}")
print("\n验证完成!")
```

### 执行命令

```bash
cd skills/joinquant_nookbook
node run-skill.js \
  --notebook-url <your_research_notebook_url> \
  --cell-source "$(cat /tmp/verify_03.py)" \
  --timeout-ms 360000
```

### 预期输出与判断标准

| 指标 | 判断逻辑 |
|------|---------|
| 插件 vs 基线回撤改善 | 改善 > 5% 才值得接入 |
| 空仓率 | > 40% 说明信号过于保守 |
| 夏普提升 | 有提升才算"收益增强型" |
| 当前信号 | 三个信号一致才建议满仓 |

### 结论记录

> 运行后在此填写：推荐接入哪 1-2 个插件，当前市场信号状态，以及是否建议满仓。
