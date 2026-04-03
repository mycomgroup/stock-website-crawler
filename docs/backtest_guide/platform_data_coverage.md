# 各平台数据覆盖对比

> 聚焦"数据"维度：各平台提供哪些数据、数据范围、数据种类、有什么缺口
> 更新时间：2026-04-03
> 覆盖平台：JoinQuant / RiceQuant / THSQuant / BigQuant

---

## 一、数据种类总览

| 数据类型 | JoinQuant | RiceQuant | THSQuant | BigQuant |
|---------|-----------|-----------|----------|----------|
| **日K线（含复权）** | ✅ | ✅ | ✅ | ✅ |
| **分钟线** | ✅ | ✅ | ✅ | ❌ 需付费 |
| **Tick 数据** | ✅ | ❌ 回测不可用 | ✅ | ❌ |
| **实时快照** | ✅ `get_current_data()` | ✅ `bar_dict` | ✅ `get_last_tick()` | ❌ 无实时 |
| **涨跌停价** | ✅ 直接获取 | ✅ `limit_up` 字段 | ✅ 内置 | ✅ `upper_limit` 字段 |
| **集合竞价数据** | ❌ | ❌ | ✅ `get_call_auction()` | ❌ |
| **指数K线** | ✅ | ✅ | ✅ | ❌ 需付费 |
| **指数成分股** | ✅ | ✅ | ✅ | ❌ 需付费 |
| **指数权重** | ✅ | ✅ | ✅ `get_index_weight()` | ❌ |
| **ETF 数据** | ✅ | ✅ | ✅ | ❌ |
| **期货数据** | ✅ | ✅ | ✅ | ❌ |
| **期权数据** | ✅ | ✅ | ✅ | ❌ |
| **估值因子（PE/PB）** | ✅ | ✅ | ✅ | ✅ |
| **财务报表** | ✅ | ✅ | ✅ | ✅（需 filters）|
| **财务指标（ROE/ROA）** | ✅ | ✅ | ✅ | ❌ 需付费 |
| **现金流数据** | ✅ | ✅ | ✅ | ✅（资产负债表）|
| **行业分类** | ✅ 申万/中信 | ✅ 申万 | ✅ 中信 | ✅ 恒生（静态）|
| **概念板块** | ✅ | ❌ | ✅ | ❌ 需付费 |
| **融资融券** | ✅ | ❌ | ✅ `get_mtss()` | ❌ 需付费 |
| **资金流向** | ❌ | ❌ | ✅ `get_money_flow_step()` | ❌ 需付费 |
| **分红数据** | ✅ | ✅ | ✅ | ✅ `cn_stock_dividend` |
| **停牌数据** | ✅ | ✅ | ✅ | ✅ `cn_stock_suspend` |
| **问财自然语言查询** | ✅ | ❌ | ✅ `get_iwencai()` | ❌ |
| **宏观数据（CPI/PMI）** | ✅ | ❌ | ❌ | ❌ 需付费 |
| **压力支撑位** | ❌ | ❌ | ✅ `get_resistance_support()` | ❌ |
| **北交所数据** | ✅ | ⚠️ 部分 | ✅ | ⚠️ 部分 |
| **港股数据** | ✅ | ❌ | ❌ | ❌ |

---

## 二、数据时间范围

| 数据类型 | JoinQuant | RiceQuant | THSQuant | BigQuant |
|---------|-----------|-----------|----------|----------|
| **日K线历史起点** | 1990-12-19 | 1990-12-19 | 1990-12-19 | ~2005 |
| **分钟线历史起点** | 2005-01-04 | 2005-01-04 | 2005-01-04 | 需付费 |
| **财务数据起点** | 1990 年报 | 1990 年报 | 1990 年报 | ~2010 |
| **数据更新频率** | T+1 | T+1 | T+1 | T+1 |
| **实时数据** | ✅ 盘中可用 | ✅ 盘中可用 | ✅ 盘中可用 | ❌ 无 |

---

## 三、股票代码格式

| 平台 | 沪市格式 | 深市格式 | 示例 |
|------|---------|---------|------|
| JoinQuant | `.XSHG` | `.XSHE` | `000001.XSHE` / `600000.XSHG` |
| RiceQuant | `.XSHG` | `.XSHE` | `000001.XSHE` / `600000.XSHG` |
| THSQuant | `.SH` | `.SZ` | `000001.SZ` / `600000.SH` |
| BigQuant | `.SH` | `.SZ` | `000001.SZ` / `600000.SH` |

**迁移注意**：JQ/RQ 用 `.XSHG/.XSHE`，THS/BQ 用 `.SH/.SZ`，跨平台时必须转换。

