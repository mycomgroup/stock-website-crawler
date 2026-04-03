---
id: "url-51093523"
type: "api"
title: "Facts (by CIK)"
url: "https://docs.financialdatasets.ai/api/company/facts/cik"
description: "Get company facts for a ticker."
source: ""
tags: []
crawl_time: "2026-03-18T03:13:26.022Z"
metadata:
  requestMethod: "GET"
  endpoint: "https://api.financialdatasets.ai/company/facts"
  requestParams:
    - {"name":"X-API-KEY","type":"string","required":"是","description":"API key for authentication. (Header参数)"}
    - {"name":"ticker","type":"string","required":"","description":"The ticker symbol."}
    - {"name":"cik","type":"string","required":"","description":"The CIK of the company."}
  responseFields:
    - {"name":"ticker","type":"string","description":"The ticker symbol of the company."}
    - {"name":"name","type":"string","description":"The name of the company."}
    - {"name":"cik","type":"string","description":"The Central Index Key (CIK) of the company."}
    - {"name":"industry","type":"string","description":"The industry of the company."}
    - {"name":"sector","type":"string","description":"The sector of the company."}
    - {"name":"category","type":"string","description":"The category of the company."}
    - {"name":"exchange","type":"string","description":"The exchange of the company."}
    - {"name":"is_active","type":"boolean","description":"Whether the company is currently active."}
    - {"name":"location","type":"string","description":"The location of the company."}
    - {"name":"sec_filings_url","type":"string","description":"<uri>"}
    - {"name":"sic_code","type":"string","description":"The Standard Industrial Classification (SIC) code of the company."}
    - {"name":"sic_industry","type":"string","description":"The industry of the company based on the SIC code."}
    - {"name":"sic_sector","type":"string","description":"The sector of the company based on the SIC code."}
  codeExamples:
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/company/facts \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/company/facts \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"json","code":"{\n  \"company_facts\": {\n    \"ticker\": \"<string>\",\n    \"name\": \"<string>\",\n    \"cik\": \"<string>\",\n    \"industry\": \"<string>\",\n    \"sector\": \"<string>\",\n    \"category\": \"<string>\",\n    \"exchange\": \"<string>\",\n    \"is_active\": true,\n    \"location\": \"<string>\",\n    \"sec_filings_url\": \"<string>\",\n    \"sic_code\": \"<string>\",\n    \"sic_industry\": \"<string>\",\n    \"sic_sector\": \"<string>\"\n  }\n}"}
    - {"language":"json","code":"{\n  \"company_facts\": {\n    \"ticker\": \"<string>\",\n    \"name\": \"<string>\",\n    \"cik\": \"<string>\",\n    \"industry\": \"<string>\",\n    \"sector\": \"<string>\",\n    \"category\": \"<string>\",\n    \"exchange\": \"<string>\",\n    \"is_active\": true,\n    \"location\": \"<string>\",\n    \"sec_filings_url\": \"<string>\",\n    \"sic_code\": \"<string>\",\n    \"sic_industry\": \"<string>\",\n    \"sic_sector\": \"<string>\"\n  }\n}"}
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/company/facts \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/company/facts \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"json","code":"{\n  \"company_facts\": {\n    \"ticker\": \"<string>\",\n    \"name\": \"<string>\",\n    \"cik\": \"<string>\",\n    \"industry\": \"<string>\",\n    \"sector\": \"<string>\",\n    \"category\": \"<string>\",\n    \"exchange\": \"<string>\",\n    \"is_active\": true,\n    \"location\": \"<string>\",\n    \"sec_filings_url\": \"<string>\",\n    \"sic_code\": \"<string>\",\n    \"sic_industry\": \"<string>\",\n    \"sic_sector\": \"<string>\"\n  }\n}"}
    - {"language":"json","code":"{\n  \"company_facts\": {\n    \"ticker\": \"<string>\",\n    \"name\": \"<string>\",\n    \"cik\": \"<string>\",\n    \"industry\": \"<string>\",\n    \"sector\": \"<string>\",\n    \"category\": \"<string>\",\n    \"exchange\": \"<string>\",\n    \"is_active\": true,\n    \"location\": \"<string>\",\n    \"sec_filings_url\": \"<string>\",\n    \"sic_code\": \"<string>\",\n    \"sic_industry\": \"<string>\",\n    \"sic_sector\": \"<string>\"\n  }\n}"}
    - {"language":"python","code":"import requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\ncik = '0000320193'\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/company/facts'\n    f'?cik={cik}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse company_facts from the response\ncompany_facts = response.json().get('company_facts')"}
    - {"language":"python","code":"import requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\ncik = '0000320193'\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/company/facts'\n    f'?cik={cik}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse company_facts from the response\ncompany_facts = response.json().get('company_facts')"}
  rawContent: "Financial Datasets home page\nSearch...\n⌘K\nSupport\nDashboard\nDashboard\nPricing\nDiscord\nOverview\nIntroduction\nData Provenance\nMarket Coverage\nMCP Server\nSupport\nAPIs\nAnalyst Estimates\nCompany\nGET\nFacts (by CIK)\nGET\nFacts (by ticker)\nEarnings\nFinancial Metrics\nFinancial Statements\nInsider Trades\nNews\nInstitutional Ownership\nInterest Rates\nSearch\nSEC Filings\nSegmented Financials\nStock Prices\nGet company facts\n\ncURL\n\nCopy\ncurl --request GET \\\n  --url https://api.financialdatasets.ai/company/facts \\\n  --header 'X-API-KEY: <api-key>'\n200\n400\n401\n404\nCopy\n{\n  \"company_facts\": {\n    \"ticker\": \"<string>\",\n    \"name\": \"<string>\",\n    \"cik\": \"<string>\",\n    \"industry\": \"<string>\",\n    \"sector\": \"<string>\",\n    \"category\": \"<string>\",\n    \"exchange\": \"<string>\",\n    \"is_active\": true,\n    \"location\": \"<string>\",\n    \"sec_filings_url\": \"<string>\",\n    \"sic_code\": \"<string>\",\n    \"sic_industry\": \"<string>\",\n    \"sic_sector\": \"<string>\"\n  }\n}\nCompany\nFacts (by CIK)\n\nGet company facts for a ticker.\n\nGET\n/\ncompany\n/\nfacts\nTry it\n​\nOverview\nCompany facts includes data like name, CIK, market cap, total employees, website URL, and more.\nThe company facts API provides a simple way to access the most important high-level information about a company.\nPlease note: This API is experimental and free to use.\nTo get started, please create an account and grab your API key at financialdatasets.ai.\nYou will use the API key to authenticate your API requests.\n​\nAvailable CIKs\nYou can fetch a list of available CIKs with a GET request to: https://api.financialdatasets.ai/company/facts/ciks/\n​\nGetting Started\nThere are only 3 steps for making a successful API call:\nAdd your API key to the header of the request as X-API-KEY.\nAdd query params like cik filter the data.\nExecute the API request.\nNote: You must include the cik in your query params.\n​\nExample\nCompany Facts\nCopy\nimport requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\ncik = '0000320193'\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/company/facts'\n    f'?cik={cik}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse company_facts from the response\ncompany_facts = response.json().get('company_facts')\n\nAuthorizations\n​\nX-API-KEY\nstringheaderrequired\n\nAPI key for authentication.\n\nQuery Parameters\n​\nticker\nstring\n\nThe ticker symbol.\n\n​\ncik\nstring\n\nThe CIK of the company.\n\nResponse\n200\napplication/json\n\nCompany facts response\n\n​\ncompany_facts\nobject\n\nHide child attributes\n\n​\ncompany_facts.ticker\nstring\n\nThe ticker symbol of the company.\n\n​\ncompany_facts.name\nstring\n\nThe name of the company.\n\n​\ncompany_facts.cik\nstring\n\nThe Central Index Key (CIK) of the company.\n\n​\ncompany_facts.industry\nstring\n\nThe industry of the company.\n\n​\ncompany_facts.sector\nstring\n\nThe sector of the company.\n\n​\ncompany_facts.category\nstring\n\nThe category of the company.\n\n​\ncompany_facts.exchange\nstring\n\nThe exchange of the company.\n\n​\ncompany_facts.is_active\nboolean\n\nWhether the company is currently active.\n\n​\ncompany_facts.location\nstring\n\nThe location of the company.\n\n​\ncompany_facts.sec_filings_url\nstring<uri>\n\nThe URL of the company's SEC filings.\n\n​\ncompany_facts.sic_code\nstring\n\nThe Standard Industrial Classification (SIC) code of the company.\n\n​\ncompany_facts.sic_industry\nstring\n\nThe industry of the company based on the SIC code.\n\n​\ncompany_facts.sic_sector\nstring\n\nThe sector of the company based on the SIC code.\n\nAnalyst Estimates\nFacts (by ticker)\nx\ngithub\nPowered by\nThis documentation is built and hosted on Mintlify, a developer documentation platform"
  suggestedFilename: "company_facts_cik"
