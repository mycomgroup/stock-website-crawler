---
id: "url-217e360e"
type: "api"
title: "Facts (by ticker)"
url: "https://docs.financialdatasets.ai/api/company/facts/ticker"
description: "Get company facts for a ticker."
source: ""
tags: []
crawl_time: "2026-03-18T04:35:36.856Z"
metadata:
  requestMethod: "GET"
  endpoint: "https://api.financialdatasets.ai/company/facts"
  requestParams:
    - {"name":"X-API-KEY","type":"string","required":"是","description":"API key for authentication. (Header参数)"}
    - {"name":"ticker","type":"string","required":"","description":"The ticker symbol."}
    - {"name":"cik","type":"string","required":"","description":"The CIK of the company."}
  responseFields: []
  codeExamples:
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/company/facts \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/company/facts \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"json","code":"{\n  \"company_facts\": {\n    \"ticker\": \"<string>\",\n    \"name\": \"<string>\",\n    \"cik\": \"<string>\",\n    \"industry\": \"<string>\",\n    \"sector\": \"<string>\",\n    \"category\": \"<string>\",\n    \"exchange\": \"<string>\",\n    \"is_active\": true,\n    \"location\": \"<string>\",\n    \"sec_filings_url\": \"<string>\",\n    \"sic_code\": \"<string>\",\n    \"sic_industry\": \"<string>\",\n    \"sic_sector\": \"<string>\"\n  }\n}"}
    - {"language":"json","code":"{\n  \"company_facts\": {\n    \"ticker\": \"<string>\",\n    \"name\": \"<string>\",\n    \"cik\": \"<string>\",\n    \"industry\": \"<string>\",\n    \"sector\": \"<string>\",\n    \"category\": \"<string>\",\n    \"exchange\": \"<string>\",\n    \"is_active\": true,\n    \"location\": \"<string>\",\n    \"sec_filings_url\": \"<string>\",\n    \"sic_code\": \"<string>\",\n    \"sic_industry\": \"<string>\",\n    \"sic_sector\": \"<string>\"\n  }\n}"}
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/company/facts \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/company/facts \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"json","code":"{\n  \"company_facts\": {\n    \"ticker\": \"<string>\",\n    \"name\": \"<string>\",\n    \"cik\": \"<string>\",\n    \"industry\": \"<string>\",\n    \"sector\": \"<string>\",\n    \"category\": \"<string>\",\n    \"exchange\": \"<string>\",\n    \"is_active\": true,\n    \"location\": \"<string>\",\n    \"sec_filings_url\": \"<string>\",\n    \"sic_code\": \"<string>\",\n    \"sic_industry\": \"<string>\",\n    \"sic_sector\": \"<string>\"\n  }\n}"}
    - {"language":"json","code":"{\n  \"company_facts\": {\n    \"ticker\": \"<string>\",\n    \"name\": \"<string>\",\n    \"cik\": \"<string>\",\n    \"industry\": \"<string>\",\n    \"sector\": \"<string>\",\n    \"category\": \"<string>\",\n    \"exchange\": \"<string>\",\n    \"is_active\": true,\n    \"location\": \"<string>\",\n    \"sec_filings_url\": \"<string>\",\n    \"sic_code\": \"<string>\",\n    \"sic_industry\": \"<string>\",\n    \"sic_sector\": \"<string>\"\n  }\n}"}
    - {"language":"python","code":"import requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\nticker = 'AAPL'\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/company/facts'\n    f'?ticker={ticker}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse company_facts from the response\ncompany_facts = response.json().get('company_facts')"}
    - {"language":"python","code":"import requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\nticker = 'AAPL'\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/company/facts'\n    f'?ticker={ticker}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse company_facts from the response\ncompany_facts = response.json().get('company_facts')"}
  rawContent: "Financial Datasets home page\nSearch...\n⌘K\nSupport\nDashboard\nDashboard\nPricing\nDiscord\nOverview\nIntroduction\nData Provenance\nMarket Coverage\nMCP Server\nSupport\nAPIs\nAnalyst Estimates\nCompany\nGET\nFacts (by CIK)\nGET\nFacts (by ticker)\nEarnings\nFinancial Metrics\nFinancial Statements\nInsider Trades\nNews\nInstitutional Ownership\nInterest Rates\nSearch\nSEC Filings\nSegmented Financials\nStock Prices\nGet company facts\n\ncURL\n\nCopy\ncurl --request GET \\\n  --url https://api.financialdatasets.ai/company/facts \\\n  --header 'X-API-KEY: <api-key>'\n200\n400\n401\n404\nCopy\n{\n  \"company_facts\": {\n    \"ticker\": \"<string>\",\n    \"name\": \"<string>\",\n    \"cik\": \"<string>\",\n    \"industry\": \"<string>\",\n    \"sector\": \"<string>\",\n    \"category\": \"<string>\",\n    \"exchange\": \"<string>\",\n    \"is_active\": true,\n    \"location\": \"<string>\",\n    \"sec_filings_url\": \"<string>\",\n    \"sic_code\": \"<string>\",\n    \"sic_industry\": \"<string>\",\n    \"sic_sector\": \"<string>\"\n  }\n}\nCompany\nFacts (by ticker)\n\nGet company facts for a ticker.\n\nGET\n/\ncompany\n/\nfacts\nTry it\n​\nOverview\nCompany facts includes data like name, CIK, market cap, total employees, website URL, and more.\nThe company facts API provides a simple way to access the most important high-level information about a company.\nPlease note: This API is experimental and free to use.\nTo get started, please create an account and grab your API key at financialdatasets.ai.\nYou will use the API key to authenticate your API requests.\n​\nAvailable Tickers\nYou can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/company/facts/tickers/\n​\nGetting Started\nThere are only 3 steps for making a successful API call:\nAdd your API key to the header of the request as X-API-KEY.\nAdd query params like ticker filter the data.\nExecute the API request.\nNote: You must include the ticker in your query params.\n​\nExample\nCompany Facts\nCopy\nimport requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\nticker = 'AAPL'\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/company/facts'\n    f'?ticker={ticker}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse company_facts from the response\ncompany_facts = response.json().get('company_facts')\n\nAuthorizations\n​\nX-API-KEY\nstringheaderrequired\n\nAPI key for authentication.\n\nQuery Parameters\n​\nticker\nstring\n\nThe ticker symbol.\n\n​\ncik\nstring\n\nThe CIK of the company.\n\nResponse\n200\napplication/json\n\nCompany facts response\n\n​\ncompany_facts\nobject\n\nShow child attributes\n\nFacts (by CIK)\nEarnings\nx\ngithub\nPowered by\nThis documentation is built and hosted on Mintlify, a developer documentation platform"
  suggestedFilename: "company_facts_ticker"
