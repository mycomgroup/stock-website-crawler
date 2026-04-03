# Finnhub API Skill

## 概述

Finnhub 是一个全面的金融数据 API，提供实时股票报价、历史数据、公司信息、新闻、财务数据、技术指标等服务。API 采用 RESTful 架构，支持 WebSocket 实时数据流。

- **Base URL**: `https://finnhub.io/api/v1`
- **WebSocket URL**: `wss://ws.finnhub.io`
- **文档**: https://finnhub.io/docs/api/
- **Swagger Schema**: 可在官网下载

## 认证

所有 GET 请求需要在 URL 中添加 token 参数或使用 Header 认证：

**方式 1 - URL 参数:**
```
GET /api/v1/quote?symbol=AAPL&token=YOUR_API_KEY
```

**方式 2 - Header:**
```
X-Finnhub-Token: YOUR_API_KEY
```

获取 API Key: https://finnhub.io/dashboard

## 速率限制

- **限制**: 30 次/秒
- **超出限制**: 返回 HTTP 429 状态码
- **免费版**: 60 次/分钟
- **不同套餐**: 根据订阅套餐有不同的月度调用限制

---

## 免费 vs 付费接口

### 接口统计
- **总计接口**: 118 个
- **免费接口**: 51 个
- **付费接口 (Premium)**: 67 个

### 免费用户可用接口 (51个)

#### 基础市场数据
- **Quote** - 实时报价 (`/quote`)
- **Market Status** - 市场状态 (`/stock/market-status`)
- **Market Holiday** - 市场假日 (`/stock/market-holiday`)
- **Stock Symbol** - 股票代码列表 (`/stock/symbol`)
- **Symbol Lookup** - 代码搜索 (`/search`)

#### 新闻数据
- **Market News** - 市场新闻 (`/news`)
- **Company News** - 公司新闻 (`/company-news`) - 免费版支持 1 年历史数据，仅限北美公司

#### 财务与基本面
- **Company Basic Financials** - 公司基础财务指标 (`/stock/metric`)
- **SEC Filings** - SEC 申报文件 (`/stock/filings`)
- **Financials As Reported** - 财务报表 (`/stock/financials-reported`)
- **Recommendation Trends** - 分析师推荐趋势 (`/stock/recommendation`)
- **Stock Dividends** - 股票分红 (`/stock/dividends`)
- **Stock Splits** - 股票拆股 (`/stock/splits`)
- **Basic Financials** - 基础财务数据 (`/stock/financials`)

#### 加密货币与外汇
- **Crypto Exchanges** - 加密货币交易所 (`/crypto/exchanges`)
- **Crypto Symbol** - 加密货币代码 (`/crypto/symbol`)
- **Forex Exchanges** - 外汇交易所 (`/forex/exchanges`)
- **Forex Symbol** - 外汇代码 (`/forex/symbol`)

#### 内部人与机构数据
- **Insider Transactions** - 内部人交易 (`/stock/insider-transactions`)
- **Insider Sentiment** - 内部人情绪 (`/stock/insider-sentiment`)

#### 宏观经济
- **Earnings Calendar** - 盈利日历 (`/calendar/earnings`)
- **IPO Calendar** - IPO 日历 (`/calendar/ipo`)
- **Economic Calendar** - 经济日历 (`/calendar/economic`)

#### 实时数据 (WebSocket)
- **WebSocket Trades** - 实时交易数据
- **WebSocket News** - 实时新闻

#### ETF 与基金
- **ETFs Allocation** - ETF 资产配置
- **ETFs Holdings** - ETF 持仓
- **Mutual Fund Profile** - 共同基金档案
- **Mutual Fund Holdings** - 共同基金持仓

#### 其他
- **FDA Committee Meeting Calendar** - FDA 委员会会议日历
- **USA Spending** - 美国政府支出数据
- **USPTO Patents** - 美国专利数据
- **Open Data** - 开放数据
- **Stock Lobbying** - 股票游说数据
- **Global Filings Download** - 全球文件下载

### 付费接口 (Premium) - 需要订阅

以下接口需要付费订阅才能访问：

#### 历史与K线数据
- **Stock Candles** - 股票K线数据
- **Crypto Candles** - 加密货币K线数据
- **Forex Candles** - 外汇K线数据
- **Bond Tick Data** - 债券逐笔数据
- **Stock Tick Data** - 股票逐笔数据
- **Historical NBBO** - 历史NBBO数据

