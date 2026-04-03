---
id: "url-3de6eeeb"
type: "api"
title: "Stablecoin Supply History API"
url: "https://eulerpool.com/developers/api/crypto/extended/stablecoin/supply"
description: "Returns granular per-stablecoin circulating supply over time. Stablecoin flows are a leading indicator for crypto market movements."
source: ""
tags: []
crawl_time: "2026-03-18T06:16:38.742Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/stablecoin-supply"
  responses:
    - {"code":"200","description":"Returns stablecoin supply data"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/stablecoin-supply?symbol=USDT' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"symbol\": \"USDT\",\n  \"date\": \"2024-01-15T00:00:00.000Z\",\n  \"circulating\": 95000000000\n}\n]"
  suggestedFilename: "crypto_extended_stablecoin_supply"
---

# Stablecoin Supply History API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/stablecoin/supply

## 描述

Returns granular per-stablecoin circulating supply over time. Stablecoin flows are a leading indicator for crypto market movements.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/stablecoin-supply`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns stablecoin supply data |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/stablecoin-supply?symbol=USDT' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "symbol": "USDT",
  "date": "2024-01-15T00:00:00.000Z",
  "circulating": 95000000000
}
]
```

## 文档正文

Returns granular per-stablecoin circulating supply over time. Stablecoin flows are a leading indicator for crypto market movements.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/stablecoin-supply`
