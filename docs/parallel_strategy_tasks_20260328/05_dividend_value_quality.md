# 任务 05：红利 / 价值 / 质量防守进攻线

## 设计文档

### 任务定位

- 优先级：高
- 类型：当前市场适配型策略母线
- 目标：在弱宽度、低估值环境中，找到最可能先跑出效果的价值红利方向

### 为什么值得现在研究

- 本地快照显示：市场宽度偏低，但整体估值不贵
- 这种环境下，红利、价值、低杠杆、质量股比高换手短线更有现实意义
- 这条线与 RFScore7 互补，也更适合做中低换手实盘

### 参考矿脉

- `聚宽有价值策略558/04 高股息低市盈率高增长的价投策略.txt`
- `聚宽有价值策略558/16 大市值价值投资，从2005年至今超额稳定.txt`
- `聚宽有价值策略558/24 大容量低回撤价值投资-排除小市值因子.txt`
- `聚宽有价值策略558/35 【菜场大妈】股息率小市值策略,10年206倍,5年10.8倍.txt`
- `聚宽有价值策略558/36 【菜场大妈】股息率小市值策略,10年206倍,5年10.8倍.txt`
- `聚宽有价值策略558/70 超稳的股息率+均线选股策略.txt`
- `聚宽有价值策略558/79 国九条-新的红利因子，修正「审计意见」函数.txt`

### 核心假设

- 当前更值得研究的是“价值 / 红利 / 质量”的交叉区，而不是单一高股息
- 大容量价值与小市值红利是两条不同分支，不能混看
- 这条线应重点看容量、换手、风格依赖，而不是追最炸的历史曲线

### 本轮只做什么

1. 拆出三条代表线：`大盘价值`、`高股息质量`、`红利小盘`。
2. 用统一口径比较它们在最近样本的表现。
3. 结合当前低估值环境，判断哪一条最值得先跑。
4. 输出一个当前市场下的价值红利优先级排序。

### 明确不做什么

- 不把所有价值策略揉成一个大杂烩
- 不只看“年化”两个字
- 不默认小盘红利一定比大盘价值更优

### 交付物

1. 一张三条分支的对比表。
2. 一份当前市场适配判断：防守更适合哪条，进攻更适合哪条。
3. 一个建议：是否值得进入第一批实跑名单。

### 成功判据

- 能给出“当前最该先跑哪条价值红利线”的明确答案
- 能说清容量、换手、风格风险

## 子任务提示词

```text
你现在是价值红利子任务。你的目标是从仓库材料里挖出一条适合当前市场的价值 / 红利 / 质量策略线，而不是做泛泛的价值投资综述。

请优先阅读这些材料：
- 聚宽有价值策略558/04 高股息低市盈率高增长的价投策略.txt
- 聚宽有价值策略558/16 大市值价值投资，从2005年至今超额稳定.txt
- 聚宽有价值策略558/24 大容量低回撤价值投资-排除小市值因子.txt
- 聚宽有价值策略558/35 【菜场大妈】股息率小市值策略,10年206倍,5年10.8倍.txt
- 聚宽有价值策略558/70 超稳的股息率+均线选股策略.txt
- 聚宽有价值策略558/79 国九条-新的红利因子，修正「审计意见」函数.txt

请完成以下事情：
1. 拆成三条母线：
   - 大盘价值
   - 高股息质量
   - 红利小盘
2. 用统一口径比较最近样本的收益、回撤、换手、容量。
3. 结合当前“低宽度、低估值”的市场状态，判断更适合先跑哪条线。
4. 如果发现某条线明显依赖旧风格红利行情，要直接降级。

输出要求：
- 必须给出优先级排序。
- 必须明确写出适合当前市场的是“防守策略”还是“进攻策略”。
- 必须指出这条线与 RFScore7 的重合和差异。
```

## 实际效果验证

### 验证方式

在聚宽 Research 中对比大盘价值、高股息质量、红利小盘三条分支在最近样本的真实表现，结合当前低宽度低估值环境给出优先级。

### 验证代码

