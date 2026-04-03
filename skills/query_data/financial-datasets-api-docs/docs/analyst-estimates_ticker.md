---
id: "url-4b067b47"
type: "api"
title: "Analyst Estimates"
url: "https://docs.financialdatasets.ai/api/analyst-estimates/ticker"
description: "The ticker to get analyst estimates for."
source: ""
tags: []
crawl_time: "2026-03-18T03:13:44.835Z"
metadata:
  requestMethod: "GET"
  endpoint: "https://api.financialdatasets.ai/analyst-estimates"
  requestParams:
    - {"name":"X-API-KEY","type":"string","required":"是","description":"API key for authentication. (Header参数)"}
    - {"name":"ticker","type":"string","required":"是","description":"The ticker to get analyst estimates for."}
    - {"name":"period","type":"enum","required":"","description":"The period to get analyst estimates for. Use the /analyst-estimates/periods endpoint to get a list of available periods. Defaults to 'annual'."}
  responseFields:
    - {"name":"fiscal_period","type":"string","description":"<date>"}
    - {"name":"period","type":"enum<string>","description":"The period of the analyst estimate."}
    - {"name":"revenue","type":"integer","description":"The estimated revenue."}
    - {"name":"earnings_per_share","type":"number","description":"The estimated earnings per share."}
  codeExamples:
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/analyst-estimates \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/analyst-estimates \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"json","code":"{\n  \"analyst_estimates\": [\n    {\n      \"fiscal_period\": \"2023-12-25\",\n      \"period\": \"annual\",\n      \"revenue\": 123,\n      \"earnings_per_share\": 123\n    }\n  ]\n}"}
    - {"language":"json","code":"{\n  \"analyst_estimates\": [\n    {\n      \"fiscal_period\": \"2023-12-25\",\n      \"period\": \"annual\",\n      \"revenue\": 123,\n      \"earnings_per_share\": 123\n    }\n  ]\n}"}
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/analyst-estimates \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/analyst-estimates \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"json","code":"{\n  \"analyst_estimates\": [\n    {\n      \"fiscal_period\": \"2023-12-25\",\n      \"period\": \"annual\",\n      \"revenue\": 123,\n      \"earnings_per_share\": 123\n    }\n  ]\n}"}
    - {"language":"json","code":"{\n  \"analyst_estimates\": [\n    {\n      \"fiscal_period\": \"2023-12-25\",\n      \"period\": \"annual\",\n      \"revenue\": 123,\n      \"earnings_per_share\": 123\n    }\n  ]\n}"}
    - {"language":"python","code":"import requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\nticker = 'AAPL'\nperiod = 'annual'         # possible values are {'annual', 'quarterly'}\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/analyst-estimates/'\n    f'?ticker={ticker}'\n    f'&period={period}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse estimates from the response\nestimates = response.json().get('analyst_estimates')"}
    - {"language":"python","code":"import requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\nticker = 'AAPL'\nperiod = 'annual'         # possible values are {'annual', 'quarterly'}\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/analyst-estimates/'\n    f'?ticker={ticker}'\n    f'&period={period}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse estimates from the response\nestimates = response.json().get('analyst_estimates')"}
  rawContent: "Financial Datasets home page\nSearch...\n⌘K\nSupport\nDashboard\nDashboard\nPricing\nDiscord\nOverview\nIntroduction\nData Provenance\nMarket Coverage\nMCP Server\nSupport\nAPIs\nAnalyst Estimates\nGET\nAnalyst Estimates\nCompany\nEarnings\nFinancial Metrics\nFinancial Statements\nInsider Trades\nNews\nInstitutional Ownership\nInterest Rates\nSearch\nSEC Filings\nSegmented Financials\nStock Prices\nAnalyst Estimates\n\ncURL\n\nCopy\ncurl --request GET \\\n  --url https://api.financialdatasets.ai/analyst-estimates \\\n  --header 'X-API-KEY: <api-key>'\n200\n400\n401\n402\n404\nCopy\n{\n  \"analyst_estimates\": [\n    {\n      \"fiscal_period\": \"2023-12-25\",\n      \"period\": \"annual\",\n      \"revenue\": 123,\n      \"earnings_per_share\": 123\n    }\n  ]\n}\nAnalyst Estimates\nAnalyst Estimates\nGET\n/\nanalyst-estimates\nTry it\n​\nOverview\nThis API provides earnings per share (EPS) and revenue estimates for a given ticker.\nThe data is generated from our own internal models and should be considered as probabilistic forecasts, not guarantees of future performance. Our mean estimates track consensus closely, with an average deviation of less than 1% compared to leading sell-side consensus providers.\n​\nAvailable Tickers\nYou can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/analyst-estimates/tickers/\n​\nExample\nAnalyst Estimates\nCopy\nimport requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\nticker = 'AAPL'\nperiod = 'annual'         # possible values are {'annual', 'quarterly'}\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/analyst-estimates/'\n    f'?ticker={ticker}'\n    f'&period={period}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse estimates from the response\nestimates = response.json().get('analyst_estimates')\n\nAuthorizations\n​\nX-API-KEY\nstringheaderrequired\n\nAPI key for authentication.\n\nQuery Parameters\n​\nticker\nstringrequired\n\nThe ticker to get analyst estimates for.\n\n​\nperiod\nenum<string>\n\nThe period to get analyst estimates for. Use the /analyst-estimates/periods endpoint to get a list of available periods. Defaults to 'annual'.\n\nAvailable options: annual, quarterly \nResponse\n200\napplication/json\n\nAnalyst estimates response\n\n​\nanalyst_estimates\nobject[]\n\nHide child attributes\n\n​\nanalyst_estimates.fiscal_period\nstring<date>\n\nThe fiscal period of the analyst estimate.\n\n​\nanalyst_estimates.period\nenum<string>\n\nThe period of the analyst estimate.\n\nAvailable options: annual, quarterly \n​\nanalyst_estimates.revenue\ninteger\n\nThe estimated revenue.\n\n​\nanalyst_estimates.earnings_per_share\nnumber\n\nThe estimated earnings per share.\n\nSupport\nFacts (by CIK)\nx\ngithub\nPowered by\nThis documentation is built and hosted on Mintlify, a developer documentation platform"
  suggestedFilename: "analyst-estimates_ticker"
