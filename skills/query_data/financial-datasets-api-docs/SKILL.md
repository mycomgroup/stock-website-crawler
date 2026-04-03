# Financial Datasets API

## 概述

Financial Datasets API 提供全面的美股金融数据，包括：
- 股票历史价格和实时行情
- 财务报表（利润表、资产负债表、现金流量表）
- 财务指标和估值数据
- 分析师预测和盈利数据
- 公司基本信息
- 内幕交易数据
- 机构持仓数据
- 新闻资讯
- SEC文件
- 宏观经济数据（利率）

**API基础URL**: `https://api.financialdatasets.ai`
**官方文档**: https://docs.financialdatasets.ai

---

## 认证

所有API请求都需要在Header中包含API密钥：

```
X-API-KEY: your_api_key_here
```

获取API密钥: https://financialdatasets.ai

---

## API端点速查

### 1. 股票价格 (Stock Prices)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/prices` | GET | 获取历史价格数据（日/周/月/年） |
| `/prices/snapshot` | GET | 获取实时价格快照 |

**关键参数**:
- `ticker` (必需): 股票代码，如 AAPL
- `interval`: 时间间隔 (`day`, `week`, `month`, `year`)
- `start_date`: 开始日期 (YYYY-MM-DD)
- `end_date`: 结束日期 (YYYY-MM-DD)

**示例**:
```python
import requests

headers = {"X-API-KEY": "your_api_key"}
url = f"https://api.financialdatasets.ai/prices?ticker=AAPL&interval=day&start_date=2025-01-01&end_date=2025-03-25"
response = requests.get(url, headers=headers)
prices = response.json().get('prices')
```

---

### 2. 财务报表 (Financial Statements)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/financials/income-statements` | GET | 利润表 |
| `/financials/balance-sheets` | GET | 资产负债表 |
| `/financials/cash-flow-statements` | GET | 现金流量表 |
| `/financials/all-financial-statements` | GET | 所有财务报表 |

**关键参数**:
- `ticker` 或 `cik` (必需): 股票代码或CIK
- `period`: 报告周期 (`annual`, `quarterly`, `ttm`)
- `limit`: 返回记录数限制
- `report_period`: 精确报告日期 (YYYY-MM-DD)
- `report_period_gte/lte/gt/lt`: 日期范围过滤

**示例**:
```python
url = f"https://api.financialdatasets.ai/financials/income-statements?ticker=NVDA&period=annual&limit=4"
response = requests.get(url, headers=headers)
income_statements = response.json().get('income_statements')
```

---

### 3. 财务指标 (Financial Metrics)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/financial-metrics/snapshot` | GET | 实时财务指标快照 |
| `/financial-metrics` | GET | 历史财务指标 |

**包含指标**:
- 估值指标: P/E, P/B, P/S, EV/EBITDA, 市值, 企业价值
- 盈利能力: 毛利率、营业利润率、净利率、ROE、ROA、ROIC
- 运营效率: 资产周转率、存货周转率、应收账款周转率
- 流动性: 流动比率、速动比率、现金比率
- 杠杆: 负债权益比、负债资产比、利息保障倍数
- 成长性: 收入增长、盈利增长、自由现金流增长

**示例**:
```python
url = f"https://api.financialdatasets.ai/financial-metrics/snapshot?ticker=AAPL"
response = requests.get(url, headers=headers)
snapshot = response.json().get('snapshot')
pe_ratio = snapshot.get('price_to_earnings_ratio')
market_cap = snapshot.get('market_cap')
```

---

### 4. 公司信息 (Company)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/company/facts` | GET | 公司基本信息（按ticker或CIK） |

**返回字段**: 公司名称、CIK、行业、板块、交易所、位置、SIC代码等

**示例**:
```python
url = f"https://api.financialdatasets.ai/company/facts?ticker=AAPL"
response = requests.get(url, headers=headers)
company_facts = response.json().get('company_facts')
```

---

### 5. 盈利数据 (Earnings)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/earnings` | GET | 最新盈利快照 |
| `/earnings/press-releases` | GET | 盈利新闻稿 |

**返回数据**:
- 季度和年度收入、EPS（实际值和预期值）
- 惊喜值（BEAT/MISS）
- 净利润、毛利润、营业收入
- 现金流数据
- 同比增长率

