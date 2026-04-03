# Balance Sheets

## 源URL

https://docs.financialdatasets.ai/api/financials/balance-sheets

## 描述

Get balance sheets for a ticker.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/financials/balance-sheets`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The ticker symbol. |
| `period` | enum | 是 | - | The time period of the balance sheets. |
| `limit` | integer | 否 | - | The maximum number of balance sheets to return |
| `cik` | string | 否 | - | The Central Index Key (CIK) of the company. |
| `report_period` | string | 否 | - | Filter by exact report period date in YYYY-MM-DD format. |
| `report_period_gte` | string | 否 | - | Filter by report period greater than or equal to date in YYYY-MM-DD format. |
| `report_period_lte` | string | 否 | - | Filter by report period less than or equal to date in YYYY-MM-DD format. |
| `report_period_gt` | string | 否 | - | Filter by report period greater than date in YYYY-MM-DD format. |
| `report_period_lt` | string | 否 | - | Filter by report period less than date in YYYY-MM-DD format. |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/financials/balance-sheets \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "balance_sheets": [
    {
      "ticker": "<string>",
      "report_period": "2023-12-25",
      "fiscal_period": "<string>",
      "period": "quarterly",
      "currency": "<string>",
      "accession_number": "<string>",
      "filing_url": "<string>",
      "total_assets": 123,
      "current_assets": 123,
      "cash_and_equivalents": 123,
      "inventory": 123,
      "current_investments": 123,
      "trade_and_non_trade_receivables": 123,
      "non_current_assets": 123,
      "property_plant_and_equipment": 123,
      "goodwill_and_intangible_assets": 123,
      "investments": 123,
      "non_current_investments": 123,
      "outstanding_shares": 123,
      "tax_assets": 123,
      "total_liabilities": 123,
      "current_liabilities": 123,
      "current_debt": 123,
      "trade_and_non_trade_payables": 123,
      "deferred_revenue": 123,
      "deposit_liabilities": 123,
      "non_current_liabilities": 123,
      "non_current_debt": 123,
      "tax_liabilities": 123,
      "shareholders_equity": 123,
      "retained_earnings": 123,
      "accumulated_other_comprehensive_income": 123,
      "total_debt": 123
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
period = 'annual'   # possible values are 'annual', 'quarterly', or 'ttm'
limit = 30          # number of statements to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/financials/balance-sheets'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse balance_sheets from the response
balance_sheets = response.json().get('balance_sheets')
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
GET
Income Statements
GET
Balance Sheets
GET
Cash Flow Statements
GET
All Financial Statements
Insider Trades
News
Institutional Ownership
Interest Rates
Search
SEC Filings
Segmented Financials
Stock Prices
Get balance sheets

cURL

Copy
curl --request GET \
  --url https://api.financialdatasets.ai/financials/balance-sheets \
  --header 'X-API-KEY: <api-key>'
200
400
401
402
404
Copy
{
  "balance_sheets": [
    {
      "ticker": "<string>",
      "report_period": "2023-12-25",
      "fiscal_period": "<string>",
      "period": "quarterly",
      "currency": "<string>",
      "accession_number": "<string>",
      "filing_url": "<string>",
      "total_assets": 123,
      "current_assets": 123,
      "cash_and_equivalents": 123,
      "inventory": 123,
      "current_investments": 123,
      "trade_and_non_trade_receivables": 123,
      "non_current_assets": 123,
      "property_plant_and_equipment": 123,
      "goodwill_and_intangible_assets": 123,
      "investments": 123,
      "non_current_investments": 123,
      "outstanding_shares": 123,
      "tax_assets": 123,
      "total_liabilities": 123,
      "current_liabilities": 123,
      "current_debt": 123,
      "trade_and_non_trade_payables": 123,
      "deferred_revenue": 123,
      "deposit_liabilities": 123,
      "non_current_liabilities": 123,
      "non_current_debt": 123,
      "tax_liabilities": 123,
      "shareholders_equity": 123,
      "retained_earnings": 123,
      "accumulated_other_comprehensive_income": 123,
      "total_debt": 123
    }
  ]
}
Financial Statements
Balance Sheets

Get balance sheets for a ticker.

GET
/
financials
/
balance-sheets
Try it
​
Overview
The balance sheets API provides balance sheet data for a given stock ticker.
Balance sheets are financial statements that summarize a company’s assets, liabilities, and shareholders’ equity at a specific point in time.
You can filter the data by ticker, period, limit, and cik.
The period parameter can be set to annual, quarterly, or ttm (trailing twelve months). The limit parameter is used to specify the number of statements to return.
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.
​
Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/financials/balance-sheets/tickers/
​
Getting Started
There are only 3 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Add query params like ticker, period and limit to filter the data.
Execute the API request.
​
Filtering the Data
You can filter the data by ticker, period, limit, and report_period.
Note: ticker and period are required. Alternatively, you can use cik instead of ticker as a company identifier in your request.
By default, period is annual,limit is 4, and report_period is null.
The period parameter can be set to annual, quarterly, or ttm (trailing twelve months). The limit parameter is used to specify the number of periods to return.
The report_period parameter is used to specify the date of the statement. For example, you can include filters like report_period_lte=2024-09-30 and report_period_gte=2024-01-01 to get statements between January 1, 2024 and September 30, 2024.
The available report_period operations are:
report_period_lte
report_period_lt
report_period_gte
report_period_gt
report_period
​
Example
Balance Sheets
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     # stock ticker
period = 'annual'   # possible values are 'annual', 'quarterly', or 'ttm'
limit = 30          # number of statements to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/financials/balance-sheets'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse balance_sheets from the response
balance_sheets = response.json().get('balance_sheets')

​
Example (with report_period)
Balance Sheets
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'  
period = 'annual'
limit = 100      
report_period_lte = '2024-01-01' # end date
report_period_gte = '2020-01-01' # start date

# create the URL
url = (
    f'https://api.financialdatasets.ai/financials/balance-sheets'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
    f'&report_period_lte={report_period_lte}'
    f'&report_period_gte={report_period_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse balance_sheets 
