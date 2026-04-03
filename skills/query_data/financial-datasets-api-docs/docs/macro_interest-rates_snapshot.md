# Snapshot

## 源URL

https://docs.financialdatasets.ai/api/macro/interest-rates/snapshot

## 描述

Get the current interest rates from all major central banks in the world.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/macro/interest-rates/snapshot`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/macro/interest-rates/snapshot \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "interest_rates": [
    {
      "bank": "<string>",
      "name": "<string>",
      "rate": 123,
      "date": "<string>"
    }
  ]
}
```

### 示例 3 (python)

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# create the URL
url = 'https://api.financialdatasets.ai/macro/interest-rates/snapshot'

# make API request
response = requests.get(url, headers=headers)

# parse snapshot from the response
interest_rates = response.json().get('interest_rates')
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
GET
Historical
GET
Snapshot
Search
SEC Filings
Segmented Financials
Stock Prices
Interest Rates (Real-Time)

cURL

Copy
curl --request GET \
  --url https://api.financialdatasets.ai/macro/interest-rates/snapshot \
  --header 'X-API-KEY: <api-key>'
200
401
402
404
Copy
{
  "interest_rates": [
    {
      "bank": "<string>",
      "name": "<string>",
      "rate": 123,
      "date": "<string>"
    }
  ]
}
Interest Rates
Snapshot

Get the current interest rates from all major central banks in the world.

GET
/
macro
/
interest-rates
/
snapshot
Try it
​
Overview
The Interest Rates Snapshot API lets you pull the latest published interest rate data for all major central banks in the world.
We source our data directly from global central banks like the Federal Reserve, People’s Bank of China, European Central Bank, Bank of Japan, and other major monetary authorities. The real-time interest rate data comes from official monetary policy announcements.
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.
​
Available Central Banks
You can fetch a list of available central banks with a GET request to: https://api.financialdatasets.ai/macro/interest-rates/banks/
​
Getting Started
There are only 2 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Execute the API request.
​
Example
Interest Rates Snapshot
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# create the URL
url = 'https://api.financialdatasets.ai/macro/interest-rates/snapshot'

# make API request
response = requests.get(url, headers=headers)

# parse snapshot from the response
interest_rates = response.json().get('interest_rates')

Authorizations
​
X-API-KEY
stringheaderrequired

API key for authentication.

Response
200
application/json

Interest rates snapshot response

​
interest_rates
object[]

Hide child attributes

​
interest_rates.bank
string

The symbol of the central bank.

​
interest_rates.name
string

The name of the central bank.

​
interest_rates.rate
number

The interest rate of the central bank.

​
interest_rates.date
string

The date of the interest rate in YYYY-MM-DD format.

Historical
Stock Screener
x
github
Powered by
This documentation is built and hosted on Mintlify, a developer documentation platform
