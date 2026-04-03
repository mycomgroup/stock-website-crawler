---
id: "url-5335b902"
type: "api"
title: "Discover Stocks API"
url: "https://eulerpool.com/developers/api/equity/discover"
description: "Returns a curated list of 25 top stocks by market capitalization for discovery and exploration"
source: ""
tags: []
crawl_time: "2026-03-18T05:51:45.493Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/discover"
  responses:
    - {"code":"200","description":"Returns discover stock list."}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/discover' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"name\": \"string\",\n  \"isin\": \"string\",\n  \"ticker\": \"string\",\n  \"currency\": \"string\",\n  \"color\": \"string\",\n  \"route_name\": \"string\"\n}\n]"
  suggestedFilename: "equity_discover"
---

# Discover Stocks API

## 源URL

https://eulerpool.com/developers/api/equity/discover

## 描述

Returns a curated list of 25 top stocks by market capitalization for discovery and exploration

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/discover`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns discover stock list. |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/discover' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "name": "string",
  "isin": "string",
  "ticker": "string",
  "currency": "string",
  "color": "string",
  "route_name": "string"
}
]
```

## 文档正文

Returns a curated list of 25 top stocks by market capitalization for discovery and exploration

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/discover`
