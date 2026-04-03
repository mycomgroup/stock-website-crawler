# 各平台数据覆盖对比

> 聚焦"数据"维度：各平台提供哪些数据、数据范围、数据种类、有什么缺口
> 更新时间：2026-04-03
> 覆盖平台：JoinQuant / RiceQuant / THSQuant / BigQuant / AKShare / 理杏仁(Lixinger)

---

## 一、数据种类总览

| 数据类型 | JoinQuant | RiceQuant | THSQuant | BigQuant | AKShare | 理杏仁 |
|---------|-----------|-----------|----------|----------|---------|--------|
| **日K线（含复权）** | ✅ | ✅ | ✅ | ✅ | ✅ 东财/新浪/腾讯多源 | ✅ |
| **分钟线** | ✅ | ✅ | ✅ | ❌ 需付费 | ✅ 1/5/15/30/60分钟 | ❌ |
| **Tick/分笔数据** | ✅ | ❌ 回测不可用 | ✅ | ❌ | ✅ 历史分笔+日内分时 | ❌ |
| **实时快照** | ✅ `get_current_data()` | ✅ `bar_dict` | ✅ `get_last_tick()` | ❌ 无实时 | ✅ 多源实时行情 | ✅ 实时估值 |
| **涨跌停价** | ✅ 直接获取 | ✅ `limit_up` 字段 | ✅ 内置 | ✅ `upper_limit` 字段 | ✅ 行情数据内含 | ❌ |
| **集合竞价数据** | ❌ | ❌ | ✅ `get_call_auction()` | ❌ | ✅ 盘前分钟数据 | ❌ |
| **指数K线** | ✅ | ✅ | ✅ | ❌ 需付费 | ✅ | ✅ |
| **指数成分股** | ✅ | ✅ | ✅ | ❌ 需付费 | ✅ | ✅ |
| **指数权重** | ✅ | ✅ | ✅ `get_index_weight()` | ❌ | ✅ | ✅ |
| **ETF 数据** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **期货数据** | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| **期权数据** | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| **估值因子（PE/PB）** | ✅ | ✅ | ✅ | ✅ | ✅ 东财/新浪多源 | ✅ 历史分位点 |
| **财务报表（三大表）** | ✅ | ✅ | ✅ | ✅（需 filters）| ✅ 东财/新浪/同花顺 | ✅ |
| **财务指标（ROE/ROA）** | ✅ | ✅ | ✅ | ❌ 需付费 | ✅ | ✅ |
| **现金流数据** | ✅ | ✅ | ✅ | ✅（资产负债表）| ✅ | ✅ |
| **行业分类** | ✅ 申万/中信 | ✅ 申万 | ✅ 中信 | ✅ 恒生（静态）| ✅ 申万/中信/东财 | ✅ 申万 |
| **概念板块** | ✅ | ❌ | ✅ | ❌ 需付费 | ✅ 东财概念板块完整 | ❌ |
| **融资融券** | ✅ | ❌ | ✅ `get_mtss()` | ❌ 需付费 | ✅ 沪深两市明细 | ❌ |
| **资金流向** | ❌ | ❌ | ✅ `get_money_flow_step()` | ❌ 需付费 | ✅ 个股/行业/大盘 | ❌ |
| **北向/南向资金** | ❌ | ❌ | ❌ | ❌ | ✅ 沪深港通历史+分时 | ❌ |
| **龙虎榜** | ✅ | ❌ | ❌ | ❌ | ✅ 东财+新浪完整 | ❌ |
| **大宗交易** | ✅ | ❌ | ❌ | ❌ | ✅ 每日明细+统计 | ❌ |
| **分红数据** | ✅ | ✅ | ✅ | ✅ `cn_stock_dividend` | ✅ 历史分红完整 | ✅ 股息率历史 |
| **停牌数据** | ✅ | ✅ | ✅ | ✅ `cn_stock_suspend` | ✅ | ❌ |
| **问财自然语言查询** | ✅ | ❌ | ✅ `get_iwencai()` | ❌ | ❌ | ❌ |
| **宏观数据（CPI/PMI）** | ✅ | ❌ | ❌ | ❌ 需付费 | ✅ 独立宏观模块 | ❌ |
| **压力支撑位** | ❌ | ❌ | ✅ `get_resistance_support()` | ❌ | ❌ | ❌ |
| **北交所数据** | ✅ | ⚠️ 部分 | ✅ | ⚠️ 部分 | ✅ | ❌ |
| **港股数据** | ✅ | ❌ | ❌ | ❌ | ✅ 完整港股行情+财务 | ✅ 港股估值 |
| **美股数据** | ❌ | ❌ | ❌ | ❌ | ✅ 完整美股行情+财务 | ✅ 美股估值 |
| **股东/持股数据** | ✅ | ❌ | ❌ | ❌ | ✅ 十大股东/机构持股 | ❌ |
| **限售解禁** | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **股权质押** | ✅ | ❌ | ❌ | ❌ | ✅ 市场概况+明细 | ❌ |
| **新股数据** | ✅ | ❌ | ✅ | ❌ | ✅ 打新收益/中签率 | ❌ |
| **涨停板行情** | ❌ | ❌ | ❌ | ❌ | ✅ 涨停/跌停/炸板池 | ❌ |
| **ESG 评级** | ❌ | ❌ | ❌ | ❌ | ✅ MSCI/路孚特/华证 | ❌ |
| **估值历史分位点** | ❌ | ❌ | ❌ | ❌ | ⚠️ 需自己计算 | ✅ 核心功能 |

