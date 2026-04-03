---
id: "url-b763dc6"
type: "api"
title: "Screener Universe"
url: "https://eulerpool.com/developers/api/screener/universe"
description: "Returns available countries and continents for the stock screener"
source: ""
tags: []
crawl_time: "2026-03-18T05:57:01.369Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/screener/universe"
  responses:
    - {"code":"200","description":"Screener universe metadata"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/screener/universe' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"country\": \"US\",\n  \"continent\": \"North America\",\n  \"countryName\": \"United States\"\n}\n]"
  suggestedFilename: "screener_universe"
---

# Screener Universe

## 源URL

https://eulerpool.com/developers/api/screener/universe

## 描述

Returns available countries and continents for the stock screener

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/screener/universe`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Screener universe metadata |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/screener/universe' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "country": "US",
  "continent": "North America",
  "countryName": "United States"
}
]
```

## 文档正文

Returns available countries and continents for the stock screener

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/screener/universe`
