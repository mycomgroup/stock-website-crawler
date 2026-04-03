---
id: "url-ea30912"
type: "api"
title: "Commodity Profile API"
url: "https://eulerpool.com/developers/api/commodity/profile"
description: "Returns profile information for a commodity (Gold, Crude Oil, Silver, Natural Gas, etc.)"
source: ""
tags: []
crawl_time: "2026-03-18T05:31:22.582Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/commodity/profile/{ticker}"
  responses:
    - {"code":"200","description":"Returns commodity profile"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Commodity not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/commodity/profile/XAU' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "commodity_profile"
---

# Commodity Profile API

## 源URL

https://eulerpool.com/developers/api/commodity/profile

## 描述

Returns profile information for a commodity (Gold, Crude Oil, Silver, Natural Gas, etc.)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/commodity/profile/{ticker}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns commodity profile |
| 401 | Token not valid |
| 404 | Commodity not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/commodity/profile/XAU' \
  -H 'Accept: application/json'
```

## 文档正文

Returns profile information for a commodity (Gold, Crude Oil, Silver, Natural Gas, etc.)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/commodity/profile/{ticker}`