---

## 二、数据时间范围

| 数据类型 | JoinQuant | RiceQuant | THSQuant | BigQuant | AKShare | 理杏仁 |
|---------|-----------|-----------|----------|----------|---------|--------|
| **日K线历史起点** | 1990-12-19 | 1990-12-19 | 1990-12-19 | ~2005 | 1990-12-19（新浪源）| ~2005 |
| **分钟线历史起点** | 2005-01-04 | 2005-01-04 | 2005-01-04 | 需付费 | 近期（1分钟近5日）| ❌ |
| **财务数据起点** | 1990 年报 | 1990 年报 | 1990 年报 | ~2010 | 1990 年报 | ~2010 |
| **数据更新频率** | T+1 | T+1 | T+1 | T+1 | T+1（实时行情除外）| T+1 |
| **实时数据** | ✅ 盘中可用 | ✅ 盘中可用 | ✅ 盘中可用 | ❌ 无 | ✅ 盘中可用 | ✅ 盘中可用 |

---

## 三、股票代码格式

| 平台 | 沪市格式 | 深市格式 | 示例 |
|------|---------|---------|------|
| JoinQuant | `.XSHG` | `.XSHE` | `000001.XSHE` / `600000.XSHG` |
| RiceQuant | `.XSHG` | `.XSHE` | `000001.XSHE` / `600000.XSHG` |
| THSQuant | `.SH` | `.SZ` | `000001.SZ` / `600000.SH` |
| BigQuant | `.SH` | `.SZ` | `000001.SZ` / `600000.SH` |
| AKShare | 无后缀（东财源）| 无后缀 | `000001` / `600000` |
| 理杏仁 | `.SH` | `.SZ` | `000001.SZ` / `600000.SH` |

AKShare 代码格式随数据源变化：新浪源用 `sz000001`，东财源用纯数字 `000001`，雪球源用 `SZ000001`。

---

## 四、AKShare 核心接口速查

AKShare 是纯 Python 库，免费开源，无需账号，直接 `pip install akshare` 使用。数据来自东财、新浪、同花顺等多个公开源。

### 4.1 行情数据

```python
import akshare as ak

# 日K线（推荐，东财源，质量高）
df = ak.stock_zh_a_hist(symbol="000001", period="daily",
                        start_date="20200101", end_date="20241231",
                        adjust="qfq")  # qfq前复权 hfq后复权

# 全市场实时行情（沪深京A股）
df = ak.stock_zh_a_spot_em()

# 分钟线（5分钟，近期数据）
df = ak.stock_zh_a_hist_min_em(symbol="000001", period="5",
                               start_date="2024-01-01 09:30:00",
                               end_date="2024-01-31 15:00:00",
                               adjust="qfq")

# 涨停板行情
df = ak.stock_zt_pool_em(date="20241008")       # 涨停股池
df = ak.stock_zt_pool_dtgc_em(date="20241008")  # 跌停股池
df = ak.stock_zt_pool_zbgc_em(date="20241008")  # 炸板股池
```

