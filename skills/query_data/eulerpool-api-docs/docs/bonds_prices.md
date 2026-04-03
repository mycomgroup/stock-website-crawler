---
id: "url-2af4a202"
type: "api"
title: "Bond Prices API"
url: "https://eulerpool.com/developers/api/bonds/prices"
description: "Returns historical price data for the given bond identifier"
source: ""
tags: []
crawl_time: "2026-03-18T05:43:23.316Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/bonds/prices/{identifier}"
  responses:
    - {"code":"200","description":"Returns bond price history"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/bonds/prices/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"date\": \"2024-01-15T00:00:00.000Z\",\n  \"close\": 97.5,\n  \"open\": 97,\n  \"high\": 98,\n  \"low\": 96.5,\n  \"volume\": 50000\n}\n]"
  suggestedFilename: "bonds_prices"
---

# Bond Prices API

## 源URL

https://eulerpool.com/developers/api/bonds/prices

## 描述

Returns historical price data for the given bond identifier

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/bonds/prices/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns bond price history |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/bonds/prices/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "date": "2024-01-15T00:00:00.000Z",
  "close": 97.5,
  "open": 97,
  "high": 98,
  "low": 96.5,
  "volume": 50000
}
]
```

## 文档正文

Returns historical price data for the given bond identifier

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/bonds/prices/{identifier}`
