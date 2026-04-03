# Earnings

## 源URL

https://docs.financialdatasets.ai/api/earnings/earnings

## 描述

Get the most recent earnings snapshot for a ticker. Optional estimate/surprise and change fields are returned only when available.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/earnings`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The ticker symbol. |
| `earnings` | object | 否 | - | Hide child attributes |

## 响应字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `ticker` | string | The requested ticker symbol. |
| `report_period` | string | <date> |
| `fiscal_period` | string | \| null |
| `currency` | string | \| null |
| `quarterly` | object | Show child attributes |
| `annual` | object | Hide child attributes |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/earnings \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "earnings": {
    "ticker": "<string>",
    "report_period": "2023-12-25",
    "fiscal_period": "<string>",
    "currency": "<string>",
    "quarterly": {
      "fiscal_period": "<string>",
      "currency": "<string>",
      "revenue": 123,
      "estimated_revenue": 123,
      "revenue_surprise": "BEAT",
      "earnings_per_share": 123,
      "estimated_earnings_per_share": 123,
      "eps_surprise": "BEAT",
      "net_income": 123,
      "gross_profit": 123,
      "operating_income": 123,
      "weighted_average_shares": 123,
      "weighted_average_shares_diluted": 123,
      "cash_and_equivalents": 123,
      "total_debt": 123,
      "total_assets": 123,
      "total_liabilities": 123,
      "shareholders_equity": 123,
      "net_cash_flow_from_operations": 123,
      "capital_expenditure": 123,
      "net_cash_flow_from_investing": 123,
      "net_cash_flow_from_financing": 123,
      "change_in_cash_and_equivalents": 123,
      "free_cash_flow": 123,
      "revenue_chg": 123,
      "net_income_chg": 123,
      "operating_income_chg": 123,
      "gross_profit_chg": 123,
      "net_cash_flow_from_operations_chg": 123,
      "net_cash_flow_from_investing_chg": 123,
      "net_cash_flow_from_financing_chg": 123,
      "free_cash_flow_chg": 123
    },
    "annual": {
      "fiscal_period": "<string>",
      "currency": "<string>",
      "revenue": 123,
      "estimated_revenue": 123,
      "revenue_surprise": "BEAT",
      "earnings_per_share": 123,
      "estimated_earnings_per_share": 123,
      "eps_surprise": "BEAT",
      "net_income": 123,
      "gross_profit": 123,
      "operating_income": 123,
      "weighted_average_shares": 123,
      "weighted_average_shares_diluted": 123,
      "cash_and_equivalents": 123,
      "total_debt": 123,
      "total_assets": 123,
      "total_liabilities": 123,
      "shareholders_equity": 123,
      "net_cash_flow_from_operations": 123,
      "capital_expenditure": 123,
      "net_cash_flow_from_investing": 123,
      "net_cash_flow_from_financing": 123,
      "change_in_cash_and_equivalents": 123,
      "free_cash_flow": 123,
      "revenue_chg": 123,
      "net_income_chg": 123,
      "operating_income_chg": 123,
      "gross_profit_chg": 123,
      "net_cash_flow_from_operations_chg": 123,
      "net_cash_flow_from_investing_chg": 123,
      "net_cash_flow_from_financing_chg": 123,
      "free_cash_flow_chg": 123
    }
  }
}
```

### 示例 3 (python)

```python
import requests

headers = {
    "X-API-KEY": "your_api_key_here"
}

ticker = "AAPL"
url = f"https://api.financialdatasets.ai/earnings?ticker={ticker}"

response = requests.get(url, headers=headers)
data = response.json()
earnings = data["earnings"]
```

### 示例 4 (json)

```json
{
  "earnings": {
    "ticker": "AAPL",
    "report_period": "2025-12-31",
    "fiscal_period": "2025-Q4",
    "currency": "USD",
    "quarterly": {
      "revenue": 123456789.0,
      "estimated_revenue": 120000000.0,
      "revenue_surprise": "BEAT",
      "earnings_per_share": 2.18,
      "estimated_earnings_per_share": 2.10,
      "eps_surprise": "BEAT",
      "net_income": 32000000.0,
      "gross_profit": 54000000.0,
      "operating_income": 41000000.0,
      "weighted_average_shares": 15500000.0,
      "weighted_average_shares_diluted": 15600000.0,
      "cash_and_equivalents": 63000000.0,
      "total_debt": 98000000.0,
      "total_assets": 350000000.0,
      "total_liabilities": 290000000.0,
      "shareholders_equity": 60000000.0,
      "net_cash_flow_from_operations": 28000000.0,
      "capital_expenditure": -2500000.0,
      "net_cash_flow_from_investing": -5000000.0,
      "net_cash_flow_from_financing": -12000000.0,
      "change_in_cash_and_equivalents": 11000000.0,
      "free_cash_flow": 25500000.0
    },
    "annual": {
      "revenue": 500000000.0,
      "estimated_revenue": null,
      "revenue_surprise": null,
      "earnings_per_share": 8.75,
      "estimated_earnings_per_share": null,
      "eps_surprise": null,
      "net_income": 120000000.0,
      "gross_profit": 210000000.0,
      "operating_income": 170000000.0,
      "weighted_average_shares": 15600000.0,
      "weighted_average_shares_diluted": 15700000.0,
      "cash_and_equivalents": 63000000.0,
      "total_debt": 98000000.0,
      "total_assets": 350000000.0,
      "total_liabilities": 290000000.0,
      "shareholders_equity": 60000000.0,
      "net_cash_flow_from_operations": 105000000.0,
      "capital_expenditure": -10000000.0,
      "net_cash_flow_from_investing": -25000000.0,
      "net_cash_flow_from_financing": -60000000.0,
      "change_in_cash_and_equivalents": 20000000.0,
      "free_cash_flow": 95000000.0
    }
  }
}
```
