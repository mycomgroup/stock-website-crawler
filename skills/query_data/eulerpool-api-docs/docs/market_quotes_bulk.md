---
id: "url-758ac594"
type: "api"
title: "Bulk Quotes"
url: "https://eulerpool.com/developers/api/market/quotes/bulk"
description: "Returns the latest quote for multiple ISINs in a single request (max 50)"
source: ""
tags: []
crawl_time: "2026-03-18T06:00:40.331Z"
metadata:
  requestMethod: "POST"
  endpoint: "/api/1/market/quotes/bulk"
  responses:
    - {"code":"200","description":"Latest quotes for requested ISINs"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X POST \\\n  'https://api.eulerpool.com/api/1/market/quotes/bulk' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"quotes\": {\n    \"isin\": \"US0378331005\",\n    \"ticker\": \"AAPL\",\n    \"name\": \"Apple Inc\",\n    \"price\": 178.72,\n    \"currency\": \"USD\",\n    \"timestamp\": 1709312400000,\n    \"change\": 2.15,\n    \"changePct\": 1.22\n  },\n  \"errors\": {\n    \"isin\": \"string\",\n    \"error\": \"string\"\n  }\n}"
  suggestedFilename: "market_quotes_bulk"
---

# Bulk Quotes

## 源URL

https://eulerpool.com/developers/api/market/quotes/bulk

## 描述

Returns the latest quote for multiple ISINs in a single request (max 50)

## API 端点

**Method**: `POST`
**Endpoint**: `/api/1/market/quotes/bulk`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Latest quotes for requested ISINs |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X POST \
  'https://api.eulerpool.com/api/1/market/quotes/bulk' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "quotes": {
    "isin": "US0378331005",
    "ticker": "AAPL",
    "name": "Apple Inc",
    "price": 178.72,
    "currency": "USD",
    "timestamp": 1709312400000,
    "change": 2.15,
    "changePct": 1.22
  },
  "errors": {
    "isin": "string",
    "error": "string"
  }
}
```

## 文档正文

Returns the latest quote for multiple ISINs in a single request (max 50)

## API 端点

**Method:** `POST`
**Endpoint:** `/api/1/market/quotes/bulk`