### 4.2 财务数据

```python
# 资产负债表（全市场，按季度）
df = ak.stock_zcfz_em(date="20240331")

# 利润表
df = ak.stock_lrb_em(date="20240331")

# 现金流量表
df = ak.stock_xjll_em(date="20240331")

# 个股财务指标（东财，按报告期）
df = ak.stock_financial_analysis_indicator_em(symbol="000001.SZ", indicator="按报告期")

# 业绩报表（全市场）
df = ak.stock_yjbb_em(date="20240331")
```

### 4.3 估值数据

```python
# 全市场估值（东财，含PE/PB/市值）
df = ak.stock_zh_a_spot_em()  # 字段含 市盈率-动态, 市净率, 总市值, 流通市值

# 个股历史估值（百度股市通）
df = ak.stock_zh_valuation_baidu(symbol="000001", indicator="市盈率(TTM)", period="近五年")

# A股等权重/中位数市盈率（乐咕乐股）
df = ak.stock_a_ttm_lyr()

# 指数市盈率历史（乐咕乐股）
df = ak.stock_index_pe_lg(symbol="沪深300")

# 巴菲特指标
df = ak.stock_buffett_index_lg()
```

### 4.4 资金流向

```python
# 个股资金流（东财，近100日）
df = ak.stock_individual_fund_flow(stock="000001", market="sz")

# 大盘资金流
df = ak.stock_market_fund_flow()

# 行业资金流排名
df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")

# 北向资金历史
df = ak.stock_hsgt_hist_em(symbol="北向资金")

# 北向资金分时
df = ak.stock_hsgt_fund_min_em(symbol="北向资金")
```

### 4.5 AKShare 独有数据（其他平台没有）

| 数据 | 接口 | 说明 |
|------|------|------|
| 涨停板行情池 | `stock_zt_pool_em` | 涨停/跌停/炸板/强势股池 |
| 北向资金分时 | `stock_hsgt_fund_min_em` | 每分钟北向资金流入 |
| 龙虎榜完整数据 | `stock_lhb_detail_em` | 含营业部买卖明细 |
| 大宗交易明细 | `stock_dzjy_mrmx` | 每日大宗交易 |
| ESG 评级 | `stock_esg_rate_sina` | MSCI/路孚特/华证多机构 |
| 股权质押明细 | `stock_gpzy_pledge_ratio_detail_em` | 含预估平仓线 |
| 限售解禁详情 | `stock_restricted_release_detail_em` | 含解禁后涨跌幅 |
| 打新收益率 | `stock_dxsyl_em` | 历史打新收益统计 |
| 机构调研 | `stock_jgdy_tj_em` | 机构调研统计 |
| 股票热度 | `stock_hot_rank_em` | 东财/雪球人气榜 |
| 盘口异动 | `stock_changes_em` | 大笔买入/封涨停等 |
| 宏观数据 | `macro_china_*` 系列 | CPI/PPI/PMI/GDP等 |
| 美股完整行情 | `stock_us_hist` | 历史+实时+财务 |
| 港股完整行情 | `stock_hk_hist` | 历史+实时+财务 |

---

## 五、理杏仁(Lixinger) 核心能力

理杏仁是专注估值分析的平台，通过 `skills/lixinger-screener` 接入。

### 5.1 核心优势

| 能力 | 说明 |
|------|------|
| **估值历史分位点** | PE/PB/PS/PCF 的 3/5/10年历史分位点，直接可用 |
| **股息率历史** | 历史股息率走势 |
| **多维度筛选** | 支持按估值分位点、财务指标组合筛选 |
| **A/H/美股** | 同时覆盖三个市场的估值数据 |
| **指数估值** | 沪深300/中证500等指数的历史估值 |

### 5.2 使用方式

```bash
# 低估值高股息筛选
node skills/lixinger-screener/run-skill.js \
  --query "PE-TTM(扣非)统计值10年分位点小于30%，股息率大于2%"

# 使用配置文件
node skills/lixinger-screener/run-skill.js \
  --input-file skills/lixinger-screener/low-val-dividend-dip.json
```

