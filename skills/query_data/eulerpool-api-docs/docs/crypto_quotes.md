---
id: "url-37ae23b0"
type: "api"
title: "Crypto Quotes API"
url: "https://eulerpool.com/developers/api/crypto/quotes"
description: "Returns historical price data for the given cryptocurrency. Dates are in milliseconds since 1970."
source: ""
tags: []
crawl_time: "2026-03-18T05:44:43.082Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto/quotes/{identifier}"
  responses:
    - {"code":"200","description":"Returns price history as [timestamp, price] pairs"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Identifier not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto/quotes/BTC?startdate=1704067200000&enddate=1735689600000' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"timestamp\": 1732621245000,\n  \"price\": 42300\n}\n]"
  suggestedFilename: "crypto_quotes"
---

# Crypto Quotes API

## 源URL

https://eulerpool.com/developers/api/crypto/quotes

## 描述

Returns historical price data for the given cryptocurrency. Dates are in milliseconds since 1970.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto/quotes/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns price history as [timestamp, price] pairs |
| 401 | Token not valid |
| 404 | Identifier not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto/quotes/BTC?startdate=1704067200000&enddate=1735689600000' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "timestamp": 1732621245000,
  "price": 42300
}
]
```

## 文档正文

Returns historical price data for the given cryptocurrency. Dates are in milliseconds since 1970.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto/quotes/{identifier}`
