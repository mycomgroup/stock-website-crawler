# Eulerpool Financial Data API Skill

## 概述

Eulerpool Financial Data API 提供对全球 100,000+ 证券的机构级金融数据访问，覆盖 90+ 交易所。API 包含 180+ 端点，涵盖股票、ETF、期权、债券、加密货币、外汇、大宗商品、结构性产品、分析师研究、收益、情绪和另类数据。

**API Base URL:** `https://api.eulerpool.com/api/1`
**官方文档:** https://eulerpool.com/developers/
**定价页面:** https://eulerpool.com/financial-data-api/pricing

### 数据覆盖情况

| 数据类别 | 接口数量 | 说明 |
|---------|---------|------|
| 股票基础数据 (Equity) | ~50 | 公司概况、财务报表、估值、行情等 |
| 股票扩展数据 (Equity Extended) | ~18 | 高级财务指标、技术指标、SEC文件等 |
| 市场数据 (Market) | ~14 | 实时报价、期权链、市场指标等 |
| ETF 数据 | ~7 | ETF持仓、行业/国家分布等 |
| 加密货币 (Crypto) | ~3 | 基础币种数据 |
| 加密扩展数据 (Crypto Extended) | ~20 | DeFi、链上数据、衍生品等 |
| 宏观经济 (Macro) | ~20 | FRED、ECB、IMF、World Bank数据源 |
| 另类数据 (Alternative) | ~8 | 超级投资者、国会交易、情绪指标等 |
| 债券/商品/结构性产品 | ~12 | 债券收益率、商品价格等 |
| 研究/情绪/筛选器 | ~15 | 分析师推荐、新闻、情绪分析等 |
| 日历/机构/其他 | ~13 | 财报日历、13-F持仓等 |
| **总计** | **~180** | 所有接口均可在免费计划中使用 |

### 免费与付费说明

**免费计划 (Free Plan):**
- 所有 180+ 接口均可访问
- 每日限额：1,000 次请求
- 涵盖股票、ETF、加密货币、宏观经济、另类数据等全部数据类别
- 适合个人开发者和小型项目

**付费计划:**
- 更高/无限的请求配额
- 优先技术支持
- 商业使用许可
- 具体定价请参考官网定价页面

**重要说明:**
- Eulerpool API 采用统一的访问模式，没有单独的"付费接口"
- `extended` 和 `alternative` 标记的接口（共 46 个）提供更高级的数据，但在免费计划中同样可用
- 所有接口都需要有效的 API Key（通过 Header 或 Query Parameter 传递）

## 认证方式

### 方法 1: Query Parameter
```
GET /api/1/equity/quotes/US0378331005?token=YOUR_API_KEY
```

### 方法 2: Authorization Header
```
Authorization: Bearer YOUR_API_KEY
```

**示例:**
```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/quotes/US0378331005' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Accept: application/json'
```

## MCP Server

Eulerpool 提供官方的 Model Context Protocol (MCP) Server，可直接连接 Claude、Cursor、Windsurf 等 AI 助手。

**配置:**
```json
{
  "mcpServers": {
    "eulerpool": {
      "command": "npx",
      "args": ["-y", "eulerpool-mcp"],
      "env": { "EULERPOOL_API_KEY": "YOUR_API_KEY" }
    }
  }
}
```

## API 分类速查

### 1. 股票数据 (Equity)

#### 基础信息
- **搜索股票** - `GET /equity/search?q={query}`
  - 通过名称、代码或 ISIN 搜索股票、ETF 和加密货币
  - 支持模糊搜索和拼写容错

- **股票列表** - `GET /equity/list`
  - 获取所有可交易股票列表

- **公司概况** - `GET /equity/profile/{identifier}`
  - 获取公司简介、行业、市值等基本信息

- **最新行情** - `GET /equity/quotes/{identifier}`
  - 获取指定 ISIN 或加密货币代码的历史价格
  - 参数: `startdate`, `enddate` (毫秒时间戳)

#### 财务报表
- **利润表** - `GET /equity/incomestatement/{identifier}`
  - 返回完整利润表数据 (收入、成本、净利润等)

- **资产负债表** - `GET /equity/balancesheet/{identifier}`
  - 返回资产负债表数据 (资产、负债、股东权益)