---

# Analyst Estimates

## 源URL

https://docs.financialdatasets.ai/api/analyst-estimates/ticker

## 描述

The ticker to get analyst estimates for.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/analyst-estimates`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The ticker to get analyst estimates for. |
| `period` | enum | 否 | - | The period to get analyst estimates for. Use the /analyst-estimates/periods endpoint to get a list of available periods. Defaults to 'annual'. |

## 响应字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `fiscal_period` | string | <date> |
| `period` | enum<string> | The period of the analyst estimate. |
| `revenue` | integer | The estimated revenue. |
| `earnings_per_share` | number | The estimated earnings per share. |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/analyst-estimates \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "analyst_estimates": [
    {
      "fiscal_period": "2023-12-25",
      "period": "annual",
      "revenue": 123,
      "earnings_per_share": 123
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
period = 'annual'         # possible values are {'annual', 'quarterly'}

# create the URL
url = (
    f'https://api.financialdatasets.ai/analyst-estimates/'
    f'?ticker={ticker}'
    f'&period={period}'
)

# make API request
response = requests.get(url, headers=headers)

# parse estimates from the response
estimates = response.json().get('analyst_estimates')
```

## 文档正文

The ticker to get analyst estimates for.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.financialdatasets.ai/analyst-estimates`

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
GET
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
Analyst Estimates

cURL

Copy
curl --request GET \
  --url https://api.financialdatasets.ai/analyst-estimates \
  --header 'X-API-KEY: <api-key>'
200
400
401
402
404
Copy
{
  "analyst_estimates": [
    {
      "fiscal_period": "2023-12-25",
      "period": "annual",
      "revenue": 123,
      "earnings_per_share": 123
    }
  ]
}
Analyst Estimates
Analyst Estimates
GET
/
analyst-estimates
Try it

Overview
This API provides earnings per share (EPS) and revenue estimates for a given ticker.
The data is generated from our own internal models and should be considered as probabilistic forecasts, not guarantees of future performance. Our mean estimates track consensus closely, with an average deviation of less than 1% compared to leading sell-side consensus providers.

Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/analyst-estimates/tickers/

Example
Analyst Estimates
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'AAPL'
period = 'annual'         # possible values are {'annual', 'quarterly'}

# create the URL
url = (
    f'https://api.financialdatasets.ai/analyst-estimates/'
    f'?ticker={ticker}'
    f'&period={period}'
)

# make API request
response = requests.get(url, headers=headers)

# parse estimates from the response
estimates = response.json().get('analyst_estimates')

Authorizations

X-API-KEY
stringheaderrequired

API key for authentication.

Query Parameters

ticker
stringrequired

The ticker to get analyst estimates for.

period
enum<string>

The period to get analyst estimates for. Use the /analyst-estimates/periods endpoint to get a list of available periods. Defaults to 'annual'.

Available options: annual, quarterly 
Response
200
application/json

Analyst estimates response

analyst_estimates
object[]

Hide child attributes

analyst_estimates.fiscal_period
string<date>

The fiscal period of the analyst estimate.

analyst_estimates.period
enum<string>

The period of the analyst estimate.

Available options: annual, quarterly 

analyst_estimates.revenue
integer

The estimated revenue.

analyst_estimates.earnings_per_share
number

The estimated earnings per share.

Support
Facts (by CIK)
x
github
Powered by
This documentation is built and hosted on Mintlify, a developer documentation platform
