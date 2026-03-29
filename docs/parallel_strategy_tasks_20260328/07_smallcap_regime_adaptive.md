# 任务 07：小市值 / 国九 / 微盘适配线

## 设计文档

### 任务定位

- 优先级：中高
- 类型：高弹性但高风格依赖赛道
- 目标：判断小市值线在当前规则与当前市场下，是否还有值得保留的母策略

### 为什么值得现在研究

- 仓库里小市值、微盘、国九条、低价股相关材料非常多，是天然的大分支
- 这条线潜在收益高，但也最容易被风格切换、流动性、监管变化击穿
- 如果能筛出“低摩擦、可解释、不过分依赖极端行情”的版本，价值很高

### 参考矿脉

- `聚宽有价值策略558/06 国九小市值策略【年化100.5% 回撤25.6%】.txt`
- `聚宽有价值策略558/08 国九条后中小板微盘小改，年化135.40%.txt`
- `聚宽有价值策略558/15 小市值策略之再优化，年化接近翻倍.txt`
- `聚宽有价值策略558/18 微盘股400多角度深入研究.txt`
- `聚宽有价值策略558/94 微盘股和大盘股分析，然后预测小市值行情.ipynb`
- `聚宽有价值策略558/03 截止到21年12月依然有效的小市值适配因子.txt`
- `聚宽有价值策略558/89 基于Gyro^.^大神的小市值策略的因子匹配研究.txt`

### 核心假设

- 小市值不是不能做，而是必须先区分 `可实盘` 和 `回测很猛`
- 当前更应优先研究“规则适配 + 容量可接受 + 风险可控”的版本
- 小市值是否值得上仓位，必须和市场状态联动判断

### 本轮只做什么

1. 拆分 `国九条筛选`、`微盘再平衡`、`成长小盘` 三条线。
2. 看它们对成交额、持仓数量、再平衡频率的要求。
3. 判断当前市场下，小市值线应否进入第一批实跑。
4. 输出一版“小市值启用条件”。

### 明确不做什么

- 不追逐标题里离谱的历史收益
- 不忽视容量、涨停买不到、冲击成本
- 不把微盘和小盘混为一谈

### 交付物

1. 一张小市值三分支对比表。
2. 一份当前市场适配判断：能不能做、什么时候做、做哪类。
3. 一个结论：`先跑 / 观察 / 暂不碰`

### 成功判据

- 能把这条高噪音赛道压缩成少数几个可行动版本
- 能明确指出“当前最不该先碰”的那一类小市值策略

## 子任务提示词

```text
你现在是小市值赛道子任务。你的目标是从仓库里最拥挤、最吵闹的一条线中，筛出真正值得保留的母策略，而不是继续被一堆高收益标题带偏。

请优先阅读这些材料：
- 聚宽有价值策略558/06 国九小市值策略【年化100.5% 回撤25.6%】.txt
- 聚宽有价值策略558/08 国九条后中小板微盘小改，年化135.40%.txt
- 聚宽有价值策略558/15 小市值策略之再优化，年化接近翻倍.txt
- 聚宽有价值策略558/18 微盘股400多角度深入研究.txt
- 聚宽有价值策略558/94 微盘股和大盘股分析，然后预测小市值行情.ipynb
- 聚宽有价值策略558/03 截止到21年12月依然有效的小市值适配因子.txt

请完成以下事情：
1. 把赛道拆成：
   - 国九条/规则筛选型
   - 微盘再平衡型
   - 成长小盘型
2. 分别评估：
   - 容量
   - 流动性
   - 调仓频率
   - 当前市场适配性
3. 给出“小市值启用条件”：
   - 什么市场可以做
   - 什么市场不该做
   - 需要哪些风控

输出要求：
- 必须明确指出最值得保留的一条小市值母线。
- 必须明确指出最像“回测幻觉”的一条线。
- 如果当前不适合做小市值，要明确说不建议先跑。
```

## 实际效果验证

### 验证方式

在聚宽 Research 中对比国九条筛选、微盘再平衡、成长小盘三条线的容量、流动性和当前市场适配性，重点排查"回测幻觉"。

### 验证代码

