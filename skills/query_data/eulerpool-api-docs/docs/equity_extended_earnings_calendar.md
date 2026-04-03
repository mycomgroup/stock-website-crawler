---
id: "url-7b5c099d"
type: "api"
title: "Earnings Calendar API"
url: "https://eulerpool.com/developers/api/equity/extended/earnings/calendar"
description: "Returns upcoming and historical earnings dates with EPS actual/estimate and surprises"
source: ""
tags: []
crawl_time: "2026-03-18T06:16:26.513Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/earnings-calendar/{identifier}"
  responses:
    - {"code":"200","description":"Returns earnings calendar data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/earnings-calendar/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"date\": \"2024-01-25T00:00:00.000Z\",\n  \"epsActual\": 2.18,\n  \"epsEstimate\": 2.1,\n  \"revenueActual\": 119580000000,\n  \"revenueEstimate\": 118260000000,\n  \"quarter\": 1,\n  \"year\": 2024\n}\n]"
  suggestedFilename: "equity_extended_earnings_calendar"
---

# Earnings Calendar API

## 源URL

https://eulerpool.com/developers/api/equity/extended/earnings/calendar

## 描述

Returns upcoming and historical earnings dates with EPS actual/estimate and surprises

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/earnings-calendar/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns earnings calendar data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/earnings-calendar/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "date": "2024-01-25T00:00:00.000Z",
  "epsActual": 2.18,
  "epsEstimate": 2.1,
  "revenueActual": 119580000000,
  "revenueEstimate": 118260000000,
  "quarter": 1,
  "year": 2024
}
]
```

## 文档正文

Returns upcoming and historical earnings dates with EPS actual/estimate and surprises

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/earnings-calendar/{identifier}`