```python
# JQ/RQ → THS/BQ 代码转换
def convert_code(code, to_platform='ths'):
    if to_platform in ('ths', 'bq'):
        return code.replace('.XSHG', '.SH').replace('.XSHE', '.SZ')
    else:
        return code.replace('.SH', '.XSHG').replace('.SZ', '.XSHE')
```

---

## 四、各平台数据获取 API 横向对比

### 4.1 日K线数据

| 平台 | API | 返回格式 | 批量支持 | 复权方式 |
|------|-----|---------|---------|---------|
| JoinQuant | `get_price(stocks, end_date, count, fields)` | DataFrame | ✅ 一次多只 | `fq='pre'` 前复权 |
| RiceQuant | `history_bars(stock, count, '1d', fields)` | numpy 结构化数组 | ❌ 需循环 | 默认前复权 |
| THSQuant | `history(stocks, fields, count, '1d', fq='pre')` | DataFrame | ✅ 一次多只 | `fq='pre'/'post'/None` |
| BigQuant | `dai.query("SELECT ... FROM cn_stock_bar1d ...")` | DataFrame | ✅ SQL IN 子句 | 已内置前复权 |

**关键差异**：
- RiceQuant 不支持批量获取，对全市场扫描性能影响大
- BigQuant 用 SQL，灵活但需要手写查询
- THSQuant 和 JoinQuant API 最相似，迁移成本最低

### 4.2 涨跌停价

| 平台 | 获取方式 | 是否直接 | 注意事项 |
|------|---------|---------|---------|
| JoinQuant | `get_current_data()[stock].high_limit` | ✅ 直接 | 仅盘中可用，历史需计算 |
| JoinQuant（历史） | `get_price(stock, fields=['high_limit'])` | ✅ 直接 | 历史数据可用 |
| RiceQuant | `history_bars(stock, 1, '1d', 'limit_up')[-1]` | ✅ 直接 | 字段名 `limit_up` |
| THSQuant | 内置于 bar 数据 | ✅ 直接 | 无需额外查询 |
| BigQuant | `cn_stock_bar1d.upper_limit` | ✅ 直接 | SQL 字段，最方便 |

**结论**：四个平台都能直接获取涨跌停价，无需手动计算。

### 4.3 估值数据（PE/PB/市值）

| 平台 | API | PE 字段名 | PB 字段名 | 市值字段名 |
|------|-----|---------|---------|---------|
| JoinQuant | `get_fundamentals(query(valuation.*))` | `pe_ratio` | `pb_ratio` | `market_cap`（亿元）|
| RiceQuant | `get_fundamentals(query(fundamentals.eod_derivative_indicator.*))` | `pe_ratio` | `pb_ratio` | `market_cap`（元）|
| THSQuant | `get_fundamentals(query(valuation.*))` | `pe_ratio` | `pb_ratio` | `market_cap`（元）|
| BigQuant | `dai.query("SELECT ... FROM cn_stock_valuation")` | `pe_ttm` | `pb` | `total_market_cap`（元）|

**关键差异**：
- JoinQuant 市值单位是**亿元**，其他平台是**元**，换算时注意 `× 1e8`
- BigQuant 的 PE 字段名是 `pe_ttm`，不是 `pe_ratio`
- BigQuant 的 PB 字段名是 `pb`，不是 `pb_ratio`

### 4.4 财务指标（ROE/ROA/毛利率）

| 平台 | API | ROE | ROA | 毛利率 | 净利润增长 |
|------|-----|-----|-----|-------|---------|
| JoinQuant | `get_fundamentals(query(indicator.*))` | `roe` | `roa` | `gross_profit_margin` | `net_profit_growth_rate` |
| RiceQuant | `get_fundamentals(query(fundamentals.financial_indicator.*))` | `roe` | `roa` | `gross_profit_margin` | `inc_net_profit_year` |
| THSQuant | `get_fundamentals(query(profit.*))` | `roe` | `roa` | `gross_profit_margin` | — |
| BigQuant | `cn_stock_financial_indicator`（需付费）| — | — | — | — |

**BigQuant 缺口**：财务指标表需付费，免费账户只有资产负债表（`cn_stock_balance_sheet`）。

### 4.5 行业分类

| 平台 | 支持标准 | API | 返回格式 |
|------|---------|-----|---------|
| JoinQuant | 申万一/二/三级、中信 | `get_industry(stocks, date)` | dict |
| RiceQuant | 申万一/二级 | `instruments(stock).shenwan_industry_name` | 字符串 |
| THSQuant | 中信一/二/三级 | `get_symbol_industry(stock, date)` | dict |
| BigQuant | 恒生（静态，无日期） | `cn_stock_industry` 表 | DataFrame |

**关键差异**：
- 各平台行业标准不同（申万 vs 中信 vs 恒生），同一只股票分类可能不同
- BigQuant 行业表是静态的，不支持历史某日的行业分类
- 跨平台对比行业轮动策略时，需注意行业标准统一

