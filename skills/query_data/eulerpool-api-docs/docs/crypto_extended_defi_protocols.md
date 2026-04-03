---
id: "url-5822f093"
type: "api"
title: "DeFi Protocols List API"
url: "https://eulerpool.com/developers/api/crypto/extended/defi/protocols"
description: "Returns top DeFi protocols ranked by TVL with 1d/7d change, category, and chain info"
source: ""
tags: []
crawl_time: "2026-03-18T06:15:03.323Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/defi-protocols"
  responses:
    - {"code":"200","description":"Returns DeFi protocols"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/defi-protocols?limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"slug\": \"lido\",\n  \"name\": \"Lido\",\n  \"symbol\": \"LDO\",\n  \"category\": \"Liquid Staking\",\n  \"chain\": \"Ethereum\",\n  \"tvl\": 14500000000,\n  \"change_1d\": 0,\n  \"change_7d\": 0\n}\n]"
  suggestedFilename: "crypto_extended_defi_protocols"
---

# DeFi Protocols List API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/defi/protocols

## 描述

Returns top DeFi protocols ranked by TVL with 1d/7d change, category, and chain info

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/defi-protocols`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns DeFi protocols |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/defi-protocols?limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "slug": "lido",
  "name": "Lido",
  "symbol": "LDO",
  "category": "Liquid Staking",
  "chain": "Ethereum",
  "tvl": 14500000000,
  "change_1d": 0,
  "change_7d": 0
}
]
```

## 文档正文

Returns top DeFi protocols ranked by TVL with 1d/7d change, category, and chain info

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/defi-protocols`
