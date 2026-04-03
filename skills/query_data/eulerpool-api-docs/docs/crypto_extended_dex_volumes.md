---
id: "url-52bf4de4"
type: "api"
title: "DEX Volumes API"
url: "https://eulerpool.com/developers/api/crypto/extended/dex/volumes"
description: "Returns daily DEX trading volumes by protocol (Uniswap, dYdX, etc.) for the last 30 days"
source: ""
tags: []
crawl_time: "2026-03-18T06:13:28.477Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/dex-volumes"
  responses:
    - {"code":"200","description":"Returns DEX volumes"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/dex-volumes' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"protocol\": \"uniswap\",\n  \"chain\": \"Ethereum\",\n  \"date\": \"2024-01-15T00:00:00.000Z\",\n  \"volume\": 1500000000\n}\n]"
  suggestedFilename: "crypto_extended_dex_volumes"
---

# DEX Volumes API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/dex/volumes

## 描述

Returns daily DEX trading volumes by protocol (Uniswap, dYdX, etc.) for the last 30 days

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/dex-volumes`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns DEX volumes |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/dex-volumes' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "protocol": "uniswap",
  "chain": "Ethereum",
  "date": "2024-01-15T00:00:00.000Z",
  "volume": 1500000000
}
]
```

## 文档正文

Returns daily DEX trading volumes by protocol (Uniswap, dYdX, etc.) for the last 30 days

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/dex-volumes`
