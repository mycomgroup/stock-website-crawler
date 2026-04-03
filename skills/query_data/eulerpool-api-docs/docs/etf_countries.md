---
id: "url-3a599e07"
type: "api"
title: "ETF Countries API"
url: "https://eulerpool.com/developers/api/etf/countries"
description: "Returns country allocation for the given ETF"
source: ""
tags: []
crawl_time: "2026-03-18T05:45:03.065Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/etf/countries/{identifier}"
  responses:
    - {"code":"200","description":"Returns ETF country allocation"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/etf/countries/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"symbol\": \"SWDA.L\",\n  \"country\": \"United States\",\n  \"exposure\": 72.31035\n}\n]"
  suggestedFilename: "etf_countries"
---

# ETF Countries API

## 源URL

https://eulerpool.com/developers/api/etf/countries

## 描述

Returns country allocation for the given ETF

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/etf/countries/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns ETF country allocation |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/etf/countries/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "symbol": "SWDA.L",
  "country": "United States",
  "exposure": 72.31035
}
]
```

## 文档正文

Returns country allocation for the given ETF

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/etf/countries/{identifier}`
