---
id: "url-db23b28"
type: "api"
title: "Intraday Quotes"
url: "https://eulerpool.com/developers/api/market/quotes/intraday"
description: "Returns intraday price data for the current/previous trading day"
source: ""
tags: []
crawl_time: "2026-03-18T06:07:04.533Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/quotes/intraday/{identifier}"
  responses:
    - {"code":"200","description":"Intraday quote ticks"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/quotes/intraday/{identifier}?exchange=XNAS' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"exchange\": \"XNAS\",\n  \"currency\": \"USD\",\n  \"price\": 178.42,\n  \"volume\": 1250000,\n  \"timestamp\": \"2026-03-02T14:30:00.000Z\"\n}\n]"
  suggestedFilename: "market_quotes_intraday"
---

# Intraday Quotes

## 源URL

https://eulerpool.com/developers/api/market/quotes/intraday

## 描述

Returns intraday price data for the current/previous trading day

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/quotes/intraday/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Intraday quote ticks |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/quotes/intraday/{identifier}?exchange=XNAS' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "exchange": "XNAS",
  "currency": "USD",
  "price": 178.42,
  "volume": 1250000,
  "timestamp": "2026-03-02T14:30:00.000Z"
}
]
```

## 文档正文

Returns intraday price data for the current/previous trading day

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/quotes/intraday/{identifier}`
