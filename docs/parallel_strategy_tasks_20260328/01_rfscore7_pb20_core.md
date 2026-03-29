# 任务 01：RFScore7 + PB20 核心母策略复核

## 设计文档

### 任务定位

- 优先级：最高
- 类型：实盘候选母策略
- 目标：确认这条线是不是当前仓库里最接近“能先跑起来”的股票主策略

### 为什么值得现在研究

- `RFScore7终极版策略总结.md` 已经给出仓库内最完整的一条证据链
- 当前本地结论指向 `RFScore7 + PB低20% + 温和市场状态调节`，不是裸 `RFScore7`
- `2026-03-27` 的本地市场快照显示：市场宽度偏低、估值偏低，这种环境更适合做“质量 + 低估 + 控仓”

### 参考矿脉

- `RFScore7终极版策略总结.md`
- `strategies/rfscore7_pb20_final.py`
- `strategies/rfscore7_base_800.py`
- `聚宽有价值策略558/98 FScore9因子模型改进——RFScore7因子.ipynb`
- `聚宽有价值策略558/52 市场宽度——简洁版.ipynb`
- `聚宽有价值策略558/59 研究 【复现】RSRS择时改进.ipynb`
- `聚宽有价值策略558/60 研究 【分享】对RSRS模型的一次修改.ipynb`

### 核心假设

- 原始 `RFScore7` 是质量主引擎
- `PB` 是最有效的估值增强器
- 当前市场下，弱宽度环境里“少持仓、精选股、温和降仓”比激进满仓更合理

### 本轮只做什么

1. 复核 `RFScore7 + PB20` 在最近样本是否仍是最优版本。
2. 比较 `PB10 / PB20 / PB30-40 / 不加PB` 四个版本。
3. 比较 `无状态过滤 / 宽度过滤 / 宽度+趋势过滤` 三种风控。
4. 输出当前交易日候选股、目标持仓数和是否建议实盘跟踪。

### 明确不做什么

- 不扩成几十个花哨因子
- 不优先追求历史最好看的净值
- 不把文档里的旧收益数字直接当结论

### 交付物

1. 一张参数对比表：收益、回撤、夏普、胜率、换手、持仓集中度。
2. 一份当前市场候选清单：代码、排序原因、为何入选。
3. 一个结论：`继续作为一号母策略 / 降级为备选 / 放弃`
4. 一个下一步建议：最值得继续微调的 2 到 3 个参数

### 成功判据

- 能确认这条线是否仍然是仓库里最强实盘候选
- 能解释“为什么这个版本比别的版本更靠谱”
- 能给出当前市场是否值得跟踪、应持多少仓的明确判断

## 子任务提示词

```text
你现在是一个量化研究子任务，负责复核仓库里证据最完整的股票母策略：RFScore7 + PB低估增强。

你的工作目标不是写综述，而是判断这条线现在是否值得优先实盘跟踪。

请优先阅读这些材料：
- RFScore7终极版策略总结.md
- strategies/rfscore7_pb20_final.py
- strategies/rfscore7_base_800.py
- 聚宽有价值策略558/98 FScore9因子模型改进——RFScore7因子.ipynb
- 聚宽有价值策略558/52 市场宽度——简洁版.ipynb
- 聚宽有价值策略558/59 研究 【复现】RSRS择时改进.ipynb
- 聚宽有价值策略558/60 研究 【分享】对RSRS模型的一次修改.ipynb

请完成以下事情：
1. 先还原原始 RFScore7 的真实定义，避免用错“简化版”。
2. 用统一口径比较以下版本：
   - 裸 RFScore7
   - RFScore7 + PB10
   - RFScore7 + PB20
   - RFScore7 + PB30-40
3. 比较以下风控方式：
   - 不做状态过滤
   - 仅宽度过滤
   - 宽度 + 趋势过滤
4. 输出当前市场下的候选股、目标持仓数和实盘建议。

输出要求：
- 先给结论，再给证据。
- 必须明确写出 Go / No-Go / Watch。
- 必须指出这条线最可能失效的市场环境。
- 如果发现现有代码或文档有错，直接指出并修正口径。
- 不要停留在“值得研究”，要回答“值不值得先跑”。
```

## 实际效果验证

### 验证方式

通过 `skills/joinquant_nookbook` 在聚宽 Research 环境中运行以下代码，对 RFScore7 + PB 各版本做真实数据对比，不依赖文档里的历史数字。

### 验证代码

将以下代码通过 `joinquant_nookbook` 提交到聚宽 notebook 执行：

