# All Financial Statements

## 源URL

https://docs.financialdatasets.ai/api/financials/all-financial-statements

## 描述

Get all financial statements for a ticker.

## 请求端点

**方法**: `GET`

```text
https://api.financialdatasets.ai/financials
```

## 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `X-API-KEY` | string | ✓ | API key for authentication. (Header参数) |
| `ticker` | string | ✓ | The ticker symbol. |
| `period` | enum | ✓ | The time period of the financial statements. |
| `limit` | integer | - | The maximum number of financial statements to return. |
| `cik` | string | - | The Central Index Key (CIK) of the company. |
| `report_period` | string | - | Filter by exact report period date in YYYY-MM-DD format. |
| `report_period_gte` | string | - | Filter by report period greater than or equal to date in YYYY-MM-DD format. |
| `report_period_lte` | string | - | Filter by report period less than or equal to date in YYYY-MM-DD format. |
| `report_period_gt` | string | - | Filter by report period greater than date in YYYY-MM-DD format. |
| `report_period_lt` | string | - | Filter by report period less than date in YYYY-MM-DD format. |

## 响应字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `get` | - | ('income_statements') |
| `income_statements` | object | [] |
| `balance_sheets` | object | [] |
| `cash_flow_statements` | object | [] |

## cURL 示例

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/financials \
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
ticker = 'NVDA'     # stock ticker
period = 'annual'   # possible values are 'annual', 'quarterly', or 'ttm'
limit = 30          # number of statements to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/financials/'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse financials from the response
financials = response.json().get('financials')

# get income statements
income_statements = financials.get('income_statements')

# get balance sheets
balance_sheets = financials.get('balance_sheets')

# get cash flow statements
cash_flow_statements = financials.get('cash_flow_statements')
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
period = 'annual'
limit = 100 
report_period_lte = '2024-01-01' # end date
report_period_gte = '2020-01-01' # start date

# create the URL
url = (
    f'https://api.financialdatasets.ai/financials/'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
    f'&report_period_lte={report_period_lte}'
    f'&report_period_gte={report_period_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse financials from the response
financials = response.json().get('financials')
```

## 响应示例

```json
{
  "financials": {
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
    ],
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
    ],
    "cash_flow_statements": [
      {
        "ticker": "<string>",
        "report_period": "2023-12-25",
        "fiscal_period": "<string>",
        "period": "quarterly",
        "currency": "<string>",
        "accession_number": "<string>",
        "filing_url": "<string>",
        "net_income": 123,
        "depreciation_and_amortization": 123,
        "share_based_compensation": 123,
        "net_cash_flow_from_operations": 123,
        "capital_expenditure": 123,
        "business_acquisitions_and_disposals": 123,
        "investment_acquisitions_and_disposals": 123,
        "net_cash_flow_from_investing": 123,
        "issuance_or_repayment_of_debt_securities": 123,
        "issuance_or_purchase_of_equity_shares": 123,
        "dividends_and_other_cash_distributions": 123,
        "net_cash_flow_from_financing": 123,
        "change_in_cash_and_equivalents": 123,
        "effect_of_exchange_rate_changes": 123,
        "ending_cash_balance": 123,
        "free_cash_flow": 123
      }
    ]
  }
}
```

---

## 详细文档

```
Get all financial statements

cURL

curl --request GET \
  --url https://api.financialdatasets.ai/financials \
  --header 'X-API-KEY: <api-key>'

{
  "financials": {
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
    ],
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
    ],
    "cash_flow_statements": [
      {
        "ticker": "<string>",
        "report_period": "2023-12-25",
        "fiscal_period": "<string>",
        "period": "quarterly",
        "currency": "<string>",
        "accession_number": "<string>",
        "filing_url": "<string>",
        "net_income": 123,
        "depreciation_and_amortization": 123,
        "share_based_compensation": 123,
        "net_cash_flow_from_operations": 123,
        "capital_expenditure": 123,
        "business_acquisitions_and_disposals": 123,
        "investment_acquisitions_and_disposals": 123,
        "net_cash_flow_from_investing": 123,
        "issuance_or_repayment_of_debt_securities": 123,
        "issuance_or_purchase_of_equity_shares": 123,
        "dividends_and_other_cash_distributions": 123,
        "net_cash_flow_from_financing": 123,
        "change_in_cash_and_equivalents": 123,
        "effect_of_exchange_rate_changes": 123,
        "ending_cash_balance": 123,
        "free_cash_flow": 123
      }
    ]
  }
}
Financial Statements
All Financial Statements

Get all financial statements for a ticker.

GET
/
financials


Overview
This endpoint aggregates all financial statements for a ticker into a single API call.
So, instead of calling 3 endpoints to get income statements, balance sheets, and cash flow statements, you can call this endpoint once and get all financial statements in one go.
The endpoint returns the following financial statements:
Income Statements
Balance Sheets
Cash Flow Statements
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.

Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/financials/tickers/

Getting Started
There are only 3 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Add query params like ticker, period and limit to filter the data.
Execute the API request.

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

Example
All Financial Statements
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
    f'https://api.financialdatasets.ai/financials/'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse financials from the response
financials = response.json().get('financials')

# get income statements
income_statements = financials.get('income_statements')

# get balance sheets
balance_sheets = financials.get('balance_sheets')

# get cash flow statements
cash_flow_statements = financials.get('cash_flow_statements')


Example (with report_period)
All Financial Statements
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
    f'https://api.financialdatasets.ai/financials/'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
    f'&report_period_lte={report_period_lte}'
    f'&report_period_gte={report_period_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse financials from the response
financials = response.json().get('financials')

Authorizations

X-API-KEY
stringheaderrequired

API key for authentication.

Query Parameters

ticker
stringrequired

The ticker symbol.


period
enum<string>required

The time period of the financial statements.

Available options: annual, quarterly, ttm 

limit
integer<int32>

The maximum number of financial statements to return.


cik
string

The Central Index Key (CIK) of the company.


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

Financial statements response


financials
object

Hide child attributes


financials.income_statements
object[]

Show child attributes


financials.balance_shee
... (内容已截断)
```
