# 任务 08：宏观 + 市场状态路由器

## 设计文档

### 任务定位

- 优先级：高
- 类型：顶层认知与策略路由
- 目标：不是做纯宏观报告，而是做一个能指导“现在该偏哪类策略”的状态机

### 为什么值得现在研究

- 你当前最关键的问题之一就是：要不要先做宏观分析，再跑策略
- 仓库里已经有市场宽度、风险溢价、情绪、牛熊、FED 指标、格雷厄姆指数等材料
- 最合理的做法不是“先闭门研究宏观一周”，而是做一个轻量状态路由器，和策略验证并行推进

### 参考矿脉

- `聚宽_notebook_实测结果汇总.md`
- `聚宽有价值策略558/33 研究 基于风险溢价的沪深300择时.ipynb`
- `聚宽有价值策略558/45 研究 市场宽度.ipynb`
- `聚宽有价值策略558/52 市场宽度——简洁版.ipynb`
- `聚宽有价值策略558/63 研究 【复现】华泰证券-波动率和换手率构建牛熊指标.ipynb`
- `聚宽有价值策略558/93 【复现】国信投资者情绪指数择时模型.ipynb`
- `聚宽有价值策略558/97 大周期顶底判断：FED指标+格雷厄姆指数一次搞定.ipynb`
- `聚宽有价值策略558/99 计算每日全A市场个股创新高比例(改).ipynb`

### 核心假设

- 宏观与市场状态更适合作为“路由器”，而不是直接选股器
- 状态路由器的价值在于决定：偏 RFScore、偏 ETF、偏红利、还是降仓观望
- 轻量级状态机比复杂宏观叙事更适合当前阶段

### 本轮只做什么

1. 定义少量高价值状态指标：宽度、估值、风险溢价、情绪、创新高比例。
2. 构建 3 到 5 个市场状态。
3. 给每个状态匹配更适合的策略方向。
4. 输出一份“当前市场属于哪一档，应偏向什么”的路由表。

### 明确不做什么

- 不写宏观周报式长文
- 不引入大量不可落地的宏观变量
- 不让状态机复杂到无法维护

### 交付物

1. 一张状态定义表。
2. 一份策略路由表：每个状态更适合什么策略。
3. 一份当前状态判断：现在更该偏向 RFScore、ETF、红利、小市值，还是防守。

### 成功判据

- 能直接回答“是不是先做宏观分析，再跑策略”
- 能让后续所有策略任务都知道自己适合在什么环境里被启用

## 子任务提示词

```text
你现在是宏观 + 市场状态路由器子任务。你的目标不是做纯宏观研究，而是构建一个能指导策略分配的轻量状态机。

请优先阅读这些材料：
- 聚宽_notebook_实测结果汇总.md
- 聚宽有价值策略558/33 研究 基于风险溢价的沪深300择时.ipynb
- 聚宽有价值策略558/45 研究 市场宽度.ipynb
- 聚宽有价值策略558/52 市场宽度——简洁版.ipynb
- 聚宽有价值策略558/63 研究 【复现】华泰证券-波动率和换手率构建牛熊指标.ipynb
- 聚宽有价值策略558/93 【复现】国信投资者情绪指数择时模型.ipynb
- 聚宽有价值策略558/97 大周期顶底判断：FED指标+格雷厄姆指数一次搞定.ipynb

请完成以下事情：
1. 从上述材料里挑出最有用的少量状态指标。
2. 定义 3 到 5 个市场状态，例如：
   - 底部试错
   - 趋势进攻
   - 震荡轮动
   - 高估防守
3. 给每个状态写出更适合的策略方向。
4. 判断当前市场属于什么状态，并给出策略优先级。

输出要求：
- 必须回答：宏观分析应该怎么做才不拖慢策略推进。
- 必须给出当前状态的明确标签。
- 必须用策略路由语言输出，而不是纯市场评论。
```

## 实际效果验证

### 验证方式

在聚宽 Research 中计算当前市场状态指标，输出状态标签和策略路由建议，验证状态机是否能给出可操作的判断。

### 验证代码

