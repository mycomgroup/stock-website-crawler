---
id: "url-69b298a8"
type: "api"
title: "Superinvestor Holdings API"
url: "https://eulerpool.com/developers/api/alternative/superinvestors/holdings"
description: "Returns the portfolio holdings of a specific superinvestor by slug"
source: ""
tags: []
crawl_time: "2026-03-18T06:16:51.251Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/alternative/superinvestors/holdings/{slug}"
  responses:
    - {"code":"200","description":"Returns investor profile and holdings"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Investor not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/alternative/superinvestors/holdings/warren-buffett-berkshire-hathaway' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"investor\": {},\n  \"holdings\": []\n}"
  suggestedFilename: "alternative_superinvestors_holdings"
---

# Superinvestor Holdings API

## 源URL

https://eulerpool.com/developers/api/alternative/superinvestors/holdings

## 描述

Returns the portfolio holdings of a specific superinvestor by slug

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/alternative/superinvestors/holdings/{slug}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns investor profile and holdings |
| 401 | Token not valid |
| 404 | Investor not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/alternative/superinvestors/holdings/warren-buffett-berkshire-hathaway' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "investor": {},
  "holdings": []
}
```

## 文档正文

Returns the portfolio holdings of a specific superinvestor by slug

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/alternative/superinvestors/holdings/{slug}`
