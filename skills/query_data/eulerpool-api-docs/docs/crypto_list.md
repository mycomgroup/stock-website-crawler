---
id: "url-4c62ddb7"
type: "api"
title: "Crypto List (Paginated) API"
url: "https://eulerpool.com/developers/api/crypto/list"
description: "Returns a paginated list of all cryptocurrency identifiers. Max 2000 per request."
source: ""
tags: []
crawl_time: "2026-03-18T05:29:21.723Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto/list/{start}/{end}"
  responses:
    - {"code":"200","description":"Returns a paged list of crypto identifiers"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto/list/0/10' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"start\": 0,\n  \"size\": 2000,\n  \"total\": 10000,\n  \"results\": [\n    \"BTC\"\n  ]\n}"
  suggestedFilename: "crypto_list"
---

# Crypto List (Paginated) API

## 源URL

https://eulerpool.com/developers/api/crypto/list

## 描述

Returns a paginated list of all cryptocurrency identifiers. Max 2000 per request.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto/list/{start}/{end}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns a paged list of crypto identifiers |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto/list/0/10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "start": 0,
  "size": 2000,
  "total": 10000,
  "results": [
    "BTC"
  ]
}
```

## 文档正文

Returns a paginated list of all cryptocurrency identifiers. Max 2000 per request.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto/list/{start}/{end}`
