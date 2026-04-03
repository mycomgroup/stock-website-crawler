---
id: "url-c9ab0ef"
type: "api"
title: "Valuation History API"
url: "https://eulerpool.com/developers/api/equity/valuation/history"
description: "Returns historical valuation multiples (P/E, P/S, EV/EBIT) as daily/weekly/monthly time series plus per-year snapshot. Essential for quant models and historical valuation analysis."
source: ""
tags: []
crawl_time: "2026-03-18T06:10:56.178Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/valuation-history/{identifier}"
  responses:
    - {"code":"200","description":"Returns valuation time series"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/valuation-history/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"valuationData\": {\n    \"period\": \"2024\",\n    \"kgv\": \"28.50\",\n    \"kuv\": \"7.20\",\n    \"kev\": \"22.10\"\n  },\n  \"earnings\": {},\n  \"revenue\": {},\n  \"ebit\": {},\n  \"currents\": {}\n}"
  suggestedFilename: "equity_valuation_history"
---

# Valuation History API

## 源URL

https://eulerpool.com/developers/api/equity/valuation/history

## 描述

Returns historical valuation multiples (P/E, P/S, EV/EBIT) as daily/weekly/monthly time series plus per-year snapshot. Essential for quant models and historical valuation analysis.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/valuation-history/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns valuation time series |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/valuation-history/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "valuationData": {
    "period": "2024",
    "kgv": "28.50",
    "kuv": "7.20",
    "kev": "22.10"
  },
  "earnings": {},
  "revenue": {},
  "ebit": {},
  "currents": {}
}
```

## 文档正文

Returns historical valuation multiples (P/E, P/S, EV/EBIT) as daily/weekly/monthly time series plus per-year snapshot. Essential for quant models and historical valuation analysis.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/valuation-history/{identifier}`