#### 公司详细信息
- **Company Profile** - 公司档案 (company-profile, company-profile2)
- **Company Executive** - 公司高管信息
- **Company Peers** - 同行公司
- **Historical Employee Count** - 历史员工数量
- **Historical Market Cap** - 历史市值

#### 盈利与预测
- **Company Earnings** - 公司盈利数据
- **EBIT Estimates** - EBIT预测
- **EBITDA Estimates** - EBITDA预测
- **EPS Estimates** - EPS预测
- **Revenue Estimates** - 收入预测
- **Earnings Call Transcripts** - 财报电话会议记录

#### 高级财务数据
- **Price Metrics** - 价格指标
- **Price Target** - 价格目标
- **Revenue Breakdown** - 收入细分
- **Revenue Breakdown & KPI** - 收入细分与KPI
- **Sector Metrics** - 行业指标
- **Basic Financials Premium** - 高级基础财务数据

#### 另类数据
- **Congressional Trading** - 国会交易
- **News Sentiment** - 新闻情绪
- **Social Sentiment** - 社交情绪
- **Filings Sentiment** - 申报文件情绪
- **Search In Filing** - 在文件中搜索
- **Supply Chain Relationships** - 供应链关系
- **Similarity Index** - 相似性指数

#### 机构数据
- **Institutional Ownership** - 机构持股
- **Institutional Portfolio (13F)** - 机构投资组合
- **Institutional Profile** - 机构档案
- **Fund Ownership** - 基金持股
- **Ownership** - 持股数据

#### 指数与ETF
- **Indices Constituents** - 指数成分股
- **Indices Historical Constituents** - 指数历史成分股
- **ETFs Country Exposure** - ETF国家敞口
- **ETFs Sector Exposure** - ETF行业敞口
- **ETFs Profile** - ETF档案

#### 债券
- **Bond Profile** - 债券档案
- **Bond Yield Curve** - 债券收益率曲线
- **Bond Price** - 债券价格

#### 技术指标
- **Aggregate Indicators** - 综合技术指标
- **Pattern Recognition** - 形态识别
- **Support/Resistance** - 支撑/阻力位
- **Technical Indicator** - 技术指标

#### ESG数据
- **ESG Score** - ESG评分
- **Historical ESG Score** - 历史ESG评分

#### 全球文件
- **Global Filings Search** - 全球文件搜索
- **Global Filings Search Filter** - 全球文件搜索筛选
- **International Filings** - 国际申报文件
- **ISIN Change** - ISIN变更
- **Symbol Change** - 代码变更

#### 其他高级功能
- **Upgrade/Downgrade** - 评级上调/下调
- **Investment Themes** - 投资主题
- **AI Copilot** - AI助手
- **Bank Branch List** - 银行网点列表
- **Economic Code/Data** - 经济代码/数据
- **Mutual Fund Country/Sector Exposure** - 共同基金国家/行业敞口
- **Mutual Fund EET** - 共同基金EET
- **Stock Newsroom** - 股票新闻室
- **Stock Presentation Slide** - 股票演示幻灯片
- **Stock Visa Application** - 股票签证申请
- **Transcripts List** - 会议记录列表
- **WebSocket Press Releases** - WebSocket新闻稿

---

## 核心 API 端点

### 1. 股票行情数据

#### 获取实时报价
```
GET /quote?symbol={symbol}
```

**参数:**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| symbol | string | 是 | 股票代码，如 AAPL |

**响应字段:**
| 字段 | 说明 |
|------|------|
| c | 当前价格 |
| d | 涨跌额 |
| dp | 涨跌幅百分比 |
| h | 当日最高价 |
| l | 当日最低价 |
| o | 当日开盘价 |
| pc | 前收盘价 |
| t | 时间戳 |

**示例:**
```python
import finnhub
finnhub_client = finnhub.Client(api_key="YOUR_API_KEY")
print(finnhub_client.quote('AAPL'))
```

#### 获取 K 线数据 (Premium)
```
GET /stock/candle?symbol={symbol}&resolution={resolution}&from={from}&to={to}
```

**参数:**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| symbol | string | 是 | 股票代码 |
| resolution | string | 是 | 时间周期: 1, 5, 15, 30, 60, D, W, M |
| from | integer | 是 | 开始时间 (UNIX 时间戳) |
| to | integer | 是 | 结束时间 (UNIX 时间戳) |

**说明:**
- 日线数据会进行拆股调整
- 日内数据不进行拆股调整
- 一次最多返回 1 个月的日内数据

