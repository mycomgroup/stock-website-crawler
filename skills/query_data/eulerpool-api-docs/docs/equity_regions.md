---
id: "url-3615cdb6"
type: "api"
title: "Revenue by Region API"
url: "https://eulerpool.com/developers/api/equity/regions"
description: "Returns geographic revenue breakdown for the given ISIN, showing revenue distribution across different countries and regions"
source: ""
tags: []
crawl_time: "2026-03-18T05:48:03.984Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/regions/{identifier}"
  responses:
    - {"code":"200","description":"Returns geographic revenue breakdown."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/regions/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"period\": \"2024-06-30T00:00:00.000Z\",\n  \"unit\": \"u_usd\",\n  \"axis\": \"srt_StatementGeographicalAxis\",\n  \"label\": \"United States\",\n  \"value\": 100280000000,\n  \"percentage\": 40.92,\n  \"member\": \"country_US\",\n  \"symbol\": \"MSFT\"\n}\n]"
  suggestedFilename: "equity_regions"
---

# Revenue by Region API

## 源URL

https://eulerpool.com/developers/api/equity/regions

## 描述

Returns geographic revenue breakdown for the given ISIN, showing revenue distribution across different countries and regions

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/regions/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns geographic revenue breakdown. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/regions/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "period": "2024-06-30T00:00:00.000Z",
  "unit": "u_usd",
  "axis": "srt_StatementGeographicalAxis",
  "label": "United States",
  "value": 100280000000,
  "percentage": 40.92,
  "member": "country_US",
  "symbol": "MSFT"
}
]
```

## 文档正文

Returns geographic revenue breakdown for the given ISIN, showing revenue distribution across different countries and regions

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/regions/{identifier}`
