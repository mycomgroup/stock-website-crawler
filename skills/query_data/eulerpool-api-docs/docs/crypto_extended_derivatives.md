---
id: "url-4ab06f0f"
type: "api"
title: "Crypto Derivatives API"
url: "https://eulerpool.com/developers/api/crypto/extended/derivatives"
description: "Returns 30-day time series of futures derivatives data: funding rates, open interest, long/short ratios, taker buy/sell volumes, and top trader positions"
source: ""
tags: []
crawl_time: "2026-03-18T06:12:46.500Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/derivatives/{symbol}"
  responses:
    - {"code":"200","description":"Returns derivatives time series"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Symbol not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/derivatives/BTC' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"symbol\": \"BTCUSDT\",\n  \"funding\": [],\n  \"openInterest\": [],\n  \"longShort\": [],\n  \"takerBuySell\": [],\n  \"topTrader\": []\n}"
  suggestedFilename: "crypto_extended_derivatives"
---

# Crypto Derivatives API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/derivatives

## 描述

Returns 30-day time series of futures derivatives data: funding rates, open interest, long/short ratios, taker buy/sell volumes, and top trader positions

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/derivatives/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns derivatives time series |
| 401 | Token not valid |
| 404 | Symbol not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/derivatives/BTC' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "symbol": "BTCUSDT",
  "funding": [],
  "openInterest": [],
  "longShort": [],
  "takerBuySell": [],
  "topTrader": []
}
```

## 文档正文

Returns 30-day time series of futures derivatives data: funding rates, open interest, long/short ratios, taker buy/sell volumes, and top trader positions

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/derivatives/{symbol}`
