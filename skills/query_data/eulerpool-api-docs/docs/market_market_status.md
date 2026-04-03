---
id: "url-1b0d1067"
type: "api"
title: "Market Status"
url: "https://eulerpool.com/developers/api/market/market/status"
description: "Returns whether major stock exchanges are currently open or closed based on trading hours"
source: ""
tags: []
crawl_time: "2026-03-18T06:03:21.068Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/market-status"
  responses:
    - {"code":"200","description":"Exchange status"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/market-status' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"exchanges\": {\n    \"code\": \"XNYS\",\n    \"name\": \"New York Stock Exchange\",\n    \"country\": \"US\",\n    \"isOpen\": true,\n    \"timezone\": \"America/New_York\",\n    \"localTime\": \"14:30\"\n  },\n  \"timestamp\": 0\n}"
  suggestedFilename: "market_market_status"
---

# Market Status

## 源URL

https://eulerpool.com/developers/api/market/market/status

## 描述

Returns whether major stock exchanges are currently open or closed based on trading hours

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/market-status`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Exchange status |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/market-status' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "exchanges": {
    "code": "XNYS",
    "name": "New York Stock Exchange",
    "country": "US",
    "isOpen": true,
    "timezone": "America/New_York",
    "localTime": "14:30"
  },
  "timestamp": 0
}
```

## 文档正文

Returns whether major stock exchanges are currently open or closed based on trading hours

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/market-status`
