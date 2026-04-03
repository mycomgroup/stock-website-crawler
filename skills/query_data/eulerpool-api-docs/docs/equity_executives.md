---
id: "url-5c8d30a0"
type: "api"
title: "Company Executives API"
url: "https://eulerpool.com/developers/api/equity/executives"
description: "Returns executive information for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T05:57:21.395Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/executives/{identifier}"
  responses:
    - {"code":"200","description":"Returns executive information."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/executives/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"name\": \"Mr. Satya Nadella\",\n  \"age\": 57,\n  \"compensation\": 79106183,\n  \"currency\": \"USD\",\n  \"position\": \"Chairman of the Board, Chief Executive Officer\",\n  \"sex\": \"male\",\n  \"since\": \"2011\",\n  \"symbol\": \"MSFT\"\n}\n]"
  suggestedFilename: "equity_executives"
---

# Company Executives API

## 源URL

https://eulerpool.com/developers/api/equity/executives

## 描述

Returns executive information for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/executives/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns executive information. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/executives/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "name": "Mr. Satya Nadella",
  "age": 57,
  "compensation": 79106183,
  "currency": "USD",
  "position": "Chairman of the Board, Chief Executive Officer",
  "sex": "male",
  "since": "2011",
  "symbol": "MSFT"
}
]
```

## 文档正文

Returns executive information for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/executives/{identifier}`
