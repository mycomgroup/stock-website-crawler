---
id: "url-5b081f3e"
type: "api"
title: "Binance Symbol Map API"
url: "https://eulerpool.com/developers/api/crypto/extended/symbol/map"
description: "Returns the mapping between Binance trading pair symbols and internal crypto identifiers. Useful for resolving which pairs are available and their trading status."
source: ""
tags: []
crawl_time: "2026-03-18T06:12:22.466Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/symbol-map"
  responses:
    - {"code":"200","description":"Returns symbol mappings"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/symbol-map' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"binance_symbol\": \"BTCUSDT\",\n  \"base_asset\": \"BTC\",\n  \"quote_asset\": \"USDT\",\n  \"identifier\": \"BTC\",\n  \"status\": \"TRADING\"\n}\n]"
  suggestedFilename: "crypto_extended_symbol_map"
---

# Binance Symbol Map API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/symbol/map

## 描述

Returns the mapping between Binance trading pair symbols and internal crypto identifiers. Useful for resolving which pairs are available and their trading status.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/symbol-map`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns symbol mappings |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/symbol-map' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "binance_symbol": "BTCUSDT",
  "base_asset": "BTC",
  "quote_asset": "USDT",
  "identifier": "BTC",
  "status": "TRADING"
}
]
```

## 文档正文

Returns the mapping between Binance trading pair symbols and internal crypto identifiers. Useful for resolving which pairs are available and their trading status.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/symbol-map`
