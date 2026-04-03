---
id: "url-3e4e6d5c"
type: "api"
title: "Certificate List API"
url: "https://eulerpool.com/developers/api/certificates/list"
description: "Returns a paginated list of available certificates / structured products"
source: ""
tags: []
crawl_time: "2026-03-18T05:57:41.325Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/certificates/list"
  responses:
    - {"code":"200","description":"Returns certificate list with total count"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/certificates/list?offset=0&limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"data\": [],\n  \"total\": 5432,\n  \"offset\": 0,\n  \"limit\": 50\n}"
  suggestedFilename: "certificates_list"
---

# Certificate List API

## 源URL

https://eulerpool.com/developers/api/certificates/list

## 描述

Returns a paginated list of available certificates / structured products

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/certificates/list`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns certificate list with total count |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/certificates/list?offset=0&limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "data": [],
  "total": 5432,
  "offset": 0,
  "limit": 50
}
```

## 文档正文

Returns a paginated list of available certificates / structured products

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/certificates/list`
