---
id: "url-3a2f0f5b"
type: "api"
title: "Earnings Calendar (Weekly)"
url: "https://eulerpool.com/developers/api/calendar/earnings"
description: "Returns all earnings reports for the week containing the given date"
source: ""
tags: []
crawl_time: "2026-03-18T05:56:21.915Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/calendar/earnings/{date}"
  responses:
    - {"code":"200","description":"Earnings reports for the week"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/calendar/earnings/2026-01-30' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"symbol\": \"AAPL\",\n  \"name\": \"Apple\",\n  \"isin\": \"US0378331005\",\n  \"date\": \"2026-03-05T00:00:00.000Z\",\n  \"epsEstimate\": 0,\n  \"revenueEstimate\": 0,\n  \"time\": \"bmo\"\n}\n]"
  suggestedFilename: "calendar_earnings"
---

# Earnings Calendar (Weekly)

## 源URL

https://eulerpool.com/developers/api/calendar/earnings

## 描述

Returns all earnings reports for the week containing the given date

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/calendar/earnings/{date}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Earnings reports for the week |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/calendar/earnings/2026-01-30' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "symbol": "AAPL",
  "name": "Apple",
  "isin": "US0378331005",
  "date": "2026-03-05T00:00:00.000Z",
  "epsEstimate": 0,
  "revenueEstimate": 0,
  "time": "bmo"
}
]
```

## 文档正文

Returns all earnings reports for the week containing the given date

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/calendar/earnings/{date}`