### 4.6 指数成分股

| 平台 | API | 指数代码格式 | 历史成分支持 |
|------|-----|------------|------------|
| JoinQuant | `get_index_stocks('000300.XSHG', date)` | `.XSHG` | ✅ |
| RiceQuant | `index_components('000300.XSHG')` | `.XSHG` | ⚠️ 默认当前 |
| THSQuant | `get_index_stocks('000300.SH', date)` | `.SH` | ✅ |
| BigQuant | `cn_index_components`（需付费）| `.SH` | ❌ 需付费 |

**BigQuant 缺口**：指数成分股需付费，免费账户无法做指数增强策略。

---

## 五、各平台独有数据（其他平台没有）

### JoinQuant 独有

| 数据 | API | 用途 |
|------|-----|------|
| 港股数据 | `get_price('00700.HKG', ...)` | 港股策略 |
| 宏观数据 | `macro.MAC_AREA_RESIDENT_PRICE_INDEX` | 宏观择时 |
| 问财查询 | `get_iwencai(query)` | 自然语言选股 |
| jqfactor 因子库 | `jqfactor.get_factor_values(...)` | 专业因子研究 |
| 龙虎榜数据 | `get_billboard_list(date)` | 游资策略 |
| 大宗交易 | `get_bulk_trade_detail(date)` | 机构动向 |

### THSQuant 独有

| 数据 | API | 用途 |
|------|-----|------|
| 资金流向 | `get_money_flow_step(stocks, ...)` | 主力资金监控 |
| 压力支撑位 | `get_resistance_support(stocks, ...)` | 技术分析 |
| 集合竞价 | `get_call_auction(symbol, dt)` | 开盘策略 |
| 问财查询 | `get_iwencai(query)` | 自然语言选股 |
| 涨跌区间统计 | `get_stats(date)` | 市场情绪 |

### BigQuant 独有

| 数据 | 表名 | 用途 |
|------|------|------|
| 分红数据（结构化）| `cn_stock_dividend` | 股息策略 |
| 停牌数据（结构化）| `cn_stock_suspend` | 风控 |
| SQL 灵活查询 | DAI 接口 | 复杂数据处理 |

---

## 六、免费账户数据限制

| 平台 | 主要限制 | 影响策略类型 |
|------|---------|------------|
| JoinQuant | 每日回测时间 180 分钟 | 长期回测、参数扫描 |
| RiceQuant | 每日回测时间 180 分钟；无 Tick 数据 | 高频策略 |
| THSQuant | 每日回测时间限制（具体未知）| 长期回测 |
| BigQuant | 无分钟线、无指数K线、无财务指标表、无成分股 | 指数增强、分钟策略 |

---

## 七、策略类型 × 平台数据可行性

| 策略类型 | JoinQuant | RiceQuant | THSQuant | BigQuant | 推荐平台 |
|---------|-----------|-----------|----------|----------|---------|
| 小市值选股 | ✅ | ✅ | ✅ | ✅ | 任意 |
| PE/PB 价值选股 | ✅ | ✅ | ✅ | ✅ | 任意 |
| 多因子（ROE/ROA/成长）| ✅ | ✅ | ✅ | ❌ 需付费 | JQ/RQ/THS |
| 涨停板策略 | ✅ | ✅ | ✅ | ✅ | 任意 |
| 首板低开策略 | ✅ | ✅ | ✅ | ✅ | 任意 |
| 指数增强 | ✅ | ✅ | ✅ | ❌ 需付费 | JQ/RQ/THS |
| 行业轮动 | ✅ 申万 | ✅ 申万 | ✅ 中信 | ⚠️ 恒生静态 | JQ/RQ |
| 动量/均线 | ✅ | ✅ | ✅ | ✅ | 任意 |
| 技术指标（MACD/RSI）| ✅ jqfactor | ⚠️ 手动计算 | ✅ | ⚠️ 手动计算 | JQ/THS |
| 融资融券策略 | ✅ | ❌ | ✅ | ❌ | JQ/THS |
| 资金流向策略 | ❌ | ❌ | ✅ | ❌ | THS 独有 |
| 宏观择时 | ✅ | ❌ | ❌ | ❌ 需付费 | JQ 独有 |
| 港股策略 | ✅ | ❌ | ❌ | ❌ | JQ 独有 |
| 分钟级策略 | ✅ | ✅ | ✅ | ❌ 需付费 | JQ/RQ/THS |
| 问财自然语言选股 | ✅ | ❌ | ✅ | ❌ | JQ/THS |

---

## 八、数据质量已知差异

以下是实测中发现的跨平台数据差异，使用时需注意：

### 8.1 复权方式

