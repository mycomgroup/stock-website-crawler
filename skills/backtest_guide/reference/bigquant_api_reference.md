# BigQuant DAI 数据 API 完整参考

> 实测日期：2026-04-03，账户类型：免费账户

## 一、数据表可用性总览

### ✅ 免费可用

| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `cn_stock_bar1d` | 日K线（含涨跌停价） | date, instrument, open, high, low, close, volume, amount, pre_close, adjust_factor, change_ratio, turn, **upper_limit, lower_limit** |
| `cn_stock_valuation` | 估值数据 | date, instrument, total_market_cap, float_market_cap, pe_ttm, pe_leading, pe_trailing, pb, ps_ttm, pcf_net_ttm, dividend_yield_ratio |
| `cn_stock_instruments` | 股票列表 | date, instrument, name, type（需 filters） |
| `cn_stock_industry` | 行业分类（恒生标准） | industry, industry_level1/2/3/4_name/code |
| `cn_stock_balance_sheet` | 资产负债表 | 完整财务字段（需 filters） |
| `cn_stock_dividend` | 分红数据 | date, instrument, bonus_rate, cash_before_tax, ex_date |
| `cn_stock_suspend` | 停牌数据 | date, instrument, suspend_period, suspend_reason |

### ❌ 需付费

| 表名 | 说明 |
|------|------|
| `cn_stock_bar1m/5m/15m/30m/60m` | 分钟线 |
| `cn_index_bar1d` | 指数日K线 |
| `cn_index_components` | 指数成分股 |
| `cn_stock_financial_indicator` | 财务指标 |
| `cn_stock_income_statement` | 利润表 |
| `cn_stock_cash_flow` | 现金流量表 |
| `cn_stock_moneyflow` | 资金流向 |
| `cn_macro_*` | 宏观数据（CPI/PPI/GDP/PMI） |
| `cn_stock_margin` | 融资融券 |
| `cn_stock_concept` | 概念板块 |

---

## 二、核心表字段详情

### cn_stock_bar1d — 日K线

```python
import dai

df = dai.query("""
    SELECT date, instrument, name,
           open, high, low, close, pre_close,
           volume, amount, deal_number,
           adjust_factor,    -- 复权因子（已前复权）
           change_ratio,     -- 涨跌幅
           turn,             -- 换手率
           upper_limit,      -- 涨停价（直接可用！）
           lower_limit       -- 跌停价（直接可用！）
    FROM cn_stock_bar1d
    WHERE date = '2024-01-02'
      AND instrument = '000001.SZ'
""").df()
```

**注意**：价格已经是前复权价格（adjust_factor 已乘入），直接使用。

### cn_stock_valuation — 估值

```python
df = dai.query("""
    SELECT date, instrument,
           total_market_cap,      -- 总市值（元）
           float_market_cap,      -- 流通市值（元）
           pe_ttm,                -- 市盈率TTM
           pe_leading,            -- 市盈率（预测）
           pe_trailing,           -- 市盈率（历史）
           pb,                    -- 市净率
           ps_ttm,                -- 市销率TTM
           pcf_net_ttm,           -- 市现率（净现金流）TTM
           pcf_op_ttm,            -- 市现率（经营现金流）TTM
           dividend_yield_ratio   -- 股息率
    FROM cn_stock_valuation
    WHERE date = '2024-01-02'
""").df()
```

**注意**：市值单位是**元**（不是亿元）。50亿 = 5e9。

### cn_stock_instruments — 股票列表

```python
# 必须用 filters 参数指定日期
df = dai.query(
    "SELECT date, instrument, name, type FROM cn_stock_instruments",
    filters={"date": ["2024-01-02"]}
).df()

# type 值：stock（股票）、fund（基金）等
stocks = df[df["type"] == "stock"]["instrument"].tolist()
```

### cn_stock_industry — 行业分类

```python
# 恒生行业分类，不需要日期参数
df = dai.query("SELECT * FROM cn_stock_industry").df()
# 字段：industry, industry_level1/2/3/4_name/code
# industry 值：hs2023（恒生2023标准）
```

