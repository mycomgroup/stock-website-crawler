---
id: "url-43035b0"
type: "api"
title: "Company Peers API"
url: "https://eulerpool.com/developers/api/equity/extended/peers"
description: "Returns a list of peer/comparable company symbols for the given security"
source: ""
tags: []
crawl_time: "2026-03-18T06:05:03.090Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/peers/{identifier}"
  responses:
    - {"code":"200","description":"Returns peer symbols"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/peers/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"symbol\": \"AAPL\",\n  \"peers\": [\n    \"MSFT\",\n    \"GOOG\",\n    \"META\"\n  ]\n}"
  suggestedFilename: "equity_extended_peers"
---

# Company Peers API

## 源URL

https://eulerpool.com/developers/api/equity/extended/peers

## 描述

Returns a list of peer/comparable company symbols for the given security

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/peers/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns peer symbols |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/peers/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "symbol": "AAPL",
  "peers": [
    "MSFT",
    "GOOG",
    "META"
  ]
}
```

## 文档正文

Returns a list of peer/comparable company symbols for the given security

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/peers/{identifier}`
