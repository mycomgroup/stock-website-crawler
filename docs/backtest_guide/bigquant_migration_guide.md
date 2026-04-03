# BigQuant 平台迁移指南

## 一、平台概述

BigQuant AIStudio 是基于 VS Code Web + Jupyter 的量化研究平台，使用 **DAI（Data Access Interface）** 作为核心数据接口，通过 SQL 查询获取数据。

**Skill 目录**：`skills/bigquant_strategy`

**运行方式**：
```bash
node run-skill.js --strategy your_strategy.py --start-date 2023-01-01 --end-date 2023-12-31
```

---

## 二、免费账户可用数据（实测）

| 数据类型 | 表名 | 可用字段 | 状态 |
|---------|------|---------|------|
| 日K线 | `cn_stock_bar1d` | date, instrument, name, open, high, low, close, volume, amount, pre_close, adjust_factor, change_ratio, turn, **upper_limit, lower_limit** | ✅ |
| 估值 | `cn_stock_valuation` | date, instrument, total_market_cap, float_market_cap, pe_ttm, pe_leading, pb, ps_ttm, pcf_net_ttm, dividend_yield_ratio | ✅ |
| 股票列表 | `cn_stock_instruments` | date, instrument, name, type | ✅（需 filters） |
| 行业分类 | `cn_stock_industry` | industry, industry_level1/2/3/4_name/code | ✅ |
| 资产负债表 | `cn_stock_balance_sheet` | 完整财务字段 | ✅（需 filters） |
| 分钟线 | `cn_stock_bar1m` | — | ❌ 需付费 |
| 指数K线 | `cn_index_bar1d` | — | ❌ 需付费 |
| 财务指标 | `cn_stock_financial_indicator` | — | ❌ 需付费 |

> `cn_stock_bar1d` 已包含 `upper_limit`（涨停价）和 `lower_limit`（跌停价），无需手动计算。

---

## 三、DAI 核心用法

### 基本查询

```python
import dai
import pandas as pd

# 查询日K线
df = dai.query("""
    SELECT date, instrument, open, high, low, close, volume, amount,
           upper_limit, lower_limit, change_ratio, turn
    FROM cn_stock_bar1d
    WHERE date = '2024-01-02'
    LIMIT 100
""").df()

# 查询估值
df = dai.query("""
    SELECT date, instrument, pe_ttm, pb, total_market_cap, float_market_cap
    FROM cn_stock_valuation
    WHERE date = '2024-01-02'
""").df()

# 需要 filters 的表（大表必须指定分区）
df = dai.query(
    "SELECT * FROM cn_stock_instruments",
    filters={"date": ["2024-01-02"]}
).df()

df = dai.query(
    "SELECT * FROM cn_stock_balance_sheet WHERE instrument='000001.SZ'",
    filters={"date": ["2024-01-01", "2024-12-31"]}
).df()
```

### 多日期查询

```python
# 查询一段时间的数据
df = dai.query("""
    SELECT date, instrument, close, volume
    FROM cn_stock_bar1d
    WHERE date >= '2024-01-01' AND date <= '2024-03-31'
      AND instrument IN ('000001.SZ', '000002.SZ', '600000.SH')
    ORDER BY date, instrument
""").df()
```

---

## 四、API 对照表

### 4.1 获取股票列表

| 平台 | 代码 |
|------|------|
| JoinQuant | `get_all_securities("stock", date).index.tolist()` |
| RiceQuant | `[s.order_book_id for s in all_instruments("CS")]` |
| **BigQuant** | `dai.query("SELECT instrument FROM cn_stock_instruments", filters={"date": [date]}).df()["instrument"].tolist()` |

### 4.2 获取历史K线

| 平台 | 代码 |
|------|------|
| JoinQuant | `get_price(stock, end_date=date, count=20, fields=["close"])` |
| RiceQuant | `history_bars(stock, 20, "1d", "close")` |
| **BigQuant** | `dai.query(f"SELECT date,close FROM cn_stock_bar1d WHERE instrument='{stock}' ORDER BY date DESC LIMIT 20").df()` |

### 4.3 获取估值数据

| 平台 | 代码 |
|------|------|
| JoinQuant | `get_fundamentals(query(valuation.pe_ratio, valuation.pb_ratio), date=date)` |
| RiceQuant | `get_fundamentals(query(fundamentals.eod_derivative_indicator.pe_ratio), entry_date=date)` |
| **BigQuant** | `dai.query(f"SELECT instrument,pe_ttm,pb,total_market_cap FROM cn_stock_valuation WHERE date='{date}'").df()` |

### 4.4 获取涨跌停价

| 平台 | 代码 |
|------|------|
| JoinQuant | `get_current_data()[stock].high_limit` |
| RiceQuant | `history_bars(stock, 1, "1d", "limit_up")[-1]` |
| **BigQuant** | `dai.query(f"SELECT upper_limit,lower_limit FROM cn_stock_bar1d WHERE date='{date}' AND instrument='{stock}'").df()` |

### 4.5 获取行业分类

