---
id: "url-34332f3e"
type: "api"
title: "Short Interest API"
url: "https://eulerpool.com/developers/api/equity/extended/short/interest"
description: "Returns FINRA short interest data: short shares outstanding, days to cover, and changes"
source: ""
tags: []
crawl_time: "2026-03-18T06:14:48.760Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/short-interest/{identifier}"
  responses:
    - {"code":"200","description":"Returns short interest data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/short-interest/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"settlement_date\": \"2024-01-15T00:00:00.000Z\",\n  \"short_shares\": 12345678,\n  \"prev_short_shares\": 0,\n  \"change_pct\": 3.5,\n  \"days_to_cover\": 1.8\n}\n]"
  suggestedFilename: "equity_extended_short_interest"
---

# Short Interest API

## 源URL

https://eulerpool.com/developers/api/equity/extended/short/interest

## 描述

Returns FINRA short interest data: short shares outstanding, days to cover, and changes

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/short-interest/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns short interest data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/short-interest/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "settlement_date": "2024-01-15T00:00:00.000Z",
  "short_shares": 12345678,
  "prev_short_shares": 0,
  "change_pct": 3.5,
  "days_to_cover": 1.8
}
]
```

## 文档正文

Returns FINRA short interest data: short shares outstanding, days to cover, and changes

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/short-interest/{identifier}`
