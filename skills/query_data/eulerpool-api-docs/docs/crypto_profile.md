---
id: "url-7de99f0"
type: "api"
title: "Crypto Profile API"
url: "https://eulerpool.com/developers/api/crypto/profile"
description: "Returns profile information for the given cryptocurrency symbol/identifier"
source: ""
tags: []
crawl_time: "2026-03-18T05:47:23.387Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto/profile/{symbol}"
  responses:
    - {"code":"200","description":"Returns crypto profile data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Symbol not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto/profile/bitcoin' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"identifier\": \"BTC\",\n  \"symbol\": \"BTC\",\n  \"name\": \"Bitcoin\",\n  \"description_en\": \"string\",\n  \"marketCap\": 0,\n  \"category\": \"coin\",\n  \"coingecko_rank\": 1,\n  \"genesis_date\": \"2009-01-03T00:00:00.000Z\",\n  \"hashing_algo\": \"SHA-256\"\n}"
  suggestedFilename: "crypto_profile"
---

# Crypto Profile API

## 源URL

https://eulerpool.com/developers/api/crypto/profile

## 描述

Returns profile information for the given cryptocurrency symbol/identifier

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto/profile/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns crypto profile data |
| 401 | Token not valid |
| 404 | Symbol not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto/profile/bitcoin' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "identifier": "BTC",
  "symbol": "BTC",
  "name": "Bitcoin",
  "description_en": "string",
  "marketCap": 0,
  "category": "coin",
  "coingecko_rank": 1,
  "genesis_date": "2009-01-03T00:00:00.000Z",
  "hashing_algo": "SHA-256"
}
```

## 文档正文

Returns profile information for the given cryptocurrency symbol/identifier

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto/profile/{symbol}`
