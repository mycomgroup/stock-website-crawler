# Massive (Polygon.io) API Skill

## 数据源概述

Massive API（前身为Polygon.io）提供全面的金融市场数据服务，包括美国股票、加密货币、外汇、期货、期权和指数的实时及历史数据。

**基础URL**: `https://api.massive.com`
**文档地址**: https://massive.com/docs

## 认证方式

所有API请求需要在URL参数中添加API Key:
```
?apiKey=YOUR_API_KEY
```

## 数据类型覆盖

### 1. 股票数据 (Stocks)
- **覆盖范围**: 所有19个主要美国股票交易所 + 暗池 + FINRA交易设施 + OTC市场
- **交易时段**: 
  - 盘前: 4:00 AM - 9:30 AM ET
  - 常规: 9:30 AM - 4:00 PM ET
  - 盘后: 4:00 PM - 8:00 PM ET
- **时间戳**: Unix时间戳(毫秒)，UTC时区

### 2. 加密货币 (Crypto)
- 主要加密货币交易对的OHLC数据
- 交易数据和聚合数据
- UTC时区

### 3. 外汇 (Forex)
- 货币对报价和交易数据
- 日聚合和分钟聚合数据
- 历史数据从2009年开始

### 4. 期货 (Futures)
- 期货合约数据
- 交易报价和合约信息

### 5. 期权 (Options)
- 期权合约数据
- 日聚合和分钟聚合
- 交易和报价数据

### 6. 指数 (Indices)
- 主要市场指数数据
- 日聚合和分钟聚合

### 7. 经济数据 (Economy)
- 通胀预期和通胀数据
- 劳动力市场数据
- 国债收益率

## 核心API端点

### 股票API

