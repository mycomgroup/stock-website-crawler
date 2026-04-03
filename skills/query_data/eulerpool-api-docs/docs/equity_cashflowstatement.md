---
id: "url-2e88439"
type: "api"
title: "Cash Flow Statement API"
url: "https://eulerpool.com/developers/api/equity/cashflowstatement"
description: "Returns all Cash Flow Statement data for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T06:10:48.085Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/cashflowstatement/{identifier}"
  responses:
    - {"code":"200","description":"Returns a array of cashflowstatement data."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/cashflowstatement/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"ticker\": \"MSFT\",\n  \"period\": \"1987-06-30T00:00:00.000Z\",\n  \"netIncomeStartingLine\": 72,\n  \"amortization\": 8,\n  \"deferredTaxesInvestmentTaxCredit\": 0,\n  \"changesinWorkingCapital\": -20,\n  \"nonCashItems\": 0,\n  \"cashInterestPaid\": 1,\n  \"cashTaxesPaid\": 32,\n  \"netOperatingCashFlow\": 59,\n  \"capex\": -58,\n  \"netInvestingCashFlow\": -101,\n  \"otherInvestingCashFlowItemsTotal\": -44,\n  \"issuanceReductionDebtNet\": 3,\n  \"issuanceReductionCapitalStock\": 2,\n  \"otherFundsFinancingItems\": 24,\n  \"cashDividendsPaid\": 0,\n  \"netCashFinancingActivities\": 29,\n  \"cashNet\": -13,\n  \"foreignExchangeEffects\": 0,\n  \"fcf\": 1,\n  \"year\": 1987,\n  \"changeinCash\": 0\n}\n]"
  suggestedFilename: "equity_cashflowstatement"
---

# Cash Flow Statement API

## 源URL

https://eulerpool.com/developers/api/equity/cashflowstatement

## 描述

Returns all Cash Flow Statement data for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/cashflowstatement/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns a array of cashflowstatement data. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/cashflowstatement/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "ticker": "MSFT",
  "period": "1987-06-30T00:00:00.000Z",
  "netIncomeStartingLine": 72,
  "amortization": 8,
  "deferredTaxesInvestmentTaxCredit": 0,
  "changesinWorkingCapital": -20,
  "nonCashItems": 0,
  "cashInterestPaid": 1,
  "cashTaxesPaid": 32,
  "netOperatingCashFlow": 59,
  "capex": -58,
  "netInvestingCashFlow": -101,
  "otherInvestingCashFlowItemsTotal": -44,
  "issuanceReductionDebtNet": 3,
  "issuanceReductionCapitalStock": 2,
  "otherFundsFinancingItems": 24,
  "cashDividendsPaid": 0,
  "netCashFinancingActivities": 29,
  "cashNet": -13,
  "foreignExchangeEffects": 0,
  "fcf": 1,
  "year": 1987,
  "changeinCash": 0
}
]
```

## 文档正文

Returns all Cash Flow Statement data for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/cashflowstatement/{identifier}`