- **现金流量表** - `GET /equity/cashflowstatement/{identifier}`
  - 返回现金流量表数据

- **季度财务报表** - `GET /equity/income/statement/quarterly`
  - 季度利润表

#### 估值与分析
- **财务指标** - `GET /equity/metrics/{identifier}`
  - PE、PB、ROE、ROA 等财务比率

- **估值历史** - `GET /equity/valuation/history/{identifier}`
  - 历史估值数据

- **增长率** - `GET /equity/growth/{identifier}`
  - 收入、利润增长率

- **利润率** - `GET /equity/margins/{identifier}`
  - 毛利率、净利率等

- **分析师预测** - `GET /equity/estimates/{identifier}`
  - 分析师 EPS、收入预测

#### 股东与持仓
- **股权结构** - `GET /equity/ownership/{identifier}`
  - 大股东、机构持仓

- **高管信息** - `GET /equity/executives/{identifier}`
  - 公司高管列表

- **内部人交易** - `GET /equity/insider/trades/{identifier}`
  - 公司内部人员交易记录

- **做空数据** - `GET /equity/short/interest/positions/{identifier}`
  - 做空持仓量

#### 分红与拆分
- **分红历史** - `GET /equity/dividends/{identifier}`
  - 历史分红数据

- **分红质量** - `GET /equity/dividend/quality/{identifier}`
  - 分红质量评分

- **股票拆分** - `GET /equity/splits/{identifier}`
  - 股票拆分历史

#### 其他
- **同行公司** - `GET /equity/peers/{identifier}`
  - 获取同行业可比公司

- **供应链** - `GET /equity/supply/chain/{identifier}`
  - 公司供应链信息

- **业务分部** - `GET /equity/segments/{identifier}`
  - 按业务分部的收入

- **按地区收入** - `GET /equity/regions/{identifier}`
  - 按地区划分的收入

- **ESG 评级** - `GET /equity/esg/rating/{identifier}`
  - 环境、社会和治理评级

- **SWOT 分析** - `GET /equity/swot/{identifier}`
  - 公司 SWOT 分析

- **KPI 包** - `GET /equity/kpi/{identifier}`
  - 关键绩效指标汇总

- **数据覆盖** - `GET /equity/coverage/{identifier}`
  - 数据可用性检查

### 2. 市场行情 (Market Data)

- **最新报价 (批量)** - `GET /market/quotes/latest?stocks={isin1},{isin2}`
  - 获取多个股票的最新价格

- **日内行情** - `GET /market/quotes/intraday`
  - 日内价格数据

- **批量报价 (POST)** - `POST /market/quotes/bulk`
  - 批量获取报价

- **多交易所报价** - `GET /market/quotes/exchanges`
  - 多交易所价格对比

- **涨跌幅榜** - `GET /market/top/movers`
  - 涨幅/跌幅最大的股票

- **市场状态** - `GET /market/market/status`
  - 市场开闭市状态

- **市场假期** - `GET /market/holidays`
  - 交易日历

- **市场指标** - `GET /market/indicators`
  - VIX、波动率等市场指标

- **期权链** - `GET /market/options/{ticker}`
  - 通过 CBOE 获取完整期权链

- **外汇汇率** - `GET /market/fx`
  - 外汇汇率系列

- **风险分析** - `GET /market/analytics/risk`
  - 风险与收益分析

- **相关性** - `GET /market/analytics/correlation`
  - 股票相关性分析

- **52周分析** - `GET /market/analytics/52week`
  - 52周高点/低点分析

- **外汇收益** - `GET /market/analytics/fx/returns`
  - 外汇调整收益

### 3. ETF 数据

- **ETF 列表** - `GET /etf/list`
  - 所有 ETF 列表

- **ETF 概况** - `GET /etf/profile/{identifier}`
  - ETF 基本信息

- **ETF 持仓** - `GET /etf/holdings/{identifier}`
  - ETF 重仓股列表
  - 返回: symbol, name, isin, percent, share, value

- **ETF 行情** - `GET /etf/quotes/{identifier}`
  - ETF 价格数据

- **ETF 国家分布** - `GET /etf/countries/{identifier}`
  - 按国家分布

