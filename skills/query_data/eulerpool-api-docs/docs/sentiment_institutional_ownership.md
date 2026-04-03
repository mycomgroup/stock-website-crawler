---
id: "url-564da2d2"
type: "api"
title: "Institutional Ownership API"
url: "https://eulerpool.com/developers/api/sentiment/institutional/ownership"
description: "Returns institutional investors holding the given security from 13-F filings"
source: ""
tags: []
crawl_time: "2026-03-18T06:16:01.361Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/sentiment/institutional-ownership/{identifier}"
  responses:
    - {"code":"200","description":"Returns institutional ownership data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/sentiment/institutional-ownership/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"holder_name\": \"BlackRock Institutional Trust Co NA\",\n  \"shares\": 187354850,\n  \"change\": -2500563,\n  \"change_pct\": -1.32,\n  \"value\": 28500000000,\n  \"filing_date\": \"2024-03-31T00:00:00.000Z\"\n}\n]"
  suggestedFilename: "sentiment_institutional_ownership"
---

# Institutional Ownership API

## 源URL

https://eulerpool.com/developers/api/sentiment/institutional/ownership

## 描述

Returns institutional investors holding the given security from 13-F filings

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/sentiment/institutional-ownership/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns institutional ownership data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/sentiment/institutional-ownership/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "holder_name": "BlackRock Institutional Trust Co NA",
  "shares": 187354850,
  "change": -2500563,
  "change_pct": -1.32,
  "value": 28500000000,
  "filing_date": "2024-03-31T00:00:00.000Z"
}
]
```

## 文档正文

Returns institutional investors holding the given security from 13-F filings

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/sentiment/institutional-ownership/{identifier}`
