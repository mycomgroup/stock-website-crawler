# Stock Screener

## 源URL

https://docs.financialdatasets.ai/api/financials/search-screener

## 描述

Search for stocks by filtering across financial metrics from income statements, balance sheets, and cash flow statements.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/financials/search/screener`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |

## 代码示例

### 示例 1 (bash)

```bash
curl --request POST \
  --url https://api.financialdatasets.ai/financials/search/screener \
  --header 'Content-Type: application/json' \
  --header 'X-API-KEY: <api-key>' \
  --data '
{
  "filters": [
    {
      "field": "<string>",
      "operator": "gt",
      "value": 123
    }
  ],
  "limit": 10
}
'
```

### 示例 2 (json)

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

### 示例 3 (text)

```text
// Send JSON Request
{
  "filters": [
    {
      "field": "revenue",
      "operator": "gt",
      "value": 100000000
    },
    {
      "field": "pe_ratio",
      "operator": "lt",
      "value": 20
    }
  ]
}
```

### 示例 4 (text)

```text
// Receive JSON Response
{
  "results": [
    {
      "ticker": "AA",
      "pe_ratio": 8.37,
      "report_period": "2025-09-30",
      "currency": "USD",
      "revenue": 12868000000.0
    },
    {
      "ticker": "AAL",
      "pe_ratio": 14.65,
      "report_period": "2025-09-30",
      "currency": "USD",
      "revenue": 54294000000.0
    }
  ]
}
```

### 示例 5 (text)

```text
# List of valid filter fields for the income statement
fields = [
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

### 示例 6 (python)

```python
import requests
import json

headers = {
    "X-API-KEY": "your_api_key_here",
    "Content-Type": "application/json"
}

body = {
    "limit": 5,
    "currency": "USD",
    "filters": [
        {
            "field": "pe_ratio",      # from financial metrics
            "operator": "lt",
            "value": 20
        },
        {
            "field": "revenue",       # from income statement
            "operator": "gte",
            "value": 1000000000
        },
        {
            "field": "total_debt",    # from balance sheet
            "operator": "lt",
            "value": 500000000
        },
    ]
}

url = 'https://api.financialdatasets.ai/financials/search/screener'
response = requests.post(url, headers=headers, data=json.dumps(body))

results = response.json().get('results')

for result in results:
    print(f"Ticker: {result['ticker']}")
    print(f"P/E Ratio: {result.get('pe_ratio')}")
    print(f"Revenue: {result.get('revenue')}")
    print(f"Total Debt: {result.get('total_debt')}")
    print("---")
```
