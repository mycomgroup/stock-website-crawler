---
id: "url-7f30ea6a"
type: "api"
title: "Multi-Exchange Quotes"
url: "https://eulerpool.com/developers/api/market/quotes/exchanges"
description: "Returns real-time quotes from all exchanges where a stock is listed"
source: ""
tags: []
crawl_time: "2026-03-18T06:09:04.348Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/quotes/exchanges/{identifier}"
  responses:
    - {"code":"200","description":"Exchange quotes with primary exchange"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/quotes/exchanges/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"primary\": \"XNAS\",\n  \"exchanges\": {\n    \"exchange\": \"XNAS\",\n    \"currency\": \"USD\",\n    \"bid\": 178.4,\n    \"ask\": 178.45,\n    \"timestamp\": 1709312400\n  }\n}"
  suggestedFilename: "market_quotes_exchanges"
---

# Multi-Exchange Quotes

## 源URL

https://eulerpool.com/developers/api/market/quotes/exchanges

## 描述

Returns real-time quotes from all exchanges where a stock is listed

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/quotes/exchanges/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Exchange quotes with primary exchange |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/quotes/exchanges/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "primary": "XNAS",
  "exchanges": {
    "exchange": "XNAS",
    "currency": "USD",
    "bid": 178.4,
    "ask": 178.45,
    "timestamp": 1709312400
  }
}
```

## 文档正文

Returns real-time quotes from all exchanges where a stock is listed

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/quotes/exchanges/{identifier}`