---

# Facts (by CIK)

## 源URL

https://docs.financialdatasets.ai/api/company/facts/cik

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

## 响应字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `ticker` | string | The ticker symbol of the company. |
| `name` | string | The name of the company. |
| `cik` | string | The Central Index Key (CIK) of the company. |
| `industry` | string | The industry of the company. |
| `sector` | string | The sector of the company. |
| `category` | string | The category of the company. |
| `exchange` | string | The exchange of the company. |
| `is_active` | boolean | Whether the company is currently active. |
| `location` | string | The location of the company. |
| `sec_filings_url` | string | <uri> |
| `sic_code` | string | The Standard Industrial Classification (SIC) code of the company. |
| `sic_industry` | string | The industry of the company based on the SIC code. |
| `sic_sector` | string | The sector of the company based on the SIC code. |

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
cik = '0000320193'

# create the URL
url = (
    f'https://api.financialdatasets.ai/company/facts'
    f'?cik={cik}'
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
Facts (by CIK)

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

Available CIKs
You can fetch a list of available CIKs with a GET request to: https://api.financialdatasets.ai/company/facts/ciks/

Getting Started
There are only 3 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Add query params like cik filter the data.
Execute the API request.
Note: You must include the cik in your query params.

Example
Company Facts
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
cik = '0000320193'

# create the URL
url = (
    f'https://api.financialdatasets.ai/company/facts'
    f'?cik={cik}'
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

Hide child attributes

company_facts.ticker
string

The ticker symbol of the company.

company_facts.name
string

The name of the company.

company_facts.cik
string

The Central Index Key (CIK) of the company.

company_facts.industry
string

The industry of the company.

company_facts.sector
string

The sector of the company.

company_facts.category
string

The category of the company.

company_facts.exchange
string

The exchange of the company.

company_facts.is_active
boolean

Whether the company is currently active.

company_facts.location
string

The location of the company.

company_facts.sec_filings_url
string<uri>

The URL of the company's SEC filings.

company_facts.sic_code
string

The Standard Industrial Classification (SIC) code of the company.

company_facts.sic_industry
string

The industry of the company based on the SIC code.

company_facts.sic_sector
string

The sector of the company based on the SIC code.

Analyst Estimates
Facts (by ticker)
x
github
Powered by
This documentation is built and hosted on Mintlify, a developer documentation platform
