---
id: "url-2fd0b227"
type: "api"
title: "Institutional 13-F Portfolio API"
url: "https://eulerpool.com/developers/api/institutional/portfolio"
description: "Returns the full 13-F portfolio holdings of an institutional investor. Includes all positions with share counts, values, and changes from the latest filing."
source: ""
tags: []
crawl_time: "2026-03-18T06:07:44.538Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/institutional/portfolio/{cik}"
  responses:
    - {"code":"200","description":"Returns 13-F portfolio holdings"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"CIK not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/institutional/portfolio/0001067983' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"cusip\": \"037833100\",\n  \"name\": \"APPLE INC\",\n  \"shares\": 915560382,\n  \"value\": 157258000,\n  \"change\": -10000,\n  \"percentage\": 49.5\n}\n]"
  suggestedFilename: "institutional_portfolio"
---

# Institutional 13-F Portfolio API

## 源URL

https://eulerpool.com/developers/api/institutional/portfolio

## 描述

Returns the full 13-F portfolio holdings of an institutional investor. Includes all positions with share counts, values, and changes from the latest filing.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/institutional/portfolio/{cik}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns 13-F portfolio holdings |
| 401 | Token not valid |
| 404 | CIK not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/institutional/portfolio/0001067983' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "cusip": "037833100",
  "name": "APPLE INC",
  "shares": 915560382,
  "value": 157258000,
  "change": -10000,
  "percentage": 49.5
}
]
```

## 文档正文

Returns the full 13-F portfolio holdings of an institutional investor. Includes all positions with share counts, values, and changes from the latest filing.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/institutional/portfolio/{cik}`
