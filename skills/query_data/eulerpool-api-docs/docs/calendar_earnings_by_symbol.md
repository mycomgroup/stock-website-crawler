---
id: "url-5746f566"
type: "api"
title: "Earnings Calendar by Symbol"
url: "https://eulerpool.com/developers/api/calendar/earnings/by/symbol"
description: "Returns upcoming and past earnings dates for a specific company"
source: ""
tags: []
crawl_time: "2026-03-18T06:12:57.737Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/calendar/earnings-by-symbol/{symbol}"
  responses:
    - {"code":"200","description":"Earnings dates for the symbol"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/calendar/earnings-by-symbol/AAPL' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"symbol\": \"AAPL\",\n  \"date\": \"2026-04-30T00:00:00.000Z\",\n  \"epsEstimate\": 0,\n  \"epsActual\": 0,\n  \"revenueEstimate\": 0,\n  \"revenueActual\": 0\n}\n]"
  suggestedFilename: "calendar_earnings_by_symbol"
---

# Earnings Calendar by Symbol

## 源URL

https://eulerpool.com/developers/api/calendar/earnings/by/symbol

## 描述

Returns upcoming and past earnings dates for a specific company

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/calendar/earnings-by-symbol/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Earnings dates for the symbol |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/calendar/earnings-by-symbol/AAPL' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "symbol": "AAPL",
  "date": "2026-04-30T00:00:00.000Z",
  "epsEstimate": 0,
  "epsActual": 0,
  "revenueEstimate": 0,
  "revenueActual": 0
}
]
```

## 文档正文

Returns upcoming and past earnings dates for a specific company

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/calendar/earnings-by-symbol/{symbol}`
