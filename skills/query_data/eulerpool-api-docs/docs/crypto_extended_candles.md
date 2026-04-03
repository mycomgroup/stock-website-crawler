---
id: "url-5d3adfc9"
type: "api"
title: "Crypto OHLCV Candles API"
url: "https://eulerpool.com/developers/api/crypto/extended/candles"
description: "Returns OHLCV candle data from Binance for the given crypto pair. Available intervals: 1h, 4h, 1d, 1w."
source: ""
tags: []
crawl_time: "2026-03-18T06:10:08.077Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/candles/{symbol}"
  responses:
    - {"code":"200","description":"Returns OHLCV candles"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/candles/BTC?interval=1d&limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"open_time\": 1705276800000,\n  \"open\": 42150.5,\n  \"high\": 42500,\n  \"low\": 41900,\n  \"close\": 42300,\n  \"volume\": 15234.5\n}\n]"
  suggestedFilename: "crypto_extended_candles"
---

# Crypto OHLCV Candles API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/candles

## 描述

Returns OHLCV candle data from Binance for the given crypto pair. Available intervals: 1h, 4h, 1d, 1w.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/candles/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns OHLCV candles |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/candles/BTC?interval=1d&limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "open_time": 1705276800000,
  "open": 42150.5,
  "high": 42500,
  "low": 41900,
  "close": 42300,
  "volume": 15234.5
}
]
```

## 文档正文

Returns OHLCV candle data from Binance for the given crypto pair. Available intervals: 1h, 4h, 1d, 1w.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/candles/{symbol}`
