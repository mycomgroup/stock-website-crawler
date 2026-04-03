---
id: "url-6ef344df"
type: "api"
title: "DeFi Protocol Stats API"
url: "https://eulerpool.com/developers/api/crypto/extended/defi"
description: "Returns DeFi protocol details by symbol/slug: TVL history, fees/revenue, top yield pools, and protocol metadata. Data sourced from DefiLlama."
source: ""
tags: []
crawl_time: "2026-03-18T06:03:41.593Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/defi/{symbol}"
  responses:
    - {"code":"200","description":"Returns DeFi protocol stats"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Protocol not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/defi/aave' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"protocol\": {},\n  \"tvlHistory\": [],\n  \"fees\": [],\n  \"yields\": []\n}"
  suggestedFilename: "crypto_extended_defi"
---

# DeFi Protocol Stats API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/defi

## 描述

Returns DeFi protocol details by symbol/slug: TVL history, fees/revenue, top yield pools, and protocol metadata. Data sourced from DefiLlama.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/defi/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns DeFi protocol stats |
| 401 | Token not valid |
| 404 | Protocol not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/defi/aave' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "protocol": {},
  "tvlHistory": [],
  "fees": [],
  "yields": []
}
```

## 文档正文

Returns DeFi protocol details by symbol/slug: TVL history, fees/revenue, top yield pools, and protocol metadata. Data sourced from DefiLlama.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/defi/{symbol}`