### 5.3 理杏仁 vs AKShare 估值数据对比

| 特性 | 理杏仁 | AKShare |
|------|--------|---------|
| 历史分位点 | ✅ 直接提供 3/5/10年 | ❌ 需自己计算 |
| 实时估值 | ✅ | ✅ |
| 历史估值走势 | ✅ | ✅（百度股市通源）|
| 筛选功能 | ✅ 多条件组合 | ❌ 需自己写代码 |
| 港股估值 | ✅ | ✅ |
| 美股估值 | ✅ | ✅ |
| 免费使用 | ⚠️ 需账号，有限制 | ✅ 完全免费 |

---

## 六、各平台数据获取 API 横向对比

### 6.1 日K线数据

| 平台 | API | 返回格式 | 批量支持 | 复权方式 |
|------|-----|---------|---------|---------|
| JoinQuant | `get_price(stocks, end_date, count, fields)` | DataFrame | ✅ 一次多只 | `fq='pre'` 前复权 |
| RiceQuant | `history_bars(stock, count, '1d', fields)` | numpy 结构化数组 | ❌ 需循环 | 默认前复权 |
| THSQuant | `history(stocks, fields, count, '1d', fq='pre')` | DataFrame | ✅ 一次多只 | `fq='pre'/'post'/None` |
| BigQuant | `dai.query("SELECT ... FROM cn_stock_bar1d ...")` | DataFrame | ✅ SQL IN 子句 | 已内置前复权 |
| AKShare | `ak.stock_zh_a_hist(symbol, period, start_date, end_date, adjust)` | DataFrame | ❌ 单只 | `qfq`/`hfq`/`""` |

### 6.2 涨跌停价

| 平台 | 获取方式 | 是否直接 | 注意事项 |
|------|---------|---------|---------|
| JoinQuant | `get_current_data()[stock].high_limit` | ✅ 直接 | 仅盘中可用，历史需 `get_price(fields=['high_limit'])` |
| RiceQuant | `history_bars(stock, 1, '1d', 'limit_up')[-1]` | ✅ 直接 | 字段名 `limit_up` |
| THSQuant | 内置于 bar 数据 | ✅ 直接 | 无需额外查询 |
| BigQuant | `cn_stock_bar1d.upper_limit` | ✅ 直接 | SQL 字段，最方便 |
| AKShare | `stock_zh_a_spot_em()` 含涨停/跌停字段 | ✅ 直接 | 实时行情含涨停价 |

### 6.3 估值数据（PE/PB/市值）

| 平台 | API | PE 字段名 | PB 字段名 | 市值字段名 | 市值单位 |
|------|-----|---------|---------|---------|---------|
| JoinQuant | `get_fundamentals(query(valuation.*))` | `pe_ratio` | `pb_ratio` | `market_cap` | **亿元** |
| RiceQuant | `get_fundamentals(query(fundamentals.eod_derivative_indicator.*))` | `pe_ratio` | `pb_ratio` | `market_cap` | 元 |
| THSQuant | `get_fundamentals(query(valuation.*))` | `pe_ratio` | `pb_ratio` | `market_cap` | 元 |
| BigQuant | `dai.query("SELECT ... FROM cn_stock_valuation")` | `pe_ttm` | `pb` | `total_market_cap` | 元 |
| AKShare | `stock_zh_a_spot_em()` | `市盈率-动态` | `市净率` | `总市值` | 元 |
| 理杏仁 | `lixinger-screener` skill | `pe_ttm` | `pb` | `market_cap` | 元 |

### 6.4 行业分类

| 平台 | 支持标准 | API | 历史行业支持 |
|------|---------|-----|------------|
| JoinQuant | 申万一/二/三级、中信 | `get_industry(stocks, date)` | ✅ |
| RiceQuant | 申万一/二级 | `instruments(stock).shenwan_industry_name` | ⚠️ 当前 |
| THSQuant | 中信一/二/三级 | `get_symbol_industry(stock, date)` | ✅ |
| BigQuant | 恒生（静态，无日期）| `cn_stock_industry` 表 | ❌ |
| AKShare | 申万/中信/东财行业 | `stock_board_industry_name_em()` | ⚠️ 当前 |

---

## 七、各平台独有数据