**注意**：这个表是静态的，不含 instrument 字段，需要通过其他方式关联。

### cn_stock_balance_sheet — 资产负债表

```python
# 必须用 filters 参数
df = dai.query(
    "SELECT * FROM cn_stock_balance_sheet WHERE instrument='000001.SZ'",
    filters={"date": ["2024-01-01", "2024-12-31"]}
).df()
# 包含：total_assets, total_liab, total_owner_equity 等完整财务字段
```

---

## 三、API 对照表（JoinQuant / RiceQuant / BigQuant）

### 3.1 获取股票列表

| 平台 | 代码 |
|------|------|
| JoinQuant | `get_all_securities("stock", date).index.tolist()` |
| RiceQuant | `[s.order_book_id for s in all_instruments("CS")]` |
| BigQuant | `dai.query("SELECT instrument FROM cn_stock_instruments", filters={"date": [date]}).df()["instrument"].tolist()` |

### 3.2 获取历史K线

| 平台 | 代码 |
|------|------|
| JoinQuant | `get_price(stock, end_date=date, count=20, fields=["close"])` |
| RiceQuant | `history_bars(stock, 20, "1d", "close")` |
| BigQuant | `dai.query("SELECT date,close FROM cn_stock_bar1d WHERE instrument='{}' ORDER BY date DESC LIMIT 20".format(stock)).df()` |

### 3.3 获取估值数据

| 平台 | 代码 |
|------|------|
| JoinQuant | `get_fundamentals(query(valuation.pe_ratio, valuation.pb_ratio), date=date)` |
| RiceQuant | `get_fundamentals(query(fundamentals.eod_derivative_indicator.pe_ratio), entry_date=date)` |
| BigQuant | `dai.query("SELECT instrument,pe_ttm,pb,total_market_cap FROM cn_stock_valuation WHERE date='{}'".format(date)).df()` |

### 3.4 获取涨跌停价

| 平台 | 代码 |
|------|------|
| JoinQuant | `get_current_data()[stock].high_limit` |
| RiceQuant | `history_bars(stock, 1, "1d", "limit_up")[-1]` |
| BigQuant | `dai.query("SELECT upper_limit,lower_limit FROM cn_stock_bar1d WHERE date='{}' AND instrument='{}'".format(date, stock)).df()` |

### 3.5 判断涨停

| 平台 | 代码 |
|------|------|
| JoinQuant | `close == get_current_data()[stock].high_limit` |
| RiceQuant | `close >= limit_up * 0.999` |
| BigQuant | `close >= upper_limit * 0.999`（cn_stock_bar1d 直接有字段） |

### 3.6 获取行业

| 平台 | 代码 |
|------|------|
| JoinQuant | `get_industry(stocks, date=date)` |
| RiceQuant | `instruments(stock).shenwan_industry_name` |
| BigQuant | `dai.query("SELECT * FROM cn_stock_industry").df()`（静态表，需手动关联） |

---

## 四、DAI 查询技巧

### 4.1 基本语法

```python
import dai

# 简单查询
df = dai.query("SELECT * FROM cn_stock_bar1d WHERE date='2024-01-02' LIMIT 10").df()

# 带 filters（大表必须用）
df = dai.query(
    "SELECT * FROM cn_stock_instruments",
    filters={"date": ["2024-01-02"]}
).df()

# 日期范围 filters
df = dai.query(
    "SELECT * FROM cn_stock_balance_sheet WHERE instrument='000001.SZ'",
    filters={"date": ["2024-01-01", "2024-12-31"]}
).df()
```

### 4.2 多股票查询

```python
stocks = ["000001.SZ", "000002.SZ", "600000.SH"]
inst_str = "','".join(stocks)
df = dai.query("""
    SELECT date, instrument, close, volume
    FROM cn_stock_bar1d
    WHERE date >= '2024-01-01' AND date <= '2024-03-31'
      AND instrument IN ('{}')
    ORDER BY date, instrument
""".format(inst_str)).df()
```

### 4.3 JOIN 查询

