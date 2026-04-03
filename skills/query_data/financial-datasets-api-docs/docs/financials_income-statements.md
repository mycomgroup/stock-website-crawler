# Income Statements

## 源URL

https://docs.financialdatasets.ai/api/financials/income-statements

## 描述

Get income statements for a ticker.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/financials/income-statements`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The ticker symbol. |
| `period` | enum | 是 | - | The time period of the income statements. |
| `limit` | integer | 否 | - | The maximum number of income statements to return. |
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
  --url https://api.financialdatasets.ai/financials/income-statements \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "income_statements": [
    {
      "ticker": "<string>",
      "report_period": "2023-12-25",
      "fiscal_period": "<string>",
      "period": "quarterly",
      "currency": "<string>",
      "accession_number": "<string>",
      "filing_url": "<string>",
      "revenue": 123,
      "cost_of_revenue": 123,
      "gross_profit": 123,
      "operating_expense": 123,
      "selling_general_and_administrative_expenses": 123,
      "research_and_development": 123,
      "operating_income": 123,
      "interest_expense": 123,
      "ebit": 123,
      "income_tax_expense": 123,
      "net_income_discontinued_operations": 123,
      "net_income_non_controlling_interests": 123,
      "net_income": 123,
      "net_income_common_stock": 123,
      "preferred_dividends_impact": 123,
      "consolidated_income": 123,
      "earnings_per_share": 123,
      "earnings_per_share_diluted": 123,
      "dividends_per_common_share": 123,
      "weighted_average_shares": 123,
      "weighted_average_shares_diluted": 123
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
    f'https://api.financialdatasets.ai/financials/income-statements'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse income_statements from the response
income_statements = response.json().get('income_statements')
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
Get income statements

cURL

Copy
curl --request GET \
  --url https://api.financialdatasets.ai/financials/income-statements \
  --header 'X-API-KEY: <api-key>'
200
400
401
402
404
Copy
{
  "income_statements": [
    {
      "ticker": "<string>",
      "report_period": "2023-12-25",
      "fiscal_period": "<string>",
      "period": "quarterly",
      "currency": "<string>",
      "accession_number": "<string>",
      "filing_url": "<string>",
      "revenue": 123,
      "cost_of_revenue": 123,
      "gross_profit": 123,
      "operating_expense": 123,
      "selling_general_and_administrative_expenses": 123,
      "research_and_development": 123,
      "operating_income": 123,
      "interest_expense": 123,
      "ebit": 123,
      "income_tax_expense": 123,
      "net_income_discontinued_operations": 123,
      "net_income_non_controlling_interests": 123,
      "net_income": 123,
      "net_income_common_stock": 123,
      "preferred_dividends_impact": 123,
      "consolidated_income": 123,
      "earnings_per_share": 123,
      "earnings_per_share_diluted": 123,
      "dividends_per_common_share": 123,
      "weighted_average_shares": 123,
      "weighted_average_shares_diluted": 123
    }
  ]
}
Financial Statements
Income Statements

Get income statements for a ticker.

GET
/
financials
/
income-statements
Try it
​
Overview
The income statements API provides income statements for a given stock ticker.
Income statements are financial statements that provide information about a company’s revenues, expenses, and profits over a specific period.
You can filter the data by ticker, period, limit, and cik.
The period parameter can be set to annual, quarterly, or ttm (trailing twelve months). The limit parameter is used to specify the number of statements to return.
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.
​
Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/financials/income-statements/tickers/
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
Income Statements
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
    f'https://api.financialdatasets.ai/financials/income-statements'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse income_statements from the response
income_statements = response.json().get('income_statements')

​
Example (with report_period)
Income Statements
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
    f'https://api.financialdatasets.ai/financials/income-statements'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
    f'&report_period_lte={report_period_lte}'
    f'&report_period_gte={report_period_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse income_statements from the response
income_statements = response.json().get('income_statement
