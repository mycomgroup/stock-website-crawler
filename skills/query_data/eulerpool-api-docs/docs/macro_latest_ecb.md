---
id: "url-2dfde68c"
type: "api"
title: "ECB Latest Values API"
url: "https://eulerpool.com/developers/api/macro/latest/ecb"
description: "Returns the latest observation for all ECB series -- snapshot of European rates, inflation, and monetary conditions"
source: ""
tags: []
crawl_time: "2026-03-18T05:56:02.251Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/latest/ecb"
  responses:
    - {"code":"200","description":"Returns latest ECB values"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/latest/ecb' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "macro_latest_ecb"
---

# ECB Latest Values API

## 源URL

https://eulerpool.com/developers/api/macro/latest/ecb

## 描述

Returns the latest observation for all ECB series -- snapshot of European rates, inflation, and monetary conditions

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/latest/ecb`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns latest ECB values |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/latest/ecb' \
  -H 'Accept: application/json'
```

## 文档正文

Returns the latest observation for all ECB series -- snapshot of European rates, inflation, and monetary conditions

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/latest/ecb`