**响应字段:**
| 字段 | 说明 |
|------|------|
| c | 收盘价列表 |
| h | 最高价列表 |
| l | 最低价列表 |
| o | 开盘价列表 |
| v | 成交量列表 |
| t | 时间戳列表 |
| s | 状态 (ok/no_data) |

---

### 2. 公司信息

#### 公司基本信息 (Premium)
```
GET /stock/profile?symbol={symbol}
GET /stock/profile?isin={isin}
GET /stock/profile?cusip={cusip}
```

**参数:**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| symbol | string | 否 | 股票代码 |
| isin | string | 否 | ISIN 编码 |
| cusip | string | 否 | CUSIP 编码 |

**说明:** symbol、isin、cusip 三个参数至少需要提供一个

**响应字段:**
| 字段 | 说明 |
|------|------|
| name | 公司名称 |
| ticker | 股票代码 |
| exchange | 交易所 |
| ipo | IPO 日期 |
| marketCapitalization | 市值 |
| shareOutstanding | 流通股数 |
| employeeTotal | 员工数量 |
| description | 公司简介 |
| address/city/state/country | 公司地址信息 |
| weburl | 公司网站 |
| logo | Logo 图片 URL |
| gsector/ggroup/gind/gsubind | GICS 行业分类 |
| finnhubIndustry | Finnhub 行业分类 |
| currency | 货币 |
| phone | 电话 |

#### 公司高管信息
```
GET /stock/executive?symbol={symbol}
```

#### 公司同行 (Peers)
```
GET /stock/peers?symbol={symbol}
```

---

### 3. 新闻数据

#### 公司新闻
```
GET /company-news?symbol={symbol}&from={from}&to={to}
```

**参数:**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| symbol | string | 是 | 股票代码 |
| from | string | 是 | 开始日期 (YYYY-MM-DD) |
| to | string | 是 | 结束日期 (YYYY-MM-DD) |

**说明:**
- 免费版: 1 年历史数据
- 仅支持北美公司

**响应字段:**
| 字段 | 说明 |
|------|------|
| category | 新闻分类 |
| datetime | 发布时间 (UNIX 时间戳) |
| headline | 标题 |
| id | 新闻 ID |
| image | 缩略图 URL |
| related | 相关股票 |
| source | 新闻来源 |
| summary | 摘要 |
| url | 原文链接 |

#### 市场新闻
```
GET /news?category={category}&minId={minId}
```

**参数:**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| category | string | 是 | 分类: general, forex, crypto, merger |
| minId | integer | 否 | 只返回此 ID 之后的新闻，默认 0 |

---

### 4. 财务数据

#### 基础财务指标 (Premium)
```
GET /stock/metric?symbol={symbol}&metric={metric}
```

**metric 参数:**
- `all`: 所有指标
- `price`: 价格相关指标
- `valuation`: 估值指标
- `growth`: 增长指标
- `margin`: 利润率指标
- `management`: 管理效率指标
- `financials`: 财务实力指标

#### 财务报表 (Premium)
```
GET /stock/financials?symbol={symbol}&statement={statement}&freq={freq}
```

**参数:**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| symbol | string | 是 | 股票代码 |
| statement | string | 是 | 报表类型: bs (资产负债表), ic (利润表), cf (现金流量表) |
| freq | string | 是 | 频率: annual, quarterly |

#### 盈利数据
```
GET /stock/earnings?symbol={symbol}
```

---

### 5. 搜索功能

#### 代码搜索
```
GET /search?q={query}&exchange={exchange}
```

**参数:**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| q | string | 是 | 查询文本 (代码、名称、ISIN、CUSIP) |
| exchange | string | 否 | 交易所限制 |

**响应字段:**
| 字段 | 说明 |
|------|------|
| count | 结果数量 |
| result | 结果数组 |
| result[].symbol | 唯一代码 |
| result[].displaySymbol | 显示代码 |
| result[].description | 描述 |
| result[].type | 证券类型 |

---

### 6. 技术指标 (Premium)

#### 综合技术指标信号
```
GET /scan/technical-indicator?symbol={symbol}&resolution={resolution}
```

**说明:** 综合 MACD、RSI、移动平均线等多个技术指标的信号

**响应字段:**
| 字段 | 说明 |
|------|------|
| technicalAnalysis.signal | 信号: buy, sell, neutral |
| technicalAnalysis.count | 各信号数量统计 |
| trend.adx | ADX 值 |
| trend.trending | 是否处于趋势中 |

---

### 7. WebSocket 实时数据