| 平台 | 代码 |
|------|------|
| JoinQuant | `get_industry(stocks, date=date)` |
| RiceQuant | `instruments(stock).shenwan_industry_name` |
| **BigQuant** | `dai.query("SELECT instrument,industry_level1_name,industry_level2_name FROM cn_stock_industry").df()` |

---

## 五、策略代码迁移模板

### 5.1 选股策略（Notebook 格式）

```python
import dai
import pandas as pd

# ── 参数 ──────────────────────────────────────────────
date = "2024-01-02"
pb_max = 2.0
pe_max = 30.0
market_cap_min = 5e9   # 50亿
top_n = 30

# ── 获取股票池 ────────────────────────────────────────
stocks_df = dai.query(
    "SELECT instrument, name FROM cn_stock_instruments",
    filters={"date": [date]}
).df()
stocks_df = stocks_df[stocks_df["type"] == "stock"]
print("股票总数:", len(stocks_df))

# ── 获取估值数据 ──────────────────────────────────────
val_df = dai.query("""
    SELECT instrument, pe_ttm, pb, total_market_cap, float_market_cap
    FROM cn_stock_valuation
    WHERE date = '{date}'
""".format(date=date)).df()

# ── 合并筛选 ──────────────────────────────────────────
df = stocks_df.merge(val_df, on="instrument", how="inner")
df = df[
    (df["pb"] > 0) & (df["pb"] < pb_max) &
    (df["pe_ttm"] > 0) & (df["pe_ttm"] < pe_max) &
    (df["total_market_cap"] > market_cap_min)
].sort_values("total_market_cap").head(top_n)

print("选出股票:", len(df))
print(df[["instrument", "name", "pe_ttm", "pb", "total_market_cap"]].to_string())
```

### 5.2 回测框架（手动实现）

```python
import dai
import pandas as pd
import numpy as np

# ── 参数 ──────────────────────────────────────────────
START_DATE = "2023-01-01"
END_DATE   = "2023-12-31"
CAPITAL    = 1_000_000
TOP_N      = 20
REBALANCE  = "monthly"  # monthly / weekly

# ── 获取交易日 ────────────────────────────────────────
cal_df = dai.query("""
    SELECT DISTINCT date FROM cn_stock_bar1d
    WHERE date >= '{start}' AND date <= '{end}'
    ORDER BY date
""".format(start=START_DATE, end=END_DATE)).df()
trade_dates = cal_df["date"].tolist()
print("交易日数:", len(trade_dates))

# ── 选股函数 ──────────────────────────────────────────
def select_stocks(date):
    val = dai.query("""
        SELECT v.instrument, v.pe_ttm, v.pb, v.total_market_cap
        FROM cn_stock_valuation v
        WHERE v.date = '{date}'
          AND v.pb > 0 AND v.pb < 3
          AND v.pe_ttm > 0 AND v.pe_ttm < 40
          AND v.total_market_cap > 3e9
        ORDER BY v.total_market_cap ASC
        LIMIT {n}
    """.format(date=date, n=TOP_N)).df()
    return val["instrument"].tolist()

# ── 获取收益率 ────────────────────────────────────────
def get_returns(stocks, start, end):
    if not stocks:
        return {}
    inst_list = "','".join(stocks)
    df = dai.query("""
        SELECT instrument, date, close
        FROM cn_stock_bar1d
        WHERE date >= '{start}' AND date <= '{end}'
          AND instrument IN ('{insts}')
        ORDER BY instrument, date
    """.format(start=start, end=end, insts=inst_list)).df()

    returns = {}
    for inst, g in df.groupby("instrument"):
        g = g.sort_values("date")
        if len(g) >= 2:
            returns[inst] = g["close"].iloc[-1] / g["close"].iloc[0] - 1
    return returns

# ── 简单回测循环 ──────────────────────────────────────
portfolio_value = [CAPITAL]
rebalance_dates = trade_dates[::20]  # 每月约20个交易日

for i, rb_date in enumerate(rebalance_dates[:-1]):
    next_rb = rebalance_dates[i + 1]
    stocks = select_stocks(rb_date)
    if not stocks:
        portfolio_value.append(portfolio_value[-1])
        continue
    rets = get_returns(stocks, rb_date, next_rb)
    avg_ret = np.mean(list(rets.values())) if rets else 0
    portfolio_value.append(portfolio_value[-1] * (1 + avg_ret))

# ── 计算指标 ──────────────────────────────────────────
pv = pd.Series(portfolio_value)
total_return = pv.iloc[-1] / pv.iloc[0] - 1
annual_return = (1 + total_return) ** (252 / len(trade_dates)) - 1
drawdown = (pv / pv.cummax() - 1).min()

print("\n=== 回测结果 ===")
print("总收益率: {:.2f}%".format(total_return * 100))
print("年化收益率: {:.2f}%".format(annual_return * 100))
print("最大回撤: {:.2f}%".format(drawdown * 100))
```

---

## 六、从 JoinQuant/RiceQuant 迁移

### 6.1 迁移难度评估

