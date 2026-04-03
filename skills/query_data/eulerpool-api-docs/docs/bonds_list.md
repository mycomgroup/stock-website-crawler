---
id: "url-6b4d7352"
type: "api"
title: "Bond List / Search API"
url: "https://eulerpool.com/developers/api/bonds/list"
description: "Returns a list of available bonds. Optionally filter by ISIN prefix, exchange, or description keyword. Paginated."
source: ""
tags: []
crawl_time: "2026-03-18T05:40:20.926Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/bonds/list"
  responses:
    - {"code":"200","description":"Returns bond list"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/bonds/list?q=Apple&exchange=XNAS&offset=0&limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"data\": {\n    \"isin\": \"US912810TD00\",\n    \"figi\": \"string\",\n    \"description\": \"string\",\n    \"exchange\": \"string\"\n  },\n  \"total\": 12345,\n  \"offset\": 0,\n  \"limit\": 50\n}"
  suggestedFilename: "bonds_list"
---

# Bond List / Search API

## 源URL

https://eulerpool.com/developers/api/bonds/list

## 描述

Returns a list of available bonds. Optionally filter by ISIN prefix, exchange, or description keyword. Paginated.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/bonds/list`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns bond list |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/bonds/list?q=Apple&exchange=XNAS&offset=0&limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "data": {
    "isin": "US912810TD00",
    "figi": "string",
    "description": "string",
    "exchange": "string"
  },
  "total": 12345,
  "offset": 0,
  "limit": 50
}
```

## 文档正文

Returns a list of available bonds. Optionally filter by ISIN prefix, exchange, or description keyword. Paginated.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/bonds/list`
