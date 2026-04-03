---
id: "url-75540e14"
type: "api"
title: "ICE-SWAP data api"
url: "https://eulerpool.com/developers/api/ice/swap"
description: "Returns the ICE-SWAP data for the given code."
source: ""
tags: []
crawl_time: "2026-03-18T05:28:41.132Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/ice-swap/{code}"
  responses:
    - {"code":"200","description":"Returns a array of qoute year combinations for ICE-SWAP data."}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/ice-swap/EUR' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"year\": 1,\n  \"quote\": 2.5\n}\n]"
  suggestedFilename: "ice_swap"
---

# ICE-SWAP data api

## 源URL

https://eulerpool.com/developers/api/ice/swap

## 描述

Returns the ICE-SWAP data for the given code.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/ice-swap/{code}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns a array of qoute year combinations for ICE-SWAP data. |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/ice-swap/EUR' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "year": 1,
  "quote": 2.5
}
]
```

## 文档正文

Returns the ICE-SWAP data for the given code.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/ice-swap/{code}`
