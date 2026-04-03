---
id: "url-2a0539df"
type: "api"
title: "Chain TVL API"
url: "https://eulerpool.com/developers/api/crypto/extended/chain/tvl"
description: "Returns Total Value Locked (TVL) by blockchain over time (Ethereum, Solana, Arbitrum, etc.). Essential for crypto macro analysis."
source: ""
tags: []
crawl_time: "2026-03-18T06:12:03.410Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/chain-tvl"
  responses:
    - {"code":"200","description":"Returns chain TVL data"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/chain-tvl' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"chain\": \"Ethereum\",\n  \"date\": \"2024-01-15T00:00:00.000Z\",\n  \"tvl\": 32000000000\n}\n]"
  suggestedFilename: "crypto_extended_chain_tvl"
---

# Chain TVL API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/chain/tvl

## 描述

Returns Total Value Locked (TVL) by blockchain over time (Ethereum, Solana, Arbitrum, etc.). Essential for crypto macro analysis.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/chain-tvl`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns chain TVL data |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/chain-tvl' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "chain": "Ethereum",
  "date": "2024-01-15T00:00:00.000Z",
  "tvl": 32000000000
}
]
```

## 文档正文

Returns Total Value Locked (TVL) by blockchain over time (Ethereum, Solana, Arbitrum, etc.). Essential for crypto macro analysis.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/chain-tvl`
