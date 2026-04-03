# Press Releases

## 源URL

https://docs.financialdatasets.ai/api/earnings/press-releases

## 描述

Get earnings press releases for a ticker.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/earnings/press-releases`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The ticker symbol. |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/earnings/press-releases \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "press_releases": [
    {
      "ticker": "<string>",
      "title": "<string>",
      "url": "<string>",
      "date": "2023-12-25",
      "text": "<string>"
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
ticker = 'AAPL'

# create the URL
url = (
    f'https://api.financialdatasets.ai/earnings/press-releases'
    f'?ticker={ticker}'
)

# make API request
response = requests.get(url, headers=headers)

# parse press releases from the response
press_releases = response.json().get('press_releases')
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
GET
Earnings
GET
Press Releases
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
Get earnings press releases

cURL

Copy
curl --request GET \
  --url https://api.financialdatasets.ai/earnings/press-releases \
  --header 'X-API-KEY: <api-key>'
200
400
401
402
404
Copy
{
  "press_releases": [
    {
      "ticker": "<string>",
      "title": "<string>",
      "url": "<string>",
      "date": "2023-12-25",
      "text": "<string>"
    }
  ]
}
Earnings
Press Releases

Get earnings press releases for a ticker.

GET
/
earnings
/
press-releases
Try it
​
Overview
The Earnings Press Releases API allows you to fetch a list of earnings-related press releases for a given company.
This data is powered by RSS feeds and is updated instantly when new press releases are published.
The endpoint returns all of the earnings-related press releases that the company has filed with the SEC.
The data returned from the API includes the URL, publish date, and full text of the press release.
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.
​
Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/earnings/press-releases/tickers/
​
Getting Started
There are only 3 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Add query params like ticker to filter the data.
Execute the API request.
Note: You must include either the ticker in your query params.
​
Example
Press Releases
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
    f'https://api.financialdatasets.ai/earnings/press-releases'
    f'?ticker={ticker}'
)

# make API request
response = requests.get(url, headers=headers)

# parse press releases from the response
press_releases = response.json().get('press_releases')

Authorizations
​
X-API-KEY
stringheaderrequired

API key for authentication.

Query Parameters
​
ticker
stringrequired

The ticker symbol.

Response
200
application/json

Earnings press releases response

​
press_releases
object[]

Hide child attributes

​
press_releases.ticker
string

The ticker symbol of the company.

​
press_releases.title
string

The title of the press release.

​
press_releases.url
string<uri>

The URL of the press release.

​
press_releases.date
string<date>

The date the press release was published.

​
press_releases.text
string

The full text of the press release.

Earnings
Historical
x
github
Powered by
This documentation is built and hosted on Mintlify, a developer documentation platform
