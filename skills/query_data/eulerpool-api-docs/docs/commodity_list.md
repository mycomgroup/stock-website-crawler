---
id: "url-61ff91d5"
type: "api"
title: "Commodities List API"
url: "https://eulerpool.com/developers/api/commodity/list"
description: "Returns a list of all available commodities with their current prices and metadata"
source: ""
tags: []
crawl_time: "2026-03-18T05:49:45.283Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/commodity/list"
  responses:
    - {"code":"200","description":"Returns commodity list"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/commodity/list' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "commodity_list"
---

# Commodities List API

## 源URL

https://eulerpool.com/developers/api/commodity/list

## 描述

Returns a list of all available commodities with their current prices and metadata

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/commodity/list`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns commodity list |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/commodity/list' \
  -H 'Accept: application/json'
```

## 文档正文

Returns a list of all available commodities with their current prices and metadata

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/commodity/list`
