---
id: "url-630c61c0"
type: "api"
title: "Earnings Surprises"
url: "https://eulerpool.com/developers/api/calendar/earnings/surprises"
description: "Returns historical earnings surprises (actual vs estimate) for a company"
source: ""
tags: []
crawl_time: "2026-03-18T06:12:33.933Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/calendar/earnings-surprises/{symbol}"
  responses:
    - {"code":"200","description":"Earnings surprise history"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/calendar/earnings-surprises/AAPL' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"symbol\": \"AAPL\",\n  \"date\": \"2026-01-30T00:00:00.000Z\",\n  \"epsEstimate\": 2.1,\n  \"epsActual\": 2.18,\n  \"epsDifference\": 0.08,\n  \"surprisePercent\": 3.81\n}\n]"
  suggestedFilename: "calendar_earnings_surprises"
---

# Earnings Surprises

## 源URL

https://eulerpool.com/developers/api/calendar/earnings/surprises

## 描述

Returns historical earnings surprises (actual vs estimate) for a company

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/calendar/earnings-surprises/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Earnings surprise history |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/calendar/earnings-surprises/AAPL' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "symbol": "AAPL",
  "date": "2026-01-30T00:00:00.000Z",
  "epsEstimate": 2.1,
  "epsActual": 2.18,
  "epsDifference": 0.08,
  "surprisePercent": 3.81
}
]
```

## 文档正文

Returns historical earnings surprises (actual vs estimate) for a company

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/calendar/earnings-surprises/{symbol}`
