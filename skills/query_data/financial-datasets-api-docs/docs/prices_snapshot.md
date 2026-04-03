# Snapshot

## 源URL

https://docs.financialdatasets.ai/api/prices/snapshot

## 描述

Get the real-time price snapshot for a stock, including the current price, day change, and day change percent.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/prices/snapshot`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The stock ticker symbol (e.g. AAPL, MSFT). |
| `snapshot` | object | 否 | - | Hide child attributes |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/prices/snapshot \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "snapshot": {
    "price": 123,
    "ticker": "<string>",
    "day_change": 123,
    "day_change_percent": 123,
    "time": "<string>",
    "time_milliseconds": 123
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
    f'https://api.financialdatasets.ai/prices/snapshot'
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
Financial Statements
Insider Trades
News
Institutional Ownership
Interest Rates
Search
SEC Filings
Segmented Financials
Stock Prices
GET
Historical
GET
Snapshot
Price Snapshot (Real-Time)

cURL

Copy
curl --request GET \
  --url https://api.financialdatasets.ai/prices/snapshot \
  --header 'X-API-KEY: <api-key>'
200
400
401
402
404
Copy
{
  "snapshot": {
    "price": 123,
    "ticker": "<string>",
    "day_change": 123,
    "day_change_percent": 123,
    "time": "<string>",
    "time_milliseconds": 123
  }
}
Stock Prices
Snapshot

Get the real-time price snapshot for a stock, including the current price, day change, and day change percent.

GET
/
prices
/
snapshot
Try it
​
Overview
The Snapshot API lets you pull a price snapshot for a given ticker. We cover all actively traded US stocks.
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.
​
Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/prices/snapshot/tickers/
​
Getting Started
There are only 3 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Add query params like ticker to filter the data.
Execute the API request.
Note: You must provide the ticker.
​
Example
Price Snapshot
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
    f'https://api.financialdatasets.ai/prices/snapshot'
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
stringrequired

The stock ticker symbol (e.g. AAPL, MSFT).

Response
200
application/json

Price snapshot response

​
snapshot
object

Hide child attributes

​
snapshot.price
number

The current price of the stock.

​
snapshot.ticker
string

The ticker symbol.

​
snapshot.day_change
number

The price change since the previous trading day's close.

​
snapshot.day_change_percent
number

The percentage price change since the previous trading day's close.

​
snapshot.time
string

The timestamp of the price snapshot in human-readable format in UTC.

​
snapshot.time_milliseconds
number

The timestamp of the price snapshot in milliseconds since epoch.

Historical
x
github
Powered by
This documentation is built and hosted on Mintlify, a developer documentation platform
