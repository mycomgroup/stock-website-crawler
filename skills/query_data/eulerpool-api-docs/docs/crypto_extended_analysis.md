---
id: "url-14579a79"
type: "api"
title: "Crypto Analysis Summary API"
url: "https://eulerpool.com/developers/api/crypto/extended/analysis"
description: "Returns a comprehensive analysis for a crypto pair: technical indicators (RSI, MACD, SMA, EMA, Bollinger Bands), BTC correlation, and derivatives data (funding rate, open interest, long/short ratios)"
source: ""
tags: []
crawl_time: "2026-03-18T06:11:10.189Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/analysis/{symbol}"
  responses:
    - {"code":"200","description":"Returns analysis data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Symbol not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/analysis/BTC' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"symbol\": \"BTCUSDT\",\n  \"technical\": {},\n  \"correlation\": {},\n  \"derivatives\": {}\n}"
  suggestedFilename: "crypto_extended_analysis"
---

# Crypto Analysis Summary API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/analysis

## 描述

Returns a comprehensive analysis for a crypto pair: technical indicators (RSI, MACD, SMA, EMA, Bollinger Bands), BTC correlation, and derivatives data (funding rate, open interest, long/short ratios)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/analysis/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns analysis data |
| 401 | Token not valid |
| 404 | Symbol not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/analysis/BTC' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "symbol": "BTCUSDT",
  "technical": {},
  "correlation": {},
  "derivatives": {}
}
```

## 文档正文

Returns a comprehensive analysis for a crypto pair: technical indicators (RSI, MACD, SMA, EMA, Bollinger Bands), BTC correlation, and derivatives data (funding rate, open interest, long/short ratios)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/analysis/{symbol}`
