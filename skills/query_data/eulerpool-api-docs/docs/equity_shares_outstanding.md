---
id: "url-41f98eac"
type: "api"
title: "Historical Shares Outstanding API"
url: "https://eulerpool.com/developers/api/equity/shares/outstanding"
description: "Returns historical diluted average shares outstanding per fiscal year for the given ISIN. Shows how share count has changed over time due to buybacks, issuances, and stock splits."
source: ""
tags: []
crawl_time: "2026-03-18T06:11:50.333Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/shares-outstanding/{identifier}"
  responses:
    - {"code":"200","description":"Returns historical shares outstanding."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/shares-outstanding/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"year\": \"2024\",\n  \"period\": \"2024-06-30T00:00:00.000Z\",\n  \"sharesOutstanding\": 15460000000,\n  \"dilutedEPS\": 6.13\n}\n]"
  suggestedFilename: "equity_shares_outstanding"
---

# Historical Shares Outstanding API

## 源URL

https://eulerpool.com/developers/api/equity/shares/outstanding

## 描述

Returns historical diluted average shares outstanding per fiscal year for the given ISIN. Shows how share count has changed over time due to buybacks, issuances, and stock splits.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/shares-outstanding/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns historical shares outstanding. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/shares-outstanding/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "year": "2024",
  "period": "2024-06-30T00:00:00.000Z",
  "sharesOutstanding": 15460000000,
  "dilutedEPS": 6.13
}
]
```

## 文档正文

Returns historical diluted average shares outstanding per fiscal year for the given ISIN. Shows how share count has changed over time due to buybacks, issuances, and stock splits.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/shares-outstanding/{identifier}`
