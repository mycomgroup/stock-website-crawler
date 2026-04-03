---
id: "url-5fe5eb3c"
type: "api"
title: "Available Countries API"
url: "https://eulerpool.com/developers/api/macro/countries"
description: "Returns all countries with available macro economic data, including country name, code, and URL slug"
source: ""
tags: []
crawl_time: "2026-03-18T05:53:04.946Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/countries"
  responses:
    - {"code":"200","description":"Returns country list"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/countries' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "macro_countries"
---

# Available Countries API

## 源URL

https://eulerpool.com/developers/api/macro/countries

## 描述

Returns all countries with available macro economic data, including country name, code, and URL slug

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/countries`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns country list |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/countries' \
  -H 'Accept: application/json'
```

## 文档正文

Returns all countries with available macro economic data, including country name, code, and URL slug

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/countries`
