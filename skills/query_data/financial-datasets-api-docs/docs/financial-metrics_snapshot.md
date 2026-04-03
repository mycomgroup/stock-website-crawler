# Snapshot

## 源URL

https://docs.financialdatasets.ai/api/financial-metrics/snapshot

## 描述

Get the real-time financial metrics snapshot for a stock, including valuation ratios, profitability, efficiency, liquidity, leverage, growth, and per share metrics.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/financial-metrics/snapshot`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 否 | - | The ticker symbol of the company. |
| `cik` | string | 否 | - | The Central Index Key (CIK) of the company. Can be used instead of ticker. |
| `snapshot` | object | 否 | - | Hide child attributes |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/financial-metrics/snapshot \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "snapshot": {
    "ticker": "<string>",
    "market_cap": 123,
    "enterprise_value": 123,
    "price_to_earnings_ratio": 123,
    "price_to_book_ratio": 123,
    "price_to_sales_ratio": 123,
    "enterprise_value_to_ebitda_ratio": 123,
    "enterprise_value_to_revenue_ratio": 123,
    "free_cash_flow_yield": 123,
    "peg_ratio": 123,
    "gross_margin": 123,
    "operating_margin": 123,
    "net_margin": 123,
    "return_on_equity": 123,
    "return_on_assets": 123,
    "return_on_invested_capital": 123,
    "asset_turnover": 123,
    "inventory_turnover": 123,
    "receivables_turnover": 123,
    "days_sales_outstanding": 123,
    "operating_cycle": 123,
    "working_capital_turnover": 123,
    "current_ratio": 123,
    "quick_ratio": 123,
    "cash_ratio": 123,
    "operating_cash_flow_ratio": 123,
    "debt_to_equity": 123,
    "debt_to_assets": 123,
    "interest_coverage": 123,
    "revenue_growth": 123,
    "earnings_growth": 123,
    "book_value_growth": 123,
    "earnings_per_share_growth": 123,
    "free_cash_flow_growth": 123,
    "operating_income_growth": 123,
    "ebitda_growth": 123,
    "payout_ratio": 123,
    "earnings_per_share": 123,
    "book_value_per_share": 123,
    "free_cash_flow_per_share": 123
  }
}
```

### 示例 3 (python)

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'AAPL'

# create the URL
url = (
    f'https://api.financialdatasets.ai/financial-metrics/snapshot'
    f'?ticker={ticker}'
)

# make API request
response = requests.get(url, headers=headers)

# parse snapshot from the response
snapshot = response.json().get('snapshot')
```

## 详细内容

Financial Datasets home page
Search...
⌘K
Support
Dashboard
Dashboard
Pricing
Discord
Overview
Introduction
Data Provenance
Market Coverage
MCP Server
Support
APIs
Analyst Estimates
Company
Earnings
Financial Metrics
GET
Historical
GET
Snapshot
Financial Statements
Insider Trades
News
Institutional Ownership
Interest Rates
Search
SEC Filings
Segmented Financials
Stock Prices
Financial Metrics Snapshot (Real-Time)

cURL

Copy
curl --request GET \
  --url https://api.financialdatasets.ai/financial-metrics/snapshot \
  --header 'X-API-KEY: <api-key>'
200
400
401
402
404
Copy
{
  "snapshot": {
    "ticker": "<string>",
    "market_cap": 123,
    "enterprise_value": 123,
    "price_to_earnings_ratio": 123,
    "price_to_book_ratio": 123,
    "price_to_sales_ratio": 123,
    "enterprise_value_to_ebitda_ratio": 123,
    "enterprise_value_to_revenue_ratio": 123,
    "free_cash_flow_yield": 123,
    "peg_ratio": 123,
    "gross_margin": 123,
    "operating_margin": 123,
    "net_margin": 123,
    "return_on_equity": 123,
    "return_on_assets": 123,
    "return_on_invested_capital": 123,
    "asset_turnover": 123,
    "inventory_turnover": 123,
    "receivables_turnover": 123,
    "days_sales_outstanding": 123,
    "operating_cycle": 123,
    "working_capital_turnover": 123,
    "current_ratio": 123,
    "quick_ratio": 123,
    "cash_ratio": 123,
    "operating_cash_flow_ratio": 123,
    "debt_to_equity": 123,
    "debt_to_assets": 123,
    "interest_coverage": 123,
    "revenue_growth": 123,
    "earnings_growth": 123,
    "book_value_growth": 123,
    "earnings_per_share_growth": 123,
    "free_cash_flow_growth": 123,
    "operating_income_growth": 123,
    "ebitda_growth": 123,
    "payout_ratio": 123,
    "earnings_per_share": 123,
    "book_value_per_share": 123,
    "free_cash_flow_per_share": 123
  }
}
Financial Metrics
Snapshot

Get the real-time financial metrics snapshot for a stock, including valuation ratios, profitability, efficiency, liquidity, leverage, growth, and per share metrics.

GET
/
financial-metrics
/
snapshot
Try it
​
Overview
We have real-time financial metrics for all actively-traded equities in the US.
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.
​
Getting Started
There are only 3 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Add query params like ticker to filter the data.
Execute the API request.
Note: You must provide the ticker.
​
Example
Financial Metrics Snapshot
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'AAPL'

# create the URL
url = (
    f'https://api.financialdatasets.ai/financial-metrics/snapshot'
    f'?ticker={ticker}'
)

# make API request
response = requests.get(url, headers=headers)

# parse snapshot from the response
snapshot = response.json().get('snapshot')

Authorizations
​
X-API-KEY
stringheaderrequired

API key for authentication.

Query Parameters
​
ticker
string

The ticker symbol of the company.

​
cik
string

The Central Index Key (CIK) of the company. Can be used instead of ticker.

Response
200
application/json

Financial metrics snapshot response

​
snapshot
object

Hide child attributes

​
snapshot.ticker
string

The ticker symbol of the company.

​
snapshot.market_cap
number | null

The total market capitalization (stock price × shares outstanding).

​
snapshot.enterprise_value
number | null

The total value of the company (market cap + debt - cash).

​
snapshot.price_to_earnings_ratio
number | null

Price to earnings ratio.

​
snapshot.price_to_book_ratio
number | null

Price to book ratio.

​
snapshot.price_to_sales_ratio
number | null

Price to sales ratio.

​
snapshot.enterprise_value_to_ebitda_ratio
number | null

Enterprise value to EBITDA ratio.

​
snapshot.enterprise_value_to_revenue_ratio
number | null

Enterprise value to revenue ratio.

​
snapshot.free_cash_flow_yield
number | null

Free cash flow yield.

​
snapshot.peg_ratio
number | null

Price to earnings growth ratio.

​
snapshot.gross_margin
number | null

Gross profit as a percentage of revenue.

​
snapshot.operating_margin
number | null

Operating income as a percentage of revenue.

​
snapshot.net_margin
number | null

Net income as a percentage of revenue.

​
snapshot.return_on_equity
number | null

Net income as a percentage of shareholders' equity.

​
snapshot.return_on_assets
number | null

Net income as a percentage of total assets.

​
snapshot.return_on_invested_capital
number | null

Net operating profit after taxes as a percentage of invested capital.

​
snapshot.asset_turnover
number | null

Revenue divided by average total assets.

​
snapshot.inventory_turnover
number | null

Cost of goods sold divided by average inventory.

​
snapshot.receivables_turnover
number | null

Revenue divided by average accounts receivable.

​
snapshot
