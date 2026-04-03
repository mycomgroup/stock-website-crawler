# Search Financials

## 源URL

https://docs.financialdatasets.ai/api/financials/search-by-line-items

## 描述

Search for specific financial metrics across income statements, balance sheets, and cash flow statements for a list of tickers.

## 请求端点

**方法**: `GET`

```text
https://api.financialdatasets.ai/financials/search/line-items
```

## 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `X-API-KEY` | string | ✓ | API key for authentication. (Header参数) |

## cURL 示例

### 示例 1

```bash
curl --request POST \
  --url https://api.financialdatasets.ai/financials/search/line-items \
  --header 'Content-Type: application/json' \
  --header 'X-API-KEY: <api-key>' \
  --data '
{
  "line_items": [
    "<string>"
  ],
  "tickers": [
    "<string>"
  ],
  "period": "ttm",
  "limit": 1
}
'
```

### 示例 2

```bash
# List of valid line_items for the income statement
line_items = [
    "consolidated_income",
    "cost_of_revenue",
    "dividends_per_common_share",
    "earnings_per_share",
    "earnings_per_share_diluted",
    "ebit",
    "ebit_usd",
    "earnings_per_share_usd",
    "gross_profit",
    "income_tax_expense",
    "interest_expense",
    "net_income",
    "net_income_common_stock",
    "net_income_common_stock_usd",
    "net_income_discontinued_operations",
    "net_income_non_controlling_interests",
    "operating_expense",
    "operating_income",
    "preferred_dividends_impact",
    "research_and_development",
    "revenue",
    "revenue_usd",
    "selling_general_and_administrative_expenses",
    "weighted_average_shares",
    "weighted_average_shares_diluted",
]
```

## Python 示例

```python
import requests
import json

# Add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here",
    "Content-Type": "application/json"
}

# Prepare the request body
body = {
  "period": "ttm",
  "tickers": ["NVDA", "AAPL"],
  "limit": 1,
  "line_items": [
    "net_income",
    "total_debt"
  ]
}

# Create the URL
url = 'https://api.financialdatasets.ai/financials/search/line-items'

# Make API request
response = requests.post(url, headers=headers, data=json.dumps(body))

# Parse search results, which are ordered by report period, newest to oldest
search_results = response.json().get('search_results')

# Print the results
for result in search_results:
    print(f"Ticker: {result['ticker']}")
    print(f"Report Period: {result['report_period']}")
    print(f"Revenue: ${result['net_income']:,.0f}")
    print(f"Total Debt: ${result['total_debt']:,.0f}")
    print("---")
```

## 响应示例

### 示例 1

```json
{
  "search_results": [
    {
      "ticker": "<string>",
      "report_period": "2023-12-25",
      "period": "annual",
      "currency": "<string>"
    }
  ]
}
```

### 示例 2

```json
{
  "search_results": [
    {
      "ticker": "NVDA",
      "report_period": "2024-07-28",
      "period": "ttm",
      "net_income": 53008000000,
      "total_debt": 9765000000
    },
    {
      "ticker": "AAPL",
      "report_period": "2024-06-29",
      "period": "ttm",
      "net_income": 101956000000,
      "total_debt": 101304000000
    }
  ]
}
```

---

## 详细文档

```
Search specific financial metrics

cURL

curl --request POST \
  --url https://api.financialdatasets.ai/financials/search/line-items \
  --header 'Content-Type: application/json' \
  --header 'X-API-KEY: <api-key>' \
  --data '
{
  "line_items": [
    "<string>"
  ],
  "tickers": [
    "<string>"
  ],
  "period": "ttm",
  "limit": 1
}
'

{
  "search_results": [
    {
      "ticker": "<string>",
      "report_period": "2023-12-25",
      "period": "annual",
      "currency": "<string>"
    }
  ]
}
Search
Search Financials

Search for specific financial metrics across income statements, balance sheets, and cash flow statements for a list of tickers.

POST
/
financials
/
search
/
line-items


Overview
This Line Items Search API lets you pull specific line items for a list of tickers by specifying a set of line_items in your request.
Line items are financial data points that are found in the income statement, balance sheet, and cash flow statement.
Examples of line items are revenue, net income, total debt, free cash flow, and so on.
The purpose of this API is to let you easily get specific data points for a list of tickers in a single API request.
You can also specify a start_date and end_date to filter the line items by a specific date range.
Finally, you can specify a period, which must be one of "ttm", "annual", or "quarterly".
For example, you can search for net_income and total_debt for NVDA and AAPL and receive the following response:
Copy
{
  "search_results": [
    {
      "ticker": "NVDA",
      "report_period": "2024-07-28",
      "period": "ttm",
      "net_income": 53008000000,
      "total_debt": 9765000000
    },
    {
      "ticker": "AAPL",
      "report_period": "2024-06-29",
      "period": "ttm",
      "net_income": 101956000000,
      "total_debt": 101304000000
    }
  ]
}


Available Line Items
Income Statement
Balance Sheet
Cash Flow Statement
Copy
# List of valid line_items for the income statement
line_items = [
    "consolidated_income",
    "cost_of_revenue",
    "dividends_per_common_share",
    "earnings_per_share",
    "earnings_per_share_diluted",
    "ebit",
    "ebit_usd",
    "earnings_per_share_usd",
    "gross_profit",
    "income_tax_expense",
    "interest_expense",
    "net_income",
    "net_income_common_stock",
    "net_income_common_stock_usd",
    "net_income_discontinued_operations",
    "net_income_non_controlling_interests",
    "operating_expense",
    "operating_income",
    "preferred_dividends_impact",
    "research_and_development",
    "revenue",
    "revenue_usd",
    "selling_general_and_administrative_expenses",
    "weighted_average_shares",
    "weighted_average_shares_diluted",
]


Code Example
Financials Search
Copy
import requests
import json

# Add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here",
    "Content-Type": "application/json"
}

# Prepare the request body
body = {
  "period": "ttm",
  "tickers": ["NVDA", "AAPL"],
  "limit": 1,
  "line_items": [
    "net_income",
    "total_debt"
  ]
}

# Create the URL
url = 'https://api.financialdatasets.ai/financials/search/line-items'

# Make API request
response = requests.post(url, headers=headers, data=json.dumps(body))

# Parse search results, which are ordered by report period, newest to oldest
search_results = response.json().get('search_results')

# Print the results
for result in search_results:
    print(f"Ticker: {result['ticker']}")
    print(f"Report Period: {result['report_period']}")
    print(f"Revenue: ${result['net_income']:,.0f}")
    print(f"Total Debt: ${result['total_debt']:,.0f}")
    print("---")

Authorizations

X-API-KEY
stringheaderrequired

API key for authentication.

Body
application/json

line_items
string[]required

An array of line items to apply to the search.

Minimum array length: 1

The financial metric to search for.


tickers
string[]required

An array of tickers to apply to the search.

Minimum array length: 1

The tickers to search for.


period
enum<string>default:ttm

The time period for the financial data.

Available options: annual, quarterly, ttm 

limit
integerdefault:1

The maximum number of results to return.

Required range: x >= 1
Response
200
application/json

Successful search response


search_results
object[]

Hide child attributes


search_results.ticker
string

The ticker symbol of the company.


search_results.report_period
string<date>

The reporting period of the financial data.


search_results.period
enum<string>

The time period of the financial data.

Available options: annual, quarterly, ttm 

search_results.currency
string

The currency of the financial data.


search_results.{key}
string

Additional financial metrics based on the search criteria.

Stock Screener
Filings
```