- **ETF 行业分布** - `GET /etf/sectors/{identifier}`
  - 按行业分布

- **ETF 描述** - `GET /etf/description/{identifier}`
  - ETF 详细描述

### 4. 加密货币 (Crypto)

#### 基础数据
- **币种列表** - `GET /crypto/list`
- **币种概况** - `GET /crypto/profile/{identifier}`
- **币种行情** - `GET /crypto/quotes/{identifier}`

#### 扩展数据
- **顶级币种** - `GET /crypto/extended/top/coins`
- **市场概览** - `GET /crypto/extended/market/overview`
- **分析摘要** - `GET /crypto/extended/analysis`
- **衍生品** - `GET /crypto/extended/derivatives`
- **链上指标** - `GET /crypto/extended/onchain`
- **DeFi 协议** - `GET /crypto/extended/defi`
- **DeFi 协议列表** - `GET /crypto/extended/defi/protocols`
- **DeFi 收益** - `GET /crypto/extended/defi/yields`
- **DEX 交易量** - `GET /crypto/extended/dex/volumes`
- **稳定币市值** - `GET /crypto/extended/stablecoins`
- **恐惧贪婪历史** - `GET /crypto/extended/fear/greed/history`
- **K线数据** - `GET /crypto/extended/candles`
- **链 TVL** - `GET /crypto/extended/chain/tvl`
- **DeFi 费用收入** - `GET /crypto/extended/defi/fees`
- **稳定币供应** - `GET /crypto/extended/stablecoin/supply`
- **跨链桥交易量** - `GET /crypto/extended/bridge/volumes`
- **资金费率** - `GET /crypto/extended/funding/rates`
- **持仓量** - `GET /crypto/extended/open/interest`
- **日内行情** - `GET /crypto/extended/intraday`
- **币安代码映射** - `GET /crypto/extended/symbol/map`

### 5. 研究数据 (Research)

- **分析师推荐** - `GET /research/recommendations/{identifier}`
  - 买入/卖出/持有评级

- **公司新闻** - `GET /research/news/{ticker}`
  - 公司相关新闻
  - 返回: headline, summary, source, url, datetime

- **新闻稿** - `GET /research/press/releases/{identifier}`
  - 公司新闻稿

### 6. 日历数据 (Calendar)

- **分红日历** - `GET /calendar/dividends`
  - 即将分红的公司

- **财报日历 (周度)** - `GET /calendar/earnings`
  - 本周财报发布

- **财报日历 (按代码)** - `GET /calendar/earnings/by/symbol/{identifier}`
  - 特定股票财报日期

- **财报惊喜** - `GET /calendar/earnings/surprises`
  - 超预期的财报

- **IPO 日历** - `GET /calendar/ipo`
  - 即将上市的新股

### 7. 情绪与分析 (Sentiment)

- **内部人情绪** - `GET /sentiment/insider/sentiment/{identifier}`
- **新闻情绪** - `GET /sentiment/news/sentiment/{identifier}`
- **社交媒体情绪** - `GET /sentiment/social/sentiment/{identifier}`
- **价格指标** - `GET /sentiment/price/metrics/{identifier}`
- **基金持仓** - `GET /sentiment/fund/ownership/{identifier}`
- **机构持仓** - `GET /sentiment/institutional/ownership/{identifier}`
- **行业指标** - `GET /sentiment/sector/metrics/{identifier}`

### 8. 另类数据 (Alternative Data)

- **超级投资者列表** - `GET /alternative/superinvestors/list`
- **超级投资者持仓** - `GET /alternative/superinvestors/holdings`
- **超级投资者重仓** - `GET /alternative/superinvestors/top/holdings`
- **超级投资者近期活动** - `GET /alternative/superinvestors/recent/activity`
- **国会交易** - `GET /alternative/congress/trading`
- **投资主题** - `GET /alternative/investment/themes`
- **恐惧贪婪指数** - `GET /alternative/fear/and/greed`
- **COT 持仓报告** - `GET /alternative/cot`

### 9. 宏观经济 (Macro)

- **国家列表** - `GET /macro/countries`
- **国家数据** - `GET /macro/country/{country_code}`
- **国家风险** - `GET /macro/country/risk`
- **指标数据** - `GET /macro/indicator/{indicator_code}`
- **日历** - `GET /macro/calendar`
- **日历属性** - `GET /macro/calendar/properties`
- **搜索** - `GET /macro/search`