#### 1. 获取聚合OHLC数据 (Aggregates/Bars)
```
GET /v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

**参数**:
- `stocksTicker`: 股票代码(如AAPL)
- `multiplier`: 时间跨度乘数
- `timespan`: 时间窗口大小 (minute, hour, day, week, month, quarter, year)
- `from`: 开始日期(YYYY-MM-DD)或毫秒时间戳
- `to`: 结束日期(YYYY-MM-DD)或毫秒时间戳
- `adjusted`: 是否调整拆股(默认true)
- `sort`: 排序方式(asc/desc)
- `limit`: 返回结果数量(默认5000，最大50000)

**响应字段**:
- `c`: 收盘价
- `h`: 最高价
- `l`: 最低价
- `o`: 开盘价
- `v`: 成交量
- `vw`: 成交量加权平均价
- `n`: 交易次数
- `t`: Unix毫秒时间戳

**示例**:
```bash
curl -X GET "https://api.massive.com/v2/aggs/ticker/AAPL/range/1/day/2025-11-03/2025-11-28?adjusted=true&sort=asc&limit=120&apiKey=YOUR_API_KEY"
```

#### 2. 获取所有股票代码 (Tickers)
```
GET /v3/reference/tickers
```

**参数**:
- `ticker`: 股票代码筛选
- `type`: 资产类型
- `market`: 市场类型(stocks, crypto, fx, indices)
- `exchange`: 交易所MIC代码
- `search`: 搜索关键词
- `active`: 是否只返回活跃交易的股票(默认true)
- `limit`: 返回数量(默认100，最大1000)

**响应字段**:
- `ticker`: 交易代码
- `name`: 公司名称
- `market`: 市场类型
- `locale`: 地区(us/global)
- `primary_exchange`: 主要交易所ISO代码
- `type`: 资产类型
- `active`: 是否活跃
- `currency_name`: 货币名称
- `cik`: CIK编号
- `composite_figi`: OpenFIGI编号

**示例**:
```bash
curl -X GET "https://api.massive.com/v3/reference/tickers?market=stocks&active=true&limit=100&apiKey=YOUR_API_KEY"
```

#### 3. 获取股票基本信息 (Ticker Details)
```
GET /v3/reference/tickers/{ticker}
```

返回特定股票的详细信息，包括公司描述、行业、员工数等。

#### 4. 财务报表数据 (Financials) ⚠️ 已弃用
```
GET /vX/reference/financials
```

**注意**: 此端点将于2026年2月23日移除，请使用以下替代端点:
- Balance Sheets: `/vX/reference/financials?ticker={ticker}&timeframe=quarterly`
- Cash Flow Statements
- Income Statements

**参数**:
- `ticker`: 股票代码
- `cik`: CIK编号
- `filing_date`: 申报日期(YYYY-MM-DD)
- `period_of_report_date`: 报告期日期
- `timeframe`: 时间框架(quarterly, annual, ttm)
- `limit`: 返回数量(默认10，最大100)

**响应包含**:
- `balance_sheet`: 资产负债表
- `cash_flow_statement`: 现金流量表
- `income_statement`: 利润表
- `comprehensive_income`: 综合收益
- `filing_date`: 申报日期
- `fiscal_period`: 财政期间(Q1/Q2/Q3/Q4/FY)
- `fiscal_year`: 财政年度

#### 5. 公司行为数据

**分红数据**:
```
GET /v3/reference/dividends
```

**拆股数据**:
```
GET /v3/reference/splits
```

**IPO数据**:
```
GET /vX/reference/ipos
```

#### 6. 股票新闻
```
GET /v2/reference/news
```

获取与股票相关的新闻文章。

### 加密货币API

#### 1. 获取加密货币OHLC数据
```
GET /v2/aggs/ticker/{cryptoTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

**注意**: 加密货币代码格式为 `X:{BASE}{QUOTE}`，如 `X:BTCUSD`

**示例**:
```bash
curl -X GET "https://api.massive.com/v2/aggs/ticker/X:BTCUSD/range/1/day/2025-11-03/2025-11-28?apiKey=YOUR_API_KEY"
```

#### 2. 获取所有加密货币代码
```
GET /v3/reference/tickers?market=crypto
```

#### 3. 获取加密货币交易所列表
```
GET /v1/meta/crypto-exchanges
```

### 外汇API

#### 1. 获取外汇OHLC数据
```
GET /v2/aggs/ticker/{forexTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

**注意**: 外汇代码格式为 `C:{FROM}{TO}`，如 `C:EURUSD`

#### 2. 货币转换
```
GET /v1/conversion/{from}/{to}
```

实时货币汇率转换。

### 期货API

#### 1. 获取期货合约数据
```
GET /v3/reference/futures/contracts
```

#### 2. 获取期货OHLC数据
```
GET /v2/aggs/ticker/{futuresTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

### 期权API

#### 1. 获取期权合约
```
GET /v3/reference/options/contracts
```

#### 2. 获取期权OHLC数据
```
GET /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

**注意**: 期权代码格式为 `O:{UNDERLYING}{EXPIRY}{TYPE}{STRIKE}`

### 指数API

#### 1. 获取指数数据
```
GET /v2/aggs/ticker/{indicesTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

**注意**: 指数代码格式为 `I:{INDEX}`，如 `I:SPX`

### 经济数据API

#### 1. 通胀预期
```
GET /v2/economy/expectations/inflation
```

#### 2. 通胀数据
```
GET /v2/economy/inflation/{indicator}
```

#### 3. 劳动力市场数据
```
GET /v2/economy/labor/{indicator}
```

#### 4. 国债收益率
```
GET /v2/economy/treasury/{maturity}
```

## 通用参数说明

### 分页参数
- `limit`: 每页返回数量
- `next_url`: 下一页URL(在响应中提供)

### 排序参数
- `sort`: 排序字段
- `order`: 排序方向(asc/desc)

### 日期格式
- 日期字符串: `YYYY-MM-DD`
- 时间戳: 毫秒级Unix时间戳

## 错误处理

API返回标准HTTP状态码:
- `200`: 成功
- `400`: 请求参数错误
- `401`: API Key无效
- `403`: 权限不足
- `404`: 资源不存在
- `429`: 请求频率超限
- `500`: 服务器错误

错误响应格式:
```json
{
  "status": "ERROR",
  "error": "错误描述信息"
}
```

## 使用示例

### Python示例

```python
import requests

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.massive.com"

# 获取AAPL日K线数据
def get_stock_bars(ticker, from_date, to_date, timespan="day", multiplier=1):
    endpoint = f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
    url = f"{BASE_URL}{endpoint}?apiKey={API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "OK":
            return data.get("results", [])
    return None

# 获取股票列表
def get_tickers(market="stocks", limit=100):
    endpoint = "/v3/reference/tickers"
    url = f"{BASE_URL}{endpoint}?market={market}&limit={limit}&apiKey={API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "OK":
            return data.get("results", [])
    return None

# 使用示例
bars = get_stock_bars("AAPL", "2025-01-01", "2025-01-31")
print(bars)
```

### JavaScript/Node.js示例

```javascript
const API_KEY = "YOUR_API_KEY";
const BASE_URL = "https://api.massive.com";

// 获取股票数据
async function getStockBars(ticker, fromDate, toDate, timespan = "day", multiplier = 1) {
    const endpoint = `/v2/aggs/ticker/${ticker}/range/${multiplier}/${timespan}/${fromDate}/${toDate}`;
    const url = `${BASE_URL}${endpoint}?apiKey=${API_KEY}`;
    
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.status === "OK") {
        return data.results;
    }
    return null;
}

// 使用示例
getStockBars("AAPL", "2025-01-01", "2025-01-31")
    .then(bars => console.log(bars));
```

## 注意事项

1. **时区处理**: 股票数据使用ET时区，加密货币使用UTC时区
2. **时间戳**: 所有时间戳均为Unix毫秒时间戳
3. **分页**: 大数据集使用`next_url`进行分页获取
4. **限制**: 注意API调用频率限制
5. **弃用接口**: Financials端点已弃用，请使用替代端点

## 数据覆盖范围

### 股票交易所
- NYSE, NYSE American, NYSE Arca, NYSE Chicago, NYSE National
- Nasdaq (OMX, BX, PSX, Philadelphia)
- Cboe Global Markets (BZX, BYX, EDGX, EDGA)
- MIAX Exchange Group (Pearl, Emerald, Equities)
- Members Exchange (MEMX)
- Investors Exchange (IEX)
- Long-Term Stock Exchange (LTSE)
- FINRA Trading Facilities
- OTC Reporting Facility

### 历史数据
- 股票: 从2003年开始
- 外汇: 从2009年开始
- 加密货币: 从2010年开始
- 期权: 从2014年开始

## 参考资源

- 完整文档: https://massive.com/docs
- API状态页: https://status.massive.com
- 支持邮箱: support@massive.com
