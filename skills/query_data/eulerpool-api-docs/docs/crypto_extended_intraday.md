---
id: "url-7416801b"
type: "api"
title: "Crypto Intraday Quotes API"
url: "https://eulerpool.com/developers/api/crypto/extended/intraday"
description: "Returns 7-day rolling intraday price ticks for a cryptocurrency. Includes price, volume, market cap, and dominance at each tick."
source: ""
tags: []
crawl_time: "2026-03-18T06:11:15.990Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/intraday/{symbol}"
  responses:
    - {"code":"200","description":"Returns intraday ticks"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Symbol not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/intraday/AAPL' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"timestamp\": 1705276800000,\n  \"price\": 42300,\n  \"volume\": 0,\n  \"market_cap\": 0,\n  \"dominance\": 0\n}\n]"
  suggestedFilename: "crypto_extended_intraday"
---

# Crypto Intraday Quotes API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/intraday

## 描述

Returns 7-day rolling intraday price ticks for a cryptocurrency. Includes price, volume, market cap, and dominance at each tick.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/intraday/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns intraday ticks |
| 401 | Token not valid |
| 404 | Symbol not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/intraday/AAPL' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "timestamp": 1705276800000,
  "price": 42300,
  "volume": 0,
  "market_cap": 0,
  "dominance": 0
}
]
```

## 文档正文

Returns 7-day rolling intraday price ticks for a cryptocurrency. Includes price, volume, market cap, and dominance at each tick.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/intraday/{symbol}`
