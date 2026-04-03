---
id: "url-b2cb106"
type: "api"
title: "Stock Ownership API"
url: "https://eulerpool.com/developers/api/equity/ownership"
description: "Returns a list of owners for the given stock isin"
source: ""
tags: []
crawl_time: "2026-03-18T05:31:01.879Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/ownership/{identifier}"
  responses:
    - {"code":"200","description":"Returns a array of ownership data including name, percentage, share count, change since last time, the date where shares had been filed"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/ownership/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"name\": \"Warren Buffett\",\n  \"share\": 50000,\n  \"change\": 1000,\n  \"filingDate\": \"2023-01-01T00:00:00.000Z\",\n  \"symbol\": \"AAPL\",\n  \"percent\": 3\n}\n]"
  suggestedFilename: "equity_ownership"
---

# Stock Ownership API

## 源URL

https://eulerpool.com/developers/api/equity/ownership

## 描述

Returns a list of owners for the given stock isin

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/ownership/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns a array of ownership data including name, percentage, share count, change since last time, the date where shares had been filed |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/ownership/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "name": "Warren Buffett",
  "share": 50000,
  "change": 1000,
  "filingDate": "2023-01-01T00:00:00.000Z",
  "symbol": "AAPL",
  "percent": 3
}
]
```

## 文档正文

Returns a list of owners for the given stock isin

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/ownership/{identifier}`