**示例**:
```python
url = f"https://api.financialdatasets.ai/earnings?ticker=AAPL"
response = requests.get(url, headers=headers)
earnings = response.json().get('earnings')
quarterly_eps = earnings['quarterly']['earnings_per_share']
```

---

### 6. 分析师预测 (Analyst Estimates)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/analyst-estimates` | GET | 收入和EPS预测 |

**示例**:
```python
url = f"https://api.financialdatasets.ai/analyst-estimates?ticker=AAPL&period=annual"
response = requests.get(url, headers=headers)
estimates = response.json().get('analyst_estimates')
```

---

### 7. 新闻 (News)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/news` | GET | 公司新闻 |

**关键参数**:
- `ticker` (必需): 股票代码
- `limit`: 返回文章数量（最大10）

**示例**:
```python
url = f"https://api.financialdatasets.ai/news?ticker=AAPL&limit=5"
response = requests.get(url, headers=headers)
news = response.json().get('news')
```

---

### 8. 内幕交易 (Insider Trades)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/insider-trades` | GET | 内幕交易数据 |

**返回字段**: 交易日期、交易类型（买入/卖出）、交易股数、交易价格、持仓变化等

**示例**:
```python
url = f"https://api.financialdatasets.ai/insider-trades?ticker=AAPL"
response = requests.get(url, headers=headers)
trades = response.json().get('insider_trades')
```

---

### 9. 机构持仓 (Institutional Ownership)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/institutional-ownership` | GET | 按股票代码获取机构持仓 |
| `/institutional-ownership/investor` | GET | 按投资机构获取持仓 |

**示例**:
```python
# 按股票查询
url = f"https://api.financialdatasets.ai/institutional-ownership?ticker=AAPL"

# 按机构查询
url = f"https://api.financialdatasets.ai/institutional-ownership/investor?investor_name=Berkshire%20Hathaway"
```

---

### 10. SEC文件 (Filings)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/filings` | GET | 获取公司SEC文件列表 |
| `/filings/items` | GET | 获取文件具体项目内容 |

**示例**:
```python
url = f"https://api.financialdatasets.ai/filings?ticker=AAPL&form=10-K"
response = requests.get(url, headers=headers)
filings = response.json().get('filings')
```

---

### 11. 股票筛选器 (Stock Screener)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/financials/search/screener` | POST | 基于财务指标筛选股票 |

**支持筛选字段**:
- 利润表: revenue, gross_profit, operating_income, net_income, earnings_per_share 等
- 资产负债表: total_assets, total_debt, shareholders_equity 等
- 财务指标: pe_ratio 等

**操作符**: `gt` (>), `lt` (<), `gte` (>=), `lte` (<=), `eq` (=)

**示例**:
```python
import requests
import json

headers = {
    "X-API-KEY": "your_api_key",
    "Content-Type": "application/json"
}

body = {
    "limit": 10,
    "currency": "USD",
    "filters": [
        {"field": "pe_ratio", "operator": "lt", "value": 20},
        {"field": "revenue", "operator": "gte", "value": 1000000000},
        {"field": "total_debt", "operator": "lt", "value": 500000000}
    ]
}

url = "https://api.financialdatasets.ai/financials/search/screener"
response = requests.post(url, headers=headers, data=json.dumps(body))
results = response.json().get('results')
```

---

### 12. 宏观经济数据 (Macro)

| 端点 | 方法 | 描述 |
|------|------|------|
| `/macro/interest-rates` | GET | 利率历史数据 |
| `/macro/interest-rates/snapshot` | GET | 实时利率快照 |

**示例**:
```python
url = f"https://api.financialdatasets.ai/macro/interest-rates"
response = requests.get(url, headers=headers)
rates = response.json().get('interest_rates')
```

---

## 可用Ticker列表

大多数端点支持获取可用ticker列表：

```
GET /{endpoint}/tickers/
```

例如：
- `https://api.financialdatasets.ai/financials/income-statements/tickers/`
- `https://api.financialdatasets.ai/prices/tickers/`

---

## 通用参数参考

