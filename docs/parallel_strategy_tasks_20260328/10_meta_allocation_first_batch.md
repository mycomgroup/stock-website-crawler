# 任务 10：首批实跑组合与资金分配

## 设计文档

### 任务定位

- 优先级：最高
- 类型：资源约束下的最终决策层
- 目标：在资源有限的前提下，给出“先跑哪几条、怎么配、怎么观察”的执行答案

### 为什么值得现在研究

- 你现在最现实的问题不是“仓库里还有多少方向”，而是“先启动哪几个最有胜率”
- 单条策略研究完成后，如果没有组合与优先级判断，还是容易陷入信息堆积
- 这条任务就是把前 9 个方向的结果汇总成第一批行动方案

### 参考矿脉

- `RFScore7终极版策略总结.md`
- `ETF轮动与择时_总结与后续工作.md`
- `聚宽_notebook_实测结果汇总.md`
- `聚宽有价值策略558/65 神级策略：桥水全天候策略-7年最大回撤仅3.5%.txt`
- `聚宽有价值策略558/07 股债波动平衡.txt`
- `聚宽有价值策略558/57 别人恐惧我贪婪3——年化20%的股债组合.txt`
- `聚宽有价值策略558/27 中证500指增+CTA，胜率52%盈亏比1.9。不输顶尖私募.txt`
- `聚宽有价值策略558/90 国债固收+.txt`

### 核心假设

- 真正可执行的答案通常不是“只押一条”，而是 `2 到 3 条母策略 + 一个防守资产或风控层`
- 当前环境下，更需要“先跑代表性强、摩擦低、逻辑清晰”的版本
- 组合层的价值在于资源优先级，不是追求表面多样化

### 本轮只做什么

1. 结合前 9 个任务的结论，筛出第一批最值得实跑的 2 到 3 条策略。
2. 给出每条策略适合的资金占比、观察周期、淘汰条件。
3. 判断是否需要接入债券 / 现金 / 全天候防守层。
4. 形成“本周就能启动”的策略优先级清单。

### 明确不做什么

- 不做完美组合优化
- 不因为想分散而硬塞很多低质量策略
- 不把历史回测相关性当成未来可靠结论

### 交付物

1. 一份首批实跑清单：`策略名 + 理由 + 资金占比 + 观察周期`
2. 一份淘汰与晋级规则：什么情况下减仓、停跑、升级
3. 一份防守方案：是否需要债券 / 货基 / 全天候底仓

### 成功判据

- 能直接回答“资源有限时先跑谁”
- 能把研究工作真正收束成交易与跟踪动作

## 子任务提示词

```text
你现在是执行决策层子任务。你的目标是把仓库里最有价值的方向收束成第一批实跑名单，而不是再多开十条研究线。

请优先参考这些材料：
- RFScore7终极版策略总结.md
- ETF轮动与择时_总结与后续工作.md
- 聚宽_notebook_实测结果汇总.md
- 聚宽有价值策略558/65 神级策略：桥水全天候策略-7年最大回撤仅3.5%.txt
- 聚宽有价值策略558/07 股债波动平衡.txt
- 聚宽有价值策略558/57 别人恐惧我贪婪3——年化20%的股债组合.txt
- 聚宽有价值策略558/27 中证500指增+CTA，胜率52%盈亏比1.9。不输顶尖私募.txt
- 前 9 个并行任务的阶段结论

请完成以下事情：
1. 在资源有限的前提下，挑出首批最值得实跑的 2 到 3 条策略。
2. 为每条策略给出：
   - 推荐资金占比
   - 观察周期
   - 淘汰条件
   - 晋级条件
3. 判断是否需要加入债券 / 现金 / 全天候层做防守。
4. 输出一个“先跑顺序表”。

输出要求：
- 必须明确说出：先跑谁，为什么不是别人。
- 必须把“强研究价值”与“适合本周启动”分开。
- 必须给出一个简洁、可执行的第一批启动方案。
```

## 实际效果验证

### 验证方式

在聚宽 Research 中运行首批实跑组合的模拟配置，验证各策略当前信号状态，输出可直接执行的第一批启动方案。

