# Historical

## 源URL

https://docs.financialdatasets.ai/api/financial-metrics/historical

## 描述

Get financial metrics for a ticker, including valuation, profitability, efficiency, liquidity, leverage, growth, and per share metrics.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/financial-metrics`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The ticker symbol of the company. |
| `period` | enum | 是 | - | The time period for the financial data. |
| `limit` | integer | 否 | - | The maximum number of results to return. |
| `report_period` | string | 否 | - | Filter by exact report period date in YYYY-MM-DD format. |
| `report_period_gte` | string | 否 | - | Filter by report period greater than or equal to date in YYYY-MM-DD format. |
| `report_period_lte` | string | 否 | - | Filter by report period less than or equal to date in YYYY-MM-DD format. |
| `report_period_gt` | string | 否 | - | Filter by report period greater than date in YYYY-MM-DD format. |
| `report_period_lt` | string | 否 | - | Filter by report period less than date in YYYY-MM-DD format. |
| `fiscal_period` | string | 否 | - | The fiscal period of the financial metrics. |
| `currency` | string | 否 | - | The currency in which the financial data is reported. |
| `enterprise_value` | number | 否 | - | The total value of the company (market cap + debt - cash). |
| `price_to_earnings_ratio` | number | 否 | - | Price to earnings ratio. |
| `price_to_book_ratio` | number | 否 | - | Price to book ratio. |
| `price_to_sales_ratio` | number | 否 | - | Price to sales ratio. |
| `enterprise_value_to_ebitda_ratio` | number | 否 | - | Enterprise value to EBITDA ratio. |
| `enterprise_value_to_revenue_ratio` | number | 否 | - | Enterprise value to revenue ratio. |
| `free_cash_flow_yield` | number | 否 | - | Free cash flow yield. |
| `peg_ratio` | number | 否 | - | Price to earnings growth ratio. |
| `gross_margin` | number | 否 | - | Gross profit as a percentage of revenue. |
| `operating_margin` | number | 否 | - | Operating income as a percentage of revenue. |
| `net_margin` | number | 否 | - | Net income as a percentage of revenue. |
| `return_on_equity` | number | 否 | - | Net income as a percentage of shareholders' equity. |
| `return_on_assets` | number | 否 | - | Net income as a percentage of total assets. |
| `return_on_invested_capital` | number | 否 | - | Net operating profit after taxes as a percentage of invested capital. |
| `asset_turnover` | number | 否 | - | Revenue divided by average total assets. |
| `inventory_turnover` | number | 否 | - | Cost of goods sold divided by average inventory. |
| `receivables_turnover` | number | 否 | - | Revenue divided by average accounts receivable. |
| `days_sales_outstanding` | number | 否 | - | Average accounts receivable divided by revenue over the period. |
| `operating_cycle` | number | 否 | - | Inventory turnover + receivables turnover. |
| `working_capital_turnover` | number | 否 | - | Revenue divided by average working capital. |
| `current_ratio` | number | 否 | - | Current assets divided by current liabilities. |
| `quick_ratio` | number | 否 | - | Quick assets divided by current liabilities. |
| `cash_ratio` | number | 否 | - | Cash and cash equivalents divided by current liabilities. |
| `operating_cash_flow_ratio` | number | 否 | - | Operating cash flow divided by current liabilities. |
| `debt_to_equity` | number | 否 | - | Total debt divided by shareholders' equity. |
| `debt_to_assets` | number | 否 | - | Total debt divided by total assets. |
| `interest_coverage` | number | 否 | - | EBIT divided by interest expense. |
| `revenue_growth` | number | 否 | - | Year-over-year growth in revenue. |
| `earnings_growth` | number | 否 | - | Year-over-year growth in earnings. |
| `book_value_growth` | number | 否 | - | Year-over-year growth in book value. |
| `earnings_per_share_growth` | number | 否 | - | Growth in earnings per share over the period. |
| `free_cash_flow_growth` | number | 否 | - | Growth in free cash flow over the period. |
| `operating_income_growth` | number | 否 | - | Growth in operating income over the period. |
| `ebitda_growth` | number | 否 | - | Growth in EBITDA over the period. |
| `payout_ratio` | number | 否 | - | Dividends paid as a percentage of net income. |
| `earnings_per_share` | number | 否 | - | Net income divided by weighted average shares outstanding. |
| `book_value_per_share` | number | 否 | - | Shareholders' equity divided by shares outstanding. |
| `free_cash_flow_per_share` | number | 否 | - | Free cash flow divided by shares outstanding. |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/financial-metrics \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "ticker": "<string>",
  "report_period": "2023-12-25",
  "fiscal_period": "<string>",
  "period": "quarterly",
  "currency": "<string>",
  "accession_number": "<string>",
  "filing_url": "<string>",
  "enterprise_value": 123,
  "price_to_earnings_ratio": 123,
  "price_to_book_ratio": 123,
  "price_to_sales_ratio": 123,
  "enterprise_value_to_ebitda_ratio": 123,
  "enterprise_value_to_revenue_ratio": 123,
  "free_cash_flow_yield": 123,
  "peg_ratio": 123,
  "gross_margin": 123,
  "operating_margin": 123,
  "net_margin": 123,
  "return_on_equity": 123,
  "return_on_assets": 123,
  "return_on_invested_capital": 123,
  "asset_turnover": 123,
  "inventory_turnover": 123,
  "receivables_turnover": 123,
  "days_sales_outstanding": 123,
  "operating_cycle": 123,
  "working_capital_turnover": 123,
  "current_ratio": 123,
  "quick_ratio": 123,
  "cash_ratio": 123,
  "operating_cash_flow_ratio": 123,
  "debt_to_equity": 123,
  "debt_to_assets": 123,
  "interest_coverage": 123,
  "revenue_growth": 123,
  "earnings_growth": 123,
  "book_value_growth": 123,
  "earnings_per_share_growth": 123,
  "free_cash_flow_growth": 123,
  "operating_income_growth": 123,
  "ebitda_growth": 123,
  "payout_ratio": 123,
  "earnings_per_share": 123,
  "book_value_per_share": 123,
  "free_cash_flow_per_share": 123
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
limit = 30          # number of periods to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/financial-metrics'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse financial_metrics from the response
financial_metrics = response.json().get('financial_metrics')
```