| 策略类型 | 迁移难度 | 说明 |
|---------|---------|------|
| 小市值选股 | 低 | `cn_stock_valuation.total_market_cap` 直接可用 |
| PE/PB 价值选股 | 低 | `cn_stock_valuation` 完整支持 |
| 涨停板策略 | 低 | `cn_stock_bar1d.upper_limit` 直接可用 |
| 行业轮动 | 低 | `cn_stock_industry` 支持 |
| 动量/均线策略 | 中 | 需用 SQL 查询历史K线手动计算 |
| 财务因子策略 | 中 | `cn_stock_balance_sheet` 需 filters |
| 指数增强 | 高 | 指数K线需付费 |
| 分钟级策略 | 高 | 分钟线需付费 |

### 6.2 关键差异

| 特性 | JoinQuant/RiceQuant | BigQuant |
|------|---------------------|---------|
| 数据接口 | 函数调用 | SQL 查询（DAI） |
| 回测框架 | 内置（initialize/handle_bar） | 无，需手动实现 |
| 指数数据 | 免费 | 需付费 |
| 涨跌停价 | 需计算或特殊API | `cn_stock_bar1d` 直接有 |
| 复权因子 | 自动 | `adjust_factor` 字段，需手动处理 |
| 时间限制 | 180分钟/天 | 无限制（免费资源） |

### 6.3 复权处理

BigQuant 的 `cn_stock_bar1d` 返回的是**前复权价格**（adjust_factor 已乘入），直接使用即可：

```python
# 直接使用，已是前复权价格
df = dai.query("""
    SELECT date, instrument, close, volume
    FROM cn_stock_bar1d
    WHERE instrument = '000001.SZ'
    ORDER BY date DESC LIMIT 60
""").df()
```

---

## 七、完整示例：小市值策略

```python
"""
小市值策略 - BigQuant 版本
对应 JoinQuant 的 small_cap_strategy.py
"""
import dai
import pandas as pd
import numpy as np

START_DATE = "2023-01-01"
END_DATE   = "2023-12-31"
CAPITAL    = 1_000_000
TOP_N      = 30

def select_stocks(date):
    """选出市值最小的 TOP_N 只股票"""
    df = dai.query("""
        SELECT v.instrument, v.total_market_cap, v.pe_ttm, v.pb
        FROM cn_stock_valuation v
        INNER JOIN (
            SELECT instrument FROM cn_stock_instruments
        ) i ON v.instrument = i.instrument
        WHERE v.date = '{date}'
          AND v.total_market_cap > 0
          AND v.pe_ttm > 0
        ORDER BY v.total_market_cap ASC
        LIMIT {n}
    """.format(date=date, n=TOP_N)).df()
    return df["instrument"].tolist()

# 获取月度调仓日
dates_df = dai.query("""
    SELECT DISTINCT date FROM cn_stock_bar1d
    WHERE date >= '{s}' AND date <= '{e}'
    ORDER BY date
""".format(s=START_DATE, e=END_DATE)).df()
all_dates = dates_df["date"].tolist()
rebalance_dates = all_dates[::20]

# 回测
nav = [1.0]
for i in range(len(rebalance_dates) - 1):
    d0, d1 = rebalance_dates[i], rebalance_dates[i+1]
    stocks = select_stocks(d0)
    if not stocks:
        nav.append(nav[-1])
        continue

    inst_str = "','".join(stocks)
    price_df = dai.query("""
        SELECT instrument, date, close
        FROM cn_stock_bar1d
        WHERE date IN ('{d0}', '{d1}')
          AND instrument IN ('{insts}')
    """.format(d0=d0, d1=d1, insts=inst_str)).df()

    rets = []
    for inst, g in price_df.groupby("instrument"):
        g = g.sort_values("date")
        if len(g) == 2:
            rets.append(g["close"].iloc[1] / g["close"].iloc[0] - 1)

    nav.append(nav[-1] * (1 + np.mean(rets) if rets else 1))

total = nav[-1] - 1
annual = (nav[-1]) ** (252 / len(all_dates)) - 1
nav_s = pd.Series(nav)
mdd = (nav_s / nav_s.cummax() - 1).min()

print("=== 小市值策略回测结果 ===")
print("总收益: {:.2f}%".format(total * 100))
print("年化收益: {:.2f}%".format(annual * 100))
print("最大回撤: {:.2f}%".format(mdd * 100))
```

---

## 八、何时选择 BigQuant

**适合 BigQuant 的场景：**
- 需要无时间限制的长期回测
- 策略依赖涨跌停价（直接内置）
- 需要 SQL 灵活查询数据
- 想用 Python 完全自定义回测逻辑

**不适合 BigQuant 的场景（免费账户）：**
- 需要指数K线数据（如 000300.SH）
- 需要分钟级数据
- 需要复杂财务因子（需付费数据）

**与其他平台的定位：**

| 阶段 | 平台 | 原因 |
|------|------|------|
| 快速验证 | JoinQuant Notebook | 无时间限制，API 丰富 |
| 完整回测 | RiceQuant 策略编辑器 | 自动回测框架 |
| 长期研究 | **BigQuant** | 无时间限制 + SQL 灵活查询 |
| 最终验证 | JoinQuant Strategy | 最权威平台 |