```python
# 小市值三分支验证
# 重点: 容量、流动性、当前市场适配性

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 70)
print("小市值三分支验证 (2022-01-01 ~ 2025-12-31)")
print("=" * 70)

START  = "2022-01-01"
END    = "2025-12-31"
HOLD_N = 20
COST   = 0.003  # 小市值冲击成本更高，用3倍

def get_monthly_dates(start, end):
    days = get_trade_days(start, end)
    result, last_m = [], None
    for d in days:
        if d.month != last_m:
            result.append(d)
            last_m = d.month
    return result

def filter_basic(stocks, date):
    try:
        is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()
    except:
        pass
    return stocks

# ---- 分支1: 国九条筛选型 ----
def select_guojiu(date, n=HOLD_N):
    """国九条: 市值10-50亿 + 正盈利 + 低PE + 成交额过滤"""
    q = query(
        valuation.code, valuation.market_cap, valuation.pe_ratio,
        indicator.inc_net_profit_year_on_year, valuation.circulating_market_cap
    ).filter(
        valuation.market_cap > 10,
        valuation.market_cap < 50,
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 40,
        indicator.inc_net_profit_year_on_year > 0
    ).order_by(valuation.pe_ratio.asc()).limit(n * 5)
    df = get_fundamentals(q, date=date)
    # 流动性过滤: 日均成交额 > 3000万
    stks = filter_basic(df["code"].tolist(), date)
    try:
        money = get_price(stks, end_date=date, count=20, fields=["money"], panel=False)
        avg_money = money.groupby("code")["money"].mean()
        liquid = avg_money[avg_money > 3e7].index.tolist()
        stks = [s for s in stks if s in liquid]
    except:
        pass
    return stks[:n]

# ---- 分支2: 微盘再平衡型 ----
def select_micro_cap(date, n=HOLD_N):
    """微盘: 市值<30亿 + 低PB + 月度再平衡"""
    q = query(
        valuation.code, valuation.market_cap, valuation.pb_ratio,
        valuation.circulating_market_cap
    ).filter(
        valuation.market_cap > 5,
        valuation.market_cap < 30,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < 3
    ).order_by(valuation.market_cap.asc()).limit(n * 5)
    df = get_fundamentals(q, date=date)
    stks = filter_basic(df["code"].tolist(), date)
    # 严格流动性: 日均成交额 > 1000万
    try:
        money = get_price(stks, end_date=date, count=20, fields=["money"], panel=False)
        avg_money = money.groupby("code")["money"].mean()
        liquid = avg_money[avg_money > 1e7].index.tolist()
        stks = [s for s in stks if s in liquid]
    except:
        pass
    return stks[:n]

# ---- 分支3: 成长小盘型 ----
def select_growth_small(date, n=HOLD_N):
    """成长小盘: 市值30-150亿 + 高增长 + 合理估值"""
    q = query(
        valuation.code, valuation.market_cap, valuation.pe_ratio,
        indicator.inc_net_profit_year_on_year, indicator.roe
    ).filter(
        valuation.market_cap > 30,
        valuation.market_cap < 150,
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 50,
        indicator.inc_net_profit_year_on_year > 20,
        indicator.roe > 10
    ).order_by(indicator.inc_net_profit_year_on_year.desc()).limit(n * 3)
    df = get_fundamentals(q, date=date)
    stks = filter_basic(df["code"].tolist(), date)
    return stks[:n]

def run_branch(select_fn, label, dates):
    rets, turnovers = [], []
    prev = []
    for i, d in enumerate(dates[:-1]):
        d_str = str(d)
        next_d_str = str(dates[i+1])
        try:
            selected = select_fn(d_str)
            if not selected:
                continue
            p0 = get_price(selected, end_date=d_str, count=1, fields=["close"], panel=False)
            p1 = get_price(selected, end_date=next_d_str, count=1, fields=["close"], panel=False)
            p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
            gross = ((p1 / p0) - 1).dropna().mean()
            turnover = len(set(selected) - set(prev)) / max(len(selected), 1)
            rets.append(gross - turnover * COST * 2)
            turnovers.append(turnover)
            prev = selected
        except:
            continue
    if not rets:
        return None
    s = pd.Series(rets)
    cum = (1 + s).cumprod()
    ann = cum.iloc[-1] ** (12 / len(s)) - 1
    dd = (cum / cum.cummax() - 1).min()
    sharpe = s.mean() / s.std() * (12 ** 0.5) if s.std() > 0 else 0
    avg_to = np.mean(turnovers)
    return {"分支": label, "年化(扣费)": f"{ann:.1%}", "最大回撤": f"{dd:.1%}",
            "夏普": f"{sharpe:.2f}", "平均换手": f"{avg_to:.0%}", "样本月数": len(s)}

dates = get_monthly_dates(START, END)
print(f"调仓次数: {len(dates)-1}  (注: 小市值用3倍成本口径)")

branches = [
    (select_guojiu,      "国九条筛选型"),
    (select_micro_cap,   "微盘再平衡型"),
    (select_growth_small,"成长小盘型"),
]

rows = []
for fn, label in branches:
    print(f"  运行: {label} ...")
    r = run_branch(fn, label, dates)
    if r:
        rows.append(r)
        print(f"    年化={r['年化(扣费)']}  回撤={r['最大回撤']}  换手={r['平均换手']}")

print("\n" + "=" * 70)
print("【小市值三分支对比汇总】")
print("=" * 70)
if rows:
    df_res = pd.DataFrame(rows).set_index("分支")
    print(df_res.to_string())

# 当前市场适配性检查
print("\n" + "=" * 70)
print("【当前市场小市值适配性检查】")
print("=" * 70)
today = get_trade_days(end_date="2026-03-28", count=1)[-1]
# 检查微盘指数近期表现
try:
    micro_prices = get_price("399101.XSHE", end_date=str(today), count=60,
                             fields=["close"], panel=False)["close"]
    ret_1m = micro_prices.iloc[-1] / micro_prices.iloc[-20] - 1
    ret_3m = micro_prices.iloc[-1] / micro_prices.iloc[-60] - 1
    print(f"  中证2000近1月: {ret_1m:.1%}")
    print(f"  中证2000近3月: {ret_3m:.1%}")
    if ret_1m < -0.05 or ret_3m < -0.10:
        print("  ⚠️  当前小市值趋势偏弱，建议观察而非先跑")
    else:
        print("  ✓  小市值趋势尚可，可考虑小仓位试跑")
except Exception as e:
    print(f"  检查失败: {e}")
print("\n验证完成!")
```

### 执行命令

```bash
cd skills/joinquant_nookbook
node run-skill.js \
  --notebook-url <your_research_notebook_url> \
  --cell-source "$(cat /tmp/verify_07.py)" \
  --timeout-ms 300000
```

### 预期输出与判断标准

| 指标 | 判断逻辑 |
|------|---------|
| 扣费后年化 | 小市值用3倍成本，仍 > 15% 才值得 |
| 最大回撤 | > 40% 说明风险不可控 |
| 平均换手 | > 80% 说明冲击成本被严重低估 |
| 当前趋势 | 近1月 < -5% 则建议观察 |

### 结论记录

> 运行后在此填写：先跑 / 观察 / 暂不碰，以及最值得保留的一条小市值母线。