### JoinQuant 独有

| 数据 | API | 用途 |
|------|-----|------|
| 港股数据 | `get_price('00700.HKG', ...)` | 港股策略 |
| 宏观数据 | `macro.MAC_AREA_RESIDENT_PRICE_INDEX` | 宏观择时 |
| 问财查询 | `get_iwencai(query)` | 自然语言选股 |
| jqfactor 因子库 | `jqfactor.get_factor_values(...)` | 专业因子研究 |
| 龙虎榜数据 | `get_billboard_list(date)` | 游资策略 |

### THSQuant 独有

| 数据 | API | 用途 |
|------|-----|------|
| 资金流向 | `get_money_flow_step(stocks, ...)` | 主力资金监控 |
| 压力支撑位 | `get_resistance_support(stocks, ...)` | 技术分析 |
| 集合竞价 | `get_call_auction(symbol, dt)` | 开盘策略 |
| 涨跌区间统计 | `get_stats(date)` | 市场情绪 |

### BigQuant 独有

| 数据 | 表名 | 用途 |
|------|------|------|
| 分红数据（结构化）| `cn_stock_dividend` | 股息策略 |
| 停牌数据（结构化）| `cn_stock_suspend` | 风控 |
| SQL 灵活查询 | DAI 接口 | 复杂数据处理 |

### AKShare 独有

| 数据 | 接口 | 用途 |
|------|------|------|
| 涨停板行情池 | `stock_zt_pool_em` | 涨停策略研究 |
| 北向资金分时 | `stock_hsgt_fund_min_em` | 北向资金监控 |
| 龙虎榜完整 | `stock_lhb_detail_em` | 游资行为分析 |
| 大宗交易明细 | `stock_dzjy_mrmx` | 机构动向 |
| ESG 评级 | `stock_esg_rate_sina` | ESG 因子 |
| 股权质押明细 | `stock_gpzy_pledge_ratio_detail_em` | 风险监控 |
| 打新收益率 | `stock_dxsyl_em` | 打新策略 |
| 宏观数据 | `macro_china_*` 系列 | 宏观择时 |
| 美股完整数据 | `stock_us_hist` | 美股策略 |
| 股票热度 | `stock_hot_rank_em` | 情绪因子 |
| 盘口异动 | `stock_changes_em` | 实时监控 |

### 理杏仁独有

| 数据 | 说明 | 用途 |
|------|------|------|
| 估值历史分位点 | PE/PB 的 3/5/10年分位点 | 价值投资核心指标 |
| 多维度估值筛选 | 组合条件筛选 | 快速选股 |

---

## 八、免费账户数据限制

| 平台 | 主要限制 | 影响策略类型 |
|------|---------|------------|
| JoinQuant | 每日回测时间 180 分钟 | 长期回测、参数扫描 |
| RiceQuant | 每日回测时间 180 分钟；无 Tick 数据 | 高频策略 |
| THSQuant | 每日回测时间限制 | 长期回测 |
| BigQuant | 无分钟线、无指数K线、无财务指标表、无成分股 | 指数增强、分钟策略 |
| AKShare | **无限制**，完全免费 | 无 |
| 理杏仁 | 需账号，免费版有查询次数限制 | 高频筛选 |

---

## 九、策略类型 × 平台数据可行性

| 策略类型 | JQ | RQ | THS | BQ | AKShare | 理杏仁 | 推荐 |
|---------|----|----|-----|----|---------|--------|------|
| 小市值选股 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 任意 |
| PE/PB 价值选股 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 分位点 | 理杏仁+JQ |
| 多因子（ROE/ROA/成长）| ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | JQ/RQ/THS |
| 涨停板策略 | ✅ | ✅ | ✅ | ✅ | ✅ 涨停池 | ❌ | AKShare+JQ |
| 首板低开策略 | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | 任意 |
| 指数增强 | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | JQ/RQ/THS |
| 行业轮动 | ✅ 申万 | ✅ 申万 | ✅ 中信 | ⚠️ 恒生 | ✅ | ✅ | JQ/RQ |
| 动量/均线 | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | 任意 |
| 技术指标（MACD/RSI）| ✅ jqfactor | ⚠️ 手动 | ✅ | ⚠️ 手动 | ⚠️ 手动 | ❌ | JQ/THS |
| 融资融券策略 | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | JQ/THS/AKShare |
| 资金流向策略 | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | THS/AKShare |
| 北向资金策略 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | AKShare 独有 |
| 宏观择时 | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | JQ/AKShare |
| 港股策略 | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | JQ/AKShare |
| 分钟级策略 | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | JQ/RQ/THS |
| 打新策略 | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | AKShare |
| ESG 因子 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | AKShare 独有 |