```python
df = dai.query("""
    SELECT b.instrument, b.close, b.upper_limit,
           v.pe_ttm, v.pb, v.float_market_cap
    FROM cn_stock_bar1d b
    LEFT JOIN cn_stock_valuation v
      ON b.instrument = v.instrument AND b.date = v.date
    WHERE b.date = '2024-01-02'
      AND v.float_market_cap > 5e9
      AND v.float_market_cap < 30e9
    ORDER BY v.float_market_cap ASC
    LIMIT 30
""").df()
```

### 4.4 常见错误处理

```python
# 错误：表不存在或无权限
# FAIL Invalid Input Error: Attempting to execute an unsuccessful or closed pending query result
# → 该表需要付费或表名错误

# 错误：需要 filters
# FAIL Permission Error: 请在查询表 xxx 时使用 filters 参数
# → 加 filters={"date": ["2024-01-01"]}

# 错误：无访问权限
# FAIL 没有访问 cn_stock_bar1m
# → 该数据需要付费订阅
```

---

## 五、Skill 使用方式

```bash
cd skills/bigquant_strategy

# 基本用法
node run-skill.js --strategy examples/my_strategy.py

# 指定业务名称（推荐，方便在平台上识别）
node run-skill.js --strategy examples/my_strategy.py --name 小市值选股_2023H1

# 完整参数
node run-skill.js \
  --strategy examples/my_strategy.py \
  --name 小市值选股_2023H1 \
  --start-date 2023-01-01 \
  --end-date 2023-06-30 \
  --capital 1000000 \
  --timeout-ms 300000
```

**注意**：
- 每次运行都会创建新的 Task，历史 Task 不会被删除
- 不指定 `--name` 时，自动用文件名 + 时间戳命名
- 结果保存在 `skills/bigquant_strategy/data/bigquant-result-*.json`

---

## 六、结果数据结构

```json
{
  "capturedAt": "2026-04-03T09:30:00.000Z",
  "platform": "bigquant",
  "taskId": "xxx-xxx-xxx",
  "runId": "yyy-yyy-yyy",
  "taskName": "小市值选股_2023H1_20260403_0930",
  "config": {
    "startDate": "2023-01-01",
    "endDate": "2023-06-30",
    "capital": 1000000,
    "benchmark": "000300.XSHG",
    "frequency": "day"
  },
  "success": true,
  "state": "completed",
  "metrics": {
    "totalReturn": 12.5,
    "annualReturn": 25.0,
    "maxDrawdown": -8.3,
    "sharpe": 1.2,
    "winRate": 58.3,
    "tradeCount": 120
  },
  "executions": [{
    "taskId": "...",
    "runId": "...",
    "strategyFile": "examples/my_strategy.py",
    "source": "...",
    "status": "ok",
    "textOutput": "=== 回测结果 ===\n总收益: 12.5%\n...",
    "metrics": { ... },
    "outputs": [],
    "logs": ["2026-04-03 09:30:00 任务运行开始...", "..."]
  }]
}
```

---

## 七、迁移难度速查

| 策略类型 | 难度 | 关键数据 | 备注 |
|---------|------|---------|------|
| 小市值选股 | 低 | cn_stock_valuation.float_market_cap | 单位是元，注意换算 |
| PE/PB 价值选股 | 低 | cn_stock_valuation | 完整支持 |
| 涨停板策略 | 低 | cn_stock_bar1d.upper_limit | 直接内置，无需计算 |
| 首板低开 | 低 | cn_stock_bar1d（upper_limit + open） | 直接可用 |
| 行业轮动 | 中 | cn_stock_industry | 需手动关联 instrument |
| 动量/均线 | 中 | cn_stock_bar1d | 需 SQL 计算 |
| 财务因子 | 中 | cn_stock_balance_sheet | 需 filters |
| 指数增强 | 高 | cn_index_bar1d | 需付费 |
| 分钟级策略 | 高 | cn_stock_bar1m | 需付费 |
| 宏观择时 | 高 | cn_macro_* | 需付费 |
