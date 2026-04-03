---
id: "url-52012712"
type: "api"
title: "Stock Splits API"
url: "https://eulerpool.com/developers/api/equity/splits"
description: "Returns stock splits history for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T05:45:43.279Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/splits/{identifier}"
  responses:
    - {"code":"200","description":"Returns stock splits data."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/splits/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"date\": \"2003-02-18T00:00:00.000Z\",\n  \"fromFactor\": 1,\n  \"toFactor\": 2\n}\n]"
  suggestedFilename: "equity_splits"
---

# Stock Splits API

## 源URL

https://eulerpool.com/developers/api/equity/splits

## 描述

Returns stock splits history for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/splits/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns stock splits data. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/splits/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "date": "2003-02-18T00:00:00.000Z",
  "fromFactor": 1,
  "toFactor": 2
}
]
```

## 文档正文

Returns stock splits history for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/splits/{identifier}`