---

## 十、数据质量已知差异

### 10.1 复权方式

四个回测平台默认都是前复权，AKShare 需显式指定 `adjust="qfq"`。

### 10.2 市值单位差异（重要）

```python
# JoinQuant：市值单位是亿元
market_cap_jq = 50  # 表示 50 亿元

# RiceQuant / THSQuant / BigQuant / AKShare：市值单位是元
market_cap = 5_000_000_000  # 表示 50 亿元

# 换算
market_cap_yuan = market_cap_jq * 1e8
```

### 10.3 PE/PB 计算口径

| 平台 | PE 口径 | 说明 |
|------|---------|------|
| JoinQuant | TTM | 滚动12个月 |
| RiceQuant | TTM | 滚动12个月 |
| THSQuant | TTM | 滚动12个月 |
| BigQuant | `pe_ttm` / `pe_leading` / `pe_trailing` | 提供多种口径 |
| AKShare | 动态市盈率（东财源）| 近似 TTM |
| 理杏仁 | TTM（扣非）| 扣除非经常性损益 |

### 10.4 AKShare 数据源稳定性

AKShare 依赖第三方网站，部分接口可能因网站改版失效。稳定性排序：
- 高稳定：东财系列（`_em` 后缀）
- 中稳定：同花顺系列（`_ths` 后缀）
- 低稳定：新浪系列（`_sina` 后缀，容易封 IP）

---

## 十一、数据缺口汇总与应对

| 缺口 | 受影响平台 | 应对方案 |
|------|----------|---------|
| 无宏观数据 | RQ / THS / BQ | 用 AKShare `macro_china_*` 或 JQ 获取 |
| 无指数成分股（免费）| BQ | 用 JQ/RQ/THS 或 AKShare 获取 |
| 无财务指标（免费）| BQ | 用 AKShare `stock_zcfz_em` 等接口 |
| 无融资融券 | RQ / BQ | 用 AKShare `stock_margin_detail_sse` |
| 无资金流向 | JQ / RQ / BQ | 用 AKShare `stock_individual_fund_flow` |
| 无北向资金 | JQ / RQ / THS / BQ | 用 AKShare `stock_hsgt_hist_em` |
| 无 Tick 数据 | RQ / BQ | 用 AKShare `stock_zh_a_tick_tx_js` |
| 无港股 | RQ / THS / BQ | 用 JQ 或 AKShare `stock_hk_hist` |
| 无估值分位点 | 所有回测平台 | 用理杏仁 screener skill |
| 无涨停板行情池 | 所有回测平台 | 用 AKShare `stock_zt_pool_em` |

---

## 十二、平台选择决策树（数据维度）

```
需要什么数据？
│
├── 估值历史分位点（PE/PB 几年低位）→ 理杏仁 screener
│
├── 宏观数据（CPI/PMI/GDP）→ AKShare 或 JoinQuant
│
├── 港股数据 → JoinQuant 或 AKShare
│
├── 美股数据 → AKShare
│
├── 资金流向 → AKShare 或 THSQuant
│
├── 北向资金 → AKShare
│
├── 融资融券 → AKShare / JoinQuant / THSQuant
│
├── 涨停板行情池 → AKShare（唯一免费来源）
│
├── 指数成分股（免费）→ JoinQuant / RiceQuant / THSQuant / AKShare
│
├── 财务指标（ROE/ROA/毛利率）
│   ├── 免费 → JoinQuant / RiceQuant / THSQuant / AKShare
│   └── 付费 → BigQuant 也可以
│
├── 日K线 + 估值（PE/PB/市值）→ 六个平台都支持
│
└── 需要 SQL 灵活查询 → BigQuant（DAI 接口）
```

---

## 十三、相关文档

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