```python
# 宏观 + 市场状态路由器验证
# 计算当前状态指标，输出策略路由建议

from jqdata import *
import pandas as pd
import numpy as np
from scipy import stats

print("=" * 70)
print("市场状态路由器 - 当前状态计算 (2026-03-28)")
print("=" * 70)

TODAY = get_trade_days(end_date="2026-03-28", count=1)[-1]
TODAY_STR = str(TODAY)

# ---- 指标1: 市场宽度 ----
print("\n【1】市场宽度 (沪深300成分股 close > MA20 比例)")
try:
    stks = get_index_stocks("000300.XSHG", date=TODAY_STR)[:200]
    prices = get_price(stks, end_date=TODAY_STR, count=21, fields=["close"], panel=False)
    pivot = prices.pivot(index="time", columns="code", values="close").dropna(axis=1)
    ma20 = pivot.rolling(20).mean().iloc[-1]
    breadth = (pivot.iloc[-1] > ma20).mean()
    print(f"  市场宽度: {breadth:.1%}")
    breadth_state = "底部" if breadth < 0.3 else ("顶部" if breadth > 0.7 else "中性")
    print(f"  宽度状态: {breadth_state}")
except Exception as e:
    breadth = 0.5
    print(f"  计算失败: {e}")

# ---- 指标2: 估值 (FED + 格雷厄姆) ----
print("\n【2】估值指标 (FED + 格雷厄姆指数)")
try:
    hs300_stks = get_index_stocks("000300.XSHG", date=TODAY_STR)
    pe_df = get_fundamentals(
        query(valuation.code, valuation.pe_ratio)
        .filter(valuation.code.in_(hs300_stks), valuation.pe_ratio > 0),
        date=TODAY_STR
    )
    hs300_pe = pe_df["pe_ratio"].median()
    earnings_yield = 100 / hs300_pe
    bond_yield = 1.8  # 2026年近似10年国债收益率
    fed = earnings_yield - bond_yield
    graham = earnings_yield / bond_yield
    print(f"  沪深300 PE中位数: {hs300_pe:.1f}")
    print(f"  盈利收益率: {earnings_yield:.2f}%")
    print(f"  FED指标: {fed:.2f} ({'低估' if fed > 0 else '高估'})")
    print(f"  格雷厄姆指数: {graham:.2f} ({'低估' if graham > 1.5 else '中性' if graham > 1 else '高估'})")
    valuation_state = "低估" if fed > 1 and graham > 1.5 else ("高估" if fed < -1 else "中性")
except Exception as e:
    valuation_state = "中性"
    print(f"  计算失败: {e}")

# ---- 指标3: RSRS 趋势 ----
print("\n【3】RSRS 趋势信号")
try:
    prices_rsrs = get_price("000300.XSHG", end_date=TODAY_STR, count=820,
                            fields=["high","low"], panel=False).set_index("time")
    N, M = 18, 600
    slopes = []
    for i in range(N, len(prices_rsrs)):
        sl, _, _, _, _ = stats.linregress(
            prices_rsrs["low"].values[i-N:i], prices_rsrs["high"].values[i-N:i])
        slopes.append(sl)
    s = pd.Series(slopes)
    z = (s - s.rolling(M).mean()) / s.rolling(M).std()
    right = s * z
    latest_right = right.dropna().iloc[-1]
    print(f"  RSRS右偏分: {latest_right:.3f}")
    rsrs_state = "趋势向上" if latest_right > 0.7 else ("趋势向下" if latest_right < -0.7 else "震荡")
    print(f"  趋势状态: {rsrs_state}")
except Exception as e:
    rsrs_state = "震荡"
    print(f"  计算失败: {e}")

# ---- 指标4: 创新高比例 ----
print("\n【4】创新高比例 (120日)")
try:
    all_stks = get_index_stocks("000906.XSHG", date=TODAY_STR)
    prices_nh = get_price(all_stks[:300], end_date=TODAY_STR, count=121,
                          fields=["close"], panel=False)
    pivot_nh = prices_nh.pivot(index="time", columns="code", values="close").dropna(axis=1)
    if len(pivot_nh) >= 121:
        is_new_high = (pivot_nh.iloc[-1] == pivot_nh.max())
        nh_pct = is_new_high.mean()
        print(f"  创120日新高比例: {nh_pct:.1%}")
        nh_state = "强势" if nh_pct > 0.05 else ("弱势" if nh_pct < 0.01 else "中性")
        print(f"  新高状态: {nh_state}")
    else:
        nh_state = "中性"
except Exception as e:
    nh_state = "中性"
    print(f"  计算失败: {e}")

# ---- 状态路由表 ----
print("\n" + "=" * 70)
print("【市场状态路由表】")
print("=" * 70)

ROUTING_TABLE = {
    "底部试错":  {"宽度": "<30%", "估值": "低估", "趋势": "向下/震荡", "策略": "RFScore7+PB20 小仓位, 高股息防守"},
    "趋势进攻":  {"宽度": ">50%", "估值": "中性", "趋势": "向上",     "策略": "ETF动量满仓, RFScore7满仓"},
    "震荡轮动":  {"宽度": "30-50%","估值": "中性", "趋势": "震荡",    "策略": "ETF轮动半仓, 行业增强"},
    "高估防守":  {"宽度": ">70%", "估值": "高估", "趋势": "向上",     "策略": "降仓至30%, 债券/货基"},
}

df_route = pd.DataFrame(ROUTING_TABLE).T
print(df_route.to_string())

# ---- 当前状态判断 ----
print("\n" + "=" * 70)
print("【当前状态判断与策略建议】")
print("=" * 70)
print(f"  市场宽度: {breadth_state}")
print(f"  估值状态: {valuation_state}")
print(f"  趋势状态: {rsrs_state}")

# 简单规则路由
if breadth_state == "底部" and valuation_state == "低估":
    current_regime = "底部试错"
elif rsrs_state == "趋势向上" and breadth_state != "底部":
    current_regime = "趋势进攻"
elif valuation_state == "高估":
    current_regime = "高估防守"
else:
    current_regime = "震荡轮动"

print(f"\n  => 当前状态: 【{current_regime}】")
print(f"  => 策略建议: {ROUTING_TABLE[current_regime]['策略']}")
print("\n验证完成!")
```

### 执行命令

```bash
cd skills/joinquant_nookbook
node run-skill.js \
  --notebook-url <your_research_notebook_url> \
  --cell-source "$(cat /tmp/verify_08.py)" \
  --timeout-ms 120000
```

### 预期输出与判断标准

| 状态标签 | 对应策略优先级 |
|---------|--------------|
| 底部试错 | RFScore7+PB20 小仓位，高股息防守 |
| 趋势进攻 | ETF动量满仓，RFScore7满仓 |
| 震荡轮动 | ETF轮动半仓，行业增强辅助 |
| 高估防守 | 降仓至30%，债券/货基 |

### 结论记录

> 运行后在此填写：当前市场状态标签，以及对应的策略优先级建议。
