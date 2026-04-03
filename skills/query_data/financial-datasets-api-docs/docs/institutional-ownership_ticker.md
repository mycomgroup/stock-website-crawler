# Ownership (by ticker)

## 源URL

https://docs.financialdatasets.ai/api/institutional-ownership/ticker

## 描述

Get institutional ownership by investor or ticker. Requires either investor or ticker parameter, but not both.

## 请求端点

**方法**: `GET`

```text
https://api.financialdatasets.ai/institutional-ownership
```

## 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `X-API-KEY` | string | ✓ | API key for authentication. (Header参数) |
| `investor` | string | - | The name of the investment manager |
| `ticker` | string | - | The ticker symbol, if queried by investor. |
| `report_period` | string | - | Filter by exact report period date in YYYY-MM-DD format. |
| `report_period_gte` | string | - | Filter by report period greater than or equal to date in YYYY-MM-DD format. |
| `report_period_lte` | string | - | Filter by report period less than or equal to date in YYYY-MM-DD format. |
| `report_period_gt` | string | - | Filter by report period greater than date in YYYY-MM-DD format. |
| `report_period_lt` | string | - | Filter by report period less than date in YYYY-MM-DD format. |

## cURL 示例

```bash
curl --request GET \
  --url 'https://api.financialdatasets.ai/institutional-ownership?limit=10' \
  --header 'X-API-KEY: <api-key>'
```

## Python 示例

### 示例 1

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     # ticker
limit = 100         # number of holdings to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/institutional-ownership/'
    f'?ticker={ticker}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse institutional_ownership from the response
institutional_ownership = response.json().get('institutional_ownership')
```

### 示例 2

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     
limit = 100      
report_period_lte = '2024-01-01' # end date
report_period_gte = '2020-01-01' # start date

# create the URL
url = (
    f'https://api.financialdatasets.ai/institutional-ownership'
    f'?ticker={ticker}'
    f'&limit={limit}'
    f'&report_period_lte={report_period_lte}'
    f'&report_period_gte={report_period_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse institutional_ownership from the response
institutional_ownership = response.json().get('institutional_ownership')
```

## 响应示例

```json
{
  "institutional-ownership": [
    {
      "ticker": "<string>",
      "investor": "<string>",
      "report_period": "2023-12-25",
      "price": 123,
      "shares": 123,
      "market_value": 123
    }
  ]
}
```

---

## 详细文档

```
Get the equity holdings of an investment manager

cURL

curl --request GET \
  --url 'https://api.financialdatasets.ai/institutional-ownership?limit=10' \
  --header 'X-API-KEY: <api-key>'

{
  "institutional-ownership": [
    {
      "ticker": "<string>",
      "investor": "<string>",
      "report_period": "2023-12-25",
      "price": 123,
      "shares": 123,
      "market_value": 123
    }
  ]
}
Institutional Ownership
Ownership (by ticker)

Get institutional ownership by investor or ticker. Requires either investor or ticker parameter, but not both.

GET
/
institutional-ownership


Overview
The institutional ownership API provides access to the equity holdings of investment managers overseeing $100M+ in assets.
This quarterly data comes directly from Form 13F filings and includes tickers, share quantities, estimated holding prices, and market values.
When you query by ticker, the API returns the institutional owners of the specified ticker.
You can use this data to:
Track the institutional owners of a ticker
Identify emerging sector rotations and market themes
Build investment strategies based on institutional money flows
Monitor industry concentration and portfolio overlap
Note: Form 13F filings have a 45-day lag from quarter end and only include long positions in SEC-registered securities.
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.

Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/institutional-ownership/tickers/

Getting Started
There are only 3 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Add query params like ticker and limit to filter the data.
Execute the API request.

Filtering the Data
You can filter the data by ticker, limit, and report_period.
Note: ticker is required required. By default, limit is 10 and report_period is null.
The limit parameter is used to specify the number of periods to return.
The report_period parameter is used to specify the date of the holdings. For example, you can include filters like report_period_lte=2024-09-30 and report_period_gte=2024-01-01 to get holdings between January 1, 2024 and September 30, 2024.
The available report_period operations are:
report_period_lte
report_period_lt
report_period_gte
report_period_gt
report_period

Example
Institutional Ownership
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     # ticker
limit = 100         # number of holdings to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/institutional-ownership/'
    f'?ticker={ticker}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse institutional_ownership from the response
institutional_ownership = response.json().get('institutional_ownership')


Example (with report_period)
Institutional Ownership
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     
limit = 100      
report_period_lte = '2024-01-01' # end date
report_period_gte = '2020-01-01' # start date

# create the URL
url = (
    f'https://api.financialdatasets.ai/institutional-ownership'
    f'?ticker={ticker}'
    f'&limit={limit}'
    f'&report_period_lte={report_period_lte}'
    f'&report_period_gte={report_period_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse institutional_ownership from the response
institutional_ownership = response.json().get('institutional_ownership')

Authorizations

X-API-KEY
stringheaderrequired

API key for authentication.

Query Parameters

investor
string

The name of the investment manager


ticker
string

The ticker symbol, if queried by investor.


limit
integerdefault:10

The maximum number of holdings to return (default: 10).


report_period
string<date>

Filter by exact report period date in YYYY-MM-DD format.


report_period_gte
string<date>

Filter by report period greater than or equal to date in YYYY-MM-DD format.


report_period_lte
string<date>

Filter by report period less than or equal to date in YYYY-MM-DD format.


report_period_gt
string<date>

Filter by report period greater than date in YYYY-MM-DD format.


report_period_lt
string<date>

Filter by report period less than date in YYYY-MM-DD format.

Response
200
application/json

Institutional ownership response


institutional-ownership
object[]

Hide child attributes


institutional-ownership.ticker
string

The ticker symbol, if queried by investor.


institutional-ownership.investor
string

The investor name, if queried by ticker.


institutional-ownership.report_period
string<date>

The reporting period of the institutional ownership.


institutional-ownership.price
number

The estimated purchase price of the equity position.


institutional-ownership.shares
number

The number of shares held by the investment manager.


institutional-ownership.market_value
number

The market value of the equity position.

Ownership (by investor)
Historical
```
