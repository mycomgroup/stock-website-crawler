---
id: "url-560656af"
type: "api"
title: "Stock OHLCV Candles API"
url: "https://eulerpool.com/developers/api/equity/candles"
description: "Returns OHLCV-like candle data for a stock. Provides daily price data with open, high, low, close approximated from daily quotes, and volume where available."
source: ""
tags: []
crawl_time: "2026-03-18T05:48:44.047Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/candles/{identifier}"
  responses:
    - {"code":"200","description":"Returns stock candle data."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/candles/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"timestamp\": 1705276800000,\n  \"open\": 178.5,\n  \"high\": 182,\n  \"low\": 177.8,\n  \"close\": 181.2\n}\n]"
  suggestedFilename: "equity_candles"
---

# Stock OHLCV Candles API

## 源URL

https://eulerpool.com/developers/api/equity/candles

## 描述

Returns OHLCV-like candle data for a stock. Provides daily price data with open, high, low, close approximated from daily quotes, and volume where available.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/candles/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns stock candle data. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/candles/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "timestamp": 1705276800000,
  "open": 178.5,
  "high": 182,
  "low": 177.8,
  "close": 181.2
}
]
```

## 文档正文

Returns OHLCV-like candle data for a stock. Provides daily price data with open, high, low, close approximated from daily quotes, and volume where available.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/candles/{identifier}`