#### 实时交易数据
```
wss://ws.finnhub.io?token=YOUR_API_KEY
```

**订阅消息:**
```json
{"type":"subscribe","symbol":"AAPL"}
{"type":"subscribe","symbol":"AMZN"}
{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| type | 消息类型 (trade) |
| data | 交易数据数组 |
| data[].s | 代码 |
| data[].p | 最新价格 |
| data[].t | 时间戳 (毫秒) |
| data[].v | 成交量 |
| data[].c | 交易条件 |

**Python 示例:**
```python
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(data)

def on_open(ws):
    # 订阅股票
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

ws = websocket.WebSocketApp(
    "wss://ws.finnhub.io?token=YOUR_API_KEY",
    on_message=on_message,
    on_open=on_open
)
ws.run_forever()
```

**注意:**
- 每个 API Key 只能维持 1 个 WebSocket 连接
- FXCM、Forex.com、FHFX 不支持流式传输

---

### 8. 加密货币和外汇

#### 加密货币 K 线
```
GET /crypto/candle?symbol={symbol}&resolution={resolution}&from={from}&to={to}
```

#### 外汇汇率
```
GET /forex/rates?base={base}
```

**参数:**
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| base | string | 否 | 基础货币，默认 USD |

---

## 常用代码示例

### Python
```python
import finnhub

# 初始化客户端
finnhub_client = finnhub.Client(api_key="YOUR_API_KEY")

# 获取实时报价
quote = finnhub_client.quote('AAPL')
print(f"当前价格: {quote['c']}")

# 获取公司信息
profile = finnhub_client.company_profile(symbol='AAPL')
print(f"公司名称: {profile['name']}")

# 获取公司新闻
news = finnhub_client.company_news('AAPL', _from="2024-01-01", to="2024-12-31")
for item in news[:5]:
    print(f"{item['headline']} - {item['source']}")

# 搜索代码
results = finnhub_client.symbol_lookup('apple')
for result in results['result']:
    print(f"{result['symbol']}: {result['description']}")
```

### JavaScript
```javascript
const finnhub = require('finnhub');

const api_key = finnhub.ApiClient.instance.authentications['api_key'];
api_key.apiKey = "YOUR_API_KEY"
const finnhubClient = new finnhub.DefaultApi()

// 获取实时报价
finnhubClient.quote("AAPL", (error, data, response) => {
  console.log(data)
});

// 获取公司新闻
finnhubClient.companyNews("AAPL", "2024-01-01", "2024-12-31", (error, data, response) => {
  console.log(data)
});
```

### cURL
```bash
# 获取实时报价
curl "https://finnhub.io/api/v1/quote?symbol=AAPL&token=YOUR_API_KEY"

# 获取公司信息
curl "https://finnhub.io/api/v1/stock/profile2?symbol=AAPL&token=YOUR_API_KEY"

# 获取公司新闻
curl "https://finnhub.io/api/v1/company-news?symbol=AAPL&from=2024-01-01&to=2024-12-31&token=YOUR_API_KEY"
```

---

## 错误处理

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 429 | 超出速率限制 |
| 500 | 服务器错误 |

---

## 最佳实践

1. **使用 WebSocket 获取实时数据**: 不要轮询 HTTP API 获取实时价格，使用 WebSocket
2. **缓存数据**: 适当缓存不经常变化的数据（如公司信息）
3. **处理速率限制**: 实现指数退避重试机制
4. **使用批量请求**: 减少 API 调用次数
5. **错误处理**: 始终处理网络错误和 API 错误

---

## 文档文件列表

本 Skill 基于以下文档生成:

- `api_overview.md` - API 概览
- `authentication.md` - 认证说明
- `rate-limit.md` - 速率限制
- `quote.md` - 实时报价
- `stock-candles.md` - K 线数据
- `company-profile.md` - 公司信息
- `company-news.md` - 公司新闻
- `market-news.md` - 市场新闻
- `symbol-search.md` - 代码搜索
- `technical-indicator.md` - 技术指标
- `websocket-trades.md` - WebSocket 实时数据
- `company-earnings.md` - 盈利数据
- `company-executive.md` - 高管信息
- `company-peers.md` - 同行公司
- `financials.md` - 财务报表
- `crypto-candles.md` - 加密货币数据
- `forex-rates.md` - 外汇汇率
- 其他 100+ 个端点文档

完整文档位于: `/Users/yuping/Downloads/git/stock-website-crawler/stock-crawler/merged_output/finnhub-api-docs/docs/`
