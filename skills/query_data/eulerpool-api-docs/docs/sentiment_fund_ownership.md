---
id: "url-b7ff35a"
type: "api"
title: "Fund Ownership API"
url: "https://eulerpool.com/developers/api/sentiment/fund/ownership"
description: "Returns mutual fund holders for the given security, including allocation percentages"
source: ""
tags: []
crawl_time: "2026-03-18T06:11:28.575Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/sentiment/fund-ownership/{identifier}"
  responses:
    - {"code":"200","description":"Returns fund ownership data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/sentiment/fund-ownership/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"fund_name\": \"Vanguard Total Stock Market Index Fund\",\n  \"ownership_pct\": 1.88,\n  \"shares\": 5145353,\n  \"change\": 57427,\n  \"filing_date\": \"2024-03-31T00:00:00.000Z\"\n}\n]"
  suggestedFilename: "sentiment_fund_ownership"
---

# Fund Ownership API

## 源URL

https://eulerpool.com/developers/api/sentiment/fund/ownership

## 描述

Returns mutual fund holders for the given security, including allocation percentages

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/sentiment/fund-ownership/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns fund ownership data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/sentiment/fund-ownership/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "fund_name": "Vanguard Total Stock Market Index Fund",
  "ownership_pct": 1.88,
  "shares": 5145353,
  "change": 57427,
  "filing_date": "2024-03-31T00:00:00.000Z"
}
]
```

## 文档正文

Returns mutual fund holders for the given security, including allocation percentages

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/sentiment/fund-ownership/{identifier}`
