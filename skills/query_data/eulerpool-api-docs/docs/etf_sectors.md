---
id: "url-4597ae20"
type: "api"
title: "ETF Sectors API"
url: "https://eulerpool.com/developers/api/etf/sectors"
description: "Returns sector allocation for the given ETF"
source: ""
tags: []
crawl_time: "2026-03-18T05:41:22.797Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/etf/sectors/{identifier}"
  responses:
    - {"code":"200","description":"Returns ETF sector allocation"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/etf/sectors/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"symbol\": \"SWDA.L\",\n  \"industry\": \"Information Technology\",\n  \"exposure\": 26.45\n}\n]"
  suggestedFilename: "etf_sectors"
---

# ETF Sectors API

## 源URL

https://eulerpool.com/developers/api/etf/sectors

## 描述

Returns sector allocation for the given ETF

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/etf/sectors/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns ETF sector allocation |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/etf/sectors/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "symbol": "SWDA.L",
  "industry": "Information Technology",
  "exposure": 26.45
}
]
```

## 文档正文

Returns sector allocation for the given ETF

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/etf/sectors/{identifier}`
