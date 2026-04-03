---
id: "url-7022a56b"
type: "api"
title: "ETF List API"
url: "https://eulerpool.com/developers/api/etf/list"
description: "Returns a paginated list of all ETF ISINs available. Maximum results returned is limited to 2000 per request."
source: ""
tags: []
crawl_time: "2026-03-18T05:39:21.013Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/etf/list/{start}/{end}"
  responses:
    - {"code":"200","description":"Returns a paged response of ETF ISINs for the given offsets"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/etf/list/0/10' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"start\": 0,\n  \"size\": 10,\n  \"total\": 19008,\n  \"results\": [\n    \"AEC000730023\",\n    \"AEC000730031\",\n    \"AEC000730049\"\n  ]\n}"
  suggestedFilename: "etf_list"
---

# ETF List API

## 源URL

https://eulerpool.com/developers/api/etf/list

## 描述

Returns a paginated list of all ETF ISINs available. Maximum results returned is limited to 2000 per request.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/etf/list/{start}/{end}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns a paged response of ETF ISINs for the given offsets |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/etf/list/0/10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "start": 0,
  "size": 10,
  "total": 19008,
  "results": [
    "AEC000730023",
    "AEC000730031",
    "AEC000730049"
  ]
}
```

## 文档正文

Returns a paginated list of all ETF ISINs available. Maximum results returned is limited to 2000 per request.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/etf/list/{start}/{end}`
