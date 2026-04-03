---
id: "url-196661a6"
type: "api"
title: "Forex List API"
url: "https://eulerpool.com/developers/api/forex/list"
description: "Returns a list of all available base currencies for forex rates"
source: ""
tags: []
crawl_time: "2026-03-18T05:29:01.334Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/forex/list"
  responses:
    - {"code":"200","description":"Returns list of available base currencies"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/forex/list' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "forex_list"
---

# Forex List API

## 源URL

https://eulerpool.com/developers/api/forex/list

## 描述

Returns a list of all available base currencies for forex rates

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/forex/list`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns list of available base currencies |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/forex/list' \
  -H 'Accept: application/json'
```

## 文档正文

Returns a list of all available base currencies for forex rates

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/forex/list`