### 验证代码

```python
# 首批实跑组合验证
# 汇总各策略当前信号，输出资金分配建议

from jqdata import *
import pandas as pd
import numpy as np
from scipy import stats

print("=" * 70)
print("首批实跑组合 - 当前信号汇总与资金分配建议")
print("=" * 70)

TODAY = get_trade_days(end_date="2026-03-28", count=1)[-1]
TODAY_STR = str(TODAY)
TOTAL_CAPITAL = 100  # 百分比

# ============ 信号1: RFScore7+PB20 当前候选 ============
print("\n【策略1】RFScore7 + PB20% 当前候选股")
print("-" * 50)
try:
    universe = get_index_stocks("000906.XSHG")
    q = query(
        valuation.code, indicator.roe, indicator.roa,
        indicator.gross_profit_margin, indicator.net_profit_margin,
        indicator.inc_net_profit_year_on_year, indicator.inc_revenue_year_on_year,
        valuation.pe_ratio, valuation.pb_ratio
    ).filter(valuation.code.in_(universe))
    df = get_fundamentals(q, date=TODAY_STR).set_index("code").dropna(subset=["roe","pb_ratio"])
    # 过滤ST
    is_st = get_extras("is_st", df.index.tolist(), end_date=TODAY_STR, count=1).iloc[-1]
    df = df[~is_st.reindex(df.index).fillna(True)]
    # RFScore7
    score = (df["roe"] > 0).astype(int) + (df["roa"] > 0).astype(int) + \
            (df["gross_profit_margin"] > df["gross_profit_margin"].median()).astype(int) + \
            (df["net_profit_margin"] > 0).astype(int) + \
            (df["inc_net_profit_year_on_year"] > 0).astype(int) + \
            (df["inc_revenue_year_on_year"] > 0).astype(int) + \
            (df["pe_ratio"] > 0).astype(int)
    df["rfscore7"] = score
    pb_thresh = df["pb_ratio"].quantile(0.20)
    candidates = df[df["pb_ratio"] <= pb_thresh].nlargest(20, "rfscore7")
    print(f"  候选股数: {len(candidates)}")
    print(f"  平均RFScore7: {candidates['rfscore7'].mean():.1f}/7")
    print(f"  平均PE: {candidates['pe_ratio'].mean():.1f}")
    print(f"  平均PB: {candidates['pb_ratio'].mean():.2f}")
    rfscore_ready = len(candidates) >= 15
    print(f"  信号状态: {'✓ 就绪' if rfscore_ready else '⚠️ 候选不足'}")
except Exception as e:
    rfscore_ready = False
    print(f"  计算失败: {e}")

# ============ 信号2: ETF动量基线当前排名 ============
print("\n【策略2】ETF 动量基线当前排名 (20日)")
print("-" * 50)
ETF_POOL = {
    "510300.XSHG": "沪深300ETF", "510500.XSHG": "中证500ETF",
    "159915.XSHE": "创业板ETF",  "588000.XSHG": "科创50ETF",
    "518880.XSHG": "黄金ETF",    "511010.XSHG": "国债ETF",
    "159941.XSHE": "纳指ETF",    "513500.XSHG": "标普500ETF",
}
try:
    codes = list(ETF_POOL.keys())
    prices = get_price(codes, end_date=TODAY_STR, count=21, fields=["close"], panel=False)
    pivot = prices.pivot(index="time", columns="code", values="close").dropna(axis=1)
    mom = (pivot.iloc[-1] / pivot.iloc[0] - 1).sort_values(ascending=False)
    print("  20日动量排名:")
    for code, val in mom.items():
        tag = "★ 持有" if code in mom.nlargest(3).index else "  "
        print(f"  {tag} {ETF_POOL.get(code, code)}: {val:+.2%}")
    etf_ready = True
except Exception as e:
    etf_ready = False
    print(f"  计算失败: {e}")

# ============ 信号3: 市场状态路由 ============
print("\n【市场状态路由】")
print("-" * 50)
try:
    stks300 = get_index_stocks("000300.XSHG", date=TODAY_STR)[:150]
    prices_b = get_price(stks300, end_date=TODAY_STR, count=21, fields=["close"], panel=False)
    pivot_b = prices_b.pivot(index="time", columns="code", values="close").dropna(axis=1)
    breadth = (pivot_b.iloc[-1] > pivot_b.rolling(20).mean().iloc[-1]).mean()

    pe_df = get_fundamentals(
        query(valuation.code, valuation.pe_ratio)
        .filter(valuation.code.in_(stks300), valuation.pe_ratio > 0), date=TODAY_STR)
    hs300_pe = pe_df["pe_ratio"].median()
    fed = (100 / hs300_pe) - 1.8

    print(f"  市场宽度: {breadth:.1%}")
    print(f"  FED指标: {fed:.2f}")

    if breadth < 0.35 and fed > 1:
        regime = "底部试错"
        rfscore_alloc = 30
        etf_alloc = 20
        cash_alloc = 50
    elif breadth > 0.55 and fed > 0:
        regime = "趋势进攻"
        rfscore_alloc = 50
        etf_alloc = 40
        cash_alloc = 10
    elif fed < -1:
        regime = "高估防守"
        rfscore_alloc = 10
        etf_alloc = 20
        cash_alloc = 70
    else:
        regime = "震荡轮动"
        rfscore_alloc = 35
        etf_alloc = 35
        cash_alloc = 30

    print(f"\n  => 当前状态: 【{regime}】")
except Exception as e:
    regime = "震荡轮动"
    rfscore_alloc, etf_alloc, cash_alloc = 35, 35, 30
    print(f"  计算失败，使用默认配置: {e}")

# ============ 首批实跑方案 ============
print("\n" + "=" * 70)
print("【首批实跑方案】")
print("=" * 70)
print(f"""
当前市场状态: {regime}

┌─────────────────────┬──────────┬──────────┬──────────────────────┐
│ 策略                │ 资金占比 │ 观察周期 │ 淘汰条件             │
├─────────────────────┼──────────┼──────────┼──────────────────────┤
│ RFScore7 + PB20%    │ {rfscore_alloc:>6}%  │ 3个月    │ 连续2月跑输基准>5%   │
│ ETF 动量基线        │ {etf_alloc:>6}%  │ 1个月    │ 最大回撤 > 15%       │
│ 现金/货基           │ {cash_alloc:>6}%  │ 持续     │ 市场状态切换时调整   │
└─────────────────────┴──────────┴──────────┴──────────────────────┘

晋级条件:
  - RFScore7: 3个月超额 > 5% → 提升至 50%
  - ETF基线: 1个月回撤 < 8% → 提升至 50%

防守方案:
  - 市场宽度 < 25% 时，现金仓位提升至 60%
  - FED < -1 时，全面降仓至 30%
""")

print("验证完成!")
```

### 执行命令

```bash
cd skills/joinquant_nookbook
node run-skill.js \
  --notebook-url <your_research_notebook_url> \
  --cell-source "$(cat /tmp/verify_10.py)" \
  --timeout-ms 120000
```

### 通过 joinquant_strategy 运行回测验证

如果已有策略文件，可通过以下命令运行完整回测：

```bash
# 验证 RFScore7+PB20 策略回测
cd skills/joinquant_strategy
node run-skill.js \
  --id <your_rfscore7_algorithm_id> \
  --file strategies/rfscore7_pb20_final.py \
  --start 2023-01-01 \
  --end 2025-12-31 \
  --capital 100000

# 列出所有可用策略
node list-strategies.js
```

### 预期输出与判断标准

| 检查项 | 通过标准 |
|--------|---------|
| RFScore7 候选股数 | >= 15 只才就绪 |
| ETF 动量排名 | 前3名动量均为正才满仓 |
| 市场状态 | 明确输出状态标签和资金分配 |
| 首批方案 | 能直接指导本周操作 |

### 结论记录

> 运行后在此填写：首批实跑清单（策略名 + 资金占比 + 观察周期），以及是否需要防守底仓。