| 参数 | 类型 | 描述 |
|------|------|------|
| `ticker` | string | 股票代码（如 AAPL, MSFT, TSLA） |
| `cik` | string | SEC Central Index Key |
| `period` | enum | `annual`, `quarterly`, `ttm` |
| `limit` | integer | 返回记录数量限制 |
| `start_date` | string | 开始日期 (YYYY-MM-DD) |
| `end_date` | string | 结束日期 (YYYY-MM-DD) |
| `report_period` | string | 精确报告日期 |
| `report_period_gte` | string | 报告日期 >= |
| `report_period_lte` | string | 报告日期 <= |

---

## 响应状态码

- `200`: 成功
- `400`: 请求参数错误
- `401`: 认证失败（API密钥无效）
- `402`: 需要付费
- `404`: 数据不存在

---

## 数据更新频率

- **价格数据**: 实时（日内）和日终（EOD）
- **财务数据**: 季度和年度报告发布后立即更新
- **财务指标**: 实时计算
- **新闻**: 实时更新

---

## 数据来源

所有数据直接来源于主要数据源：
- SEC EDGAR（财务报表、文件）
- 交易所（价格数据）
- 公司内部披露（内幕交易）
- 13F文件（机构持仓）
- RSS源（新闻）

**特点**: 零第三方依赖，完全可追溯的数据来源

---

## 代码模板

### 基础请求模板

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "https://api.financialdatasets.ai"

def make_request(endpoint, params=None):
    headers = {"X-API-KEY": API_KEY}
    url = f"{BASE_URL}{endpoint}"
    
    if params:
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{url}?{query_string}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# 使用示例
data = make_request("/financial-metrics/snapshot", {"ticker": "AAPL"})
```

---

## API定价与免费额度

### 免费API（1个）

| API | 端点 | 说明 |
|-----|------|------|
| **Company Facts** | `/company/facts` | 获取公司基本信息（名称、CIK、行业、板块、交易所等） |

**说明**: Company Facts API 是实验性的免费API，无需付费即可访问。支持通过 `ticker` 或 `cik` 参数查询。

### 付费API（26个）

其余所有API均为付费API，包括：

| 类别 | API数量 | 端点示例 |
|------|---------|----------|
| 股票价格 | 2 | `/prices`, `/prices/snapshot` |
| 财务报表 | 4 | `/financials/income-statements`, `/financials/balance-sheets`, `/financials/cash-flow-statements`, `/financials/all-financial-statements` |
| 财务指标 | 2 | `/financial-metrics`, `/financial-metrics/snapshot` |
| 盈利数据 | 2 | `/earnings`, `/earnings/press-releases` |
| 分析师预测 | 1 | `/analyst-estimates` |
| 内幕交易 | 1 | `/insider-trades` |
| 机构持仓 | 2 | `/institutional-ownership`, `/institutional-ownership/investor` |
| 新闻 | 1 | `/news` |
| SEC文件 | 2 | `/filings`, `/filings/items` |
| 宏观经济 | 2 | `/macro/interest-rates`, `/macro/interest-rates/snapshot` |
| 股票筛选 | 2 | `/financials/search/screener`, `/financials/search/line-items` |
| 分部财务 | 1 | `/financials/segmented-revenues` |
| Ticker列表 | 4 | 各端点 `/tickers/` 或 `/ciks/` 后缀 |

**总计**: 27个API端点中，**1个免费**，**26个付费**。

### 付费提示

- **HTTP 402**: 当调用付费API但账户没有有效订阅时，会返回 `402 Payment Required` 状态码
- **订阅计划**: 参考官方定价页面了解不同套餐的调用限制和价格
- **免费试用**: 部分功能可能提供免费试用额度，需查看官网最新政策

---

## 注意事项

1. **速率限制**: 根据订阅计划有不同的API调用限制
2. **数据覆盖**: 主要覆盖美国上市股票
3. **免费API**: 仅 Company Facts API 是免费的（实验性功能）
4. **日期格式**: 所有日期使用 YYYY-MM-DD 格式
5. **货币**: 默认使用公司报告货币（通常是USD）
6. **付费订阅**: 大部分数据需要付费订阅才能访问

---

## 相关链接

- 官方文档: https://docs.financialdatasets.ai
- 获取API密钥: https://financialdatasets.ai
- 定价页面: https://financialdatasets.ai/pricing
- Discord社区: https://discord.gg/financialdatasets
