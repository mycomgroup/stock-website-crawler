---
id: "url-321d270c"
type: "api"
title: "Dividend Quality API"
url: "https://eulerpool.com/developers/api/equity/dividend/quality"
description: "Returns dividend quality metrics: consecutive years paid, years not decreased, years increased, current yield, payout frequency, and upcoming ex/pay dates"
source: ""
tags: []
crawl_time: "2026-03-18T06:08:04.553Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/dividend-quality/{identifier}"
  responses:
    - {"code":"200","description":"Returns dividend quality data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/dividend-quality/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"dividend\": 0.96,\n  \"dividendYield\": 0.52,\n  \"yearsPaid\": 12,\n  \"yearsNotDecreased\": 10,\n  \"yearsIncreased\": 10,\n  \"frequency\": \"quarterly\",\n  \"payoutMonths\": [\n    2,\n    5,\n    8,\n    11\n  ],\n  \"lastExDate\": \"2024-11-01T00:00:00.000Z\",\n  \"lastPayDate\": \"2024-11-14T00:00:00.000Z\"\n}"
  suggestedFilename: "equity_dividend_quality"
---

# Dividend Quality API

## 源URL

https://eulerpool.com/developers/api/equity/dividend/quality

## 描述

Returns dividend quality metrics: consecutive years paid, years not decreased, years increased, current yield, payout frequency, and upcoming ex/pay dates

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/dividend-quality/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns dividend quality data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/dividend-quality/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "dividend": 0.96,
  "dividendYield": 0.52,
  "yearsPaid": 12,
  "yearsNotDecreased": 10,
  "yearsIncreased": 10,
  "frequency": "quarterly",
  "payoutMonths": [
    2,
    5,
    8,
    11
  ],
  "lastExDate": "2024-11-01T00:00:00.000Z",
  "lastPayDate": "2024-11-14T00:00:00.000Z"
}
```

## 文档正文

Returns dividend quality metrics: consecutive years paid, years not decreased, years increased, current yield, payout frequency, and upcoming ex/pay dates

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/dividend-quality/{identifier}`