| 平台 | 默认复权 | 说明 |
|------|---------|------|
| JoinQuant | 前复权 | `fq='pre'` |
| RiceQuant | 前复权 | 默认 |
| THSQuant | 前复权 | `fq='pre'` |
| BigQuant | 前复权 | `adjust_factor` 已乘入 |

四个平台默认都是前复权，但复权基准日可能不同，导致历史价格有细微差异。

### 8.2 财务数据更新时机

| 平台 | 财务数据更新 | 说明 |
|------|------------|------|
| JoinQuant | 公告日 | 使用 `statDate` 参数 |
| RiceQuant | 公告日 | 使用 `entry_date` 参数 |
| THSQuant | 公告日 | 使用 `date` 参数 |
| BigQuant | 公告日 | 使用 `filters` 日期范围 |

财务数据的"日期"含义各平台一致（公告日），但字段名不同，注意区分。

### 8.3 市值单位差异（重要）

```python
# JoinQuant：市值单位是亿元
market_cap_jq = 50  # 表示 50 亿元

# RiceQuant / THSQuant / BigQuant：市值单位是元
market_cap_rq = 5_000_000_000  # 表示 50 亿元

# 换算
market_cap_yuan = market_cap_jq * 1e8
market_cap_yi = market_cap_rq / 1e8
```

### 8.4 PE/PB 计算口径

| 平台 | PE 口径 | 说明 |
|------|---------|------|
| JoinQuant | TTM | 滚动12个月 |
| RiceQuant | TTM | 滚动12个月 |
| THSQuant | TTM | 滚动12个月 |
| BigQuant | `pe_ttm` / `pe_leading` / `pe_trailing` | 提供多种口径 |

BigQuant 提供了最丰富的 PE 口径，其他平台默认 TTM。

---

## 九、数据缺口汇总与应对

### 9.1 各平台缺口

| 缺口 | 受影响平台 | 应对方案 |
|------|----------|---------|
| 无宏观数据 | RQ / THS / BQ | 用 JoinQuant 获取宏观数据，导出后在其他平台使用 |
| 无指数成分股（免费）| BQ | 用 JoinQuant/RiceQuant 获取成分股列表，硬编码到 BQ 策略 |
| 无财务指标（免费）| BQ | 用 `cn_stock_balance_sheet` 手动计算 ROE/ROA |
| 无融资融券 | RQ / BQ | 用 JoinQuant/THSQuant 获取，或跳过该因子 |
| 无资金流向 | JQ / RQ / BQ | 仅 THSQuant 支持，或用换手率替代 |
| 无 Tick 数据 | RQ / BQ | 用分钟线替代，或仅在 JQ/THS 做高频策略 |
| 无港股 | RQ / THS / BQ | 仅 JoinQuant 支持 |

### 9.2 BigQuant 免费账户手动计算财务指标

```python
import dai

# 用资产负债表手动计算 ROE
def calc_roe(instrument, date):
    df = dai.query(
        """SELECT total_owner_equity, net_profit
           FROM cn_stock_balance_sheet
           WHERE instrument = '{inst}'""".format(inst=instrument),
        filters={"date": [date]}
    ).df()
    if df.empty or df["total_owner_equity"].iloc[0] == 0:
        return None
    return df["net_profit"].iloc[0] / df["total_owner_equity"].iloc[0]
```

---

## 十、平台选择决策树（数据维度）

```
需要什么数据？
│
├── 宏观数据（CPI/PMI/GDP）→ 只能用 JoinQuant
│
├── 港股数据 → 只能用 JoinQuant
│
├── 资金流向 → 只能用 THSQuant
│
├── 融资融券 → JoinQuant 或 THSQuant
│
├── 指数成分股（免费）→ JoinQuant / RiceQuant / THSQuant
│
├── 财务指标（ROE/ROA/毛利率）
│   ├── 免费 → JoinQuant / RiceQuant / THSQuant
│   └── 付费 → BigQuant 也可以
│
├── 涨跌停价 → 四个平台都支持
│
├── 日K线 + 估值（PE/PB/市值）→ 四个平台都支持
│
└── 需要 SQL 灵活查询 → BigQuant（DAI 接口）
```

---

## 十一、相关文档

| 文档 | 内容 |
|------|------|
| `API_DIFF.md` | JoinQuant vs RiceQuant API 函数对照 |
| `joinquant_to_ricequant_migration_guide.md` | JQ→RQ 完整迁移指南 |
| `bigquant_api_reference.md` | BigQuant DAI 数据表完整参考 |
| `bigquant_migration_guide.md` | BigQuant 迁移指南 |
| `thsquant_api_guide.md` | THSQuant API 完整指南 |
| `ricequant_factor_list.md` | RiceQuant 因子列表速查 |
| `ricequant_factors_guide.md` | RiceQuant 因子使用指南 |

---

*最后更新：2026-04-03*
