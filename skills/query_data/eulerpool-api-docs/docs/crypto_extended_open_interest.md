---
id: "url-1eeb27d2"
type: "api"
title: "Crypto Open Interest API"
url: "https://eulerpool.com/developers/api/crypto/extended/open/interest"
description: "Returns open interest time series for Binance perpetual futures. Tracks the total outstanding contracts for the given crypto pair."
source: ""
tags: []
crawl_time: "2026-03-18T06:14:42.980Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/open-interest/{symbol}"
  responses:
    - {"code":"200","description":"Returns open interest time series"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/open-interest/BTC' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"symbol\": \"BTCUSDT\",\n  \"timestamp\": 1705276800000,\n  \"open_interest\": 52345.67\n}\n]"
  suggestedFilename: "crypto_extended_open_interest"
---

# Crypto Open Interest API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/open/interest

## 描述

Returns open interest time series for Binance perpetual futures. Tracks the total outstanding contracts for the given crypto pair.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/open-interest/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns open interest time series |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/open-interest/BTC' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "symbol": "BTCUSDT",
  "timestamp": 1705276800000,
  "open_interest": 52345.67
}
]
```

## 文档正文

Returns open interest time series for Binance perpetual futures. Tracks the total outstanding contracts for the given crypto pair.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/open-interest/{symbol}`