```python
# 红利 / 价值 / 质量三条分支验证
# 统一口径: 月度调仓, 持仓20只, 扣费比较

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 70)
print("红利/价值/质量三分支验证 (2022-01-01 ~ 2025-12-31)")
print("=" * 70)

START = "2022-01-01"
END   = "2025-12-31"
HOLD_N = 20
COST   = 0.001

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

# ---- 分支1: 大盘价值 ----
def select_large_value(date, n=HOLD_N):
    """大市值 + 低PE + 低PB + 正ROE"""
    q = query(
        valuation.code, valuation.pe_ratio, valuation.pb_ratio,
        valuation.market_cap, indicator.roe
    ).filter(
        valuation.market_cap > 200,   # 市值>200亿
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 25,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < 3,
        indicator.roe > 8
    ).order_by(valuation.pe_ratio.asc()).limit(n * 3)
    df = get_fundamentals(q, date=date)
    stks = filter_basic(df["code"].tolist(), date)
    return stks[:n]

# ---- 分支2: 高股息质量 ----
def select_dividend_quality(date, n=HOLD_N):
    """高股息率 + 低负债 + 稳定盈利"""
    q = query(
        valuation.code, valuation.pe_ratio, valuation.pb_ratio,
        indicator.roe, indicator.inc_net_profit_year_on_year,
        balance.total_liability, balance.total_assets
    ).filter(
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 20,
        indicator.roe > 10,
        indicator.inc_net_profit_year_on_year > 0
    ).order_by(indicator.roe.desc()).limit(n * 3)
    df = get_fundamentals(q, date=date)
    # 低负债率过滤
    df["debt_ratio"] = df["total_liability"] / df["total_assets"]
    df = df[df["debt_ratio"] < 0.6]
    stks = filter_basic(df["code"].tolist(), date)
    return stks[:n]

# ---- 分支3: 红利小盘 ----
def select_small_dividend(date, n=HOLD_N):
    """小市值 + 低PE + 正增长"""
    q = query(
        valuation.code, valuation.pe_ratio, valuation.pb_ratio,
        valuation.market_cap, indicator.inc_net_profit_year_on_year
    ).filter(
        valuation.market_cap > 10,
        valuation.market_cap < 100,  # 10-100亿小盘
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 30,
        indicator.inc_net_profit_year_on_year > 5
    ).order_by(valuation.pe_ratio.asc()).limit(n * 3)
    df = get_fundamentals(q, date=date)
    stks = filter_basic(df["code"].tolist(), date)
    return stks[:n]

def run_branch(select_fn, label, dates):
    rets = []
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
            turnover = len(set(selected) - set(prev)) / len(selected)
            rets.append(gross - turnover * COST * 2)
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
    win = (s > 0).mean()
    return {"分支": label, "年化(扣费)": f"{ann:.1%}", "最大回撤": f"{dd:.1%}",
            "夏普": f"{sharpe:.2f}", "月胜率": f"{win:.0%}", "样本月数": len(s)}

dates = get_monthly_dates(START, END)
print(f"调仓次数: {len(dates)-1}")

branches = [
    (select_large_value,    "大盘价值"),
    (select_dividend_quality, "高股息质量"),
    (select_small_dividend, "红利小盘"),
]

rows = []
for fn, label in branches:
    print(f"  运行: {label} ...")
    r = run_branch(fn, label, dates)
    if r:
        rows.append(r)
        print(f"    年化={r['年化(扣费)']}  回撤={r['最大回撤']}  夏普={r['夏普']}")

print("\n" + "=" * 70)
print("【三分支对比汇总】")
print("=" * 70)
if rows:
    df_res = pd.DataFrame(rows).set_index("分支")
    print(df_res.to_string())

# 当前市场候选 (大盘价值)
print("\n" + "=" * 70)
print("【当前大盘价值候选股 (Top10)】")
print("=" * 70)
today = get_trade_days(end_date="2026-03-28", count=1)[-1]
candidates = select_large_value(str(today), n=10)
if candidates:
    q = query(valuation.code, valuation.pe_ratio, valuation.pb_ratio,
              indicator.roe).filter(valuation.code.in_(candidates))
    df_c = get_fundamentals(q, date=str(today)).set_index("code")
    print(df_c.to_string())
print("\n验证完成!")
```

### 执行命令

```bash
cd skills/joinquant_nookbook
node run-skill.js \
  --notebook-url <your_research_notebook_url> \
  --cell-source "$(cat /tmp/verify_05.py)" \
  --timeout-ms 300000
```

### 预期输出与判断标准

| 分支 | 当前市场适配性判断逻辑 |
|------|----------------------|
| 大盘价值 | 低宽度环境首选，容量大，换手低 |
| 高股息质量 | 防守首选，与 RFScore7 互补 |
| 红利小盘 | 需确认流动性，当前宽度偏低时谨慎 |

### 结论记录

> 运行后在此填写：三条分支优先级排序，当前最适合先跑哪条，以及与 RFScore7 的重合度。