---

# Facts (by ticker)

## 源URL

https://docs.financialdatasets.ai/api/company/facts/ticker

## 描述

Get company facts for a ticker.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/company/facts`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 否 | - | The ticker symbol. |
| `cik` | string | 否 | - | The CIK of the company. |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/company/facts \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "company_facts": {
    "ticker": "<string>",
    "name": "<string>",
    "cik": "<string>",
    "industry": "<string>",
    "sector": "<string>",
    "category": "<string>",
    "exchange": "<string>",
    "is_active": true,
    "location": "<string>",
    "sec_filings_url": "<string>",
    "sic_code": "<string>",
    "sic_industry": "<string>",
    "sic_sector": "<string>"
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
    f'https://api.financialdatasets.ai/company/facts'
    f'?ticker={ticker}'
)

# make API request
response = requests.get(url, headers=headers)

# parse company_facts from the response
company_facts = response.json().get('company_facts')
```

## 文档正文

Get company facts for a ticker.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.financialdatasets.ai/company/facts`

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
GET
Facts (by CIK)
GET
Facts (by ticker)
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
Get company facts

cURL

Copy
curl --request GET \
  --url https://api.financialdatasets.ai/company/facts \
  --header 'X-API-KEY: <api-key>'
200
400
401
404
Copy
{
  "company_facts": {
    "ticker": "<string>",
    "name": "<string>",
    "cik": "<string>",
    "industry": "<string>",
    "sector": "<string>",
    "category": "<string>",
    "exchange": "<string>",
    "is_active": true,
    "location": "<string>",
    "sec_filings_url": "<string>",
    "sic_code": "<string>",
    "sic_industry": "<string>",
    "sic_sector": "<string>"
  }
}
Company
Facts (by ticker)

Get company facts for a ticker.

GET
/
company
/
facts
Try it

Overview
Company facts includes data like name, CIK, market cap, total employees, website URL, and more.
The company facts API provides a simple way to access the most important high-level information about a company.
Please note: This API is experimental and free to use.
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.

Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/company/facts/tickers/

Getting Started
There are only 3 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Add query params like ticker filter the data.
Execute the API request.
Note: You must include the ticker in your query params.

Example
Company Facts
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
    f'https://api.financialdatasets.ai/company/facts'
    f'?ticker={ticker}'
)

# make API request
response = requests.get(url, headers=headers)

# parse company_facts from the response
company_facts = response.json().get('company_facts')

Authorizations

X-API-KEY
stringheaderrequired

API key for authentication.

Query Parameters

ticker
string

The ticker symbol.

cik
string

The CIK of the company.

Response
200
application/json

Company facts response

company_facts
object

Show child attributes

Facts (by CIK)
Earnings
x
github
Powered by
This documentation is built and hosted on Mintlify, a developer documentation platform