```python
# RFScore7 + PB 版本对比验证
# 运行方式: node skills/joinquant_nookbook/run-skill.js --notebook-url <your_notebook_url> --cell-source "$(cat this_code)"

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 70)
print("RFScore7 + PB 版本对比验证 (2023-01-01 ~ 2025-12-31)")
print("=" * 70)

START = "2023-01-01"
END   = "2025-12-31"
HOLD_N = 20          # 持仓数量
REBAL_FREQ = "month" # 月度调仓

def get_monthly_rebal_dates(start, end):
    days = get_trade_days(start, end)
    result, last_m = [], None
    for d in days:
        if d.month != last_m:
            result.append(d)
            last_m = d.month
    return result

def calc_rfscore7(stocks, date):
    """计算 RFScore7 核心因子 (7个财务质量维度)"""
    q = query(
        valuation.code,
        indicator.roe,
        indicator.roa,
        indicator.gross_profit_margin,
        indicator.net_profit_margin,
        indicator.inc_net_profit_year_on_year,
        indicator.inc_revenue_year_on_year,
        valuation.pb_ratio,
        valuation.pe_ratio,
        valuation.market_cap,
    ).filter(valuation.code.in_(stocks))
    df = get_fundamentals(q, date=date).set_index("code").dropna(subset=["roe","roa","pb_ratio"])

    score = pd.Series(0, index=df.index)
    score += (df["roe"] > 0).astype(int)
    score += (df["roa"] > 0).astype(int)
    score += (df["gross_profit_margin"] > df["gross_profit_margin"].median()).astype(int)
    score += (df["net_profit_margin"] > 0).astype(int)
    score += (df["inc_net_profit_year_on_year"] > 0).astype(int)
    score += (df["inc_revenue_year_on_year"] > 0).astype(int)
    score += (df["pe_ratio"] > 0).astype(int)
    df["rfscore7"] = score
    return df

def filter_stocks_basic(stocks, date):
    """过滤ST和停牌"""
    try:
        is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()
    except:
        pass
    return stocks

def run_version(pb_pct, label, dates, universe):
    """运行一个 PB 版本的月度回测"""
    monthly_rets = []
    for i, d in enumerate(dates[:-1]):
        d_str = str(d)
        next_d_str = str(dates[i+1])
        try:
            stks = filter_stocks_basic(universe, d_str)
            df = calc_rfscore7(stks, d_str)
            if df.empty:
                continue
            # PB 过滤
            if pb_pct is not None:
                pb_thresh = df["pb_ratio"].quantile(pb_pct / 100)
                df = df[df["pb_ratio"] <= pb_thresh]
            # 按 RFScore7 降序选 HOLD_N 只
            selected = df.nlargest(HOLD_N, "rfscore7").index.tolist()
            if not selected:
                continue
            p0 = get_price(selected, end_date=d_str, count=1, fields=["close"], panel=False)
            p1 = get_price(selected, end_date=next_d_str, count=1, fields=["close"], panel=False)
            p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
            ret = ((p1 / p0) - 1).dropna().mean()
            monthly_rets.append(ret)
        except Exception as e:
            continue
    if not monthly_rets:
        return None
    s = pd.Series(monthly_rets)
    cum = (1 + s).cumprod()
    ann = (cum.iloc[-1]) ** (12 / len(s)) - 1
    dd = (cum / cum.cummax() - 1).min()
    sharpe = s.mean() / s.std() * (12 ** 0.5) if s.std() > 0 else 0
    win = (s > 0).mean()
    return {"版本": label, "年化收益": f"{ann:.1%}", "最大回撤": f"{dd:.1%}",
            "夏普": f"{sharpe:.2f}", "月胜率": f"{win:.0%}", "样本月数": len(s)}

# 股票池：中证800
universe = get_index_stocks("000906.XSHG")
dates = get_monthly_rebal_dates(START, END)
print(f"股票池: 中证800 ({len(universe)}只), 调仓次数: {len(dates)-1}")

versions = [
    (None,  "裸 RFScore7"),
    (10,    "RFScore7 + PB10%"),
    (20,    "RFScore7 + PB20%"),
    (35,    "RFScore7 + PB30-40%"),
]

rows = []
for pb_pct, label in versions:
    print(f"\n  运行: {label} ...")
    r = run_version(pb_pct, label, dates, universe)
    if r:
        rows.append(r)
        print(f"    年化={r['年化收益']}  回撤={r['最大回撤']}  夏普={r['夏普']}  胜率={r['月胜率']}")

print("\n" + "=" * 70)
print("【版本对比汇总】")
print("=" * 70)
if rows:
    df_res = pd.DataFrame(rows).set_index("版本")
    print(df_res.to_string())

# 当前市场候选股 (最新调仓日)
print("\n" + "=" * 70)
print("【当前市场候选股 (RFScore7 + PB20%)】")
print("=" * 70)
today = get_trade_days(end_date="2026-03-28", count=1)[-1]
stks = filter_stocks_basic(universe, str(today))
df_today = calc_rfscore7(stks, str(today))
pb_thresh = df_today["pb_ratio"].quantile(0.20)
df_today = df_today[df_today["pb_ratio"] <= pb_thresh]
candidates = df_today.nlargest(HOLD_N, "rfscore7")[["rfscore7","pb_ratio","pe_ratio","roe"]]
print(f"候选日期: {today}")
print(candidates.to_string())
print("\n验证完成!")
```

### 执行命令

```bash
# 1. 列出可用 notebook
cd skills/joinquant_nookbook
node run-skill.js --notebook-url <your_research_notebook_url> \
  --cell-source "print('ping')" --timeout-ms 10000

# 2. 运行完整验证（将上方代码保存为 /tmp/verify_01.py 后执行）
node run-skill.js \
  --notebook-url <your_research_notebook_url> \
  --cell-source "$(cat /tmp/verify_01.py)" \
  --timeout-ms 300000
```

### 预期输出与判断标准

| 指标 | 通过标准 | 不通过 |
|------|---------|--------|
| RFScore7+PB20 年化收益 | > 裸 RFScore7 | 无明显提升则降级 |
| 最大回撤 | < 30% | > 40% 需加风控 |
| 夏普比率 | > 0.8 | < 0.5 需重新审视 |
| 月胜率 | > 55% | < 50% 需排查 |

### 结论记录

> 运行后在此填写实测结论：Go / No-Go / Watch，以及最值得微调的参数。
