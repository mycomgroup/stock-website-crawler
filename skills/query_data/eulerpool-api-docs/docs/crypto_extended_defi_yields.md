---
id: "url-2c07decc"
type: "api"
title: "DeFi Yields API"
url: "https://eulerpool.com/developers/api/crypto/extended/defi/yields"
description: "Returns top DeFi yield farming opportunities across all protocols and chains, ranked by APY"
source: ""
tags: []
crawl_time: "2026-03-18T06:13:21.950Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/defi-yields"
  responses:
    - {"code":"200","description":"Returns DeFi yields"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/defi-yields?limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"pool_id\": \"string\",\n  \"chain\": \"Ethereum\",\n  \"project\": \"aave-v3\",\n  \"symbol\": \"USDC\",\n  \"tvl_usd\": 0,\n  \"apy\": 5.23,\n  \"apy_base\": 0,\n  \"apy_reward\": 0,\n  \"stable_coin\": false\n}\n]"
  suggestedFilename: "crypto_extended_defi_yields"
---

# DeFi Yields API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/defi/yields

## 描述

Returns top DeFi yield farming opportunities across all protocols and chains, ranked by APY

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/defi-yields`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns DeFi yields |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/defi-yields?limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "pool_id": "string",
  "chain": "Ethereum",
  "project": "aave-v3",
  "symbol": "USDC",
  "tvl_usd": 0,
  "apy": 5.23,
  "apy_base": 0,
  "apy_reward": 0,
  "stable_coin": false
}
]
```

## 文档正文

Returns top DeFi yield farming opportunities across all protocols and chains, ranked by APY

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/defi-yields`
