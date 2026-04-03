---
id: "url-21d1aacf"
type: "api"
title: "Income Statement API"
url: "https://eulerpool.com/developers/api/equity/incomestatement"
description: "Returns all Income Statement data for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T06:05:43.247Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/incomestatement/{identifier}"
  responses:
    - {"code":"200","description":"Returns a array of incomestatement data."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/incomestatement/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"costOfGoodsSold\": 16,\n  \"depreciationAmortization\": 0,\n  \"diluted_eps\": 0,\n  \"dilutedAverageSharesOutstanding\": 0,\n  \"ebit\": 11,\n  \"gainLossOnDispositionOfAssets\": 0,\n  \"grossIncome\": 34,\n  \"interestIncomeExpense\": 0,\n  \"netIncome\": 6,\n  \"nonRecurringItems\": 0,\n  \"operationsMaintenance\": 0,\n  \"otherOperatingExpensesTotal\": 0,\n  \"otherRevenue\": 0,\n  \"period\": \"1983-06-30T00:00:00.000Z\",\n  \"pretaxIncome\": 11,\n  \"provisionforIncomeTaxes\": 5,\n  \"researchDevelopment\": 7,\n  \"revenue\": 50,\n  \"sgaExpense\": 17,\n  \"shares\": 6532,\n  \"ticker\": \"MSFT\",\n  \"totalOperatingExpense\": 23,\n  \"totalOtherIncomeExpenseNet\": 0\n}\n]"
  suggestedFilename: "equity_incomestatement"
---

# Income Statement API

## 源URL

https://eulerpool.com/developers/api/equity/incomestatement

## 描述

Returns all Income Statement data for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/incomestatement/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns a array of incomestatement data. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/incomestatement/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "costOfGoodsSold": 16,
  "depreciationAmortization": 0,
  "diluted_eps": 0,
  "dilutedAverageSharesOutstanding": 0,
  "ebit": 11,
  "gainLossOnDispositionOfAssets": 0,
  "grossIncome": 34,
  "interestIncomeExpense": 0,
  "netIncome": 6,
  "nonRecurringItems": 0,
  "operationsMaintenance": 0,
  "otherOperatingExpensesTotal": 0,
  "otherRevenue": 0,
  "period": "1983-06-30T00:00:00.000Z",
  "pretaxIncome": 11,
  "provisionforIncomeTaxes": 5,
  "researchDevelopment": 7,
  "revenue": 50,
  "sgaExpense": 17,
  "shares": 6532,
  "ticker": "MSFT",
  "totalOperatingExpense": 23,
  "totalOtherIncomeExpenseNet": 0
}
]
```

## 文档正文

Returns all Income Statement data for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/incomestatement/{identifier}`