#### 数据源
- **FRED 数据** - `GET /macro/fred/series`, `GET /macro/fred/observations`
- **ECB 数据** - `GET /macro/ecb/series`, `GET /macro/ecb/observations`
- **世界银行** - `GET /macro/worldbank/series`, `GET /macro/worldbank/observations`
- **Eurostat** - `GET /macro/eurostat/series`, `GET /macro/eurostat/observations`
- **IMF** - `GET /macro/imf/series`, `GET /macro/imf/observations`

### 10. 债券 (Bonds)

- **债券列表** - `GET /bonds/list`
- **债券价格** - `GET /bonds/prices/{identifier}`
- **债券概况** - `GET /bonds/profile/{identifier}`
- **债券行情** - `GET /bonds/ticks/{identifier}`
- **收益率曲线** - `GET /bonds/yield/curve`

### 11. 大宗商品 (Commodities)

- **商品列表** - `GET /commodity/list`
- **商品概况** - `GET /commodity/profile/{identifier}`
- **商品行情** - `GET /commodity/quotes/{identifier}`

### 12. 结构性产品 (Certificates)

- **产品列表** - `GET /certificates/list`
- **产品概况** - `GET /certificates/profile/{identifier}`
- **产品行情** - `GET /certificates/quotes/{identifier}`

### 13. 机构数据 (Institutional)

- **机构概况** - `GET /institutional/profile/{cik}`
- **13-F 持仓** - `GET /institutional/portfolio/{cik}`

### 14. 筛选器 (Screener)

- **元数据** - `GET /screener/metadata`
- **筛选** - `POST /screener/screen`
- **搜索** - `GET /screener/search`
- **股票池** - `GET /screener/universe`

### 15. 外汇 (Forex)

- **货币对列表** - `GET /forex/list`
- **汇率** - `GET /forex/rates`

### 16. 指数 (Indices)

- **成分股** - `GET /index/constituents/{index_code}`

### 17. 其他

- **ICE-SWAP 数据** - `GET /ice/swap`
- **AAQS 评分** - `GET /aaqs/by/isin/{isin}`
- **公允价值** - `GET /fair/value/by/isin/{isin}`
- **新闻 RSS** - `GET /eulerpool/news/feed.xml`
- **财报电话会议** - `GET /earning/calls/list`, `GET /earning/calls/transcript`
- **趋势** - `GET /trends/ticker/trends`

## 请求格式

### 路径参数
- `{identifier}` - ISIN 代码 (如 US0378331005) 或股票代码
- `{ticker}` - 股票代码 (如 AAPL)
- `{country_code}` - 国家代码 (如 US, DE, CN)
- `{cik}` - CIK 编号 (机构识别码)

### 查询参数
- `token` - API 密钥 (可选，也可用 Header)
- `startdate` - 开始日期 (毫秒时间戳)
- `enddate` - 结束日期 (毫秒时间戳)
- `q` - 搜索关键词
- `stocks` - 逗号分隔的 ISIN 列表

### Header
- `Authorization: Bearer YOUR_API_KEY`
- `Accept: application/json`

## 响应格式

所有端点返回 JSON 格式数据。

**成功响应示例 (股票行情):**
```json
[
  {
    "timestamp": 1732621245000,
    "price": 123.23
  }
]
```

**成功响应示例 (财务报表):**
```json
[
  {
    "revenue": 50,
    "netIncome": 6,
    "ebit": 11,
    "period": "1983-06-30T00:00:00.000Z",
    "ticker": "MSFT"
  }
]
```

**成功响应示例 (新闻):**
```json
[
  {
    "headline": "Apple Reports Record Q4 Revenue",
    "summary": "string",
    "source": "Reuters",
    "url": "https://example.com/article",
    "datetime": "2026-03-01T10:30:00.000Z",
    "category": "string",
    "image": "string"
  }
]
```

## 错误处理

### 状态码
- `200` - 成功
- `400` - 请求参数错误
- `401` - API 密钥无效或缺失
- `404` - 资源未找到

