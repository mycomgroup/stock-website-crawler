---
id: "url-1f16eb0"
type: "api"
title: "Screener Metadata"
url: "https://eulerpool.com/developers/api/screener/metadata"
description: "Returns available filter dimensions for the stock screener: distinct countries (with stock count), sectors, and industries. Use this to build screener UIs or validate filter parameters."
source: ""
tags: []
crawl_time: "2026-03-18T05:56:41.593Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/screener/metadata"
  responses:
    - {"code":"200","description":"Screener filter metadata"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/screener/metadata' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"countries\": {\n    \"country\": \"US\",\n    \"countryName\": \"United States\",\n    \"continent\": \"North America\",\n    \"count\": 5432\n  },\n  \"sectors\": {\n    \"sector\": \"Technology\",\n    \"count\": 1234\n  },\n  \"industries\": {\n    \"industry\": \"Software\",\n    \"sector\": \"Technology\",\n    \"count\": 456\n  },\n  \"totalStocks\": 45000\n}"
  suggestedFilename: "screener_metadata"
---

# Screener Metadata

## 源URL

https://eulerpool.com/developers/api/screener/metadata

## 描述

Returns available filter dimensions for the stock screener: distinct countries (with stock count), sectors, and industries. Use this to build screener UIs or validate filter parameters.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/screener/metadata`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Screener filter metadata |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/screener/metadata' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "countries": {
    "country": "US",
    "countryName": "United States",
    "continent": "North America",
    "count": 5432
  },
  "sectors": {
    "sector": "Technology",
    "count": 1234
  },
  "industries": {
    "industry": "Software",
    "sector": "Technology",
    "count": 456
  },
  "totalStocks": 45000
}
```

## 文档正文

Returns available filter dimensions for the stock screener: distinct countries (with stock count), sectors, and industries. Use this to build screener UIs or validate filter parameters.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/screener/metadata`
