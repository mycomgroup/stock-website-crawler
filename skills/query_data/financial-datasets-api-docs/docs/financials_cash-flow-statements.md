# Cash Flow Statements

## 源URL

https://docs.financialdatasets.ai/api/financials/cash-flow-statements

## 描述

Get cash flow statements for a ticker.

## 请求端点

**方法**: `GET`

```text
https://api.financialdatasets.ai/financials/cash-flow-statements
```

## 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `X-API-KEY` | string | ✓ | API key for authentication. (Header参数) |
| `ticker` | string | ✓ | The ticker symbol. |
| `period` | enum | ✓ | The time period of the cash flow statements. |
| `limit` | integer | - | The maximum number of cash flow statements to return. |
| `cik` | string | - | The Central Index Key (CIK) of the company. |
| `report_period` | string | - | Filter by exact report period date in YYYY-MM-DD format. |
| `report_period_gte` | string | - | Filter by report period greater than or equal to date in YYYY-MM-DD format. |
| `report_period_lte` | string | - | Filter by report period less than or equal to date in YYYY-MM-DD format. |
| `report_period_gt` | string | - | Filter by report period greater than date in YYYY-MM-DD format. |
| `report_period_lt` | string | - | Filter by report period less than date in YYYY-MM-DD format. |

## cURL 示例

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/financials/cash-flow-statements \
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
    f'https://api.financialdatasets.ai/financials/cash-flow-statements'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse cash_flow_statements from the response
cash_flow_statements = response.json().get('cash_flow_statements')
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
    f'https://api.financialdatasets.ai/financials/cash-flow-statements'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
    f'&report_period_lte={report_period_lte}'
    f'&report_period_gte={report_period_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse cash_flow_statements from the response
cash_flow_statements = response.json().get('cash_flow_statements')
```

## 响应示例

```json
{
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
```

---

## 详细文档

```
Get cash flow statements

cURL

curl --request GET \
  --url https://api.financialdatasets.ai/financials/cash-flow-statements \
  --header 'X-API-KEY: <api-key>'

{
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
Financial Statements
Cash Flow Statements

Get cash flow statements for a ticker.

GET
/
financials
/
cash-flow-statements


Overview
The cash flow statemenet API provides a company’s cash inflows and outflows over a specific period.
Cash flow statements are divided into three sections: operating activities, investing activities, and financing activities.
You can filter the data by ticker, period, limit, and cik.
The period parameter can be set to annual, quarterly, or ttm (trailing twelve months). The limit parameter is used to specify the number of statements to return.
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.

Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/financials/cash-flow-statements/tickers/

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
Cash Flow Statements
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
    f'https://api.financialdatasets.ai/financials/cash-flow-statements'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse cash_flow_statements from the response
cash_flow_statements = response.json().get('cash_flow_statements')


Example (with report_period)
Cash Flow Statements
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
    f'https://api.financialdatasets.ai/financials/cash-flow-statements'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
    f'&report_period_lte={report_period_lte}'
    f'&report_period_gte={report_period_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse cash_flow_statements from the response
cash_flow_statements = response.json().get('cash_flow_statements')

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

The time period of the cash flow statements.

Available options: annual, quarterly, ttm 

limit
integer<int32>

The maximum number of cash flow statements to return.


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

Cash flow statements response


cash_flow_statements
object[]

Hide child attributes


cash_flow_statements.ticker
string

The ticker symbol.


cash_flow_statements.report_period
string<date>

The reporting period of the cash flow statement.


cash_flow_statements.fiscal_period
string

The fiscal period of the cash flow statement.


cash_flow_statements.period
enum<string>

The time period of the cash flow statement.

Available options: quarterly, ttm, annual 

cash_flow_statements.currency
string

The currency in which the financial data is reported.


cash_flow_statements.accession_number
string | null

The SEC accession number of the filing.


cash_flow_statements.filing_url
string<uri> | null

URL to the SEC filing.


cash_flow_statements.net_income
number

The net income of the company.


cash_flow_statements.depreciation_and_amortization
number

The depreciation and amortization of the company.


cash_flow_statements.share_based_compensation
number

The share-based compensation of the company.


cash_flow_statements.net_cash_flow_from_operations
number

The net cash flow from operations of the company.


cash_flow_statements.capital_expenditure
number

The capital expenditure of the company.


cash_flow_statements.business_acquisitions_and_disposals
number

The business acquisitions and disposals of the company.


cash_flow_statements.investment_acquisitions_and_disposals
number

The investment acquisitions and disposals of the company.


cash_flow_statements.net_cash_flow_from_investing
number

The net cash flow from investing of the company.


cash_flow_statements.issuance_or_repayment_of_debt_securities
number

The issuance or repayment of debt securities of the company.


cash_flow_statements.issuance_or_purchase_of_equity_shares
number

The issuance or purchase of equity shares of the company.


cash_flow_statements.dividends_and_other_cash_distributions
number

The dividends and other cash distributions of the company.


cash_flow_statements.net_cash_flow_from_financing
number

The net cash flow from financing of the company.


cash_flow_statements.change_in_cash_and_equivalents
number

The change in cash and equivalents of the company.


cash_flow_statements.effect_of_exchange_rate_changes
number

The effect of exchange rate changes of the company.


cash_flow_statements.ending_cash_balance
number

The ending cash balance of the company.


cash_flow_statements.free_cash_flow
number

The free cash flow of the company.

Balance Sheets
All Financial Statements
```