### 错误响应格式
```json
{
  "error": "Error description",
  "code": 401
}
```

## 使用场景示例

### 场景 1: 获取股票基本信息和财务报表
```bash
# 1. 搜索股票获取 ISIN
curl 'https://api.eulerpool.com/api/1/equity/search?q=Apple'
# 返回 ISIN: US0378331005

# 2. 获取公司概况
curl 'https://api.eulerpool.com/api/1/equity/profile/US0378331005' \
  -H 'Authorization: Bearer YOUR_API_KEY'

# 3. 获取利润表
curl 'https://api.eulerpool.com/api/1/equity/incomestatement/US0378331005' \
  -H 'Authorization: Bearer YOUR_API_KEY'

# 4. 获取资产负债表
curl 'https://api.eulerpool.com/api/1/equity/balancesheet/US0378331005' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 场景 2: 获取最新股价
```bash
# 单只股票
curl 'https://api.eulerpool.com/api/1/market/quotes/latest?stocks=US0378331005' \
  -H 'Authorization: Bearer YOUR_API_KEY'

# 多只股票
curl 'https://api.eulerpool.com/api/1/market/quotes/latest?stocks=US0378331005,US5949181045' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 场景 3: 获取 ETF 持仓
```bash
curl 'https://api.eulerpool.com/api/1/etf/holdings/IE00B4L5Y983' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 场景 4: 获取公司新闻
```bash
curl 'https://api.eulerpool.com/api/1/research/news/AAPL' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 场景 5: 获取财报日历
```bash
# 本周所有财报
curl 'https://api.eulerpool.com/api/1/calendar/earnings' \
  -H 'Authorization: Bearer YOUR_API_KEY'

# 特定股票财报日期
curl 'https://api.eulerpool.com/api/1/calendar/earnings/by/symbol/US0378331005' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 场景 6: 获取分析师推荐
```bash
curl 'https://api.eulerpool.com/api/1/research/recommendations/US0378331005' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 场景 7: 获取期权链
```bash
curl 'https://api.eulerpool.com/api/1/market/options/AAPL' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 场景 8: 获取内部人交易
```bash
curl 'https://api.eulerpool.com/api/1/equity/insider/trades/US0378331005' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 场景 9: 获取宏观经济数据
```bash
# FRED 数据
curl 'https://api.eulerpool.com/api/1/macro/fred/series/GDP' \
  -H 'Authorization: Bearer YOUR_API_KEY'

# 数据观测值
curl 'https://api.eulerpool.com/api/1/macro/fred/observations/GDP' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### 场景 10: 加密货币数据
```bash
# 顶级币种
curl 'https://api.eulerpool.com/api/1/crypto/extended/top/coins' \
  -H 'Authorization: Bearer YOUR_API_KEY'

# DeFi 收益
curl 'https://api.eulerpool.com/api/1/crypto/extended/defi/yields' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

## 最佳实践

1. **缓存策略**: 对于不经常变化的数据 (如公司简介、财务报表历史数据)，建议缓存结果
2. **批量请求**: 使用批量端点 (`/market/quotes/bulk`) 获取多只股票数据，减少 API 调用次数
3. **错误重试**: 对 5xx 错误实施指数退避重试策略
4. **日期格式**: 时间戳使用毫秒 (Unix epoch milliseconds)
5. **标识符**: 优先使用 ISIN 代码，全球唯一且稳定

## 常用 ISIN 示例

- **Apple (AAPL)**: US0378331005
- **Microsoft (MSFT)**: US5949181045
- **Tesla (TSLA)**: US88160R1014
- **NVIDIA (NVDA)**: US67066G1040
- **Amazon (AMZN)**: US0231351067
- **Google (GOOGL)**: US02079K3059
- **Tencent (0700.HK)**: KYG875721634
- **Alibaba (BABA)**: US01609W1027

## 文档参考

完整文档位于本地目录:
- 主文档: `docs/API_Documentation.md`
- 端点文档: `docs/*.md` (180+ 个端点文档)
- 索引文件: `index.json`

## 支持

- 官方网站: https://eulerpool.com
- 开发者门户: https://eulerpool.com/developers/
- 定价页面: https://eulerpool.com/financial-data-api/pricing
- 邮件支持: api@eulerpool.com
