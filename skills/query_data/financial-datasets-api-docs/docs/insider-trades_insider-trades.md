# Insider Trades (by ticker)

## 源URL

https://docs.financialdatasets.ai/api/insider-trades/insider-trades

## 描述

Get insider trades like buys and sells for a ticker by a company insider.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/insider-trades`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The ticker symbol of the company. |

## 响应字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `ticker` | string | The ticker symbol of the company. |
| `issuer` | string | The name of the issuing company. |
| `name` | string | The name of the insider. |
| `title` | string | The title of the insider. |
| `is_board_director` | boolean | Whether the insider is a board director. |
| `transaction_date` | string | <date> |
| `transaction_shares` | number | The number of shares involved in the transaction. |
| `transaction_price_per_share` | number | The price per share in the transaction. |
| `transaction_value` | number | The total value of the transaction. |
| `shares_owned_before_transaction` | number | The number of shares owned before the transaction. |
| `shares_owned_after_transaction` | number | The number of shares owned after the transaction. |
| `security_title` | string | The title of the security involved in the transaction. |
| `filing_date` | string | <date> |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url 'https://api.financialdatasets.ai/insider-trades?limit=10' \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "insider_trades": [
    {
      "ticker": "<string>",
      "issuer": "<string>",
      "name": "<string>",
      "title": "<string>",
      "is_board_director": true,
      "transaction_date": "2023-12-25",
      "transaction_shares": 123,
      "transaction_price_per_share": 123,
      "transaction_value": 123,
      "shares_owned_before_transaction": 123,
      "shares_owned_after_transaction": 123,
      "security_title": "<string>",
      "filing_date": "2023-12-25"
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

# set your query params
ticker = 'NVDA'     # stock ticker
limit = 100         # number of trades to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/insider-trades'
    f'?ticker={ticker}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse insider_trades from the response
insider_trades = response.json().get('insider_trades')
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
GET
Insider Trades (by ticker)
News
Institutional Ownership
Interest Rates
Search
SEC Filings
Segmented Financials
Stock Prices
Get insider trades

cURL

Copy
curl --request GET \
  --url 'https://api.financialdatasets.ai/insider-trades?limit=10' \
  --header 'X-API-KEY: <api-key>'
200
400
401
402
404
Copy
{
  "insider_trades": [
    {
      "ticker": "<string>",
      "issuer": "<string>",
      "name": "<string>",
      "title": "<string>",
      "is_board_director": true,
      "transaction_date": "2023-12-25",
      "transaction_shares": 123,
      "transaction_price_per_share": 123,
      "transaction_value": 123,
      "shares_owned_before_transaction": 123,
      "shares_owned_after_transaction": 123,
      "security_title": "<string>",
      "filing_date": "2023-12-25"
    }
  ]
}
Insider Trades
Insider Trades (by ticker)

Get insider trades like buys and sells for a ticker by a company insider.

GET
/
insider-trades
Try it
​
Overview
The insider trades API lets you access the stock buys and sales of public company insiders like CEOs, CFOs, and Directors.
In addition to the stock buys and sales, you can also access the current ownership stakes of insiders.
This data is useful for understanding the sentiment of company insiders. For example, you can answer questions like:
How many shares of Nvidia does Jensen Huang own?
How many shares of Microsoft did Satya Nadella buy last quarter?
How many shares of Apple has Tim Cook sold over the past year?
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.
​
Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/insider-trades/tickers/
​
Getting Started
There are only 3 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Add query params like ticker and limit to filter the data.
Execute the API request.
​
Filtering the Data
You can filter the data by ticker, limit, and filing_date.
Note: ticker is required required. By default, limit is 100 and filing_date is null.
The limit parameter is used to specify the number of trades to return. The maximum value is 1000.
The filing_date parameter is used to specify the date of the trades. For example, you can include filters like filing_date_lte=2024-09-30 and filing_date_gte=2024-01-01 to get trades between January 1, 2024 and September 30, 2024.
The available filing_date operations are:
filing_date_lte
filing_date_lt
filing_date_gte
filing_date_gt
filing_date
​
Example
Insider Trades
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     # stock ticker
limit = 100         # number of trades to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/insider-trades'
    f'?ticker={ticker}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse insider_trades from the response
insider_trades = response.json().get('insider_trades')

​
Example (with filing_date)
Insider Trades
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     
filing_date_lte = '2024-01-01' # end date
filing_date_gte = '2020-01-01' # start date

# create the URL
url = (
    f'https://api.financialdatasets.ai/insider-trades'
    f'?ticker={ticker}'
    f'&filing_date_lte={filing_date_lte}'
    f'&filing_date_gte={filing_date_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse insider_trades from the response
insider_trades = response.json().get('insider_trades')

Authorizations
​
X-API-KEY
stringheaderrequired

API key for authentication.

Query Parameters
​
ticker
stringrequired

The ticker symbol of the company.

​
limit
integerdefault:10

The maximum number of transactions to return (default: 10).

Response
200
application/json

Insider trades response

​
insider_trades
object[]

Hide child attributes

​
insider_trades.ticker
string

The ticker symbol of the company.

​
insider_trades.issuer
string

The name of the issuing company.

​
insider_trades.name
string

The name of the insider.

​
insider_trades.title
string

The title of the insider.

​
insider_trades.is_board_director
boolean

Whether the insider is a board director.

​
insider_trades.transaction_date
string<date>

The date of the transaction.

​
insider_trades.transaction_shares
number

The number of shares involved in the transaction.

​
insider_trades.transaction_price_per_share
number

The price per share in the transaction.

​
insider_trades.transaction_v
