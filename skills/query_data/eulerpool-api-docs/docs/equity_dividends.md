---
id: "url-6b343e11"
type: "api"
title: "Dividends API"
url: "https://eulerpool.com/developers/api/equity/dividends"
description: "Returns individual dividend payments for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T05:54:43.387Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/dividends/{identifier}"
  responses:
    - {"code":"200","description":"Returns dividend payments."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/dividends/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"payDate\": \"2003-03-07T00:00:00.000Z\",\n  \"period\": \"2003-03-07T00:00:00.000Z\",\n  \"dividend\": 0.08\n}\n]"
  suggestedFilename: "equity_dividends"
---

# Dividends API

## 源URL

https://eulerpool.com/developers/api/equity/dividends

## 描述

Returns individual dividend payments for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/dividends/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns dividend payments. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/dividends/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "payDate": "2003-03-07T00:00:00.000Z",
  "period": "2003-03-07T00:00:00.000Z",
  "dividend": 0.08
}
]
```

## 文档正文

Returns individual dividend payments for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/dividends/{identifier}`
